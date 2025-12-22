"""
Custom Exceptions for Library Management System

This module contains all custom exceptions used throughout the application.
Each exception is designed for specific business logic scenarios.
"""

from rest_framework.exceptions import APIException
from rest_framework import status


# ============================================
# BOOK EXCEPTIONS
# ============================================

class BookNotAvailableError(APIException):
    """
    Raised when a book is not available for borrowing
    
    Status: 400 Bad Request
    Code: book_not_available
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'This book is currently not available for borrowing'
    default_code = 'book_not_available'


class BookAlreadyBorrowedError(APIException):
    """
    Raised when user tries to borrow a book they've already borrowed
    
    Status: 400 Bad Request
    Code: book_already_borrowed
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'You have already borrowed this book'
    default_code = 'book_already_borrowed'


class BookAlreadyReturnedError(APIException):
    """
    Raised when trying to return a book that's already been returned
    
    Status: 400 Bad Request
    Code: book_already_returned
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'This book has already been returned'
    default_code = 'book_already_returned'


class ISBNAlreadyExistsError(APIException):
    """
    Raised when trying to create a book with duplicate ISBN
    
    Status: 409 Conflict
    Code: isbn_duplicate
    """
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'A book with this ISBN already exists'
    default_code = 'isbn_duplicate'


class InvalidISBNFormatError(APIException):
    """
    Raised when ISBN format is invalid
    
    Status: 400 Bad Request
    Code: invalid_isbn_format
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'ISBN format is invalid. Expected: ISBN-13 format'
    default_code = 'invalid_isbn_format'


class InsufficientStockError(APIException):
    """
    Raised when there are not enough books in stock
    
    Status: 400 Bad Request
    Code: insufficient_stock
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Not enough books in stock'
    default_code = 'insufficient_stock'


# ============================================
# USER/BORROWING EXCEPTIONS
# ============================================

class BorrowLimitExceededError(APIException):
    """
    Raised when user exceeds maximum borrow limit
    
    Status: 403 Forbidden
    Code: borrow_limit_exceeded
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You have reached the maximum number of borrowed books (5)'
    default_code = 'borrow_limit_exceeded'


class NotBookOwnerError(APIException):
    """
    Raised when user tries to return a book they didn't borrow
    
    Status: 403 Forbidden
    Code: not_book_owner
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You can only return books that you borrowed'
    default_code = 'not_book_owner'


class OverdueBooksError(APIException):
    """
    Raised when user has overdue books
    
    Status: 403 Forbidden
    Code: overdue_books
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You have overdue books. Please return them first.'
    default_code = 'overdue_books'


# ============================================
# AUTHOR EXCEPTIONS
# ============================================

class AuthorLimitExceededError(APIException):
    """
    Raised when author reaches maximum book limit
    
    Status: 400 Bad Request
    Code: author_limit_exceeded
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'This author has reached the maximum number of books (100)'
    default_code = 'author_limit_exceeded'


# ============================================
# VALIDATION EXCEPTIONS
# ============================================

class InvalidDateRangeError(APIException):
    """
    Raised when date range is invalid
    
    Status: 400 Bad Request
    Code: invalid_date_range
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Start date must be before end date'
    default_code = 'invalid_date_range'


class FutureDateError(APIException):
    """
    Raised when date is in the future
    
    Status: 400 Bad Request
    Code: future_date
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Published date cannot be in the future'
    default_code = 'future_date'


class NegativePriceError(APIException):
    """
    Raised when price is negative
    
    Status: 400 Bad Request
    Code: negative_price
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Price must be a positive number'
    default_code = 'negative_price'


# ============================================
# RATE LIMITING EXCEPTIONS
# ============================================

class RateLimitExceededError(APIException):
    """
    Raised when API rate limit is exceeded
    
    Status: 429 Too Many Requests
    Code: rate_limit_exceeded
    """
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = 'Rate limit exceeded. Please try again later.'
    default_code = 'rate_limit_exceeded'
    
    def __init__(self, retry_after=60, detail=None, code=None):
        super().__init__(detail, code)
        self.retry_after = retry_after
        if detail is None:
            self.detail = f'Rate limit exceeded. Retry after {retry_after} seconds.'


class DailyQuotaExceededError(APIException):
    """
    Raised when daily API quota is exceeded
    
    Status: 429 Too Many Requests
    Code: daily_quota_exceeded
    """
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = 'Daily API quota exceeded. Try again tomorrow.'
    default_code = 'daily_quota_exceeded'


# ============================================
# PERMISSION EXCEPTIONS
# ============================================

class AdminOnlyError(APIException):
    """
    Raised when non-admin tries admin-only action
    
    Status: 403 Forbidden
    Code: admin_only
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'This action can only be performed by administrators'
    default_code = 'admin_only'


# ============================================
# EXTERNAL SERVICE EXCEPTIONS
# ============================================

class PaymentServiceError(APIException):
    """
    Raised when payment service is unavailable
    
    Status: 502 Bad Gateway
    Code: payment_service_error
    """
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = 'Payment service is currently unavailable'
    default_code = 'payment_service_error'


class EmailServiceError(APIException):
    """
    Raised when email service is unavailable
    
    Status: 503 Service Unavailable
    Code: email_service_error
    """
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Email service is currently unavailable'
    default_code = 'email_service_error'


# ============================================
# EXCEPTION HIERARCHY (Optional)
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