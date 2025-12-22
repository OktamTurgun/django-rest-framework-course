# Misollar: SMS va Push Bildirishnomalar

## Umumiy Ko'rinish

Bu papkada Twilio va Firebase yordamida SMS va Push bildirishnomalarni amalga oshirish uchun amaliy kod misollari mavjud.

---

## Fayllar Tuzilishi

| Fayl | Tavsif | Asosiy Tushunchalar |
|------|--------|---------------------|
| `01-twilio-sms-basic.py` | Asosiy Twilio SMS integratsiyasi | Sozlash, SMS yuborish, xatolarni boshqarish |
| `02-twilio-sms-templates.py` | Shablonlar bilan SMS | Shablon tizimi, kontekst o'zgaruvchilari |
| `03-firebase-push-basic.py` | Asosiy Firebase FCM sozlash | Kredensiallar, push yuborish, qurilma tokenlari |
| `04-firebase-push-advanced.py` | Qo'shimcha push imkoniyatlari | Boy bildirishnomalar, mavzular, ma'lumot yuklash |
| `05-notification-manager.py` | Yagona bildirishnoma tizimi | Ko'p kanalli, sozlamalar, loglash |

---

## Tezkor Boshlash

### Talablar

```bash
# Kerakli paketlarni o'rnatish
pip install twilio
pip install firebase-admin
pip install phonenumbers
```

### Muhit O'zgaruvchilari

`.env` faylini yarating:

```env
# Twilio
TWILIO_ACCOUNT_SID=sizning_account_sid
TWILIO_AUTH_TOKEN=sizning_auth_token
TWILIO_PHONE_NUMBER=+998901234567

# Firebase
FIREBASE_CREDENTIALS_PATH=serviceAccountKey.json ga yo'l
```

---

## Misollar Tafsiloti

### 01 - Twilio SMS Asoslari
**Nima qiladi:**
- Twilio'ga ulanadi
- Oddiy SMS yuboradi
- Xatolarni boshqaradi

**Ishga tushirish:**
```bash
python 01-twilio-sms-basic.py
```

**Natija:**
```
SMS muvaffaqiyatli yuborildi!
SID: SM1234567890abcdef
Holat: queued
```

---

### 02 - Twilio SMS Shablonlari
**Nima qiladi:**
- SMS shablonlarini yaratadi
- Kontekst o'zgaruvchilaridan foydalanadi
- Xabarlarni dinamik yaratadi

**Ishga tushirish:**
```bash
python 02-twilio-sms-templates.py
```

**Natija:**
```
Xush kelibsiz SMS yuborildi: +998901234567
Eslatma SMS yuborildi: +998901234567
```

---

### 03 - Firebase Push Asoslari
**Nima qiladi:**
- Firebase Admin SDK'ni ishga tushiradi
- Push bildirishnoma yuboradi
- Qurilma tokenlarini boshqaradi

**Ishga tushirish:**
```bash
python 03-firebase-push-basic.py
```

**Natija:**
```
Bildirishnoma muvaffaqiyatli yuborildi!
Xabar ID: projects/123/messages/abc
```

---

### 04 - Firebase Push Qo'shimcha
**Nima qiladi:**
- Rasm bilan boy bildirishnomalar
- Mavzuga asoslangan xabarlar
- Ma'lumot yuklamalari
- Platformaga xos konfiguratsiyalar

**Ishga tushirish:**
```bash
python 04-firebase-push-advanced.py
```

**Natija:**
```
Boy bildirishnoma yuborildi!
Mavzu bildirishnomasi yuborildi!
Ma'lumot xabari yuborildi!
```

---

### 05 - Bildirishnoma Menejeri
**Nima qiladi:**
- Barcha kanallar uchun yagona interfeys
- Foydalanuvchi sozlamalarini boshqarish
- Yetkazilishni kuzatish
- Xatolarni boshqarish

**Ishga tushirish:**
```bash
python 05-notification-manager.py
```

**Natija:**
```
Bildirishnoma yuborildi: email, sms, push
Yetkazilish holati: 
  Email: ✓ Yuborildi
  SMS: ✓ Yuborildi
  Push: ✓ Yuborildi
```

---

## Konfiguratsiya

### Twilio Sozlash

1. [twilio.com](https://www.twilio.com/try-twilio) da ro'yxatdan o'ting
2. Account SID va Auth Token oling
3. Telefon raqamini oling
4. `.env` fayliga qo'shing

### Firebase Sozlash

1. [console.firebase.google.com](https://console.firebase.google.com/) da loyiha yarating
2. Project Settings → Service Accounts ga o'ting
3. Yangi private key yarating
4. `serviceAccountKey.json` sifatida saqlang
5. Yo'lni `.env` fayliga qo'shing

---

## Test Qilish

### SMS Test
```bash
# Tasdiqlangan raqamingizga yuboring
python 01-twilio-sms-basic.py
# Telefoningizda SMS ni tekshiring
```

### Push Test
```bash
# Avval qurilma tokeni kerak
# Mobil ilovangizdan oling
python 03-firebase-push-basic.py
# Qurilmangizda bildirishnomani tekshiring
```

---

## Muammolarni Hal Qilish

### SMS olinmadi
- Twilio konsoli loglarini tekshiring
- Telefon raqami formatini tekshiring (+[mamlakat][raqam])
- Akkauntda kredit borligiga ishonch hosil qiling
- Raqam tasdiqlangan ekanligini tekshiring (sinov akkauntlari)

### Push yetib bormadi
- Qurilma tokeni amal qilishini tekshiring
- Firebase konsoli loglarini ko'ring
- Ilovada bildirishnoma ruxsatlari borligiga ishonch hosil qiling
- Kredensial fayl yo'lini tekshiring

---

## Maslahatlar

1. **Asosiy misollardan boshlang** - Avval asoslarni tushuning
2. **Muhit o'zgaruvchilaridan foydalaning** - Hech qachon kredensiallarni hardcode qilmang
3. **Bosqichma-bosqich test qiling** - Misollarni birin-ketin ishga tushiring
4. **Xato xabarlarini o'qing** - Ular foydali!
5. **Rasmiy hujjatlarni tekshiring** - Batafsil ma'lumot uchun

---

## Manbalar

- [Twilio Python SDK Hujjatlari](https://www.twilio.com/docs/libraries/python)
- [Firebase Admin Python SDK](https://firebase.google.com/docs/admin/setup)
- [Telefon Raqamlari Kutubxonasi](https://github.com/daviddrysdale/python-phonenumbers)

---

## O'rganish Tekshiruv Ro'yxati

Barcha misollarni ishga tushirgandan so'ng, siz quyidagilarni tushunishingiz kerak:

- [ ] Twilio bilan SMS qanday yuboriladi
- [ ] SMS shablonlari qanday ishlatiladi
- [ ] Firebase Admin SDK qanday ishga tushiriladi
- [ ] Push bildirishnomalar qanday yuboriladi
- [ ] Qurilma tokenlari qanday boshqariladi
- [ ] Boy bildirishnomalar qanday yuboriladi
- [ ] Yagona bildirishnoma tizimi qanday yaratiladi
- [ ] Xatolar qanday boshqariladi

---

## Keyingi Qadamlar

1. Barcha misollarni ishga tushiring
2. Misollarni o'z ma'lumotlaringiz bilan o'zgartiring
3. Django loyihasiga integratsiya qiling
4. Bildirishnoma menejerini yarating
5. Foydalanuvchi sozlamalarini qo'shing
6. Yaxshilab test qiling

---

**Baxtli O'rganish!**