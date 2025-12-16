from django.urls import path
from books.views.book_views import BookListCreateView, BookDetailView, BookFeedView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/feed/', BookFeedView.as_view(), name='book-feed'),
]
