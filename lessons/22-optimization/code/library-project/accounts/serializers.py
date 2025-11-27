from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


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
        fields = ('id', 'username', 'email', 'password', 'password2')
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
        
        # Foydalanuvchini yaratamiz
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Foydalanuvchi ma'lumotlarini ko'rsatish uchun serializer
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)