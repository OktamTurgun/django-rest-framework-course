"""
Genre views with filtering and searching - Lesson 18
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from books.models import Genre
from books.serializers import GenreSerializer, GenreDetailSerializer
from books.filters import GenreFilter


class GenreListCreateView(generics.ListCreateAPIView):
    """
    GET: Barcha janrlar ro'yxati
    POST: Yangi janr yaratish
    
    Filters:
    - DjangoFilterBackend: name, min_books
    - SearchFilter: name, description
    - OrderingFilter: name, created_at
    
    Examples:
    /api/genres/
    /api/genres/?search=programming
    /api/genres/?ordering=name
    /api/genres/?min_books=5
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Filter backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # DjangoFilter
    filterset_class = GenreFilter
    
    # SearchFilter
    search_fields = ['name', 'description']
    
    # OrderingFilter
    ordering_fields = ['name', 'created_at']
    ordering = ['name']  # Default: alphabetical


class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Bitta janr detali (kitoblar soni bilan)
    PUT/PATCH: Janrni yangilash
    DELETE: Janrni o'chirish
    """
    queryset = Genre.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        """GET uchun detail serializer"""
        if self.request.method == 'GET':
            return GenreDetailSerializer
        return GenreSerializer