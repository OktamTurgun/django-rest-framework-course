# 16-Dars: Permissions (Ruxsatlar)

## Mundarija
1. [Kirish](#kirish)
2. [Permission nima?](#permission-nima)
3. [Built-in Permissions](#built-in-permissions)
4. [Custom Permissions](#custom-permissions)
5. [Object-level Permissions](#object-level-permissions)
6. [Combining Permissions](#combining-permissions)
7. [Amaliy mashg'ulot](#amaliy-mashgulot)
8. [Best Practices](#best-practices)

---

## Kirish

### ❓ Muammo

Hozirgi loyihada **authentication** bor, lekin **authorization** yo'q!

```python
# Hozirgi holat: Lesson 15
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
```

**Muammo:**
- ❌ Har kim ham kitobni o'zgartirishi mumkin
- ❌ Kitob egasi ham, begona odam ham o'chirishi mumkin
- ❌ Admin huquqlar yo'q
- ❌ Obyekt-darajasidagi nazorat yo'q

**Misol:**
```
User A: kitob yaratdi (id=1)
User B: User A'ning kitobini o'chirdi! ❌
User C: Admin, lekin maxsus huquqlari yo'q ❌
```

---

## Permission nima?

### Ta'rif

**Permission** - foydalanuvchiga API operatsiyalarini bajarish uchun ruxsat berish yoki rad etish mexanizmi.

### Authentication vs Authorization

```
┌─────────────────────────────────────────┐
│  Authentication (Kim siz?)              │
│  ├─ Token                               │
│  ├─ Session                             │
│  └─ JWT                                 │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Authorization (Nima qila olasiz?)      │
│  ├─ Permissions                         │
│  ├─ Roles                               │
│  └─ Object-level access                 │
└─────────────────────────────────────────┘
```

**Authentication:** "Siz kimligingizni isbotlang"  
**Permission:** "Siz buni qilishga ruxsatingiz bormi?"

---

## Built-in Permissions

DRF'da 4 ta asosiy built-in permission bor:

### 1. AllowAny

```python
from rest_framework.permissions import AllowAny

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
```

**Xususiyatlari:**
- ✅ Hamma uchun ochiq (hatto anonymous)
- ✅ CRUD barcha operatsiyalar
- ⚠️ **Xavfli!** Production'da foydalanmang

**Qachon ishlatiladi:**
- Public API (masalan, yangiliklar)
- Open data endpoints
- Testing

---

### 2. IsAuthenticated

```python
from rest_framework.permissions import IsAuthenticated

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
```

**Xususiyatlari:**
- ✅ Faqat login qilgan foydalanuvchilar
- ✅ Barcha operatsiyalar (CRUD)
- ❌ Anonymous users - 401 Unauthorized

**Qachon ishlatiladi:**
- Private API
- User-specific data
- Internal tools

**Test:**
```bash
# Without token - 401
GET /api/books/

# With token - 200
GET /api/books/
Authorization: Token abc123...
```

---

### 3. IsAuthenticatedOrReadOnly

```python
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
```

**Xususiyatlari:**
- ✅ GET requests - hamma (anonymous ham)
- ✅ POST/PUT/DELETE - faqat authenticated
- ✅ Eng ko'p ishlatiladigan!

**Qachon ishlatiladi:**
- Blog API (o'qish - hamma, yozish - faqat login)
- E-commerce (mahsulotlarni ko'rish - hamma, sotib olish - login)
- Forum API

**Test:**
```bash
# Anonymous - OK
GET /api/books/

# Anonymous - 401 Unauthorized
POST /api/books/
{"title": "New Book"}

# Authenticated - 201 Created
POST /api/books/
Authorization: Token abc123...
{"title": "New Book"}
```

---

### 4. IsAdminUser

```python
from rest_framework.permissions import IsAdminUser

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
```

**Xususiyatlari:**
- ✅ Faqat `user.is_staff = True`
- ✅ Admin panel access kerak
- ❌ Oddiy foydalanuvchilar - 403 Forbidden

**Qachon ishlatiladi:**
- Admin dashboard API
- System settings
- User management

**Test:**
```python
# Oddiy user
user.is_staff = False
GET /api/books/  # 403 Forbidden

# Admin user
admin.is_staff = True
GET /api/books/  # 200 OK
```

---

## Custom Permissions

### Custom Permission yaratish

```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Faqat owner o'zgartirishi mumkin.
    Boshqalar faqat o'qiy oladi.
    """
    
    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS - hamma uchun
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # PUT, PATCH, DELETE - faqat owner
        return obj.owner == request.user
```

**Ishlatish:**
```python
class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
```

---

### has_permission vs has_object_permission

```python
class CustomPermission(permissions.BasePermission):
    
    # 1. View-level (list, create)
    def has_permission(self, request, view):
        """
        Birinchi check - view darajasida
        list(), create() uchun
        """
        return request.user.is_authenticated
    
    # 2. Object-level (retrieve, update, delete)
    def has_object_permission(self, request, view, obj):
        """
        Ikkinchi check - obyekt darajasida
        retrieve(), update(), destroy() uchun
        """
        return obj.owner == request.user
```

**Ishlash tartibi:**
```
1. has_permission() → False bo'lsa, 403
2. has_permission() → True bo'lsa, davom etadi
3. has_object_permission() → False bo'lsa, 403
4. has_object_permission() → True bo'lsa, ruxsat beriladi
```

---

### Custom Permission misollar

#### 1. IsOwner (Faqat egasi)

```python
class IsOwner(permissions.BasePermission):
    """
    Faqat owner bilan ishlashi mumkin.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
```

---

#### 2. IsAuthorOrReadOnly

```python
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Faqat muallif o'zgartirishi mumkin.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
```

---

#### 3. IsPremiumUser

```python
class IsPremiumUser(permissions.BasePermission):
    """
    Faqat premium foydalanuvchilar uchun.
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.profile.is_premium
        )
```

---

#### 4. IsPublishedOrOwner

```python
class IsPublishedOrOwner(permissions.BasePermission):
    """
    Published kitoblarni hamma ko'radi.
    Unpublished - faqat owner.
    """
    
    def has_object_permission(self, request, view, obj):
        # Published - hamma ko'radi
        if obj.published:
            return True
        
        # Unpublished - faqat owner
        return obj.owner == request.user
```

---

## Object-level Permissions

### Nima?

**Object-level permission** - har bir obyekt uchun alohida ruxsat tekshirish.

### Qanday ishlaydi?

```python
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    
    # ViewSet avtomatik chaqiradi:
    # 1. list() - has_permission()
    # 2. retrieve() - has_permission() + has_object_permission()
    # 3. update() - has_permission() + has_object_permission()
    # 4. destroy() - has_permission() + has_object_permission()
```

### Misol

```python
# User A
POST /api/books/
{"title": "Book A"}
# Response: {"id": 1, "owner": "userA"}

# User B tries to delete
DELETE /api/books/1/
# Response: 403 Forbidden (IsOwnerOrReadOnly)

# User A can delete
DELETE /api/books/1/
# Response: 204 No Content ✅
```

---

## Combining Permissions

### Multiple Permissions

```python
class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly
    ]
```

**Logic:** AND (hammasidan o'tishi kerak)

```
IsAuthenticated AND IsOwnerOrReadOnly
     ✅                  ✅           → Ruxsat beriladi
     ✅                  ❌           → 403 Forbidden
     ❌                  ✅           → 401 Unauthorized
```

---

### OR Logic

```python
from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Owner yoki Admin
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin - ruxsat
        if request.user.is_staff:
            return True
        
        # Owner - ruxsat
        return obj.owner == request.user
```

---

### Complex Logic

```python
class ComplexPermission(BasePermission):
    """
    - Published: hamma ko'ra oladi
    - Unpublished: faqat owner yoki admin
    - O'zgartirish: faqat owner (admin ham yo'q!)
    """
    
    def has_object_permission(self, request, view, obj):
        # GET request
        if request.method in permissions.SAFE_METHODS:
            # Published - hamma
            if obj.published:
                return True
            # Unpublished - owner yoki admin
            return obj.owner == request.user or request.user.is_staff
        
        # PUT/PATCH/DELETE - faqat owner
        return obj.owner == request.user
```

---

## Amaliy mashg'ulot

### Loyiha strukturasi

```
16-permissions/
├── code/
│   └── library-project/
│       ├── books/
│       │   ├── models.py         (owner field qo'shamiz)
│       │   ├── permissions.py    (yangi!)
│       │   ├── serializers.py    (owner auto-set)
│       │   └── views.py          (permissions qo'shamiz)
│       └── ...
├── examples/
│   ├── 01-built-in-permissions.py
│   ├── 02-custom-permissions.py
│   ├── 03-object-level.py
│   └── 04-combining-permissions.py
├── README.md
└── homework.md
```

---

## Best Practices

### Do's (Qiling)

1. **Default permission** - har doim o'rnating
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}
```

2. **Aniq nomlash**
```python
# ✅ Yaxshi
class IsOwnerOrReadOnly(BasePermission):
    pass

# ❌ Yomon
class CustomPerm(BasePermission):
    pass
```

3. **Docstring yozing**
```python
class IsOwner(BasePermission):
    """
    Faqat owner operatsiya bajarishi mumkin.
    """
```

4. **Test yozing**
```python
def test_owner_can_delete():
    # Owner o'chirishi mumkin
    pass

def test_non_owner_cannot_delete():
    # Boshqa odam o'chira olmaydi
    pass
```

---

### ❌ Don'ts (Qilmang)

1. **AllowAny production'da**
```python
# ❌ Production'da xavfli
permission_classes = [AllowAny]
```

2. **Permission'siz qoldirish**
```python
# ❌ Nima uchun permission yo'q?
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    # permission_classes = ???
```

3. **Murakkab logic permission'da**
```python
# ❌ Juda murakkab
def has_permission(self, request, view):
    # 50 qator kod...
    pass

# Alohida service'ga ajrating
```

---

## Xulosa

### Nima o'rgandik:

1. **Built-in Permissions**
   - AllowAny, IsAuthenticated
   - IsAuthenticatedOrReadOnly
   - IsAdminUser

2. **Custom Permissions**
   - BasePermission
   - has_permission()
   - has_object_permission()

3. **Object-level Permissions**
   - IsOwner, IsOwnerOrReadOnly
   - Per-object checks

4. **Combining Permissions**
   - AND logic (default)
   - OR logic (custom)
   - Complex scenarios

---

### Permission Decision Tree

```
Request keldi
    ↓
Authentication tekshirish
    ↓
has_permission() → False? → 403 Forbidden
    ↓ True
View darajasida ruxsat
    ↓
has_object_permission() → False? → 403 Forbidden
    ↓ True
Obyekt darajasida ruxsat
    ↓
SUCCESS
```

---

## Keyingi dars

**Lesson 17: Nested Serializers & Relations**

---

## Foydali havolalar

- [DRF Permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [Django Authentication](https://docs.djangoproject.com/en/5.0/topics/auth/)
- [Security Best Practices](https://owasp.org/www-project-api-security/)

---

**API xavfsizligini ta'minlang!**