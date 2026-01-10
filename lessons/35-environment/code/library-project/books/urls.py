from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorViewSet, GenreViewSet, BookViewSet,
    UserProfileViewSet, BookLogListView,
    BorrowHistoryListView, MyBorrowHistoryView,
    BulkImportBooksView, ReviewViewSet,
    export_books_excel,
    export_books_pdf,
    export_book_detail_pdf,
    generate_borrow_invoice,
    dashboard_stats,
    books_by_genre,
    books_by_author,
    popular_books,
    price_distribution,
    stock_analysis,
    recommendations,
    complete_analytics,
)

router = DefaultRouter()
router.register('authors', AuthorViewSet, basename='author')
router.register('genres', GenreViewSet, basename='genre')  # Genre, not Category
router.register('books', BookViewSet, basename='book')
router.register('profiles', UserProfileViewSet, basename='profile')
router.register('reviews', ReviewViewSet, basename='review')  # Added Review

urlpatterns = [

    # Custom endpoints
    path('logs/', BookLogListView.as_view(), name='book-logs'),
    path('borrow-history/', BorrowHistoryListView.as_view(), name='borrow-history'),
    path('my-borrows/', MyBorrowHistoryView.as_view(), name='my-borrows'),
    path('books/bulk-import/', BulkImportBooksView.as_view(), name='bulk-import'),

    # ============================================================================
    # EXPORT ENDPOINTS
    # ============================================================================
    path('export/excel/', export_books_excel, name='export-books-excel'),
    path('export/pdf/', export_books_pdf, name='export-books-pdf'),
    path('<int:pk>/export/pdf/', export_book_detail_pdf, name='export-book-detail-pdf'),
    
    # ============================================================================
    # ANALYTICS ENDPOINTS
    # ============================================================================
    path('analytics/dashboard/', dashboard_stats, name='analytics-dashboard'),
    path('analytics/by-genre/', books_by_genre, name='analytics-by-genre'),
    path('analytics/by-author/', books_by_author, name='analytics-by-author'),
    path('analytics/popular/', popular_books, name='analytics-popular'),
    path('analytics/price-distribution/', price_distribution, name='analytics-price-distribution'),
    path('analytics/stock-analysis/', stock_analysis, name='analytics-stock-analysis'),
    path('analytics/recommendations/', recommendations, name='analytics-recommendations'),
    path('analytics/complete/', complete_analytics, name='analytics-complete'),

    # Router URLs
    path('', include(router.urls)),
]