# 14-dars: Foydalanuvchi ro'yxatdan o'tkazish (User Registration)

## Dars maqsadi
Ushbu darsda siz Django REST Framework'da foydalanuvchilarni ro'yxatdan o'tkazish (registration) tizimini yaratishni o'rganasiz.

## O'rganadigan mavzular

### 1. User Registration asoslari
- Yangi foydalanuvchi yaratish
- Parol xavfsizligi
- Email va username validatsiyasi
- Ma'lumotlarni saqlash

### 2. Serializer yaratish
- UserSerializer yaratish
- Parol xeshlanishi (hashing)
- Parol tasdiqlash (confirm password)
- Read-only va write-only fieldlar

### 3. Registration API endpoint
- POST /api/accounts/register/
- Foydalanuvchi ma'lumotlarini qabul qilish
- Validatsiya qilish
- Response qaytarish

### 4. Parol validatsiyasi
- Minimum uzunlik tekshirish
- Murakkablik tekshirish (raqam, harf, maxsus belglar)
- Parol va tasdiq paroli bir xilligini tekshirish

### 5. Email va Username validatsiyasi
- Unique email tekshirish
- Unique username tekshirish
- Email formati tekshirish

## Amaliy qism

### Loyihaga kerakli o'zgarishlar

1. **accounts/serializers.py** - Yangi fayl yaratish
2. **accounts/views.py** - Registration view qo'shish
3. **accounts/urls.py** - Registration URL qo'shish
4. **library_project/settings.py** - Parol validatorlarini sozlash

### API Endpoints

```
POST /api/accounts/register/
```

**Request body:**
```json
{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
}
```

**Response (201 Created):**
```json
{
    "id": 3,
    "username": "newuser",
    "email": "newuser@example.com",
    "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi"
}
```

**Response (400 Bad Request):**
```json
{
    "username": ["Bu username allaqachon mavjud."],
    "email": ["Bu email allaqachon ro'yxatdan o'tgan."],
    "password": ["Parollar bir xil emas."]
}
```

## Testlash

### Postman orqali test
1. POST so'rovi yuborish
2. Body -> raw -> JSON
3. Ma'lumotlarni kiritish va yuborish

### cURL orqali test
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "password2": "TestPass123!"
  }'
```

### Python requests orqali test
```python
import requests

url = "http://127.0.0.1:8000/api/accounts/register/"
data = {
    "username": "pythonuser",
    "email": "python@example.com",
    "password": "PythonPass123!",
    "password2": "PythonPass123!"
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
```

## Xavfsizlik

### 1. Parol xeshlash
Django avtomatik ravishda parollarni PBKDF2 algoritmi bilan xeshlaydi.

### 2. Parol talablari
- Minimum 8 ta belgi
- Kamida 1 ta raqam
- Kamida 1 ta katta harf
- Kamida 1 ta kichik harf

### 3. Ma'lumotlarni himoyalash
- Parollar hech qachon ochiq ko'rinishda saqlanmaydi
- Email uniquelikni tekshirish
- CSRF himoyasi

## Kengaytirish imkoniyatlari

1. **Email tasdiqlanishi**
   - Email orqali tasdiqlash havolasi yuborish
   - Faollashtirish tokeni yaratish

2. **Qo'shimcha ma'lumotlar**
   - Ism, familiya
   - Telefon raqami
   - Avatar rasmi

3. **Social Authentication**
   - Google orqali kirish
   - Facebook orqali kirish
   - GitHub orqali kirish

## Keyingi dars
15-dars: JWT Authentication - Token-based authentication tizimi

## Foydali resurslar
- [Django User Model](https://docs.djangoproject.com/en/5.0/ref/contrib/auth/)
- [DRF Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [Password Validation](https://docs.djangoproject.com/en/5.0/topics/auth/passwords/)