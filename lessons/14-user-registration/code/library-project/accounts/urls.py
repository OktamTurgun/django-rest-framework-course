"""
Accounts app URL Configuration
"""

from django.urls import path
from . import views

# === IMPORTS FOR HOMEWORK 2: JWT AUTHENTICATION ===
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Profile
    path('me/', views.UserInfoView.as_view(), name='user_info'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    
    # Password
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),

    # Homework 1: Password Reset
    path('password-reset-request/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Homework 2: JWT Authentication
    path('jwt/login/', views.JWTLoginView.as_view(), name='jwt_login'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),

    # Homework 3: Session Authentication
    path('session/login/', views.SessionLoginView.as_view(), name='session_login'),
    path('session/logout/', views.SessionLogoutView.as_view(), name='session_logout'),
    path('session/me/', views.SessionUserInfoView.as_view(), name='session_user_info'),

    # Homework 4: Basic Authentication
    path('basic/me/', views.BasicAuthUserInfoView.as_view(), name='basic_auth_user_info'),
    path('basic/test/', views.BasicAuthTestView.as_view(), name='basic_auth_test'),
]