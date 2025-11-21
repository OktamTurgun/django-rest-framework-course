"""
Book views with filtering and searching - Lesson 18
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


class BookListCreateView(generics.ListCreateAPIView):
    """
    GET: Barcha kitoblar ro'yxati
    POST: Yangi kitob yaratish
    
    Filters:
    - DjangoFilterBackend: title, price range, date range, author, genres, etc.
    - SearchFilter: title, subtitle, author__name, publisher
    - OrderingFilter: price, published_date, title, pages
    
    Examples:
    /api/books/
    /api/books/?search=django
    /api/books/?ordering=-published_date
    /api/books/?author=1&published=true
    /api/books/?min_price=20&max_price=50
    /api/books/?search=python&ordering=price&published_year=2024
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
    
    def get_queryset(self):
        """Optimized queryset"""
        return Book.objects.select_related('author', 'owner').prefetch_related('genres')
    
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
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Optimized queryset"""
        return Book.objects.select_related('author', 'owner').prefetch_related('genres')
    
    def get_serializer_class(self):
        """GET va PUT/PATCH uchun turli serializerlar"""
        if self.request.method in ['PUT', 'PATCH']:
            return BookCreateUpdateSerializer
        return BookDetailSerializer