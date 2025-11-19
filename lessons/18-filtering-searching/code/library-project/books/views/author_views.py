"""Author views - Lesson 17"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Prefetch
from books.models import Author, Book
from books.serializers import (
    AuthorSerializer,
    AuthorDetailSerializer,
    AuthorWithBooksCreateSerializer,
    AuthorWithBooksUpdateSerializer,
)


class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AuthorDetailView(generics.RetrieveAPIView):
    serializer_class = AuthorDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Author.objects.prefetch_related(
            Prefetch('books', queryset=Book.objects.prefetch_related('genres'))
        )


class AuthorCreateView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorWithBooksCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class AuthorUpdateView(generics.UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorWithBooksUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class AuthorDeleteView(generics.DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]