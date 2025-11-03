from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import (
    BookSerializer,
    BookModelSerializer,
    BookListSerializer,
    BookDetailSerializer
)


# ============================================
# ODDIY SERIALIZER BILAN ISHLASH
# ============================================

class BookListCreateView(APIView):
    """
    Oddiy Serializer bilan ishlash
    URL: /api/books/
    """
    
    def get(self, request):
        """Barcha kitoblar ro'yxati"""
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({
            'message': 'Oddiy Serializer ishlatildi',
            'count': len(serializer.data),
            'results': serializer.data
        })
    
    def post(self, request):
        """Yangi kitob yaratish"""
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    """
    Oddiy Serializer bilan detail view
    URL: /api/books/<pk>/
    """
    
    def get_object(self, pk):
        return get_object_or_404(Book, pk=pk)
    
    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response({
            'message': 'Oddiy Serializer ishlatildi',
            'data': serializer.data
        })
    
    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(
            {"message": "Kitob muvaffaqiyatli o'chirildi"},
            status=status.HTTP_204_NO_CONTENT
        )


# ============================================
# MODEL SERIALIZER BILAN ISHLASH
# ============================================

class BookModelListCreateView(APIView):
    """
    ModelSerializer bilan ishlash
    URL: /api/books-model/
    """
    
    def get(self, request):
        """Barcha kitoblar (sodda format)"""
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)
        return Response({
            'message': 'ModelSerializer (List) ishlatildi',
            'count': len(serializer.data),
            'results': serializer.data
        })
    
    def post(self, request):
        """Yangi kitob yaratish"""
        serializer = BookModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookModelDetailView(APIView):
    """
    ModelSerializer bilan detail view
    URL: /api/books-model/<pk>/
    To'liq ma'lumot va qo'shimcha fieldlar bilan
    """
    
    def get_object(self, pk):
        return get_object_or_404(Book, pk=pk)
    
    def get(self, request, pk):
        """Bitta kitob (to'liq ma'lumot)"""
        book = self.get_object(pk)
        serializer = BookDetailSerializer(book)
        return Response({
            'message': 'ModelSerializer (Detail) ishlatildi',
            'data': serializer.data
        })
    
    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookModelSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        book = self.get_object(pk)
        serializer = BookModelSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(
            {"message": "Kitob muvaffaqiyatli o'chirildi"},
            status=status.HTTP_204_NO_CONTENT
        )