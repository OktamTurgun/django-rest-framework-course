"""
V2 API URLs
"""
from django.urls import path
from . import views

app_name = 'v2'

urlpatterns = [
    # Books
    path('books/', views.BookListAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailAPIView.as_view(), name='book-detail'),
    path('books/<int:pk>/reviews/', views.BookReviewsAPIView.as_view(), name='book-reviews'),  
    path('books/statistics/', views.BookStatisticsAPIView.as_view(), name='book-statistics'),
    
    # Authors
    path('authors/', views.AuthorListAPIView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailAPIView.as_view(), name='author-detail'),
    path('authors/<int:pk>/books/', views.AuthorBooksAPIView.as_view(), name='author-books'),
    
    # Metrics (Admin only)
    path('metrics/', views.APIMetricsView.as_view(), name='api-metrics'),
    # Error Testing Endpoint
    path('test-errors/', views.ErrorTestAPIView.as_view(), name='test-errors'),
]