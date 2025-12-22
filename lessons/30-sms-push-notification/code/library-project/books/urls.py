from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorViewSet, GenreViewSet, BookViewSet,
    UserProfileViewSet, BookLogListView,
    BorrowHistoryListView, MyBorrowHistoryView,
    BulkImportBooksView, ReviewViewSet
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

    # Router URLs
    path('', include(router.urls)),
]