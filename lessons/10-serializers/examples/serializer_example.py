"""
Oddiy Serializer misoli
========================

Bu faylda Serializer class'idan foydalanib,
qanday qilib ma'lumotlarni serialization va
deserialization qilish ko'rsatilgan.
"""

from rest_framework import serializers
from datetime import date

# ============================================
# 1. Oddiy Serializer (Model bilan bog'liq emas)
# ============================================

class PersonSerializer(serializers.Serializer):
    """Model bilan bog'liq bo'lmagan oddiy serializer"""
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
    email = serializers.EmailField()
    
    def validate_age(self, value):
        """Yoshni tekshirish"""
        if value < 0:
            raise serializers.ValidationError("Yosh musbat bo'lishi kerak")
        if value > 150:
            raise serializers.ValidationError("Yosh 150 dan katta bo'lishi mumkin emas")
        return value


# ============================================
# 2. Book uchun oddiy Serializer
# ============================================

class BookSerializer(serializers.Serializer):
    """Kitob uchun to'liq qo'lda yozilgan serializer"""
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    subtitle = serializers.CharField(max_length=200, required=False, allow_blank=True)
    author = serializers.CharField(max_length=100)
    isbn = serializers.CharField(max_length=13)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    published_date = serializers.DateField()
    description = serializers.CharField()
    
    # ======= Field-level validation =======
    def validate_isbn(self, value):
        """ISBN formatini tekshirish"""
        if len(value) not in [10, 13]:
            raise serializers.ValidationError(
                "ISBN 10 yoki 13 ta belgidan iborat bo'lishi kerak"
            )
        return value
    
    def validate_price(self, value):
        """Narx musbat bo'lishini tekshirish"""
        if value < 0:
            raise serializers.ValidationError("Narx musbat son bo'lishi kerak")
        if value < 10:
            raise serializers.ValidationError("Kitob narxi kamida 10$ bo'lishi kerak")
        return value
    
    # ======= Object-level validation =======
    def validate(self, data):
        """Umumiy validation"""
        if data.get('published_date') and data['published_date'] > date.today():
            raise serializers.ValidationError({
                "published_date": "Nashr sanasi kelajakda bo'lishi mumkin emas"
            })
        return data
    
    # ======= Create method =======
    def create(self, validated_data):
        """
        Yangi kitob yaratish
        Bu metodni qo'lda yozish SHART!
        """
        # Real loyihada:
        # from books.models import Book
        # return Book.objects.create(**validated_data)
        
        # Demo uchun:
        print("Yangi kitob yaratildi:", validated_data)
        return validated_data
    
    # ======= Update method =======
    def update(self, instance, validated_data):
        """
        Mavjud kitobni yangilash
        Bu metodni ham qo'lda yozish SHART!
        """
        instance['title'] = validated_data.get('title', instance.get('title'))
        instance['subtitle'] = validated_data.get('subtitle', instance.get('subtitle'))
        instance['author'] = validated_data.get('author', instance.get('author'))
        instance['isbn'] = validated_data.get('isbn', instance.get('isbn'))
        instance['price'] = validated_data.get('price', instance.get('price'))
        instance['published_date'] = validated_data.get('published_date', instance.get('published_date'))
        instance['description'] = validated_data.get('description', instance.get('description'))
        
        # Real loyihada:
        # instance.save()
        
        print("Kitob yangilandi:", instance)
        return instance


# ============================================
# 3. Login uchun Serializer (Model yo'q)
# ============================================

class LoginSerializer(serializers.Serializer):
    """
    Login uchun serializer
    Model bilan bog'liq emas, faqat ma'lumot olish uchun
    """
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    
    def validate(self, data):
        """Username va password tekshirish"""
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            raise serializers.ValidationError(
                "Username va password kiritilishi shart"
            )
        
        # Bu yerda authentication login bo'ladi
        # Real loyihada Django'ning authenticate funksiyasi ishlatiladi
        
        return data


# ============================================
# ISHLATISH MISOLLARI
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("SERIALIZER MISOLLARI")
    print("=" * 50)
    
    # ===== Misol 1: Serialization (Python -> JSON) =====
    print("\n1. SERIALIZATION (Python dict -> JSON)")
    print("-" * 50)
    
    book_data = {
        'id': 1,
        'title': 'Clean Code',
        'subtitle': 'A Handbook of Agile Software Craftsmanship',
        'author': 'Robert C. Martin',
        'isbn': '9780132350884',
        'price': '45.99',
        'published_date': '2008-08-01',
        'description': 'Great book about writing clean code'
    }
    
    serializer = BookSerializer(data=book_data)
    if serializer.is_valid():
        print("✅ Ma'lumotlar to'g'ri!")
        print("Serialized data:", serializer.validated_data)
    else:
        print("❌ Xatolik:", serializer.errors)
    
    # ===== Misol 2: Validation xatosi =====
    print("\n2. VALIDATION XATOSI")
    print("-" * 50)
    
    invalid_book = {
        'title': 'Test Book',
        'author': 'Test Author',
        'isbn': '12345',  # Noto'g'ri format
        'price': '5.99',  # 10$ dan kam
        'published_date': '2026-01-01',  # Kelajak sanasi
        'description': 'Test'
    }
    
    serializer = BookSerializer(data=invalid_book)
    if not serializer.is_valid():
        print("❌ Xatolar topildi:")
        for field, errors in serializer.errors.items():
            print(f"  - {field}: {errors[0]}")
    
    # ===== Misol 3: Person serializer =====
    print("\n3. PERSON SERIALIZER")
    print("-" * 50)
    
    person_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'age': 30,
        'email': 'john@example.com'
    }
    
    person_serializer = PersonSerializer(data=person_data)
    if person_serializer.is_valid():
        print("✅ Person ma'lumotlari to'g'ri!")
        print(person_serializer.validated_data)
    
    # ===== Misol 4: Login serializer =====
    print("\n4. LOGIN SERIALIZER")
    print("-" * 50)
    
    login_data = {
        'username': 'admin',
        'password': 'secret123'
    }
    
    login_serializer = LoginSerializer(data=login_data)
    if login_serializer.is_valid():
        print("✅ Login ma'lumotlari to'g'ri!")
        print("Username:", login_serializer.validated_data['username'])
        # Password write_only bo'lgani uchun validated_data'da ko'rinadi
    
    print("\n" + "=" * 50)
    print("Serializer misollari tugadi!")
    print("=" * 50)