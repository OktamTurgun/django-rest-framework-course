"""
Books Views - Django REST Framework
Lesson 16: Permissions Implementation

This file contains:
- Legacy APIView endpoints (for learning/reference)
- Modern ViewSet with Permissions (current approach)
"""

# ============================================
# IMPORTS
# ============================================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from books.models import Book
from books.serializers import (
    # Validation serializers (old lessons)
    BookFieldValidationSerializer,
    BookObjectValidationSerializer,
    BookCustomValidatorsSerializer,
    BookBuiltInValidatorsSerializer,
    BookCompleteValidationSerializer,
    BookHomeworkFieldValidationSerializer,
    BookHomeworkObjectValidationSerializer,
    
    # Current serializer
    BookSerializer,
)
from books.permissions import (
    IsOwnerOrReadOnly,
    IsPublishedOrOwner,
    IsOwnerOrAdmin,
)


# ============================================
# LEGACY APIVIEW ENDPOINTS
# (Kept for learning/reference - Lesson 8-11)
# ============================================

class BookFieldValidationListView(APIView):
    """
    Field-level validation bilan
    URL: /api/old/field-validation/
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
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
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookObjectValidationListView(APIView):
    """
    Object-level validation bilan
    URL: /api/old/object-validation/
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
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
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookCustomValidatorsListView(APIView):
    """
    Custom validators bilan
    URL: /api/old/custom-validators/
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
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookBuiltInValidatorsListView(APIView):
    """
    Built-in validators bilan
    URL: /api/old/builtin-validators/
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
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
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListCreateView(APIView):
    """
    Complete validation endpoint
    URL: /api/old/books/
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
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
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    """
    Single book operations
    URL: /api/old/books/<pk>/
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
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
    Homework: Field-level validation
    URL: /api/homework/field-validation/
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
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
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookHomeworkObjectValidationView(APIView):
    """
    Homework: Object-level validation
    URL: /api/homework/object-validation/
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
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
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================
# AUTHENTICATION TEST ENDPOINT
# ============================================

class ProtectedView(APIView):
    """
    Test authentication types
    URL: /api/protected/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Determine authentication type
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
# CURRENT APPROACH: VIEWSET WITH PERMISSIONS
# (Lesson 15 & 16)
# ============================================

class BookViewSet(viewsets.ModelViewSet):
    """
    Modern ViewSet for Book model with Permissions
    
    URL: /api/books/
    
    Permissions:
    - IsAuthenticatedOrReadOnly: GET - anyone, POST/PUT/DELETE - authenticated
    - IsOwnerOrReadOnly: Only owner can modify
    
    Standard Actions:
    - list: GET /api/books/ - Anyone
    - create: POST /api/books/ - Authenticated users (auto-set owner)
    - retrieve: GET /api/books/{id}/ - Anyone
    - update: PUT /api/books/{id}/ - Owner only
    - partial_update: PATCH /api/books/{id}/ - Owner only
    - destroy: DELETE /api/books/{id}/ - Owner only
    
    Custom Actions:
    - published: GET /api/books/published/ - Anyone
    - statistics: GET /api/books/statistics/ - Anyone
    - my_books: GET /api/books/my_books/ - Authenticated users
    - publish: POST /api/books/{id}/publish/ - Owner only
    - unpublish: POST /api/books/{id}/unpublish/ - Owner only
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Multiple permissions: BOTH must pass (AND logic)
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        """
        Automatically set owner when creating a book
        """
        serializer.save(owner=self.request.user)
    
    # ========== CUSTOM ACTIONS ==========
    
    @action(detail=False, methods=['get'])
    def published(self, request):
        """
        GET /api/books/published/
        Returns only published books
        Permission: Anyone
        """
        published_books = Book.objects.filter(published=True)
        serializer = self.get_serializer(published_books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        GET /api/books/statistics/
        Returns book statistics
        Permission: Anyone
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
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_books(self, request):
        """
        GET /api/books/my_books/
        Returns current user's books
        Permission: Authenticated users only
        """
        my_books = Book.objects.filter(owner=request.user)
        serializer = self.get_serializer(my_books, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def publish(self, request, pk=None):
        """
        POST /api/books/{id}/publish/
        Set book as published
        Permission: Owner only
        """
        book = self.get_object()
        book.published = True
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def unpublish(self, request, pk=None):
        """
        POST /api/books/{id}/unpublish/
        Set book as unpublished
        Permission: Owner only
        """
        book = self.get_object()
        book.published = False
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)


# ============================================
# ALTERNATIVE: DYNAMIC PERMISSIONS PER ACTION
# (Advanced example - for learning)
# ============================================

class BookViewSetWithDynamicPermissions(viewsets.ModelViewSet):
    """
    Example: ViewSet with action-based permissions
    
    Different permissions for different actions:
    - list: Anyone
    - create: Authenticated
    - retrieve: Anyone (if published) or Owner (if unpublished)
    - update/destroy: Owner or Admin
    
    NOTE: This is not used in URLs, kept as example
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Instantiate and return list of permissions for this action
        """
        if self.action == 'list':
            # Anyone can list books
            permission_classes = []
        elif self.action == 'create':
            # Only authenticated users can create
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            # Published or Owner
            permission_classes = [IsPublishedOrOwner]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Owner or Admin
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            # Default: authenticated or read-only
            permission_classes = [IsAuthenticatedOrReadOnly]
        
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Auto-set owner"""
        serializer.save(owner=self.request.user)


# ============================================
# SUMMARY
# ============================================
"""
Active ViewSets (used in urls.py):
- BookViewSet: Modern approach with permissions

Legacy Views (kept for reference):
- BookFieldValidationListView
- BookObjectValidationListView
- BookCustomValidatorsListView
- BookBuiltInValidatorsListView
- BookListCreateView
- BookDetailView
- BookHomeworkFieldValidationView
- BookHomeworkObjectValidationView
- ProtectedView

Example (not in URLs):
- BookViewSetWithDynamicPermissions
"""