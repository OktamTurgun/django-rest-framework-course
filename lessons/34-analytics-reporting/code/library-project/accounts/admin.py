from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'membership_type', 
        'is_social_authenticated',
        'email_verified',
        'created_at'
    ]
    list_filter = [
        'membership_type', 
        'is_premium',
        'email_verified',
        'created_at'
    ]
    search_fields = ['user__username', 'user__email', 'bio']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'bio', 'birth_date')
        }),
        ('Contact', {
            'fields': ('phone', 'location', 'website')
        }),
        ('Social Auth', {
            'fields': (
                'profile_picture_url',
                'github_url',
                'github_username',
                'company',
                'linkedin_url',
                'twitter_url'
            )
        }),
        ('Membership', {
            'fields': ('membership_type', 'is_premium')
        }),
        ('Statistics', {
            'fields': ('books_borrowed', 'books_returned')
        }),
        ('Verification', {
            'fields': ('email_verified', 'phone_verified')
        }),
        ('Preferences', {
            'fields': ('language', 'timezone', 'subscribed_to_notifications')
        }),
        ('Media', {
            'fields': ('avatar', 'avatar_thumbnail')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def is_social_authenticated(self, obj):
        """Show if user has social auth"""
        return obj.is_social_authenticated
    is_social_authenticated.boolean = True
    is_social_authenticated.short_description = 'Social Auth'
