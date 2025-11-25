# 21-dars: File Upload - Uy ishi

## Maqsad
DRF da file upload tizimini amalda qo'llash va turli xil file handling texnikalarini o'rganish.

---

## Vazifa 1: Book Cover Upload - Basic (3 ball)

### Tavsif
Library API ga kitob muqovasi yuklash funksiyasini qo'shing.

### Talablar

**Model:**
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13)
    cover_image = models.ImageField(
        upload_to='book_covers/',
        blank=True,
        null=True
    )
    published_date = models.DateField()
```

**Endpoint lar:**
1. `POST /api/books/` - Kitob yaratish (cover bilan)
2. `PUT /api/books/{id}/` - Kitobni yangilash (cover o'zgartirish)
3. `GET /api/books/{id}/` - Kitob va cover URL ni ko'rish

**Validation:**
- Faqat JPG, PNG formatlar
- Max hajm: 2MB
- Min o'lcham: 200x300 pixels

### Baholash mezoni
- ✅ Model to'g'ri yaratilgan (0.5 ball)
- ✅ Serializer to'g'ri ishlaydi (1 ball)
- ✅ Upload endpoint ishlaydi (1 ball)
- ✅ Validation qo'shilgan (0.5 ball)

---

## Vazifa 2: User Profile with Avatar (4 ball)

### Tavsif
User profile tizimini yarating va avatar yuklash qo'shing.

### Talablar

**Model:**
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )
    avatar_thumbnail = models.ImageField(
        upload_to='avatars/thumbnails/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
```

**Endpoint lar:**
1. `GET /api/profile/` - O'z profilini ko'rish
2. `PUT /api/profile/` - Profilni yangilash
3. `POST /api/profile/avatar/` - Avatar yuklash
4. `DELETE /api/profile/avatar/` - Avatar ni o'chirish

**Xususiyatlar:**
- Avatar yuklanganda avtomatik thumbnail yaratish (150x150)
- Eski avatar o'chirilishi kerak (yangi yuklanganda)
- Avatar URL va thumbnail URL qaytarish

### Baholash mezoni
- ✅ Model va migrations to'g'ri (0.5 ball)
- ✅ Thumbnail avtomatik yaratiladi (1.5 ball)
- ✅ CRUD endpoints ishlaydi (1.5 ball)
- ✅ Eski fayllar tozalanadi (0.5 ball)

---

## Vazifa 3: Multiple Images Upload - Gallery (4 ball)

### Tavsif
Book uchun gallery yarating - bir nechta rasm yuklash imkoniyati.

### Talablar

**Models:**
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    # ... other fields

class BookImage(models.Model):
    book = models.ForeignKey(Book, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='book_gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'uploaded_at']
```

**Endpoint lar:**
1. `POST /api/books/{id}/images/` - Bir nechta rasm yuklash
2. `GET /api/books/{id}/images/` - Barcha rasmlarni ko'rish
3. `DELETE /api/books/{id}/images/{image_id}/` - Rasmni o'chirish
4. `PATCH /api/books/{id}/images/{image_id}/` - Caption va order o'zgartirish

**Xususiyatlar:**
- Bir requestda ko'p rasm yuklash (max 5 ta)
- Har bir rasm uchun caption
- Rasmlarni tartib bo'yicha ordering

### Baholash mezoni
- ✅ Models va relationships to'g'ri (1 ball)
- ✅ Multiple upload ishlaydi (1.5 ball)
- ✅ CRUD operations to'g'ri (1 ball)
- ✅ Ordering ishlaydi (0.5 ball)

---

## Vazifa 4: Document Management System (5 ball)

### Tavsif
Turli xil dokument yuklash va boshqarish tizimi.

### Talablar

**Models:**
```python
class DocumentCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('pdf', 'PDF'),
        ('doc', 'Word Document'),
        ('xls', 'Excel Spreadsheet'),
        ('txt', 'Text File'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    category = models.ForeignKey(DocumentCategory, on_delete=models.SET_NULL, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file_size = models.BigIntegerField()  # bytes
    downloads_count = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

**Endpoint lar:**
1. `POST /api/documents/` - Dokument yuklash
2. `GET /api/documents/` - Barcha dokumentlar (filter, search)
3. `GET /api/documents/{id}/download/` - Yuklab olish (counter++)
4. `DELETE /api/documents/{id}/` - O'chirish (faqat owner)

**Validation:**
- File type bo'yicha extension tekshirish
- Max hajm: 10MB
- File_size avtomatik saqlanishi
- Faqat owner o'chira oladi

**Qo'shimcha:**
- Filter by category
- Search by title
- Order by downloads_count, uploaded_at

### Baholash mezoni
- ✅ Models va validation to'g'ri (1 ball)
- ✅ Upload va download ishlaydi (1.5 ball)
- ✅ Permissions to'g'ri (1 ball)
- ✅ Filtering va search (1 ball)
- ✅ Downloads counter (0.5 ball)

---

## Vazifa 5: Advanced - Video Upload with Processing (4 ball)

### Tavsif
Video yuklash va metadata extraction.

### Talablar

**Model:**
```python
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True)
    
    # Video metadata
    duration = models.DurationField(null=True, blank=True)
    resolution = models.CharField(max_length=20, blank=True)  # 1920x1080
    file_size = models.BigIntegerField()
    format = models.CharField(max_length=10, blank=True)  # mp4, avi, etc
    
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    views_count = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

**Endpoint lar:**
1. `POST /api/videos/` - Video yuklash
2. `GET /api/videos/` - Barcha videolar
3. `GET /api/videos/{id}/` - Video metadata
4. `GET /api/videos/{id}/stream/` - Video stream (views_count++)

**Xususiyatlar:**
- Video yuklanganda metadata extraction
- Avtomatik thumbnail generation (birinchi frame)
- File validation (faqat video formatlar)
- Max hajm: 100MB

**Kutubxonalar:**
```python
# Install qilish kerak
pip install opencv-python
pip install moviepy  # yoki ffmpeg-python
```

### Baholash mezoni
- ✅ Model va migrations (0.5 ball)
- ✅ Video upload ishlaydi (1 ball)
- ✅ Metadata extraction (1.5 ball)
- ✅ Thumbnail generation (1 ball)

---

## Bonus Vazifa: Cloud Storage Integration (2 ball)

### Tavsif
AWS S3 yoki boshqa cloud storage bilan integratsiya.

### Talablar

**AWS S3 Setup:**
```python
# Install
pip install django-storages boto3

# settings.py
AWS_ACCESS_KEY_ID = 'your-key'
AWS_SECRET_ACCESS_KEY = 'your-secret'
AWS_STORAGE_BUCKET_NAME = 'your-bucket'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

**Test:**
- File S3 ga yuklanishi
- URL S3 dan kelishi
- Download S3 dan ishlashi

### Baholash mezoni
- ✅ S3 sozlangan (1 ball)
- ✅ Upload/Download S3 orqali ishlaydi (1 ball)

---

## Topshirish

### Format
```
homework-21-file-upload/
├── book_covers/           # Vazifa 1
├── user_profiles/         # Vazifa 2
├── book_gallery/          # Vazifa 3
├── document_system/       # Vazifa 4
├── video_upload/          # Vazifa 5
├── README.md              # Har birida
└── requirements.txt
```

### README.md
Har bir vazifada:
- Setup instructions
- API endpoints list
- Postman collection (export)
- Screenshots

### Postman Collection
Har bir vazifa uchun:
- Upload requests
- GET requests
- DELETE requests
- Examples with actual files

### Deadline
**4 kun ichida**

---

## Baholash tizimi

| Vazifa | Ball | Tavsif |
|--------|------|--------|
| Vazifa 1 | 3 | Book cover upload |
| Vazifa 2 | 4 | User avatar + thumbnail |
| Vazifa 3 | 4 | Multiple images gallery |
| Vazifa 4 | 5 | Document management |
| Vazifa 5 | 4 | Video upload + processing |
| **Jami** | **20** | |
| Bonus | 2 | Cloud storage |
| **Maksimal** | **22** | |

### Baholash mezonlari

**18-22 ball:** ⭐⭐⭐⭐⭐ A'lo - File upload ustasi!
- Barcha vazifalar to'liq
- Validation va security
- Clean code
- Cloud storage

**14-17 ball:** ⭐⭐⭐⭐ Yaxshi - Ajoyib!
- Ko'p vazifalar bajarilgan
- Asosiy funksiyalar ishlaydi
- Yaxshi kod

**10-13 ball:** ⭐⭐⭐ O'rtacha - Yaxshi urinish
- Ba'zi vazifalar bajarilgan
- Asosiy tushunchalar bor
- Qo'shimcha ishlash kerak

**0-9 ball:** ⭐⭐ Qayta ishlash kerak
- Ko'p vazifalar bajarilmagan
- Mavzuni qayta o'rganish kerak

---

## Foydali maslahatlar

### 1. File Validation
```python
def validate_image_size(image):
    if image.size > 5 * 1024 * 1024:  # 5MB
        raise ValidationError('Image too large')
```

### 2. Thumbnail yaratish
```python
from PIL import Image
from io import BytesIO

img = Image.open(file)
img.thumbnail((150, 150))
thumb_io = BytesIO()
img.save(thumb_io, format='JPEG')
```

### 3. Postman da file yuklash
```
POST /api/upload/
Content-Type: multipart/form-data
Body (form-data):
  - file: [Select File]
  - title: My File
```

### 4. Eski fayllarni o'chirish
```python
@receiver(pre_save, sender=Profile)
def delete_old_avatar(sender, instance, **kwargs):
    if instance.pk:
        old = Profile.objects.get(pk=instance.pk)
        if old.avatar != instance.avatar:
            old.avatar.delete(save=False)
```

---

## Qo'shimcha resurslar

- [DRF File Upload Guide](https://www.django-rest-framework.org/api-guide/parsers/)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Django Storages](https://django-storages.readthedocs.io/)
- [AWS S3 Setup](https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html)

**Omad yor bo'lsin!**