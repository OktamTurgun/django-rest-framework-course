from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Foydalanuvchi ro'yxatdan o'tkazish uchun serializer
    """
    # Parolni ikki marta kiritish uchun qo'shimcha field
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    # Parolni write_only qilamiz (response'da ko'rinmaydi)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True}  # Emailni majburiy qilamiz
        }

    def validate(self, attrs):
        """
        Parollarning bir xilligini tekshirish
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Parollar bir xil emas."
            })
        return attrs

    def validate_email(self, value):
        """
        Email uniqueligini tekshirish
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Bu email allaqachon ro'yxatdan o'tgan."
            )
        return value

    def create(self, validated_data):
        """
        Yangi foydalanuvchi yaratish
        """
        # password2 ni olib tashlaymiz (kerak emas)
        validated_data.pop('password2')
        # Extract optional names
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')

        # Foydalanuvchini yaratamiz
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

        # Set additional name fields
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()

        return user
    

class CustomLoginSerializer(LoginSerializer):
    username = None  # username maydonini olib tashlaymiz
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    {"non_field_errors": ["Unable to log in with provided credentials."]}
                )
        else:
            raise serializers.ValidationError(
                {"non_field_errors": ['Must include "email" and "password".']}
            )

        attrs['user'] = user
        return attrs



class UserSerializer(serializers.ModelSerializer):
    """
    Foydalanuvchi ma'lumotlarini ko'rsatish uchun serializer
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'date_joined',
        ]
        read_only_fields = ['id', 'date_joined']

# ============================================================================
# SOCIAL AUTH SERIALIZERS (accounts/serializers.py ga qo'shing)
# ============================================================================

from rest_framework import serializers
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount


class SocialAccountSerializer(serializers.ModelSerializer):
    """Social Account Serializer"""
    provider_name = serializers.SerializerMethodField()
    profile_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SocialAccount
        fields = [
            'id',
            'provider',
            'provider_name',
            'uid',
            'extra_data',
            'date_joined',
            'last_login',
            'profile_url',
        ]
        read_only_fields = fields
    
    def get_provider_name(self, obj):
        return obj.provider.capitalize()
    
    def get_profile_url(self, obj):
        if obj.provider == 'github':
            username = obj.extra_data.get('login')
            if username:
                return f"https://github.com/{username}"
        elif obj.provider == 'facebook':
            return f"https://facebook.com/{obj.uid}"
        return None


class UserProfileSerializer(serializers.ModelSerializer):
    """
    User Profile Serializer with Social Accounts
    
    FIXED VERSION - Profile fields through 'profile' relationship
    """
    full_name = serializers.SerializerMethodField()
    display_picture = serializers.SerializerMethodField()
    social_accounts = SocialAccountSerializer(
        many=True, 
        read_only=True, 
        source='socialaccount_set'
    )
    has_password = serializers.SerializerMethodField()
    social_providers = serializers.SerializerMethodField()
    is_social_authenticated = serializers.SerializerMethodField()
    
    # Profile fields - FIXED: SerializerMethodField ishlatamiz
    bio = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    website = serializers.SerializerMethodField()
    github_url = serializers.SerializerMethodField()
    github_username = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    email_verified = serializers.SerializerMethodField()
    membership_type = serializers.SerializerMethodField()
    is_premium = serializers.SerializerMethodField()
    profile_picture_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'display_picture',
            
            # Profile fields
            'bio',
            'location',
            'phone',
            'company',
            'website',
            'github_url',
            'github_username',
            'language',
            'email_verified',
            'membership_type',
            'is_premium',
            'profile_picture_url',
            
            # Metadata
            'date_joined',
            'last_login',
            'is_active',
            
            # Social accounts
            'social_accounts',
            'has_password',
            'social_providers',
            'is_social_authenticated',
        ]
        read_only_fields = [
            'id',
            'username',
            'date_joined',
            'last_login',
            'social_accounts',
            'has_password',
            'social_providers',
            'is_social_authenticated',
        ]
    
    def get_full_name(self, obj):
        """Full name"""
        if hasattr(obj, 'profile'):
            return obj.profile.full_name
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username
    
    def get_display_picture(self, obj):
        """Display picture"""
        if hasattr(obj, 'profile'):
            return obj.profile.display_picture
        return None
    
    def get_bio(self, obj):
        return obj.profile.bio if hasattr(obj, 'profile') else ""
    
    def get_location(self, obj):
        return obj.profile.location if hasattr(obj, 'profile') else ""
    
    def get_phone(self, obj):
        return obj.profile.phone if hasattr(obj, 'profile') else ""
    
    def get_company(self, obj):
        return obj.profile.company if hasattr(obj, 'profile') else None
    
    def get_website(self, obj):
        return obj.profile.website if hasattr(obj, 'profile') else None
    
    def get_github_url(self, obj):
        return obj.profile.github_url if hasattr(obj, 'profile') else None
    
    def get_github_username(self, obj):
        return obj.profile.github_username if hasattr(obj, 'profile') else None
    
    def get_language(self, obj):
        return obj.profile.language if hasattr(obj, 'profile') else 'en'
    
    def get_email_verified(self, obj):
        return obj.profile.email_verified if hasattr(obj, 'profile') else False
    
    def get_membership_type(self, obj):
        return obj.profile.membership_type if hasattr(obj, 'profile') else 'free'
    
    def get_is_premium(self, obj):
        return obj.profile.is_premium if hasattr(obj, 'profile') else False
    
    def get_profile_picture_url(self, obj):
        return obj.profile.profile_picture_url if hasattr(obj, 'profile') else None
    
    def get_has_password(self, obj):
        """User parol o'rnatganmi?"""
        return obj.has_usable_password()
    
    def get_social_providers(self, obj):
        """Ulangan social providerlar ro'yxati"""
        return [acc.provider for acc in obj.socialaccount_set.all()]
    
    def get_is_social_authenticated(self, obj):
        """Social authentication bormi?"""
        return obj.socialaccount_set.exists()


class UpdateProfileSerializer(serializers.Serializer):
    """Profile ni update qilish uchun"""
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)
    location = serializers.CharField(max_length=100, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    company = serializers.CharField(max_length=100, required=False, allow_blank=True)
    website = serializers.URLField(max_length=200, required=False, allow_blank=True)
    language = serializers.CharField(max_length=10, required=False)
    
    def validate_phone(self, value):
        """Phone validation"""
        if value and not value.replace('+', '').replace(' ', '').replace('-', '').isdigit():
            raise serializers.ValidationError("Invalid phone number format")
        return value
    
    def update(self, instance, validated_data):
        """Update user and profile"""
        # User fields
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']
        
        instance.save()
        
        # Profile fields
        if hasattr(instance, 'profile'):
            profile = instance.profile
            profile_fields = ['bio', 'location', 'phone', 'company', 'website', 'language']
            
            for field in profile_fields:
                if field in validated_data:
                    setattr(profile, field, validated_data[field])
            
            profile.save()
        
        return instance


class SetPasswordSerializer(serializers.Serializer):
    """Parol o'rnatish (social auth userlar uchun)"""
    new_password = serializers.CharField(
        min_length=8,
        max_length=128,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        min_length=8,
        max_length=128,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """Validate passwords match"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                "new_password_confirm": "Passwords do not match."
            })
        return attrs
    
    def save(self, user):
        """Set password"""
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class SocialAccountDetailSerializer(serializers.ModelSerializer):
    """Detailed Social Account info"""
    provider_name = serializers.SerializerMethodField()
    profile_data = serializers.SerializerMethodField()
    
    class Meta:
        model = SocialAccount
        fields = [
            'id',
            'provider',
            'provider_name',
            'uid',
            'profile_data',
            'date_joined',
            'last_login',
        ]
        read_only_fields = fields
    
    def get_provider_name(self, obj):
        return obj.provider.capitalize()
    
    def get_profile_data(self, obj):
        """Provider-specific data"""
        data = obj.extra_data
        
        if obj.provider == 'google':
            return {
                'email': data.get('email'),
                'name': data.get('name'),
                'picture': data.get('picture'),
                'verified_email': data.get('verified_email'),
                'locale': data.get('locale'),
            }
        elif obj.provider == 'github':
            return {
                'username': data.get('login'),
                'name': data.get('name'),
                'avatar': data.get('avatar_url'),
                'bio': data.get('bio'),
                'location': data.get('location'),
                'company': data.get('company'),
                'blog': data.get('blog'),
                'public_repos': data.get('public_repos'),
                'followers': data.get('followers'),
            }
        
        return data

class UserBasicSerializer(serializers.ModelSerializer):
    """
    Basic User Serializer
    
    Minimal user ma'lumotlari (masalan, book authorlarida)
    """
    full_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'full_name',
            'avatar',
        ]
    
    def get_full_name(self, obj):
        """Full name"""
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username
    
    def get_avatar(self, obj):
        """Profile picture"""
        return getattr(obj, 'profile_picture', None)


class UpdateProfileSerializer(serializers.Serializer):
    """
    Profile ni update qilish uchun serializer
    
    PATCH /api/v1/users/me/
    """
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)
    location = serializers.CharField(max_length=100, required=False, allow_blank=True)
    company = serializers.CharField(max_length=100, required=False, allow_blank=True)
    
    def update(self, instance, validated_data):
        """Update user profile"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class SetPasswordSerializer(serializers.Serializer):
    """
    Parol o'rnatish (social auth userlar uchun)
    
    POST /api/v1/users/me/set-password/
    """
    new_password = serializers.CharField(
        min_length=8,
        max_length=128,
        write_only=True,
        required=True
    )
    new_password_confirm = serializers.CharField(
        min_length=8,
        max_length=128,
        write_only=True,
        required=True
    )
    
    def validate(self, attrs):
        """Validate passwords match"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                "new_password_confirm": "Passwords do not match."
            })
        return attrs
    
    def save(self, user):
        """Set password"""
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class SocialAccountDisconnectSerializer(serializers.Serializer):
    """
    Social account ni disconnect qilish validatsiyasi
    """
    provider = serializers.CharField(required=True)
    
    def validate_provider(self, value):
        """Validate provider exists"""
        valid_providers = ['google', 'github', 'facebook', 'twitter']
        if value not in valid_providers:
            raise serializers.ValidationError(
                f"Invalid provider. Must be one of: {', '.join(valid_providers)}"
            )
        return value