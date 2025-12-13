"""
Example 02: Custom Exception Handler

Bu file'da global exception handler yaratish va sozlashni ko'ramiz.

Topics:
- DRF default exception handler
- Custom exception handler
- Response formatting
- Logging integration
- Context information
- Environment-based handling
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
import logging
import sys
import traceback

logger = logging.getLogger(__name__)


# ============================================
# 1. SIMPLE CUSTOM EXCEPTION HANDLER
# ============================================

def simple_exception_handler(exc, context):
    """
    Simple custom exception handler
    
    Wraps DRF default handler and adds custom fields
    """
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Add custom fields to response
        response.data['status'] = 'error'
        response.data['error_type'] = exc.__class__.__name__
    
    return response


# ============================================
# 2. DETAILED EXCEPTION HANDLER
# ============================================

def detailed_exception_handler(exc, context):
    """
    Detailed exception handler with structured error format
    
    Returns:
    {
        "status": "error",
        "error": {
            "type": "ValidationError",
            "message": "Validation failed",
            "code": "validation_error",
            "details": {...}
        }
    }
    """
    # Get DRF response
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
        
        # Create custom response structure
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


# ============================================
# 3. COMPREHENSIVE EXCEPTION HANDLER
# ============================================

def comprehensive_exception_handler(exc, context):
    """
    Comprehensive exception handler with:
    - Logging
    - Context information
    - Stack trace (in DEBUG mode)
    - User-friendly messages
    """
    from django.conf import settings
    
    # Get request and view
    request = context.get('request')
    view = context.get('view')
    
    # Call DRF handler
    response = exception_handler(exc, context)
    
    # Handle unhandled exceptions
    if response is None:
        # Log unexpected error
        logger.critical(
            f"Unhandled exception: {exc.__class__.__name__}",
            exc_info=sys.exc_info(),
            extra={
                'request': request,
                'view': view,
            }
        )
        
        # Create error response
        response = Response(
            {
                'status': 'error',
                'error': {
                    'type': 'InternalServerError',
                    'message': 'An unexpected error occurred',
                    'code': 'internal_error'
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Add custom error structure
    if response is not None:
        # Base error info
        error_data = {
            'status': 'error',
            'error': {
                'type': exc.__class__.__name__,
                'message': str(exc),
                'code': getattr(exc, 'default_code', 'error'),
            }
        }
        
        # Add original error details
        if hasattr(response, 'data'):
            error_data['error']['details'] = response.data
        
        # Add timestamp
        from datetime import datetime
        error_data['timestamp'] = datetime.now().isoformat()
        
        # Add request info
        if request:
            error_data['path'] = request.path
            error_data['method'] = request.method
        
        # Add stack trace in DEBUG mode
        if settings.DEBUG:
            error_data['error']['traceback'] = traceback.format_exc()
        
        response.data = error_data
    
    return response


# ============================================
# 4. ENVIRONMENT-AWARE EXCEPTION HANDLER
# ============================================

def environment_aware_exception_handler(exc, context):
    """
    Different error details for development vs production
    """
    from django.conf import settings
    
    response = exception_handler(exc, context)
    
    if response is not None:
        # Development: Full error details
        if settings.DEBUG:
            error_data = {
                'status': 'error',
                'error': {
                    'type': exc.__class__.__name__,
                    'message': str(exc),
                    'code': getattr(exc, 'default_code', 'error'),
                    'details': response.data,
                    'traceback': traceback.format_exc(),
                    'context': {
                        'view': str(context.get('view')),
                        'request': {
                            'method': context.get('request').method,
                            'path': context.get('request').path,
                            'user': str(context.get('request').user),
                        }
                    }
                }
            }
        
        # Production: Minimal error details
        else:
            error_data = {
                'status': 'error',
                'error': {
                    'message': 'An error occurred',
                    'code': getattr(exc, 'default_code', 'error'),
                }
            }
            
            # Only show details for client errors (4xx)
            if 400 <= response.status_code < 500:
                error_data['error']['message'] = str(exc)
                error_data['error']['details'] = response.data
        
        response.data = error_data
    
    return response


# ============================================
# 5. EXCEPTION HANDLER WITH NOTIFICATIONS
# ============================================

def notifying_exception_handler(exc, context):
    """
    Exception handler that sends notifications for critical errors
    """
    response = exception_handler(exc, context)
    
    # Send notification for 5xx errors
    if response is not None and response.status_code >= 500:
        # Log critical error
        logger.critical(
            f"Critical error: {exc.__class__.__name__}: {str(exc)}",
            exc_info=True,
            extra={'context': context}
        )
        
        # Send notification (email, Slack, etc.)
        send_error_notification(exc, context)
    
    # Format response
    if response is not None:
        response.data = {
            'status': 'error',
            'error': {
                'type': exc.__class__.__name__,
                'message': str(exc),
                'code': getattr(exc, 'default_code', 'error')
            }
        }
    
    return response


def send_error_notification(exc, context):
    """
    Send error notification via email/Slack
    """
    # Implementation: Send email or Slack message
    pass


# ============================================
# 6. HANDLING DJANGO CORE EXCEPTIONS
# ============================================

def django_exception_handler(exc, context):
    """
    Handle both DRF and Django core exceptions
    """
    # Handle Django's ObjectDoesNotExist
    if isinstance(exc, ObjectDoesNotExist):
        exc = Http404()
    
    # Handle Django's PermissionDenied
    elif isinstance(exc, PermissionDenied):
        from rest_framework.exceptions import PermissionDenied as DRFPermissionDenied
        exc = DRFPermissionDenied()
    
    # Call DRF handler
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data = {
            'status': 'error',
            'error': {
                'type': exc.__class__.__name__,
                'message': str(exc),
                'code': getattr(exc, 'default_code', 'error')
            }
        }
    
    return response


# ============================================
# 7. EXCEPTION HANDLER WITH SENTRY
# ============================================

def sentry_exception_handler(exc, context):
    """
    Exception handler with Sentry integration
    """
    import sentry_sdk
    
    # Send to Sentry
    with sentry_sdk.push_scope() as scope:
        # Add context
        scope.set_context("request", {
            "url": context.get('request').build_absolute_uri(),
            "method": context.get('request').method,
            "user": str(context.get('request').user),
        })
        
        scope.set_context("view", {
            "name": context.get('view').__class__.__name__,
        })
        
        # Capture exception
        sentry_sdk.capture_exception(exc)
    
    # Continue with normal handling
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data = {
            'status': 'error',
            'error': {
                'type': exc.__class__.__name__,
                'message': str(exc),
                'code': getattr(exc, 'default_code', 'error')
            }
        }
    
    return response


# ============================================
# 8. USAGE IN SETTINGS.PY
# ============================================

"""
# settings.py

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'path.to.comprehensive_exception_handler',
}

# Different handlers for different environments
if DEBUG:
    REST_FRAMEWORK['EXCEPTION_HANDLER'] = 'path.to.detailed_exception_handler'
else:
    REST_FRAMEWORK['EXCEPTION_HANDLER'] = 'path.to.environment_aware_exception_handler'
"""


# ============================================
# 9. TESTING EXCEPTION HANDLERS
# ============================================

def test_exception_handlers():
    """Test different exception handlers"""
    
    from rest_framework.exceptions import ValidationError, NotFound
    
    print("=" * 60)
    print("TESTING EXCEPTION HANDLERS")
    print("=" * 60)
    
    # Mock context
    class MockRequest:
        method = 'POST'
        path = '/api/v2/books/'
        user = 'testuser'
    
    class MockView:
        pass
    
    context = {
        'request': MockRequest(),
        'view': MockView()
    }
    
    # Test 1: Validation Error
    print("\n1. Testing ValidationError:")
    exc = ValidationError({'isbn': 'This field is required'})
    response = detailed_exception_handler(exc, context)
    if response:
        print(f"   Status: {response.status_code}")
        print(f"   Data: {response.data}")
    
    # Test 2: Not Found Error
    print("\n2. Testing NotFound:")
    exc = NotFound('Book not found')
    response = comprehensive_exception_handler(exc, context)
    if response:
        print(f"   Status: {response.status_code}")
        print(f"   Data: {response.data}")
    
    print("\n" + "=" * 60)
    print("TESTS COMPLETED!")
    print("=" * 60)


# ============================================
# BEST PRACTICES
# ============================================

"""
BEST PRACTICES FOR EXCEPTION HANDLERS:

1.  Always call DRF's default handler first
2.  Return None for unhandled exceptions to let Django handle them
3.  Log all errors with appropriate levels
4.  Use consistent error response format
5.  Include error codes for programmatic handling
6.  Show detailed errors only in DEBUG mode
7.  Send notifications for critical errors
8.  Integrate with error tracking (Sentry)
9.  Add request context to errors
10.  Test your exception handler thoroughly
"""


# ============================================
# RUN TESTS
# ============================================

if __name__ == '__main__':
    test_exception_handlers()