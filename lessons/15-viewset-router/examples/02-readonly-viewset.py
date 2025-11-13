"""
02 - ReadOnlyModelViewSet misoli
Faqat o'qish uchun API (list va retrieve)
"""

from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin


# 1. ReadOnly ViewSet
class BookReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Faqat GET operatsiyalari:
    - list() - barcha kitoblar
    - retrieve() - bitta kitob
    
    POST, PUT, PATCH, DELETE - MAVJUD EMAS!
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# 2. GenericViewSet bilan qo'lda control
class CustomBookViewSet(viewsets.GenericViewSet):
    """
    Faqat kerakli action'larni qo'shamiz
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Faqat list va create qo'shamiz
    from rest_framework.mixins import ListModelMixin, CreateModelMixin
    
    
class LimitedBookViewSet(ListModelMixin, 
                         CreateModelMixin,
                         viewsets.GenericViewSet):
    """
    Faqat list va create mavjud
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# 3. ViewSet (eng minimal)
class MinimalViewSet(viewsets.ViewSet):
    """
    Hech qanday avtomatik funksional yo'q
    Hamma narsani qo'lda yozish kerak
    """
    
    def list(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)


# Router bilan:
"""
router = DefaultRouter()
router.register(r'books', BookReadOnlyViewSet)
router.register(r'limited-books', LimitedBookViewSet)
"""