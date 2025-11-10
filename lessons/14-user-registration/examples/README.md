# 14-dars: Misollar

Bu papkada foydalanuvchi ro'yxatdan o'tkazish bilan bog'liq misollar mavjud.

## Fayllar

### 1. registration_example.py
**Maqsad:** Registration API'ni test qilish

**Qanday ishlatish:**
```bash
# Serverni ishga tushiring
python manage.py runserver

# Boshqa terminalda
cd examples
python registration_example.py
```

**Testlar:**
- Muvaffaqiyatli ro'yxatdan o'tish
- Takroriy username
- Takroriy email
- Parollar bir xil emas
- Zaif parol
- Email yo'q

---

### 2. password_validation_example.py
**Maqsad:** Parol validatsiyasini ko'rsatish

**Qanday ishlatish:**
```bash
python password_validation_example.py
```

**Imkoniyatlar:**
- Custom parol validator
- Parol kuchliligini baholash
- Turli parollarni test qilish

**Parol talablari:**
- Minimum 8 ta belgi
- Katta harf (A-Z)
- Kichik harf (a-z)
- Raqam (0-9)
- Maxsus belgi (!@#$%^&*)

---

### 3. custom_user_example.py
**Maqsad:** User modelini kengaytirish

**Qamrab olgan mavzular:**
- UserProfile modeli
- OneToOne relationship
- Django signals
- Serializer'lar
- View'lar

**Qo'shimcha fieldlar:**
- phone_number
- bio
- birth_date
- city, country
- avatar
- website, github, linkedin

---

## Ishlatish bo'yicha maslahatlar

### 1. Testlarni ishga tushirish

```bash
# Birinchi server ishga tushishi kerak
python manage.py runserver

# Keyin testlarni ishga tushiring
python examples/registration_example.py
```

### 2. Virtual environment

Agar virtual environment ishlatmasangiz:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Kerakli paketlarni o'rnatish
pip install requests
```

### 3. Serverning ishlab turganini tekshirish

```bash
curl http://127.0.0.1:8000/
```

yoki brauzerda: `http://127.0.0.1:8000/`

---

## Kengaytirilgan misollar

### Email jo'natish (Console backend)

`settings.py` ga qo'shing:
```python
# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Custom validator ishlatish

```python
# settings.py
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'accounts.validators.CustomPasswordValidator',
    },
]
```

### Profile signal

```python
# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

---

## Tez-tez uchraydigan xatolar

### 1. Connection Error
**Xato:** `requests.exceptions.ConnectionError`

**Yechim:** Server ishlamayapti
```bash
python manage.py runserver
```

### 2. Import Error
**Xato:** `ModuleNotFoundError: No module named 'requests'`

**Yechim:** requests paketini o'rnatish
```bash
pip install requests
```

### 3. Migration Error
**Xato:** `No such table: accounts_userprofile`

**Yechim:** Migratsiyalarni bajarish
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Permission Denied
**Xato:** `403 Forbidden`

**Yechim:** View'da `permission_classes` tekshiring
```python
@permission_classes([AllowAny])
```

---

## Foydali buyruqlar

```bash
# Barcha foydalanuvchilarni ko'rish
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()

# Test foydalanuvchi yaratish
python manage.py createsuperuser

# Database'ni tozalash
python manage.py flush

# Migratsiyalarni qaytarish
python manage.py migrate accounts zero
```

---

## Keyingi qadamlar

1. Registration API'ni test qiling
2. Custom validator qo'shing
3. UserProfile modelini qo'shing
4. Email confirmation qo'shing
5. JWT authentication o'rganing (keyingi dars)

---

## Savollar?

Agar savol bo'lsa:
1. README.md fayllarini o'qing
2. Code'dagi kommentariyalarni o'qing
3. Django dokumentatsiyasiga qarang
4. Stack Overflow'da qidiring

---

**Omad!**