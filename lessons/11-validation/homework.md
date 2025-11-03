# Uyga vazifa: Validation qoidalari

## Maqsad
Django REST Framework'da turli validation usullarini amalda qo'llash va ma'lumotlarni to'g'ri tekshirishni o'rganish.

---

## Vazifa 1: Field-level validation

### 1.1. Book modeliga validationlar qo'shish

`books/serializers.py` da `BookSerializer` yarating va quyidagi field-level validation'larni qo'shing:
```python
class BookValidationSerializer(serializers.ModelSerializer):
    
    def validate_title(self, value):
        """
        ✅ Kamida 2 ta so'zdan iborat
        ✅ Bosh harf bilan boshlanishi
        ✅ Maxsus belgilar yo'q (faqat harflar, raqamlar, :,.)
        """
        pass
    
    def validate_author(self, value):
        """
        ✅ Kamida 2 ta so'z (ism va familiya)
        ✅ Har bir so'z bosh harf bilan
        ✅ Faqat harflar va bo'shliq
        """
        pass
    
    def validate_isbn(self, value):
        """
        ✅ 10 yoki 13 ta belgidan iborat
        ✅ Faqat raqamlar (va '-' ruxsat)
        ✅ Unique bo'lishi kerak
        """
        pass
    
    def validate_price(self, value):
        """
        ✅ Musbat son
        ✅ 5$ dan kam emas
        ✅ 1000$ dan ko'p emas
        """
        pass
    
    def validate_published_date(self, value):
        """
        ✅ Kelajakda emas
        ✅ 1450-yildan keyin
        ✅ Bugundan 100 yildan ortiq emas
        """
        pass
```

### 1.2. Test qilish

Postman'da quyidagi test case'larni sinab ko'ring:

**Test 1: Noto'g'ri title**
```json
{
  "title": "Book",  // ❌ 2 ta so'z emas
  "author": "John Doe",
  "isbn": "1234567890",
  "price": 25.99,
  "published_date": "2020-01-01"
}
```

**Test 2: Noto'g'ri price**
```json
{
  "title": "Clean Code Book",
  "author": "Robert Martin",
  "isbn": "1234567890",
  "price": 2.99,  // ❌ 5$ dan kam
  "published_date": "2020-01-01"
}
```

**Test 3: To'g'ri ma'lumot**
```json
{
  "title": "Clean Code Book",
  "author": "Robert Martin",
  "isbn": "1234567890",
  "price": 45.99,
  "published_date": "2008-08-01",
  "description": "Great book"
}
```

---

## Vazifa 2: Object-level validation

### 2.1. Murakkab validation qoidalari

`validate()` metodida quyidagi qoidalarni amalga oshiring:
```python
def validate(self, data):
    """
    1. Agar discount_price mavjud bo'lsa:
       - price'dan kam bo'lishi kerak
       - Kamida 10% chegirma bo'lishi kerak
    
    2. Agar stock = 0 bo'lsa:
       - is_available = False bo'lishi kerak
    
    3. Agar is_bestseller = True bo'lsa:
       - Oxirgi 2 yil ichida chiqgan bo'lishi kerak
       - Price kamida 20$ bo'lishi kerak
    
    4. Agar pages < 50 bo'lsa:
       - category "Brochure" yoki "Pamphlet" bo'lishi kerak
    """
    pass
```

### 2.2. Test case'lar

**Test 1: Noto'g'ri discount**
```json
{
  "title": "Test Book Example",
  "author": "John Doe",
  "isbn": "1234567891",
  "price": 100,
  "discount_price": 95,  // ❌ 10% dan kam chegirma
  "published_date": "2020-01-01"
}
```

**Test 2: Stock va availability**
```json
{
  "title": "Another Test Book",
  "author": "Jane Smith",
  "isbn": "1234567892",
  "price": 50,
  "stock": 0,
  "is_available": true,  // ❌ Stock 0 bo'lsa mavjud bo'lishi mumkin emas
  "published_date": "2020-01-01"
}
```

---

## Vazifa 3: Custom validators

### 3.1. Validator funksiyalari yaratish

`books/validators.py` faylini yarating:
```python
from rest_framework import serializers
import re

def validate_isbn_format(value):
    """
    ISBN format: XXXX-XXXX-XX yoki XXXXXXXXXXXXX
    """
    pass

def validate_no_special_chars(value):
    """
    Maxsus belgilar yo'q (faqat harflar, raqamlar, bo'shliq)
    """
    pass

def validate_capitalized(value):
    """
    Har bir so'z bosh harf bilan
    """
    pass

class PriceRangeValidator:
    """
    Narx oralig'ini tekshirish
    """
    def __init__(self, min_price, max_price):
        self.min_price = min_price
        self.max_price = max_price
    
    def __call__(self, value):
        pass

class PhoneNumberValidator:
    """
    Telefon raqam formati: +998XXXXXXXXX
    """
    def __call__(self, value):
        pass
```

### 3.2. Validator'larni ishlatish
```python
from .validators import (
    validate_isbn_format,
    validate_no_special_chars,
    PriceRangeValidator,
    PhoneNumberValidator
)

class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        validators=[validate_no_special_chars]
    )
    
    isbn = serializers.CharField(
        validators=[validate_isbn_format]
    )
    
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[PriceRangeValidator(5, 1000)]
    )
    
    phone = serializers.CharField(
        required=False,
        validators=[PhoneNumberValidator()]
    )
```

---

## Vazifa 4: Built-in validators

### 4.1. Django validators ishlatish
```python
from django.core.validators import (
    RegexValidator,
    EmailValidator,
    URLValidator,
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    MaxLengthValidator
)

class AuthorSerializer(serializers.ModelSerializer):
    # Full name: faqat harflar va bo'shliq
    full_name = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]+$',
                message='Faqat harflar va bo\'shliqlar'
            ),
            MinLengthValidator(5),
            MaxLengthValidator(100)
        ]
    )
    
    # Email
    email = serializers.CharField(
        validators=[EmailValidator()]
    )
    
    # Website
    website = serializers.CharField(
        required=False,
        validators=[URLValidator()]
    )
    
    # Age: 18-100
    age = serializers.IntegerField(
        validators=[
            MinValueValidator(18),
            MaxValueValidator(100)
        ]
    )
```

### 4.2. UniqueValidator va UniqueTogetherValidator
```python
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

class BookSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Book.objects.all(),
                message='Bu ISBN allaqachon mavjud'
            )
        ]
    )
    
    class Meta:
        model = Book
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Book.objects.all(),
                fields=['title', 'author'],
                message='Bu muallif bunday nomli kitobni allaqachon yozgan'
            )
        ]
```

---

## Bonus vazifa

### Custom ValidationError handling

Validation xatolarini JSON formatda qaytarish:
```python
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    """
    Custom validation error format
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response = {
            'status': 'error',
            'code': response.status_code,
            'message': 'Validation xatolari',
            'errors': response.data
        }
        response.data = custom_response
    
    return response
```

`settings.py` ga qo'shing:
```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'books.exceptions.custom_exception_handler'
}
```

---

## Topshirish tartibi

### 1. Kod yozish
- ✅ Field-level validation
- ✅ Object-level validation
- ✅ Custom validators
- ✅ Built-in validators

### 2. Test qilish
Postman'da:
- ✅ To'g'ri ma'lumotlar
- ✅ Har bir validation uchun noto'g'ri ma'lumotlar
- ✅ Screenshot'lar oling

### 3. Git Commit
```bash
git checkout -b lesson-11-validation
git add .
git commit -m "feat: Complete lesson 11 - Validation rules"
git push origin lesson-11-validation
```

### 4. Hisobot

`HOMEWORK_REPORT.md` yarating:
```markdown
# Homework 11 Hisoboti

## Bajargan vazifalarim
- [x] Vazifa 1: Field-level validation
- [x] Vazifa 2: Object-level validation
- [x] Vazifa 3: Custom validators
- [x] Vazifa 4: Built-in validators
- [ ] Bonus: Custom exception handler

## Test natijalari

### Field-level validation
- ✅ Title validation ishladi
- ✅ Price validation ishladi
- ✅ ISBN validation ishladi


## O'rgangan narsalarim
1. Field-level vs Object-level validation farqi
2. Custom validator'lar yaratish
3. Built-in validator'lardan foydalanish
```
---

## Yordam

- [DRF Validators](https://www.django-rest-framework.org/api-guide/validators/)
- [Django Validators](https://docs.djangoproject.com/en/stable/ref/validators/)
- Oldingi darslarni qayta ko'ring
