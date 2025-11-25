# 21-dars: File Upload

## Mavzu: DRF da fayl yuklash

### Darsning maqsadi
Ushbu darsda Django REST Framework da fayllar (rasm, PDF, dokument) yuklash va boshqarishni o'rganamiz.

## Nazariy qism

### File Upload nima?

File Upload - foydalanuvchilardan fayllarni qabul qilish va serverda saqlash jarayoni. DRF da bu:

**Asosiy tushunchalar:**
1.  **FileField** - har qanday fayl turi
2.  **ImageField** - faqat rasmlar (Pillow kerak)
3.  **Multipart/form-data** - fayl yuklash formati
4.  **Media files** - yuklangan fayllarni saqlash
5.  **Validation** - fayl hajmi, turi, formatini tekshirish

### Django da media files sozlash

**settings.py:**
```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Media files sozlamalari
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

**urls.py (Development):**
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your urls
]

# Development da media fayllarni serve qilish
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )
```

---

## Model da FileField

### 1. Oddiy FileField

```python
from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

**upload_to parametrlari:**
```python
# Statik papka
file = models.FileField(upload_to='documents/')
# Natija: media/documents/file.pdf

# Dinamik papka (yil/oy)
file = models.FileField(upload_to='documents/%Y/%m/')
# Natija: media/documents/2024/11/file.pdf

# Custom function
def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

file = models.FileField(upload_to=user_directory_path)
# Natija: media/user_5/file.pdf
```

### 2. ImageField

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"{self.user.username}'s profile"
```

**ImageField xususiyatlari:**
- Pillow kutubxonasi talab qilinadi
- Faqat rasm formatlarini qabul qiladi
- `.height` va `.width` propertylari bor

---

## Serializer da file fields

### 1. Basic FileField

```python
from rest_framework import serializers

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'uploaded_at']
        read_only_fields = ['uploaded_at']
```

### 2. Custom file representation

```python
class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'file_url', 'file_size']
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.file.url)
        return None
    
    def get_file_size(self, obj):
        if obj.file:
            return obj.file.size
        return None
```

### 3. ImageField serializer

```python
class ProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar', 'avatar_url']
    
    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.avatar.url)
        return None
```

---

## View da file upload

### 1. APIView bilan

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, format=None):
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # File ni saqlash
        document = Document.objects.create(
            title=file_obj.name,
            file=file_obj
        )
        
        serializer = DocumentSerializer(document, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

### 2. ViewSet bilan

```python
from rest_framework import viewsets

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
```

---

## File Validation

### 1. File hajmini cheklash

```python
from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize = value.size
    
    # 5 MB
    max_size_mb = 5
    if filesize > max_size_mb * 1024 * 1024:
        raise ValidationError(f'File size cannot exceed {max_size_mb}MB')

class Document(models.Model):
    file = models.FileField(
        upload_to='documents/',
        validators=[validate_file_size]
    )
```

### 2. File extension tekshirish

```python
import os

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx', '.txt']
    
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class Document(models.Model):
    file = models.FileField(
        upload_to='documents/',
        validators=[validate_file_size, validate_file_extension]
    )
```

### 3. Image format validation

```python
from PIL import Image

def validate_image(value):
    try:
        img = Image.open(value)
        img.verify()
    except:
        raise ValidationError('Invalid image file')
    
    # Min dimensions
    if img.width < 100 or img.height < 100:
        raise ValidationError('Image must be at least 100x100 pixels')
    
    # Max dimensions
    if img.width > 4096 or img.height > 4096:
        raise ValidationError('Image too large (max 4096x4096)')
```

### 4. Serializer level validation

```python
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file']
    
    def validate_file(self, value):
        # File size
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise serializers.ValidationError('File too large')
        
        # File type
        ext = os.path.splitext(value.name)[1]
        if ext not in ['.pdf', '.docx']:
            raise serializers.ValidationError('Invalid file type')
        
        return value
```

---

## Image Processing (Pillow)

### 1. O'rnatish

```bash
pip install Pillow
```

### 2. Image thumbnail yaratish

```python
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars/')
    avatar_thumbnail = models.ImageField(
        upload_to='avatars/thumbnails/',
        blank=True,
        null=True
    )
    
    def save(self, *args, **kwargs):
        if self.avatar:
            # Thumbnail yaratish
            img = Image.open(self.avatar)
            
            # Resize
            output_size = (150, 150)
            img.thumbnail(output_size)
            
            # Save to BytesIO
            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=85)
            
            # Create InMemoryUploadedFile
            thumb_file = InMemoryUploadedFile(
                thumb_io,
                None,
                f'{self.avatar.name.split(".")[0]}_thumb.jpg',
                'image/jpeg',
                thumb_io.tell(),
                None
            )
            
            self.avatar_thumbnail = thumb_file
        
        super().save(*args, **kwargs)
```

### 3. Image compress

```python
def compress_image(image_file, quality=85):
    img = Image.open(image_file)
    
    # RGB ga o'tkazish (JPEG uchun)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Siqish
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)
    
    return output
```

---

## Multiple files upload

### 1. Multiple FileField

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    image1 = models.ImageField(upload_to='posts/', blank=True)
    image2 = models.ImageField(upload_to='posts/', blank=True)
    image3 = models.ImageField(upload_to='posts/', blank=True)
```

### 2. Separate model (Tavsiya)

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

**Serializer:**
```python
class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image', 'uploaded_at']

class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'images', 'created_at']
```

**View:**
```python
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    @action(detail=True, methods=['post'])
    def upload_images(self, request, pk=None):
        post = self.get_object()
        images = request.FILES.getlist('images')
        
        for image in images:
            PostImage.objects.create(post=post, image=image)
        
        serializer = self.get_serializer(post)
        return Response(serializer.data)
```

---

## Best Practices

### 1. File naming

```python
import uuid
from django.utils.text import slugify

def upload_to_uuid(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return f'documents/{filename}'

class Document(models.Model):
    file = models.FileField(upload_to=upload_to_uuid)
```

### 2. Security

```python
# Content-Type tekshirish
def validate_file_mimetype(value):
    import magic
    
    mime = magic.from_buffer(value.read(1024), mime=True)
    value.seek(0)
    
    valid_mimes = ['application/pdf', 'image/jpeg', 'image/png']
    if mime not in valid_mimes:
        raise ValidationError('Invalid file type')
```

### 3. Cleanup old files

```python
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

@receiver(pre_delete, sender=Document)
def delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)

@receiver(pre_save, sender=Document)
def delete_old_file_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    
    try:
        old_file = sender.objects.get(pk=instance.pk).file
    except sender.DoesNotExist:
        return
    
    new_file = instance.file
    if old_file and old_file != new_file:
        old_file.delete(save=False)
```

### 4. Permissions

```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user == request.user

class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
```

---

## Production: Cloud Storage

### AWS S3

```python
# Install
pip install django-storages boto3

# settings.py
INSTALLED_APPS = [
    'storages',
]

AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
AWS_S3_REGION_NAME = 'us-east-1'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

---

## Postman da test qilish

### File upload request

```
POST http://localhost:8000/api/documents/
Content-Type: multipart/form-data

Body (form-data):
- title: My Document
- file: [Select File]
```

**Headers:**
```
Authorization: Token your-token-here
```

---

## Xulosa

File upload DRF da:

**Afzalliklar:**
- Oson sozlanadi
- Django bilan yaxshi integratsiya
- Validation va security
- Cloud storage support

**E'tiborli bo'lish kerak:**
- File hajmini cheklash
- File type validation
- Security (malicious files)
- Storage optimization

## Keyingi dars
22-darsda **Caching** mavzusini o'rganamiz.

## Qo'shimcha resurslar
- [DRF Parsers](https://www.django-rest-framework.org/api-guide/parsers/)
- [Django File Uploads](https://docs.djangoproject.com/en/stable/topics/http/file-uploads/)
- [Pillow Documentation](https://pillow.readthedocs.io/)