"""
Error Handling Examples - Overview

Bu file barcha error handling concepts'ning qisqa overview'ini beradi.
"""

# ============================================
# 1. CUSTOM EXCEPTIONS
# ============================================

from rest_framework.exceptions import APIException
from rest_framework import status
from books.models import Book
from rest_framework import viewsets
from books.serializers import BookSerializer
from rest_framework.exceptions import ValidationError


class BookNotAvailableError(APIException):
    """Custom exception when book is not available"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Book is not available for borrowing'
    default_code = 'book_not_available'


# Usage in views
def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if not book.available:
        raise BookNotAvailableError(
            detail=f"Book '{book.title}' is currently unavailable"
        )
    # Borrowing logic...


# ============================================
# 2. EXCEPTION HANDLER
# ============================================

from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """
    Custom exception handler for consistent error responses
    """
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
# 3. LOGGING
# ============================================

import logging

logger = logging.getLogger(__name__)


def create_book(request):
    logger.info(f"Creating book: {request.data.get('title')}")
    
    try:
        book = Book.objects.create(**request.data)
        logger.info(f"Book created successfully: {book.id}")
        return Response({'id': book.id})
    
    except Exception as e:
        logger.error(f"Error creating book: {str(e)}", exc_info=True)
        raise


# ============================================
# 4. SENTRY
# ============================================

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Initialize Sentry
sentry_sdk.init(
    dsn="https://your-dsn@sentry.io/project-id",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    environment="development"
)


# Capture custom error
def risky_operation():
    try:
        # Some risky code
        result = 1 / 0
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise


# ============================================
# COMPLETE EXAMPLE
# ============================================

class BookViewSet(viewsets.ModelViewSet):
    """
    Book ViewSet with complete error handling
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def create(self, request, *args, **kwargs):
        # Logging
        logger.info(f"User {request.user} creating book")
        
        try:
            # Validation
            if not request.data.get('isbn'):
                raise ValidationError({'isbn': 'ISBN is required'})
            
            # Create book
            response = super().create(request, *args, **kwargs)
            
            # Success logging
            logger.info(f"Book created: {response.data['id']}")
            
            return response
            
        except ValidationError as e:
            # Log validation errors
            logger.warning(f"Validation error: {e.detail}")
            raise
            
        except Exception as e:
            # Log unexpected errors
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            
            # Send to Sentry
            sentry_sdk.capture_exception(e)
            
            # Re-raise
            raise APIException('An unexpected error occurred')


# ============================================
# TESTING ERROR HANDLING
# ============================================

def test_error_handling():
    """
    Test different error scenarios
    """
    
    # Test 1: Custom exception
    try:
        raise BookNotAvailableError()
    except BookNotAvailableError as e:
        print(f"✓ Custom exception: {e}")
    
    # Test 2: Logging
    logger.info("Test log message")
    logger.error("Test error message")
    
    # Test 3: Sentry (if configured)
    try:
        1 / 0
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print("✓ Error sent to Sentry")


if __name__ == '__main__':
    print("=" * 50)
    print("ERROR HANDLING EXAMPLES")
    print("=" * 50)
    test_error_handling()