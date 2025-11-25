# examples/05-advanced-upload.py
"""
Advanced File Upload - Signals, Cleanup, Progress, Chunked Upload
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.core.cache import cache
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import os
import hashlib
import uuid


# =============================================================================
# 1. File Cleanup with Signals
# =============================================================================

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


@receiver(pre_delete, sender=Document)
def delete_file_on_model_delete(sender, instance, **kwargs):
    """
    Model o'chirilganda faylni ham o'chirish
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(pre_save, sender=Document)
def delete_old_file_on_update(sender, instance, **kwargs):
    """
    Fayl yangilanganda eskisini o'chirish
    """
    if not instance.pk:
        return False
    
    try:
        old_file = sender.objects.get(pk=instance.pk).file
    except sender.DoesNotExist:
        return False
    
    new_file = instance.file
    
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


# =============================================================================
# 2. File Hash - Duplicate Detection
# =============================================================================

def calculate_file_hash(file_obj):
    """
    File MD5 hash ni hisoblash
    """
    hash_md5 = hashlib.md5()
    
    for chunk in file_obj.chunks():
        hash_md5.update(chunk)
    
    file_obj.seek(0)  # Reset file pointer
    return hash_md5.hexdigest()


class HashedDocument(models.Model):
    """
    File hash bilan duplicate detection
    """
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    file_hash = models.CharField(max_length=32, unique=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['file_hash']),
        ]


class HashedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashedDocument
        fields = ['id', 'title', 'file', 'file_hash', 'uploaded_at']
        read_only_fields = ['file_hash', 'uploaded_at']
    
    def create(self, validated_data):
        file_obj = validated_data['file']
        
        # Calculate hash
        file_hash = calculate_file_hash(file_obj)
        
        # Check if exists
        existing = HashedDocument.objects.filter(file_hash=file_hash).first()
        if existing:
            raise serializers.ValidationError(
                {'file': f'This file already exists (ID: {existing.id})'}
            )
        
        validated_data['file_hash'] = file_hash
        return super().create(validated_data)


# =============================================================================
# 3. Upload Progress Tracking
# =============================================================================

class UploadProgress(models.Model):
    """
    Upload progress tracking
    """
    upload_id = models.UUIDField(default=uuid.uuid4, unique=True)
    filename = models.CharField(max_length=255)
    total_size = models.BigIntegerField()
    uploaded_size = models.BigIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('uploading', 'Uploading'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def progress_percentage(self):
        if self.total_size > 0:
            return (self.uploaded_size / self.total_size) * 100
        return 0


from rest_framework.views import APIView

class InitiateUploadView(APIView):
    """
    Upload ni boshlash - progress tracking uchun
    """
    def post(self, request):
        filename = request.data.get('filename')
        filesize = request.data.get('filesize')
        
        if not filename or not filesize:
            return Response(
                {'error': 'filename and filesize required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create progress record
        progress = UploadProgress.objects.create(
            filename=filename,
            total_size=int(filesize),
            status='pending'
        )
        
        return Response({
            'upload_id': progress.upload_id,
            'message': 'Upload initiated'
        })


class UploadProgressView(APIView):
    """
    Upload progress ni ko'rish
    """
    def get(self, request, upload_id):
        try:
            progress = UploadProgress.objects.get(upload_id=upload_id)
        except UploadProgress.DoesNotExist:
            return Response(
                {'error': 'Upload not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'upload_id': progress.upload_id,
            'filename': progress.filename,
            'total_size': progress.total_size,
            'uploaded_size': progress.uploaded_size,
            'progress': progress.progress_percentage,
            'status': progress.status
        })


# =============================================================================
# 4. Chunked Upload (Katta fayllar uchun)
# =============================================================================

class ChunkedUpload(models.Model):
    """
    Chunked upload tracking
    """
    upload_id = models.UUIDField(default=uuid.uuid4, unique=True)
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='temp_uploads/', blank=True)
    total_size = models.BigIntegerField()
    uploaded_chunks = models.JSONField(default=list)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class ChunkedUploadView(APIView):
    """
    Chunk upload endpoint
    """
    parser_classes = [MultiPartParser]
    
    def post(self, request, upload_id):
        """
        Upload chunk
        """
        try:
            upload = ChunkedUpload.objects.get(upload_id=upload_id)
        except ChunkedUpload.DoesNotExist:
            return Response(
                {'error': 'Upload session not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        chunk = request.FILES.get('chunk')
        chunk_number = int(request.data.get('chunk_number'))
        
        if not chunk:
            return Response(
                {'error': 'No chunk provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save chunk
        chunk_path = f'temp_uploads/{upload_id}_{chunk_number}'
        
        with open(chunk_path, 'wb+') as destination:
            for chunk_data in chunk.chunks():
                destination.write(chunk_data)
        
        # Update tracking
        upload.uploaded_chunks.append(chunk_number)
        upload.save()
        
        return Response({
            'message': f'Chunk {chunk_number} uploaded',
            'uploaded_chunks': len(upload.uploaded_chunks)
        })
    
    def put(self, request, upload_id):
        """
        Complete upload - combine chunks
        """
        try:
            upload = ChunkedUpload.objects.get(upload_id=upload_id)
        except ChunkedUpload.DoesNotExist:
            return Response(
                {'error': 'Upload not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Combine chunks
        final_path = f'documents/{upload.filename}'
        
        with open(final_path, 'wb') as final_file:
            for chunk_num in sorted(upload.uploaded_chunks):
                chunk_path = f'temp_uploads/{upload_id}_{chunk_num}'
                
                with open(chunk_path, 'rb') as chunk_file:
                    final_file.write(chunk_file.read())
                
                # Delete chunk
                os.remove(chunk_path)
        
        # Update upload
        upload.completed = True
        upload.file = final_path
        upload.save()
        
        return Response({
            'message': 'Upload completed',
            'file_url': upload.file.url
        })


# =============================================================================
# 5. Background Processing with Celery
# =============================================================================

"""
# Install celery
pip install celery redis

# celery.py
from celery import Celery

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
"""

# tasks.py
"""
from celery import shared_task
from PIL import Image
import os

@shared_task
def process_uploaded_image(image_id):
    from .models import UploadedImage
    
    try:
        image_obj = UploadedImage.objects.get(id=image_id)
        
        # Open image
        img = Image.open(image_obj.image.path)
        
        # Create thumbnail
        img.thumbnail((300, 300))
        
        # Save thumbnail
        thumb_path = image_obj.image.path.replace('.jpg', '_thumb.jpg')
        img.save(thumb_path)
        
        # Update model
        image_obj.thumbnail_generated = True
        image_obj.save()
        
        return f'Processed image {image_id}'
    except Exception as e:
        return f'Error: {str(e)}'
"""


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    thumbnail_generated = models.BooleanField(default=False)
    processing_status = models.CharField(max_length=20, default='pending')


@receiver(post_save, sender=UploadedImage)
def process_image_async(sender, instance, created, **kwargs):
    """
    Rasm yuklangandan keyin background da process qilish
    """
    if created:
        # Celery task ni launch qilish
        # process_uploaded_image.delay(instance.id)
        pass


# =============================================================================
# 6. Virus Scanning
# =============================================================================

"""
# Install ClamAV (antivirus)
pip install clamd

# Ubuntu/Debian
sudo apt-get install clamav clamav-daemon

# Start daemon
sudo service clamav-daemon start
"""

import clamd

def scan_file_for_virus(file_path):
    """
    Faylni virus uchun scan qilish
    """
    try:
        cd = clamd.ClamdUnixSocket()
        
        # Scan file
        scan_result = cd.scan(file_path)
        
        if scan_result:
            # Virus topildi
            return False, scan_result
        
        # Clean
        return True, None
    except Exception as e:
        # ClamAV ishlamayotgan bo'lsa
        return True, f"Scanner error: {str(e)}"


class SecureDocument(models.Model):
    file = models.FileField(upload_to='secure/')
    scan_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('clean', 'Clean'),
            ('infected', 'Infected'),
        ],
        default='pending'
    )
    scan_result = models.TextField(blank=True)


@receiver(post_save, sender=SecureDocument)
def scan_uploaded_file(sender, instance, created, **kwargs):
    """
    Yuklangan faylni scan qilish
    """
    if created and instance.file:
        is_clean, result = scan_file_for_virus(instance.file.path)
        
        if is_clean:
            instance.scan_status = 'clean'
        else:
            instance.scan_status = 'infected'
            instance.scan_result = str(result)
            
            # Delete infected file
            os.remove(instance.file.path)
            instance.file = None
        
        instance.save()


# =============================================================================
# 7. File Metadata Extraction
# =============================================================================

import mimetypes
from datetime import datetime

class FileMetadata(models.Model):
    """
    File metadata
    """
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    mime_type = models.CharField(max_length=100)
    file_size = models.BigIntegerField()
    checksum = models.CharField(max_length=64)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


def extract_file_metadata(file_obj):
    """
    File metadata ni extract qilish
    """
    metadata = {}
    
    # MIME type
    mime_type, _ = mimetypes.guess_type(file_obj.name)
    metadata['mime_type'] = mime_type
    
    # Size
    metadata['file_size'] = file_obj.size
    
    # Checksum (SHA256)
    sha256_hash = hashlib.sha256()
    for chunk in file_obj.chunks():
        sha256_hash.update(chunk)
    metadata['checksum'] = sha256_hash.hexdigest()
    
    # Image dimensions
    if mime_type and mime_type.startswith('image/'):
        try:
            from PIL import Image
            img = Image.open(file_obj)
            metadata['width'] = img.width
            metadata['height'] = img.height
        except:
            pass
    
    file_obj.seek(0)
    return metadata


# =============================================================================
# 8. Complete Example with All Features
# =============================================================================

class AdvancedDocument(models.Model):
    """
    Barcha feature lar bilan
    """
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='advanced/')
    file_hash = models.CharField(max_length=64, unique=True)
    file_size = models.BigIntegerField()
    mime_type = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    scan_status = models.CharField(max_length=20, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class AdvancedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvancedDocument
        fields = '__all__'
        read_only_fields = ['file_hash', 'file_size', 'mime_type', 'scan_status']
    
    def create(self, validated_data):
        file_obj = validated_data['file']
        
        # Extract metadata
        metadata = extract_file_metadata(file_obj)
        validated_data['file_hash'] = metadata['checksum']
        validated_data['file_size'] = metadata['file_size']
        validated_data['mime_type'] = metadata['mime_type']
        
        return super().create(validated_data)


# =============================================================================
# URLs.py
# =============================================================================

URL_PATTERNS = """
from django.urls import path
from . import views

urlpatterns = [
    # Progress tracking
    path('upload/initiate/', views.InitiateUploadView.as_view()),
    path('upload/progress/<uuid:upload_id>/', views.UploadProgressView.as_view()),
    
    # Chunked upload
    path('upload/chunk/<uuid:upload_id>/', views.ChunkedUploadView.as_view()),
]
"""


# =============================================================================
# Requirements
# =============================================================================

REQUIREMENTS = """
# Advanced features
celery==5.3.4
redis==5.0.1
clamd==1.0.2  # Virus scanning
python-magic==0.4.27  # MIME type detection
"""