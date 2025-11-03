# Validation Misollari

Bu papkada Django REST Framework validation'ning turli usullari ko'rsatilgan.

---

## Fayllar

### 1. `field_validation_example.py`
**Field-level validation misollari**

Ichida:
- ✅ Har bir field uchun alohida validation
- ✅ Title, author, ISBN, price validation
- ✅ Email, URL, phone validation
- ✅ Integer, choice, float validation
- ✅ 6 ta test case

**Ishlatish:**
```bash
cd examples
python field_validation_example.py
```

**Asosiy kontseptsiyalar:**
```python
def validate_<field_name>(self, value):
    if condition:
        raise serializers.ValidationError("Xato")
    return value
```

---

### 2. `object_validation_example.py`
**Object-level validation misollari**

Ichida:
- ✅ Bir nechta fieldlarni birgalikda tekshirish
- ✅ Discount price vs price
- ✅ Stock va availability
- ✅ Conditional validation (event type)
- ✅ Subscription plan qoidalari
- ✅ 5 ta test case

**Ishlatish:**
```bash
cd examples
python object_validation_example.py
```

**Asosiy kontseptsiyalar:**
```python
def validate(self, data):
    # Bir nechta fieldlarni tekshirish
    if data['field1'] > data['field2']:
        raise serializers.ValidationError({
            'field1': 'Xato xabari'
        })
    return data
```

---

### 3. `custom_validators_example.py`
**Custom validators misollari**

Ichida:
- ✅ Function-based validators
- ✅ Class-based validators
- ✅ Composite validators (PasswordStrength)
- ✅ Regex validators
- ✅ Range validators
- ✅ 6 ta test case

**Ishlatish:**
```bash
cd examples
python custom_validators_example.py
```

**Asosiy kontseptsiyalar:**
```python
# Function validator
def validate_positive(value):
    if value <= 0:
        raise ValidationError("Musbat bo'lishi kerak")

# Class validator
class RangeValidator:
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val
    
    def __call__(self, value):
        if not (self.min_val <= value <= self.max_val):
            raise ValidationError("Oraliqdan tashqari")
```

---

## Validation turlari

### 1. Field-level Validation
**Qachon ishlatish:** Bitta field tekshirish kerak bo'lganda
```python
class BookSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def validate_price(self, value):
        if value < 10:
            raise ValidationError("Kamida 10$ bo'lishi kerak")
        return value
```

**Afzalliklari:**
- ✅ Aniq va tushunarli
- ✅ Har bir field mustaqil
- ✅ Xato xabari field bilan bog'liq

---

### 2. Object-level Validation
**Qachon ishlatish:** Bir nechta fieldlar o'rtasidagi bog'liqlik
```python
def validate(self, data):
    if data['discount_price'] >= data['price']:
        raise ValidationError({
            'discount_price': 'Asl narxdan kam bo\'lishi kerak'
        })
    return data
```

**Afzalliklari:**
- ✅ Murakkab biznes logikasi
- ✅ Bir nechta fieldlarni birga tekshirish
- ✅ Conditional validation

---

### 3. Custom Validators
**Qachon ishlatish:** Qayta ishlatish kerak bo'lganda
```python
def validate_isbn(value):
    if len(value) not in [10, 13]:
        raise ValidationError("ISBN noto'g'ri")

# Serializer'da
isbn = serializers.CharField(validators=[validate_isbn])
```

**Afzalliklari:**
- ✅ Kod takrorlanmaydi
- ✅ Qayta ishlatish oson
- ✅ Test qilish oson

---

## Taqqoslash

| Tur | Murakkablik | Qayta ishlatish | Qachon ishlatish |
|-----|-------------|-----------------|------------------|
| **Field-level** | Oddiy | ❌ Yo'q | Bitta field |
| **Object-level** | O'rta | ❌ Yo'q | Bir nechta field |
| **Custom validators** | O'rta | ✅ Ha | Har yerda |

---

## 🧪 Test qilish

Har bir misolni alohida ishlatib ko'ring:
```bash
# 1. Field validation
python field_validation_example.py

# 2. Object validation
python object_validation_example.py

# 3. Custom validators
python custom_validators_example.py
```

**Kutilayotgan natija:**
- ✅ To'g'ri ma'lumotlar uchun: "Ma'lumotlar to'g'ri!"
- ❌ Noto'g'ri ma'lumotlar uchun: Xato xabarlari

---

## 💡 Best Practices

### 1. Field-level dan boshlang
```python
def validate_price(self, value):
    # Oddiy tekshiruvlar
    pass
```

### 2. Murakkab logika uchun Object-level
```python
def validate(self, data):
    # Bir nechta fieldlar o'rtasidagi bog'liqlik
    pass
```

### 3. Qayta ishlatiladigan qoidalar uchun Custom validators
```python
def validate_positive(value):
    # Har yerda ishlatish mumkin
    pass
```

### 4. Tushunarli xato xabarlari
```python
raise ValidationError("Narx 10$ dan kam bo'lmasligi kerak")
# ✅ Aniq
# ❌ "Invalid price"
```

### 5. Bir vaqtning o'zida bir narsa tekshiring
```python
# ✅ Yaxshi
def validate_price(self, value):
    if value < 10:
        raise ValidationError("Kamida 10$")
    return value

# ❌ Yomon
def validate_price(self, value):
    if value < 10 or value > 1000 or value % 5 != 0:
        raise ValidationError("...")  # Qaysi shart buzilgan?
```

---

## Qo'shimcha resurslar

- [DRF Validators](https://www.django-rest-framework.org/api-guide/validators/)
- [Django Validators](https://docs.djangoproject.com/en/stable/ref/validators/)
- [Validation Best Practices](https://www.django-rest-framework.org/api-guide/serializers/#validation)

---

## 🎓 Keyingi qadamlar

1. ✅ Har bir misolni ishlatib ko'ring
2. ✅ O'zingizning validator'laringizni yarating
3. ✅ Real loyihada qo'llang
4. ✅ Homework'ni bajaring

Omad!