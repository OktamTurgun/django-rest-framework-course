from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView,
    ListCreateAPIView, RetrieveUpdateAPIView,
    RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
)
from .models import Book
from .serializers import BookSerializer


# 1 Faqat ro‘yxat
class BookListAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# 2 Faqat bitta obyektni olish
class BookDetailAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# 3 Faqat yangi obyekt yaratish
class BookCreateAPIView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# 4 Faqat obyektni yangilash
class BookUpdateAPIView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# 5 Faqat obyektni o‘chirish
class BookDeleteAPIView(DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# 6 Ro‘yxat + Yaratish
class BookListCreateAPIView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# 7 Ko‘rsatish + Yangilash
class BookRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# 8 Ko‘rsatish + O‘chirish
class BookRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# 9 Ko‘rsatish + Yangilash + O‘chirish (To‘liq CRUD bitta obyekt uchun)
class BookRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
