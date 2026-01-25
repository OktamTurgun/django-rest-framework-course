"""
users/urls.py - 2FA URL Configuration
"""

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # ==================== TOTP URLs ====================
    path('2fa/totp/setup/', views.setup_totp, name='totp-setup'),
    path('2fa/totp/verify-setup/', views.verify_totp_setup, name='totp-verify-setup'),
    path('2fa/totp/verify/', views.verify_totp_login, name='totp-verify-login'),
    
    # ==================== Backup Codes URLs ====================
    path('2fa/backup-codes/', views.get_backup_codes, name='get-backup-codes'),
    path('2fa/backup-codes/regenerate/', views.regenerate_backup_codes, name='regenerate-backup-codes'),
    path('2fa/backup-codes/verify/', views.verify_backup_code, name='verify-backup-code'),
    
    # ==================== General 2FA URLs ====================
    path('2fa/status/', views.two_factor_status, name='2fa-status'),
    path('2fa/disable/', views.disable_two_factor, name='disable-2fa'),
]