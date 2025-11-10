"""
Custom User Model misoli
Bu misolda qo'shimcha ma'lumotlar bilan User modelini kengaytirish ko'rsatilgan
"""

# =============================================================================
# 1-USUL: User modelini extend qilish (OneToOne relation)
# =============================================================================

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserProfile(models.Model):
    """
    User modeliga qo'shimcha ma'lumotlar qo'shish
    Bu usul mavjud loyihalar uchun yaxshi
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # Qo'shimcha ma'lumotlar
    phone_regex = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Telefon raqami: +998XXXXXXXXX formatida bo'lishi kerak"
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=13,
        blank=True,
        null=True
    )
    
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    # Manzil
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Uzbekistan')
    
    # Avatar
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )
    
    # Ijtimoiy tarmoqlar
    website = models.URLField(max_length=200, blank=True)
    github = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    
    # Statistika
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Foydalanuvchi Profili'
        verbose_name_plural = 'Foydalanuvchi Profillari'
    
    def __str__(self):
        return f"{self.user.username} - Profile"


# Signal: User yaratilganda avtomatik UserProfile yaratish
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """User yaratilganda UserProfile yaratish"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """User saqlanganida UserProfile ni ham saqlash"""
    instance.profile.save()


# =============================================================================
# Serializer - Profile bilan
# =============================================================================

from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    """UserProfile serializer"""
    
    class Meta:
        model = UserProfile
        fields = [
            'phone_number', 'bio', 'birth_date',
            'city', 'country', 'avatar',
            'website', 'github', 'linkedin'
        ]


class UserWithProfileSerializer(serializers.ModelSerializer):
    """User va Profile birga"""
    profile = UserProfileSerializer()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name',
            'profile'
        ]
        read_only_fields = ['id']


class UserRegistrationWithProfileSerializer(serializers.ModelSerializer):
    """Ro'yxatdan o'tish - profile bilan"""
    
    password2 = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    # Profile fieldlari
    phone_number = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name',
            'phone_number', 'bio', 'city'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
    
    def validate(self, attrs):
        """Parollarni tekshirish"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Parollar bir xil emas."
            })
        return attrs
    
    def create(self, validated_data):
        """User va Profile yaratish"""
        # Profile ma'lumotlarini ajratish
        phone_number = validated_data.pop('phone_number', None)
        bio = validated_data.pop('bio', '')
        city = validated_data.pop('city', '')
        password2 = validated_data.pop('password2')
        
        # User yaratish
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Profile yangilash (signal orqali allaqachon yaratilgan)
        profile = user.profile
        if phone_number:
            profile.phone_number = phone_number
        profile.bio = bio
        profile.city = city
        profile.save()
        
        return user


# =============================================================================
# View - Profile bilan
# =============================================================================

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([AllowAny])
def register_with_profile(request):
    """Ro'yxatdan o'tish - profile bilan"""
    
    serializer = UserRegistrationWithProfileSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # User va profile ma'lumotlarini qaytarish
        user_data = UserWithProfileSerializer(user).data
        
        return Response({
            'user': user_data,
            'message': 'Foydalanuvchi muvaffaqiyatli ro\'yxatdan o\'tdi'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Foydalanuvchi profilini ko'rish va tahrirlash
    
    GET - Profilni ko'rish
    PUT - To'liq yangilash
    PATCH - Qisman yangilash
    """
    user = request.user
    
    if request.method == 'GET':
        serializer = UserWithProfileSerializer(user)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        # User ma'lumotlarini yangilash
        user_fields = ['first_name', 'last_name', 'email']
        for field in user_fields:
            if field in request.data:
                setattr(user, field, request.data[field])
        user.save()
        
        # Profile ma'lumotlarini yangilash
        profile_serializer = UserProfileSerializer(
            user.profile,
            data=request.data,
            partial=(request.method == 'PATCH')
        )
        
        if profile_serializer.is_valid():
            profile_serializer.save()
            
            # Yangilangan ma'lumotlarni qaytarish
            user_serializer = UserWithProfileSerializer(user)
            return Response(user_serializer.data)
        
        return Response(
            profile_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =============================================================================
# Test ma'lumotlar
# =============================================================================

def create_sample_data():
    """Test uchun ma'lumotlar yaratish"""
    
    # Admin
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    admin.profile.phone_number = '+998901234567'
    admin.profile.bio = 'Administrator'
    admin.profile.city = 'Tashkent'
    admin.profile.save()
    
    # Oddiy foydalanuvchilar
    users_data = [
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '+998901111111',
            'bio': 'Software Developer',
            'city': 'Samarkand'
        },
        {
            'username': 'jane_smith',
            'email': 'jane@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone': '+998902222222',
            'bio': 'Designer',
            'city': 'Bukhara'
        },
    ]
    
    for data in users_data:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password='password123',
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.profile.phone_number = data['phone']
        user.profile.bio = data['bio']
        user.profile.city = data['city']
        user.profile.save()
        
        print(f"✅ Created user: {user.username}")


# =============================================================================
# Management Command
# =============================================================================

"""
management/commands/create_sample_users.py

from django.core.management.base import BaseCommand
from accounts.models import create_sample_data

class Command(BaseCommand):
    help = 'Test uchun foydalanuvchilar yaratish'
    
    def handle(self, *args, **options):
        create_sample_data()
        self.stdout.write(
            self.style.SUCCESS('Test ma\'lumotlar yaratildi!')
        )
"""


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║          CUSTOM USER MODEL MISOLI                        ║
    ╚══════════════════════════════════════════════════════════╝
    
    Bu faylda quyidagilar ko'rsatilgan:
    
    1. UserProfile modeli yaratish
    2. Signal orqali avtomatik profile yaratish
    3. Serializer'lar
    4. View'lar (register, get/update profile)
    5. Test ma'lumotlar
    
    Qo'llash uchun:
    1. models.py ga UserProfile modelini qo'shing
    2. signals.py yarating va signallarni qo'shing
    3. apps.py da signallarni ulang
    4. python manage.py makemigrations
    5. python manage.py migrate
    
    """)