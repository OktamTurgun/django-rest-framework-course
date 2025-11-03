# 11-dars: Validation qoidalari

## Darsning maqsadi
Django REST Framework'da ma'lumotlarni tekshirishning turli usullarini o'rganish: field-level validation, object-level validation, custom validators va built-in validators.

---

## Mundarija
1. [Validation nima?](#1-validation-nima)
2. [Field-level validation](#2-field-level-validation)
3. [Object-level validation](#3-object-level-validation)
4. [Custom validators](#4-custom-validators)
5. [Built-in validators](#5-built-in-validators)
6. [UniqueValidator va UniqueTogetherValidator](#6-uniquevalidator-va-uniquetogethervalidator)
7. [ValidationError bilan ishlash](#7-validationerror-bilan-ishlash)
8. [Amaliy mashq](#8-amaliy-mashq)

---

## 1. Validation nima?

**Validation** - bu foydalanuvchidan kelgan ma'lumotlarni tekshirish va noto'g'ri ma'lumotlarni rad etish jarayoni.

### Validationning maqsadi:
- ✅ Ma'lumotlar bazasiga noto'g'ri ma'lumot kirmasligi
- ✅ Biznes logikasi qoidalariga rioya qilish
- ✅ Xavfsizlikni ta'minlash
- ✅ Foydalanuvchiga tushunarli xato xabarlari berish

### Validation darajlari (tartib bo'yicha):
```python
1. Field type validation (CharField, IntegerField)
   ↓
2. Field-level validation (validate_<field_name>)
   ↓
3. Validators (RegexValidator, EmailValidator)
   ↓
4. Object-level validation (validate method)
   ↓
5. Model validation (Model.clean)
```

---

## 2. Field-level validation

Field-level validation - har bir field uchun alohida tekshirish.

### 2.1. Sintaksis
```python
def validate_<field_name>(self, value):
    """
    Field uchun validation
    'value' - field qiymati
    """
    if condition:
        raise serializers.ValidationError("Xato xabari")
    return value
```

### 2.2. Misollar
```python
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    
    def validate_title(self, value):
        """Title kamida 3 ta belgidan iborat bo'lishi kerak"""
        if len(value) < 3:
            raise serializers.ValidationError(
                "Kitob nomi kamida 3 ta belgidan iborat bo'lishi kerak"
            )
        return value
    
    def validate_isbn(self, value):
        """ISBN 10 yoki 13 ta belgidan iborat"""
        if len(value) not in [10, 13]:
            raise serializers.ValidationError(
                "ISBN 10 yoki 13 ta belgidan iborat bo'lishi kerak"
            )
        
        # Faqat raqamlardan iborat
        if not value.isdigit():
            raise serializers.ValidationError(
                "ISBN faqat raqamlardan iborat bo'lishi kerak"
            )
        
        return value
    
    def validate_price(self, value):
        """Narx musbat va 10$ dan kam bo'lmasligi kerak"""
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
        """Nashr sanasi kelajakda bo'lmasligi kerak"""
        from datetime import date
        
        if value > date.today():
            raise serializers.ValidationError(
                "Nashr sanasi kelajakda bo'lishi mumkin emas"
            )
        
        # Juda eski sana emas
        if value.year < 1450:  # Gutenberg 1450-yilda bosmaxona ixtiro qilgan
            raise serializers.ValidationError(
                "Nashr sanasi 1450-yildan katta bo'lishi kerak"
            )
        
        return value
```

### 2.3. Afzalliklari va kamchiliklari

**✅ Afzalliklari:**
- Har bir field mustaqil tekshiriladi
- Aniq va tushunarli
- Qayta ishlatish oson

**❌ Kamchiliklari:**
- Bir nechta fieldlar o'rtasidagi bog'liqlikni tekshira olmaydi
- Har bir field uchun alohida metod yozish kerak

---

## 3. Object-level validation

Object-level validation - barcha fieldlarni birgalikda tekshirish.

### 3.1. Sintaksis
```python
def validate(self, data):
    """
    Barcha fieldlarni tekshirish
    'data' - validated_data (dictionary)
    """
    if condition:
        raise serializers.ValidationError({
            'field_name': 'Xato xabari',
            'another_field': 'Boshqa xato'
        })
    return data
```

### 3.2. Misollar
```python
class BookSerializer(serializers.ModelSerializer):
    
    def validate(self, data):
        """Object-level validation"""
        
        # 1. Ikki field o'rtasidagi bog'liqlik
        if data.get('discount_price') and data.get('price'):
            if data['discount_price'] >= data['price']:
                raise serializers.ValidationError({
                    'discount_price': 'Chegirma narxi asl narxdan kam bo\'lishi kerak'
                })
        
        # 2. Bir nechta shartlar
        published_date = data.get('published_date')
        is_bestseller = data.get('is_bestseller', False)
        
        if is_bestseller and published_date:
            from datetime import date, timedelta
            # Bestseller faqat oxirgi 2 yil ichida chiqgan kitoblar bo'lishi mumkin
            two_years_ago = date.today() - timedelta(days=730)
            if published_date < two_years_ago:
                raise serializers.ValidationError({
                    'is_bestseller': 'Faqat oxirgi 2 yil ichida chiqgan kitoblar bestseller bo\'lishi mumkin'
                })
        
        # 3. Business logic
        if data.get('status') == 'published' and not data.get('isbn'):
            raise serializers.ValidationError({
                'isbn': 'Nashr qilingan kitoblarda ISBN bo\'lishi shart'
            })
        
        return data
```

### 3.3. Qachon ishlatish kerak?

**Object-level validation ishlatish kerak:**
- ✅ Bir nechta fieldlar o'rtasidagi bog'liqlik
- ✅ Murakkab biznes logikasi
- ✅ Conditional validation (shartli tekshirish)
- ✅ Bir fieldning qiymati boshqa fieldga bog'liq

---

## 4. Custom validators

Custom validators - qayta ishlatish mumkin bo'lgan validator funksiyalari.

### 4.1. Oddiy validator funksiyasi
```python
from rest_framework import serializers

def validate_even_number(value):
    """Faqat juft sonlar"""
    if value % 2 != 0:
        raise serializers.ValidationError("Faqat juft sonlar ruxsat etiladi")

def validate_positive(value):
    """Faqat musbat sonlar"""
    if value <= 0:
        raise serializers.ValidationError("Musbat son bo'lishi kerak")

def validate_isbn_format(value):
    """ISBN formatini tekshirish"""
    if len(value) not in [10, 13]:
        raise serializers.ValidationError(
            "ISBN 10 yoki 13 ta belgidan iborat bo'lishi kerak"
        )
    if not value.isdigit():
        raise serializers.ValidationError(
            "ISBN faqat raqamlardan iborat bo'lishi kerak"
        )
```

### 4.2. Class-based validators
```python
class MinValueValidator:
    """Minimum qiymat validator"""
    
    def __init__(self, min_value):
        self.min_value = min_value
    
    def __call__(self, value):
        if value < self.min_value:
            raise serializers.ValidationError(
                f"Qiymat {self.min_value} dan kam bo'lmasligi kerak"
            )

class MaxValueValidator:
    """Maximum qiymat validator"""
    
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
```

### 4.3. Validator'larni ishlatish
```python
class BookSerializer(serializers.ModelSerializer):
    # Function-based validators
    isbn = serializers.CharField(
        max_length=13,
        validators=[validate_isbn_format]
    )
    
    # Class-based validators
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            RangeValidator(10, 10000)
        ]
    )
    
    stock = serializers.IntegerField(
        validators=[
            validate_positive,
            validate_even_number
        ]
    )
    
    class Meta:
        model = Book
        fields = '__all__'
```

---

## 5. Built-in validators

DRF'da tayyor validator'lar mavjud.

### 5.1. RegexValidator
```python
from django.core.validators import RegexValidator

class BookSerializer(serializers.ModelSerializer):
    # Faqat harflar va bo'shliq
    title = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]+$',
                message='Faqat harflar va bo\'shliqlar ruxsat etiladi'
            )
        ]
    )
    
    # Phone number format
    phone = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+998\d{9}$',
                message='Telefon raqam +998XXXXXXXXX formatida bo\'lishi kerak'
            )
        ]
    )
```

### 5.2. EmailValidator
```python
from django.core.validators import EmailValidator

email = serializers.CharField(
    validators=[EmailValidator(message='Email noto\'g\'ri formatda')]
)
```

### 5.3. URLValidator
```python
from django.core.validators import URLValidator

website = serializers.CharField(
    validators=[URLValidator(message='URL noto\'g\'ri formatda')]
)
```

### 5.4. MinValueValidator, MaxValueValidator
```python
from django.core.validators import MinValueValidator, MaxValueValidator

price = serializers.DecimalField(
    max_digits=10,
    decimal_places=2,
    validators=[
        MinValueValidator(10),
        MaxValueValidator(10000)
    ]
)
```

### 5.5. MinLengthValidator, MaxLengthValidator
```python
from django.core.validators import MinLengthValidator, MaxLengthValidator

title = serializers.CharField(
    validators=[
        MinLengthValidator(3, message='Kamida 3 ta belgi'),
        MaxLengthValidator(200, message='Ko\'pi bilan 200 ta belgi')
    ]
)
```

---

## 6. UniqueValidator va UniqueTogetherValidator

### 6.1. UniqueValidator

Bir field qiymati unique bo'lishi uchun.
```python
from rest_framework.validators import UniqueValidator

class BookSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(
        max_length=13,
        validators=[
            UniqueValidator(
                queryset=Book.objects.all(),
                message='Bu ISBN allaqachon mavjud'
            )
        ]
    )
```

### 6.2. UniqueTogetherValidator

Bir nechta fieldlar birgalikda unique bo'lishi uchun.
```python
from rest_framework.validators import UniqueTogetherValidator

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Book.objects.all(),
                fields=['title', 'author'],
                message='Bu muallif tomonidan bunday nomli kitob allaqachon mavjud'
            )
        ]
```

---

## 7. ValidationError bilan ishlash

### 7.1. Oddiy xato
```python
raise serializers.ValidationError("Bu field xato")
```

### 7.2. Bir nechta xato (dict)
```python
raise serializers.ValidationError({
    'title': 'Kitob nomi xato',
    'price': 'Narx xato',
    'isbn': 'ISBN formati noto\'g\'ri'
})
```

### 7.3. List xatolar
```python
raise serializers.ValidationError([
    'Birinchi xato',
    'Ikkinchi xato'
])
```

### 7.4. Non-field errors
```python
raise serializers.ValidationError({
    'non_field_errors': ['Umumiy xato xabari']
})
```

---

## 8. Amaliy mashq

Keling, barcha validation turlarini amalda ko'rsatamiz!

### 8.1. To'liq misol
```python
from rest_framework import serializers
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from rest_framework.validators import UniqueValidator
from datetime import date, timedelta
from .models import Book

# Custom validators
def validate_isbn_format(value):
    """ISBN formatini tekshirish"""
    if len(value) not in [10, 13]:
        raise serializers.ValidationError(
            "ISBN 10 yoki 13 ta belgidan iborat bo'lishi kerak"
        )
    if not value.replace('-', '').isdigit():
        raise serializers.ValidationError(
            "ISBN faqat raqamlar va '-' dan iborat bo'lishi kerak"
        )

class PriceRangeValidator:
    """Narx oralig'ini tekshirish"""
    def __init__(self, min_price, max_price):
        self.min_price = min_price
        self.max_price = max_price
    
    def __call__(self, value):
        if not (self.min_price <= value <= self.max_price):
            raise serializers.ValidationError(
                f"Narx {self.min_price}$ va {self.max_price}$ orasida bo'lishi kerak"
            )


class BookSerializer(serializers.ModelSerializer):
    # Field validators
    title = serializers.CharField(
        max_length=200,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\s\-:,\.]+$',
                message='Faqat harflar, raqamlar va asosiy belgilar'
            )
        ]
    )
    
    isbn = serializers.CharField(
        max_length=17,  # 13 + 4 ta '-'
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
        validators=[PriceRangeValidator(10, 10000)]
    )
    
    class Meta:
        model = Book
        fields = '__all__'
    
    # Field-level validation
    def validate_title(self, value):
        """Title kamida 3 ta so'zdan iborat"""
        words = value.split()
        if len(words) < 2:
            raise serializers.ValidationError(
                "Kitob nomi kamida 2 ta so'zdan iborat bo'lishi kerak"
            )
        return value.title()  # Har bir so'zni bosh harf bilan
    
    def validate_published_date(self, value):
        """Nashr sanasi kelajakda bo'lmasligi kerak"""
        if value > date.today():
            raise serializers.ValidationError(
                "Nashr sanasi kelajakda bo'lishi mumkin emas"
            )
        
        if value.year < 1450:
            raise serializers.ValidationError(
                "Nashr sanasi 1450-yildan katta bo'lishi kerak"
            )
        
        return value
    
    # Object-level validation
    def validate(self, data):
        """Barcha fieldlarni tekshirish"""
        
        # 1. Discount price tekshirish
        if 'discount_price' in data and 'price' in data:
            if data['discount_price'] >= data['price']:
                raise serializers.ValidationError({
                    'discount_price': 'Chegirma narxi asl narxdan kam bo\'lishi kerak'
                })
        
        # 2. Stock va availability
        stock = data.get('stock', 0)
        is_available = data.get('is_available', False)
        
        if is_available and stock == 0:
            raise serializers.ValidationError({
                'is_available': 'Omborda yo\'q kitob mavjud deb belgilanishi mumkin emas'
            })
        
        # 3. Bestseller qoidalari
        is_bestseller = data.get('is_bestseller', False)
        published_date = data.get('published_date')
        
        if is_bestseller and published_date:
            two_years_ago = date.today() - timedelta(days=730)
            if published_date < two_years_ago:
                raise serializers.ValidationError({
                    'is_bestseller': 'Faqat oxirgi 2 yil ichida chiqgan kitoblar bestseller bo\'lishi mumkin'
                })
        
        return data
```

### Keyingi qadamlarda amaliy kod yozamiz!

---

## Xulosa

### Validation turlari

| Tur | Qachon ishlatish | Afzallik |
|-----|-----------------|----------|
| **Field-level** | Bitta field tekshirish | Sodda, aniq |
| **Object-level** | Bir nechta field birga | Murakkab logika |
| **Custom validators** | Qayta ishlatish kerak | Kod takrorlanmaydi |
| **Built-in validators** | Standart tekshiruvlar | Tayyor, ishonchli |

### Best practices

1. ✅ **Field-level** dan boshlang
2. ✅ **Built-in validators** ni afzal ko'ring
3. ✅ **Custom validators** yaratib qayta ishlating
4. ✅ **Object-level** da murakkab logika
5. ✅ Tushunarli xato xabarlari yozing
6. ✅ Validation'larni test qiling

---

## Keyingi dars
**12-dars: Autentifikatsiya turlari** - Token, Session, JWT authentication