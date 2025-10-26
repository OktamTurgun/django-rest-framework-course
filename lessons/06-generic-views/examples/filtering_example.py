"""
DRF Filter Backends Examples
=============================

Ushbu faylda Django REST Framework'ning turli xil filter backend'lari
(SearchFilter, OrderingFilter, DjangoFilterBackend) ishlatish misollari keltirilgan.
"""

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
# from .models import Book
# from .serializers import BookSerializer


# =============================================================================
# 1. SearchFilter - Qidirish
# =============================================================================

class BookSearchView(generics.ListAPIView):
    """
    Qidiruv - title va author bo‘yicha (exact match)
    Example: GET /books/search/?search=django
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=title', '=author']


# =============================================================================
# 2. OrderingFilter - Tartiblash
# =============================================================================

class BookOrderingView(generics.ListAPIView):
    """
    Tartiblash - price, publish_date, title bo‘yicha.
    Examples:
      - GET /books/ordering/?ordering=price
      - GET /books/ordering/?ordering=-price
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price', 'publish_date', 'title', 'pages']
    ordering = ['-publish_date']  # Default: yangi kitoblar birinchi


# =============================================================================
# 3. Search + Ordering birgalikda
# =============================================================================

class BookSearchAndOrderView(generics.ListAPIView):
    """
    Qidirish VA tartiblash birgalikda.
    Example: GET /books/?search=python&ordering=-price
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'description']
    ordering_fields = ['price', 'publish_date', 'title']
    ordering = ['-publish_date']


# =============================================================================
# 4. DjangoFilterBackend - Aniq field'lar bo‘yicha filter
# =============================================================================

class BookDjangoFilterView(generics.ListAPIView):
    """
    Aniq field'lar bo‘yicha filter.
    Examples:
      - GET /books/filter/?available=true
      - GET /books/filter/?author=Alisher
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['available', 'author', 'price']


# =============================================================================
# 5. DjangoFilterBackend + Search + Ordering (Full Power)
# =============================================================================

class BookFullFilterView(generics.ListAPIView):
    """
    Uchala filter turi birgalikda ishlatiladi.
    Example: GET /books/?available=true&search=django&ordering=-price
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['available', 'author']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'publish_date']
    ordering = ['-publish_date']


# =============================================================================
# 6. Advanced Search - related field'lar
# =============================================================================

class BookAdvancedSearchView(generics.ListAPIView):
    """
    Murakkab qidirish (relationship field’larda ham qidiradi).
    Example: GET /books/?search=uzbekistan
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'title',
        'author',
        'description',
        'category__name',
        'publisher__name'
    ]


# =============================================================================
# 7. Exact match qidirish
# =============================================================================

class BookExactSearchView(generics.ListAPIView):
    """
    To‘liq mos keladigan natijalarni topadi.
    Example: GET /books/?search=Django
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=title', '=author']


# =============================================================================
# 8. Case-insensitive qidirish (default)
# =============================================================================

class BookCaseInsensitiveSearchView(generics.ListAPIView):
    """
    Katta-kichik harf farqi muhim emas.
    Example: GET /books/?search=django
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author']


# =============================================================================
# 9. Starts with qidirish
# =============================================================================

class BookStartsWithSearchView(generics.ListAPIView):
    """
    So‘zning boshidan mos keladigan natijalarni topadi.
    Example: GET /books/?search=Py → Python, PyTorch
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title', '^author']


# =============================================================================
# 10. Full-text search (PostgreSQL)
# =============================================================================

class BookFullTextSearchView(generics.ListAPIView):
    """
    PostgreSQL'da full-text search (so‘z kontekstini hisobga oladi).
    Example: GET /books/?search=python programming
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['$title', '$description']
