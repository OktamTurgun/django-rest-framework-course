"""
02 - Custom Permissions
O'zingizning permission class'laringizni yaratish
"""

from rest_framework import permissions, viewsets
from .models import Book
from .serializers import BookSerializer


# ============================================
# 1. IsOwner - Faqat owner
# ============================================

class IsOwner(permissions.BasePermission):
    """
    Faqat owner operatsiya bajarishi mumkin
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Object-level check
        obj = Book instance
        """
        return obj.owner == request.user


# Usage
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


# ============================================
# 2. IsOwnerOrReadOnly - Owner o'zgartiradi, boshqalar o'qiydi
# ============================================

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    SAFE_METHODS (GET, HEAD, OPTIONS) - hamma
    Other methods - faqat owner
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions - hamma uchun
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions - faqat owner
        return obj.owner == request.user


# ============================================
# 3. IsAuthor - Author field bo'yicha
# ============================================

class IsAuthor(permissions.BasePermission):
    """
    Agar model'da 'author' field bo'lsa
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


# ============================================
# 4. IsPublishedOrOwner - Published/Unpublished logic
# ============================================

class IsPublishedOrOwner(permissions.BasePermission):
    """
    Complex logic:
    - Published books: hamma ko'ra oladi
    - Unpublished books: faqat owner ko'ra oladi
    - Modification: faqat owner
    """
    
    def has_object_permission(self, request, view, obj):
        # GET request
        if request.method in permissions.SAFE_METHODS:
            # Published - hamma ko'ra oladi
            if obj.published:
                return True
            # Unpublished - faqat owner
            return obj.owner == request.user
        
        # POST/PUT/DELETE - faqat owner
        return obj.owner == request.user


# ============================================
# 5. IsPremiumUser - User profile'ga asoslangan
# ============================================

class IsPremiumUser(permissions.BasePermission):
    """
    User profile'da 'is_premium' field bor deb faraz qilamiz
    """
    
    def has_permission(self, request, view):
        """
        View-level check (list, create)
        """
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and
            request.user.profile.is_premium
        )


# ============================================
# 6. IsOwnerOrAdmin - Owner yoki Admin
# ============================================

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Owner yoki staff user to'liq huquqlar
    Boshqalar faqat o'qiy oladi
    """
    
    def has_object_permission(self, request, view, obj):
        # Read - hamma
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Admin - hamma narsa
        if request.user.is_staff:
            return True
        
        # Owner - o'z obyektini
        return obj.owner == request.user


# ============================================
# 7. IsNotSuspended - Suspended user'lar uchun block
# ============================================

class IsNotSuspended(permissions.BasePermission):
    """
    User model'da 'is_suspended' field bor deb faraz qilamiz
    """
    message = "Your account has been suspended."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True  # Anonymous - boshqa permission tekshiradi
        
        return not getattr(request.user, 'is_suspended', False)


# ============================================
# 8. CanEditOwnOrPublished - Murakkab logic
# ============================================

class CanEditOwnOrPublished(permissions.BasePermission):
    """
    - O'z kitobini edit qilishi mumkin
    - Published kitoblarni edit qilishi mumkin (editor role)
    """
    
    def has_object_permission(self, request, view, obj):
        # Read - hamma
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Own book - edit qilishi mumkin
        if obj.owner == request.user:
            return True
        
        # Published books - editor'lar edit qilishi mumkin
        if obj.published and hasattr(request.user, 'profile'):
            return request.user.profile.role == 'editor'
        
        return False


# ============================================
# 9. TimeBasedPermission - Vaqtga bog'liq
# ============================================

from datetime import datetime, time

class BusinessHoursPermission(permissions.BasePermission):
    """
    Faqat ish vaqtida (9:00-18:00) operatsiya bajarish mumkin
    """
    message = "This operation is only allowed during business hours (9 AM - 6 PM)."
    
    def has_permission(self, request, view):
        now = datetime.now().time()
        start = time(9, 0)  # 9 AM
        end = time(18, 0)   # 6 PM
        
        return start <= now <= end


# ============================================
# 10. RateLimitPermission - Rate limiting
# ============================================

from django.core.cache import cache

class RateLimitPermission(permissions.BasePermission):
    """
    Har bir user 100 ta request/soat
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True
        
        cache_key = f'rate_limit_{request.user.id}'
        request_count = cache.get(cache_key, 0)
        
        if request_count >= 100:
            return False
        
        cache.set(cache_key, request_count + 1, 3600)  # 1 hour
        return True


# ============================================
# Best Practices
# ============================================

"""
1. Clear naming:
   IsOwner, IsOwnerOrReadOnly, IsPublished
   NOT: CustomPerm1, MyPermission

2. Docstrings:
   Har bir permission'da docstring yozing

3. Custom message:
   class MyPermission(BasePermission):
       message = "You don't have permission."

4. has_permission vs has_object_permission:
   has_permission - view-level (list, create)
   has_object_permission - object-level (retrieve, update, delete)

5. Combine with built-ins:
   permission_classes = [IsAuthenticated, IsOwner]

6. Test thoroughly:
   Har bir permission class uchun test yozing

7. Keep it simple:
   Permission logic murakkab bo'lsa, service layer'ga o'tkazing
"""


# ============================================
# Testing Custom Permissions
# ============================================

"""
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class PermissionTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', password='pass')
        self.user2 = User.objects.create_user('user2', password='pass')
        self.book = Book.objects.create(
            title='Test',
            owner=self.user1
        )
    
    def test_owner_can_delete(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, 204)
    
    def test_non_owner_cannot_delete(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, 403)
"""