"""
LimitOffsetPagination Example

SQL LIMIT va OFFSET kabi ishlaydi.
Flexible pagination - ixtiyoriy miqdorda skip qilish.
"""

from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from books.models import Book
from books.serializers import BookSerializer, BookListSerializer
from books.filters import BookFilter


# ==================== 1. DEFAULT LIMIT OFFSET PAGINATION ====================

# settings.py da global sozlash:
"""
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}
"""

class BookListView(generics.ListAPIView):
    """
    Default LimitOffsetPagination
    
    Usage:
    GET /api/books/                    # 0-9 (first 10)
    GET /api/books/?limit=10           # 0-9
    GET /api/books/?limit=10&offset=10 # 10-19
    GET /api/books/?limit=20&offset=0  # 0-19
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


"""
Response:
{
    "count": 100,
    "next": "http://localhost:8000/api/books/?limit=10&offset=10",
    "previous": null,
    "results": [
        // 10 ta kitob
    ]
}
"""


# ==================== 2. CUSTOM LIMIT OFFSET ====================

class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    Custom limit/offset pagination
    """
    default_limit = 20  # Default limit
    max_limit = 100     # Maximum allowed limit
    limit_query_param = 'limit'
    offset_query_param = 'offset'


class BookCustomView(generics.ListAPIView):
    """
    Custom limit/offset
    
    Usage:
    GET /api/books/                    # 0-19 (default 20)
    GET /api/books/?limit=50           # 0-49
    GET /api/books/?limit=10&offset=20 # 20-29
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomLimitOffsetPagination


# ==================== 3. DIFFERENT DEFAULTS ====================

class SmallLimitPagination(LimitOffsetPagination):
    """Kichik limit - 5 items"""
    default_limit = 5
    max_limit = 50


class MediumLimitPagination(LimitOffsetPagination):
    """O'rta limit - 25 items"""
    default_limit = 25
    max_limit = 100


class LargeLimitPagination(LimitOffsetPagination):
    """Katta limit - 100 items"""
    default_limit = 100
    max_limit = 500


# ==================== 4. CUSTOM QUERY PARAMETERS ====================

class CustomParamLimitOffset(LimitOffsetPagination):
    """
    Custom parameter nomlari
    """
    default_limit = 10
    max_limit = 100
    limit_query_param = 'take'    # ?take=20
    offset_query_param = 'skip'   # ?skip=10


"""
Usage:
GET /api/books/?take=20&skip=40
"""


# ==================== 5. SQL-LIKE PAGINATION ====================

class SQLStylePagination(LimitOffsetPagination):
    """
    SQL LIMIT OFFSET kabi
    
    SQL: SELECT * FROM books LIMIT 10 OFFSET 20
    API: GET /api/books/?limit=10&offset=20
    """
    default_limit = 10
    max_limit = 1000


"""
Advantages:
✅ Familiar to SQL developers
✅ Flexible - skip to any position
✅ Good for data export

Disadvantages:
❌ Performance issues with large offsets
❌ Can skip items if data changes
❌ Not suitable for infinite scroll
"""


# ==================== 6. PAGINATION WITH RANGES ====================

class RangePagination(LimitOffsetPagination):
    """
    Range-based pagination
    """
    default_limit = 50
    max_limit = 200
    
    def get_paginated_response(self, data):
        """Add range info to response"""
        offset = self.offset
        limit = self.limit
        count = self.count
        
        from rest_framework.response import Response
        from collections import OrderedDict
        
        return Response(OrderedDict([
            ('count', count),
            ('range', {
                'from': offset,
                'to': min(offset + limit, count),
                'showing': len(data)
            }),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


"""
Response:
{
    "count": 100,
    "range": {
        "from": 0,
        "to": 10,
        "showing": 10
    },
    "next": "...",
    "previous": null,
    "results": [...]
}
"""


# ==================== 7. BATCH PROCESSING ====================

class BatchPagination(LimitOffsetPagination):
    """
    Batch processing uchun - katta limitlar
    """
    default_limit = 100
    max_limit = 1000  # Batch processing uchun katta limit


class BookBatchView(generics.ListAPIView):
    """
    Batch processing endpoint
    
    Usage:
    GET /api/books/batch/?limit=500&offset=0     # 0-499
    GET /api/books/batch/?limit=500&offset=500   # 500-999
    GET /api/books/batch/?limit=500&offset=1000  # 1000-1499
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BatchPagination


# ==================== 8. PAGINATION WITH FILTERS ====================

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class BookFilteredView(generics.ListAPIView):
    """
    LimitOffset + Filters
    
    Usage:
    GET /api/books/?search=django&limit=20&offset=40
    GET /api/books/?author=1&limit=50
    GET /api/books/?ordering=price&limit=25&offset=0
    """
    queryset = Book.objects.select_related('author').prefetch_related('genres')
    serializer_class = BookListSerializer
    
    # Pagination
    pagination_class = CustomLimitOffsetPagination
    
    # Filters
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['price', 'published_date']


# ==================== 9. INFINITE SCROLL SIMULATION ====================

class InfiniteScrollPagination(LimitOffsetPagination):
    """
    Infinite scroll uchun
    """
    default_limit = 20
    max_limit = 50
    
    def get_paginated_response(self, data):
        """Simplified response for infinite scroll"""
        from rest_framework.response import Response
        
        return Response({
            'has_more': self.get_next_link() is not None,
            'total': self.count,
            'data': data
        })


"""
Response:
{
    "has_more": true,
    "total": 100,
    "data": [...]
}

Frontend usage:
let offset = 0;
function loadMore() {
    fetch(`/api/books/?limit=20&offset=${offset}`)
    offset += 20;
}
"""


# ==================== 10. CONDITIONAL LIMIT ====================

class ConditionalLimitPagination(LimitOffsetPagination):
    """
    Query param ga qarab limit o'zgartirish
    """
    default_limit = 10
    max_limit = 100
    
    def get_limit(self, request):
        """Custom limit logic"""
        # Admin uchun katta limit
        if request.user.is_staff:
            return min(int(request.query_params.get(self.limit_query_param, 50)), 500)
        
        # Oddiy user uchun default
        return super().get_limit(request)


# ==================== URLS ====================

from django.urls import path

urlpatterns = [
    # Default
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Custom
    path('books/custom/', BookCustomView.as_view(), name='book-custom'),
    
    # Batch processing
    path('books/batch/', BookBatchView.as_view(), name='book-batch'),
    
    # Filtered
    path('books/filtered/', BookFilteredView.as_view(), name='book-filtered'),
]


# ==================== USE CASES ====================

"""
1. DATA EXPORT:
   GET /api/books/?limit=1000&offset=0
   GET /api/books/?limit=1000&offset=1000
   GET /api/books/?limit=1000&offset=2000
   
   Use Case: Export all data in chunks

2. PAGINATION TABLE:
   GET /api/books/?limit=25&offset=0     # Page 1
   GET /api/books/?limit=25&offset=25    # Page 2
   GET /api/books/?limit=25&offset=50    # Page 3
   
   Use Case: Data table with custom page navigation

3. LAZY LOADING:
   GET /api/books/?limit=10&offset=0
   GET /api/books/?limit=10&offset=10
   GET /api/books/?limit=10&offset=20
   
   Use Case: Load more on scroll

4. RANGE QUERIES:
   GET /api/books/?limit=50&offset=100
   
   Use Case: Get items 100-149
"""


# ==================== ADVANTAGES & DISADVANTAGES ====================

"""
ADVANTAGES:
✅ Flexible - jump to any position
✅ SQL-like syntax (familiar)
✅ Good for batch processing
✅ Suitable for data export
✅ Can calculate total pages easily

DISADVANTAGES:
❌ Performance degrades with large offsets
   (OFFSET 100000 is slow)
❌ Inconsistent if data changes during pagination
   (items can be skipped or duplicated)
❌ Not ideal for infinite scroll
❌ Database must scan all skipped rows

WHEN TO USE:
✅ Data tables with page numbers
✅ Batch processing / data export
✅ Admin panels
✅ Small to medium datasets

WHEN NOT TO USE:
❌ Real-time feeds
❌ Infinite scroll (use CursorPagination)
❌ Very large datasets with deep pagination
❌ High-frequency data changes
"""


# ==================== PERFORMANCE TIPS ====================

"""
1. DATABASE INDEXES:
   - Add index on ordering field
   - Use composite indexes if needed

2. LIMIT OFFSETS:
   - Avoid very large offsets (> 10000)
   - Consider using CursorPagination instead

3. COUNT QUERY:
   - Cache count for large datasets
   - Or disable count for very large tables

4. QUERY OPTIMIZATION:
   - Use select_related() / prefetch_related()
   - Only fetch needed fields (.only())
   - Consider materialized views for complex queries

Example:
class OptimizedView(generics.ListAPIView):
    pagination_class = CustomLimitOffsetPagination
    
    def get_queryset(self):
        return Book.objects.select_related('author').only(
            'id', 'title', 'price', 'author__name'
        )
"""


# ==================== TESTING ====================

"""
Test Cases:

1. Default Limit:
   GET /api/books/
   Expected: 0-9 (10 items)

2. Custom Limit:
   GET /api/books/?limit=20
   Expected: 0-19 (20 items)

3. Offset:
   GET /api/books/?limit=10&offset=20
   Expected: 20-29 (items 20-29)

4. Large Offset:
   GET /api/books/?limit=10&offset=90
   Expected: 90-99 (last 10 items)

5. Beyond Last:
   GET /api/books/?limit=10&offset=100
   Expected: Empty array

6. Max Limit:
   GET /api/books/?limit=1000
   Expected: max_limit enforced (100)

7. With Filters:
   GET /api/books/?author=1&limit=20&offset=0
   Expected: Filtered and paginated

8. Negative Offset:
   GET /api/books/?offset=-10
   Expected: Error or 0 offset
"""


# ==================== COMPARISON ====================

"""
PageNumberPagination vs LimitOffsetPagination:

PageNumber:
- ?page=2&page_size=10
- User-friendly (page numbers)
- Better for UI pagination

LimitOffset:
- ?limit=10&offset=10
- SQL-like syntax
- More flexible (jump anywhere)
- Better for programmatic access

Choose based on:
- UI: PageNumberPagination
- API/Backend: LimitOffsetPagination
- Data Export: LimitOffsetPagination
- Mobile Apps: Could use either
"""