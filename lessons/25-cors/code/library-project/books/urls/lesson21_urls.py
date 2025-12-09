# books/urls/lesson21_urls.py
"""
Lesson 21 URLs - File Upload
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views.lesson_21_views import BookFileUploadViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'books', BookFileUploadViewSet, basename='book-upload')
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]