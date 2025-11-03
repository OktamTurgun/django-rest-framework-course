from django.urls import path
from .views import (
    BookListCreateView,
    BookDetailView,
    BookModelListCreateView,
    BookModelDetailView,
)

urlpatterns = [
    # ===== Oddiy Serializer endpoint'lari =====
    path('books/', BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # ===== ModelSerializer endpoint'lari =====
    path('books-model/', BookModelListCreateView.as_view(), name='book-model-list'),
    path('books-model/<int:pk>/', BookModelDetailView.as_view(), name='book-model-detail'),
]