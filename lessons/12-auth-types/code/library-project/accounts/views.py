from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    """
    Foydalanuvchi login qilish va token olish
    
    POST /api/accounts/login/
    Body: {"username": "admin", "password": "admin123"}
    """
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
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'email': user.email,
                'created': created  # Yangi token yaratildimi?
            }, status=status.HTTP_200_OK)
        
        return Response(
            {"error": "Login yoki parol noto'g'ri"},
            status=status.HTTP_401_UNAUTHORIZED
        )


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
        })
