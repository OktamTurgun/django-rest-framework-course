# Error Handling Implementation

##  Implemented Features

### 1. Custom Exceptions
-  15+ custom exception classes in `books/exceptions.py`
-  Business logic exceptions (BookNotAvailable, ISBNExists, etc.)
-  Validation exceptions (FutureDate, NegativePrice, etc.)
-  Permission exceptions (AdminOnly, NotBookOwner, etc.)
-  Rate limiting exceptions

### 2. Global Exception Handler
-  Custom exception handler in `library_project/exception_handler.py`
-  Consistent error response format
-  Context information (timestamp, path, method)
-  Stack trace in DEBUG mode
-  Automatic logging integration

### 3. Comprehensive Logging
-  Multiple log files (app.log, errors.log, api.log, daily.log)
-  Log rotation (10MB files, 5-10 backups)
-  Different log levels (INFO, WARNING, ERROR, CRITICAL)
-  Structured logging with context
-  Performance logging

### 4. Sentry Integration
-  Sentry SDK installed and configured
-  Automatic error capture
-  User context tracking
-  Performance monitoring
-  Sensitive data filtering
-  Release tracking

##  Error Response Format
```json
{
    "status": "error",
    "error": {
        "type": "ISBNAlreadyExistsError",
        "message": "Book with ISBN 978-1234567890 already exists",
        "code": "isbn_duplicate",
        "details": {...}
    },
    "timestamp": "2024-12-13T10:30:00",
    "path": "/api/v2/books/",
    "method": "POST"
}
```

##  Testing

### Test Custom Exceptions
```bash
# ISBN duplicate
POST /api/v2/books/
{
    "isbn": "existing-isbn",
    ...
}

# Future date
POST /api/v2/books/
{
    "published_date": "2030-01-01",
    ...
}

# Negative price
POST /api/v2/books/
{
    "price": "-10.99",
    ...
}
```

### Test Error Endpoint (Development)
```bash
GET /api/v2/test-errors/?type=isbn_duplicate
GET /api/v2/test-errors/?type=server_error
```

### Check Logs
```bash
# Windows
type logs\errors.log
type logs\api.log

# Linux/Mac
cat logs/errors.log
cat logs/api.log
```

##  Log Files

- **app.log**: General application logs (INFO+)
- **errors.log**: Error logs only (ERROR+)
- **api.log**: API request/response logs
- **daily.log**: Daily rotating log (30 days retention)

##  Configuration

### Environment Variables
```bash
# .env
SENTRY_DSN=https://your-dsn@sentry.io/project-id
ENVIRONMENT=development
RELEASE_VERSION=v1.0.0
```

### Django Settings
```python
# Exception handler
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'library_project.exception_handler.custom_exception_handler',
}

# Logging
LOGGING = {...}

# Sentry
sentry_sdk.init(dsn=SENTRY_DSN, ...)
```

##  Monitoring

### Sentry Dashboard
- View all errors in real-time
- Track performance issues
- Monitor release health
- Set up alerts

### Log Analysis
- Use `grep` or `findstr` to search logs
- Monitor error patterns
- Track API usage
- Identify slow operations

##  Best Practices

1.  Always use custom exceptions for business logic
2.  Log at appropriate levels
3.  Include context in logs
4.  Filter sensitive data
5.  Monitor production errors
6.  Set up alerts for critical errors
7.  Review logs regularly
8.  Keep logs rotated and archived

##  Production Checklist

- [ ] Sentry DSN configured
- [ ] Log files writable
- [ ] Log rotation working
- [ ] Email alerts configured
- [ ] Sensitive data filtered
- [ ] Error rates monitored
- [ ] Team has access to logs
- [ ] Backup strategy for logs