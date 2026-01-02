# Lesson 32: Two-Factor Authentication (2FA)

## Mundarija
1. [Kirish](#kirish)
2. [2FA nima?](#2fa-nima)
3. [2FA turlari](#2fa-turlari)
4. [O'rnatish](#ornatish)
5. [Loyihani sozlash](#loyihani-sozlash)
6. [Models](#models)
7. [Serializers](#serializers)
8. [Views](#views)
9. [URLs](#urls)
10. [Postman testlar](#postman-testlar)
11. [Best Practices](#best-practices)
12. [Xulosa](#xulosa)

---

## Kirish

Two-Factor Authentication (2FA) - bu ikki bosqichli autentifikatsiya tizimi. Foydalanuvchi login va paroldan tashqari, qo'shimcha kod yoki tasdiqlashni ham o'tkazishi kerak.

### Nima uchun 2FA kerak?

- ✅ Xavfsizlikni oshiradi
- ✅ Parol o'g'irlansa ham himoya qiladi
- ✅ Hacking hujumlaridan saqlaydi
- ✅ Professional ilovalarda majburiy

---

## 2FA nima?

**2FA (Two-Factor Authentication)** - bu ikki bosqichli tasdiqlash:

1. **Birinchi bosqich:** Username va parol
2. **Ikkinchi bosqich:** TOTP kod, SMS kod, yoki backup kod

### Misol:
```
1. Username: johndoe
2. Password: mypassword123
3. 2FA Code: 123456  ← Bu qo'shimcha himoya!
```

---

## 2FA turlari

### 1. TOTP (Time-based One-Time Password)
- Google Authenticator
- Microsoft Authenticator  
- Authy ilovalarida ishlaydi
- Har 30 sekundda yangi kod generatsiya qiladi
- Internet kerak emas

### 2. SMS Verification
- Telefon raqamiga SMS yuboriladi
- 6 xonali kod keladi
- Internet kerak
- Telefon raqami talab qilinadi

### 3. Backup Codes
- Authenticator yo'qolsa ishlatiladi
- Bir martalik kodlar
- 10 ta kod beriladi
- Xavfsiz joyda saqlanadi

---

## O'rnatish

### 1. Virtual environment faollashtiring

```bash
# Windows (pipenv)
cd C:\Users\User\Documents\GitHub\django-rest-framework-course\lessons\32-two-factor-auth\code\library-project
pipenv shell

# Linux/Mac (pipenv)
cd ~/django-rest-framework-course/lessons/32-two-factor-auth/code/library-project
pipenv shell
```

### 2. Kerakli paketlarni o'rnating

```bash
# pipenv bilan
pipenv install django-otp==1.3.0
pipenv install qrcode==7.4.2
pipenv install pyotp==2.9.0
pipenv install django-phonenumber-field==7.3.0
pipenv install phonenumbers==8.13.27
pipenv install Pillow==10.1.0

# yoki pip bilan
pip install django-otp==1.3.0 qrcode==7.4.2 pyotp==2.9.0 django-phonenumber-field==7.3.0 phonenumbers==8.13.27 Pillow==10.1.0
```

### 3. Pipfile tekshirish

```bash
pipenv graph
```

---

## Loyihani sozlash

### settings.py

`library_project/settings.py` faylini oching va quyidagilarni qo'shing:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'rest_framework.authtoken',
    'django_otp',                          # ← YANGI
    'django_otp.plugins.otp_totp',         # ← YANGI
    'django_otp.plugins.otp_static',       # ← YANGI
    'phonenumber_field',                   # ← YANGI
    
    # Local apps
    'users',
    'books',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',  # ← YANGI (AuthenticationMiddleware dan keyin!)
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# OTP Settings
OTP_TOTP_ISSUER = 'Library Project'
OTP_LOGIN_URL = '/api/v1/users/2fa/verify/'

# Media files (QR code uchun)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## Models

### users/models.py

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import secrets
import string
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    
    # 2FA fields
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_method = models.CharField(
        max_length=10,
        choices=[
            ('totp', 'TOTP'),
            ('sms', 'SMS'),
            ('none', 'None')
        ],
        default='none'
    )
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username


class BackupCode(models.Model):
    """Backup codes for 2FA recovery"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='backup_codes')
    code = models.CharField(max_length=10, unique=True)
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'backup_codes'
        ordering = ['-created_at']
    
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
        """Generate backup codes for a user"""
        codes = []
        for _ in range(count):
            code = cls.generate_code()
            backup_code = cls.objects.create(user=user, code=code)
            codes.append(code)
        return codes


class SMSVerification(models.Model):
    """SMS verification for 2FA"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()
    code = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'sms_verifications'
        ordering = ['-created_at']
    
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
        """Create a new SMS verification"""
        code = cls.generate_code()
        expires_at = timezone.now() + timedelta(minutes=10)
        
        return cls.objects.create(
            user=user,
            phone_number=phone_number,
            code=code,
            expires_at=expires_at
        )
```

### Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Serializers

### users/serializers.py

```python
from rest_framework import serializers
from django_otp.plugins.otp_totp.models import TOTPDevice
from .models import User, BackupCode, SMSVerification


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
            raise serializers.ValidationError("Token faqat raqamlardan iborat bo'lishi kerak")
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


class TwoFactorStatusSerializer(serializers.ModelSerializer):
    """Serializer for 2FA status"""
    has_totp = serializers.SerializerMethodField()
    has_sms = serializers.SerializerMethodField()
    backup_codes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'two_factor_enabled',
            'two_factor_method',
            'has_totp',
            'has_sms',
            'backup_codes_count'
        ]
    
    def get_has_totp(self, obj):
        return TOTPDevice.objects.filter(user=obj, confirmed=True).exists()
    
    def get_has_sms(self, obj):
        return bool(obj.phone_number)
    
    def get_backup_codes_count(self, obj):
        return BackupCode.objects.filter(user=obj, used=False).count()
```

---

## Views

### users/views.py

```python
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.utils import timezone
import pyotp
import qrcode
import io
import base64

from .models import User, BackupCode
from .serializers import (
    TOTPSetupSerializer,
    TOTPVerifySerializer,
    BackupCodeSerializer,
    BackupCodeVerifySerializer,
    TwoFactorStatusSerializer
)


# ==================== TOTP Views ====================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setup_totp(request):
    """
    Setup TOTP for authenticated user
    
    POST /api/v1/users/2fa/totp/setup/
    """
    user = request.user
    
    # Delete existing unconfirmed devices
    TOTPDevice.objects.filter(user=user, confirmed=False).delete()
    
    # Create new device
    device = TOTPDevice.objects.create(user=user, name='default', confirmed=False)
    
    # Generate secret key
    secret = pyotp.random_base32()
    device.key = secret
    device.save()
    
    # Create OTP URI
    totp = pyotp.TOTP(secret)
    otp_uri = totp.provisioning_uri(
        name=user.email or user.username,
        issuer_name='Library Project'
    )
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(otp_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    data = {
        'secret_key': secret,
        'qr_code': f'data:image/png;base64,{qr_code_base64}',
        'manual_entry_key': secret,
        'message': 'QR kodni Google Authenticator ilovasida skanerlang yoki manual kiriting'
    }
    
    serializer = TOTPSetupSerializer(data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_totp_setup(request):
    """
    Verify TOTP setup
    
    POST /api/v1/users/2fa/totp/verify-setup/
    Body: {"token": "123456"}
    """
    serializer = TOTPVerifySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    token = serializer.validated_data['token']
    
    # Find unconfirmed device
    device = TOTPDevice.objects.filter(user=user, confirmed=False).first()
    if not device:
        return Response(
            {'error': 'TOTP device topilmadi. Avval setup qiling'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verify token
    totp = pyotp.TOTP(device.key)
    if not totp.verify(token, valid_window=1):
        return Response(
            {'error': 'Token noto\'g\'ri yoki muddati o\'tgan'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Confirm device
    device.confirmed = True
    device.save()
    
    # Update user
    user.two_factor_enabled = True
    user.two_factor_method = 'totp'
    user.save()
    
    # Generate backup codes
    backup_codes = BackupCode.generate_codes_for_user(user)
    
    return Response({
        'message': 'TOTP muvaffaqiyatli faollashtirildi',
        'backup_codes': backup_codes,
        'warning': 'Backup kodlarni xavfsiz joyda saqlang!'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_totp_login(request):
    """
    Verify TOTP token during login
    
    POST /api/v1/users/2fa/totp/verify/
    Body: {"token": "123456"}
    """
    serializer = TOTPVerifySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    token = serializer.validated_data['token']
    
    device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
    if not device:
        return Response(
            {'error': 'TOTP faollashtirilmagan'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    totp = pyotp.TOTP(device.key)
    if not totp.verify(token, valid_window=1):
        return Response(
            {'error': 'Token noto\'g\'ri yoki muddati o\'tgan'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response({
        'message': '2FA verifikatsiya muvaffaqiyatli',
        'verified': True
    }, status=status.HTTP_200_OK)


# ==================== Backup Codes Views ====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_backup_codes(request):
    """
    Get all unused backup codes
    
    GET /api/v1/users/2fa/backup-codes/
    """
    user = request.user
    backup_codes = BackupCode.objects.filter(user=user, used=False)
    serializer = BackupCodeSerializer(backup_codes, many=True)
    
    return Response({
        'backup_codes': serializer.data,
        'count': backup_codes.count()
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def regenerate_backup_codes(request):
    """
    Regenerate backup codes
    
    POST /api/v1/users/2fa/backup-codes/regenerate/
    """
    user = request.user
    
    # Delete all old codes
    BackupCode.objects.filter(user=user).delete()
    
    # Generate new codes
    backup_codes = BackupCode.generate_codes_for_user(user)
    
    return Response({
        'message': 'Yangi backup kodlar yaratildi',
        'backup_codes': backup_codes,
        'warning': 'Eski kodlar endi ishlamaydi!'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_backup_code(request):
    """
    Verify a backup code
    
    POST /api/v1/users/2fa/backup-codes/verify/
    Body: {"code": "ABCD123456"}
    """
    serializer = BackupCodeVerifySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    code = serializer.validated_data['code']
    
    backup_code = BackupCode.objects.filter(user=user, code=code, used=False).first()
    
    if not backup_code:
        return Response({
            'error': 'Kod topilmadi yoki allaqachon ishlatilgan',
            'verified': False
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Mark as used
    backup_code.used = True
    backup_code.used_at = timezone.now()
    backup_code.save()
    
    # Count remaining codes
    remaining_codes = BackupCode.objects.filter(user=user, used=False).count()
    
    response_data = {
        'message': '2FA verifikatsiya muvaffaqiyatli',
        'verified': True,
        'remaining_backup_codes': remaining_codes
    }
    
    if remaining_codes <= 2:
        response_data['warning'] = f'Faqat {remaining_codes} ta kod qoldi. Yangisini yarating!'
    
    return Response(response_data, status=status.HTTP_200_OK)


# ==================== General 2FA Views ====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def two_factor_status(request):
    """
    Get 2FA status
    
    GET /api/v1/users/2fa/status/
    """
    user = request.user
    serializer = TwoFactorStatusSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disable_two_factor(request):
    """
    Disable 2FA
    
    POST /api/v1/users/2fa/disable/
    """
    user = request.user
    
    # Delete all 2FA data
    TOTPDevice.objects.filter(user=user).delete()
    BackupCode.objects.filter(user=user).delete()
    
    # Update user
    user.two_factor_enabled = False
    user.two_factor_method = 'none'
    user.save()
    
    return Response({
        'message': '2FA muvaffaqiyatli o\'chirildi'
    }, status=status.HTTP_200_OK)
```

---

## URLs

### users/urls.py

```python
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # TOTP URLs
    path('2fa/totp/setup/', views.setup_totp, name='totp-setup'),
    path('2fa/totp/verify-setup/', views.verify_totp_setup, name='totp-verify-setup'),
    path('2fa/totp/verify/', views.verify_totp_login, name='totp-verify-login'),
    
    # Backup Codes URLs
    path('2fa/backup-codes/', views.get_backup_codes, name='get-backup-codes'),
    path('2fa/backup-codes/regenerate/', views.regenerate_backup_codes, name='regenerate-backup-codes'),
    path('2fa/backup-codes/verify/', views.verify_backup_code, name='verify-backup-code'),
    
    # General 2FA URLs
    path('2fa/status/', views.two_factor_status, name='2fa-status'),
    path('2fa/disable/', views.disable_two_factor, name='disable-2fa'),
]
```

### library_project/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
]
```

---

## Postman Testlar

### Collection Setup

**Environment Variables:**
```
base_url: http://127.0.0.1:8000
token: (login'dan keyin avtomatik)
```

### Request 1: TOTP Setup

```
POST {{base_url}}/api/v1/users/2fa/totp/setup/
Headers:
  Authorization: Token {{token}}
```

**Response:**
```json
{
    "secret_key": "JBSWY3DPEHPK3PXP",
    "qr_code": "data:image/png;base64,...",
    "manual_entry_key": "JBSWY3DPEHPK3PXP",
    "message": "QR kodni Google Authenticator ilovasida skanerlang..."
}
```

### Request 2: TOTP Verify Setup

```
POST {{base_url}}/api/v1/users/2fa/totp/verify-setup/
Headers:
  Authorization: Token {{token}}
Body:
{
    "token": "123456"
}
```

**Response:**
```json
{
    "message": "TOTP muvaffaqiyatli faollashtirildi",
    "backup_codes": ["A1B2C3...", "D4E5F6...", ...],
    "warning": "Backup kodlarni xavfsiz joyda saqlang!"
}
```

### Request 3: 2FA Status

```
GET {{base_url}}/api/v1/users/2fa/status/
Headers:
  Authorization: Token {{token}}
```

**Response:**
```json
{
    "two_factor_enabled": true,
    "two_factor_method": "totp",
    "has_totp": true,
    "has_sms": false,
    "backup_codes_count": 10
}
```

### Request 4: TOTP Verify

```
POST {{base_url}}/api/v1/users/2fa/totp/verify/
Headers:
  Authorization: Token {{token}}
Body:
{
    "token": "654321"
}
```

**Response:**
```json
{
    "message": "2FA verifikatsiya muvaffaqiyatli",
    "verified": true
}
```

### Request 5: Get Backup Codes

```
GET {{base_url}}/api/v1/users/2fa/backup-codes/
Headers:
  Authorization: Token {{token}}
```

**Response:**
```json
{
    "backup_codes": [
        {
            "code": "A1B2C3D4E5",
            "used": false,
            "used_at": null,
            "created_at": "2025-01-02T10:30:00Z"
        },
        ...
    ],
    "count": 10
}
```

### Request 6: Verify Backup Code

```
POST {{base_url}}/api/v1/users/2fa/backup-codes/verify/
Headers:
  Authorization: Token {{token}}
Body:
{
    "code": "A1B2C3D4E5"
}
```

**Response:**
```json
{
    "message": "2FA verifikatsiya muvaffaqiyatli",
    "verified": true,
    "remaining_backup_codes": 9
}
```

### Request 7: Regenerate Backup Codes

```
POST {{base_url}}/api/v1/users/2fa/backup-codes/regenerate/
Headers:
  Authorization: Token {{token}}
```

**Response:**
```json
{
    "message": "Yangi backup kodlar yaratildi",
    "backup_codes": ["X1Y2Z3...", "A4B5C6...", ...],
    "warning": "Eski kodlar endi ishlamaydi!"
}
```

### Request 8: Disable 2FA

```
POST {{base_url}}/api/v1/users/2fa/disable/
Headers:
  Authorization: Token {{token}}
```

**Response:**
```json
{
    "message": "2FA muvaffaqiyatli o'chirildi"
}
```

---

## Best Practices

### 1. Security

✅ **DO:**
- Use `secrets` module for random generation
- Hash backup codes in production
- Implement rate limiting
- Log all 2FA events
- Use HTTPS in production

❌ **DON'T:**
- Use `random` module for security
- Store plaintext secrets
- Allow unlimited attempts
- Ignore failed login attempts

### 2. User Experience

✅ **DO:**
- Provide clear instructions
- Show QR code and manual entry
- Give 10 backup codes
- Warn when codes running out
- Allow 2FA disable

❌ **DON'T:**
- Force 2FA without warning
- Hide backup codes option
- Make setup too complicated

### 3. Code Quality

✅ **DO:**
- Use serializers for validation
- Handle all error cases
- Write clear docstrings
- Use proper HTTP status codes
- Follow DRF conventions

❌ **DON'T:**
- Skip validation
- Return generic errors
- Ignore edge cases

---

## Xulosa

### Nima o'rgandik?

✅ Two-Factor Authentication nima  
✅ TOTP (Google Authenticator) implementatsiya  
✅ QR code generatsiya  
✅ Backup codes tizimi  
✅ django-otp kutubxonasi  
✅ Security best practices  

### Keyingi Qadamlar

1. SMS verification qo'shish
2. Email 2FA qo'shish
3. Trusted devices
4. Rate limiting
5. Admin panel

### Foydali Resurslar

- [django-otp docs](https://django-otp-official.readthedocs.io/)
- [pyotp docs](https://pyauth.github.io/pyotp/)
- [TOTP RFC 6238](https://tools.ietf.org/html/rfc6238)
- [Google Authenticator](https://support.google.com/accounts/answer/1066447)

---

**Homework:** `homework.md` faylida topshiriqlar!

**Examples:** `examples/` papkasida amaliy misollar!

**Happy Coding!**