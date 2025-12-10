"""
Book views with filtering, searching, pagination and optimization - Lesson 18, 19, 22
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from books.models import Book
from books.serializers import (
    BookListSerializer,
    BookDetailSerializer,
    BookCreateUpdateSerializer,
)
from books.filters import BookFilter
from books.pagination import StandardResultsSetPagination, BookFeedPagination


class BookListCreateView(generics.ListCreateAPIView):
    """
    GET: Barcha kitoblar ro'yxati
    POST: Yangi kitob yaratish
    
    Features:
    - Pagination: 10 items per page (customizable)
    - Filters: DjangoFilterBackend
    - Search: title, subtitle, author__name, publisher
    - Ordering: price, published_date, title, pages
    - Query Optimization: select_related, prefetch_related (Lesson 22)
    
    Examples:
    /api/books/
    /api/books/?page=2
    /api/books/?page_size=20
    /api/books/?search=django&page=2
    /api/books/?author=1&published=true&ordering=-price&page=3
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Filter backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # DjangoFilter
    filterset_class = BookFilter
    
    # SearchFilter
    search_fields = ['title', 'subtitle', 'author__name', 'publisher']
    
    # OrderingFilter
    ordering_fields = ['price', 'published_date', 'title', 'pages', 'created_at']
    ordering = ['-published_date']  # Default ordering
    
    # Pagination
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Optimized queryset
        Lesson 22: Query Optimization
        """
        return Book.objects.select_related(
            'author',
            'owner'
        ).prefetch_related(
            'genres'
        )
    
    def get_serializer_class(self):
        """POST uchun boshqa serializer"""
        if self.request.method == 'POST':
            return BookCreateUpdateSerializer
        return BookListSerializer
    
    def perform_create(self, serializer):
        """Kitob yaratishda owner ni avtomatik belgilash"""
        serializer.save(owner=self.request.user)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Bitta kitob detali
    PUT/PATCH: Kitobni yangilash
    DELETE: Kitobni o'chirish
    
    Lesson 22: Optimized with select_related and prefetch_related
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """
        Optimized queryset
        Lesson 22: Query Optimization
        """
        return Book.objects.select_related(
            'author',
            'owner'
        ).prefetch_related(
            'genres'
        )
    
    def get_serializer_class(self):
        """GET va PUT/PATCH uchun turli serializerlar"""
        if self.request.method in ['PUT', 'PATCH']:
            return BookCreateUpdateSerializer
        return BookDetailSerializer


class BookFeedView(generics.ListAPIView):
    """
    Book feed - cursor pagination bilan
    Real-time yangi kitoblar feed'i
    
    Features:
    - Cursor pagination (high performance)
    - Real-time updates
    - Infinite scroll support
    - Only published books
    - Query Optimization (Lesson 22)
    
    Usage:
    GET /api/books/feed/
    GET /api/books/feed/?cursor=cD0yMDI0...
    """
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BookFeedPagination
    
    def get_queryset(self):
        """
        Faqat published kitoblar, optimized
        Lesson 22: Query Optimization
        """
        return Book.objects.filter(
            published=True
        ).select_related(
            'author',
            'owner'
        ).prefetch_related(
            'genres'
        )