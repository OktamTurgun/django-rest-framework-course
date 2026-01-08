"""
V1 API URLs
"""
from django.urls import path
from . import views

app_name = 'v1'

urlpatterns = [
    # Books
    path('books/', views.BookListAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailAPIView.as_view(), name='book-detail'),
    
    # Authors
    path('authors/', views.AuthorListAPIView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailAPIView.as_view(), name='author-detail'),
     path('authors/<int:pk>/books/', views.AuthorBooksAPIView.as_view(), name='author-books'),
]