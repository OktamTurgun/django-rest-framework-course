"""
JWT Authentication Example
JSON Web Token authentication bilan ishlash
"""

# ============================================
# JWT NIMA?
# ============================================

"""
JWT (JSON Web Token) - bu stateless authentication usuli.

TOKEN vs JWT:

┌─────────────────────────────────────────────────────────┐
│ TOKEN (DRF Default)        │ JWT                        │
├────────────────────────────┼────────────────────────────┤
│ Database'da saqlanadi      │ Database'siz               │
│ 40 characters random       │ Encoded JSON data          │
│ Server'da validate qilish  │ Client'da decode mumkin    │
│ Logout = token delete      │ Logout = client delete     │
│ Tezroq (DB lookup)         │ Sekinroq (decode)          │
└────────────────────────────┴────────────────────────────┘

JWT STRUKTURA:
    header.payload.signature
    
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.     <- header
    eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImpvaG4i...  <- payload  
    SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c   <- signature

AFZALLIKLARI:
✅ Database'ga bog'liq emas (scalable)
✅ Microservices'da qulay
✅ Mobile app'lar uchun yaxshi
✅ Cross-domain ishlaydi
✅ Payload'da user info bo'lishi mumkin

KAMCHILIKLARI:
❌ Token revoke qilish qiyin
❌ Katta hajm (long string)
❌ XSS attack'ga zaif
❌ Refresh token kerak
"""


# ============================================
# 1. SETTINGS.PY SOZLAMALARI
# ============================================

"""
# O'rnatish
pip install djangorestframework-simplejwt

# settings.py

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# JWT sozlamalari
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),    # 1 soat
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),       # 1 hafta
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}
"""


# ============================================
# 2. URLS.PY SOZLAMALARI
# ============================================

"""
# urls.py

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # JWT token olish
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Token yangilash
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Token tekshirish
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
"""


# ============================================
# 3. TOKEN OLISH (Login)
# ============================================

"""
REQUEST:
POST http://127.0.0.1:8000/api/token/
Content-Type: application/json

{
    "username": "testuser",
    "password": "testpass123"
}

RESPONSE:
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

ACCESS TOKEN: API requests uchun (60 min)
REFRESH TOKEN: Yangi access token olish uchun (7 days)
"""


# ============================================
# 4. ACCESS TOKEN BILAN SO'ROV
# ============================================

"""
REQUEST:
GET http://127.0.0.1:8000/api/books/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

RESPONSE:
[
    {
        "id": 1,
        "title": "Book 1",
        ...
    }
]

⚠️ "Bearer" so'zi majburiy!
⚠️ Token "Authorization" header'da bo'lishi kerak
"""


# ============================================
# 5. TOKEN YANGILASH (Refresh)
# ============================================

"""
Access token 60 daqiqadan keyin amal qilmaydi.
Yangi access token olish uchun refresh token ishlatiladi.

REQUEST:
POST http://127.0.0.1:8000/api/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

RESPONSE:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."  <- Yangi access token
}
"""


# ============================================
# 6. CUSTOM JWT VIEWS
# ============================================

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT token'ga qo'shimcha ma'lumot qo'shish
    """
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Qo'shimcha claims qo'shish
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Response'ga qo'shimcha ma'lumot qo'shish
        data['username'] = self.user.username
        data['email'] = self.user.email
        
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view
    """
    serializer_class = CustomTokenObtainPairSerializer


"""
URLS.PY:
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

RESPONSE:
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "username": "testuser",       <- Qo'shimcha
    "email": "test@example.com"   <- Qo'shimcha
}
"""


# ============================================
# 7. JWT TOKEN DECODE QILISH
# ============================================

import jwt
from django.conf import settings

def decode_jwt_token(token):
    """
    JWT tokenni decode qilish va ichidagi ma'lumotlarni ko'rish
    """
    try:
        # Token decode
        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )
        
        print("🔓 Token decoded:")
        print(f"  User ID: {decoded.get('user_id')}")
        print(f"  Username: {decoded.get('username')}")
        print(f"  Email: {decoded.get('email')}")
        print(f"  Exp: {decoded.get('exp')}")
        print(f"  Token type: {decoded.get('token_type')}")
        
        return decoded
    except jwt.ExpiredSignatureError:
        print("❌ Token muddati o'tgan")
    except jwt.InvalidTokenError:
        print("❌ Token noto'g'ri")


# ============================================
# 8. MANUAL TOKEN YARATISH
# ============================================

from rest_framework_simplejwt.tokens import RefreshToken

def create_tokens_for_user(user):
    """
    User uchun manual token yaratish
    """
    refresh = RefreshToken.for_user(user)
    
    # Qo'shimcha claims
    refresh['username'] = user.username
    refresh['email'] = user.email
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


"""
VIEWS.PY DA ISHLATISH:

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def custom_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        tokens = create_tokens_for_user(user)
        return Response(tokens)
    
    return Response({'error': 'Invalid credentials'}, status=401)
"""


# ============================================
# 9. JWT BLACKLIST (Token bekor qilish)
# ============================================

"""
JWT tokenlarni bekor qilish uchun blacklist kerak.

# O'rnatish
pip install djangorestframework-simplejwt[blacklist]

# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt.token_blacklist',
]

# Migration
python manage.py migrate

# SIMPLE_JWT settings
SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
"""

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    JWT logout (refresh token blacklist'ga qo'shish)
    """
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()  # Tokenni blacklist'ga qo'shish
        
        return Response({'message': 'Logout muvaffaqiyatli'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)


"""
REQUEST:
POST http://127.0.0.1:8000/api/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
"""


# ============================================
# 10. FRONTEND BILAN ISHLASH
# ============================================

"""
JAVASCRIPT EXAMPLE:

// 1. Login va tokenlarni saqlash
async function login(username, password) {
    const response = await fetch('http://localhost:8000/api/token/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, password})
    });
    
    const data = await response.json();
    
    // LocalStorage'ga saqlash
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
}

// 2. API so'rovlari
async function getBooks() {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch('http://localhost:8000/api/books/', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    return await response.json();
}

// 3. Token yangilash
async function refreshAccessToken() {
    const refresh = localStorage.getItem('refresh_token');
    
    const response = await fetch('http://localhost:8000/api/token/refresh/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({refresh})
    });
    
    const data = await response.json();
    localStorage.setItem('access_token', data.access);
}

// 4. Avtomatik refresh (interceptor)
async function apiRequest(url, options = {}) {
    let token = localStorage.getItem('access_token');
    
    options.headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`
    };
    
    let response = await fetch(url, options);
    
    // Agar 401 bo'lsa - refresh qilish
    if (response.status === 401) {
        await refreshAccessToken();
        token = localStorage.getItem('access_token');
        options.headers['Authorization'] = `Bearer ${token}`;
        response = await fetch(url, options);
    }
    
    return response;
}
"""


# ============================================
# 11. SECURITY BEST PRACTICES
# ============================================

"""
JWT SECURITY CHECKLIST:

✅ HTTPS ishlatish (production'da majburiy)
✅ Access token lifetime qisqa (15-60 min)
✅ Refresh token lifetime uzun (7-30 days)
✅ Token blacklist yoqish
✅ CORS to'g'ri sozlash
✅ XSS dan himoya (sanitize input)
✅ CSRF token ishlatish (cookies bilan)
✅ Secure va HttpOnly cookie flags

❌ Token'ni URL'da yubormaslik
❌ Token'ni git'ga commit qilmaslik
❌ Token'ni console.log qilmaslik
❌ Public API'da long-lived token ishlatmaslik

STORAGE OPTIONS:

1. LocalStorage (oson, lekin XSS zaif)
   ✅ Oddiy
   ❌ XSS attack
   
2. SessionStorage (har safar login)
   ✅ Tab yopilsa o'chadi
   ❌ XSS attack
   
3. HttpOnly Cookies (eng xavfsiz)
   ✅ JavaScript'dan o'qib bo'lmaydi
   ✅ CSRF protection bilan
   ❌ Murakkab setup
   
4. Memory (Redux, Zustand)
   ✅ XSS dan himoya
   ❌ Refresh bo'lsa yo'qoladi
"""


# ============================================
# 12. TOKEN vs JWT XULOSA
# ============================================

"""
QACHON TOKEN ISHLATISH:

✅ Simple CRUD app
✅ Bitta server
✅ Admin panel
✅ Token revoke muhim
✅ Database tez

QACHON JWT ISHLATISH:

✅ Microservices
✅ Mobile app
✅ Scalable system
✅ Stateless kerak
✅ Cross-domain auth

KO'P HOLLARDA:
- Start with Token
- Upgrade to JWT when needed
"""


# ============================================
# TEST FUNKSIYASI
# ============================================

def show_jwt_info():
    """
    JWT haqida umumiy ma'lumot
    """
    print("=" * 60)
    print("JWT AUTHENTICATION INFO")
    print("=" * 60)
    
    print("\n📦 JWT STRUKTURA:")
    print("-" * 60)
    print("header.payload.signature")
    print("\nHeader: {\"alg\": \"HS256\", \"typ\": \"JWT\"}")
    print("Payload: {\"user_id\": 1, \"username\": \"john\", \"exp\": 1234567890}")
    print("Signature: HMACSHA256(base64(header) + \".\" + base64(payload), secret)")
    
    print("\n⚙️  SETTINGS:")
    print("-" * 60)
    print("ACCESS_TOKEN_LIFETIME: 60 minutes")
    print("REFRESH_TOKEN_LIFETIME: 7 days")
    print("ALGORITHM: HS256")
    
    print("\n🔄 WORKFLOW:")
    print("-" * 60)
    print("1. User login → Get access + refresh tokens")
    print("2. Use access token for API requests")
    print("3. Access token expires → Use refresh to get new access")
    print("4. Refresh token expires → Login again")
    
    print("\n📡 API ENDPOINTS:")
    print("-" * 60)
    print("POST /api/token/          - Login (get tokens)")
    print("POST /api/token/refresh/  - Refresh access token")