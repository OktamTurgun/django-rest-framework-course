# Lesson 27: Error Handling in Django REST Framework

##  Maqsad
Django REST Framework'da professional error handling, custom exceptions, logging va real-time error tracking (Sentry) bilan ishlashni o'rganish.

##  Mavzular

### 1. Custom Exceptions (examples_01)
- Business logic exceptions
- HTTP exceptions
- Validation exceptions
- Custom error codes
- User-friendly error messages

### 2. Exception Handler (examples_02)
- Global exception handler
- Custom response format
- Error context
- Stack trace handling
- Different responses for different environments

### 3. Logging Configuration (examples_03)
- Python logging module
- Django logging settings
- Log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Multiple log files
- Log rotation
- Custom formatters

### 4. Sentry Integration (examples_04)
- Installation and setup
- Error tracking
- Performance monitoring
- Release tracking
- User context
- Custom tags and breadcrumbs

##  Amaliy Qism

### Custom Exception Types
```python
# Business Logic Exceptions
class BookNotAvailableError(Exception)
class AuthorLimitExceededError(Exception)
class InvalidISBNError(Exception)

# API Exceptions
class ResourceNotFoundError(APIException)
class PermissionDeniedError(APIException)
class ValidationError(APIException)
```

### Exception Handler
```python
def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns:
    - Error type
    - Error message
    - Error code
    - Context information
    - Stack trace (in DEBUG mode)
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data = {
            'error': {
                'type': exc.__class__.__name__,
                'message': str(exc),
                'code': getattr(exc, 'code', 'error'),
                'details': response.data
            }
        }
    
    return response
```

### Logging Configuration
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/errors.log',
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

##  Response Format

### Success Response
```json
{
    "status": "success",
    "data": {...}
}
```

### Error Response
```json
{
    "status": "error",
    "error": {
        "type": "ValidationError",
        "message": "Invalid input data",
        "code": "validation_error",
        "details": {
            "isbn": ["This field is required"],
            "price": ["Price must be positive"]
        }
    }
}
```

##  Testing

### Test Custom Exceptions
```python
# Test book not available
POST /api/v2/books/1/borrow/
Response: 400 Bad Request
{
    "error": {
        "type": "BookNotAvailableError",
        "message": "This book is currently not available"
    }
}
```

### Test Logging
```python
# Check logs/errors.log
[ERROR] 2024-12-12 15:30:45 views BookNotAvailableError: Book ID 1 not available
```

### Test Sentry
- Trigger an error
- Check Sentry dashboard
- View error details, stack trace, and context

##  Benefits

### Development
-  Clear error messages
-  Easy debugging
-  Consistent error format
-  Detailed logging

### Production
-  Real-time error tracking
-  Error grouping and trends
-  Performance monitoring
-  Quick issue resolution

##  Resources

- [DRF Exception Handling](https://www.django-rest-framework.org/api-guide/exceptions/)
- [Python Logging](https://docs.python.org/3/library/logging.html)
- [Sentry Documentation](https://docs.sentry.io/)
- [Django Logging](https://docs.djangoproject.com/en/5.0/topics/logging/)

##  Homework

1. Create custom exceptions for your business logic
2. Implement global exception handler
3. Configure comprehensive logging
4. Integrate Sentry
5. Test all error scenarios
6. Document error codes

##  Learning Outcomes

O'quvchilar quyidagilarni o'rganadilar:
-  Custom exception yaratish
-  Global exception handler yozish
-  Logging configuration
-  Log rotation va management
-  Sentry integration
-  Production-ready error handling

##  Screenshots

[Error response example]
[Sentry dashboard]
[Log file example]

---

**Next:** [28 - Signals & Webhooks](.lessons/28-signals/)