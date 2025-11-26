from io import BytesIO
import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from django.core.files.uploadedfile import InMemoryUploadedFile

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
    name = models.CharField(max_length= 50, unique=True)
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

class Book(models.Model):
    """
    Book model - YANGILANDI (Lesson 17)
    
    CLEAN START: Eski ma'lumotlar o'chiriladi, yangi tuzilma bilan boshlanadi
    """
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    
    # YANGI: Author object (ForeignKey)
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        related_name='books',
        null=True,
        blank=True,
        help_text='Kitobning muallifi (Author object)',
        verbose_name='Author'
    )
    
    isbn_number = models.CharField(max_length=13, unique=True)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    pages = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    language = models.CharField(max_length=50, default='English')
    published_date = models.DateField(null=True, blank=True)
    publisher = models.CharField(max_length=100)
    published = models.BooleanField(default=False)
    
    # YANGI: Genres (ManyToMany)
    genres = models.ManyToManyField(
        Genre,
        related_name='books',
        blank=True,
        help_text='Kitobning janrlari'
    )
    
    # Owner field (Lesson 16 dan)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='books',
        help_text='User who created this book'
    )

    available_copies = models.IntegerField(default=5, validators=[MinValueValidator(0)])

    # YANGI FIELDLAR! ✅
    cover_image = models.ImageField(
        upload_to='book_covers/',
        blank=True,
        null=True,
        help_text='Book cover image'
    )
    cover_thumbnail = models.ImageField(
        upload_to='book_covers/thumbnails/',
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
    
    def __str__(self):
        if self.author:
            return f"{self.title} by {self.author.name}"
        return self.title
    
    def save(self, *args, **kwargs):
        """
        Cover image yuklanganda thumbnail yaratish
        """
        if self.cover_image and not self.cover_thumbnail:
            self.cover_thumbnail = self.make_thumbnail(self.cover_image)
        
        super().save(*args, **kwargs)
    
    def make_thumbnail(self, image, size=(200, 300)):
        """
        Thumbnail yaratish
        """
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
    
# ==================== YANGI MODEL 20-Throttling ====================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
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
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def save(self, *args, **kwargs):
        """
        Avatar yuklanganda thumbnail yaratish
        """
        if self.avatar and not self.avatar_thumbnail:
            # Thumbnail yaratish (Book.make_thumbnail dan nusxalash)
            self.avatar_thumbnail = self.make_thumbnail(self.avatar, size=(150, 150))
        
        super().save(*args, **kwargs)
    
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