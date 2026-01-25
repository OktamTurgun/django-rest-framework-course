from django.shortcuts import render
"""
users/views.py - Two-Factor Authentication Views
"""

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

from .models import BackupCode, SMSVerification
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
    device = TOTPDevice.objects.create(
        user=user, 
        name='default', 
        confirmed=False
    )
    
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
    
    # Update user profile (if exists)
    if hasattr(user, 'profile'):
        user.profile.two_factor_enabled = True
        user.profile.two_factor_method = 'totp'
        user.profile.save()
    
    # Generate backup codes
    backup_codes = BackupCode.generate_codes_for_user(user)
    
    return Response({
        'message': 'TOTP muvaffaqiyatli faollashtirildi',
        'backup_codes': backup_codes,
        'warning': 'Backup kodlarni xavfsiz joyda saqlang! Har bir kod faqat 1 marta ishlatiladi.'
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
        'warning': 'Eski kodlar endi ishlamaydi! Yangi kodlarni xavfsiz joyda saqlang.'
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
    
    backup_code = BackupCode.objects.filter(
        user=user,
        code=code,
        used=False
    ).first()
    
    if not backup_code:
        return Response({
            'error': 'Kod topilmadi yoki allaqachon ishlatilgan',
            'verified': False
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Mark as used
    backup_code.mark_as_used()
    
    # Count remaining codes
    remaining_codes = BackupCode.objects.filter(user=user, used=False).count()
    
    response_data = {
        'message': '2FA verifikatsiya muvaffaqiyatli',
        'verified': True,
        'remaining_backup_codes': remaining_codes
    }
    
    if remaining_codes <= 2:
        response_data['warning'] = (
            f'Faqat {remaining_codes} ta backup kod qoldi. '
            'Yangisini yarating!'
        )
    
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
    
    has_totp = TOTPDevice.objects.filter(user=user, confirmed=True).exists()
    backup_count = BackupCode.objects.filter(user=user, used=False).count()
    
    # Get status from profile if exists
    if hasattr(user, 'profile'):
        two_factor_enabled = user.profile.two_factor_enabled
        two_factor_method = user.profile.two_factor_method
    else:
        two_factor_enabled = has_totp
        two_factor_method = 'totp' if has_totp else 'none'
    
    data = {
        'two_factor_enabled': two_factor_enabled,
        'two_factor_method': two_factor_method,
        'has_totp': has_totp,
        'has_sms': False,  # SMS not implemented yet
        'backup_codes_count': backup_count
    }
    
    serializer = TwoFactorStatusSerializer(data)
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
    SMSVerification.objects.filter(user=user).delete()
    
    # Update user profile
    if hasattr(user, 'profile'):
        user.profile.two_factor_enabled = False
        user.profile.two_factor_method = 'none'
        user.profile.save()
    
    return Response({
        'message': '2FA muvaffaqiyatli o\'chirildi'
    }, status=status.HTTP_200_OK)