from io import BytesIO
from django.core.cache import cache
import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

class Author(models.Model):
    """Muallif modeli"""
    name = models.CharField(max_length=100)
    bio = models.TextField()
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "authors"
        ordering = ["name"]
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name
    

class Genre(models.Model):
    """Janr modeli"""
    name = models.CharField(max_length= 50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "genres"
        ordering = ["name"]
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name

# ==================== YANGILANGAN MODEL ====================

"""
Book model - FINAL FIXED VERSION
Publisher field'i o'chirilgan, faqat Author va Genre bilan ishlaydi
"""

class Book(models.Model):
    """
    Book model with optimizations
    """
    
    # Basic fields
    title = models.CharField(
        max_length=200,
        db_index=True
    )
    isbn_number = models.CharField(
        max_length=13,
        unique=True,
        db_index=True
    )
    description = models.TextField(blank=True, null=True)
    pages = models.IntegerField(default=0)
    language = models.CharField(max_length=50, default='English')
    
    # Price and stock
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_index=True
    )
    stock = models.IntegerField(default=0)
    
    # Dates
    published_date = models.DateField(
        blank=True,
        null=True,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Foreign Keys
    author = models.ForeignKey(
        'Author',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='books',
        db_index=True
    )
    
    # Many-to-Many
    genres = models.ManyToManyField(
        'Genre',
        related_name='books',
        blank=True
    )
    
    class Meta:
        ordering = ['-created_at']
        
        # Composite indexes
        indexes = [
            models.Index(fields=['title', 'author'], name='book_title_author_idx'),
            models.Index(fields=['isbn_number', 'title'], name='book_isbn_title_idx'),
            models.Index(fields=['published_date', 'author'], name='book_pub_author_idx'),
            models.Index(fields=['-created_at', 'title'], name='book_created_title_idx'),
            models.Index(fields=['price', 'title'], name='book_price_title_idx'),
        ]
        
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
    
    def __str__(self):
        return self.title
    
    # ==========================================
    # CACHED CLASS METHODS
    # ==========================================
    
    @classmethod
    def get_cached(cls, book_id):
        """Bitta kitobni cache bilan olish"""
        cache_key = f'book:optimized:{book_id}'
        book = cache.get(cache_key)
        
        if book is None:
            book = cls.objects.select_related('author').prefetch_related('genres').get(id=book_id)
            cache.set(cache_key, book, timeout=300)
        
        return book
    
    @classmethod
    def get_all_cached(cls):
        """Barcha kitoblarni cache bilan olish"""
        cache_key = 'books:all:optimized'
        books = cache.get(cache_key)
        
        if books is None:
            books = list(cls.objects.select_related('author').prefetch_related('genres').all())
            cache.set(cache_key, books, timeout=600)
        
        return books
    
    @classmethod
    def get_by_author_cached(cls, author_id):
        """Muallif bo'yicha kitoblarni cache bilan olish"""
        cache_key = f'books:author:optimized:{author_id}'
        books = cache.get(cache_key)
        
        if books is None:
            books = list(
                cls.objects.filter(author_id=author_id)
                .select_related('author')
                .prefetch_related('genres')
            )
            cache.set(cache_key, books, timeout=300)
        
        return books


# ==========================================
# SIGNAL HANDLERS
# ==========================================

@receiver(post_save, sender=Book)
def invalidate_book_cache_on_save(sender, instance, created, **kwargs):
    """Book save qilinganda cache'ni tozalash"""
    cache.delete(f'book:optimized:{instance.id}')
    cache.delete('books:all:optimized')
    
    if hasattr(instance, 'author') and instance.author:
        cache.delete(f'books:author:optimized:{instance.author.id}')
    
    try:
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection("default")
        
        patterns = [
            'books:list:optimized:*',
            'books:page:optimized:*',
            'books:statistics:optimized',
            'books:search:optimized:*'
        ]
        
        for pattern in patterns:
            keys = redis_conn.keys(pattern)
            if keys:
                redis_conn.delete(*keys)
    except:
        pass


@receiver(post_delete, sender=Book)
def invalidate_book_cache_on_delete(sender, instance, **kwargs):
    """Book delete qilinganda cache'ni tozalash"""
    cache.delete(f'book:optimized:{instance.id}')
    cache.delete('books:all:optimized')
    
    if hasattr(instance, 'author') and instance.author:
        cache.delete(f'books:author:optimized:{instance.author.id}')
    
    try:
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection("default")
        
        patterns = ['books:list:optimized:*', 'books:page:optimized:*']
        for pattern in patterns:
            keys = redis_conn.keys(pattern)
            if keys:
                redis_conn.delete(*keys)
    except:
        pass

# ==================== YANGI MODEL 20-Throttling ====================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='books_profile')
    bio = models.TextField(blank=True)
    is_premium = models.BooleanField(default=False)
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
    membership_type = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('basic', 'Basic'),
            ('premium', 'Premium')
        ],
        default='free'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.membership_type}"
    
    def save(self, *args, **kwargs):
        """
        Avatar yuklanganda thumbnail yaratish
        """
        if self.avatar and not self.avatar_thumbnail:
            # Thumbnail yaratish (Book.make_thumbnail dan nusxalash)
            self.avatar_thumbnail = self.make_thumbnail(self.avatar, size=(150, 150))
        
        super().save(*args, **kwargs)
    
    def make_thumbnail(self, image, size=(150, 150)):
        img = Image.open(image)
        
        # RGB ga o'tkazish
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Thumbnail
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        # BytesIO ga saqlash
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=85)
        thumb_io.seek(0)
        
        # Fayl nomi
        name, ext = os.path.splitext(image.name)
        thumb_filename = f'{name}_thumb.jpg'
        
        # InMemoryUploadedFile
        thumbnail = InMemoryUploadedFile(
            thumb_io,
            None,
            thumb_filename,
            'image/jpeg',
            thumb_io.tell(),
            None
        )
        
        return thumbnail