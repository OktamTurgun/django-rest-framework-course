"""Lesson 20 URLs - Throttling with ViewSets"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views.lesson_20_views import BookViewSet, AuthorViewSet

# Router yaratish
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'authors', AuthorViewSet, basename='author')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
]