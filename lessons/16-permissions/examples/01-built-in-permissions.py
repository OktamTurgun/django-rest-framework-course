"""
01 - Built-in Permissions
Django REST Framework'ning o'rnatilgan permission class'lari
"""

from rest_framework import viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from .models import Book
from .serializers import BookSerializer


# ============================================
# 1. AllowAny - Hamma uchun ochiq
# ============================================

class PublicBookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public API - hamma ko'ra oladi, hech kim o'zgartira olmaydi
    
    Use case: News, blog posts, public catalog
    """
    queryset = Book.objects.filter(published=True)
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Default, lekin explicit yaxshiroq


# ============================================
# 2. IsAuthenticated - Faqat login qilganlar
# ============================================

class PrivateBookViewSet(viewsets.ModelViewSet):
    """
    Private API - faqat authenticated users
    
    Use case: Internal tools, user dashboard
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ============================================
# 3. IsAuthenticatedOrReadOnly - Eng ko'p ishlatiladigan ⭐
# ============================================

class BookViewSet(viewsets.ModelViewSet):
    """
    Hybrid approach - o'qish hamma uchun, yozish faqat authenticated
    
    Use case: Blog, forum, e-commerce product catalog
    
    GET - hamma (anonymous ham)
    POST/PUT/DELETE - faqat authenticated
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ============================================
# 4. IsAdminUser - Faqat admin
# ============================================

class AdminBookViewSet(viewsets.ModelViewSet):
    """
    Admin-only API
    
    Use case: Admin dashboard, system management
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]


# ============================================
# 5. DjangoModelPermissions - Django permission system
# ============================================

from rest_framework.permissions import DjangoModelPermissions

class PermissionBasedBookViewSet(viewsets.ModelViewSet):
    """
    Django'ning built-in permission system bilan
    
    Permission kerak:
    - View: books.view_book
    - Add: books.add_book
    - Change: books.change_book
    - Delete: books.delete_book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [DjangoModelPermissions]


# ============================================
# Test Scenarios
# ============================================

"""
1. AllowAny:
   GET /api/public-books/ → 200 (anyone)
   POST /api/public-books/ → 405 (ReadOnly)

2. IsAuthenticated:
   GET /api/private-books/ → 401 (anonymous)
   GET /api/private-books/ → 200 (authenticated)

3. IsAuthenticatedOrReadOnly:
   GET /api/books/ → 200 (anyone)
   POST /api/books/ → 401 (anonymous)
   POST /api/books/ → 201 (authenticated)

4. IsAdminUser:
   GET /api/admin-books/ → 403 (regular user)
   GET /api/admin-books/ → 200 (admin user)

5. DjangoModelPermissions:
   Depends on user permissions in admin panel
"""


# ============================================
# URLs configuration
# ============================================

"""
# urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'public-books', PublicBookViewSet)
router.register(r'private-books', PrivateBookViewSet)
router.register(r'books', BookViewSet)
router.register(r'admin-books', AdminBookViewSet)
router.register(r'permission-books', PermissionBasedBookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
"""


# ============================================
# Best Practices
# ============================================

"""
1. Default Permission (settings.py):
   REST_FRAMEWORK = {
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticatedOrReadOnly',
       ]
   }

2. Explicit is better than implicit:
   Always set permission_classes explicitly in ViewSet

3. Most common choice: IsAuthenticatedOrReadOnly
   90% of APIs use this permission

4. Never use AllowAny in production for write operations
   GET - OK
   POST/PUT/DELETE - DANGEROUS!

5. IsAdminUser for sensitive operations only
   User management, system settings, etc.
"""