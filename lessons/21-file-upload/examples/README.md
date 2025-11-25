# File Upload Examples - Ko'rsatmalar

Bu papkada DRF File Upload ga oid amaliy misollar joylashgan.

## Fayllar tuzilmasi

### 1. `01-basic-file-upload.py`
**Mavzu:** Oddiy file upload asoslari

**O'rganiladi:**
- FileField va document model
- Serializer bilan file handling
- APIView va ViewSet
- Multiple file upload
- File download endpoint
- Media files sozlash

**Asosiy misollar:**
```python
# Model
class Document(models.Model):
    file = models.FileField(upload_to='documents/')

# Upload
file_obj = request.FILES.get('file')
document = Document.objects.create(file=file_obj)

# Download
response = FileResponse(document.file.open('rb'))
```

---

### 2. `02-image-upload.py`
**Mavzu:** Image upload va Pillow

**O'rganiladi:**
- ImageField
- Thumbnail yaratish
- Image optimization
- Image compression
- Avatar upload
- Book cover upload
- Image processing utilities

**Asosiy misollar:**
```python
# Thumbnail
img = Image.open(image)
img.thumbnail((150, 150))

# Optimize
img.save(output, format='JPEG', quality=85, optimize=True)

# Crop to square
img = img.crop((left, top, right, bottom))
```

---

### 3. `03-file-validation.py`
**Mavzu:** File validation

**O'rganiladi:**
- File size validation
- Extension validation
- Image dimensions validation
- MIME type validation
- Model level validators
- Serializer level validation
- Custom validator classes

**Asosiy misollar:**
```python
# Size validator
def validate_file_size(value):
    max_size = 5 * 1024 * 1024  # 5MB
    if value.size > max_size:
        raise ValidationError('File too large')

# Extension validator
FileExtensionValidator(['pdf', 'docx'])

# MIME type
mime = magic.from_buffer(value.read(1024), mime=True)
```

---

### 4. `04-custom-storage.py`
**Mavzu:** Custom storage va AWS S3

**O'rganiladi:**
- AWS S3 integration
- django-storages
- Public va Private storage
- Signed URLs
- Custom local storage
- Mixed storage strategy
- S3 bucket configuration

**Asosiy misollar:**
```python
# S3 Storage
class PublicMediaStorage(S3Boto3Storage):
    location = 'media/public'
    default_acl = 'public-read'

# Model
file = models.FileField(storage=PublicMediaStorage())

# Settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

---

### 5. `05-advanced-upload.py`
**Mavzu:** Advanced features

**O'rganiladi:**
- File cleanup with signals
- Duplicate detection (hash)
- Upload progress tracking
- Chunked upload
- Background processing (Celery)
- Virus scanning (ClamAV)
- Metadata extraction

**Asosiy misollar:**
```python
# Cleanup signal
@receiver(pre_delete, sender=Document)
def delete_file(sender, instance, **kwargs):
    instance.file.delete(save=False)

# Hash
file_hash = hashlib.md5()
for chunk in file_obj.chunks():
    file_hash.update(chunk)

# Chunked upload
upload = ChunkedUpload.objects.create(...)
```

---

## Fayllarni ishlatish

### 1. Loyihangizga nusxalash
```bash
# Kerakli faylni nusxalash
cp examples/01-basic-file-upload.py myproject/myapp/file_handling.py
```

### 2. Settings.py sozlash
```python
# settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# File upload limits
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
```

### 3. URLs.py da media serve qilish
```python
# urls.py

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your urls
]

# Development da media files
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
```

### 4. Requirements
```bash
# Basic
pip install Pillow

# AWS S3
pip install django-storages boto3

# Advanced
pip install celery redis clamd python-magic
```

---

## Test qilish

### Postman da file upload

**1. Single file upload:**
```
POST http://localhost:8000/api/upload/
Content-Type: multipart/form-data

Body (form-data):
- title: My Document
- file: [Select File]
```

**2. Image upload:**
```
POST http://localhost:8000/api/profile/avatar/
Content-Type: multipart/form-data
Authorization: Token YOUR_TOKEN

Body (form-data):
- avatar: [Select Image]
```

**3. Multiple files:**
```
POST http://localhost:8000/api/bulk-upload/
Content-Type: multipart/form-data

Body (form-data):
- files: [File 1]
- files: [File 2]
- files: [File 3]
```

---

## Postman Collection

```json
{
  "name": "File Upload Tests",
  "requests": [
    {
      "name": "Upload Document",
      "method": "POST",
      "url": "{{base_url}}/api/documents/",
      "body": {
        "mode": "formdata",
        "formdata": [
          {
            "key": "title",
            "value": "Test Document",
            "type": "text"
          },
          {
            "key": "file",
            "type": "file",
            "src": "/path/to/file.pdf"
          }
        ]
      }
    }
  ]
}
```

---

## Best Practices

### 1. File naming
```python
import uuid

def upload_to_uuid(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return f'documents/{filename}'
```

### 2. Validation
```python
# Size
if file.size > 5 * 1024 * 1024:
    raise ValidationError('File too large')

# Extension
allowed = ['.pdf', '.docx']
if ext not in allowed:
    raise ValidationError('Invalid file type')
```

### 3. Cleanup
```python
@receiver(pre_delete, sender=Document)
def delete_file(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)
```

### 4. Security
```python
# MIME type check
import magic
mime = magic.from_buffer(file.read(1024), mime=True)

# Dangerous extensions
dangerous = ['.exe', '.bat', '.sh']
if ext in dangerous:
    raise ValidationError('Forbidden file type')
```

---

## Common Issues

### Issue 1: Media files 404
```python
# settings.py tekshiring
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# urls.py da static() qo'shilganini tekshiring
```

### Issue 2: File too large
```python
# settings.py
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
```

### Issue 3: PIL/Pillow error
```bash
# Pillow o'rnatish
pip install Pillow

# Agar xato bo'lsa, uninstall va reinstall
pip uninstall Pillow
pip install Pillow
```

### Issue 4: S3 permission denied
```python
# IAM policy tekshiring
# Bucket policy tekshiring
# CORS configuration tekshiring
```

---

## Savol-javoblar

### Q: FileField va ImageField farqi nima?
**A:** 
- FileField - har qanday fayl
- ImageField - faqat rasmlar, Pillow kerak, .height va .width bor

### Q: Production da qayerga fayl saqlash kerak?
**A:** AWS S3, Google Cloud Storage, yoki Azure Blob Storage tavsiya etiladi.

### Q: Katta fayllar uchun nima qilish kerak?
**A:** Chunked upload yoki presigned URL ishlatish kerak.

### Q: Fayllarni qanday optimize qilish kerak?
**A:** 
- Image lar uchun: thumbnail, compression, format conversion
- Pillow ishlatish
- Background processing (Celery)

---

## Qo'shimcha resurslar

-  [Django File Uploads](https://docs.djangoproject.com/en/stable/topics/http/file-uploads/)
-  [DRF Parsers](https://www.django-rest-framework.org/api-guide/parsers/)
-  [Pillow Documentation](https://pillow.readthedocs.io/)
-  [Django Storages](https://django-storages.readthedocs.io/)
-  [AWS S3 Tutorial](https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html)

---

**Muvaffaqiyatlar!**