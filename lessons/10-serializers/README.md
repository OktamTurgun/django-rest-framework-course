# 10-dars: ModelSerializer vs Serializer

## Darsning maqsadi
Ushbu darsda biz Django REST Framework'dagi ikki asosiy serializer turini - **Serializer** va **ModelSerializer**ni o'rganamiz, ularning farqlari, afzalliklari va qachon qaysi birini ishlatish kerakligini tushunib olamiz.

---

## Mundarija
1. [Serializer nima?](#1-serializer-nima)
2. [Serializer vs ModelSerializer](#2-serializer-vs-modelserializer)
3. [Serializer bilan ishlash](#3-serializer-bilan-ishlash)
4. [ModelSerializer bilan ishlash](#4-modelserializer-bilan-ishlash)
5. [Qachon qaysi birini ishlatish kerak?](#5-qachon-qaysi-birini-ishlatish-kerak)
6. [Amaliy mashq](#6-amaliy-mashq)

---

## 1. Serializer nima?

**Serializer** - bu Python obyektlarini JSON, XML kabi formatlarga va aksincha o'girishda yordam beruvchi DRF komponentidir.

### Serializerning vazifasi:
- **Serialization**: Python obyektlarini JSON formatiga o'tkazish
- **Deserialization**: JSON ma'lumotlarini Python obyektlariga o'tkazish
- **Validation**: Ma'lumotlarni tekshirish

---

## 2. Serializer vs ModelSerializer

| Xususiyat | Serializer | ModelSerializer |
|-----------|-----------|-----------------|
| **Turi** | Oddiy serializer | Model bilan bog'liq serializer |
| **Field yozish** | Barcha fieldlarni qo'lda yozish kerak | Avtomatik model fieldlaridan oladi |
| **Meta class** | Yo'q | Meta class orqali model ko'rsatiladi |
| **Create/Update** | Qo'lda yozish kerak | Avtomatik yaratiladi (override qilish mumkin) |
| **Kod miqdori** | Ko'proq kod yozish kerak | Kamroq kod |
| **Moslashuvchanlik** | Juda moslashuvchan | Modelga bog'liq |

---

## 3. Serializer bilan ishlash

### 3.1. Oddiy Serializer yaratish
```python
# books/serializers.py
from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    subtitle = serializers.CharField(max_length=200, required=False)
    author = serializers.CharField(max_length=100)
    isbn = serializers.CharField(max_length=13)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    published_date = serializers.DateField()
    description = serializers.CharField()
    
    def create(self, validated_data):
        """Yangi kitob yaratish"""
        from books.models import Book
        return Book.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Mavjud kitobni yangilash"""
        instance.title = validated_data.get('title', instance.title)
        instance.subtitle = validated_data.get('subtitle', instance.subtitle)
        instance.author = validated_data.get('author', instance.author)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.price = validated_data.get('price', instance.price)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
```

### 3.2. Custom Validation
```python
class BookSerializer(serializers.Serializer):
    # ... fieldlar ...
    
    def validate_isbn(self, value):
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
        if 'published_date' in data:
            from datetime import date
            if data['published_date'] > date.today():
                raise serializers.ValidationError("Nashr sanasi kelajakda bo'lishi mumkin emas")
        return data
```

---

## 4. ModelSerializer bilan ishlash

### 4.1. ModelSerializer yaratish
```python
# books/serializers.py
from rest_framework import serializers
from .models import Book

class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Barcha fieldlar
        # yoki
        # fields = ['id', 'title', 'author', 'price']  # Muayyan fieldlar
        # exclude = ['created_at', 'updated_at']  # Ayrim fieldlarni chiqarib tashlash
```

### 4.2. Read-only va Write-only fieldlar
```python
class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'isbn': {'required': True},
        }
```

### 4.3. Custom fieldlar qo'shish
```python
class BookModelSerializer(serializers.ModelSerializer):
    # Qo'shimcha field
    days_since_published = serializers.SerializerMethodField()
    author_name = serializers.CharField(source='author', read_only=True)
    
    class Meta:
        model = Book
        fields = '__all__'
    
    def get_days_since_published(self, obj):
        """Nashr qilinganiga necha kun bo'lganini hisoblash"""
        from datetime import date
        delta = date.today() - obj.published_date
        return delta.days
```

### 4.4. Nested Serializers
```python
# Agar Author modeli alohida bo'lsa
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']

class BookModelSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Book
        fields = '__all__'
```

---

## 5. Qachon qaysi birini ishlatish kerak?

### Serializer ishlatish kerak:
✅ Model bilan bog'liq bo'lmagan ma'lumotlar bilan ishlashda  
✅ Bir nechta modeldan ma'lumot yig'ishda  
✅ Juda murakkab validation logikasi kerak bo'lganda  
✅ API endpoint modelga to'g'ri kelmaydiganda  
✅ To'liq nazorat kerak bo'lganda

**Misol:**
```python
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
```

### ModelSerializer ishlatish kerak:
✅ Model bilan bevosita ishlashda  
✅ CRUD operatsiyalar uchun  
✅ Tezkor ishlab chiqish kerak bo'lganda  
✅ Standart validation yetarli bo'lganda  
✅ Kod miqdorini kamaytirish uchun

**Misol:**
```python
class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```

---

## 6. Amaliy mashq

Endi amaliy qismga o'tamiz. Biz mavjud `library-project` loyihasida Serializer va ModelSerializer farqlarini amalda ko'rsatamiz.

### Loyiha tuzilishi
```
10-serializers/
├── code/
│   └── library-project/  (09-darsdan nusxa olamiz)
├── examples/
│   ├── serializer_example.py
│   └── model_serializer_example.py
├── README.md
└── homework.md
```

Amaliy qismni keyingi qadamlarda amalga oshiramiz!

---

## Xulosa

### Serializer
**Afzalliklari:**
- To'liq nazorat
- Model bilan bog'liq bo'lmagan ma'lumotlar uchun
- Murakkab logika uchun

**Kamchiliklari:**
- Ko'proq kod yozish kerak
- `create()` va `update()` metodlarini qo'lda yozish

### ModelSerializer
**Afzalliklari:**
- Kamroq kod
- Avtomatik `create()` va `update()`
- Model bilan yaxshi integratsiya

**Kamchiliklari:**
- Modelga bog'liq
- Kamroq moslashuvchan

### Tavsiya:
- Odatda **ModelSerializer** dan foydalaning
- Maxsus holatlarda **Serializer** ishlatilng
- Loyiha talab etganida ikkalasini birga ishlating

---

## Keyingi qadamlar

1.  Nazariy qismni o'qish
2.  Amaliy qismga o'tish (keyingi bo'limda)
3.  Uyga vazifani bajarish