# Examples - Permissions Misollari

Bu papkada Permission'lar bilan ishlashning turli misollarini topasiz.

## Fayllar

### 01-built-in-permissions.py
**Mavzu:** DRF'ning built-in permission'lari

**O'rganasiz:**
- AllowAny
- IsAuthenticated
- IsAuthenticatedOrReadOnly
- IsAdminUser
- DjangoModelPermissions

**Qachon ishlatiladi:**
- 90% hollarda - IsAuthenticatedOrReadOnly
- Private API - IsAuthenticated
- Admin endpoints - IsAdminUser
- Public API - AllowAny (ehtiyotkorlik bilan!)

**Kod misoli:**
```python
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # GET - hamma
    # POST/PUT/DELETE - authenticated
```

---

### 02-custom-permissions.py
**Mavzu:** Custom permission yaratish

**O'rganasiz:**
- BasePermission class
- has_permission() method
- has_object_permission() method
- IsOwner, IsOwnerOrReadOnly patterns

**Qachon ishlatiladi:**
- Owner-based access control
- Complex business logic
- Role-based permissions
- Multi-tenant applications

**Kod misoli:**
```python
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
```

---

### 03-object-level-permissions.py
**Mavzu:** Object-level permission checking

**O'rganasiz:**
- View-level vs Object-level
- get_object() va permission flow
- IsPublishedOrOwner pattern
- Conditional access

**Qachon ishlatiladi:**
- Har bir obyekt uchun alohida check
- Published/Draft content
- Privacy settings
- User-specific data

**Kod misoli:**
```python
class IsPublishedOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.published:
            return True
        return obj.owner == request.user
```

---

### 04-combining-permissions.py
**Mavzu:** Multiple permission'larni birlashtirish

**O'rganasiz:**
- AND logic (default)
- OR logic (custom)
- get_permissions() method
- Action-based permissions

**Qachon ishlatiladi:**
- Murakkab access control
- Turli action'lar uchun turli ruxsatlar
- Admin override scenarios
- Multi-condition checks

**Kod misoli:**
```python
class BookViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        return [IsOwner()]
```

---

##  Qanday ishlatish

### 1. Bitta misol faylini o'qing
```python
# Misol: 01-built-in-permissions.py
```

### 2. Konseptlarni tushuning
- Har bir permission qachon ishlatiladi?
- Qanday logic ishlaydi?
- Qanday test qilish mumkin?

### 3. O'z loyihangizda sinab ko'ring
- Misolni copy qiling
- O'z modelingizga moslang
- Test qiling

### 4. Keyingi misolga o'ting

---

##  Ketma-ketlik

Agar birinchi marta o'rganayotgan bo'lsangiz:

1.  **01-built-in-permissions.py** - Built-in'larni tushunish
2.  **02-custom-permissions.py** - O'z permission'ingizni yaratish
3.  **03-object-level-permissions.py** - Object-level logic
4.  **04-combining-permissions.py** - Complex scenarios

---

##  Maslahatlar

### 1. Har bir misolni alohida test qiling
```python
# Test qilish uchun
python manage.py shell

from books.permissions import IsOwner
from books.models import Book
from django.contrib.auth.models import User

# Test scenario
user1 = User.objects.create(username='user1')
book = Book.objects.create(title='Test', owner=user1)

# Permission check
perm = IsOwner()
perm.has_object_permission(request, view, book)
```

### 2. Postman'da test qiling
```bash
# Test collection yarating
# Har xil user'lar uchun test qiling
# Edge case'larni unutmang
```

### 3. Debug mode
```python
# Permission ichida print qo'shing
def has_object_permission(self, request, view, obj):
    print(f"Checking permission for {request.user}")
    print(f"Object owner: {obj.owner}")
    result = obj.owner == request.user
    print(f"Result: {result}")
    return result
```

### 4. Unit test yozing
```python
from rest_framework.test import APITestCase

class PermissionTest(APITestCase):
    def test_owner_can_delete(self):
        # Test logic
        pass
```

---

##  Real-world Scenarios

### Scenario 1: Blog API
```python
# Kimdir yozishi mumkin
# Faqat muallif o'zgartirishi mumkin
# Hamma o'qiy oladi

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
```

### Scenario 2: E-commerce
```python
# Mahsulotlar - hamma ko'ra oladi
# Order - faqat o'zining orderlari
# Admin - hamma orderlar

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
```

### Scenario 3: Social Media
```python
# Public posts - hamma
# Private posts - faqat followers
# Edit/Delete - faqat author

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPublicOrFollowerOrAuthor]
```

---

##  Permission Decision Matrix

| Permission | Anonymous | Authenticated | Owner | Admin |
|------------|-----------|---------------|-------|-------|
| AllowAny | ✅ | ✅ | ✅ | ✅ |
| IsAuthenticated | ❌ | ✅ | ✅ | ✅ |
| IsAuthenticatedOrReadOnly (GET) | ✅ | ✅ | ✅ | ✅ |
| IsAuthenticatedOrReadOnly (POST) | ❌ | ✅ | ✅ | ✅ |
| IsAdminUser | ❌ | ❌ | ❌ | ✅ |
| IsOwner | ❌ | ❌ | ✅ | ❌ |
| IsOwnerOrAdmin | ❌ | ❌ | ✅ | ✅ |

---

## Common Mistakes

### Mistake 1: has_permission da obj ishlatish
```python
#  Xato
def has_permission(self, request, view):
    return obj.owner == request.user  # obj yo'q!

#  To'g'ri
def has_object_permission(self, request, view, obj):
    return obj.owner == request.user
```

### Mistake 2: SAFE_METHODS unutish
```python
#  Xato
def has_object_permission(self, request, view, obj):
    return obj.owner == request.user  # GET ham blocked!

#  To'g'ri
def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
        return True
    return obj.owner == request.user
```

### Mistake 3: Anonymous user check qilmaslik
```python
# Xato
def has_permission(self, request, view):
    return request.user.profile.is_premium  # Anonymous - AttributeError!

# To'g'ri
def has_permission(self, request, view):
    return (
        request.user.is_authenticated and
        request.user.profile.is_premium
    )
```

---

## 🔍 Debugging Tips

### 1. Permission flow
```
Request → Authentication → Permission Check
                              ↓
                        has_permission()
                              ↓
                    has_object_permission()
                              ↓
                          Response
```

### 2. Print debug
```python
def has_object_permission(self, request, view, obj):
    print(f"=== Permission Debug ===")
    print(f"User: {request.user}")
    print(f"Method: {request.method}")
    print(f"Object: {obj}")
    print(f"Owner: {obj.owner}")
    result = obj.owner == request.user
    print(f"Result: {result}")
    print(f"=======================")
    return result
```

### 3. Test in shell
```python
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

factory = APIRequestFactory()
request = factory.get('/api/books/1/')
request.user = user

perm = IsOwner()
result = perm.has_object_permission(request, None, book)
print(result)
```

---

## Best Practices

### 1. Aniq naming
```python
# ✅ Yaxshi
IsOwnerOrReadOnly
IsPublishedOrOwner
IsAuthorOrAdmin

# ❌ Yomon
MyPerm
CustomPermission1
CheckAccess
```

### 2. Docstring
```python
class IsOwner(BasePermission):
    """
    Faqat owner operatsiya bajarishi mumkin.
    
    Returns:
        True: agar request.user == obj.owner
        False: boshqa hollarda
    """
```

### 3. Single Responsibility
```python
# ❌ Bir permission juda ko'p narsa qiladi
class ComplexPermission(BasePermission):
    # 100 lines of code...
    pass

# ✅ Har biri bitta vazifa
class IsOwner(BasePermission):
    pass

class IsPublished(BasePermission):
    pass
```

---

## Next Steps

Misollarni o'rgangandan keyin:
1. ✅ Homework'ni bajaring
2. ✅ O'z loyihangizda qo'llang
3. ✅ Edge case'larni test qiling
4. ✅ Documentation yozing

---

## 🔗 Foydali havolalar

- [DRF Permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [Django Auth](https://docs.djangoproject.com/en/5.0/topics/auth/)
- [Security Best Practices](https://owasp.org/www-project-api-security/)

---

**Permission'larni to'g'ri ishlating - API xavfsizligining asosi!**