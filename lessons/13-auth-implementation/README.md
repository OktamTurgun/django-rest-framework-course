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
---

## Homework - Qo'shimcha Authentication Turlari

### Implemented Features:

#### 1. Password Reset (Token Auth)
- Email bilan reset code olish
- Code bilan parolni tiklash
- Console'da kod ko'rsatish
- 15 daqiqa expire time

**Endpoints:**
```
POST /api/accounts/password-reset-request/
POST /api/accounts/password-reset-confirm/
```

#### 2. JWT Authentication
- JWT token generation
- Access token (60 min)
- Refresh token (7 days)
- Custom user data in token payload

**Endpoints:**
```
POST /api/accounts/jwt/login/
POST /api/accounts/jwt/refresh/
POST /api/accounts/jwt/verify/
```

#### 3. Session Authentication
- Cookie-based authentication
- Django session backend
- 24 hours session lifetime

**Endpoints:**
```
POST /api/accounts/session/login/
POST /api/accounts/session/logout/
GET  /api/accounts/session/me/
```

#### 4. Basic Authentication
- Username:Password base64 encoded
- Header-based authentication
- Test endpoints

**Endpoints:**
```
GET  /api/accounts/basic/me/
POST /api/accounts/basic/test/
```

---

## Authentication Comparison

| Auth Type | Stateful | DB Required | Mobile-Friendly | Security |
|-----------|----------|-------------|-----------------|----------|
| Token | ✅ | ✅ | ✅ | ⭐⭐⭐⭐ |
| JWT | ❌ | ❌ | ✅ | ⭐⭐⭐⭐ |
| Session | ✅ | ✅ | ❌ | ⭐⭐⭐ |
| Basic | ❌ | ❌ | ⚠️ | ⭐⭐ |

---

## Testing

All endpoints tested with Postman:
- ✅ 16 Main Lesson tests
- ✅ 8 Homework tests
- ✅ Total: 24 test cases

See: `Library_API_Lesson13_Complete.postman_collection.json`

---

## Technologies Used

- Django 5.2.7
- Django REST Framework 3.15.2
- djangorestframework-simplejwt 5.3.1
- Token Authentication (DRF built-in)
- JWT Authentication
- Session Authentication
- Basic Authentication

---

## Learning Outcomes

Ushbu darsdan keyin siz:
-  4 xil authentication usulini bilib oldingiz
-  Har birining afzallik va kamchiliklarini tushundingiz
-  Production-ready authentication code yoza olasiz
-  Security best practices'ni qo'llay olasiz
-  Mobile va web uchun auth implement qila olasiz

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