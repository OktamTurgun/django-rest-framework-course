from django.contrib import admin
from .models import BackupCode, SMSVerification


@admin.register(BackupCode)
class BackupCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'used', 'created_at', 'used_at']
    list_filter = ['used', 'created_at']
    search_fields = ['user__username', 'code']
    readonly_fields = ['code', 'created_at', 'used_at']


@admin.register(SMSVerification)
class SMSVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'code', 'verified', 'created_at', 'expires_at']
    list_filter = ['verified', 'created_at']
    search_fields = ['user__username', 'phone_number', 'code']
    readonly_fields = ['code', 'created_at', 'expires_at']