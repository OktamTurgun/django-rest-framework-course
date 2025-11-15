"""
04 - Combining Permissions
Bir nechta permissionlarni birlashtirish:
- AND
- OR
- NOT
- Method-level combining
- Built-in + custom permission mix
"""

from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime, time
from .models import Book
from .serializers import BookSerializer


# ============================================
# Permissionlarni birlashtirish mantiqlari
# ============================================

"""
DRF default:
permission_classes = [A, B]

Bu -> A AND B (ikkalasi ham True bo'lishi shart)

Boshqa usullar:
1) OR kombinatsiya uchun:
   permission_classes = [A | B]

2) AND kombinatsiya uchun:
   permission_classes = [A & B]

3) NOT (inkor):
   permission_classes = [~A]

4) Multiple:
   permission_classes = [(A | B) & (~C)]

5) Method-level mixing:
   def get_permissions():
       if method == "GET": return [AllowAny()]
       if method == "POST": return [IsAuthenticated()]
"""


# ============================================
# 1. Oddiy ikki permission: AND (default)
# ============================================

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsEmailConfirmed(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, "email_confirmed", False)


class BookAdminOnlyView(viewsets.ModelViewSet):
    """
    IsAdmin AND IsEmailConfirmed → har ikkisi True bo'lishi shart
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdmin, IsEmailConfirmed]


# ============================================
# 2. OR kombinatsiyasi: A yoki B
# ============================================

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsPublic(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.published


class BookView_OR(viewsets.ModelViewSet):
    """
    Owner OR Published:
    - Agar owner bo'lsa → True
    - Yoki published bo'lsa → True
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwner | IsPublic]


# ============================================
# 3. Complex combination: (A OR B) AND C
# ============================================

class IsStaffOrOwner(permissions.BasePermission):
    """
    Staff yoki owner
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.owner == request.user


class BookView_Complex(viewsets.ModelViewSet):
    """
    (IsStaff OR IsOwner) AND IsEmailConfirmed
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [(IsStaffOrOwner | IsPublic) & IsEmailConfirmed]


# ============================================
# 4. NOT operatori (~)
# ============================================

class IsBanned(permissions.BasePermission):
    """
    Ban qilingan userlar
    """
    def has_permission(self, request, view):
        return getattr(request.user, "banned", False)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ~IsBanned → Banned bo'lmaganlar kiradi
    """
    permission_classes = [~IsBanned]


# ============================================
# 5. Method-level Combining (dynamic permission)
# ============================================

class BookMethodLevelView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        """
        GET: public
        POST: authenticated
        PUT/DELETE: only owner
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]

        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]

        # PUT, DELETE uchun
        return [permissions.IsAuthenticated(), IsOwner()]


# ============================================
# 6. Custom + Built-in mix
# ============================================

class BookView_BuiltInMix(viewsets.ModelViewSet):
    """
    Only adminlar yoki ownerlar update qilishi mumkin
    (IsAdminUser OR IsOwner)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser | IsOwner]


# ============================================
# 7. Multiple-level (view + object)
# ============================================

class CanCreateButRestrictedEdit(permissions.BasePermission):
    """
    View-level: create uchun faqat authenticated
    Object-level: edit uchun owner
    """
    def has_permission(self, request, view):
        if view.action == "create":
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ["update", "partial_update", "destroy"]:
            return obj.owner == request.user
        return True


class BookView_Multi(viewsets.ModelViewSet):
    """
    IsAuthenticated AND CanCreateButRestrictedEdit
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated & CanCreateButRestrictedEdit]


# ============================================
# 8. Role-based combining (groups/roles)
# ============================================

class IsEditor(permissions.BasePermission):
    """
    User.groups orqali tekshirish
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name="editors").exists()


class BookEditorView(viewsets.ModelViewSet):
    """
    (Editor OR Admin)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsEditor | permissions.IsAdminUser]


# ============================================
# 9. Conditional permissions based on action
# ============================================

class BookView_Actions(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    action_permissions = {
        "list": [permissions.AllowAny()],
        "retrieve": [permissions.AllowAny()],
        "create": [permissions.IsAuthenticated()],
        "update": [IsOwner],
        "partial_update": [IsOwner],
        "destroy": [permissions.IsAdminUser | IsOwner],
    }

    def get_permissions(self):
        return [perm() for perm in self.action_permissions.get(self.action, [permissions.IsAuthenticated()])]


# ============================================
# 10. YANGI: Premium User Permission
# ============================================

class IsPremiumUser(permissions.BasePermission):
    """
    Premium userlar uchun maxsus permission
    """
    message = "Faqat premium userlar uchun!"
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'is_premium', False)
        )


class BookView_Premium(viewsets.ModelViewSet):
    """
    Premium feature: faqat premium userlar kirishi mumkin
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsPremiumUser]
    
    @action(detail=False, methods=['get'])
    def premium_content(self, request):
        """
        Maxsus premium content
        """
        return Response({
            'message': 'Premium content!',
            'books': self.get_queryset()[:10]
        })


# ============================================
# 11. YANGI: Time-based Permission
# ============================================

class IsBusinessHours(permissions.BasePermission):
    """
    Faqat ish vaqtida (9:00-18:00) ruxsat
    """
    message = "Ish vaqtida (9:00-18:00) foydalanish mumkin"
    
    def has_permission(self, request, view):
        now = datetime.now().time()
        start = time(9, 0)  # 9:00
        end = time(18, 0)   # 18:00
        return start <= now <= end


class BookView_BusinessHours(viewsets.ModelViewSet):
    """
    Ish vaqtida ishlaydi (IsAuthenticated AND IsBusinessHours)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsBusinessHours]


# ============================================
# 12. YANGI: Conditional Limits
# ============================================

class HasCreationLimit(permissions.BasePermission):
    """
    User limitga qarab permission
    - Premium: cheksiz
    - Oddiy: 10 ta kitob
    """
    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
            
        # Premium userlar cheksiz
        if getattr(request.user, 'is_premium', False):
            return True
        
        # Oddiy userlar: 10 ta limit
        count = Book.objects.filter(owner=request.user).count()
        if count >= 10:
            self.message = "Limit tugadi! Premium bo'ling (10/10)"
            return False
        
        return True


class BookView_WithLimit(viewsets.ModelViewSet):
    """
    Create uchun limit bor (IsAuthenticated AND HasCreationLimit)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, HasCreationLimit]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ============================================
# 13. YANGI: Advanced Action-based
# ============================================

class BookView_AdvancedActions(viewsets.ModelViewSet):
    """
    Har bir action uchun murakkab permission kombinatsiyalari
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Action asosida turli xil permissionlar
        """
        if self.action == 'list':
            # List - hammaga
            return [permissions.AllowAny()]
            
        elif self.action == 'retrieve':
            # Detail - published yoki owner
            return [IsPublic | IsOwner]
            
        elif self.action == 'create':
            # Create - authenticated VA limit check
            return [permissions.IsAuthenticated(), HasCreationLimit()]
            
        elif self.action in ['update', 'partial_update']:
            # Update - owner yoki admin
            return [IsOwner | permissions.IsAdminUser]
            
        elif self.action == 'destroy':
            # Delete - faqat admin
            return [permissions.IsAdminUser()]
            
        elif self.action == 'publish':
            # Publish - owner yoki editor
            return [IsOwner | IsEditor]
            
        elif self.action == 'premium_only':
            # Premium action - faqat premium
            return [IsPremiumUser()]
            
        # Default
        return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        Kitobni publish qilish
        """
        book = self.get_object()
        book.published = True
        book.save()
        return Response({'status': 'published'})
    
    @action(detail=False, methods=['get'])
    def premium_only(self, request):
        """
        Faqat premium userlar uchun
        """
        return Response({'message': 'Premium content!'})


# ============================================
# Best Practices
# ============================================

"""
✔ Combining AND (default), OR (|), NOT (~) imkoniyatlaridan foydalaning
✔ Bir nechta permission -> soddalashtirib guruhlang (A|B & C)
✔ get_permissions() -> action-based boshqarish uchun qulay
✔ Built-in va custom permissionlarni aralashtirish mumkin
✔ Testing juda muhim:
    - anonymous
    - owner
    - staff
    - published/unpublished
    - premium/regular
    - business hours
✔ Permissionlar qisqa bo'lsin → ko'p mantiq View ichida emas, permission classlarda bo'lsin
✔ Custom message berib qo'ying: self.message = "..."
✔ Time-based, role-based, limit-based permissionlarni birlashtirishingiz mumkin
✔ action_permissions dictionary pattern juda qulay va o'qilishi oson
"""