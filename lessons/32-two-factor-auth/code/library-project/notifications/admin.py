from django.contrib import admin
from .models import NotificationLog, DeviceToken, UserPreferences

"""
Notifications Admin
===================

Django admin interface for notification models
"""

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    """NotificationLog admin"""
    
    list_display = [
        'id', 'user', 'notification_type', 'status', 
        'title', 'sent_at'
    ]
    
    list_filter = [
        'notification_type', 'status', 'sent_at'
    ]
    
    search_fields = [
        'user__username', 'title', 'message', 'recipient'
    ]
    
    readonly_fields = [
        'sent_at', 'delivered_at'
    ]
    
    date_hierarchy = 'sent_at'
    
    fieldsets = (
        ('Asosiy Ma\'lumot', {
            'fields': ('user', 'notification_type', 'status')
        }),
        ('Xabar', {
            'fields': ('title', 'message', 'recipient')
        }),
        ('Vaqt', {
            'fields': ('sent_at', 'delivered_at')
        }),
        ('Xato', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
    )


@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    """DeviceToken admin"""
    
    list_display = [
        'id', 'user', 'device_type', 'device_name', 
        'is_active', 'created_at', 'last_used'
    ]
    
    list_filter = [
        'device_type', 'is_active', 'created_at'
    ]
    
    search_fields = [
        'user__username', 'token', 'device_name'
    ]
    
    readonly_fields = [
        'created_at', 'updated_at', 'last_used'
    ]
    
    actions = ['deactivate_tokens', 'activate_tokens']
    
    def deactivate_tokens(self, request, queryset):
        """Tokenlarni deaktivatsiya qilish"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} ta token deaktivatsiya qilindi')
    deactivate_tokens.short_description = 'Tokenlarni deaktivatsiya qilish'
    
    def activate_tokens(self, request, queryset):
        """Tokenlarni aktivatsiya qilish"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} ta token aktivatsiya qilindi')
    activate_tokens.short_description = 'Tokenlarni aktivatsiya qilish'


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    """UserPreferences admin"""
    
    list_display = [
        'user', 'email_enabled', 'sms_enabled', 'push_enabled',
        'quiet_hours_enabled', 'updated_at'
    ]
    
    list_filter = [
        'email_enabled', 'sms_enabled', 'push_enabled',
        'quiet_hours_enabled'
    ]
    
    search_fields = [
        'user__username', 'user__email'
    ]
    
    readonly_fields = [
        'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Foydalanuvchi', {
            'fields': ('user',)
        }),
        ('Kanal Sozlamalari', {
            'fields': ('email_enabled', 'sms_enabled', 'push_enabled')
        }),
        ('Sokin Soatlar', {
            'fields': (
                'quiet_hours_enabled', 
                'quiet_hours_start', 
                'quiet_hours_end'
            )
        }),
        ('Bildirishnoma Turlari', {
            'fields': (
                'new_book_notifications',
                'due_date_reminders',
                'overdue_notifications',
                'system_notifications'
            )
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
