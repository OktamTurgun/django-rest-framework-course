# accounts/models.py
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
    
    # EXISTING FIELDS (keep as is)
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
    
    # NEW: Avatar fields
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
    
    # NEW: Timestamps
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']
    
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


# EXISTING SIGNALS (keep as is)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()