"""
Custom Permissions for Books API
Lesson 16: Permissions
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Faqat obyekt egasiga uni tahrirlashga ruxsat beradigan maxsus permission.
    
    - GET, HEAD, OPTIONS: Barchaga (hatto anonim foydalanuvchilarga ham)
    - POST, PUT, PATCH, DELETE: Faqat obyekt egasiga
    
    Qo‘llanishi:
        class BookViewSet(viewsets.ModelViewSet):
            permission_classes = [IsOwnerOrReadOnly]
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.owner == request.user


class IsOwner(permissions.BasePermission):
    """
    Faqat obyekt egasiga unga murojaat qilishga ruxsat beradigan maxsus permission.
    
    - Barcha metodlar: Faqat obyekt egasi
    
    Qo‘llanishi:
        class BookViewSet(viewsets.ModelViewSet):
            permission_classes = [IsAuthenticated, IsOwner]
    """
    
    def has_object_permission(self, request, view, obj):
        # All permissions only for the owner
        return obj.owner == request.user


class IsPublishedOrOwner(permissions.BasePermission):
    """
    Nashr qilingan yoki qilinmagan kontent uchun maxsus permission.
    
    Mantiq:
    - GET so‘rovi:
        - Nashr qilingan kitoblar: Barchaga o‘qishga ruxsat
        - Nashr qilinmagan kitoblar: Faqat egasi o‘qiy oladi
    - POST, PUT, PATCH, DELETE:
        - Faqat egasi o‘zgartirishi mumkin
    
    Qo‘llanishi:
        class BookViewSet(viewsets.ModelViewSet):
            permission_classes = [IsPublishedOrOwner]
    """

    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            # Published books - anyone can read
            if obj.published:
                return True
            # Unpublished books - only owner can read
            return obj.owner == request.user
        
        # POST, PUT, PATCH, DELETE - only owner
        return obj.owner == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Faqat egasi yoki admin foydalanuvchiga obyektni o‘zgartirishga ruxsat beradigan maxsus permission.
    
    Mantiq:
    - GET, HEAD, OPTIONS: Barchaga ruxsat
    - POST, PUT, PATCH, DELETE:
        - Admin (is_staff=True): To‘liq ruxsat
        - Egasi: Faqat o‘z obyektlarini o‘zgartirishi mumkin
        - Boshqalar: Ruxsat berilmaydi
    
    Qo‘llanishi:
        class BookViewSet(viewsets.ModelViewSet):
            permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]
    """

    def has_object_permission(self, request, view, obj):
        # Xar qanday foydalanuvchi uchun o'qish ruxsatlari
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Adminlar to'liq ruxsatga ega
        if request.user.is_staff:
            return True
        
        # Faqat egasi o‘z obyektlarini o‘zgartirishi mumkin
        return obj.owner == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Faqat admin foydalanuvchiga o‘zgartirish qilishga ruxsat beradigan maxsus permission.
    
    - GET, HEAD, OPTIONS: Barchaga ruxsat
    - POST, PUT, PATCH, DELETE: Faqat admin
    
    Qo‘llanishi:
        class BookViewSet(viewsets.ModelViewSet):
            permission_classes = [IsAdminOrReadOnly]
    """

    def has_permission(self, request, view):
        # Xar qanday foydalanuvchi uchun o'qish ruxsatlari
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Yozish ruxsatlari - faqat admin
        return request.user and request.user.is_staff