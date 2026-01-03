"""
users/serializers.py - 2FA Serializers
"""

from rest_framework import serializers
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth import get_user_model
from .models import BackupCode, SMSVerification

User = get_user_model()


class TOTPSetupSerializer(serializers.Serializer):
    """Serializer for TOTP setup response"""
    secret_key = serializers.CharField(read_only=True)
    qr_code = serializers.CharField(read_only=True)
    manual_entry_key = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)


class TOTPVerifySerializer(serializers.Serializer):
    """Serializer for TOTP token verification"""
    token = serializers.CharField(max_length=6, min_length=6)
    
    def validate_token(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "Token faqat raqamlardan iborat bo'lishi kerak"
            )
        return value


class SMSSetupSerializer(serializers.Serializer):
    """Serializer for SMS setup"""
    phone_number = serializers.CharField()
    
    def validate_phone_number(self, value):
        from phonenumber_field.phonenumber import to_python
        phone = to_python(value)
        if not phone or not phone.is_valid():
            raise serializers.ValidationError(
                "Telefon raqami noto'g'ri formatda"
            )
        return str(phone)


class SMSVerifySerializer(serializers.Serializer):
    """Serializer for SMS code verification"""
    code = serializers.CharField(max_length=6, min_length=6)
    
    def validate_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "Kod faqat raqamlardan iborat bo'lishi kerak"
            )
        return value


class BackupCodeSerializer(serializers.ModelSerializer):
    """Serializer for backup codes"""
    class Meta:
        model = BackupCode
        fields = ['code', 'used', 'used_at', 'created_at']
        read_only_fields = ['code', 'used', 'used_at', 'created_at']


class BackupCodeVerifySerializer(serializers.Serializer):
    """Serializer for backup code verification"""
    code = serializers.CharField(max_length=10, min_length=10)
    
    def validate_code(self, value):
        return value.upper().strip()


class TwoFactorStatusSerializer(serializers.Serializer):
    """Serializer for 2FA status"""
    two_factor_enabled = serializers.BooleanField(read_only=True)
    two_factor_method = serializers.CharField(read_only=True)
    has_totp = serializers.BooleanField(read_only=True)
    has_sms = serializers.BooleanField(read_only=True)
    backup_codes_count = serializers.IntegerField(read_only=True)


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']