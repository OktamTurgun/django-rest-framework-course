from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Book
from .validators import (
    validate_isbn_format,
    validate_not_digits_only,
    validate_no_special_chars,
    validate_capitalized,
    PriceRangeValidator,
    MinWordsValidator,
    YearRangeValidator
)
from datetime import date


# ============================================
# 1. FIELD-LEVEL VALIDATION
# ============================================

class BookFieldValidationSerializer(serializers.ModelSerializer):
    """
    Field-level validation misollari
    Har bir field uchun alohida validate_ metodi
    """
    
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate_title(self, value):
        """
        Title validation:
        - Kamida 2 ta so'zdan iborat
        - Bosh harf bilan boshlanadi
        """
        words = value.split()
        if len(words) < 2:
            raise serializers.ValidationError(
                "Kitob nomi kamida 2 ta so'zdan iborat bo'lishi kerak"
            )
        
        if not value[0].isupper():
            raise serializers.ValidationError(
                "Kitob nomi bosh harf bilan boshlanishi kerak"
            )
        
        if value.isdigit():
            raise serializers.ValidationError(
                "Sarlavha faqat raqamlardan iborat bo'lishi mumkin emas!"
            )
        
        return value.title()  # Har bir so'zni bosh harf bilan qaytarish
    
    def validate_author(self, value):
        """
        Author validation:
        - Kamida 2 ta so'z (ism va familiya)
        - Har bir so'z bosh harf bilan
        """
        words = value.split()
        if len(words) < 2:
            raise serializers.ValidationError(
                "Muallif ismi kamida 2 ta so'zdan (ism va familiya) iborat bo'lishi kerak"
            )
        
        for word in words:
            if not word[0].isupper():
                raise serializers.ValidationError(
                    "Har bir so'z bosh harf bilan boshlanishi kerak"
                )
        
        return value
    
    def validate_isbn(self, value):
        """
        ISBN validation:
        - 10 yoki 13 ta belgi
        - Unique bo'lishi kerak
        """
        clean_value = value.replace('-', '').replace(' ', '')
        
        if len(clean_value) not in [10, 13]:
            raise serializers.ValidationError(
                "ISBN 10 yoki 13 ta belgidan iborat bo'lishi kerak"
            )
        
        if not clean_value.isdigit():
            raise serializers.ValidationError(
                "ISBN faqat raqamlardan iborat bo'lishi kerak"
            )
        
        # Uniqueness check
        if not self.instance:  # Yangi obyekt
            if Book.objects.filter(isbn_number=value).exists():
                raise serializers.ValidationError(
                    "Bu ISBN allaqachon mavjud"
                )
        else:  # Mavjud obyektni yangilash
            if Book.objects.filter(isbn_number=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError(
                    "Bu ISBN allaqachon mavjud"
                )
        
        return value
    
    def validate_price(self, value):
        """
        Price validation:
        - Musbat son
        - 15000 so'm dan kam emas
        - 1000000 so'm dan ko'p emas
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Narx musbat son bo'lishi kerak"
            )
        
        if value < 15000:
            raise serializers.ValidationError(
                "Kitob narxi kamida 15000 so'm bo'lishi kerak"
            )
        
        if value > 1000000:
            raise serializers.ValidationError(
                "Narx 1000000 so'mdan oshmasligi kerak"
            )
        
        return value
    
    def validate_published_date(self, value):
        """
        Published date validation:
        - Kelajakda emas
        - 1450-yildan keyin (Gutenberg bosmaxonasi)
        """
        if value > date.today():
            raise serializers.ValidationError(
                "Nashr sanasi kelajakda bo'lishi mumkin emas"
            )
        
        if value.year < 1450:
            raise serializers.ValidationError(
                "Nashr sanasi 1450-yildan keyin bo'lishi kerak"
            )
        
        return value


# ============================================
# 2. OBJECT-LEVEL VALIDATION
# ============================================

class BookObjectValidationSerializer(serializers.ModelSerializer):
    """
    Object-level validation misollari
    Bir nechta fieldlarni birgalikda tekshirish
    """
    
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate(self, data):
        """
        Object-level validation:
        - Title va author kombinatsiyasi unique
        - Subtitle title'dan qisqa bo'lmasligi kerak
        """
        # 1. Title va author unique kombinatsiyasi
        title = data.get('title')
        author = data.get('author')
        
        if title and author:
            queryset = Book.objects.filter(title=title, author=author)
            
            if not self.instance:  # Yangi obyekt
                if queryset.exists():
                    raise serializers.ValidationError(
                        "Bu muallif tomonidan bunday nomli kitob allaqachon mavjud"
                    )
            else:  # Mavjud obyektni yangilash
                if queryset.exclude(pk=self.instance.pk).exists():
                    raise serializers.ValidationError(
                        "Bu muallif tomonidan bunday nomli kitob allaqachon mavjud"
                    )
        
        # 2. Subtitle validation
        subtitle = data.get('subtitle', '')
        if subtitle and title:
            if len(subtitle) > len(title):
                raise serializers.ValidationError({
                    'subtitle': 'Subtitle asosiy nomdan uzun bo\'lmasligi kerak'
                })
        
        return data


# ============================================
# 3. CUSTOM VALIDATORS
# ============================================

class BookCustomValidatorsSerializer(serializers.ModelSerializer):
    """
    Custom validators bilan serializer
    Qayta ishlatish mumkin bo'lgan validator'lar
    """
    
    title = serializers.CharField(
        max_length=200,
        validators=[
            validate_no_special_chars,
            MinWordsValidator(2)
        ]
    )
    
    author = serializers.CharField(
        max_length=100,
        validators=[validate_capitalized]
    )
    
    isbn_number = serializers.CharField(
        max_length=17,
        validators=[
            validate_isbn_format,
            UniqueValidator(
                queryset=Book.objects.all(),
                message='Bu ISBN allaqachon mavjud'
            )
        ]
    )
    
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[PriceRangeValidator(5, 1000)]
    )
    
    published_date = serializers.DateField(
        validators=[YearRangeValidator(1450, date.today().year)]
    )
    
    class Meta:
        model = Book
        fields = '__all__'


# ============================================
# 4. BUILT-IN VALIDATORS
# ============================================

class BookBuiltInValidatorsSerializer(serializers.ModelSerializer):
    """
    Django built-in validators bilan serializer
    """
    
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(15000, message="Narx kamida 15000 so'm bo'lishi kerak"),
            MaxValueValidator(1000000, message="Narx 1000000 so'm dan oshmasligi kerak")
        ]
    )
    
    class Meta:
        model = Book
        fields = '__all__'


# ============================================
# 5. COMBINED VALIDATION (HAMMASINI BIRLASHTIRISH)
# ============================================

class BookCompleteValidationSerializer(serializers.ModelSerializer):
    """
    Barcha validation turlarini birlashtirgan to'liq serializer
    """
    
    # Custom validators
    title = serializers.CharField(
        max_length=200,
        validators=[
            validate_no_special_chars,
            validate_not_digits_only,
            MinWordsValidator(2)
        ]
    )
    
    isbn_number = serializers.CharField(
        max_length=17,
        validators=[
            validate_isbn_format,
            UniqueValidator(
                queryset=Book.objects.all(),
                message='Bu ISBN allaqachon mavjud'
            )
        ]
    )
    
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(15000, message="Narx kamida 15000 so'm bo'lishi kerak"),
            MaxValueValidator(1000000, message="Narx 1000000 so'm dan oshmasligi kerak")
        ]
    )
    
    published_date = serializers.DateField(
        validators=[YearRangeValidator(1450, date.today().year)]
    )
    
    class Meta:
        model = Book
        fields = '__all__'

    # Field-level validation
    def validate_author(self, value):
        """Author har bir so'z bosh harf bilan"""
        words = value.split()
        if len(words) < 2:
            raise serializers.ValidationError(
                "Muallif ismi kamida 2 ta so'zdan iborat bo'lishi kerak"
            )
        
        for word in words:
            if not word[0].isupper():
                raise serializers.ValidationError(
                    "Har bir so'z bosh harf bilan boshlanishi kerak"
                )
        
        return value
    
    # Object-level validation
    def validate(self, data):
        """Barcha fieldlarni tekshirish"""
        
        # Title va author unique kombinatsiyasi
        title = data.get('title')
        author = data.get('author')
        cover_image = data.get('cover_image')
        
        if title and author:
            queryset = Book.objects.filter(title=title, author=author)
            
            if not self.instance:
                if queryset.exists():
                    raise serializers.ValidationError(
                        "Bu muallif tomonidan bunday nomli kitob allaqachon mavjud"
                    )
            else:
                if queryset.exclude(pk=self.instance.pk).exists():
                    raise serializers.ValidationError(
                        "Bu muallif tomonidan bunday nomli kitob allaqachon mavjud"
                    )
                
        if cover_image:
            same_cover_books = Book.objects.filter(cover_image=cover_image)
            if same_cover_books.exists():
                raise serializers.ValidationError(
                    "Bu rasm boshqa kitob uchun allaqachon ishlatilgan"
                )
        
        return data


# Default serializer (backward compatibility)
BookSerializer = BookCompleteValidationSerializer
BookModelSerializer = BookCompleteValidationSerializer
BookListSerializer = BookCompleteValidationSerializer
BookDetailSerializer = BookCompleteValidationSerializer