"""
V2 API Views
Enhanced with filtering, search, and statistics
"""
from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from books.models import Book, Author, Review
from .serializers import (
    BookListSerializerV2,
    BookDetailSerializerV2,
    AuthorSerializerV2,
    ReviewSerializerV2
)
from .pagination import V2Pagination


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
    search_fields = ['title', 'description', 'isbn']
    ordering_fields = ['title', 'price', 'published_date', 'average_rating']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookListSerializerV2
        return BookDetailSerializerV2


class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    V2: Enhanced Book Detail with nested objects
    """
    queryset = Book.objects.select_related('author').prefetch_related(
        'genres', 'reviews'
    ).all()
    serializer_class = BookDetailSerializerV2
    
    def retrieve(self, request, *args, **kwargs):
        """Enhanced detail response"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'version': 'v2',
            'data': serializer.data
        })


class BookStatisticsAPIView(APIView):
    """
    V2 Only: Book statistics endpoint
    GET: Returns overall statistics
    """
    
    def get(self, request):
        """Get comprehensive book statistics"""
        from django.db.models import Avg, Count, Max, Min, Sum
        from books.models import Review, Genre
        
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
        
        return Response({
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
        })

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