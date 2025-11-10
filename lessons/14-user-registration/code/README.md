# 14-dars: Code - Foydalanuvchi ro'yxatdan o'tkazish

## Loyiha strukturasi

```
library-project/
├── accounts/                    # Foydalanuvchi boshqaruvi
│   ├── serializers.py          # User serializer'lar (YANGI)
│   ├── views.py                # Registration view'lar (YANGILANDI)
│   ├── urls.py                 # Registration URL'lar (YANGILANDI)
│   └── ...
├── books/                      # Kitoblar app'i
├── library_project/            # Asosiy sozlamalar
│   ├── settings.py             # Parol validatorlar
│   └── urls.py
└── manage.py
```

## O'zgarishlar

### 1. Yangi fayllar
- `accounts/serializers.py` - User serializer'lar

### 2. Yangilangan fayllar
- `accounts/views.py` - register_user view qo'shildi
- `accounts/urls.py` - register URL qo'shildi

## Qadamba-qadam qo'llanma

### QADAM 1: Serializers yaratish

`accounts/serializers.py` faylini yarating:

```python
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {'email': {'required': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Parollar bir xil emas."
            })
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Bu email allaqachon ro'yxatdan o'tgan."
            )
        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
```

### QADAM 2: Views yangilash

`accounts/views.py` ga qo'shing:

```python
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'message': 'Foydalanuvchi muvaffaqiyatli ro\'yxatdan o\'tdi'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### QADAM 3: URLs yangilash

`accounts/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
]
```

### QADAM 4: Serverni ishga tushirish

```bash
# Virtual environment faollashtirish
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Serverni ishga tushirish
python manage.py runserver
```

## Test qilish

### 1. Postman orqali

**URL:** `POST http://127.0.0.1:8000/api/accounts/register/`

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "password2": "TestPass123!"
}
```

**Expected Response (201):**
```json
{
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    },
    "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi"
}
```

### 2. cURL orqali

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "curluser",
    "email": "curl@example.com",
    "password": "CurlPass123!",
    "password2": "CurlPass123!"
  }'
```

### 3. Python script orqali

```bash
cd ..
python examples/registration_example.py
```

## Xatolarni bartaraf etish

### Xato 1: "This field is required"

**Sabab:** Majburiy field yuborilmagan

**Yechim:** Barcha majburiy fieldlarni yuboring:
- username
- email
- password
- password2

### Xato 2: "Parollar bir xil emas"

**Sabab:** password va password2 bir xil emas

**Yechim:** Parollarni bir xil qiling

### Xato 3: "Bu email allaqachon ro'yxatdan o'tgan"

**Sabab:** Email allaqachon mavjud

**Yechim:** Boshqa email kiriting yoki avvalgi foydalanuvchini o'chiring

### Xato 4: "This password is too short"

**Sabab:** Parol 8 ta belgidan kam

**Yechim:** Kamida 8 ta belgili parol kiriting

## Parol talablari

Django'ning default parol validatorlari:

1. **UserAttributeSimilarityValidator** - Username bilan o'xshamamasligi
2. **MinimumLengthValidator** - Minimum 8 ta belgi
3. **CommonPasswordValidator** - Umumiy parollar (123456, password) rad qilinadi
4. **NumericPasswordValidator** - Faqat raqamlardan iborat bo'lmasligi

## Database'ni ko'rish

```bash
# Django shell
python manage.py shell

# Barcha foydalanuvchilar
>>> from django.contrib.auth.models import User
>>> User.objects.all()

# Oxirgi foydalanuvchi
>>> User.objects.last()

# Email bo'yicha qidirish
>>> User.objects.filter(email='test@example.com')

# Foydalanuvchini o'chirish
>>> User.objects.filter(username='testuser').delete()
```

## Admin panel

```bash
# Superuser yaratish
python manage.py createsuperuser

# Server ishga tushirish
python manage.py runserver

# Browser'da
http://127.0.0.1:8000/admin/
```

Admin panel orqali:
- Foydalanuvchilarni ko'rish
- Tahrirlash
- O'chirish
- Yangi foydalanuvchi qo'shish

## Keyingi qadamlar

1. Registration'ni test qiling
2. Homework'ni bajaring
3. Keyingi dars: JWT Authentication
4. Email confirmation (qo'shimcha)
5. User profile (qo'shimcha)

## Foydali resurslar

- [Django Auth Documentation](https://docs.djangoproject.com/en/5.0/topics/auth/)
- [DRF Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [Password Validation](https://docs.djangoproject.com/en/5.0/topics/auth/passwords/)

---

**Muammoga duch keldingizmi?**
1. README.md'ni qaytadan o'qing
2. Xato xabarlarini diqqat bilan o'qing
3. Code'dagi kommentariyalarni tekshiring
4. Examples papkasidagi misollarni ko'ring