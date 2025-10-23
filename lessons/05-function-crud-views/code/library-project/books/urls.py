from django.urls import path
from .views import BookAPIListView

urlpatterns = [
  path('', BookAPIListView.as_view(), name='book-list'),
]