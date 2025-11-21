"""
PageNumberPagination Example

Eng oddiy va ko'p ishlatiladigan pagination turi.
Sahifa raqamlari: 1, 2, 3, ...
"""

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from books.models import Book, Genre, Log
from books.serializers import BookSerializer, GenreSerializer, LogSerializer, BookListSerializer
from books.filters import BookFilter


# ==================== 1. DEFAULT PAGE NUMBER PAGINATION ====================

# settings.py da global sozlash:
"""
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
"""

class BookListView(generics.ListAPIView):
    """
    Default pagination - settings.py dan olinadi
    
    Usage:
    GET /api/books/         # Page 1 (default)
    GET /api/books/?page=2  # Page 2
    GET /api/books/?page=3  # Page 3
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    # pagination_class ishlatilmasa, DEFAULT_PAGINATION_CLASS ishlatiladi


"""
Response:
{
    "count": 100,
    "next": "http://localhost:8000/api/books/?page=2",
    "previous": null,
    "results": [
        // 10 ta kitob
    ]
}
"""


# ==================== 2. CUSTOM PAGE SIZE ====================

class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination - 10 items per page
    User page_size ni o'zgartirishi mumkin
    """
    page_size = 10
    page_size_query_param = 'page_size'  # ?page_size=20
    max_page_size = 100  # Maximum limit


class BookStandardView(generics.ListAPIView):
    """
    Custom pagination class
    
    Usage:
    GET /api/books/                    # 10 items (default)
    GET /api/books/?page_size=20       # 20 items
    GET /api/books/?page=2&page_size=5 # Page 2, 5 items
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination


# ==================== 3. DIFFERENT PAGE SIZES ====================

class SmallResultsSetPagination(PageNumberPagination):
    """Kichik pagination - 5 items"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class MediumResultsSetPagination(PageNumberPagination):
    """O'rta pagination - 25 items"""
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class LargeResultsSetPagination(PageNumberPagination):
    """Katta pagination - 100 items"""
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 500


# Har xil view'lar uchun
class GenreListView(generics.ListAPIView):
    """Kichik dataset - 5 per page"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = SmallResultsSetPagination


class BookListView(generics.ListAPIView):
    """O'rta dataset - 25 per page"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = MediumResultsSetPagination


class LogListView(generics.ListAPIView):
    """Katta dataset - 100 per page"""
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    pagination_class = LargeResultsSetPagination


# ==================== 4. DISABLE PAGE SIZE PARAMETER ====================

class FixedPageSizePagination(PageNumberPagination):
    """
    Fixed page size - user o'zgartira olmaydi
    """
    page_size = 20
    page_size_query_param = None  # Disabled
    max_page_size = None


"""
Usage:
GET /api/books/?page_size=50  # Ishlamaydi, har doim 20 ta
"""


# ==================== 5. CUSTOM QUERY PARAMETER ====================

class CustomParamPagination(PageNumberPagination):
    """
    Custom parameter nomi
    """
    page_size = 10
    page_query_param = 'p'  # ?p=2 instead of ?page=2
    page_size_query_param = 'size'  # ?size=20


"""
Usage:
GET /api/books/?p=2&size=20
"""


# ==================== 6. RESPONSE WITH ADDITIONAL INFO ====================

from rest_framework.response import Response
from collections import OrderedDict

class DetailedPagination(PageNumberPagination):
    """
    Qo'shimcha ma'lumotlar bilan response
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page', self.page.number),
            ('num_pages', self.page.paginator.num_pages),
            ('page_size', len(data)),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


"""
Response:
{
    "count": 100,
    "page": 1,
    "num_pages": 10,
    "page_size": 10,
    "next": "...",
    "previous": null,
    "results": [...]
}
"""


# ==================== 7. PAGINATION WITH FILTERS ====================

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class BookAdvancedView(generics.ListAPIView):
    """
    Pagination + Filtering + Search + Ordering
    
    Usage:
    GET /api/books/?search=django&page=2
    GET /api/books/?author=1&page_size=20
    GET /api/books/?ordering=price&page=3
    """
    queryset = Book.objects.select_related('author').prefetch_related('genres')
    serializer_class = BookListSerializer
    
    # Pagination
    pagination_class = StandardResultsSetPagination
    
    # Filters
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['price', 'published_date']


# ==================== 8. LAST PAGE TEMPLATE ====================

class LastPageTemplatePagination(PageNumberPagination):
    """
    Template bilan ishlatish uchun
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    template = 'rest_framework/pagination/numbers.html'


# ==================== 9. DISABLE PAGINATION FOR SPECIFIC VIEW ====================

class GenreListAllView(generics.ListAPIView):
    """
    Pagination'siz - barcha genrelar
    
    Usage: Kichik dataset'lar uchun (10-50 items)
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = None  # Disabled


# ==================== 10. CONDITIONAL PAGINATION ====================

class ConditionalPaginationView(generics.ListAPIView):
    """
    Shartli pagination - query param ga qarab
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_pagination_class(self):
        """Query param ga qarab pagination tanlash"""
        if self.request.query_params.get('no_pagination'):
            return None
        return StandardResultsSetPagination
    
    @property
    def pagination_class(self):
        return self.get_pagination_class()


"""
Usage:
GET /api/books/                    # Paginated
GET /api/books/?no_pagination=true # All results
"""


# ==================== URLS ====================

from django.urls import path

urlpatterns = [
    # Default pagination
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Standard pagination
    path('books/standard/', BookStandardView.as_view(), name='book-standard'),
    
    # Different page sizes
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('logs/', LogListView.as_view(), name='log-list'),
    
    # Advanced (filters + pagination)
    path('books/advanced/', BookAdvancedView.as_view(), name='book-advanced'),
    
    # No pagination
    path('genres/all/', GenreListAllView.as_view(), name='genre-all'),
    
    # Conditional pagination
    path('books/conditional/', ConditionalPaginationView.as_view(), name='book-conditional'),
]


# ==================== BEST PRACTICES ====================

"""
1. SENSIBLE DEFAULTS:
   ✅ page_size = 10-50 (depends on data size)
   ✅ max_page_size = 100-200
   ✅ Allow user to change page_size

2. PERFORMANCE:
   ✅ Use select_related() / prefetch_related()
   ✅ Add database indexes on ordering fields
   ✅ Consider count query optimization

3. USER EXPERIENCE:
   ✅ Clear response format
   ✅ Provide next/previous links
   ✅ Show total count
   ✅ Handle edge cases (empty results, last page)

4. CONSISTENCY:
   ✅ Use same pagination across similar endpoints
   ✅ Document pagination in API docs
   ✅ Handle errors gracefully

Common Mistakes:
❌ Too large page_size default
❌ No max_page_size limit
❌ Pagination on small datasets
❌ Not optimizing queries
"""


# ==================== RESPONSE EXAMPLES ====================

"""
FIRST PAGE:
{
    "count": 100,
    "next": "http://localhost:8000/api/books/?page=2",
    "previous": null,
    "results": [...]
}

MIDDLE PAGE:
{
    "count": 100,
    "next": "http://localhost:8000/api/books/?page=6",
    "previous": "http://localhost:8000/api/books/?page=4",
    "results": [...]
}

LAST PAGE:
{
    "count": 100,
    "next": null,
    "previous": "http://localhost:8000/api/books/?page=9",
    "results": [...]
}

EMPTY RESULTS:
{
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
}

WITH FILTERS:
{
    "count": 25,
    "next": "http://localhost:8000/api/books/?search=django&page=2",
    "previous": null,
    "results": [...]
}
"""


# ==================== TESTING ====================

"""
Test Cases:

1. First Page:
   GET /api/books/
   Expected: 10 items, next link, no previous

2. Middle Page:
   GET /api/books/?page=5
   Expected: 10 items, both next and previous

3. Last Page:
   GET /api/books/?page=10
   Expected: Remaining items, no next, has previous

4. Invalid Page:
   GET /api/books/?page=999
   Expected: 404 or empty results

5. Custom Page Size:
   GET /api/books/?page_size=20
   Expected: 20 items

6. Max Page Size Exceeded:
   GET /api/books/?page_size=1000
   Expected: max_page_size enforced (100)

7. With Filters:
   GET /api/books/?author=1&page=2
   Expected: Filtered and paginated

8. Empty Results:
   GET /api/books/?search=nonexistent
   Expected: count=0, empty array
"""