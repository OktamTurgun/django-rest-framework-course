from django.urls import path
from .views import (
    BookListAPIView, BookDetailAPIView, BookCreateAPIView,
    BookUpdateAPIView, BookDeleteAPIView, BookListCreateAPIView,
    BookRetrieveUpdateAPIView, BookRetrieveDestroyAPIView,
    BookRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('list/', BookListAPIView.as_view(), name='book-list'),
    path('<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('create/', BookCreateAPIView.as_view(), name='book-create'),
    path('<int:pk>/update/', BookUpdateAPIView.as_view(), name='book-update'),
    path('<int:pk>/delete/', BookDeleteAPIView.as_view(), name='book-delete'),

    # Kombinatsiyalangan genericlar
    path('list-create/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('<int:pk>/retrieve-update/', BookRetrieveUpdateAPIView.as_view(), name='book-retrieve-update'),
    path('<int:pk>/retrieve-destroy/', BookRetrieveDestroyAPIView.as_view(), name='book-retrieve-destroy'),
    path('<int:pk>/full/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-full'),
]
