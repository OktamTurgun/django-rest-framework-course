"""
03 - Object-level Permissions
Har bir obyekt uchun alohida permission check
"""

from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book
from .serializers import BookSerializer


# ============================================
# Permission Flow
# ============================================

"""
Request → Authentication → Permission Check
                              ↓
                        has_permission()
                              ↓
                    has_object_permission()
                              ↓
                          Response

has_permission() - View-level check (list, create)
has_object_permission() - Object-level check (retrieve, update, delete)
"""


# ============================================
# 1. Basic Object-level Permission
# ============================================

class IsOwner(permissions.BasePermission):
    """
    Object-level: faqat owner
    """
    
    def has_object_permission(self, request, view, obj):
        """
        obj = Book instance
        request.user = current user
        """
        return obj.owner == request.user


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    """
    Flow:
    1. GET /api/books/ → has_permission() ✅
    2. GET /api/books/1/ → has_permission() ✅ → has_object_permission() ✅
    3. PUT /api/books/1/ → has_permission() ✅ → has_object_permission() ✅ or ❌
    """


# ============================================
# 2. Combined View & Object-level
# ============================================

class CanCreateAndEditOwn(permissions.BasePermission):
    """
    View-level: hamma authenticated user yarata oladi
    Object-level: faqat owner edit qila oladi
    """
    
    def has_permission(self, request, view):
        """
        View-level check
        list() va create() uchun
        """
        # Authenticated users can create
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Object-level check
        retrieve(), update(), destroy() uchun
        """
        # Only owner can modify
        return obj.owner == request.user


# ============================================
# 3. Different logic for different methods
# ============================================

class PublicReadPrivateWrite(permissions.BasePermission):
    """
    GET - hamma
    POST/PUT/DELETE - faqat owner
    """
    
    def has_permission(self, request, view):
        """
        View-level: GET - hamma, POST - authenticated
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Object-level: GET - hamma, PUT/DELETE - owner
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


# ============================================
# 4. Published/Unpublished Logic
# ============================================

class IsPublishedOrOwner(permissions.BasePermission):
    """
    GET:
      - Published: hamma ko'ra oladi
      - Unpublished: faqat owner
    POST/PUT/DELETE:
      - Faqat owner
    """
    
    def has_object_permission(self, request, view, obj):
        # Read request
        if request.method in permissions.SAFE_METHODS:
            # Published - public
            if obj.published:
                return True
            # Unpublished - owner only
            return obj.owner == request.user
        
        # Write request - owner only
        return obj.owner == request.user


# Usage
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsPublishedOrOwner]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ============================================
# 5. get_object() override
# ============================================

class BookViewSet(viewsets.ModelViewSet):
    """
    get_object() override qilish orqali
    queryset filter qilish
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """
        Retrieve single object
        Permission check'dan oldin queryset filter
        """
        obj = super().get_object()
        
        # Check permission
        if obj.owner != self.request.user and not obj.published:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You don't have permission to view this book.")
        
        return obj


# ============================================
# 6. get_queryset() override
# ============================================

class BookViewSet(viewsets.ModelViewSet):
    """
    get_queryset() override qilish orqali
    user'ga tegishli ma'lumotlarni ko'rsatish
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Har bir user faqat o'z kitoblarini ko'radi
        """
        user = self.request.user
        
        if user.is_staff:
            # Admin - barcha kitoblar
            return Book.objects.all()
        else:
            # Regular user - faqat o'z kitoblari
            return Book.objects.filter(owner=user)


# ============================================
# 7. Multiple Objects Permission
# ============================================

class CanDeleteMultiple(permissions.BasePermission):
    """
    Bulk delete uchun permission
    """
    
    def has_permission(self, request, view):
        if view.action == 'destroy_multiple':
            return request.user.is_staff
        return True


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, CanDeleteMultiple]
    
    @action(detail=False, methods=['delete'])
    def destroy_multiple(self, request):
        """
        DELETE /api/books/destroy_multiple/
        Body: {"ids": [1, 2, 3]}
        """
        ids = request.data.get('ids', [])
        
        # Permission check already done in CanDeleteMultiple
        deleted_count = Book.objects.filter(id__in=ids).delete()[0]
        
        return Response({
            'deleted_count': deleted_count,
            'ids': ids
        })


# ============================================
# 8. Field-level Permissions
# ============================================

class CanEditSensitiveFields(permissions.BasePermission):
    """
    Admin - barcha field'lar
    Owner - ba'zi field'lar
    """
    
    def has_object_permission(self, request, view, obj):
        # Sensitive fields faqat admin edit qila oladi
        sensitive_fields = {'published', 'featured', 'promoted'}
        
        if any(field in request.data for field in sensitive_fields):
            return request.user.is_staff
        
        # Other fields - owner edit qila oladi
        return obj.owner == request.user


# ============================================
# 9. Time-based Object Permission
# ============================================

from datetime import datetime, timedelta

class CanEditRecent(permissions.BasePermission):
    """
    Faqat oxirgi 24 soat ichida yaratilgan kitoblarni edit qilish mumkin
    """
    message = "You can only edit books created within the last 24 hours."
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Owner check
        if obj.owner != request.user:
            return False
        
        # Time check
        time_limit = datetime.now() - timedelta(hours=24)
        return obj.created_at >= time_limit


# ============================================
# 10. Related Object Permissions
# ============================================

class CanAccessRelated(permissions.BasePermission):
    """
    Related object'ga access bo'lsa, main object'ga ham access bor
    Masalan: Book'ka access bo'lsa, uning Comment'lariga ham access
    """
    
    def has_object_permission(self, request, view, obj):
        # obj = Comment instance (Book'ga related)
        # Comment'ning book'iga access bormi?
        
        if hasattr(obj, 'book'):
            # Book owner yoki published bo'lsa
            return (
                obj.book.owner == request.user or 
                obj.book.published
            )
        
        return True


# ============================================
# Testing Object-level Permissions
# ============================================

"""
from rest_framework.test import APITestCase

class ObjectPermissionTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1')
        self.user2 = User.objects.create_user('user2')
        self.book = Book.objects.create(title='Test', owner=self.user1)
    
    def test_owner_can_view(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_non_owner_cannot_edit(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(f'/api/books/{self.book.id}/', {'title': 'New'})
        self.assertEqual(response.status_code, 403)
    
    def test_published_book_public(self):
        self.book.published = True
        self.book.save()
        
        # Anonymous can view
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, 200)
"""


# ============================================
# Best Practices
# ============================================

"""
1. Always check object ownership:
   return obj.owner == request.user

2. Handle anonymous users:
   if not request.user.is_authenticated:
       return False

3. Check object existence:
   ViewSet automatically raises 404, but be careful in custom views

4. Performance consideration:
   get_queryset() is better than has_object_permission() for filtering

5. Clear error messages:
   class MyPermission(BasePermission):
       message = "Clear explanation of why access is denied"

6. Test edge cases:
   - Anonymous users
   - Owner vs non-owner
   - Published vs unpublished
   - Admin override
"""