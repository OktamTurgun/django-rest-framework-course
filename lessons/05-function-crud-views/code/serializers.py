from rest_framework import serializers
from .models import Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Book modelini serializer qilish uchun
    """
    # Read-only maydon - computed property
    is_new = serializers.ReadOnlyField()
    
    # Custom maydon - URL
    absolute_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'isbn',
            'price',
            'published_date',
            'pages',
            'language',
            'is_available',
            'is_new',
            'absolute_url',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_new']
    
    def get_absolute_url(self, obj):
        """Kitobning to'liq URL manzilini qaytarish"""
        return obj.get_absolute_url()
    
    def validate_isbn(self, value):
        """
        ISBN validatsiyasi - 13 raqam bo'lishi kerak
        """
        if not value.isdigit():
            raise serializers.ValidationError(
                "ISBN faqat raqamlardan iborat bo'lishi kerak"
            )
        
        if len(value) != 13:
            raise serializers.ValidationError(
                "ISBN 13 ta raqamdan iborat bo'lishi kerak"
            )
        
        return value
    
    def validate_price(self, value):
        """
        Narx validatsiyasi - musbat bo'lishi kerak
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Narx 0 dan katta bo'lishi kerak"
            )
        
        if value > 10000000:  # 10 million
            raise serializers.ValidationError(
                "Narx juda katta (maksimal 10,000,000)"
            )
        
        return value
    
    def validate_pages(self, value):
        """
        Sahifalar soni validatsiyasi
        """
        if value < 1:
            raise serializers.ValidationError(
                "Sahifalar soni kamida 1 bo'lishi kerak"
            )
        
        if value > 10000:
            raise serializers.ValidationError(
                "Sahifalar soni juda ko'p (maksimal 10,000)"
            )
        
        return value
    
    def validate_published_date(self, value):
        """
        Nashr sanasi validatsiyasi - kelajakda bo'lmasligi kerak
        """
        if value > datetime.now().date():
            raise serializers.ValidationError(
                "Nashr sanasi kelajakda bo'lishi mumkin emas"
            )
        
        return value
    
    def validate(self, data):
        """
        Umumiy validatsiya - bir nechta maydonlarni birga tekshirish
        """
        # Agar is_available=False bo'lsa, narx 0 bo'lishi mumkin
        if not data.get('is_available', True) and data.get('price', 0) == 0:
            raise serializers.ValidationError(
                "Mavjud bo'lmagan kitobning narxi 0 bo'lishi mumkin emas"
            )
        
        return data


class BookListSerializer(serializers.ModelSerializer):
    """
    Kitoblar ro'yxati uchun qisqa serializer
    Faqat asosiy ma'lumotlarni qaytaradi
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'is_available']


class BookCreateSerializer(serializers.ModelSerializer):
    """
    Kitob yaratish uchun maxsus serializer
    """
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'isbn',
            'price',
            'published_date',
            'pages',
            'language',
            'is_available',
        ]
    
    def create(self, validated_data):
        """
        Kitob yaratishda qo'shimcha logika
        """
        # Title'ni capitalize qilish
        validated_data['title'] = validated_data['title'].title()
        
        # Author'ni capitalize qilish
        validated_data['author'] = validated_data['author'].title()
        
        return super().create(validated_data)