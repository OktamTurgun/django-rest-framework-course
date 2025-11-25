# examples/03-file-validation.py
"""
File Validation - Fayl validatsiyasi
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from PIL import Image
import os
import magic  # python-magic


# =============================================================================
# 1. Model Level Validators
# =============================================================================

def validate_file_size(value):
    """
    File hajmini tekshirish
    """
    filesize = value.size
    
    # 5 MB limit
    max_size_mb = 5
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if filesize > max_size_bytes:
        raise ValidationError(
            f'File size cannot exceed {max_size_mb}MB. '
            f'Current size: {filesize / (1024 * 1024):.2f}MB'
        )


def validate_image_size(value):
    """
    Image hajmini tekshirish - kichikroq limit
    """
    filesize = value.size
    
    # 2 MB limit for images
    max_size_mb = 2
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if filesize > max_size_bytes:
        raise ValidationError(
            f'Image size cannot exceed {max_size_mb}MB'
        )


def validate_image_dimensions(value):
    """
    Image o'lchamlarini tekshirish
    """
    try:
        img = Image.open(value)
        width, height = img.size
        
        # Minimum dimensions
        min_width, min_height = 100, 100
        if width < min_width or height < min_height:
            raise ValidationError(
                f'Image dimensions must be at least {min_width}x{min_height} pixels. '
                f'Current: {width}x{height}'
            )
        
        # Maximum dimensions
        max_width, max_height = 4096, 4096
        if width > max_width or height > max_height:
            raise ValidationError(
                f'Image dimensions cannot exceed {max_width}x{max_height} pixels. '
                f'Current: {width}x{height}'
            )
    except Exception as e:
        raise ValidationError(f'Invalid image file: {str(e)}')


def validate_image_format(value):
    """
    Image formatini tekshirish
    """
    try:
        img = Image.open(value)
        
        # Allowed formats
        allowed_formats = ['JPEG', 'PNG', 'GIF', 'WEBP']
        
        if img.format not in allowed_formats:
            raise ValidationError(
                f'Unsupported image format: {img.format}. '
                f'Allowed formats: {", ".join(allowed_formats)}'
            )
        
        # Verify image
        img.verify()
    except Exception as e:
        raise ValidationError(f'Invalid or corrupted image: {str(e)}')


# =============================================================================
# 2. Models with Validation
# =============================================================================

class Document(models.Model):
    """
    Document model - file type va hajm validation
    """
    title = models.CharField(max_length=200)
    file = models.FileField(
        upload_to='documents/',
        validators=[
            validate_file_size,
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'xls', 'xlsx']
            )
        ]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        """
        Model level validation
        """
        super().clean()
        
        if self.file:
            # File extension tekshirish
            ext = os.path.splitext(self.file.name)[1].lower()
            
            # Qora ro'yxat
            dangerous_extensions = ['.exe', '.bat', '.sh', '.cmd']
            if ext in dangerous_extensions:
                raise ValidationError({
                    'file': f'File extension {ext} is not allowed for security reasons'
                })


class ProfileImage(models.Model):
    """
    Profile image - to'liq image validation
    """
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='profiles/',
        validators=[
            validate_image_size,
            validate_image_dimensions,
            validate_image_format,
            FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'webp'])
        ]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)


# =============================================================================
# 3. MIME Type Validation (python-magic)
# =============================================================================

def validate_mime_type(value):
    """
    MIME type tekshirish - real file content
    """
    # File content dan MIME type aniqlash
    mime = magic.from_buffer(value.read(1024), mime=True)
    value.seek(0)  # Reset file pointer
    
    # Allowed MIME types
    allowed_mimes = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'image/jpeg',
        'image/png',
        'image/gif',
    ]
    
    if mime not in allowed_mimes:
        raise ValidationError(
            f'Unsupported file type: {mime}. '
            f'File extension might be misleading.'
        )


class SecureDocument(models.Model):
    """
    MIME type validation bilan
    """
    file = models.FileField(
        upload_to='secure_docs/',
        validators=[validate_file_size, validate_mime_type]
    )


# =============================================================================
# 4. Serializer Level Validation
# =============================================================================

class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer da validation
    """
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'uploaded_at']
        read_only_fields = ['uploaded_at']
    
    def validate_file(self, value):
        """
        File field validation
        """
        # File size
        max_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_size:
            raise serializers.ValidationError(
                f'File too large. Maximum size: 10MB. '
                f'Current: {value.size / (1024 * 1024):.2f}MB'
            )
        
        # File extension
        ext = os.path.splitext(value.name)[1].lower()
        allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']
        
        if ext not in allowed_extensions:
            raise serializers.ValidationError(
                f'File extension {ext} not allowed. '
                f'Allowed: {", ".join(allowed_extensions)}'
            )
        
        # File name length
        if len(value.name) > 100:
            raise serializers.ValidationError(
                'File name too long (max 100 characters)'
            )
        
        return value
    
    def validate(self, attrs):
        """
        Multiple fields validation
        """
        file = attrs.get('file')
        title = attrs.get('title', '')
        
        # Title and filename match check
        if file and title:
            file_basename = os.path.splitext(file.name)[0]
            if title.lower() != file_basename.lower():
                # Warning, not error
                pass
        
        return attrs


class ImageSerializer(serializers.Serializer):
    """
    Image upload serializer - strict validation
    """
    image = serializers.ImageField()
    
    def validate_image(self, value):
        """
        Image validation
        """
        # Size check
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError('Image too large (max 5MB)')
        
        # Dimension check
        try:
            img = Image.open(value)
            width, height = img.size
            
            # Min dimensions
            if width < 200 or height < 200:
                raise serializers.ValidationError(
                    f'Image too small. Minimum: 200x200. Current: {width}x{height}'
                )
            
            # Max dimensions
            if width > 4000 or height > 4000:
                raise serializers.ValidationError(
                    f'Image too large. Maximum: 4000x4000. Current: {width}x{height}'
                )
            
            # Format check
            if img.format not in ['JPEG', 'PNG']:
                raise serializers.ValidationError(
                    f'Only JPEG and PNG formats allowed. Current: {img.format}'
                )
            
        except Exception as e:
            raise serializers.ValidationError(f'Invalid image: {str(e)}')
        
        return value


# =============================================================================
# 5. View Level Validation
# =============================================================================

class FileUploadView(APIView):
    """
    View da validation
    """
    parser_classes = [MultiPartParser]
    
    def post(self, request):
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Manual validation
        errors = []
        
        # 1. File size
        max_size = 10 * 1024 * 1024  # 10MB
        if file_obj.size > max_size:
            errors.append(f'File too large: {file_obj.size / (1024 * 1024):.2f}MB (max 10MB)')
        
        # 2. File extension
        ext = os.path.splitext(file_obj.name)[1].lower()
        allowed = ['.pdf', '.doc', '.docx']
        if ext not in allowed:
            errors.append(f'File type not allowed: {ext}')
        
        # 3. File name
        if len(file_obj.name) > 100:
            errors.append('File name too long')
        
        # 4. Content check (if PDF)
        if ext == '.pdf':
            content = file_obj.read(1024)
            file_obj.seek(0)
            
            # PDF magic number check
            if not content.startswith(b'%PDF'):
                errors.append('Invalid PDF file')
        
        # Agar xatolar bo'lsa
        if errors:
            return Response(
                {'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save file
        document = Document.objects.create(
            title=file_obj.name,
            file=file_obj
        )
        
        serializer = DocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# =============================================================================
# 6. Custom Validator Classes
# =============================================================================

class FileValidator:
    """
    Reusable file validator
    """
    
    def __init__(self, max_size=None, allowed_extensions=None, allowed_mimes=None):
        self.max_size = max_size
        self.allowed_extensions = allowed_extensions or []
        self.allowed_mimes = allowed_mimes or []
    
    def __call__(self, value):
        # Size check
        if self.max_size and value.size > self.max_size:
            raise ValidationError(
                f'File size exceeds {self.max_size / (1024 * 1024):.1f}MB'
            )
        
        # Extension check
        if self.allowed_extensions:
            ext = os.path.splitext(value.name)[1].lower()
            if ext not in self.allowed_extensions:
                raise ValidationError(
                    f'File extension {ext} not allowed. '
                    f'Allowed: {", ".join(self.allowed_extensions)}'
                )
        
        # MIME type check
        if self.allowed_mimes:
            mime = magic.from_buffer(value.read(1024), mime=True)
            value.seek(0)
            
            if mime not in self.allowed_mimes:
                raise ValidationError(f'File type {mime} not allowed')


class ImageValidator:
    """
    Reusable image validator
    """
    
    def __init__(self, min_width=None, min_height=None, max_width=None, max_height=None):
        self.min_width = min_width
        self.min_height = min_height
        self.max_width = max_width
        self.max_height = max_height
    
    def __call__(self, value):
        try:
            img = Image.open(value)
            width, height = img.size
            
            # Min dimensions
            if self.min_width and width < self.min_width:
                raise ValidationError(f'Image width must be at least {self.min_width}px')
            
            if self.min_height and height < self.min_height:
                raise ValidationError(f'Image height must be at least {self.min_height}px')
            
            # Max dimensions
            if self.max_width and width > self.max_width:
                raise ValidationError(f'Image width cannot exceed {self.max_width}px')
            
            if self.max_height and height > self.max_height:
                raise ValidationError(f'Image height cannot exceed {self.max_height}px')
            
            # Verify
            img.verify()
            
        except Exception as e:
            raise ValidationError(f'Invalid image: {str(e)}')


# Usage
class ValidatedDocument(models.Model):
    file = models.FileField(
        upload_to='validated/',
        validators=[
            FileValidator(
                max_size=5 * 1024 * 1024,  # 5MB
                allowed_extensions=['.pdf', '.docx'],
                allowed_mimes=['application/pdf']
            )
        ]
    )


class ValidatedImage(models.Model):
    image = models.ImageField(
        upload_to='validated_images/',
        validators=[
            ImageValidator(
                min_width=200,
                min_height=200,
                max_width=2000,
                max_height=2000
            )
        ]
    )


# =============================================================================
# 7. Error Messages Customization
# =============================================================================

class CustomDocumentSerializer(serializers.ModelSerializer):
    """
    Custom error messages
    """
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'file']
    
    def validate_file(self, value):
        errors = {}
        
        # Size
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            errors['size'] = f'Fayl hajmi {max_size / (1024 * 1024):.0f}MB dan oshmasligi kerak'
        
        # Extension
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in ['.pdf', '.docx']:
            errors['extension'] = f'{ext} formatidagi fayllar qabul qilinmaydi'
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return value


# =============================================================================
# Requirements
# =============================================================================

REQUIREMENTS = """
# Validation uchun
Pillow==10.1.0
python-magic==0.4.27
python-magic-bin==0.4.14  # Windows uchun
"""