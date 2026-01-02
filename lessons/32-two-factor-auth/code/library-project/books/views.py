from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Book, Author, Genre, BookLog, BorrowHistory, Review
from accounts.models import Profile
from .serializers import (
    BookSerializer, AuthorSerializer, GenreSerializer,
    UserProfileSerializer, BookLogSerializer, BorrowHistorySerializer,
    ReviewSerializer, BulkImportBookSerializer
)
from .signals import borrow_book, return_book, books_bulk_imported


class AuthorViewSet(viewsets.ModelViewSet):
    """Author CRUD endpoints"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class GenreViewSet(viewsets.ModelViewSet):
    """Genre CRUD endpoints"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    """Book CRUD endpoints"""
    queryset = Book.objects.select_related('author').prefetch_related('genres').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):
        """
        Borrow a book
        
        POST /api/books/{id}/borrow/
        Body: {
            "days": 14  # optional, default 14
        }
        """
        book = self.get_object()
        user = request.user
        days = request.data.get('days', 14)
        
        try:
            history = borrow_book(book.id, user, days)
            serializer = BorrowHistorySerializer(history)
            return Response({
                'message': f'Book "{book.title}" borrowed successfully',
                'history': serializer.data
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        """
        Return a borrowed book
        
        POST /api/books/{id}/return_book/
        """
        book = self.get_object()
        user = request.user
        
        try:
            history = return_book(book.id, user)
            serializer = BorrowHistorySerializer(history)
            return Response({
                'message': f'Book "{book.title}" returned successfully',
                'history': serializer.data
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """User profile view endpoints"""
    queryset = Profile.objects.select_related('user').all()  # Changed
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        profile = get_object_or_404(Profile, user=request.user)  # Changed
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class BookLogListView(generics.ListAPIView):
    """
    List all book logs
    
    GET /api/logs/
    """
    queryset = BookLog.objects.select_related('user').all()
    serializer_class = BookLogSerializer
    permission_classes = [IsAdminUser]


class BorrowHistoryListView(generics.ListAPIView):
    """
    List borrow history
    
    GET /api/borrow-history/
    """
    queryset = BorrowHistory.objects.select_related('book', 'user').all()
    serializer_class = BorrowHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter by current user if not admin"""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class MyBorrowHistoryView(generics.ListAPIView):
    """
    Get current user's borrow history
    
    GET /api/my-borrows/
    """
    serializer_class = BorrowHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BorrowHistory.objects.filter(
            user=self.request.user
        ).select_related('book').order_by('-borrowed_at')


class BulkImportBooksView(APIView):
    """
    Bulk import books
    
    POST /api/books/bulk-import/
    Body: {
        "books": [
            {
                "title": "Book 1",
                "author": 1,
                "isbn_number": "1234567890123",
                "price": 29.99,
                "stock": 10
            },
            ...
        ]
    }
    """
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        serializer = BulkImportBookSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        books_data = serializer.validated_data['books']
        created_books = []
        errors = []
        
        for idx, book_data in enumerate(books_data):
            try:
                # Get author
                author_id = book_data.get('author')
                author = Author.objects.get(id=author_id)
                
                # Get genres (optional)
                genre_ids = book_data.get('genres', [])
                
                # Create book
                book = Book.objects.create(
                    title=book_data['title'],
                    author=author,
                    isbn_number=book_data['isbn_number'],
                    description=book_data.get('description', ''),
                    price=book_data['price'],
                    stock=book_data.get('stock', 0),
                    pages=book_data.get('pages', 0),
                    language=book_data.get('language', 'English'),
                    published_date=book_data.get('published_date', None)
                )
                
                # Add genres if provided
                if genre_ids:
                    book.genres.set(genre_ids)
                
                created_books.append(book)
                
            except Author.DoesNotExist:
                errors.append(f"Book #{idx + 1}: Author with ID {author_id} not found")
            except Genre.DoesNotExist:
                errors.append(f"Book #{idx + 1}: Genre not found")
            except Exception as e:
                errors.append(f"Book #{idx + 1}: {str(e)}")
        
        # Send signal
        if created_books:
            books_bulk_imported.send(
                sender=Book,
                count=len(created_books),
                user=request.user
            )
        
        # Prepare response
        response_data = {
            'imported': len(created_books),
            'failed': len(errors),
            'books': BookSerializer(created_books, many=True).data
        }
        
        if errors:
            response_data['errors'] = errors
        
        return Response(response_data, status=status.HTTP_201_CREATED)


class ReviewViewSet(viewsets.ModelViewSet):
    """Review CRUD endpoints"""
    queryset = Review.objects.select_related('book').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]