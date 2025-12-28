"""
Accounts app URL Configuration
"""

from django.urls import path
from . import views
from .views import register_user

# === IMPORTS FOR HOMEWORK 2: JWT AUTHENTICATION ===
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = 'accounts'

urlpatterns = [
    # ========================================
    # LESSON 12-13: Old Authentication
    # ========================================
    # Authentication
    path('register-old/', views.RegisterView.as_view(), name='register-old'),
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

    # ========================================
    # LESSON 14: New User Registration (with Serializer)
    # ========================================
    # Function-based
    path('register/', views.register_user, name='register'),
    
    # Class-based (APIView)
    path('register-class/', views.RegisterUserAPIView.as_view(), name='register-class'),
    
    # Class-based (Generic)
    path('register-generic/', views.RegisterUserGenericView.as_view(), name='register-generic'),
    
    # ========================================
    # LESSON 31: SOCIAL AUTHENTICATION (NEW)
    # ========================================
    
    # ===== REST API Social Login (for Frontend apps) =====
    # Bu endpoints Frontend (React, Vue, Flutter) uchun
    path('auth/social/google/', views.GoogleLoginView.as_view(), name='google_login'),
    path('auth/social/github/', views.GitHubLoginView.as_view(), name='github_login'),
    
    # ===== User Profile Management =====
    path('users/me/', views.CurrentUserProfileView.as_view(), name='current_user_profile'),
    path('users/me/set-password/', views.SetPasswordView.as_view(), name='set_password'),
    
    # ===== Social Accounts Management =====
    path('users/me/social/', views.SocialAccountsListView.as_view(), name='social_accounts_list'),
    path('users/me/social/<str:provider>/', views.SocialAccountDetailView.as_view(), name='social_account_detail'),
    path('users/me/social/<str:provider>/disconnect/', views.DisconnectSocialAccountView.as_view(), name='disconnect_social'),
    
    # ===== Health Check =====
    path('health/', views.HealthCheckView.as_view(), name='health_check'),
    
    # ===== Admin Stats (Optional) =====
    path('admin/social-stats/', views.SocialAuthStatisticsView.as_view(), name='social_stats'),
]