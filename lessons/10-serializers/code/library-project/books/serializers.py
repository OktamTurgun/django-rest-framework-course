from rest_framework import serializers
from .models import Book
from datetime import date

# ===== 1. Oddiy Serializer =====
class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    subtitle = serializers.CharField(max_length=200, required=False, allow_blank=True)
    author = serializers.CharField(max_length=100)
    isbn_number = serializers.CharField(max_length=13)
    pages = serializers.IntegerField()
    language = serializers.CharField(max_length=30)
    cover_image = serializers.URLField(required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    published_date = serializers.DateField()
    # description = serializers.CharField()

    def validate_title(self, value):
        if str(value).isdigit():
            raise serializers.ValidationError("Sarlavha faqat raqamlardan iborat bo'lishi mumkin emas!")
        return value
    
    def validate_isbn_number(self, value):
        """ISBN formatini tekshirish"""
        if len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN 10 yoki 13 ta belgidan iborat bo'lishi kerak")
        return value
    
    def validate_price(self, value):
        """Narx musbat bo'lishini tekshirish"""
        if value < 0:
            raise serializers.ValidationError("Narx musbat son bo'lishi kerak")
        return value
    
    def validate(self, data):
        """Umumiy validation"""
        if data.get('published_date') and data['published_date'] > date.today():
            raise serializers.ValidationError({
                "published_date": "Nashr sanasi kelajakda bo'lishi mumkin emas"
            })
        return data
    
    def create(self, validated_data):
        """Yangi kitob yaratish"""
        return Book.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Mavjud kitobni yangilash"""
        instance.title = validated_data.get('title', instance.title)
        instance.subtitle = validated_data.get('subtitle', instance.subtitle)
        instance.author = validated_data.get('author', instance.author)
        instance.isbn_number = validated_data.get('isbn_number', instance.isbn_number)
        instance.price = validated_data.get('price', instance.price)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        # instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


# ===== 2. ModelSerializer =====
class BookModelSerializer(serializers.ModelSerializer):
    # Qo'shimcha field - nashr qilinganiga necha kun bo'ldi
    days_since_published = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = '__all__'
        # yoki aniq fieldlarni ko'rsatish:
        # fields = ['id', 'title', 'author', 'price', 'days_since_published']
        
        # Read-only fieldlar
        read_only_fields = ['id']
    
    def get_days_since_published(self, obj):
        """Nashr qilinganiga necha kun bo'lganini hisoblash"""
        delta = date.today() - obj.published_date
        return delta.days
    
    def validate_isbn_number(self, value):
        """ISBN formatini tekshirish"""
        if len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN 10 yoki 13 ta belgidan iborat bo'lishi kerak")
        return value
    
    def validate_price(self, value):
        """Narx musbat bo'lishini tekshirish"""
        if value < 0:
            raise serializers.ValidationError("Narx musbat son bo'lishi kerak")
        return value

    def validate_title(self, value):
        if str(value).isdigit():
            raise serializers.ValidationError("Sarlavha faqat raqamlardan iborat bo'lishi mumkin emas!")
        return value


# ===== 3. Soddalashtirilgan ModelSerializer =====
class BookListSerializer(serializers.ModelSerializer):
    """Ro'yxat ko'rinishi uchun sodda serializer"""
    class Meta:
        model = Book
        fields = "__all__"


# ===== 4. Batafsil ModelSerializer =====
class BookDetailSerializer(serializers.ModelSerializer):
    """Batafsil ko'rinish uchun to'liq serializer"""
    days_since_published = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = '__all__'
    
    def get_days_since_published(self, obj):
        delta = date.today() - obj.published_date
        return delta.days