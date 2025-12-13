"""
Example 03: Logging in Django REST Framework

Bu file'da Django logging configuration va foydalanishni ko'ramiz.

Topics:
- Python logging module
- Django logging configuration
- Log levels
- Multiple log files
- Log rotation
- Custom formatters
- Context logging
"""

import logging
from books.models import Book
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


# ============================================
# 1. BASIC LOGGING USAGE
# ============================================

# Get logger
logger = logging.getLogger(__name__)

def basic_logging_example():
    """Basic logging examples"""
    
    # Different log levels
    logger.debug("Debug message - detailed information")
    logger.info("Info message - general information")
    logger.warning("Warning message - something unexpected")
    logger.error("Error message - error occurred")
    logger.critical("Critical message - serious error")


# ============================================
# 2. LOGGING IN VIEWS
# ============================================

def logging_in_views_example():
    """How to use logging in views"""
    
    class BookViewSet:
        def create(self, request):
            # Log incoming request
            logger.info(
                f"Creating book: {request.data.get('title')}",
                extra={
                    'user': request.user.username,
                    'ip': request.META.get('REMOTE_ADDR')
                }
            )
            
            try:
                # Create book
                book = Book.objects.create(**request.data)
                
                # Log success
                logger.info(
                    f"Book created successfully: ID={book.id}",
                    extra={'book_id': book.id}
                )
                
                return Response({'id': book.id})
                
            except ValidationError as e:
                # Log validation error
                logger.warning(
                    f"Validation error: {e.detail}",
                    extra={'errors': e.detail}
                )
                raise
                
            except Exception as e:
                # Log unexpected error
                logger.error(
                    f"Unexpected error creating book: {str(e)}",
                    exc_info=True,  # Include traceback
                    extra={
                        'user': request.user.username,
                        'data': request.data
                    }
                )
                raise


# ============================================
# 3. DJANGO LOGGING CONFIGURATION
# ============================================

LOGGING_CONFIG_BASIC = {
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
    
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
            'formatter': 'verbose',
        },
    },
    
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}


# ============================================
# 4. ADVANCED LOGGING CONFIGURATION
# ============================================

LOGGING_CONFIG_ADVANCED = {
    'version': 1,
    'disable_existing_loggers': False,
    
    # ========================================
    # FORMATTERS
    # ========================================
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
    },
    
    # ========================================
    # FILTERS
    # ========================================
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    
    # ========================================
    # HANDLERS
    # ========================================
    'handlers': {
        # Console output (only in DEBUG)
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        
        # General application log
        'file_app': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        
        # Error log
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/errors.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        
        # API log
        'file_api': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/api.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        
        # Daily rotating log
        'file_daily': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/daily.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,  # Keep 30 days
            'formatter': 'verbose',
        },
        
        # Email for critical errors (Production)
        'mail_admins': {
            'level': 'CRITICAL',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
    },
    
    # ========================================
    # LOGGERS
    # ========================================
    'loggers': {
        # Django core
        'django': {
            'handlers': ['console', 'file_app', 'file_errors'],
            'level': 'INFO',
            'propagate': False,
        },
        
        # Django requests
        'django.request': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        
        # Django database queries (DEBUG only)
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        
        # Books app
        'books': {
            'handlers': ['console', 'file_api', 'file_errors'],
            'level': 'INFO',
            'propagate': False,
        },
        
        # Accounts app
        'accounts': {
            'handlers': ['console', 'file_api', 'file_errors'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    
    # ========================================
    # ROOT LOGGER
    # ========================================
    'root': {
        'handlers': ['console', 'file_app'],
        'level': 'INFO',
    },
}


# ============================================
# 5. CUSTOM LOG FORMATTER
# ============================================

class CustomFormatter(logging.Formatter):
    """
    Custom formatter with colors for console output
    """
    
    # ANSI color codes
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    
    format_string = "%(levelname)s %(asctime)s %(name)s - %(message)s"
    
    FORMATS = {
        logging.DEBUG: grey + format_string + reset,
        logging.INFO: grey + format_string + reset,
        logging.WARNING: yellow + format_string + reset,
        logging.ERROR: red + format_string + reset,
        logging.CRITICAL: bold_red + format_string + reset
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)


# ============================================
# 6. CONTEXT LOGGING
# ============================================

class ContextLogger:
    """
    Logger with automatic context information
    """
    
    def __init__(self, name):
        self.logger = logging.getLogger(name)
    
    def log_with_context(self, level, message, request=None, **extra):
        """Log with automatic context"""
        
        context = {}
        
        # Add request context
        if request:
            context.update({
                'user': getattr(request.user, 'username', 'anonymous'),
                'ip': request.META.get('REMOTE_ADDR'),
                'method': request.method,
                'path': request.path,
                'user_agent': request.META.get('HTTP_USER_AGENT'),
            })
        
        # Add timestamp
        context['timestamp'] = datetime.now().isoformat()
        
        # Merge with extra context
        context.update(extra)
        
        # Log with context
        self.logger.log(level, message, extra=context)
    
    def info(self, message, request=None, **extra):
        self.log_with_context(logging.INFO, message, request, **extra)
    
    def error(self, message, request=None, exc_info=False, **extra):
        self.log_with_context(logging.ERROR, message, request, **extra)
        if exc_info:
            self.logger.exception(message)


# ============================================
# 7. PERFORMANCE LOGGING
# ============================================

import time
from functools import wraps

def log_performance(logger_name='performance'):
    """
    Decorator to log function execution time
    """
    def decorator(func):
        logger = logging.getLogger(logger_name)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                logger.info(
                    f"{func.__name__} executed successfully",
                    extra={
                        'function': func.__name__,
                        'execution_time': f"{execution_time:.4f}s",
                        'status': 'success'
                    }
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                logger.error(
                    f"{func.__name__} failed",
                    extra={
                        'function': func.__name__,
                        'execution_time': f"{execution_time:.4f}s",
                        'status': 'error',
                        'error': str(e)
                    },
                    exc_info=True
                )
                raise
        
        return wrapper
    return decorator


# Usage example
@log_performance()
def expensive_operation():
    """Simulate expensive operation"""
    time.sleep(2)
    return "Done"


# ============================================
# 8. STRUCTURED LOGGING
# ============================================

class StructuredLogger:
    """
    Structured logging with consistent format
    """
    
    def __init__(self, name):
        self.logger = logging.getLogger(name)
    
    def log_event(self, event_type, message, **context):
        """Log structured event"""
        
        log_data = {
            'event_type': event_type,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            **context
        }
        
        self.logger.info(message, extra=log_data)
    
    def log_api_request(self, request, response, duration):
        """Log API request"""
        
        self.log_event(
            event_type='api_request',
            message=f"{request.method} {request.path}",
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            duration_ms=duration * 1000,
            user=getattr(request.user, 'username', 'anonymous'),
            ip=request.META.get('REMOTE_ADDR'),
        )
    
    def log_database_query(self, query, duration):
        """Log database query"""
        
        self.log_event(
            event_type='database_query',
            message='Database query executed',
            query=query,
            duration_ms=duration * 1000,
        )
    
    def log_error(self, error, context=None):
        """Log error with context"""
        
        self.log_event(
            event_type='error',
            message=str(error),
            error_type=error.__class__.__name__,
            context=context or {},
        )


# ============================================
# 9. LOG ROTATION EXAMPLES
# ============================================

def setup_rotating_file_handler():
    """Setup rotating file handler"""
    
    handler = RotatingFileHandler(
        filename='logs/app.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,  # Keep 5 backup files
        encoding='utf-8'
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    logger = logging.getLogger('app')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger


def setup_timed_rotating_handler():
    """Setup timed rotating handler (daily)"""
    
    handler = TimedRotatingFileHandler(
        filename='logs/daily.log',
        when='midnight',  # Rotate at midnight
        interval=1,  # Every day
        backupCount=30,  # Keep 30 days
        encoding='utf-8'
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    logger = logging.getLogger('daily')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger


# ============================================
# 10. TESTING LOGGING
# ============================================

def test_logging():
    """Test logging functionality"""
    
    print("=" * 60)
    print("TESTING LOGGING")
    print("=" * 60)
    
    # Basic logging
    print("\n1. Basic Logging:")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    # Logging with extra context
    print("\n2. Logging with Context:")
    logger.info(
        "User action",
        extra={
            'user': 'john_doe',
            'action': 'create_book',
            'book_id': 123
        }
    )
    
    # Exception logging
    print("\n3. Exception Logging:")
    try:
        result = 1 / 0
    except Exception as e:
        logger.error("Division error", exc_info=True)
    
    # Context logger
    print("\n4. Context Logger:")
    context_logger = ContextLogger('books')
    context_logger.info("Book created", book_id=456, title="Django Basics")
    
    # Performance logging
    print("\n5. Performance Logging:")
    result = expensive_operation()
    
    # Structured logging
    print("\n6. Structured Logging:")
    struct_logger = StructuredLogger('api')
    struct_logger.log_event(
        event_type='user_login',
        message='User logged in',
        user_id=789,
        ip='192.168.1.1'
    )
    
    print("\n" + "=" * 60)
    print("LOGGING TESTS COMPLETED!")
    print("=" * 60)


# ============================================
# BEST PRACTICES
# ============================================

"""
BEST PRACTICES FOR LOGGING:

1.  Use appropriate log levels:
   - DEBUG: Detailed diagnostic information
   - INFO: General informational messages
   - WARNING: Warning messages for potentially harmful situations
   - ERROR: Error messages for serious problems
   - CRITICAL: Critical messages for very serious errors

2.  Log levels in different environments:
   - Development: DEBUG
   - Staging: INFO
   - Production: WARNING or ERROR

3.  Use structured logging with context

4.  Implement log rotation to manage file size

5.  Separate logs by purpose (api.log, errors.log, etc.)

6.  Include relevant context (user, request, timestamp)

7.  Use exc_info=True for exceptions to include traceback

8.  Don't log sensitive information (passwords, tokens)

9.  Use different handlers for different environments

10.  Monitor and analyze logs regularly
"""


# ============================================
# RUN TESTS
# ============================================

if __name__ == '__main__':
    # Configure basic logging for testing
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s %(asctime)s %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    test_logging()