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


# ============================================
# REGISTER - Ro'yxatdan o'tish
# ============================================

class RegisterView(APIView):
    """
    Yangi foydalanuvchi ro'yxatdan o'tkazish
    
    POST /api/accounts/register/
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