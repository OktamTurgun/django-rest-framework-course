from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer


class BookListAPIView(APIView):
    """Barcha kitoblar ro'yxati va yangi kitob qo'shish"""
    
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(APIView):
    """Bitta kitob bilan ishlash: ko'rish, yangilash, o'chirish"""
    
    def get_object(self, pk):
        """Kitobni topish yoki 404 qaytarish"""
        return get_object_or_404(Book, pk=pk)
    
    def get(self, request, pk):
        """Bitta kitobni olish"""
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """Kitobni to'liq yangilash (barcha maydonlar kerak)"""
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        """Kitobni qisman yangilash (faqat kerakli maydonlar)"""
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Kitobni o'chirish"""
        book = self.get_object(pk)
        book.delete()
        return Response(
            {"message": "Kitob muvaffaqiyatli o'chirildi"},
            status=status.HTTP_204_NO_CONTENT
        )