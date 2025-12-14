"""
V2 API Views
Enhanced with filtering, search, and statistics
V2 API Views with Error Handling and Logging
"""
import logging
from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Max, Min, Sum
from datetime import date

from books.models import Book, Author, Genre, Review
from books.exceptions import (
    BookNotAvailableError,
    ISBNAlreadyExistsError,
    FutureDateError,
    NegativePriceError,
    BorrowLimitExceededError,
    InvalidISBNFormatError,
)
from .serializers import (
    BookListSerializerV2,
    BookDetailSerializerV2,
    AuthorSerializerV2,
    ReviewSerializerV2,
)
from .pagination import V2Pagination

# Get logger for this module
logger = logging.getLogger(__name__)


class BookListAPIView(generics.ListCreateAPIView):
    """
    V2: Enhanced Book List with filtering, search, ordering
    """
    queryset = Book.objects.select_related('author').prefetch_related('genres').all()
    pagination_class = V2Pagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['author', 'genres', 'language']
    search_fields = ['title', 'description', 'isbn_number']
    ordering_fields = ['title', 'price', 'published_date']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookListSerializerV2
        return BookDetailSerializerV2
    
    def list(self, request, *args, **kwargs):
        """List books with logging"""
        logger.info(
            f"Listing books",
            extra={
                'user': request.user.username if request.user.is_authenticated else 'anonymous',
                'filters': request.query_params.dict()
            }
        )
        
        try:
            response = super().list(request, *args, **kwargs)
            
            logger.info(
                f"Books listed successfully: {response.data.get('pagination', {}).get('count', 0)} results",
                extra={'count': response.data.get('pagination', {}).get('count', 0)}
            )
            
            return response
            
        except Exception as e:
            logger.error(
                f"Error listing books: {str(e)}",
                exc_info=True,
                extra={'user': request.user.username if request.user.is_authenticated else 'anonymous'}
            )
            raise
    
    def create(self, request, *args, **kwargs):
        """Create book with validation and logging"""
        logger.info(
            f"Creating book: {request.data.get('title')}",
            extra={
                'user': request.user.username,
                'title': request.data.get('title')
            }
        )
        
        try:
            # Validate ISBN
            isbn = request.data.get('isbn_number')
            if isbn:
                # Check format (basic validation)
                if not self.validate_isbn(isbn):
                    logger.warning(
                        f"Invalid ISBN format: {isbn}",
                        extra={'isbn': isbn, 'user': request.user.username}
                    )
                    raise InvalidISBNFormatError(
                        detail=f"Invalid ISBN format: {isbn}"
                    )
                
                # Check duplicate
                if Book.objects.filter(isbn_number=isbn).exists():
                    logger.warning(
                        f"ISBN already exists: {isbn}",
                        extra={'isbn': isbn, 'user': request.user.username}
                    )
                    raise ISBNAlreadyExistsError(
                        detail=f"Book with ISBN {isbn} already exists"
                    )
            
            # Validate published date
            published_date = request.data.get('published_date')
            if published_date:
                from datetime import datetime
                pub_date = datetime.strptime(str(published_date), '%Y-%m-%d').date()
                if pub_date > date.today():
                    logger.warning(
                        f"Future published date: {published_date}",
                        extra={'date': published_date, 'user': request.user.username}
                    )
                    raise FutureDateError(
                        detail="Published date cannot be in the future"
                    )
            
            # Validate price
            price = request.data.get('price')
            if price and float(price) < 0:
                logger.warning(
                    f"Negative price: {price}",
                    extra={'price': price, 'user': request.user.username}
                )
                raise NegativePriceError(
                    detail="Price must be a positive number"
                )
            
            # Create book
            response = super().create(request, *args, **kwargs)
            
            logger.info(
                f"Book created successfully: ID={response.data.get('id')}",
                extra={
                    'book_id': response.data.get('id'),
                    'title': response.data.get('title'),
                    'user': request.user.username
                }
            )
            
            return response
            
        except (InvalidISBNFormatError, ISBNAlreadyExistsError, 
                FutureDateError, NegativePriceError) as e:
            # These are already logged in exception handler
            raise
            
        except Exception as e:
            logger.error(
                f"Unexpected error creating book: {str(e)}",
                exc_info=True,
                extra={
                    'user': request.user.username,
                    'data': request.data
                }
            )
            raise
    
    def validate_isbn(self, isbn):
        """Basic ISBN validation"""
        # Remove hyphens and spaces
        isbn = isbn.replace('-', '').replace(' ', '')
        
        # Check length (ISBN-10 or ISBN-13)
        if len(isbn) not in [10, 13]:
            return False
        
        # Check if all characters are digits
        return isbn.isdigit()

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    V2: Enhanced Book Detail with nested objects
    """
    queryset = Book.objects.select_related('author').prefetch_related(
        'genres', 'reviews'
    ).all()
    serializer_class = BookDetailSerializerV2
    
    def retrieve(self, request, *args, **kwargs):
        """Get book detail with logging"""
        book_id = kwargs.get('pk')
        
        logger.info(
            f"Retrieving book: ID={book_id}",
            extra={'book_id': book_id, 'user': request.user.username if request.user.is_authenticated else 'anonymous'}
        )
        
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            
            logger.info(
                f"Book retrieved: {instance.title}",
                extra={'book_id': book_id, 'title': instance.title}
            )
            
            return Response({
                'version': 'v2',
                'data': serializer.data
            })
            
        except Exception as e:
            logger.error(
                f"Error retrieving book {book_id}: {str(e)}",
                exc_info=True,
                extra={'book_id': book_id}
            )
            raise
    
    def update(self, request, *args, **kwargs):
        """Update book with logging"""
        book_id = kwargs.get('pk')
        
        logger.info(
            f"Updating book: ID={book_id}",
            extra={
                'book_id': book_id,
                'user': request.user.username,
                'data': request.data
            }
        )
        
        try:
            response = super().update(request, *args, **kwargs)
            
            logger.info(
                f"Book updated successfully: ID={book_id}",
                extra={'book_id': book_id, 'user': request.user.username}
            )
            
            return response
            
        except Exception as e:
            logger.error(
                f"Error updating book {book_id}: {str(e)}",
                exc_info=True,
                extra={'book_id': book_id, 'user': request.user.username}
            )
            raise
    
    def destroy(self, request, *args, **kwargs):
        """Delete book with logging"""
        book_id = kwargs.get('pk')
        instance = self.get_object()
        
        logger.warning(
            f"Deleting book: ID={book_id}, Title={instance.title}",
            extra={
                'book_id': book_id,
                'title': instance.title,
                'user': request.user.username
            }
        )
        
        try:
            response = super().destroy(request, *args, **kwargs)
            
            logger.warning(
                f"Book deleted: ID={book_id}",
                extra={'book_id': book_id, 'user': request.user.username}
            )
            
            return response
            
        except Exception as e:
            logger.error(
                f"Error deleting book {book_id}: {str(e)}",
                exc_info=True,
                extra={'book_id': book_id, 'user': request.user.username}
            )
            raise

class BookStatisticsAPIView(APIView):
    """
    V2 Only: Book statistics endpoint
    """
    
    def get(self, request):
        """Get comprehensive book statistics"""
        logger.info(
            "Fetching book statistics",
            extra={'user': request.user.username if request.user.is_authenticated else 'anonymous'}
        )
        
        try:
            from books.models import Review
            
            # Book statistics
            book_stats = Book.objects.aggregate(
                total_books=Count('id'),
                average_price=Avg('price'),
                max_price=Max('price'),
                min_price=Min('price'),
                total_pages=Sum('pages'),
            )
            
            # Author statistics
            author_count = Author.objects.count()
            authors_with_books = Author.objects.annotate(
                book_count=Count('books')
            ).filter(book_count__gt=0).count()
            
            # Genre statistics
            genre_count = Genre.objects.count()
            
            # Review statistics
            review_stats = Review.objects.aggregate(
                total_reviews=Count('id'),
                average_rating=Avg('rating'),
                max_rating=Max('rating'),
                min_rating=Min('rating'),
            )
            
            # Books with reviews
            books_with_reviews = Book.objects.annotate(
                review_count=Count('reviews')
            ).filter(review_count__gt=0).count()
            
            statistics = {
                'version': 'v2',
                'statistics': {
                    'books': {
                        'total': book_stats['total_books'] or 0,
                        'average_price': round(float(book_stats['average_price']), 2) if book_stats['average_price'] else 0,
                        'max_price': float(book_stats['max_price']) if book_stats['max_price'] else 0,
                        'min_price': float(book_stats['min_price']) if book_stats['min_price'] else 0,
                        'total_pages': book_stats['total_pages'] or 0,
                        'with_reviews': books_with_reviews,
                    },
                    'authors': {
                        'total': author_count,
                        'with_books': authors_with_books,
                    },
                    'genres': {
                        'total': genre_count,
                    },
                    'reviews': {
                        'total': review_stats['total_reviews'] or 0,
                        'average_rating': round(float(review_stats['average_rating']), 2) if review_stats['average_rating'] else 0,
                        'max_rating': review_stats['max_rating'] or 0,
                        'min_rating': review_stats['min_rating'] or 0,
                    }
                }
            }
            
            logger.info(
                "Statistics fetched successfully",
                extra={'stats': statistics['statistics']}
            )
            
            return Response(statistics)
            
        except Exception as e:
            logger.error(
                f"Error fetching statistics: {str(e)}",
                exc_info=True
            )
            raise
class AuthorListAPIView(generics.ListCreateAPIView):
    """
    V2: Enhanced Author List with search
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializerV2
    pagination_class = V2Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email', 'bio']


class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    V2: Enhanced Author Detail
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializerV2
    
    def retrieve(self, request, *args, **kwargs):
        """Enhanced author detail"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'version': 'v2',
            'data': serializer.data
        })


class AuthorBooksAPIView(generics.ListAPIView):
    """
    V2: List all books by specific author
    """
    serializer_class = BookListSerializerV2
    pagination_class = V2Pagination
    
    def get_queryset(self):
        author_id = self.kwargs['pk']
        return Book.objects.filter(author_id=author_id).select_related(
            'author'
        ).prefetch_related('genres')
    
    def list(self, request, *args, **kwargs):
        """Custom response with author info"""
        author_id = self.kwargs['pk']
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(
                {'error': 'Author not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['author'] = {
                'id': author.id,
                'name': author.name,
                'total_books': queryset.count()
            }
            return response
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'version': 'v2',
            'author': {
                'id': author.id,
                'name': author.name,
                'total_books': queryset.count()
            },
            'books': serializer.data
        })


class APIMetricsView(APIView):
    """
    Admin only: API usage metrics
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        """Get API usage statistics"""
        from django.core.cache import cache
        from datetime import date, timedelta
        
        today = date.today()
        metrics = {}
        
        # Get last 7 days metrics
        for i in range(7):
            day = today - timedelta(days=i)
            v1_key = f'api_usage:v1:{day}'
            v2_key = f'api_usage:v2:{day}'
            
            metrics[str(day)] = {
                'v1': cache.get(v1_key, 0),
                'v2': cache.get(v2_key, 0)
            }
        
        return Response({
            'version': 'v2',
            'metrics': metrics,
            'message': 'Last 7 days API usage'
        })
    
class BookReviewsAPIView(generics.ListCreateAPIView):
    """
    V2: List and create reviews for a specific book
    """
    serializer_class = ReviewSerializerV2
    
    def get_queryset(self):
        """Filter reviews by book"""
        book_id = self.kwargs['pk']
        return Review.objects.filter(book_id=book_id).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Set book when creating review"""
        book_id = self.kwargs['pk']
        serializer.save(book_id=book_id)

class ErrorTestAPIView(APIView):
    """
    Test endpoint for error handling (Development only)
    """
    permission_classes = []  # No auth required for testing
    
    def get(self, request):
        """Test different error types"""
        error_type = request.query_params.get('type', 'generic')
        
        if error_type == 'isbn_duplicate':
            raise ISBNAlreadyExistsError(
                detail="Test: Book with ISBN 978-1234567890 already exists"
            )
        
        elif error_type == 'future_date':
            raise FutureDateError(
                detail="Test: Published date cannot be in the future"
            )
        
        elif error_type == 'negative_price':
            raise NegativePriceError(
                detail="Test: Price must be positive"
            )
        
        elif error_type == 'not_found':
            from rest_framework.exceptions import NotFound
            raise NotFound(detail="Test: Book not found")
        
        elif error_type == 'permission':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(detail="Test: Permission denied")
        
        elif error_type == 'server_error':
            # This will cause 500 error
            result = 1 / 0
        
        else:
            return Response({
                'message': 'Error test endpoint',
                'available_types': [
                    'isbn_duplicate',
                    'future_date',
                    'negative_price',
                    'not_found',
                    'permission',
                    'server_error'
                ]
            })