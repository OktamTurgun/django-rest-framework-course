"""
Example 01: Custom Exceptions in Django REST Framework

Bu file'da custom exception'lar yaratish va ulardan foydalanishni ko'ramiz.

Topics:
- Exception class hierarchy
- Custom API exceptions
- Business logic exceptions
- Error codes and messages
- HTTP status codes
"""

from rest_framework.exceptions import APIException
from rest_framework import status
from books.models import Book
from books.validators import validate_isbn_format
from rest_framework import viewsets


# ============================================
# 1. BASIC CUSTOM EXCEPTION
# ============================================

class BookNotFoundError(Exception):
    """
    Basic Python exception for book not found
    
    Usage:
        if not book:
            raise BookNotFoundError("Book with ID 123 not found")
    """
    pass


# ============================================
# 2. API EXCEPTIONS (DRF)
# ============================================

class BookNotAvailableError(APIException):
    """
    DRF API Exception - Book not available
    
    Automatically converts to proper API response with status code
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'This book is currently not available for borrowing'
    default_code = 'book_not_available'


class ISBNAlreadyExistsError(APIException):
    """Book with this ISBN already exists"""
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'A book with this ISBN already exists'
    default_code = 'isbn_duplicate'


class BookLimitExceededError(APIException):
    """User has exceeded book borrowing limit"""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You have reached the maximum number of borrowed books'
    default_code = 'borrow_limit_exceeded'


# ============================================
# 3. BUSINESS LOGIC EXCEPTIONS
# ============================================

class InvalidISBNFormatError(APIException):
    """Invalid ISBN format"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'ISBN format is invalid. Expected: ISBN-13 (978-XXXXXXXXXX)'
    default_code = 'invalid_isbn_format'


class AuthorLimitExceededError(APIException):
    """Author has too many books"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'This author has reached the maximum number of books (100)'
    default_code = 'author_limit_exceeded'


class BookAlreadyReturnedError(APIException):
    """Book already returned"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'This book has already been returned'
    default_code = 'book_already_returned'


class InsufficientStockError(APIException):
    """Not enough books in stock"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Not enough books in stock'
    default_code = 'insufficient_stock'


# ============================================
# 4. PERMISSION EXCEPTIONS
# ============================================

class NotBookOwnerError(APIException):
    """User is not the owner of this borrowed book"""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You are not the owner of this borrowed book'
    default_code = 'not_book_owner'


class AdminOnlyError(APIException):
    """This action requires admin privileges"""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'This action can only be performed by administrators'
    default_code = 'admin_only'


# ============================================
# 5. VALIDATION EXCEPTIONS
# ============================================

class InvalidDateRangeError(APIException):
    """Invalid date range"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Start date must be before end date'
    default_code = 'invalid_date_range'


class FutureDateError(APIException):
    """Date cannot be in the future"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Published date cannot be in the future'
    default_code = 'future_date'


class NegativePriceError(APIException):
    """Price cannot be negative"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Price must be a positive number'
    default_code = 'negative_price'


# ============================================
# 6. RATE LIMITING EXCEPTIONS
# ============================================

class RateLimitExceededError(APIException):
    """Rate limit exceeded"""
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = 'Rate limit exceeded. Please try again later.'
    default_code = 'rate_limit_exceeded'
    
    def __init__(self, retry_after=60):
        super().__init__()
        self.retry_after = retry_after
        self.detail = f'Rate limit exceeded. Retry after {retry_after} seconds.'


class DailyQuotaExceededError(APIException):
    """Daily API quota exceeded"""
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = 'Daily API quota exceeded'
    default_code = 'daily_quota_exceeded'


# ============================================
# 7. EXTERNAL SERVICE EXCEPTIONS
# ============================================

class PaymentServiceError(APIException):
    """Payment service error"""
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = 'Payment service is currently unavailable'
    default_code = 'payment_service_error'


class EmailServiceError(APIException):
    """Email service error"""
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Email service is currently unavailable'
    default_code = 'email_service_error'


# ============================================
# 8. USAGE EXAMPLES
# ============================================

def example_usage_in_views():
    """
    Example: Using custom exceptions in views
    """
    
    # Example 1: Book not available
    def borrow_book(book_id, user):
        book = get_book_or_404(book_id)
        
        if not book.is_available:
            raise BookNotAvailableError(
                detail=f"Book '{book.title}' is currently unavailable"
            )
        
        # Check user's borrow limit
        borrowed_count = user.borrowed_books.count()
        if borrowed_count >= 5:
            raise BookLimitExceededError(
                detail=f"You have {borrowed_count}/5 borrowed books. Please return a book first."
            )
        
        # Borrow logic...
        return book
    
    
    # Example 2: ISBN validation
    def create_book(data):
        isbn = data.get('isbn')
        
        # Check format
        if not validate_isbn_format(isbn):
            raise InvalidISBNFormatError(
                detail=f"Invalid ISBN: {isbn}"
            )
        
        # Check duplicate
        if Book.objects.filter(isbn=isbn).exists():
            raise ISBNAlreadyExistsError(
                detail=f"Book with ISBN {isbn} already exists"
            )
        
        # Create logic...
        return book
    
    
    # Example 3: Date validation
    def update_book(book, data):
        published_date = data.get('published_date')
        
        from datetime import date
        if published_date > date.today():
            raise FutureDateError(
                detail="Published date cannot be in the future"
            )
        
        # Update logic...
        return book
    
    
    # Example 4: Permission check
    def return_book(borrowed_book, user):
        if borrowed_book.user != user:
            raise NotBookOwnerError(
                detail="You can only return books that you borrowed"
            )
        
        if borrowed_book.returned_at:
            raise BookAlreadyReturnedError(
                detail="This book was already returned"
            )
        
        # Return logic...
        return borrowed_book


# ============================================
# 9. EXCEPTION HIERARCHY
# ============================================

class LibraryBaseException(APIException):
    """Base exception for all library-related errors"""
    pass


class BookException(LibraryBaseException):
    """Base exception for book-related errors"""
    pass


class UserException(LibraryBaseException):
    """Base exception for user-related errors"""
    pass


class BookNotAvailable(BookException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Book not available'
    default_code = 'book_not_available'


class BookNotFound(BookException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Book not found'
    default_code = 'book_not_found'


class UserQuotaExceeded(UserException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'User quota exceeded'
    default_code = 'quota_exceeded'


# ============================================
# 10. TESTING CUSTOM EXCEPTIONS
# ============================================

def test_custom_exceptions():
    """Test custom exceptions"""
    
    print("=" * 60)
    print("TESTING CUSTOM EXCEPTIONS")
    print("=" * 60)
    
    # Test 1: Basic exception
    try:
        raise BookNotFoundError("Book #123 not found")
    except BookNotFoundError as e:
        print(f"✓ BookNotFoundError: {e}")
    
    # Test 2: API exception with status code
    try:
        raise BookNotAvailableError()
    except BookNotAvailableError as e:
        print(f"✓ BookNotAvailableError: {e}")
        print(f"  Status Code: {e.status_code}")
        print(f"  Error Code: {e.default_code}")
    
    # Test 3: Custom detail message
    try:
        raise ISBNAlreadyExistsError(
            detail="Book with ISBN 978-1234567890 already exists"
        )
    except ISBNAlreadyExistsError as e:
        print(f"✓ ISBNAlreadyExistsError: {e}")
    
    # Test 4: Rate limit with retry_after
    try:
        exc = RateLimitExceededError(retry_after=120)
        raise exc
    except RateLimitExceededError as e:
        print(f"✓ RateLimitExceededError: {e}")
        print(f"  Retry After: {e.retry_after} seconds")
    
    # Test 5: Exception hierarchy
    try:
        raise BookNotAvailable()
    except BookException as e:
        print(f"✓ Caught as BookException: {e}")
    except LibraryBaseException as e:
        print(f"✓ Caught as LibraryBaseException: {e}")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)


# ============================================
# BEST PRACTICES
# ============================================

"""
BEST PRACTICES FOR CUSTOM EXCEPTIONS:

1. ✅ Inherit from appropriate base class:
   - APIException for API responses
   - Exception for business logic

2. ✅ Use clear, descriptive names:
   - BookNotAvailableError (good)
   - Error1 (bad)

3. ✅ Set proper HTTP status codes:
   - 400: Bad Request (validation errors)
   - 403: Forbidden (permission errors)
   - 404: Not Found
   - 409: Conflict (duplicate resources)
   - 429: Too Many Requests (rate limiting)
   - 500: Internal Server Error

4. ✅ Provide clear error messages:
   - "Book 'Django Basics' is not available" (good)
   - "Error" (bad)

5. ✅ Use error codes for programmatic handling:
   - default_code = 'book_not_available'

6. ✅ Create exception hierarchy:
   - LibraryBaseException
     - BookException
       - BookNotAvailable
       - BookNotFound
     - UserException
       - UserQuotaExceeded

7. ✅ Document exceptions in docstrings

8. ✅ Log exceptions appropriately

9. ✅ Test exception handling
"""


# ============================================
# RUN TESTS
# ============================================

if __name__ == '__main__':
    test_custom_exceptions()