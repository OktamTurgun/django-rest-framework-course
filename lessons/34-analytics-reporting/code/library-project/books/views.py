from rest_framework import viewsets, generics, status
from rest_framework.decorators import action,api_view, permission_classes
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
from .search import BookSearch

# ============================================================================
# ANALYTICS & REPORTING VIEWS Lesson 34.
# ============================================================================

from .exports import ExcelExporter
from .reports import PDFReportGenerator
from .analytics import BookAnalytics


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
        
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Elasticsearch full-text search
        GET /api/books/search/?q=python&price_min=10&price_max=50&genre=Fiction
        """
        query = request.query_params.get('q', '')
        filters = {
            'price_min': request.query_params.get('price_min'),
            'price_max': request.query_params.get('price_max'),
            'genre': request.query_params.get('genre'),
            'author': request.query_params.get('author'),
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        search = BookSearch.search_books(query, filters)
        results = search.execute()
        
        return Response({
            'total': results.hits.total.value,
            'results': [
                {
                    'id': hit.meta.id,
                    'title': hit.title,
                    'author': hit.author.name if hasattr(hit, 'author') else None,
                    'price': hit.price,
                    'score': hit.meta.score,
                }
                for hit in results
            ]
        })
    
    @action(detail=False, methods=['get'])
    def autocomplete(self, request):
        """
        Autocomplete suggestions
        GET /api/books/autocomplete/?q=pyth
        """
        query = request.query_params.get('q', '')
        results = BookSearch.autocomplete(query)
        
        suggestions = []
        if hasattr(results, 'suggest') and 'title_suggestions' in results.suggest:
            for suggestion in results.suggest['title_suggestions'][0]['options']:
                suggestions.append(suggestion['text'])
        
        return Response({'suggestions': suggestions})


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

# ============================================================================
# ANALYTICS & REPORTING VIEWS Lesson 34.
# EXCEL EXPORT
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_books_excel(request):
    """
    Export books to Excel
    
    GET /api/books/export/excel/
    GET /api/books/export/excel/?author=John&genre=Programming&price_min=20
    """
    queryset = Book.objects.all()
    
    # Apply filters
    author = request.query_params.get('author')
    genre = request.query_params.get('genre')
    price_min = request.query_params.get('price_min')
    price_max = request.query_params.get('price_max')
    
    if author:
        queryset = queryset.filter(author__name__icontains=author)
    
    if genre:
        queryset = queryset.filter(genres__name__icontains=genre)
    
    if price_min:
        queryset = queryset.filter(price__gte=price_min)
    
    if price_max:
        queryset = queryset.filter(price__lte=price_max)
    
    # Generate Excel
    return ExcelExporter.export_books(queryset, filename="books_export.xlsx")


# ============================================================================
# PDF REPORTS
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_books_pdf(request):
    """
    Export books list to PDF
    
    GET /api/books/export/pdf/
    """
    queryset = Book.objects.all()
    
    # Apply filters (same as Excel)
    author = request.query_params.get('author')
    genre = request.query_params.get('genre')
    
    if author:
        queryset = queryset.filter(author__name__icontains=author)
    
    if genre:
        queryset = queryset.filter(genres__name__icontains=genre)
    
    return PDFReportGenerator.generate_books_report(queryset, filename="books_report.pdf")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_book_detail_pdf(request, pk):
    """
    Export single book details to PDF
    
    GET /api/books/{id}/export/pdf/
    """
    try:
        book = Book.objects.get(pk=pk)
        return PDFReportGenerator.generate_book_detail_report(book)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_borrow_invoice(request, pk):
    """
    Generate invoice PDF for borrow history
    
    GET /api/borrows/{id}/invoice/
    """
    try:
        borrow = BorrowHistory.objects.get(pk=pk)
        
        # Check permission (admin or owner)
        if not request.user.is_staff and borrow.user != request.user:
            return Response({'error': 'Permission denied'}, status=403)
        
        return PDFReportGenerator.generate_invoice(borrow)
    except BorrowHistory.DoesNotExist:
        return Response({'error': 'Borrow history not found'}, status=404)


# ============================================================================
# ANALYTICS ENDPOINTS
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics
    
    GET /api/analytics/dashboard/
    """
    stats = BookAnalytics.get_dashboard_stats()
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def books_by_genre(request):
    """
    Get books statistics by genre
    
    GET /api/analytics/by-genre/
    """
    genres = BookAnalytics.get_books_by_genre()
    
    data = [{
        'genre': g.name,
        'book_count': g.book_count,
        'avg_price': float(g.avg_price),
        'total_stock': g.total_stock,
        'min_price': float(g.min_price),
        'max_price': float(g.max_price),
        'total_value': float(g.total_value),
    } for g in genres]
    
    return Response({'by_genre': data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def books_by_author(request):
    """
    Get books statistics by author
    
    GET /api/analytics/by-author/
    """
    authors = BookAnalytics.get_books_by_author()
    
    data = [{
        'author': a.name,
        'book_count': a.book_count,
        'avg_price': float(a.avg_price),
        'total_stock': a.total_stock,
        'total_pages': a.total_pages,
        'avg_pages': float(a.avg_pages),
        'total_value': float(a.total_value),
    } for a in authors]
    
    return Response({'by_author': data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def popular_books(request):
    """
    Get popular books
    
    GET /api/analytics/popular/
    """
    limit = int(request.query_params.get('limit', 10))
    books = BookAnalytics.get_popular_books(limit=limit)
    
    data = [{
        'id': b.id,
        'title': b.title,
        'author': b.author.name if b.author else None,
        'price': float(b.price),
        'stock': b.stock,
    } for b in books]
    
    return Response({'popular_books': data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def price_distribution(request):
    """
    Get price distribution
    
    GET /api/analytics/price-distribution/
    """
    distribution = BookAnalytics.get_price_distribution()
    return Response(distribution)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stock_analysis(request):
    """
    Get stock analysis
    
    GET /api/analytics/stock-analysis/
    """
    analysis = BookAnalytics.get_stock_analysis()
    
    # Serialize queryset fields
    needs_restock = [{
        'id': b.id,
        'title': b.title,
        'author': b.author.name if b.author else None,
        'stock': b.stock,
    } for b in analysis['needs_restock']]
    
    highest_stock = [{
        'id': b.id,
        'title': b.title,
        'author': b.author.name if b.author else None,
        'stock': b.stock,
    } for b in analysis['highest_stock']]
    
    return Response({
        'status': analysis['status'],
        'needs_restock': needs_restock,
        'highest_stock': highest_stock,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendations(request):
    """
    Get actionable recommendations
    
    GET /api/analytics/recommendations/
    """
    recs = BookAnalytics.get_recommendations()
    return Response({'recommendations': recs})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def complete_analytics(request):
    """
    Get complete analytics (all in one)
    
    GET /api/analytics/complete/
    """
    return Response({
        'dashboard': BookAnalytics.get_dashboard_stats(),
        'price_distribution': BookAnalytics.get_price_distribution(),
        'genre_performance': {
            k: {
                'name': v.name,
                'book_count': v.book_count,
                'avg_price': float(v.avg_price),
            } if v else None
            for k, v in BookAnalytics.get_genre_performance().items()
        },
        'author_performance': {
            k: {
                'name': v.name,
                'book_count': v.book_count,
                'avg_price': float(v.avg_price),
            } if v else None
            for k, v in BookAnalytics.get_author_performance().items()
        },
        'recommendations': BookAnalytics.get_recommendations(),
    })