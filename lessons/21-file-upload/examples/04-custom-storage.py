# examples/04-custom-storage.py
"""
Custom Storage - AWS S3 va boshqa cloud storage
"""

from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage
import os


# =============================================================================
# 1. AWS S3 Storage Setup
# =============================================================================

"""
# Install
pip install django-storages boto3

# settings.py

# AWS Credentials
AWS_ACCESS_KEY_ID = 'your-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
AWS_S3_REGION_NAME = 'us-east-1'  # yoki boshqa region

# S3 sozlamalari
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'media'

# Storage backend
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Optional: Static files ham S3 da
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# INSTALLED_APPS ga qo'shish
INSTALLED_APPS = [
    ...
    'storages',
]
"""


# =============================================================================
# 2. Custom S3 Storage Classes
# =============================================================================

class PublicMediaStorage(S3Boto3Storage):
    """
    Public media files uchun S3 storage
    """
    location = 'media/public'
    default_acl = 'public-read'
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    """
    Private media files uchun S3 storage
    """
    location = 'media/private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


class DocumentStorage(S3Boto3Storage):
    """
    Documents uchun alohida S3 storage
    """
    location = 'documents'
    default_acl = 'private'
    file_overwrite = False
    
    def get_available_name(self, name, max_length=None):
        """
        Fayl nomi unique bo'lishi
        """
        if self.exists(name):
            import uuid
            ext = os.path.splitext(name)[1]
            name = f'{uuid.uuid4()}{ext}'
        return super().get_available_name(name, max_length)


# =============================================================================
# 3. Models - Multiple Storage
# =============================================================================

class PublicDocument(models.Model):
    """
    Public document - S3 public storage
    """
    title = models.CharField(max_length=200)
    file = models.FileField(
        upload_to='documents/',
        storage=PublicMediaStorage()
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)


class PrivateDocument(models.Model):
    """
    Private document - S3 private storage
    """
    title = models.CharField(max_length=200)
    file = models.FileField(
        upload_to='private_docs/',
        storage=PrivateMediaStorage()
    )
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Document(models.Model):
    """
    Document - custom storage
    """
    title = models.CharField(max_length=200)
    file = models.FileField(storage=DocumentStorage())
    is_public = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)


# =============================================================================
# 4. Signed URLs (Private files uchun)
# =============================================================================

from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from botocore.exceptions import ClientError

@api_view(['GET'])
def download_private_document(request, pk):
    """
    Private document uchun signed URL
    """
    try:
        document = PrivateDocument.objects.get(pk=pk)
    except PrivateDocument.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)
    
    # Permission check
    if document.owner != request.user:
        return Response({'error': 'Permission denied'}, status=403)
    
    try:
        # Generate signed URL (15 minutes)
        url = document.file.storage.url(
            document.file.name,
            expire=900  # 15 minutes
        )
        
        return HttpResponseRedirect(url)
    except ClientError as e:
        return Response({'error': str(e)}, status=500)


# =============================================================================
# 5. Custom Local Storage
# =============================================================================

class CustomLocalStorage(FileSystemStorage):
    """
    Custom local storage - specific papka
    """
    
    def __init__(self, *args, **kwargs):
        kwargs['location'] = os.path.join(settings.MEDIA_ROOT, 'custom')
        kwargs['base_url'] = f"{settings.MEDIA_URL}custom/"
        super().__init__(*args, **kwargs)
    
    def get_available_name(self, name, max_length=None):
        """
        Agar fayl mavjud bo'lsa, unique nom berish
        """
        if self.exists(name):
            import uuid
            ext = os.path.splitext(name)[1]
            basename = os.path.splitext(name)[0]
            name = f'{basename}_{uuid.uuid4().hex[:8]}{ext}'
        
        return super().get_available_name(name, max_length)


class LocalDocument(models.Model):
    """
    Local storage bilan
    """
    file = models.FileField(storage=CustomLocalStorage())


# =============================================================================
# 6. Mixed Storage Strategy
# =============================================================================

class MixedStorageDocument(models.Model):
    """
    Development da local, production da S3
    """
    title = models.CharField(max_length=200)
    file = models.FileField(
        upload_to='documents/',
        # Storage settings.py dan olinadi
    )
    
    def get_storage(self):
        """
        Dynamic storage
        """
        if settings.DEBUG:
            return FileSystemStorage()
        else:
            return S3Boto3Storage()


# =============================================================================
# 7. Settings.py - Complete Example
# =============================================================================

SETTINGS_COMPLETE = """
# settings.py - Complete storage configuration

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Local Media Settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# AWS S3 Settings
USE_S3 = os.getenv('USE_S3', 'FALSE') == 'TRUE'

if USE_S3:
    # AWS Credentials (from environment)
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
    
    # S3 Settings
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_DEFAULT_ACL = 'public-read'
    AWS_LOCATION = 'media'
    
    # Use S3 for media files
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    # Update MEDIA_URL
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

# Installed Apps
INSTALLED_APPS = [
    ...
    'storages',
]
"""


# =============================================================================
# 8. .env file example
# =============================================================================

ENV_EXAMPLE = """
# .env

# Development
DEBUG=True
USE_S3=FALSE

# Production
# DEBUG=False
# USE_S3=TRUE
# AWS_ACCESS_KEY_ID=your-access-key-id
# AWS_SECRET_ACCESS_KEY=your-secret-access-key
# AWS_STORAGE_BUCKET_NAME=your-bucket-name
# AWS_S3_REGION_NAME=us-east-1
"""


# =============================================================================
# 9. Serializer - S3 URLs
# =============================================================================

from rest_framework import serializers

class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'file_url']
    
    def get_file_url(self, obj):
        """
        S3 yoki local URL
        """
        if obj.file:
            # S3 da full URL avtomatik
            if hasattr(settings, 'AWS_S3_CUSTOM_DOMAIN'):
                return obj.file.url
            
            # Local da request kerak
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            
            return obj.file.url
        return None


# =============================================================================
# 10. AWS S3 Bucket Configuration
# =============================================================================

AWS_BUCKET_POLICY = """
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::your-bucket-name/media/public/*"
        }
    ]
}
"""

AWS_CORS_CONFIGURATION = """
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "POST", "PUT"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": []
    }
]
"""


# =============================================================================
# 11. IAM User Permissions
# =============================================================================

IAM_POLICY = """
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name/*",
                "arn:aws:s3:::your-bucket-name"
            ]
        }
    ]
}
"""


# =============================================================================
# 12. Direct Upload to S3 (Presigned URL)
# =============================================================================

import boto3
from botocore.exceptions import ClientError
from rest_framework.views import APIView
from rest_framework.response import Response

class GeneratePresignedURLView(APIView):
    """
    Client dan to'g'ridan-to'g'ri S3 ga upload uchun presigned URL
    """
    
    def post(self, request):
        filename = request.data.get('filename')
        filetype = request.data.get('filetype')
        
        if not filename or not filetype:
            return Response(
                {'error': 'filename and filetype required'},
                status=400
            )
        
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        key = f'uploads/{filename}'
        
        try:
            presigned_post = s3_client.generate_presigned_post(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=key,
                Fields={'Content-Type': filetype},
                Conditions=[
                    {'Content-Type': filetype},
                    ['content-length-range', 0, 10485760]  # 10MB max
                ],
                ExpiresIn=3600  # 1 hour
            )
            
            return Response({
                'data': presigned_post,
                'url': f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{key}'
            })
            
        except ClientError as e:
            return Response({'error': str(e)}, status=500)


# =============================================================================
# 13. Cleanup - Delete old files from S3
# =============================================================================

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

@receiver(pre_delete, sender=Document)
def delete_file_from_s3(sender, instance, **kwargs):
    """
    Model o'chirilganda S3 dan ham o'chirish
    """
    if instance.file:
        instance.file.delete(save=False)


@receiver(pre_save, sender=Document)
def delete_old_file_from_s3(sender, instance, **kwargs):
    """
    Fayl yangilanganda eskisini o'chirish
    """
    if not instance.pk:
        return
    
    try:
        old_instance = sender.objects.get(pk=instance.pk)
        old_file = old_instance.file
    except sender.DoesNotExist:
        return
    
    new_file = instance.file
    
    if old_file and old_file != new_file:
        old_file.delete(save=False)


# =============================================================================
# Requirements
# =============================================================================

REQUIREMENTS = """
# AWS S3 uchun
django-storages==1.14.2
boto3==1.34.0

# Environment variables
python-decouple==3.8
# yoki
python-dotenv==1.0.0
"""


# =============================================================================
# Testing
# =============================================================================

TESTING_NOTES = """
# Local development
1. USE_S3=FALSE qilib testing
2. media/ papkaga fayllar yuklanadi

# S3 testing
1. AWS account yaratish
2. S3 bucket yaratish
3. IAM user yaratish va credentials olish
4. .env da credentials sozlash
5. USE_S3=TRUE qilish
6. Test qilish

# Postman
POST /api/documents/
Content-Type: multipart/form-data
Body:
  - title: Test Document
  - file: [Select File]

Response:
{
    "id": 1,
    "title": "Test Document",
    "file": "https://bucket-name.s3.amazonaws.com/media/documents/file.pdf",
    "file_url": "https://bucket-name.s3.amazonaws.com/media/documents/file.pdf"
}
"""