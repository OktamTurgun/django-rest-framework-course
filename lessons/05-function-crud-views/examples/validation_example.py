"""
Validation Examples - Function-based Views
=========================================

Bu faylda turli xil validatsiya usullari ko'rsatilgan.
"""

from rest_framework import serializers
from datetime import datetime, date


# ==================== FIELD-LEVEL VALIDATION ====================

class BookValidationSerializer(serializers.Serializer):
    """
    Har bir maydon uchun alohida validatsiya
    """
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=100)
    isbn = serializers.CharField(max_length=13)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    published_date = serializers.DateField()
    pages = serializers.IntegerField()
    
    def validate_title(self, value):
        """Title validatsiyasi"""
        if len(value) < 3:
            raise serializers.ValidationError(
                "Sarlavha kamida 3 ta belgidan iborat bo'lishi kerak"
            )
        
        if value.lower() in ['test', 'demo', 'sample']:
            raise serializers.ValidationError(
                "Bu nom ruxsat etilmagan"
            )
        
        return value.title()  # Har bir so'zni katta harf bilan boshlash
    
    def validate_author(self, value):
        """Author validatsiyasi"""
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError(
                "Muallif ismi faqat harflardan iborat bo'lishi kerak"
            )
        
        return value.title()
    
    def validate_isbn(self, value):
        """ISBN validatsiyasi - 13 raqam"""
        # Faqat raqamlar
        if not value.isdigit():
            raise serializers.ValidationError(
                "ISBN faqat raqamlardan iborat bo'lishi kerak"
            )
        
        # 13 ta raqam
        if len(value) != 13:
            raise serializers.ValidationError(
                "ISBN 13 ta raqamdan iborat bo'lishi kerak"
            )
        
        # Checksum validation (oddiy versiya)
        total = 0
        for i, digit in enumerate(value):
            if i % 2 == 0:
                total += int(digit)
            else:
                total += int(digit) * 3
        
        if total % 10 != 0:
            raise serializers.ValidationError(
                "ISBN checksum noto'g'ri"
            )
        
        return value
    
    def validate_price(self, value):
        """Price validatsiyasi"""
        if value <= 0:
            raise serializers.ValidationError(
                "Narx 0 dan katta bo'lishi kerak"
            )
        
        if value > 10000000:
            raise serializers.ValidationError(
                "Narx juda katta (maksimal 10,000,000)"
            )
        
        return value
    
    def validate_published_date(self, value):
        """Published date validatsiyasi"""
        # Kelajakda bo'lmasligi
        if value > date.today():
            raise serializers.ValidationError(
                "Nashr sanasi kelajakda bo'lishi mumkin emas"
            )
        
        # 1450-yildan oldin bo'lmasligi (Gutenberg printing press)
        if value.year < 1450:
            raise serializers.ValidationError(
                "Nashr sanasi 1450-yildan oldin bo'lishi mumkin emas"
            )
        
        return value
    
    def validate_pages(self, value):
        """Pages validatsiyasi"""
        if value < 1:
            raise serializers.ValidationError(
                "Sahifalar soni kamida 1 bo'lishi kerak"
            )
        
        if value > 10000:
            raise serializers.ValidationError(
                "Sahifalar soni juda ko'p (maksimal 10,000)"
            )
        
        return value


# ==================== OBJECT-LEVEL VALIDATION ====================

class BookObjectValidationSerializer(serializers.Serializer):
    """
    Bir nechta maydonlarni birga validatsiya qilish
    """
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    published_date = serializers.DateField()
    is_available = serializers.BooleanField(default=True)
    
    def validate(self, data):
        """
        Object-level validation - bir nechta maydonlarni tekshirish
        """
        
        # 1. Eski kitoblar arzon bo'lishi kerak
        years_old = (date.today() - data['published_date']).days / 365
        
        if years_old > 10 and data['price'] > 100000:
            raise serializers.ValidationError(
                "10 yildan eski kitoblar 100,000 so'mdan qimmat bo'lishi mumkin emas"
            )
        
        # 2. Mavjud bo'lmagan kitoblar 0 so'm bo'lishi mumkin emas
        if not data['is_available'] and data['price'] > 0:
            raise serializers.ValidationError(
                "Mavjud bo'lmagan kitoblar narxi 0 bo'lishi kerak"
            )
        
        # 3. Title va Author bir xil bo'lmasligi
        if data['title'].lower() == data['author'].lower():
            raise serializers.ValidationError(
                "Kitob nomi va muallif bir xil bo'lishi mumkin emas"
            )
        
        return data


# ==================== CUSTOM VALIDATORS ====================

def validate_positive_number(value):
    """Musbat son validatori"""
    if value <= 0:
        raise serializers.ValidationError(
            f"{value} musbat bo'lishi kerak"
        )


def validate_future_date(value):
    """Kelajak sana validatori"""
    if value < date.today():
        raise serializers.ValidationError(
            "Sana kelajakda bo'lishi kerak"
        )


def validate_isbn_format(value):
    """ISBN format validatori"""
    if not value.isdigit() or len(value) != 13:
        raise serializers.ValidationError(
            "ISBN 13 ta raqamdan iborat bo'lishi kerak"
        )


class BookCustomValidatorSerializer(serializers.Serializer):
    """
    Custom validatorlar bilan
    """
    title = serializers.CharField(max_length=200)
    price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[validate_positive_number]  # Custom validator
    )
    isbn = serializers.CharField(
        max_length=13,
        validators=[validate_isbn_format]  # Custom validator
    )


# ==================== DYNAMIC VALIDATION ====================

class DynamicValidationSerializer(serializers.Serializer):
    """
    Context ga qarab dinamik validatsiya
    """
    title = serializers.CharField(max_length=200)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_premium = serializers.BooleanField(default=False)
    
    def validate_price(self, value):
        """
        Context'dan user ma'lumotini olish
        """
        # Context orqali user ma'lumotini olish
        user = self.context.get('user')
        
        if user and user.is_staff:
            # Admin foydalanuvchilar har qanday narx qo'yishi mumkin
            return value
        
        # Oddiy foydalanuvchilar 1,000,000 dan ortiq qo'ya olmaydi
        if value > 1000000:
            raise serializers.ValidationError(
                "Siz 1,000,000 dan ortiq narx qo'ya olmaysiz"
            )
        
        return value
    
    def validate(self, data):
        """Premium kitoblar qimmatroq bo'lishi kerak"""
        if data.get('is_premium') and data.get('price', 0) < 50000:
            raise serializers.ValidationError(
                "Premium kitoblar kamida 50,000 so'm bo'lishi kerak"
            )
        
        return data


# ==================== VIEW'DA VALIDATION ====================

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def validate_book_data(request):
    """
    View'da qo'shimcha validatsiya qilish
    """
    serializer = BookValidationSerializer(data=request.data)
    
    # Serializer validatsiyasi
    if not serializer.is_valid():
        return Response(
            {
                'error': 'Validatsiya xatosi',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Qo'shimcha biznes logika validatsiyasi
    validated_data = serializer.validated_data
    
    # 1. Title unique ekanligini tekshirish
    from code.models import Book
    if Book.objects.filter(title__iexact=validated_data['title']).exists():
        return Response(
            {'error': 'Bu nomdagi kitob allaqachon mavjud'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 2. ISBN unique ekanligini tekshirish
    if Book.objects.filter(isbn=validated_data['isbn']).exists():
        return Response(
            {'error': 'Bu ISBN allaqachon mavjud'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 3. Muallif mavjudligini tekshirish (ixtiyoriy)
    # ... qo'shimcha validatsiyalar
    
    # Agar hammasi to'g'ri bo'lsa - saqlash
    # book = Book.objects.create(**validated_data)
    
    return Response(
        {
            'message': 'Validatsiya muvaffaqiyatli',
            'data': validated_data
        },
        status=status.HTTP_200_OK
    )


# ==================== MULTIPLE SERIALIZERS ====================

@api_view(['POST'])
def create_with_multiple_validations(request):
    """
    Turli validatsiya qatlamlaridan foydalanish
    """
    
    # 1. Birinchi qatlam - basic validation
    basic_serializer = BookValidationSerializer(data=request.data)
    if not basic_serializer.is_valid():
        return Response(
            {'error': 'Basic validation failed', 'details': basic_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 2. Ikkinchi qatlam - object validation
    object_serializer = BookObjectValidationSerializer(data=request.data)
    if not object_serializer.is_valid():
        return Response(
            {'error': 'Object validation failed', 'details': object_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 3. Uchinchi qatlam - business logic validation
    # ... database checks, external API calls, etc.
    
    return Response(
        {'message': 'Barcha validatsiyalar o\'tdi!'},
        status=status.HTTP_200_OK
    )


# ==================== ERROR FORMATTING ====================

@api_view(['POST'])
def formatted_validation_errors(request):
    """
    Validatsiya xatolarini chiroyli formatda qaytarish
    """
    serializer = BookValidationSerializer(data=request.data)
    
    if not serializer.is_valid():
        # Xatolarni chiroyli formatda
        formatted_errors = []
        
        for field, errors in serializer.errors.items():
            for error in errors:
                formatted_errors.append({
                    'field': field,
                    'message': str(error),
                    'code': 'invalid'
                })
        
        return Response(
            {
                'success': False,
                'message': 'Ma\'lumotlar noto\'g\'ri',
                'errors': formatted_errors,
                'error_count': len(formatted_errors)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response(
        {'success': True, 'message': 'Ma\'lumotlar to\'g\'ri'},
        status=status.HTTP_200_OK
    )