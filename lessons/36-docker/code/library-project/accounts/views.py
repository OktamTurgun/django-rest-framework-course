"""
Accounts app - Authentication views (Class-Based Views)
"""

# Django imports
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.core.cache import cache
from django.conf import settings
from django.db import connection

# REST framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token

# Simple JWT imports
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# dj-rest-auth imports
from dj_rest_auth.registration.views import SocialLoginView

# allauth imports
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers import registry
from allauth.socialaccount.models import SocialAccount

# Local app imports (serializers)
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserProfileSerializer,
    UserProfileSerializer,
    UpdateProfileSerializer,
    SetPasswordSerializer,
    SocialAccountSerializer,
)

# Python standard library imports
import secrets

import logging

logger = logging.getLogger(__name__)

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
            status=status.HTTP_400_BAD_REQUEST
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
        # Safely delete any token(s) for the user (if present)
        try:
            Token.objects.filter(user=request.user).delete()
        except Exception:
            # ignore any token deletion errors
            pass

        return Response(
            {'message': 'Muvaffaqiyatli logout qilindi'},
            status=status.HTTP_200_OK
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

    def patch(self, request):
        """Allow partial updates on the same user_info endpoint (first_name, last_name, email, bio)"""
        user = request.user
        # Update basic fields
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)

        new_email = request.data.get('email')
        if new_email and new_email != user.email:
            if User.objects.filter(email=new_email).exists():
                return Response({'error': 'Bu email allaqachon band'}, status=status.HTTP_400_BAD_REQUEST)
            user.email = new_email

        user.save()

        # Update profile.bio if provided
        try:
            profile = user.profile
            bio = request.data.get('bio', None)
            if bio is not None:
                profile.bio = bio
                profile.save()
        except Exception:
            pass

        return Response({
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
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

        # Update profile fields if provided
        try:
            profile = user.profile
            bio = request.data.get('bio', None)
            if bio is not None:
                profile.bio = bio
            location = request.data.get('location', None)
            if location is not None:
                profile.location = location
            birth_date = request.data.get('birth_date', None)
            if birth_date is not None:
                profile.birth_date = birth_date
            profile.save()
        except Exception:
            # If profile does not exist, ignore (signals should create it)
            pass
        
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
        new_password2 = request.data.get('new_password2')
        
        # Validatsiya
        if not old_password or not new_password or new_password2 is None:
            return Response(
                {'error': 'Eski va yangi parol talab qilinadi'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check new passwords match
        if new_password != new_password2:
            return Response(
                {'error': 'Yangi parollar mos emas'},
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

        # Do not rotate/delete tokens here to keep tests simple (client may still use same token)
        return Response({
            'message': 'Parol o\'zgartirildi'
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
    
"""
Social Authentication Views (Lesson 31)
========================================
"""

# ============================================================================
# SOCIAL LOGIN VIEWS
# ============================================================================

class GoogleLoginView(SocialLoginView):
    """Google OAuth2 login endpoint"""
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/auth/google/callback"
    client_class = OAuth2Client


class GitHubLoginView(SocialLoginView):
    """GitHub OAuth login endpoint"""
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://localhost:3000/auth/github/callback"
    client_class = OAuth2Client


# ============================================================================
# USER PROFILE VIEWS
# ============================================================================

class CurrentUserProfileView(APIView):
    """Get/Update current user profile"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get current user profile"""
        from .serializers import UserProfileSerializer
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        """Update current user profile"""
        from .serializers import UpdateProfileSerializer, UserProfileSerializer
        
        serializer = UpdateProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            profile_serializer = UserProfileSerializer(request.user)
            return Response(profile_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetPasswordView(APIView):
    """Set password for social auth users"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Set password"""
        from .serializers import SetPasswordSerializer
        
        serializer = SetPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(request.user)
            logger.info(f"✅ Password set for user: {request.user.username}")
            return Response({"message": "Password set successfully"})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================================================
# SOCIAL ACCOUNTS MANAGEMENT
# ============================================================================

class SocialAccountsListView(APIView):
    """List all connected social accounts"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """List social accounts"""
        from .serializers import SocialAccountSerializer
        
        social_accounts = SocialAccount.objects.filter(user=request.user)
        serializer = SocialAccountSerializer(social_accounts, many=True)
        
        return Response({
            "social_accounts": serializer.data,
            "has_password": request.user.has_usable_password(),
            "total_accounts": social_accounts.count()
        })


class SocialAccountDetailView(APIView):
    """Get specific social account details"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, provider):
        """Get social account details"""
        from .serializers import SocialAccountDetailSerializer
        
        try:
            social_account = SocialAccount.objects.get(
                user=request.user,
                provider=provider
            )
            serializer = SocialAccountDetailSerializer(social_account)
            return Response(serializer.data)
        except SocialAccount.DoesNotExist:
            return Response(
                {"error": f"No {provider} account connected"},
                status=status.HTTP_404_NOT_FOUND
            )


class DisconnectSocialAccountView(APIView):
    """Disconnect social account"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, provider):
        """Disconnect social account"""
        try:
            social_account = SocialAccount.objects.get(
                user=request.user,
                provider=provider
            )
            
            # Security check
            if not request.user.has_usable_password():
                other_accounts = SocialAccount.objects.filter(
                    user=request.user
                ).exclude(pk=social_account.pk)
                
                if not other_accounts.exists():
                    return Response(
                        {
                            "error": "Cannot disconnect last authentication method. "
                                   "Please set a password first."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            provider_name = provider.capitalize()
            social_account.delete()
            
            return Response({
                "message": f"{provider_name} account disconnected successfully"
            })
        
        except SocialAccount.DoesNotExist:
            return Response(
                {"error": f"No {provider} account connected"},
                status=status.HTTP_404_NOT_FOUND
            )


# ============================================================================
# HEALTH CHECK
# ============================================================================

class HealthCheckView(APIView):
    """Health check endpoint"""
    permission_classes = []

    def get(self, request):
        """Health check"""
        # DB tekshirish
        try:
            connection.ensure_connection()
            db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"

        social_providers = list(registry.provider_map.keys())

        return Response({
            "status": "ok" if db_status == "connected" else "error",
            "database": db_status,
            "social_providers": social_providers,
            "timestamp": timezone.now().isoformat(),
            "version": "1.0.0",
            "debug": settings.DEBUG,
        })



# ============================================================================
# ADMIN STATISTICS
# ============================================================================

class SocialAuthStatisticsView(APIView):
    """Social auth statistics (Admin only)"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get statistics"""
        if not request.user.is_staff:
            return Response(
                {"error": "Admin access required"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        from django.contrib.auth.models import User
        
        total_users = User.objects.count()
        social_users = User.objects.filter(
            socialaccount__isnull=False
        ).distinct().count()
        regular_users = total_users - social_users
        
        users_with_password = User.objects.exclude(
            password__in=['', '!']
        ).count()
        users_without_password = total_users - users_with_password
        
        provider_stats = {}
        for provider in ['google', 'github', 'facebook']:
            count = SocialAccount.objects.filter(provider=provider).count()
            provider_stats[provider] = count
        
        return Response({
            "total_users": total_users,
            "social_users": social_users,
            "regular_users": regular_users,
            "users_with_password": users_with_password,
            "users_without_password": users_without_password,
            "providers": provider_stats,
            "timestamp": timezone.now().isoformat()
        })