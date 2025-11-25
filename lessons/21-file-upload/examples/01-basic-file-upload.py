# examples/01-basic-file-upload.py
"""
Basic File Upload - Oddiy fayl yuklash
"""

from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action


# =============================================================================
# 1. Model - FileField
# =============================================================================

class Document(models.Model):
    """
    Oddiy dokument modeli
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title


# =============================================================================
# 2. Serializer - Basic
# =============================================================================

class DocumentSerializer(serializers.ModelSerializer):
    """
    Oddiy document serializer
    """
    uploaded_by_username = serializers.CharField(
        source='uploaded_by.username',
        read_only=True
    )
    file_url = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id',
            'title',
            'description',
            'file',
            'file_url',
            'file_name',
            'uploaded_by',
            'uploaded_by_username',
            'uploaded_at'
        ]
        read_only_fields = ['uploaded_by', 'uploaded_at']
    
    def get_file_url(self, obj):
        """Full URL qaytarish"""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    
    def get_file_name(self, obj):
        """Fayl nomini qaytarish"""
        if obj.file:
            return obj.file.name.split('/')[-1]
        return None


# =============================================================================
# 3. APIView - Manual file handling
# =============================================================================

class FileUploadAPIView(APIView):
    """
    APIView bilan file upload
    """
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, format=None):
        """
        File yuklash
        
        Request:
            title: str
            description: str (optional)
            file: file
        """
        # File olish
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Title olish
        title = request.data.get('title', file_obj.name)
        description = request.data.get('description', '')
        
        # Saqlash
        document = Document.objects.create(
            title=title,
            description=description,
            file=file_obj,
            uploaded_by=request.user
        )
        
        # Serialize qilish
        serializer = DocumentSerializer(document, context={'request': request})
        
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


# =============================================================================
# 4. ViewSet - CRUD operations
# =============================================================================

class DocumentViewSet(viewsets.ModelViewSet):
    """
    Document ViewSet - to'liq CRUD
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def perform_create(self, serializer):
        """
        Document yaratishda uploaded_by ni avtomatik qo'shish
        """
        serializer.save(uploaded_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """
        Custom create - file validation
        """
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response(
                {'error': 'File is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # File size check (5MB)
        max_size = 5 * 1024 * 1024
        if file_obj.size > max_size:
            return Response(
                {'error': f'File size cannot exceed 5MB'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().create(request, *args, **kwargs)


# =============================================================================
# 5. Custom upload_to function
# =============================================================================

def user_directory_path(instance, filename):
    """
    Faylni user papkasiga saqlash
    Natija: user_5/documents/myfile.pdf
    """
    return f'user_{instance.uploaded_by.id}/documents/{filename}'


class UserDocument(models.Model):
    """
    User-specific document papkasi bilan
    """
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to=user_directory_path)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)


# =============================================================================
# 6. Date-based upload_to
# =============================================================================

class TimeStampedDocument(models.Model):
    """
    Yil/Oy bo'yicha papkalarga saqlash
    Natija: documents/2024/11/myfile.pdf
    """
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


# =============================================================================
# 7. Multiple file handling
# =============================================================================

class BulkFileUploadAPIView(APIView):
    """
    Bir nechta fayl yuklash
    """
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        """
        Ko'p fayllarni yuklash
        
        Request:
            files: [file1, file2, file3, ...]
        """
        files = request.FILES.getlist('files')
        
        if not files:
            return Response(
                {'error': 'No files provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_documents = []
        
        for file_obj in files:
            document = Document.objects.create(
                title=file_obj.name,
                file=file_obj,
                uploaded_by=request.user
            )
            created_documents.append(document)
        
        serializer = DocumentSerializer(
            created_documents,
            many=True,
            context={'request': request}
        )
        
        return Response(
            {
                'count': len(created_documents),
                'documents': serializer.data
            },
            status=status.HTTP_201_CREATED
        )


# =============================================================================
# 8. File download
# =============================================================================

from django.http import FileResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def download_document(request, pk):
    """
    Faylni yuklab olish
    """
    try:
        document = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return Response(
            {'error': 'Document not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Fayl mavjudligini tekshirish
    if not document.file:
        return Response(
            {'error': 'File not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # FileResponse
    response = FileResponse(
        document.file.open('rb'),
        content_type='application/octet-stream'
    )
    response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
    
    return response


# =============================================================================
# Settings.py da kerakli sozlamalar
# =============================================================================

SETTINGS_EXAMPLE = """
# settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Media files sozlamalari
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Maximum file upload size (default: 2.5MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
"""


# =============================================================================
# URLs.py
# =============================================================================

URL_PATTERNS = """
# urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FileUploadAPIView,
    DocumentViewSet,
    BulkFileUploadAPIView,
    download_document
)

router = DefaultRouter()
router.register('documents', DocumentViewSet, basename='document')

urlpatterns = [
    # APIView
    path('upload/', FileUploadAPIView.as_view(), name='file-upload'),
    path('bulk-upload/', BulkFileUploadAPIView.as_view(), name='bulk-upload'),
    path('download/<int:pk>/', download_document, name='download-document'),
    
    # ViewSet
    path('', include(router.urls)),
]

# Development da media serve qilish
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""


# =============================================================================
# Postman da test qilish
# =============================================================================

POSTMAN_TEST = """
# 1. Single file upload
POST http://localhost:8000/api/upload/
Content-Type: multipart/form-data

Body (form-data):
- title: My Document
- description: Test document
- file: [Select File]

Headers:
- Authorization: Token your-token


# 2. ViewSet - Create
POST http://localhost:8000/api/documents/
Content-Type: multipart/form-data

Body (form-data):
- title: Document Title
- description: Description
- file: [Select File]


# 3. Bulk upload
POST http://localhost:8000/api/bulk-upload/
Content-Type: multipart/form-data

Body (form-data):
- files: [Select File 1]
- files: [Select File 2]
- files: [Select File 3]


# 4. List documents
GET http://localhost:8000/api/documents/


# 5. Download
GET http://localhost:8000/api/download/1/
"""