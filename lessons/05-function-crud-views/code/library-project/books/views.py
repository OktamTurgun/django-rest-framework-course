from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

# Create your views here.
class BookAPIListView(ListAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer

class BookDetailAPIView(RetrieveAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer

class BookCreateAPIView(CreateAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer

class BookUpdateAPIView(UpdateAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer

class BookDeleteAPIView(DestroyAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
