from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import (
    BookFieldValidationSerializer,
    BookHomeworkObjectValidationSerializer,
    BookObjectValidationSerializer,
    BookCustomValidatorsSerializer,
    BookBuiltInValidatorsSerializer,
    BookCompleteValidationSerializer,
    
    # Homework serializer
    BookHomeworkFieldValidationSerializer,
    BookHomeworkObjectValidationSerializer,
)

from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Book
from .serializers import BookSerializer

# ============================================
# FIELD-LEVEL VALIDATION ENDPOINTS
# ============================================

class BookFieldValidationListView(APIView):
    """
    Field-level validation bilan
    URL: /api/books/field-validation/
    """
    permission_classes = [IsAuthenticatedOrReadOnly]  # YANGI
    
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
    permission_classes = [IsAuthenticatedOrReadOnly]  # YANGI
    
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
    permission_classes = [IsAuthenticatedOrReadOnly] 
    
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
    permission_classes = [IsAuthenticatedOrReadOnly]  # GET - hamma, POST - faqat auth
    
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
    permission_classes = [IsAuthenticatedOrReadOnly]  # YANGI QO'SHDIK
    
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
    
# ============================================
# HOMEWORK ENDPOINTS
# ============================================

class BookHomeworkFieldValidationView(APIView):
    """
    Homework Vazifa 1: Field-level validation test
    URL: /api/homework/field-validation/
    """
    
    def get(self, request):
        books = Book.objects.all()
        serializer = BookHomeworkFieldValidationSerializer(books, many=True)
        return Response({
            'message': 'Homework: Field-level validation',
            'count': len(serializer.data),
            'results': serializer.data
        })
    
    def post(self, request):
        serializer = BookHomeworkFieldValidationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookHomeworkObjectValidationView(APIView):
    """
    Homework Vazifa 2: Object-level validation test
    URL: /api/homework/object-validation/
    """
    
    def get(self, request):
        books = Book.objects.all()
        serializer = BookHomeworkObjectValidationSerializer(books, many=True)
        return Response({
            'message': 'Homework: Object-level validation',
            'count': len(serializer.data),
            'results': serializer.data
        })
    
    def post(self, request):
        serializer = BookHomeworkObjectValidationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# ============================================
# PROTECTED VIEW TO TEST AUTHENTICATION TYPES
# ============================================
class ProtectedView(APIView):
    """
    Faqat autentifikatsiya qilingan foydalanuvchilar uchun
    Bu endpoint autentifikatsiya turlarini test qilish uchun
    
    GET /api/books/protected/
    Header: Authorization: Token <token>
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Qaysi autentifikatsiya turi ishlatilganini aniqlash
        auth_type = 'Unknown'
        
        if request.auth:
            auth_type = request.auth.__class__.__name__
        elif request.user.is_authenticated:
            auth_type = 'Session'
            
        return Response({
            'message': 'Siz muvaffaqiyatli autentifikatsiya qildingiz!',
            'user': request.user.username,
            'user_id': request.user.pk,
            'email': request.user.email,
            'auth_method': auth_type,
            'is_staff': request.user.is_staff
        })
    
# ============================================
# 3. ModelViewSet (Eng ko'p ishlatiladigan)
# Lesson 15 ViewSet va Router
# ============================================

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book model
    Barcha CRUD operatsiyalarini ta'minlaydi:
    - list (GET /api/books/)
    - retrieve (GET /api/books/{id}/)
    - create (POST /api/books/)
    - update (PUT /api/books/{id}/)
    - partial_update (PATCH /api/books/{id}/)
    - destroy (DELETE /api/books/{id}/)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Custom action: Faqat published kitoblarni ko'rsatish
    @action(detail=False, methods=['get'])
    def published(self, request):
        """
        GET /api/books/published/
        Faqat published=True bo'lgan kitoblarni qaytaradi
        """
        published_books = Book.objects.filter(published=True)
        serializer = self.get_serializer(published_books, many=True)
        return Response(serializer.data)
    
    # Custom action: Kitob statistikasi
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        GET /api/books/statistics/
        Kitoblar statistikasini qaytaradi
        """
        total_books = Book.objects.count()
        published_books = Book.objects.filter(published=True).count()
        unpublished_books = total_books - published_books
        
        data = {
            'total_books': total_books,
            'published_books': published_books,
            'unpublished_books': unpublished_books,
        }
        return Response(data)
    
    # Custom action: Bitta kitobni publish qilish
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        """
        POST /api/books/{id}/publish/
        Kitobni published=True qiladi
        """
        book = self.get_object()
        book.published = True
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    # Custom action: Bitta kitobni unpublish qilish
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unpublish(self, request, pk=None):
        """
        POST /api/books/{id}/unpublish/
        Kitobni published=False qiladi
        """
        book = self.get_object()
        book.published = False
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)