"""
Author views with filtering, searching, pagination and optimization - Lesson 18, 19, 22
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch

from books.models import Author, Book
from books.serializers import (
    AuthorSerializer,
    AuthorDetailSerializer,
    AuthorWithBooksCreateSerializer,
    AuthorWithBooksUpdateSerializer,
)
from books.filters import AuthorFilter
from books.pagination import MediumResultsSetPagination
from books.mixins import QueryOptimizationMixin


class AuthorListView(QueryOptimizationMixin, generics.ListAPIView):
    """
    GET: Barcha mualliflar ro'yxati
    
    Filters:
    - DjangoFilterBackend: name, email, birth_year, has_published_books, min_books
    - SearchFilter: name, email, bio
    - OrderingFilter: name, birth_date, created_at
    
    Optimization (Lesson 22):
    - Reverse ForeignKey prefetch for books
    
    Examples:
    /api/authors/
    /api/authors/?search=john
    /api/authors/?ordering=name
    /api/authors/?has_published_books=true
    /api/authors/?min_books=2
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Filter backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # DjangoFilter
    filterset_class = AuthorFilter
    
    # SearchFilter
    search_fields = ['name', 'email', 'bio']
    
    # OrderingFilter
    ordering_fields = ['name', 'birth_date', 'created_at']
    ordering = ['name']  # Default: alphabetical
    
    # Query Optimization (Lesson 22)
    prefetch_related_fields = ['books']  # Reverse ForeignKey optimization


class AuthorDetailView(QueryOptimizationMixin, generics.RetrieveAPIView):
    """
    GET: Bitta muallif detali (barcha kitoblari bilan)
    
    Optimization (Lesson 22):
    - Custom Prefetch for books with genres
    - Nested prefetch optimization
    """
    serializer_class = AuthorDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """
        Optimized queryset - kitoblar va janrlar bilan
        Lesson 22: Custom Prefetch with nested optimization
        """
        return Author.objects.prefetch_related(
            Prefetch(
                'books',
                queryset=Book.objects.select_related('owner').prefetch_related('genres')
            )
        )


class AuthorCreateView(generics.CreateAPIView):
    """
    POST: Yangi muallif yaratish (kitoblari bilan birga)
    """
    queryset = Author.objects.all()
    serializer_class = AuthorWithBooksCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        """Request'ni serializer context'iga qo'shish"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class AuthorUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Muallifni yangilash (kitoblari bilan)
    """
    queryset = Author.objects.all()
    serializer_class = AuthorWithBooksUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Optimized queryset for update
        Lesson 22: Prefetch books for efficient update
        """
        return Author.objects.prefetch_related('books')
    
    def get_serializer_context(self):
        """Request'ni serializer context'iga qo'shish"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class AuthorDeleteView(generics.DestroyAPIView):
    """
    DELETE: Muallifni o'chirish
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]