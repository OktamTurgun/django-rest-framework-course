"""
Accounts app - Authentication views (Class-Based Views)
"""

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

# === IMPORTS FOR HOMEWORK 1: PASSWORD RESET ===
import secrets
from django.core.cache import cache

# === IMPORTS FOR HOMEWORK 2: JWT AUTHENTICATION ===
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# === IMPORT FOR HOMEWORK 3: SESSION AUTHENTICATION
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authentication import SessionAuthentication

# === IMPORT FOR HOMEWORK 4: BASIC AUTHENTICATION
from rest_framework.authentication import BasicAuthentication

# === IMPORTS FOR LESSON 14: USER REGISTRATION ===
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserRegistrationSerializer, UserSerializer
from rest_framework.views import APIView


# ============================================
# REGISTER - Ro'yxatdan o'tish
# ============================================

class RegisterView(APIView):
    """
    Yangi foydalanuvchi ro'yxatdan o'tkazish
    
    POST /api/accounts/register-old/
    Body: {"username": "john", "password": "pass123", "email": "john@example.com"}
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        
        # Validatsiya
        if not username or not password:
            return Response(
                {'error': 'Username va password talab qilinadi'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Username mavjudligini tekshirish
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Bu username allaqachon band'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Email mavjudligini tekshirish
        if email and User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Bu email allaqachon band'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Foydalanuvchi yaratish
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            
            # Token yaratish
            token = Token.objects.create(user=user)
            
            return Response({
                'message': 'Foydalanuvchi muvaffaqiyatli yaratildi',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'token': token.key
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ============================================
# LOGIN - Tizimga kirish
# ============================================

class LoginView(APIView):
    """
    Foydalanuvchi login qilish va token olish
    
    POST /api/accounts/login/
    Body: {"username": "admin", "password": "admin123"}
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Validatsiya
        if not username or not password:
            return Response(
                {'error': 'Username va password talab qilinadi'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Autentifikatsiya
        user = authenticate(username=username, password=password)
        
        if user:
            # Token yaratish yoki olish
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login muvaffaqiyatli',
                'token': token.key,
                'user': {
                    'id': user.pk,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'created': created  # Yangi token yaratildimi?
            }, status=status.HTTP_200_OK)
        
        return Response(
            {"error": "Username yoki parol noto'g'ri"},
            status=status.HTTP_401_UNAUTHORIZED
        )


# ============================================
# LOGOUT - Tizimdan chiqish
# ============================================

class LogoutView(APIView):
    """
    Foydalanuvchi logout qilish va tokenni o'chirish
    
    POST /api/accounts/logout/
    Header: Authorization: Token <token>
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Foydalanuvchining tokenini o'chirish
            request.user.auth_token.delete()
            return Response(
                {'message': 'Muvaffaqiyatli logout qilindi'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# ============================================
# PROFILE - Foydalanuvchi profili
# ============================================

class UserInfoView(APIView):
    """
    Foydalanuvchi ma'lumotlarini ko'rish
    
    GET /api/accounts/me/
    Header: Authorization: Token <token>
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'date_joined': user.date_joined,
            'last_login': user.last_login
        }, status=status.HTTP_200_OK)


# ============================================
# PROFILE UPDATE - Profil yangilash
# ============================================

class ProfileUpdateView(APIView):
    """
    Profil yangilash
    
    PUT/PATCH /api/accounts/profile/update/
    Header: Authorization: Token <token>
    Body: {"first_name": "John", "last_name": "Doe", "email": "new@example.com"}
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        return self._update_profile(request)
    
    def patch(self, request):
        return self._update_profile(request)
    
    def _update_profile(self, request):
        user = request.user
        
        # Ma'lumotlarni yangilash
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        
        # Email yangilash
        new_email = request.data.get('email')
        if new_email and new_email != user.email:
            if User.objects.filter(email=new_email).exists():
                return Response(
                    {'error': 'Bu email allaqachon band'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.email = new_email
        
        user.save()
        
        return Response({
            'message': 'Profil yangilandi',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_200_OK)


# ============================================
# CHANGE PASSWORD - Parol o'zgartirish
# ============================================

class ChangePasswordView(APIView):
    """
    Parol o'zgartirish
    
    POST /api/accounts/change-password/
    Header: Authorization: Token <token>
    Body: {"old_password": "old123", "new_password": "new456"}
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        # Validatsiya
        if not old_password or not new_password:
            return Response(
                {'error': 'Eski va yangi parol talab qilinadi'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Eski parolni tekshirish
        if not user.check_password(old_password):
            return Response(
                {'error': 'Eski parol noto\'g\'ri'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Yangi parolni o'rnatish
        user.set_password(new_password)
        user.save()
        
        # Token yangilash
        Token.objects.filter(user=user).delete()
        new_token = Token.objects.create(user=user)
        
        return Response({
            'message': 'Parol o\'zgartirildi',
            'token': new_token.key
        }, status=status.HTTP_200_OK)
    
# ============================================
# HOMEWORK 1: PASSWORD RESET (Token Auth)
# ============================================
class PasswordResetRequestView(APIView):
    """
    Email orqali parol tiklash so'rovi
    
    POST /api/accounts/password-reset-request/
    Body: {"email": "user@example.com"}
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'Email talab qilinadi'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
            
            # 6 ta raqamli kod yaratish
            reset_code = secrets.randbelow(1000000)
            reset_code = f"{reset_code:06d}"  # 000123 formatda
            
            # Cache'da 15 daqiqa (900 sekund) saqlash
            cache_key = f'password_reset_{email}'
            cache.set(cache_key, reset_code, timeout=900)
            
            # Console'da ko'rsatish (email o'rniga)
            print(f"\n{'='*60}")
            print(f"PASSWORD RESET CODE for {email}")
            print(f"Code: {reset_code}")
            print(f"Valid for: 15 minutes")
            print(f"{'='*60}\n")
            
            return Response({
                'message': 'Reset code yuborildi (console ga qarang)',
                'email': email,
                'expires_in': '15 minutes'
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            # Security: email mavjud emasligini aytmaymiz
            return Response({
                'message': 'Agar email to\'g\'ri bo\'lsa, kod yuborildi'
            }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    Reset code bilan yangi parol o'rnatish
    
    POST /api/accounts/password-reset-confirm/
    Body: {
        "email": "user@example.com",
        "reset_code": "123456",
        "new_password": "newpass123"
    }
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        email = request.data.get('email')
        reset_code = request.data.get('reset_code')
        new_password = request.data.get('new_password')
        
        # Validatsiya
        if not all([email, reset_code, new_password]):
            return Response(
                {'error': 'Email, reset_code va new_password talab qilinadi'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cache'dan kodni olish
        cache_key = f'password_reset_{email}'
        cached_code = cache.get(cache_key)
        
        if not cached_code:
            return Response(
                {'error': 'Reset code muddati o\'tgan yoki mavjud emas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if cached_code != reset_code:
            return Response(
                {'error': 'Reset code noto\'g\'ri'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
            
            # Yangi parolni o'rnatish
            user.set_password(new_password)
            user.save()
            
            # Cache'dan code'ni o'chirish
            cache.delete(cache_key)
            
            # Barcha eski tokenlarni o'chirish (security)
            Token.objects.filter(user=user).delete()
            
            # Yangi token yaratish
            new_token = Token.objects.create(user=user)
            
            return Response({
                'message': 'Parol muvaffaqiyatli o\'zgartirildi',
                'token': new_token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response(
                {'error': 'User topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )
        
# ============================================
# HOMEWORK 2: JWT AUTHENTICATION
# ============================================
class CustomJWTSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer - qo'shimcha ma'lumotlar bilan
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Token payload'ga qo'shimcha claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Response'ga qo'shimcha ma'lumot
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        }
        
        return data


class JWTLoginView(TokenObtainPairView):
    """
    JWT Login - Custom response bilan
    
    POST /api/accounts/jwt/login/
    Body: {"username": "john", "password": "pass123"}
    
    Response:
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "user": {...}
    }
    """
    serializer_class = CustomJWTSerializer

# ============================================
# HOMEWORK 3: SESSION AUTHENTICATION
# ============================================


class SessionLoginView(APIView):
    """
    Session-based login (Cookie bilan)
    
    POST /api/accounts/session/login/
    Body: {"username": "john", "password": "pass123"}
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username va password talab qilinadi'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authenticate
        user = authenticate(username=username, password=password)
        
        if user:
            # Django session yaratish
            django_login(request, user)
            
            return Response({
                'message': 'Session login muvaffaqiyatli',
                'session_key': request.session.session_key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)
        
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class SessionLogoutView(APIView):
    """
    Session logout
    
    POST /api/accounts/session/logout/
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    
    def post(self, request):
        django_logout(request)
        return Response({
            'message': 'Session logout muvaffaqiyatli'
        }, status=status.HTTP_200_OK)


class SessionUserInfoView(APIView):
    """
    Session bilan user info
    
    GET /api/accounts/session/me/
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'session_key': request.session.session_key,
        }, status=status.HTTP_200_OK)
    
# ============================================
# HOMEWORK 4: BASIC AUTHENTICATION
# ============================================


class BasicAuthUserInfoView(APIView):
    """
    Basic Authentication bilan user info
    
    GET /api/accounts/basic/me/
    
    Authorization: Basic base64(username:password)
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'message': 'Basic Authentication successful',
            'auth_type': 'Basic Auth',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_200_OK)


class BasicAuthTestView(APIView):
    """
    Basic Auth test endpoint
    
    POST /api/accounts/basic/test/
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({
            'message': 'Basic Auth POST request successful',
            'username': request.user.username,
            'data_received': request.data
        })
    
# ============================================
# LESSON 14: USER REGISTRATION (3 VARIANT)
# ============================================

from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserSerializer


# ========================================
# VARIANT 1: FUNCTION-BASED VIEW
# ========================================

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Function-based registration
    
    POST /api/accounts/register/
    
    Body: {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "SecurePass123!",
        "password2": "SecurePass123!"
    }
    """
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        user_serializer = UserSerializer(user)
        
        return Response({
            'user': user_serializer.data,
            'message': 'Foydalanuvchi muvaffaqiyatli ro\'yxatdan o\'tdi (Function-based)'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================================
# VARIANT 2: CLASS-BASED VIEW (APIView)
# ========================================

class RegisterUserAPIView(APIView):
    """
    Class-based registration (APIView)
    
    POST /api/accounts/register-class/
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserSerializer(user)
            
            return Response({
                'user': user_serializer.data,
                'message': 'Foydalanuvchi muvaffaqiyatli ro\'yxatdan o\'tdi (APIView)'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================================
# VARIANT 3: GENERIC VIEW (Professional)
# ========================================

class RegisterUserGenericView(generics.CreateAPIView):
    """
    Generic view registration (Professional)
    
    POST /api/accounts/register-generic/
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        user_serializer = UserSerializer(user)
        headers = self.get_success_headers(serializer.data)
        
        return Response({
            'user': user_serializer.data,
            'message': 'Foydalanuvchi muvaffaqiyatli ro\'yxatdan o\'tdi (Generic)'
        }, status=status.HTTP_201_CREATED, headers=headers)