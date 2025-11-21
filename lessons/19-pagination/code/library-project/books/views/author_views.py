"""
Author views with filtering and searching - Lesson 18
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


class AuthorListView(generics.ListAPIView):
    """
    GET: Barcha mualliflar ro'yxati
    
    Filters:
    - DjangoFilterBackend: name, email, birth_year, has_published_books, min_books
    - SearchFilter: name, email, bio
    - OrderingFilter: name, birth_date, created_at
    
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


class AuthorDetailView(generics.RetrieveAPIView):
    """
    GET: Bitta muallif detali (barcha kitoblari bilan)
    """
    serializer_class = AuthorDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Optimized queryset - kitoblar va janrlar bilan"""
        return Author.objects.prefetch_related(
            Prefetch('books', queryset=Book.objects.prefetch_related('genres'))
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