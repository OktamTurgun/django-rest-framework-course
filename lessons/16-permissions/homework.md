# 16-Dars: Permissions - Uy Vazifasi

## Maqsad
Permission konsepsiyalarini mustahkamlash va real-world scenariolarni amalda qo'llash.

---

## Vazifa 1: Basic Permissions
**Qiyinlik:** Oson  
**Vaqt:** 30 daqiqa

### Topshiriq:
`Author` modeliga permissions qo'shing:

```python
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # TODO: Permission qo'shing
```

**Talablar:**
1. Anonymous users faqat o'qiy oladi (GET)
2. Authenticated users yarata oladi (POST)
3. Faqat admin o'chirishi mumkin (DELETE)

### Tekshirish:
```bash
# Anonymous - OK
GET /api/authors/

# Anonymous - 401
POST /api/authors/

# Authenticated non-admin - 403
DELETE /api/authors/1/

# Admin - 204
DELETE /api/authors/1/
```

### Yechim joyi:
`books/views.py` → `AuthorViewSet`

---

## Vazifa 2: IsOwner Permission
**Qiyinlik:** O'rta  
**Vaqt:** 45 daqiqa

### Topshiriq:
Custom `IsOwner` permission yarating:

```python
class IsOwner(BasePermission):
    """
    Faqat owner operatsiya bajarishi mumkin.
    """
    def has_object_permission(self, request, view, obj):
        # TODO: Implement logic
        pass
```

**Talablar:**
1. `books/permissions.py` faylida yarating
2. Faqat `obj.owner == request.user` bo'lsa `True`
3. `BookViewSet`da ishlatilsin

### Test scenariyolar:
```python
# User A creates book
POST /api/books/
# Response: {"id": 1, "owner": "userA"}

# User B tries to update
PUT /api/books/1/
# Response: 403 Forbidden ❌

# User A updates
PUT /api/books/1/
# Response: 200 OK ✅
```

### Yechim joyi:
- `books/permissions.py` → `IsOwner` class
- `books/views.py` → `BookViewSet`

---

## Vazifa 3: IsOwnerOrReadOnly
**Qiyinlik:** O'rta  
**Vaqt:** 45 daqiqa

### Topshiriq:
`IsOwnerOrReadOnly` permission yarating:

**Logic:**
- GET requests → hamma uchun
- POST/PUT/DELETE → faqat owner

```python
class IsOwnerOrReadOnly(BasePermission):
    """
    Owner o'zgartirishi mumkin.
    Boshqalar faqat o'qiy oladi.
    """
    def has_object_permission(self, request, view, obj):
        # TODO: Implement
        pass
```

**Talablar:**
1. `permissions.SAFE_METHODS` ishlatilsin
2. GET, HEAD, OPTIONS - hamma uchun
3. PUT, PATCH, DELETE - faqat owner

### Test:
```bash
# Anyone - OK
GET /api/books/1/

# Non-owner - 403
PUT /api/books/1/

# Owner - 200
PUT /api/books/1/
```

---

## Vazifa 4: IsPublishedOrOwner
**Qiyinlik:** Qiyin  
**Vaqt:** 60 daqiqa

### Topshiriq:
Murakkab permission yarating:

**Logic:**
- Published kitoblar → hamma ko'ra oladi
- Unpublished kitoblar → faqat owner ko'ra oladi
- O'zgartirish → faqat owner

```python
class IsPublishedOrOwner(BasePermission):
    """
    - Published: public
    - Unpublished: owner only
    - Modification: owner only
    """
    def has_object_permission(self, request, view, obj):
        # TODO: Implement complex logic
        pass
```

**Test scenariyolar:**

| User | Book Status | Action | Result |
|------|-------------|--------|--------|
| Anonymous | Published | GET | ✅ 200 |
| Anonymous | Unpublished | GET | ❌ 403 |
| Owner | Unpublished | GET | ✅ 200 |
| Non-owner | Unpublished | GET | ❌ 403 |
| Owner | Any | PUT | ✅ 200 |
| Non-owner | Any | PUT | ❌ 403 |

### Yechim joyi:
`books/permissions.py` → `IsPublishedOrOwner`

---

## Vazifa 5: Admin Override
**Qiyinlik:** Qiyin  
**Vaqt:** 60 daqiqa

### Topshiriq:
`IsOwnerOrAdmin` permission yarating:

**Logic:**
- Admin → hamma narsani qila oladi
- Owner → o'z obyektini boshqaradi
- Boshqalar → faqat o'qiy oladi

```python
class IsOwnerOrAdmin(BasePermission):
    """
    Admin yoki owner to'liq huquqlar.
    Boshqalar faqat o'qiy oladi.
    """
    def has_object_permission(self, request, view, obj):
        # Safe methods - hamma
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Admin - hamma narsa
        if request.user.is_staff:
            return True
        
        # Owner - o'z kitobini
        return obj.owner == request.user
```

**Test:**
```python
# Admin deletes any book
DELETE /api/books/1/  # userA's book
# Response: 204 No Content ✅

# Owner deletes own book
DELETE /api/books/2/  # userB's book
# Response: 204 No Content ✅

# Non-owner tries to delete
DELETE /api/books/1/  # userA's book
# Response: 403 Forbidden ❌
```

---

## Vazifa 6: Multiple Permissions
**Qiyinlik:** Qiyin  
**Vaqt:** 45 daqiqa

### Topshiriq:
Bir nechta permission'larni birlashtiring:

```python
class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,           # 1. Authenticated bo'lishi kerak
        IsOwnerOrReadOnly,         # 2. Owner yoki ReadOnly
    ]
```

**Logic:**
1. ✅ Authentication check
2. ✅ Owner yoki ReadOnly check
3. Ikkala shart ham o'tishi kerak (AND logic)

**Test:**
```bash
# Anonymous - 401 (IsAuthenticated fails)
POST /api/books/

# Authenticated, non-owner - 403 (IsOwnerOrReadOnly fails)
DELETE /api/books/1/

# Authenticated owner - 204 (both pass)
DELETE /api/books/1/
```

---

## Vazifa 7: Custom Action Permissions
**Qiyinlik:** Juda qiyin  
**Vaqt:** 90 daqiqa

### Topshiriq:
Har xil action'lar uchun turli permission'lar:

```python
class BookViewSet(viewsets.ModelViewSet):
    
    def get_permissions(self):
        """
        Action'ga qarab permission tanlash
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwner]
        elif self.action == 'publish':
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        
        return [permission() for permission in permission_classes]
```

**Test matrix:**

| Action | Anonymous | Authenticated | Owner | Admin |
|--------|-----------|---------------|-------|-------|
| list | ✅ | ✅ | ✅ | ✅ |
| create | ❌ | ✅ | ✅ | ✅ |
| retrieve | ✅ | ✅ | ✅ | ✅ |
| update | ❌ | ❌ | ✅ | ❌ |
| destroy | ❌ | ❌ | ✅ | ❌ |
| publish | ❌ | ❌ | ✅ | ✅ |

---

## Bonus Vazifa: Role-based Permissions
**Qiyinlik:** Expert  
**Vaqt:** 120 daqiqa

### Topshiriq:
Role-based permission system yarating:

```python
# models.py
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=[
            ('reader', 'Reader'),
            ('author', 'Author'),
            ('editor', 'Editor'),
            ('admin', 'Admin'),
        ]
    )

# permissions.py
class HasRole(BasePermission):
    """
    Check user role
    """
    required_roles = []
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.profile.role in self.required_roles
        )

class IsEditor(HasRole):
    required_roles = ['editor', 'admin']

class IsAuthor(HasRole):
    required_roles = ['author', 'editor', 'admin']
```

**Role hierarchy:**
```
Admin > Editor > Author > Reader
  ↓       ↓        ↓        ↓
 ALL   Edit all  Create  Read only
```

**Test:**
```python
# Reader
GET /api/books/  # ✅
POST /api/books/  # ❌

# Author
GET /api/books/  # ✅
POST /api/books/  # ✅
PUT /api/books/1/  # ❌ (not owner)

# Editor
PUT /api/books/1/  # ✅ (can edit anyone's book)

# Admin
DELETE /api/books/1/  # ✅ (can do anything)
```

---

## Topshirish

### 1. Code
```
books/
├── permissions.py
│   ├── IsOwner
│   ├── IsOwnerOrReadOnly
│   ├── IsPublishedOrOwner
│   ├── IsOwnerOrAdmin
│   └── (Bonus) Role-based permissions
├── models.py
│   └── owner field qo'shilgan
└── views.py
    └── Permissions qo'llanilgan
```

### 2. Testing
Postman collection yoki screenshot'lar:
- Har bir permission test qilingan
- Edge cases test qilingan
- Error scenarios test qilingan

### 3. Documentation
`TESTING.md` fayl yarating:
```markdown
# Permission Testing Results

## Vazifa 1: Basic Permissions
- [x] Anonymous read - OK
- [x] Anonymous write - 401
- [x] Admin delete - 204

## Vazifa 2: IsOwner
...
```

---

## Yordam

### Maslahatlar:
1. `permissions.SAFE_METHODS` → `['GET', 'HEAD', 'OPTIONS']`
2. `request.user.is_staff` → Admin check
3. `request.user == obj.owner` → Owner check
4. AND logic → list'da bir nechta permission
5. OR logic → custom permission ichida `or`

### Xatolar:
```python
# ❌ Xato
def has_permission(self, request, view):
    return obj.owner == request.user  # obj yo'q!

# ✅ To'g'ri
def has_object_permission(self, request, view, obj):
    return obj.owner == request.user
```

### Debug:
```python
# Permission ichida debug
def has_object_permission(self, request, view, obj):
    print(f"User: {request.user}")
    print(f"Owner: {obj.owner}")
    print(f"Is owner: {request.user == obj.owner}")
    return request.user == obj.owner
```

---

## Foydali havolalar

- [DRF Permissions Guide](https://www.django-rest-framework.org/api-guide/permissions/)
- [Django User Model](https://docs.djangoproject.com/en/5.0/ref/contrib/auth/)
- [Testing Permissions](https://www.django-rest-framework.org/api-guide/testing/)

---

**Omad! Permission'lar API xavfsizligining asosi!**