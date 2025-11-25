# examples/02-image-upload.py
"""
Image Upload - Rasm yuklash va Pillow bilan ishlash
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser

from PIL import Image
from io import BytesIO
import os


# =============================================================================
# 1. Model - ImageField
# =============================================================================

class UserProfile(models.Model):
    """
    User profili - avatar bilan
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text='User avatar image'
    )
    avatar_thumbnail = models.ImageField(
        upload_to='avatars/thumbnails/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def save(self, *args, **kwargs):
        """
        Avatar yuklanganda thumbnail yaratish
        """
        if self.avatar:
            # Thumbnail yaratish
            self.avatar_thumbnail = self.make_thumbnail(self.avatar)
        
        super().save(*args, **kwargs)
    
    def make_thumbnail(self, image, size=(150, 150)):
        """
        Thumbnail yaratish
        """
        img = Image.open(image)
        
        # RGBA -> RGB (JPEG uchun)
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        # Thumbnail yaratish
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        # BytesIO ga saqlash
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=85)
        thumb_io.seek(0)
        
        # Fayl nomi
        name, ext = os.path.splitext(image.name)
        thumb_filename = f'{name}_thumb.jpg'
        
        # InMemoryUploadedFile yaratish
        thumbnail = InMemoryUploadedFile(
            thumb_io,
            None,
            thumb_filename,
            'image/jpeg',
            thumb_io.tell(),
            None
        )
        
        return thumbnail


# =============================================================================
# 2. Book Cover Image
# =============================================================================

class Book(models.Model):
    """
    Kitob - muqova rasmi bilan
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    cover_image = models.ImageField(
        upload_to='book_covers/',
        blank=True,
        null=True
    )
    cover_thumbnail = models.ImageField(
        upload_to='book_covers/thumbnails/',
        blank=True,
        null=True
    )
    published_date = models.DateField()
    
    def save(self, *args, **kwargs):
        """
        Cover image yuklanganda thumbnail va optimize
        """
        if self.cover_image:
            # Optimize qilish
            self.cover_image = self.optimize_image(self.cover_image)
            # Thumbnail
            self.cover_thumbnail = self.make_thumbnail(self.cover_image)
        
        super().save(*args, **kwargs)
    
    def optimize_image(self, image, max_size=(800, 1200), quality=85):
        """
        Rasmni optimize qilish
        """
        img = Image.open(image)
        
        # RGB ga o'tkazish
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize (agar katta bo'lsa)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Saqlash
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        # Yangi fayl yaratish
        name, ext = os.path.splitext(image.name)
        filename = f'{name}.jpg'
        
        optimized = InMemoryUploadedFile(
            output,
            None,
            filename,
            'image/jpeg',
            output.tell(),
            None
        )
        
        return optimized
    
    def make_thumbnail(self, image, size=(200, 300)):
        """
        Thumbnail yaratish
        """
        img = Image.open(image)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=85)
        thumb_io.seek(0)
        
        name, ext = os.path.splitext(image.name)
        thumb_filename = f'{name}_thumb.jpg'
        
        return InMemoryUploadedFile(
            thumb_io,
            None,
            thumb_filename,
            'image/jpeg',
            thumb_io.tell(),
            None
        )


# =============================================================================
# 3. Serializers - Image fields
# =============================================================================

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Profile serializer - avatar URLs
    """
    avatar_url = serializers.SerializerMethodField()
    avatar_thumbnail_url = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'bio',
            'avatar',
            'avatar_url',
            'avatar_thumbnail_url',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None
    
    def get_avatar_thumbnail_url(self, obj):
        if obj.avatar_thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar_thumbnail.url)
            return obj.avatar_thumbnail.url
        return None


class BookSerializer(serializers.ModelSerializer):
    """
    Book serializer - cover image
    """
    cover_url = serializers.SerializerMethodField()
    cover_thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'isbn',
            'cover_image',
            'cover_url',
            'cover_thumbnail_url',
            'published_date'
        ]
    
    def get_cover_url(self, obj):
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
        return None
    
    def get_cover_thumbnail_url(self, obj):
        if obj.cover_thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_thumbnail.url)
        return None


# =============================================================================
# 4. ViewSet - Profile with avatar
# =============================================================================

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    User profile ViewSet
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        """
        Faqat o'z profilini ko'rish
        """
        if self.request.user.is_authenticated:
            return UserProfile.objects.filter(user=self.request.user)
        return UserProfile.objects.none()
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """
        O'z profilini olish va yangilash
        
        GET /api/profile/me/
        PUT /api/profile/me/
        """
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(
                profile,
                data=request.data,
                partial=(request.method == 'PATCH')
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def upload_avatar(self, request):
        """
        Avatar yuklash
        
        POST /api/profile/upload_avatar/
        Body: avatar (file)
        """
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        avatar = request.FILES.get('avatar')
        if not avatar:
            return Response(
                {'error': 'No image provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Eski avatar ni o'chirish
        if profile.avatar:
            profile.avatar.delete(save=False)
        if profile.avatar_thumbnail:
            profile.avatar_thumbnail.delete(save=False)
        
        # Yangi avatar
        profile.avatar = avatar
        profile.save()
        
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'])
    def delete_avatar(self, request):
        """
        Avatar ni o'chirish
        
        DELETE /api/profile/delete_avatar/
        """
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if profile.avatar:
            profile.avatar.delete(save=False)
        if profile.avatar_thumbnail:
            profile.avatar_thumbnail.delete(save=False)
        
        profile.avatar = None
        profile.avatar_thumbnail = None
        profile.save()
        
        return Response({'message': 'Avatar deleted'})


# =============================================================================
# 5. Book ViewSet with cover
# =============================================================================

class BookViewSet(viewsets.ModelViewSet):
    """
    Book ViewSet - cover image
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    @action(detail=True, methods=['post'])
    def upload_cover(self, request, pk=None):
        """
        Kitob muqovasini yuklash
        
        POST /api/books/{id}/upload_cover/
        """
        book = self.get_object()
        
        cover = request.FILES.get('cover')
        if not cover:
            return Response(
                {'error': 'No image provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Eski cover ni o'chirish
        if book.cover_image:
            book.cover_image.delete(save=False)
        if book.cover_thumbnail:
            book.cover_thumbnail.delete(save=False)
        
        # Yangi cover
        book.cover_image = cover
        book.save()
        
        serializer = self.get_serializer(book)
        return Response(serializer.data)


# =============================================================================
# 6. Image Processing Utilities
# =============================================================================

class ImageProcessor:
    """
    Image processing utilities
    """
    
    @staticmethod
    def resize_image(image_file, width, height):
        """
        Rasmni aniq o'lchamga keltirish
        """
        img = Image.open(image_file)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        output = BytesIO()
        img.save(output, format='JPEG', quality=90)
        output.seek(0)
        
        return output
    
    @staticmethod
    def crop_to_square(image_file, size=500):
        """
        Rasmni kvadratga crop qilish
        """
        img = Image.open(image_file)
        
        width, height = img.size
        min_dim = min(width, height)
        
        # Markazdan crop
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2
        
        img = img.crop((left, top, right, bottom))
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        output = BytesIO()
        img.save(output, format='JPEG', quality=90)
        output.seek(0)
        
        return output
    
    @staticmethod
    def add_watermark(image_file, watermark_text):
        """
        Rasmga watermark qo'shish
        """
        from PIL import ImageDraw, ImageFont
        
        img = Image.open(image_file)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        draw = ImageDraw.Draw(img)
        
        # Font (default)
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        # Position
        width, height = img.size
        text_width = draw.textlength(watermark_text, font=font)
        position = (width - text_width - 10, height - 50)
        
        # Draw text
        draw.text(position, watermark_text, font=font, fill=(255, 255, 255, 128))
        
        output = BytesIO()
        img.save(output, format='JPEG', quality=90)
        output.seek(0)
        
        return output


# =============================================================================
# Requirements
# =============================================================================

REQUIREMENTS = """
# Image processing uchun
Pillow==10.1.0
"""


# =============================================================================
# Postman Tests
# =============================================================================

POSTMAN_TESTS = """
# 1. Profile avatar yuklash
POST http://localhost:8000/api/profile/upload_avatar/
Content-Type: multipart/form-data
Authorization: Token YOUR_TOKEN

Body (form-data):
- avatar: [Select Image File]


# 2. Profile ni olish
GET http://localhost:8000/api/profile/me/
Authorization: Token YOUR_TOKEN


# 3. Book cover yuklash
POST http://localhost:8000/api/books/1/upload_cover/
Content-Type: multipart/form-data

Body (form-data):
- cover: [Select Image File]


# 4. Avatar ni o'chirish
DELETE http://localhost:8000/api/profile/delete_avatar/
Authorization: Token YOUR_TOKEN
"""