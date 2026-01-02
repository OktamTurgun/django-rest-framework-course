from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

User = get_user_model()


class Profile(models.Model):
    """
    User Profile - Extended for Lesson 28
    Combines: existing fields + avatar + borrow statistics
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    
    bio = models.TextField(blank=True, default='')
    location = models.CharField(max_length=100, blank=True, default='')
    birth_date = models.DateField(null=True, blank=True)
    
    # NEW: Additional contact info
    phone = models.CharField(max_length=20, blank=True)
    
    # NEW: Membership fields
    is_premium = models.BooleanField(default=False)
    membership_type = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('basic', 'Basic'),
            ('premium', 'Premium')
        ],
        default='free'
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )
    avatar_thumbnail = models.ImageField(
        upload_to='avatars/thumbnails/',
        blank=True,
        null=True
    )
    
    # NEW: Lesson 28 - Borrow statistics
    books_borrowed = models.IntegerField(default=0)
    books_returned = models.IntegerField(default=0)
    subscribed_to_notifications = models.BooleanField(default=True)

    # ============================================================================
    # NEW: Social Authentication Fields (Lesson 31)
    # ============================================================================
    
    # Social profile data
    profile_picture_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text="Profile picture from social providers (Google, GitHub)"
    )
    company = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Company name from GitHub"
    )
    website = models.URLField(
        max_length=200, 
        blank=True, 
        null=True,
        help_text="Personal website"
    )
    
    # GitHub specific
    github_url = models.URLField(
        max_length=200, 
        blank=True, 
        null=True,
        help_text="GitHub profile URL"
    )
    github_username = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="GitHub username"
    )
    
    # Social links
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    
    # Preferences
    language = models.CharField(
        max_length=10, 
        default='en',
        help_text="Preferred language (from Google OAuth)"
    )
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Verification
    email_verified = models.BooleanField(
        default=False,
        help_text="Email verified (automatically True for social auth)"
    )
    phone_verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    # ============================================================================
    # Properties (Helper methods)
    # ============================================================================
    
    @property
    def full_name(self):
        """Get user's full name"""
        full = f"{self.user.first_name} {self.user.last_name}".strip()
        return full if full else self.user.username
    
    @property
    def is_social_authenticated(self):
        """Check if user has any social authentication"""
        return self.user.socialaccount_set.exists()
    
    @property
    def social_providers(self):
        """Get list of connected social providers"""
        return [acc.provider for acc in self.user.socialaccount_set.all()]
    
    @property
    def display_picture(self):
        """
        Get display picture with priority:
        1. Uploaded avatar (if exists)
        2. Social profile picture URL (from Google/GitHub)
        3. Default placeholder
        """
        if self.avatar:
            return self.avatar.url
        elif self.profile_picture_url:
            return self.profile_picture_url
        else:
            return '/static/images/default-avatar.png'  # Default placeholder
    
    @property
    def has_github(self):
        """Check if user has GitHub account connected"""
        return self.user.socialaccount_set.filter(provider='github').exists()
    
    @property
    def has_google(self):
        """Check if user has Google account connected"""
        return self.user.socialaccount_set.filter(provider='google').exists()
    
    # ============================================================================
    # Methods
    # ============================================================================
    
    def save(self, *args, **kwargs):
        """Avatar yuklanganda thumbnail yaratish"""
        if self.avatar and not self.avatar_thumbnail:
            try:
                self.avatar_thumbnail = self.make_thumbnail(self.avatar, size=(150, 150))
            except Exception as e:
                print(f"Thumbnail creation error: {e}")
        
        super().save(*args, **kwargs)
    
    def make_thumbnail(self, image, size=(150, 150)):
        """Thumbnail yaratish"""
        try:
            img = Image.open(image)
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=85)
            thumb_io.seek(0)
            
            name, ext = os.path.splitext(image.name)
            thumb_filename = f'{name}_thumb.jpg'
            
            thumbnail = InMemoryUploadedFile(
                thumb_io,
                None,
                thumb_filename,
                'image/jpeg',
                thumb_io.tell(),
                None
            )
            
            return thumbnail
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return None
    
    def get_social_account_data(self, provider):
        """
        Get social account data for specific provider
        
        Args:
            provider (str): 'google' or 'github'
            
        Returns:
            dict: Social account extra_data or None
        """
        try:
            social_account = self.user.socialaccount_set.get(provider=provider)
            return social_account.extra_data
        except:
            return None
