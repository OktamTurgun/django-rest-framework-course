# Homework: Error Handling Implementation

##  Vazifa

Library Management System'ga professional error handling qo'shing.

---

##  Tasks

### Part 1: Custom Exceptions (30 points)

#### 1.1 Business Logic Exceptions (10 points)

`books/exceptions.py` faylida quyidagi exception'larni yarating:
```python
class BookNotAvailableError(Exception):
    """Raised when book is not available for borrowing"""
    pass

class BookAlreadyBorrowedError(Exception):
    """Raised when user tries to borrow already borrowed book"""
    pass

class MaxBorrowLimitExceededError(Exception):
    """Raised when user exceeds max borrow limit"""
    pass

class InvalidISBNError(Exception):
    """Raised when ISBN format is invalid"""
    pass

class AuthorLimitExceededError(Exception):
    """Raised when author has too many books"""
    pass
```

**Requirements:**
-  Clear docstrings
-  Descriptive names
-  Inherit from appropriate base classes

---

#### 1.2 API Exceptions (10 points)
```python
from rest_framework.exceptions import APIException
from rest_framework import status

class ResourceNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Resource not found'
    default_code = 'not_found'

class PermissionDeniedError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Permission denied'
    default_code = 'permission_denied'

class RateLimitExceededError(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = 'Rate limit exceeded'
    default_code = 'rate_limit_exceeded'
```

---

#### 1.3 Use Exceptions in Views (10 points)

Views'da exception'larni ishlatish:
```python
def borrow_book(self, request, pk=None):
    book = self.get_object()
    
    # Check availability
    if not book.is_available:
        raise BookNotAvailableError(
            f"Book '{book.title}' is currently not available"
        )
    
    # Check user's borrow limit
    user_borrowed_count = request.user.borrowed_books.count()
    if user_borrowed_count >= 5:
        raise MaxBorrowLimitExceededError(
            f"You have reached the maximum borrow limit (5 books)"
        )
    
    # Borrow logic...
```

---

### Part 2: Exception Handler (30 points)

#### 2.1 Global Exception Handler (20 points)

`library_project/exception_handler.py`:
```python
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler
    
    Returns consistent error format:
    {
        "status": "error",
        "error": {
            "type": "ErrorType",
            "message": "Error message",
            "code": "error_code",
            "details": {...}
        }
    }
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        # Log the error
        logger.error(
            f"{exc.__class__.__name__}: {str(exc)}",
            extra={
                'view': context.get('view'),
                'request': context.get('request'),
            }
        )
        
        # Custom response format
        custom_response = {
            'status': 'error',
            'error': {
                'type': exc.__class__.__name__,
                'message': str(exc),
                'code': getattr(exc, 'default_code', 'error'),
                'details': response.data
            }
        }
        
        response.data = custom_response
    
    return response
```

**Requirements:**
-  Consistent error format
-  Logging integration
-  Context information
-  Error type and code

---

#### 2.2 Settings Configuration (10 points)

`settings.py`:
```python
REST_FRAMEWORK = {
    # ...
    'EXCEPTION_HANDLER': 'library_project.exception_handler.custom_exception_handler',
}
```

---

### Part 3: Logging Configuration (25 points)

#### 3.1 Logging Setup (15 points)

`library_project/settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/errors.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'file_api': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/api.log',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_errors'],
            'level': 'INFO',
            'propagate': False,
        },
        'books': {
            'handlers': ['console', 'file_api', 'file_errors'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

**Requirements:**
-  Multiple handlers (console, file)
-  Different log levels
-  Log rotation
-  Custom formatters

---

#### 3.2 Use Logging in Views (10 points)
```python
import logging

logger = logging.getLogger(__name__)

class BookViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        logger.info(f"Creating new book: {request.data.get('title')}")
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"Book created successfully: ID {response.data['id']}")
            return response
        except Exception as e:
            logger.error(f"Error creating book: {str(e)}", exc_info=True)
            raise
```

---

### Part 4: Sentry Integration (15 points)

#### 4.1 Installation (5 points)
```bash
pip install sentry-sdk
```

---

#### 4.2 Configuration (10 points)

`settings.py`:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
    environment="development",  # or "production"
)
```

**Requirements:**
-  Proper DSN configuration
-  Django integration
-  Environment setup
-  PII configuration

---

##  Testing Requirements

### Test 1: Custom Exception
```bash
POST /api/v2/books/1/borrow/
# Book not available

Expected Response:
{
    "status": "error",
    "error": {
        "type": "BookNotAvailableError",
        "message": "Book 'Django Basics' is currently not available",
        "code": "book_not_available"
    }
}
```

### Test 2: Validation Error
```bash
POST /api/v2/books/
{
    "title": "",
    "price": -10
}

Expected Response:
{
    "status": "error",
    "error": {
        "type": "ValidationError",
        "code": "validation_error",
        "details": {
            "title": ["This field may not be blank"],
            "price": ["Price must be positive"]
        }
    }
}
```

### Test 3: Logging
```bash
# Check logs/api.log
[INFO] 2024-12-12 15:30:45 Creating new book: Django Advanced
[INFO] 2024-12-12 15:30:46 Book created successfully: ID 128

# Check logs/errors.log
[ERROR] 2024-12-12 15:31:00 BookNotAvailableError: Book ID 1 not available
```

### Test 4: Sentry
- Trigger error
- Check Sentry dashboard
- Verify error details

---

##  Grading Rubric

| Task | Points | Criteria |
|------|--------|----------|
| Custom Exceptions | 30 | All exceptions created and documented |
| Exception Handler | 30 | Working handler with consistent format |
| Logging | 25 | Complete logging configuration |
| Sentry Integration | 15 | Working Sentry integration |
| **Total** | **100** | |

---

##  Submission

1.  All code committed to Git
2.  Postman collection with tests
3.  Screenshot of Sentry dashboard
4.  Sample log files
5.  README with setup instructions

---

##  Bonus Points (+20)

- [ ] Custom error codes system (+5)
- [ ] Error rate monitoring (+5)
- [ ] Slack/Email notifications for critical errors (+5)
- [ ] Error recovery mechanisms (+5)

---

**Deadline:** 1 hafta
**Submission:** Pull Request on GitHub