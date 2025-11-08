"""
Custom Permissions Example
DRF'da custom permission class'lar yaratish va ishlatish
"""

from rest_framework import permissions

# ============================================
# 1. IsOwnerOrReadOnly - Faqat egasi tahrirlashi mumkin
# ============================================

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission: faqat yaratuvchi tahrirlashi mumkin
    Boshqalar faqat o'qishi mumkin
    
    Ishlatish:
        class BookDetailView(APIView):
            permission_classes = [IsOwnerOrReadOnly]
    """
    
    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS - hamma uchun ruxsat
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # PUT, PATCH, DELETE - faqat egasi
        # obj.owner yoki obj.created_by bo'lishi mumkin
        return obj.created_by == request.user


# ============================================
# 2. IsAdminOrReadOnly - Faqat admin tahrirlashi mumkin
# ============================================

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin - barcha amallar
    Boshqalar - faqat o'qish
    
    Ishlatish:
        class BookListView(APIView):
            permission_classes = [IsAdminOrReadOnly]
    """
    
    def has_permission(self, request, view):
        # GET, HEAD, OPTIONS - hamma uchun
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # POST, PUT, PATCH, DELETE - faqat admin
        return request.user and request.user.is_staff


# ============================================
# 3. IsOwner - Faqat egasi
# ============================================

class IsOwner(permissions.BasePermission):
    """
    Faqat object egasi barcha amallarni bajara oladi
    
    Ishlatish:
        class ProfileView(APIView):
            permission_classes = [IsAuthenticated, IsOwner]
    """
    
    def has_object_permission(self, request, view, obj):
        # Faqat egasi
        return obj.user == request.user


# ============================================
# 4. IsStaffOrTargetUser - Staff yoki o'zi
# ============================================

class IsStaffOrTargetUser(permissions.BasePermission):
    """
    Staff foydalanuvchilar yoki o'zi (self)
    
    User profil uchun: har kim o'z profilini ko'radi/tahrirlaydi
    Admin esa barcha profillarni ko'radi/tahrirlaydi
    """
    
    def has_permission(self, request, view):
        # Authenticated bo'lishi kerak
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin - barchasi mumkin
        if request.user.is_staff:
            return True
        
        # O'zi - faqat o'zini
        return obj == request.user


# ============================================
# 5. ReadOnly - Faqat o'qish
# ============================================

class ReadOnly(permissions.BasePermission):
    """
    Hech kim o'zgartira olmaydi, faqat o'qish mumkin
    
    Ishlatish:
        class StatisticsView(APIView):
            permission_classes = [ReadOnly]
    """
    
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


# ============================================
# 6. IsAuthenticatedAndEmailVerified
# ============================================

class IsAuthenticatedAndEmailVerified(permissions.BasePermission):
    """
    Authenticated va email tasdiqlanган
    
    Ishlatish:
        class PremiumContentView(APIView):
            permission_classes = [IsAuthenticatedAndEmailVerified]
    """
    
    def has_permission(self, request, view):
        # Authenticated bo'lishi kerak
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Email verified bo'lishi kerak (custom field)
        # return request.user.is_email_verified
        return True  # Oddiy holat uchun


# ============================================
# 7. IsPremiumUser - Premium foydalanuvchi
# ============================================

class IsPremiumUser(permissions.BasePermission):
    """
    Premium a'zolik bor foydalanuvchilar uchun
    
    Ishlatish:
        class PremiumBooksView(APIView):
            permission_classes = [IsPremiumUser]
    """
    
    message = "Premium a'zolik talab qilinadi"
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Premium status tekshirish (custom field)
        # return request.user.is_premium
        return request.user.is_staff  # Demo uchun


# ============================================
# 8. IsOwnerOrAdmin - Egasi yoki Admin
# ============================================

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object egasi yoki admin
    
    Eng ko'p ishlatiladigan pattern
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin - hammasi mumkin
        if request.user.is_staff:
            return True
        
        # Egasi - o'zini
        return obj.created_by == request.user


# ============================================
# 9. CustomPermissionMixin - Mixin variant
# ============================================

class CustomPermissionMixin:
    """
    View'larda mixin sifatida ishlatish
    
    Ishlatish:
        class BookDetailView(CustomPermissionMixin, RetrieveAPIView):
            pass
    """
    
    def check_object_permissions(self, request, obj):
        """Override qilingan method"""
        super().check_object_permissions(request, obj)
        
        # Qo'shimcha tekshiruvlar
        if hasattr(obj, 'is_published'):
            if not obj.is_published and not request.user.is_staff:
                self.permission_denied(
                    request,
                    message="Bu content hali nashr qilinmagan"
                )


# ============================================
# 10. Bir nechta permission birga ishlatish
# ============================================

"""
Bir nechta permission class'larni birga ishlatish mumkin:

class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [
        IsAuthenticated,           # Authenticated bo'lishi kerak
        IsOwnerOrReadOnly,         # Va egasi bo'lishi kerak (tahrirlash uchun)
    ]

LOGIC:
- Barcha permission class'lar True qaytarishi kerak
- Agar bittasi False qaytarsa - ruxsat berilmaydi
- AND operatori kabi ishlaydi
"""


# ============================================
# 11. Custom permission message
# ============================================

class CustomMessagePermission(permissions.BasePermission):
    """
    Custom xato xabari bilan permission
    """
    
    message = "Sizda bu amalni bajarish uchun ruxsat yo'q!"
    
    def has_permission(self, request, view):
        # Biror logic
        return request.user.is_authenticated


# ============================================
# 12. REAL LIFE EXAMPLE - Blog Post
# ============================================

class BlogPostPermission(permissions.BasePermission):
    """
    Blog post uchun murakkab permission
    
    Rules:
    - Hamma published postlarni ko'rishi mumkin
    - Faqat authenticated user post yaratishi mumkin
    - Faqat muallif o'z postini tahrirlashi mumkin
    - Admin barchani tahrirlashi mumkin
    """
    
    def has_permission(self, request, view):
        # GET - hamma
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # POST - authenticated
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        
        # Boshqasi - object level'da tekshiriladi
        return True
    
    def has_object_permission(self, request, view, obj):
        # GET - published bo'lsa hamma, draft bo'lsa egasi
        if request.method in permissions.SAFE_METHODS:
            if obj.status == 'published':
                return True
            return obj.author == request.user
        
        # Admin - barchasi mumkin
        if request.user.is_staff:
            return True
        
        # PUT, PATCH, DELETE - faqat muallif
        return obj.author == request.user


# ============================================
# TEST FUNKSIYASI
# ============================================

def test_permissions():
    """
    Permission class'larni test qilish
    """
    print("=" * 60)
    print("CUSTOM PERMISSIONS TEST")
    print("=" * 60)
    
    # Mock objects
    class MockRequest:
        def __init__(self, user, method='GET'):
            self.user = user
            self.method = method
    
    class MockUser:
        def __init__(self, username, is_staff=False, is_authenticated=True):
            self.username = username
            self.is_staff = is_staff
            self.is_authenticated = is_authenticated
    
    class MockObject:
        def __init__(self, created_by):
            self.created_by = created_by
    
    # Test scenarios
    admin = MockUser('admin', is_staff=True)
    user1 = MockUser('user1')
    user2 = MockUser('user2')
    
    obj_by_user1 = MockObject(user1)
    
    # Test 1: IsOwnerOrReadOnly
    print("\n1️⃣  IsOwnerOrReadOnly Test")
    print("-" * 60)
    
    perm = IsOwnerOrReadOnly()
    
    # GET - user2 o'qiy oladi
    request = MockRequest(user2, 'GET')
    result = perm.has_object_permission(request, None, obj_by_user1)
    print(f"user2 GET: {result} ✅" if result else f"user2 GET: {result} ❌")
    
    # PUT - user1 tahrirlashi mumkin
    request = MockRequest(user1, 'PUT')
    result = perm.has_object_permission(request, None, obj_by_user1)
    print(f"user1 PUT: {result} ✅" if result else f"user1 PUT: {result} ❌")
    
    # PUT - user2 tahrirlay olmaydi
    request = MockRequest(user2, 'PUT')
    result = perm.has_object_permission(request, None, obj_by_user1)
    print(f"user2 PUT: {result} ❌" if not result else f"user2 PUT: {result} ✅")
    
    # Test 2: IsAdminOrReadOnly
    print("\n2️⃣  IsAdminOrReadOnly Test")
    print("-" * 60)
    
    perm = IsAdminOrReadOnly()
    
    # GET - user1 o'qiy oladi
    request = MockRequest(user1, 'GET')
    result = perm.has_permission(request, None)
    print(f"user1 GET: {result} ✅" if result else f"user1 GET: {result} ❌")
    
    # POST - user1 yarata olmaydi
    request = MockRequest(user1, 'POST')
    result = perm.has_permission(request, None)
    print(f"user1 POST: {result} ❌" if not result else f"user1 POST: {result} ✅")
    
    # POST - admin yarata oladi
    request = MockRequest(admin, 'POST')
    result = perm.has_permission(request, None)
    print(f"admin POST: {result} ✅" if result else f"admin POST: {result} ❌")
    
    print("\n" + "=" * 60)
    print("TEST TUGADI ✅")
    print("=" * 60)


# ============================================
# QANDAY ISHLATISH
# ============================================

"""
VIEWS.PY DA ISHLATISH:

from rest_framework import generics
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]


MODELS.PY DA ISHLATISH (yaratuvchini saqlash):

class Book(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # ...

VIEWS.PY DA YARATUVCHINI SAQLASH:

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
"""

# Django shell'da test qilish:
# exec(open('examples/custom_permissions_example.py').read())
# test_permissions()