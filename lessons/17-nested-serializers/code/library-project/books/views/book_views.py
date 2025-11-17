"""Book views - Lesson 17"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from books.models import Book
from books.serializers import (
    BookListSerializer,
    BookDetailSerializer,
    BookCreateUpdateSerializer,
)


class BookListCreateView(generics.ListCreateAPIView):
    """
    GET: Barcha kitoblar ro'yxati (nested author va genres bilan)
    POST: Yangi kitob yaratish
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Book.objects.select_related('author', 'owner').prefetch_related('genres')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookCreateUpdateSerializer
        return BookListSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Bitta kitob detali
    PUT/PATCH: Yangilash
    DELETE: O'chirish
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Book.objects.select_related('author', 'owner').prefetch_related('genres')
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BookCreateUpdateSerializer
        return BookDetailSerializer