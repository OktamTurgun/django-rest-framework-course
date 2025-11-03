"""
Field-level Validation misollari
=================================

Bu faylda har bir field uchun alohida validation
qanday qilinishini ko'rsatamiz.
"""

from rest_framework import serializers
from datetime import date

# ============================================
# 1. ODDIY FIELD VALIDATION
# ============================================

class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=100)
    isbn = serializers.CharField(max_length=13)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    published_date = serializers.DateField()
    
    def validate_title(self, value):
        """
        Title validation:
        - Kamida 3 ta belgi
        - Bosh harf bilan boshlanishi
        """
        if len(value) < 3:
            raise serializers.ValidationError(
                "Kitob nomi kamida 3 ta belgidan iborat bo'lishi kerak"
            )
        
        if not value[0].isupper():
            raise serializers.ValidationError(
                "Kitob nomi bosh harf bilan boshlanishi kerak"
            )
        
        return value
    
    def validate_author(self, value):
        """
        Author validation:
        - Kamida 2 ta so'z (ism va familiya)
        - Har bir so'z bosh harf bilan
        """
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
    
    def validate_isbn(self, value):
        """
        ISBN validation:
        - 10 yoki 13 ta belgi
        - Faqat raqamlar
        """
        if len(value) not in [10, 13]:
            raise serializers.ValidationError(
                "ISBN 10 yoki 13 ta belgidan iborat bo'lishi kerak"
            )
        
        if not value.isdigit():
            raise serializers.ValidationError(
                "ISBN faqat raqamlardan iborat bo'lishi kerak"
            )
        
        return value
    
    def validate_price(self, value):
        """
        Price validation:
        - Musbat son
        - 10$ dan kam emas
        - 10000$ dan ko'p emas
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Narx musbat son bo'lishi kerak"
            )
        
        if value < 10:
            raise serializers.ValidationError(
                "Kitob narxi kamida 10$ bo'lishi kerak"
            )
        
        if value > 10000:
            raise serializers.ValidationError(
                "Narx 10,000$ dan oshmasligi kerak"
            )
        
        return value
    
    def validate_published_date(self, value):
        """
        Published date validation:
        - Kelajakda bo'lmasligi
        - 1450-yildan keyin
        """
        if value > date.today():
            raise serializers.ValidationError(
                "Nashr sanasi kelajakda bo'lishi mumkin emas"
            )
        
        if value.year < 1450:
            raise serializers.ValidationError(
                "Nashr sanasi 1450-yildan katta bo'lishi kerak"
            )
        
        return value


# ============================================
# 2. EMAIL VA URL VALIDATION
# ============================================

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    website = serializers.URLField(required=False)
    
    def validate_name(self, value):
        """Faqat harflar va bo'shliq"""
        if not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError(
                "Ism faqat harflardan iborat bo'lishi kerak"
            )
        return value.title()  # Har bir so'zni bosh harf bilan
    
    def validate_phone(self, value):
        """
        Phone format: +998XXXXXXXXX
        """
        import re
        pattern = r'^\+998\d{9}$'
        
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak"
            )
        
        return value


# ============================================
# 3. INTEGER VA CHOICE VALIDATION
# ============================================

class ProductSerializer(serializers.Serializer):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('books', 'Books'),
        ('clothing', 'Clothing'),
    ]
    
    name = serializers.CharField(max_length=200)
    category = serializers.ChoiceField(choices=CATEGORY_CHOICES)
    quantity = serializers.IntegerField()
    rating = serializers.FloatField()
    
    def validate_quantity(self, value):
        """Quantity musbat va juft son bo'lishi kerak"""
        if value < 0:
            raise serializers.ValidationError(
                "Miqdor musbat son bo'lishi kerak"
            )
        
        if value % 2 != 0:
            raise serializers.ValidationError(
                "Miqdor juft son bo'lishi kerak"
            )
        
        return value
    
    def validate_rating(self, value):
        """Rating 0 va 5 orasida bo'lishi kerak"""
        if not (0 <= value <= 5):
            raise serializers.ValidationError(
                "Rating 0 va 5 orasida bo'lishi kerak"
            )
        
        return value


# ============================================
# ISHLATISH MISOLLARI
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("FIELD-LEVEL VALIDATION MISOLLARI")
    print("=" * 60)
    
    # ===== Test 1: To'g'ri ma'lumot =====
    print("\n1. TO'G'RI MA'LUMOT")
    print("-" * 60)
    
    book_data = {
        'title': 'Clean Code',
        'author': 'Robert Martin',
        'isbn': '9780132350884',
        'price': '45.99',
        'published_date': '2008-08-01'
    }
    
    serializer = BookSerializer(data=book_data)
    if serializer.is_valid():
        print("✅ Ma'lumotlar to'g'ri!")
        print("Validated data:", serializer.validated_data)
    else:
        print("❌ Xatolar:", serializer.errors)
    
    # ===== Test 2: Noto'g'ri title =====
    print("\n2. NOTO'G'RI TITLE (juda qisqa)")
    print("-" * 60)
    
    invalid_title = {
        'title': 'AB',  # Juda qisqa
        'author': 'John Doe',
        'isbn': '1234567890',
        'price': '25.99',
        'published_date': '2020-01-01'
    }
    
    serializer = BookSerializer(data=invalid_title)
    if not serializer.is_valid():
        print("❌ Xato topildi:")
        for field, errors in serializer.errors.items():
            print(f"  {field}: {errors[0]}")
    
    # ===== Test 3: Noto'g'ri price =====
    print("\n3. NOTO'G'RI PRICE (juda arzon)")
    print("-" * 60)
    
    invalid_price = {
        'title': 'Test Book',
        'author': 'Jane Smith',
        'isbn': '1234567890',
        'price': '5.99',  # 10$ dan kam
        'published_date': '2020-01-01'
    }
    
    serializer = BookSerializer(data=invalid_price)
    if not serializer.is_valid():
        print("❌ Xato topildi:")
        for field, errors in serializer.errors.items():
            print(f"  {field}: {errors[0]}")
    
    # ===== Test 4: Noto'g'ri ISBN =====
    print("\n4. NOTO'G'RI ISBN (noto'g'ri format)")
    print("-" * 60)
    
    invalid_isbn = {
        'title': 'Another Book',
        'author': 'Test Author',
        'isbn': '12345',  # Juda qisqa
        'price': '29.99',
        'published_date': '2020-01-01'
    }
    
    serializer = BookSerializer(data=invalid_isbn)
    if not serializer.is_valid():
        print("❌ Xato topildi:")
        for field, errors in serializer.errors.items():
            print(f"  {field}: {errors[0]}")
    
    # ===== Test 5: Contact validation =====
    print("\n5. CONTACT VALIDATION")
    print("-" * 60)
    
    contact_data = {
        'name': 'john doe',
        'email': 'john@example.com',
        'phone': '+998901234567',
        'website': 'https://example.com'
    }
    
    contact_serializer = ContactSerializer(data=contact_data)
    if contact_serializer.is_valid():
        print("✅ Contact ma'lumotlari to'g'ri!")
        print("Name (capitalized):", contact_serializer.validated_data['name'])
    else:
        print("❌ Xatolar:", contact_serializer.errors)
    
    # ===== Test 6: Product validation =====
    print("\n6. PRODUCT VALIDATION")
    print("-" * 60)
    
    product_data = {
        'name': 'Laptop',
        'category': 'electronics',
        'quantity': 10,  # Juft son
        'rating': 4.5
    }
    
    product_serializer = ProductSerializer(data=product_data)
    if product_serializer.is_valid():
        print("✅ Product ma'lumotlari to'g'ri!")
        print("Validated data:", product_serializer.validated_data)
    else:
        print("❌ Xatolar:", product_serializer.errors)
    
    print("\n" + "=" * 60)
    print("FIELD-LEVEL VALIDATION TEST TUGADI!")
    print("=" * 60)