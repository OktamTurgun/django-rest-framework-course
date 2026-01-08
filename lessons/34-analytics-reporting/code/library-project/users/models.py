"""
users/models.py - Two-Factor Authentication Models
"""

from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
import secrets
import string
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class BackupCode(models.Model):
    """
    Backup codes for 2FA recovery
    
    One-time use codes that users can use when they lose access
    to their authenticator app
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='backup_codes'
    )
    code = models.CharField(max_length=10, unique=True)
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'backup_codes'
        ordering = ['-created_at']
        verbose_name = 'Backup Code'
        verbose_name_plural = 'Backup Codes'
    
    def __str__(self):
        status = 'Used' if self.used else 'Active'
        return f"{self.user.username} - {self.code} ({status})"
    
    @staticmethod
    def generate_code():
        """Generate a 10-character backup code"""
        characters = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(characters) for _ in range(10))
    
    @classmethod
    def generate_codes_for_user(cls, user, count=10):
        """
        Generate backup codes for a user
        
        Args:
            user: User instance
            count: Number of codes to generate (default: 10)
            
        Returns:
            list: List of generated codes (strings)
        """
        codes = []
        for _ in range(count):
            code = cls.generate_code()
            backup_code = cls.objects.create(user=user, code=code)
            codes.append(code)
        return codes
    
    def mark_as_used(self):
        """Mark backup code as used"""
        self.used = True
        self.used_at = timezone.now()
        self.save()


class SMSVerification(models.Model):
    """
    SMS verification for 2FA
    
    Stores verification codes sent via SMS
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()
    code = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=3)
    
    class Meta:
        db_table = 'sms_verifications'
        ordering = ['-created_at']
        verbose_name = 'SMS Verification'
        verbose_name_plural = 'SMS Verifications'
    
    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"
    
    @staticmethod
    def generate_code():
        """Generate a 6-digit SMS code"""
        return ''.join(secrets.choice(string.digits) for _ in range(6))
    
    def is_expired(self):
        """Check if code is expired"""
        return timezone.now() > self.expires_at
    
    @classmethod
    def create_verification(cls, user, phone_number):
        """
        Create a new SMS verification
        
        Args:
            user: User instance
            phone_number: Phone number to send code to
            
        Returns:
            SMSVerification: New verification instance
        """
        code = cls.generate_code()
        expires_at = timezone.now() + timedelta(minutes=10)
        
        return cls.objects.create(
            user=user,
            phone_number=phone_number,
            code=code,
            expires_at=expires_at
        )
