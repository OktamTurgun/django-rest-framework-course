# Homework: Authentication Implementation

## Vazifa 1: Password Reset Funksiyasi

### Maqsad
Email orqali parolni tiklash funksiyasini yaratish.

### Topshiriq
1. `accounts/views.py`da quyidagi endpoint'larni yarating:
   - `POST /api/accounts/password-reset/` - Email yuborish
   - `POST /api/accounts/password-reset-confirm/` - Yangi parol o'rnatish

### Kod namunasi
```python
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    """
    Email orqali parol tiklash so'rovi
    """
    email = request.data.get('email')
    
    # User topish
    # Reset token yaratish
    # Email yuborish (konsolda ko'rsatish)
    
    return Response({
        'message': 'Agar email to\'g\'ri bo\'lsa, kod yuborildi'
    })
```

### Talablar
- ✅ Email mavjudligini tekshirish
- ✅ Random token generatsiya qilish
- ✅ Token'ni saqlash (modelda yoki cache'da)
- ✅ Token bilan parol yangilash

---

## Vazifa 2: User Profile Update

### Maqsad
Foydalanuvchi o'z profilini yangilashi uchun endpoint yaratish.

### Topshiriq
1. `PUT/PATCH /api/accounts/profile/` endpoint yarating
2. Foydalanuvchi quyidagilarni yangilashi mumkin:
   - first_name
   - last_name
   - email

### Kod namunasi
```python
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Profil yangilash
    """
    user = request.user
    
    # Ma'lumotlarni yangilash
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.email = request.data.get('email', user.email)
    user.save()
    
    return Response({
        'message': 'Profil yangilandi',
        'username': user.username,
        'email': user.email
    })
```

### Talablar
- ✅ Faqat authenticated user yangilashi mumkin
- ✅ Email validation qo'shish
- ✅ PUT vs PATCH farqini qo'llash

---

## Vazifa 3: JWT Authentication

### Maqsad
Simple JWT paket yordamida JWT authentication qo'shish.

### Topshiriq
1. `djangorestframework-simplejwt` o'rnatish
2. JWT sozlamalarini qo'shish
3. Token olish va yangilash endpoint'lari

### O'rnatish
```bash
pipenv install djangorestframework-simplejwt
```

### settings.py
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

### URLs
```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

### Postman test
```http
POST http://127.0.0.1:8000/api/token/
Content-Type: application/json

{
    "username": "testuser",
    "password": "test123456"
}
```

Response:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Talablar
- ✅ JWT tokenlar olish
- ✅ Access token bilan API'ga murojaat
- ✅ Refresh token bilan yangi access token olish
- ✅ Authorization header: `Bearer <access_token>`

---

## Vazifa 4: Custom User Model

### Maqsad
AbstractUser dan meros olgan custom user model yaratish.

### Topshiriq
1. `accounts/models.py`da custom User model yarating
2. Qo'shimcha maydonlar qo'shing:
   - phone_number
   - address
   - date_of_birth
   - bio

### Kod
```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.username
```

### settings.py
```python
AUTH_USER_MODEL = 'accounts.CustomUser'
```

### Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### Talablar
- ✅ Custom User model yaratish
- ✅ AUTH_USER_MODEL sozlash
- ✅ Admin panelda custom user ko'rsatish
- ✅ Register endpoint'da yangi maydonlarni qo'llash

---

## Vazifa 5: Custom Permission - IsAdminOrReadOnly (⭐⭐⭐)

### Maqsad
Faqat admin foydalanuvchilar yaratish/tahrirlash/o'chirish, boshqalar faqat ko'rish.

### Topshiriq
1. `books/permissions.py` yarating
2. Custom permission class yarating

### Kod
```python
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin - barcha amallar
    Boshqalar - faqat GET
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
```

### views.py'da qo'llash
```python
from .permissions import IsAdminOrReadOnly

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
```

### Talablar
- ✅ SAFE_METHODS (GET, HEAD, OPTIONS) hamma uchun
- ✅ POST, PUT, PATCH, DELETE faqat admin
- ✅ Barcha book endpoint'larda qo'llash

---


## Topshirish

1. Barcha kodlarni GitHub'ga push qiling
2. Postman collection export qiling
3. Screenshot'lar tayyorlang:
   - Register response
   - Login response
   - Profile response
   - JWT token response
4. README.md'da test natijalarini yozing

## Qo'shimcha challenge

- [ ] Email verification (Email tasdiqlash)
- [ ] Two-factor authentication (2FA)
- [ ] OAuth2 integration (Google, Facebook login)
- [ ] API rate limiting per user
- [ ] User roles (Admin, Moderator, User)