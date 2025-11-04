from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import (
    BookFieldValidationSerializer,
    BookObjectValidationSerializer,
    BookCustomValidatorsSerializer,
    BookBuiltInValidatorsSerializer,
    BookCompleteValidationSerializer,
)


# ============================================
# FIELD-LEVEL VALIDATION ENDPOINTS
# ============================================

class BookFieldValidationListView(APIView):
    """
    Field-level validation bilan
    URL: /api/books/field-validation/
    """
    
    def get(self, request):
        books = Book.objects.all()
        serializer = BookFieldValidationSerializer(books, many=True)
        return Response({
            'message': 'Field-level validation',
            'count': len(serializer.data),
            'results': serializer.data
        })
    
    def post(self, request):
        serializer = BookFieldValidationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================
# OBJECT-LEVEL VALIDATION ENDPOINTS
# ============================================

class BookObjectValidationListView(APIView):
    """
    Object-level validation bilan
    URL: /api/books/object-validation/
    """
    
    def get(self, request):
        books = Book.objects.all()
        serializer = BookObjectValidationSerializer(books, many=True)
        return Response({
            'message': 'Object-level validation',
            'count': len(serializer.data),
            'results': serializer.data
        })
    
    def post(self, request):
        serializer = BookObjectValidationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================
# CUSTOM VALIDATORS ENDPOINTS
# ============================================

class BookCustomValidatorsListView(APIView):
    """
    Custom validators bilan
    URL: /api/books/custom-validators/
    """
    
    def get(self, request):
        books = Book.objects.all()
        serializer = BookCustomValidatorsSerializer(books, many=True)
        return Response({
            'message': 'Custom validators',
            'count': len(serializer.data),
            'results': serializer.data
        })
    
    def post(self, request):
        serializer = BookCustomValidatorsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================
# BUILT-IN VALIDATORS ENDPOINTS
# ============================================

class BookBuiltInValidatorsListView(APIView):
    """
    Built-in validators bilan
    URL: /api/books/builtin-validators/
    """
    
    def get(self, request):
        books = Book.objects.all()
        serializer = BookBuiltInValidatorsSerializer(books, many=True)
        return Response({
            'message': 'Built-in validators',
            'count': len(serializer.data),
            'results': serializer.data
        })
    
    def post(self, request):
        serializer = BookBuiltInValidatorsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================
# COMPLETE VALIDATION (ASOSIY ENDPOINT)
# ============================================

class BookListCreateView(APIView):
    """
    Barcha validation'lar bilan
    URL: /api/books/
    """
    
    def get(self, request):
        books = Book.objects.all()
        serializer = BookCompleteValidationSerializer(books, many=True)
        return Response({
            'message': 'Complete validation (field + object + custom)',
            'count': len(serializer.data),
            'results': serializer.data
        })
    
    def post(self, request):
        serializer = BookCompleteValidationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    """
    Bitta kitob bilan ishlash
    URL: /api/books/<pk>/
    """
    
    def get_object(self, pk):
        return get_object_or_404(Book, pk=pk)
    
    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookCompleteValidationSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookCompleteValidationSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        book = self.get_object(pk)
        serializer = BookCompleteValidationSerializer(book, data=request.data, partial=True)
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