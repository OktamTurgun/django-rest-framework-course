"""
Custom Exception Handler for Library Management System

This module provides a global exception handler that:
- Returns consistent error responses
- Logs all errors appropriately
- Adds context information
- Handles both DRF and Django core exceptions
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError as DjangoValidationError
from django.http import Http404
from datetime import datetime
import logging
import sys
import traceback

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for consistent error responses
    
    Returns error in format:
    {
        "status": "error",
        "error": {
            "type": "ErrorType",
            "message": "Error message",
            "code": "error_code",
            "details": {...}
        },
        "timestamp": "2024-12-12T15:30:00",
        "path": "/api/v2/books/",
        "method": "POST"
    }
    """
    from django.conf import settings
    
    # Get request and view from context
    request = context.get('request')
    view = context.get('view')
    
    # Handle Django core exceptions
    exc = convert_django_exceptions(exc)
    
    # Call DRF's default exception handler
    response = exception_handler(exc, context)
    
    # Handle unhandled exceptions (500 errors)
    if response is None:
        response = handle_unhandled_exception(exc, context)
    
    # Customize response format
    if response is not None:
        response = format_error_response(exc, response, request, context)
    
    # Log the error
    log_exception(exc, context, response)
    
    return response


def convert_django_exceptions(exc):
    """
    Convert Django core exceptions to DRF exceptions
    """
    from rest_framework.exceptions import NotFound, PermissionDenied as DRFPermissionDenied, ValidationError
    
    # Convert ObjectDoesNotExist to NotFound
    if isinstance(exc, ObjectDoesNotExist):
        return NotFound(detail=str(exc))
    
    # Convert Django PermissionDenied to DRF PermissionDenied
    if isinstance(exc, PermissionDenied):
        return DRFPermissionDenied(detail=str(exc))
    
    # Convert Django ValidationError to DRF ValidationError
    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, 'message_dict'):
            return ValidationError(detail=exc.message_dict)
        return ValidationError(detail={'detail': exc.messages})
    
    return exc


def handle_unhandled_exception(exc, context):
    """
    Handle exceptions not caught by DRF
    """
    logger.critical(
        f"Unhandled exception: {exc.__class__.__name__}: {str(exc)}",
        exc_info=sys.exc_info(),
        extra={
            'view': str(context.get('view')),
            'request': {
                'method': context.get('request').method if context.get('request') else None,
                'path': context.get('request').path if context.get('request') else None,
            }
        }
    )
    
    # Return generic 500 error
    return Response(
        {
            'status': 'error',
            'error': {
                'type': 'InternalServerError',
                'message': 'An unexpected error occurred. Our team has been notified.',
                'code': 'internal_error'
            }
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def format_error_response(exc, response, request, context):
    """
    Format error response with consistent structure
    """
    from django.conf import settings
    import uuid
    
    # Base error structure
    error_data = {
        'status': 'error',
        'error': {
            'type': exc.__class__.__name__,
            'message': str(exc),
            'code': getattr(exc, 'default_code', 'error'),
        },
        'timestamp': datetime.now().isoformat(),
    }
    
    # Add request information
    if request:
        error_data['path'] = request.path
        error_data['method'] = request.method
    
    # Add error details from DRF response
    if hasattr(response, 'data') and response.data:
        error_data['error']['details'] = response.data
    
    # ========================================
    # DEBUG MODE: Show detailed info
    # ========================================
    if settings.DEBUG:
        error_data['error']['traceback'] = traceback.format_exc()
        error_data['error']['context'] = {
            'view': str(context.get('view')),
            'args': context.get('args'),
            'kwargs': context.get('kwargs'),
        }
    # ========================================
    # PRODUCTION MODE: Show error ID
    # ========================================
    else:
        # Generate unique error ID for support
        error_id = str(uuid.uuid4())
        error_data['error']['error_id'] = error_id
        
        # Log error ID for tracking
        logger.error(
            f"Error ID: {error_id} - {exc.__class__.__name__}",
            extra={'error_id': error_id}
        )
        
        # For 5xx errors, show generic message
        if response and response.status_code >= 500:
            error_data['error']['message'] = (
                'An unexpected error occurred. '
                f'Please contact support with error ID: {error_id}'
            )
    
    # Add retry_after for rate limiting
    if hasattr(exc, 'retry_after'):
        error_data['retry_after'] = exc.retry_after
        response['Retry-After'] = exc.retry_after
    
    response.data = error_data
    return response

def log_exception(exc, context, response):
    """
    Log exception with appropriate level
    """
    request = context.get('request')
    view = context.get('view')
    
    # Determine log level based on status code
    if response:
        status_code = response.status_code
        
        if status_code >= 500:
            log_level = logging.ERROR
        elif status_code >= 400:
            log_level = logging.WARNING
        else:
            log_level = logging.INFO
    else:
        log_level = logging.ERROR
    
    # Create log message
    log_message = f"{exc.__class__.__name__}: {str(exc)}"
    
    # Extra context for logging
    extra_context = {
        'exception_type': exc.__class__.__name__,
        'status_code': response.status_code if response else 500,
    }
    
    if request:
        extra_context.update({
            'method': request.method,
            'path': request.path,
            'user': str(request.user) if hasattr(request, 'user') else 'anonymous',
            'ip': request.META.get('REMOTE_ADDR'),
        })
    
    if view:
        extra_context['view'] = view.__class__.__name__
    
    # Log with context
    logger.log(
        log_level,
        log_message,
        extra=extra_context,
        exc_info=(log_level >= logging.ERROR)
    )