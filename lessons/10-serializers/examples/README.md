# Serializer Misollari

Bu papkada Serializer va ModelSerializer'larning amaliy misollari joylashgan.

---

## Fayllar

### 1. `serializer_example.py`
**Oddiy Serializer misollari**

Ichida:
- ✅ Oddiy Serializer (Model bilan bog'liq emas)
- ✅ Book uchun to'liq qo'lda yozilgan Serializer
- ✅ Login Serializer (authentication uchun)
- ✅ Field-level validation
- ✅ Object-level validation
- ✅ Custom create() va update() metodlari

**Ishlatish:**
```bash
cd examples
python serializer_example.py
```

---

### 2. `model_serializer_example.py`
**ModelSerializer misollari**

Ichida:
- ✅ Oddiy ModelSerializer
- ✅ Muayyan fieldlar bilan
- ✅ Read-only fieldlar
- ✅ Extra kwargs
- ✅ SerializerMethodField
- ✅ Custom validation
- ✅ Nested Serializers
- ✅ Multiple serializers bitta model uchun

**Ishlatish:**
```bash
cd examples
python model_serializer_example.py
```

---

## Asosiy farqlar

### Serializer
```python
class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def create(self, validated_data):
        return Book.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance
```

**Xususiyatlari:**
- ❌ Barcha fieldlarni qo'lda yozish
- ❌ create() va update() yozish shart
- ✅ To'liq nazorat
- ✅ Model bilan bog'liq bo'lmagan ma'lumotlar uchun

---

### ModelSerializer
```python
class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```

**Xususiyatlari:**
- ✅ Avtomatik fieldlar
- ✅ Avtomatik create() va update()
- ✅ Kamroq kod
- ✅ Model bilan yaxshi integratsiya

---

## Qachon qaysi birini ishlatish?

### Serializer ishlatish kerak:
```python
# ✅ Login (model yo'q)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

# ✅ Bir nechta modeldan ma'lumot
class DashboardSerializer(serializers.Serializer):
    total_books = serializers.IntegerField()
    total_authors = serializers.IntegerField()
    recent_books = BookSerializer(many=True)
```

### ModelSerializer ishlatish kerak:
```python
# ✅ CRUD operatsiyalar
class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

# ✅ Model bilan bevosita ishlash
class AuthorSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books_count']
```

---

## Maslahatlar

1. **Ko'p hollarda ModelSerializer ishlatiladi**
   - Tezroq development
   - Kamroq kod
   - Kamroq xatolar

2. **Maxsus hollarda Serializer**
   - Model yo'q
   - Murakkab logika
   - Bir nechta modeldan ma'lumot

3. **Ikkalasini birga ishlatish mumkin**
```python
   class BookListSerializer(serializers.ModelSerializer):
       # List uchun sodda
       class Meta:
           model = Book
           fields = ['id', 'title', 'price']
   
   class BookDetailSerializer(serializers.ModelSerializer):
       # Detail uchun to'liq
       author = AuthorSerializer()
       class Meta:
           model = Book
           fields = '__all__'
```

---

## O'rganish uchun

1. `serializer_example.py` ni o'qing va ishlatib ko'ring
2. `model_serializer_example.py` ni o'qing va taqqoslang
3. Real loyihada ikkalasini ham sinab ko'ring
4. Homework'ni bajaring

---

## Qo'shimcha resurslar

- [DRF Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [ModelSerializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer)
- [Validation](https://www.django-rest-framework.org/api-guide/validators/)