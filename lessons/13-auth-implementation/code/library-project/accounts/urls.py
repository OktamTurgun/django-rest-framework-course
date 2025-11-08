"""
Accounts app URL Configuration
"""

from django.urls import path
from . import views

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
]