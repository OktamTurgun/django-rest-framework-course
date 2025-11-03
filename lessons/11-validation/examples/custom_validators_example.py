"""
Custom Validators misollari
============================

Bu faylda qayta ishlatish mumkin bo'lgan custom validator'lar
qanday yaratilishi va ishlatilishi ko'rsatilgan.
"""

from rest_framework import serializers
import re

# ============================================
# 1. FUNCTION-BASED VALIDATORS
# ============================================

def validate_positive(value):
    """Faqat musbat sonlar"""
    if value <= 0:
        raise serializers.ValidationError("Qiymat musbat bo'lishi kerak")

def validate_even_number(value):
    """Faqat juft sonlar"""
    if value % 2 != 0:
        raise serializers.ValidationError("Faqat juft sonlar ruxsat etiladi")

def validate_isbn_format(value):
    """ISBN formatini tekshirish: 10 yoki 13 ta raqam"""
    clean_value = value.replace('-', '').replace(' ', '')
    
    if len(clean_value) not in [10, 13]:
        raise serializers.ValidationError(
            "ISBN 10 yoki 13 ta belgidan iborat bo'lishi kerak"
        )
    
    if not clean_value.isdigit():
        raise serializers.ValidationError(
            "ISBN faqat raqamlardan iborat bo'lishi kerak"
        )

def validate_no_special_chars(value):
    """Maxsus belgilar yo'q"""
    pattern = r'^[a-zA-Z0-9\s]+$'
    if not re.match(pattern, value):
        raise serializers.ValidationError(
            "Maxsus belgilar ruxsat etilmagan"
        )

def validate_capitalized(value):
    """Har bir so'z bosh harf bilan"""
    words = value.split()
    for word in words:
        if not word[0].isupper():
            raise serializers.ValidationError(
                "Har bir so'z bosh harf bilan boshlanishi kerak"
            )

def validate_phone_uz(value):
    """O'zbekiston telefon raqami: +998XXXXXXXXX"""
    pattern = r'^\+998\d{9}$'
    if not re.match(pattern, value):
        raise serializers.ValidationError(
            "Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak"
        )


# ============================================
# 2. CLASS-BASED VALIDATORS
# ============================================

class MinValueValidator:
    """Minimal qiymat tekshirish"""
    
    def __init__(self, min_value):
        self.min_value = min_value
    
    def __call__(self, value):
        if value < self.min_value:
            raise serializers.ValidationError(
                f"Qiymat {self.min_value} dan kam bo'lmasligi kerak"
            )

class MaxValueValidator:
    """Maksimal qiymat tekshirish"""
    
    def __init__(self, max_value):
        self.max_value = max_value
    
    def __call__(self, value):
        if value > self.max_value:
            raise serializers.ValidationError(
                f"Qiymat {self.max_value} dan oshmasligi kerak"
            )

class RangeValidator:
    """Qiymat oralig'ini tekshirish"""
    
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
    
    def __call__(self, value):
        if not (self.min_value <= value <= self.max_value):
            raise serializers.ValidationError(
                f"Qiymat {self.min_value} va {self.max_value} orasida bo'lishi kerak"
            )

class LengthValidator:
    """Uzunlik oralig'ini tekshirish"""
    
    def __init__(self, min_length=None, max_length=None):
        self.min_length = min_length
        self.max_length = max_length
    
    def __call__(self, value):
        length = len(value)
        
        if self.min_length and length < self.min_length:
            raise serializers.ValidationError(
                f"Kamida {self.min_length} ta belgi bo'lishi kerak"
            )
        
        if self.max_length and length > self.max_length:
            raise serializers.ValidationError(
                f"Ko'pi bilan {self.max_length} ta belgi bo'lishi kerak"
            )

class RegexValidator:
    """Regex pattern tekshirish"""
    
    def __init__(self, pattern, message=None):
        self.pattern = pattern
        self.message = message or "Noto'g'ri format"
    
    def __call__(self, value):
        if not re.match(self.pattern, value):
            raise serializers.ValidationError(self.message)

class MultipleOfValidator:
    """Raqam biror songa qoldiqsiz bo'linishi"""
    
    def __init__(self, multiple_of):
        self.multiple_of = multiple_of
    
    def __call__(self, value):
        if value % self.multiple_of != 0:
            raise serializers.ValidationError(
                f"Qiymat {self.multiple_of} ga qoldiqsiz bo'linishi kerak"
            )


# ============================================
# 3. COMPOSITE VALIDATORS
# ============================================

class PasswordStrengthValidator:
    """
    Parol kuchliligini tekshirish:
    - Kamida 8 ta belgi
    - Kamida 1 ta katta harf
    - Kamida 1 ta kichik harf
    - Kamida 1 ta raqam
    - Kamida 1 ta maxsus belgi
    """
    
    def __init__(self, min_length=8):
        self.min_length = min_length
    
    def __call__(self, value):
        errors = []
        
        if len(value) < self.min_length:
            errors.append(f"Kamida {self.min_length} ta belgi")
        
        if not re.search(r'[A-Z]', value):
            errors.append("Kamida 1 ta katta harf")
        
        if not re.search(r'[a-z]', value):
            errors.append("Kamida 1 ta kichik harf")
        
        if not re.search(r'\d', value):
            errors.append("Kamida 1 ta raqam")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            errors.append("Kamida 1 ta maxsus belgi (!@#$...)")
        
        if errors:
            raise serializers.ValidationError(
                "Parol quyidagi talablarga javob berishi kerak: " + ", ".join(errors)
            )

class EmailDomainValidator:
    """Email domenini tekshirish"""
    
    def __init__(self, allowed_domains):
        self.allowed_domains = allowed_domains
    
    def __call__(self, value):
        domain = value.split('@')[-1]
        if domain not in self.allowed_domains:
            raise serializers.ValidationError(
                f"Faqat {', '.join(self.allowed_domains)} domenlari ruxsat etilgan"
            )

class FileExtensionValidator:
    """Fayl kengaytmasini tekshirish"""
    
    def __init__(self, allowed_extensions):
        self.allowed_extensions = [ext.lower() for ext in allowed_extensions]
    
    def __call__(self, value):
        ext = value.split('.')[-1].lower()
        if ext not in self.allowed_extensions:
            raise serializers.ValidationError(
                f"Faqat {', '.join(self.allowed_extensions)} fayllar ruxsat etilgan"
            )


# ============================================
# 4. SERIALIZER'DA ISHLATISH
# ============================================

class BookSerializer(serializers.Serializer):
    # Function-based validators
    title = serializers.CharField(
        max_length=200,
        validators=[validate_no_special_chars]
    )
    
    isbn = serializers.CharField(
        max_length=17,
        validators=[validate_isbn_format]
    )
    
    # Class-based validators
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[RangeValidator(10, 10000)]
    )
    
    pages = serializers.IntegerField(
        validators=[
            validate_positive,
            MultipleOfValidator(10)  # 10 ga bo'linishi kerak
        ]
    )
    
    stock = serializers.IntegerField(
        validators=[
            validate_positive,
            validate_even_number
        ]
    )


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=50,
        validators=[
            LengthValidator(min_length=3, max_length=50),
            RegexValidator(
                pattern=r'^[a-zA-Z0-9_]+$',
                message="Faqat harflar, raqamlar va '_' ruxsat etilgan"
            )
        ]
    )
    
    email = serializers.EmailField(
        validators=[
            EmailDomainValidator(['gmail.com', 'outlook.com', 'yahoo.com'])
        ]
    )
    
    password = serializers.CharField(
        max_length=128,
        validators=[PasswordStrengthValidator(min_length=8)]
    )
    
    phone = serializers.CharField(
        validators=[validate_phone_uz]
    )
    
    age = serializers.IntegerField(
        validators=[RangeValidator(18, 100)]
    )


class FileUploadSerializer(serializers.Serializer):
    filename = serializers.CharField(
        validators=[
            FileExtensionValidator(['pdf', 'docx', 'txt'])
        ]
    )
    
    file_size = serializers.IntegerField(
        validators=[
            MaxValueValidator(10 * 1024 * 1024)  # 10 MB
        ]
    )


# ============================================
# ISHLATISH MISOLLARI
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("CUSTOM VALIDATORS MISOLLARI")
    print("=" * 60)
    
    # ===== Test 1: Book validation =====
    print("\n1. BOOK VALIDATION - TO'G'RI")
    print("-" * 60)
    
    book_data = {
        'title': 'Clean Code Book',
        'isbn': '978-0132350884',
        'price': '45.99',
        'pages': 460,
        'stock': 20
    }
    
    serializer = BookSerializer(data=book_data)
    if serializer.is_valid():
        print("✅ Kitob ma'lumotlari to'g'ri!")
    else:
        print("❌ Xatolar:", serializer.errors)
    
    # ===== Test 2: Book validation - noto'g'ri pages =====
    print("\n2. BOOK VALIDATION - NOTO'G'RI PAGES")
    print("-" * 60)
    
    invalid_book = {
        'title': 'Test Book',
        'isbn': '1234567890',
        'price': '29.99',
        'pages': 455,  # 10 ga bo'linmaydi
        'stock': 10
    }
    
    serializer = BookSerializer(data=invalid_book)
    if not serializer.is_valid():
        print("❌ Xatolar:")
        for field, errors in serializer.errors.items():
            print(f"  {field}: {errors[0]}")
    
    # ===== Test 3: User registration - to'g'ri =====
    print("\n3. USER REGISTRATION - TO'G'RI")
    print("-" * 60)
    
    user_data = {
        'username': 'john_doe',
        'email': 'john@gmail.com',
        'password': 'SecurePass123!',
        'phone': '+998901234567',
        'age': 25
    }
    
    serializer = UserRegistrationSerializer(data=user_data)
    if serializer.is_valid():
        print("✅ Foydalanuvchi ma'lumotlari to'g'ri!")
    else:
        print("❌ Xatolar:", serializer.errors)
    
    # ===== Test 4: User registration - zaif parol =====
    print("\n4. USER REGISTRATION - ZAIF PAROL")
    print("-" * 60)
    
    weak_password = {
        'username': 'jane_smith',
        'email': 'jane@outlook.com',
        'password': 'password',  # Zaif parol
        'phone': '+998901234567',
        'age': 30
    }
    
    serializer = UserRegistrationSerializer(data=weak_password)
    if not serializer.is_valid():
        print("❌ Xatolar:")
        for field, errors in serializer.errors.items():
            print(f"  {field}: {errors[0]}")
    
    # ===== Test 5: File upload =====
    print("\n5. FILE UPLOAD")
    print("-" * 60)
    
    file_data = {
        'filename': 'document.pdf',
        'file_size': 5 * 1024 * 1024  # 5 MB
    }
    
    serializer = FileUploadSerializer(data=file_data)
    if serializer.is_valid():
        print("✅ Fayl ma'lumotlari to'g'ri!")
    else:
        print("❌ Xatolar:", serializer.errors)
    
    # ===== Test 6: File upload - noto'g'ri kengaytma =====
    print("\n6. FILE UPLOAD - NOTO'G'RI KENGAYTMA")
    print("-" * 60)
    
    invalid_file = {
        'filename': 'image.png',  # PNG ruxsat etilmagan
        'file_size': 2 * 1024 * 1024
    }
    
    serializer = FileUploadSerializer(data=invalid_file)
    if not serializer.is_valid():
        print("❌ Xatolar:")
        for field, errors in serializer.errors.items():
            print(f"  {field}: {errors[0]}")
    
    print("\n" + "=" * 60)
    print("CUSTOM VALIDATORS TEST TUGADI!")
    print("=" * 60)
    print("\n📝 Eslatma: Bu validator'larni o'z loyihalaringizda qayta ishlatishingiz mumkin!")