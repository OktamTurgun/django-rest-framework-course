from django.urls import path
from .views import BookAPIListView, BookDetailAPIView, BookCreateAPIView, BookUpdateAPIView, BookDeleteAPIView

urlpatterns = [
  path('', BookAPIListView.as_view(), name='book-list'),
  path('create/', BookCreateAPIView.as_view(), name='book-create'),
  path('<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
  path('<int:pk>/update/', BookUpdateAPIView.as_view(), name='book-update'),
  path('<int:pk>/delete/', BookDeleteAPIView.as_view(), name='book-delete'),
]