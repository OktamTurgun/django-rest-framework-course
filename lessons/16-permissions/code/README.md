# Code - Library Project (Lesson 16)

Bu papkada **16-Permissions** darsi uchun amaliy loyiha joylashgan.

## Loyiha strukturasi

```
library-project/
├── manage.py
├── db.sqlite3
├── .env
├── Pipfile
├── Pipfile.lock
│
├── library_project/
│   ├── settings.py           #  DEFAULT_PERMISSION_CLASSES
│   ├── urls.py
│   └── wsgi.py
│
├── books/
│   ├── models.py             #  owner field qo'shildi
│   ├── serializers.py        #  owner auto-set
│   ├── permissions.py        #  YANGI FAYL!
│   ├── views.py              #  Permissions qo'shildi
│   ├── urls.py
│   ├── admin.py
│   └── validators.py
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
└── static/
```

---

## Loyihani ishga tushirish

### 1. Virtual muhitni faollashtiring
```bash
cd library-project
pipenv shell
```

### 2. Migratsiyalarni bajaring
```bash
# Yangi migration'lar yaratish (owner field uchun)
python manage.py makemigrations

# Migratsiyalarni qo'llash
python manage.py migrate
```

### 3. Serverni ishga tushiring
```bash
python manage.py runserver
```

### 4. API'ni ochib ko'ring
```
http://127.0.0.1:8000/api/
```

---

##  Darsda o'zgartirilgan fayllar

###  books/models.py
**O'zgarish:** `owner` field qo'shildi

**Eski:**
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    # ...
```

**Yangi:**
```python
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    owner = models.ForeignKey(        # ← YANGI!
        User,
        on_delete=models.CASCADE,
        related_name='books'
    )
    # ...
```

**Migration:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### books/permissions.py (YANGI FAYL!)

Bu faylda custom permission'lar joylashgan:

```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Owner o'zgartirishi mumkin, boshqalar faqat o'qiy oladi.
    """
    
    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS - hamma uchun
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # PUT, PATCH, DELETE - faqat owner
        return obj.owner == request.user


class IsOwner(permissions.BasePermission):
    """
    Faqat owner operatsiya bajarishi mumkin.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsPublishedOrOwner(permissions.BasePermission):
    """
    - Published kitoblar: hamma ko'ra oladi
    - Unpublished kitoblar: faqat owner ko'ra oladi
    - O'zgartirish: faqat owner
    """
    
    def has_object_permission(self, request, view, obj):
        # GET request
        if request.method in permissions.SAFE_METHODS:
            # Published - hamma
            if obj.published:
                return True
            # Unpublished - faqat owner
            return obj.owner == request.user
        
        # PUT/PATCH/DELETE - faqat owner
        return obj.owner == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
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

---

### books/serializers.py
**O'zgarish:** `owner` field auto-set qilish

**Yangi:**
```python
class BookSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # ← YANGI!
    
    class Meta:
        model = Book
        fields = '__all__'
```

**Nima qiladi:**
- `owner` field'ni read-only qiladi
- Request'dan owner olmaydi
- Avtomatik `request.user` ni set qiladi

---

### books/views.py
**O'zgarish:** Permission'lar qo'shildi

**Eski:**
```python
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
```

**Yangi:**
```python
from .permissions import IsOwnerOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        # Owner'ni avtomatik set qilish
        serializer.save(owner=self.request.user)
```

**Nima o'zgardi:**
1.  `IsOwnerOrReadOnly` permission qo'shildi
2.  `perform_create()` method - owner auto-set
3.  GET - hamma, POST/PUT/DELETE - faqat owner

---

### library_project/settings.py
**O'zgarish:** Default permission

**Qo'shildi:**
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [          # ← YANGI!
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}
```

**Nima beradi:**
- Barcha ViewSet'lar uchun default permission
- Har bir ViewSet'da yozish shart emas
- Override qilish mumkin

---

## Mavjud Endpoint'lar

### Standard CRUD (Permission bilan)
```
GET    /api/books/              # Hamma - 200 OK
POST   /api/books/              # Authenticated - 201 Created
                                # Anonymous - 401 Unauthorized

GET    /api/books/1/            # Hamma - 200 OK

PUT    /api/books/1/            # Owner - 200 OK
                                # Non-owner - 403 Forbidden
                                # Anonymous - 401 Unauthorized

DELETE /api/books/1/            # Owner - 204 No Content
                                # Non-owner - 403 Forbidden
```

### Custom Actions
```
GET    /api/books/published/    # Hamma - 200 OK
GET    /api/books/statistics/   # Hamma - 200 OK
POST   /api/books/1/publish/    # Owner - 200 OK
POST   /api/books/1/unpublish/  # Owner - 200 OK
```

---

## Test qilish

### Test 1: Anonymous user
```bash
# GET - ishlaydi
curl http://127.0.0.1:8000/api/books/

# POST - 401 Unauthorized
curl -X POST http://127.0.0.1:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test"}'
```

### Test 2: Authenticated user (non-owner)
```bash
# Create own book - 201 Created
curl -X POST http://127.0.0.1:8000/api/books/ \
  -H "Authorization: Token user1-token" \
  -H "Content-Type: application/json" \
  -d '{"title": "User1 Book"}'

# Try to delete other's book - 403 Forbidden
curl -X DELETE http://127.0.0.1:8000/api/books/1/ \
  -H "Authorization: Token user2-token"
```

### Test 3: Owner
```bash
# Delete own book - 204 No Content
curl -X DELETE http://127.0.0.1:8000/api/books/1/ \
  -H "Authorization: Token user1-token"
```

---

## Permission Flow

```
Request → Authentication Check
              ↓
         IsAuthenticatedOrReadOnly
              ↓
         IsOwnerOrReadOnly
              ↓
    has_permission() → OK?
              ↓ Yes
    has_object_permission() → OK?
              ↓ Yes
         Response (200/201/204)
         
         
    ❌ Failure points:
    - Not authenticated → 401
    - Not owner → 403
    - Object not found → 404
```

---

##  Test Scenarios

### Scenario 1: Create book
```python
# User A authenticated
POST /api/books/
{
    "title": "Book A",
    "author": "Author A",
    ...
}

# Response: 201 Created
{
    "id": 1,
    "title": "Book A",
    "owner": "userA",  # ← Auto-set!
    ...
}
```

### Scenario 2: Non-owner tries to edit
```python
# User B authenticated
PUT /api/books/1/  # userA's book
{
    "title": "Updated"
}

# Response: 403 Forbidden
{
    "detail": "You do not have permission to perform this action."
}
```

### Scenario 3: Owner edits
```python
# User A authenticated
PUT /api/books/1/  # own book
{
    "title": "Updated"
}

# Response: 200 OK
{
    "id": 1,
    "title": "Updated",
    "owner": "userA",
    ...
}
```

---

##  Konfiguratsiya

### Database
SQLite (`db.sqlite3`)

### Environment Variables
`.env` faylida:
```
SECRET_KEY=your-secret-key
DEBUG=True
```

### Dependencies
`Pipfile` da:
```
django = "*"
djangorestframework = "*"
python-decouple = "*"
```

---

##  Keyingi qadamlar

1.  Permission'larni tushunding
2.  Nested Serializers (Keyingi dars)
3.  Filtering va Search
4.  Pagination

---

## Foydali buyruqlar

```bash
# Test user yaratish
python manage.py createsuperuser

# Shell'da test
python manage.py shell

# Token yaratish (shell'da)
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
user = User.objects.get(username='testuser')
token = Token.objects.create(user=user)
print(token.key)

# Migration
python manage.py makemigrations
python manage.py migrate

# Server
python manage.py runserver
```

---

## Muammolar va yechimlar

### Muammo 1: owner field bo'yicha xato
```
IntegrityError: NOT NULL constraint failed: books_book.owner_id
```
**Yechim:** Mavjud kitoblar uchun default owner belgilang
```bash
python manage.py shell

from books.models import Book
from django.contrib.auth.models import User
admin = User.objects.first()

Book.objects.update(owner=admin)
```

### Muammo 2: Permission ishlamayapti
```python
# Check:
print(request.user)              # User authenticated?
print(request.user.is_authenticated)
print(obj.owner)                 # Owner field mavjudmi?
print(obj.owner == request.user) # Tengligi?
```

### Muammo 3: 401 vs 403
- **401 Unauthorized** - Authentication yo'q
- **403 Forbidden** - Authenticated, lekin ruxsat yo'q

---

## Foydali havolalar

- [DRF Permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [Django User Model](https://docs.djangoproject.com/en/5.0/ref/contrib/auth/)
- [Testing Guide](https://www.django-rest-framework.org/api-guide/testing/)

---

**Loyiha tayyor! Permission'larni test qiling!**