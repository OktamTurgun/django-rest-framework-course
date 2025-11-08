# Lesson 13: Authentication Implementation

## Darsning maqsadi
Django REST Framework'da Token Authentication va Session Authentication'ni to'liq qo'llash, foydalanuvchilarni ro'yxatdan o'tkazish, login/logout funksiyalarini yaratish.

## O'rganadigan mavzular

### 1. Token Authentication Setup
- REST Framework Token Authentication o'rnatish
- Token model bilan ishlash
- Token yaratish va boshqarish

### 2. User Registration & Login
- Foydalanuvchi ro'yxatdan o'tkazish API
- Login endpoint yaratish
- Logout funksiyasi
- User profile endpoint

### 3. Permission Classes
- IsAuthenticated
- IsAuthenticatedOrReadOnly
- Custom permissions yaratish
- Object-level permissions

### 4. API Endpoints himoyalash
- Authentication qo'shish
- Permission classes qo'llash
- Token bilan so'rov yuborish
- Headers bilan ishlash

## Loyiha strukturasi
```
13-auth-implementation/
├── README.md
├── homework.md
├── code/
│   └── library-project/
│       ├── accounts/          # Authentication endpoints
│       ├── books/              # Protected API
│       └── library_project/    # Settings
└── examples/
    ├── token_auth_example.py
    ├── custom_permissions_example.py
    └── jwt_auth_example.py
```

## Kerakli paketlar
```bash
pip install djangorestframework
pip install djangorestframework-simplejwt  # JWT uchun
```

## Asosiy API Endpoints
```
POST   /api/accounts/register/  - Ro'yxatdan o'tish
POST   /api/accounts/login/     - Login qilish
POST   /api/accounts/logout/    - Logout qilish
GET    /api/accounts/profile/   - Profil ko'rish

GET    /api/books/              - Kitoblar ro'yxati (hamma)
POST   /api/books/              - Kitob yaratish (auth kerak)
GET    /api/books/<id>/         - Kitob ko'rish (hamma)
PUT    /api/books/<id>/         - Kitob tahrirlash (auth kerak)
DELETE /api/books/<id>/         - Kitob o'chirish (auth kerak)
```

## Postman bilan test qilish

### 1. Register
```http
POST http://127.0.0.1:8000/api/accounts/register/
Content-Type: application/json

{
    "username": "testuser",
    "password": "test123456",
    "email": "test@example.com"
}
```

### 2. Login
```http
POST http://127.0.0.1:8000/api/accounts/login/
Content-Type: application/json

{
    "username": "testuser",
    "password": "test123456"
}
```

Response:
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "username": "testuser"
}
```

### 3. Token bilan so'rov
```http
GET http://127.0.0.1:8000/api/accounts/profile/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## Authentication Headers
```http
# Token Authentication
Authorization: Token <your-token-here>

# Session Authentication
Cookie: sessionid=<session-id>

# JWT Authentication (bonus)
Authorization: Bearer <jwt-token>
```

## Qo'llanma

1. Virtual muhitni ishga tushiring
2. Settings.py'da authentication sozlang
3. Accounts app'da views yarating
4. URL'larni ulang
5. Migration bajaring
6. Postman'da test qiling
7. Custom permissions qo'shing

## Foydali linklar

- [DRF Authentication](https://www.django-rest-framework.org/api-guide/authentication/)
- [DRF Permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [Token Authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)