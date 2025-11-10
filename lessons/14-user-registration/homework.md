# 14-dars: Uy vazifasi

## Vazifa 1: Qo'shimcha ma'lumotlar bilan registratsiya

**Maqsad:** Foydalanuvchi ro'yxatdan o'tishda qo'shimcha ma'lumotlar qabul qilish.

### Talablar:
1. UserRegistrationSerializer'ga qo'shimcha fieldlar qo'shing:
   - `first_name` (majburiy)
   - `last_name` (majburiy)
   - `phone_number` (ixtiyoriy)

2. Telefon raqami uchun validator yozing:
   - Format: +998XXXXXXXXX
   - Faqat raqamlar va + belgisi

3. Test qiling va natijani screenshot bilan saqlang.

### Kutilayotgan natija:
```json
{
    "username": "johnsmith",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "phone_number": "+998901234567",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
}
```

---

## Vazifa 2: Custom parol validatori

**Maqsad:** O'zingizning parol validator'ingizni yozish.

### Talablar:
1. `accounts/validators.py` faylini yarating
2. Quyidagi shartlarni tekshiruvchi validator yozing:
   - Kamida 1 ta katta harf
   - Kamida 1 ta kichik harf
   - Kamida 1 ta raqam
   - Kamida 1 ta maxsus belgi (!@#$%^&*)
   - Username bilan o'xshamamasligi kerak

3. Validator'ni serializer'da ishlatish
4. Turli parollar bilan test qiling

### Maslahat:
```python
import re
from django.core.exceptions import ValidationError

class CustomPasswordValidator:
    def validate(self, password, user=None):
        # Sizning kodingiz
        pass
    
    def get_help_text(self):
        return "Parol talablari..."
```

---

## Vazifa 3: Email tasdiqlanishi (Confirmation)

**Maqsad:** Ro'yxatdan o'tgandan keyin emailni tasdiqlash tizimini yaratish.

### Talablar:
1. Foydalanuvchi ro'yxatdan o'tganda:
   - `is_active = False` bo'lsin
   - Tasdiqlash tokeni yaratilsin
   - Console'ga tasdiqlash havolasi chiqarilsin (email o'rniga)

2. Yangi endpoint yarating:
   - `GET /api/accounts/confirm/<token>/`
   - Token to'g'ri bo'lsa - `is_active = True`

3. Foydalanuvchi login qilishdan oldin active bo'lishi kerak

### Qadamlar:
1. `accounts/models.py` - ConfirmationToken modeli
2. `accounts/views.py` - confirm_email view
3. `accounts/urls.py` - yangi URL
4. Test qiling

### Model misoli:
```python
from django.db import models
from django.contrib.auth.models import User
import uuid

class ConfirmationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## Vazifa 4: Registration statistikasi

**Maqsad:** Ro'yxatdan o'tganlar haqida statistika.

### Talablar:
1. Yangi endpoint:
   - `GET /api/accounts/stats/`
   - Permission: `IsAdminUser`

2. Qaytariladigan ma'lumotlar:
   ```json
   {
       "total_users": 50,
       "active_users": 45,
       "inactive_users": 5,
       "today_registrations": 3,
       "this_week_registrations": 12,
       "this_month_registrations": 28
   }
   ```

3. Admin foydalanuvchi bilan test qiling

---

## Vazifa 5: Username formati validatsiyasi

**Maqsad:** Username uchun maxsus qoidalar qo'yish.

### Talablar:
1. Username:
   - 3-20 ta belgi
   - Faqat harflar, raqamlar va _ (underscore)
   - Raqam bilan boshlanmasligi kerak
   - Maxsus so'zlar (admin, root, user) ishlatilmasligi kerak

2. Validator yozing va serializer'da ishlatish
3. Test qiling

---

## Topshirish tartibi

1. **Code:**
   - Barcha fayllarni to'g'ri papkalarga joylashtiring
   - Kommentariyalar yozing

2. **Screenshots:**
   - Postman'dagi testlar
   - Admin panel'dagi yangi foydalanuvchilar
   - Console'dagi log'lar

3. **README.md:**
   - Qaysi vazifalarni bajardingiz
   - Qanday muammolarga duch keldingiz
   - Qanday yechimlar topdingiz

4. **Test natijasi:**
   - Barcha testlarni o'tkazing
   - Natijalarni JSON formatda saqlang

---

## Qo'shimcha

1. **Social Registration:**
   - Google orqali ro'yxatdan o'tish
   - OAuth2 protokoli

2. **User Profile:**
   - Alohida Profile modeli
   - Avatar yuklash imkoniyati
   - Bio, location va boshqa ma'lumotlar

3. **Registration Form Validation:**
   - Real-time validation (frontend)
   - React yoki Vue.js bilan

---

## Muhim eslatmalar

✅ Kodni tushunib yozing, copy-paste qilmang
✅ Har bir funksiyaga kommentariya yozing
✅ Xatolarni to'g'ri handle qiling
✅ Testlarni yozing va o'tkazing

❌ Parollarni ochiq ko'rinishda response'da qaytarmang
❌ Validatsiyasiz ma'lumotlarni qabul qilmang
❌ Xavfsizlikni unutmang

---

## Muddati: 3 kun

Omad!