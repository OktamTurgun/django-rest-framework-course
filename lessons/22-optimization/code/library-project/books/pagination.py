"""
Books app pagination classes
Different pagination strategies for different use cases
"""

from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
    CursorPagination
)
from rest_framework.response import Response
from collections import OrderedDict


# ==================== PAGE NUMBER PAGINATION ====================

class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination - 10 items per page
    User can change page_size up to 100
    
    Usage:
    GET /api/books/?page=2
    GET /api/books/?page=2&page_size=20
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class SmallResultsSetPagination(PageNumberPagination):
    """
    Small pagination - 5 items per page
    For smaller datasets (e.g., Genres)
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class MediumResultsSetPagination(PageNumberPagination):
    """
    Medium pagination - 25 items per page
    For medium datasets
    """
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class LargeResultsSetPagination(PageNumberPagination):
    """
    Large pagination - 50 items per page
    For large datasets or data export
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


# ==================== LIMIT OFFSET PAGINATION ====================

class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    Custom limit/offset pagination
    SQL-style: LIMIT 20 OFFSET 40
    
    Usage:
    GET /api/books/?limit=20&offset=40
    GET /api/books/?limit=50
    """
    default_limit = 20
    max_limit = 100
    limit_query_param = 'limit'
    offset_query_param = 'offset'


class BatchPagination(LimitOffsetPagination):
    """
    Batch processing pagination - larger limits
    For data export or batch operations
    
    Usage:
    GET /api/books/batch/?limit=100&offset=0
    """
    default_limit = 100
    max_limit = 500


# ==================== CURSOR PAGINATION ====================

class BookFeedPagination(CursorPagination):
    """
    Cursor pagination for book feed
    Real-time updates, infinite scroll
    
    Usage:
    GET /api/books/feed/
    GET /api/books/feed/?cursor=cD0yMDI0...
    """
    page_size = 10
    ordering = '-created_at'
    cursor_query_param = 'cursor'


class AuthorFeedPagination(CursorPagination):
    """
    Cursor pagination for authors
    Ordered by name alphabetically
    """
    page_size = 10
    ordering = 'name'
    cursor_query_param = 'cursor'


# ==================== CUSTOM RESPONSE FORMAT ====================

class CustomResponsePagination(PageNumberPagination):
    """
    Custom response format with detailed pagination info
    
    Response:
    {
        "pagination": {
            "total_items": 100,
            "total_pages": 10,
            "current_page": 1,
            "page_size": 10,
            "has_next": true,
            "has_previous": false
        },
        "links": {
            "next": "...",
            "previous": null
        },
        "data": [...]
    }
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('pagination', OrderedDict([
                ('total_items', self.page.paginator.count),
                ('total_pages', self.page.paginator.num_pages),
                ('current_page', self.page.number),
                ('page_size', len(data)),
                ('has_next', self.page.has_next()),
                ('has_previous', self.page.has_previous()),
            ])),
            ('links', OrderedDict([
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
            ])),
            ('data', data)
        ]))


# ==================== MOBILE-FRIENDLY PAGINATION ====================

class MobileFriendlyPagination(PageNumberPagination):
    """
    Mobile-optimized pagination
    Smaller page size, simpler response
    
    Response:
    {
        "hasMore": true,
        "total": 100,
        "items": [...]
    }
    """
    page_size = 15
    max_page_size = 50
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('hasMore', self.page.has_next()),
            ('total', self.page.paginator.count),
            ('items', data)
        ]))