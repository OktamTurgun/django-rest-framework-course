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


# ============================================================================
# AUTHOR MODEL - UPDATED with statistics fields
# ============================================================================

class Author(models.Model):
    """Muallif modeli - updated for Lesson 28"""
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)  # Made optional
    birth_date = models.DateField(null=True, blank=True)  # Made optional
    email = models.EmailField(unique=True, null=True, blank=True)  # Made optional
    
    # NEW: Statistics fields (updated by signals)
    total_books = models.IntegerField(default=0)
    available_books = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "authors"
        ordering = ["name"]
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name


# ============================================================================
# GENRE MODEL - Kept as is (same as Category concept)
# ============================================================================

class Genre(models.Model):
    """Janr modeli"""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "genres"
        ordering = ["name"]
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


# ============================================================================
# BOOK MODEL - MERGED VERSION
# ============================================================================

class Book(models.Model):
    """
    Book model - Merged version with all features
    Combines: caching, optimization, and new fields for Lesson 28
    """
    
    # Basic fields
    title = models.CharField(
        max_length=200,
        db_index=True
    )
    isbn_number = models.CharField(  # Keep original field name
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
    
    # NEW: Availability flag (for Lesson 28)
    is_available = models.BooleanField(default=True)
    
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
    # CACHED CLASS METHODS (from Lesson 24)
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

# ============================================================================
# BOOK LOG MODEL - NEW for Lesson 28
# ============================================================================

class BookLog(models.Model):
    """Book operation log"""
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
    ]

    book_title = models.CharField(max_length=255)
    book_id = models.IntegerField(null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.action.upper()}: {self.book_title} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Book Log'
        verbose_name_plural = 'Book Logs'


# ============================================================================
# BORROW HISTORY MODEL - NEW for Lesson 28
# ============================================================================

class BorrowHistory(models.Model):
    """Book borrow/return history"""
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='borrow_history'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='borrow_history'
    )
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        status = "Returned" if self.returned_at else "Borrowed"
        return f"{self.book.title} - {self.user.username} ({status})"

    @property
    def is_overdue(self):
        """Check if book is overdue"""
        if self.returned_at:
            return False
        from django.utils import timezone
        return timezone.now() > self.due_date

    class Meta:
        ordering = ['-borrowed_at']
        verbose_name = 'Borrow History'
        verbose_name_plural = 'Borrow Histories'


# ============================================================================
# REVIEW MODEL - Kept as is
# ============================================================================

class Review(models.Model):
    """Book review model"""
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE,
        related_name='reviews'  
    )
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.book.title} - Rating: {self.rating}'

    class Meta:
        ordering = ['-created_at']


# ============================================================================
# SIGNAL HANDLERS - Cache invalidation (from Lesson 24)
# ============================================================================

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