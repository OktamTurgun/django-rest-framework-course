"""Genre views - Lesson 17"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from books.models import Genre
from books.serializers import GenreSerializer, GenreDetailSerializer


class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GenreDetailSerializer
        return GenreSerializer