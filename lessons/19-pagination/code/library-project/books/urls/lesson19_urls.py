"""Lesson 17-19 URLs - Nested Serializers, Filtering, Pagination"""
from django.urls import path
from books.views import (
    BookListCreateView,
    BookDetailView,
    BookFeedView,  # Yangi
    AuthorListView,
    AuthorDetailView,
    AuthorCreateView,
    AuthorUpdateView,
    AuthorDeleteView,
    GenreListCreateView,
    GenreDetailView,
)

urlpatterns = [
    # Book endpoints
    path('books/', BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/feed/', BookFeedView.as_view(), name='book-feed'),  # Yangi
    
    # Author endpoints
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/create/', AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('authors/<int:pk>/update/', AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', AuthorDeleteView.as_view(), name='author-delete'),
    
    # Genre endpoints
    path('genres/', GenreListCreateView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),
]