# Dars 30: SMS va Push Bildirishnomalar

## O'quv Maqsadlari

Ushbu darsni tugatgandan so'ng, siz quyidagilarni amalga oshirishni o'rganasiz:

-  Twilio SMS xizmatini Django loyihasiga integratsiya qilish
-  Firebase Cloud Messaging (FCM) orqali push bildirishnomalarni yuborish
-  Yagona bildirishnoma boshqaruv tizimini yaratish
-  Foydalanuvchi bildirishnoma sozlamalarini boshqarish
-  Bildirishnomalar yetkazilish holatini kuzatish
-  Ko'p kanalli bildirishnomalarni test qilish
-  Bildirishnomalar uchun eng yaxshi amaliyotlarni qo'llash

---

## Mavzular

### 1. Twilio bilan SMS Integratsiyasi
- Twilio akkaunti va API konfiguratsiyasi
- SMS xizmat classini yaratish
- Telefon raqamlarini tekshirish va formatlash
- SMS shablonlari va mazmunni sozlash
- Yetkazilish holatini kuzatish va xatolarni boshqarish

### 2. Firebase bilan Push Bildirishnomalar
- Firebase loyihasini sozlash va konfiguratsiya
- Firebase Cloud Messaging (FCM) integratsiyasi
- Qurilma tokenlarini boshqarish
- Push bildirishnoma shablonlari
- Ko'p platformalarni qo'llab-quvvatlash (iOS, Android, Web)

### 3. Yagona Bildirishnoma Tizimi
- Bildirishnoma menejeri arxitekturasi
- Foydalanuvchi bildirishnoma sozlamalari
- Ko'p kanalli yetkazib berish strategiyasi
- Bildirishnomalarni loglash va kuzatish
- Tezlikni cheklash (rate limiting)

---

## Texnologiya To'plami

| Texnologiya | Maqsad | Hujjatlar |
|-------------|--------|-----------|
| **Twilio** | SMS Xizmati | [twilio.com/docs](https://www.twilio.com/docs) |
| **Firebase FCM** | Push Bildirishnomalar | [firebase.google.com/docs/cloud-messaging](https://firebase.google.com/docs/cloud-messaging) |
| **Django Signals** | Hodisalar Triggerlari | [docs.djangoproject.com](https://docs.djangoproject.com/en/stable/topics/signals/) |
| **Celery** (Ixtiyoriy) | Asinxron Vazifalar | [docs.celeryproject.org](https://docs.celeryproject.org) |

---

## Kerakli Paketlar

```bash
# Twilio SDK
pip install twilio

# Firebase Admin SDK
pip install firebase-admin

# Telefon raqamlarini tekshirish
pip install phonenumbers

# Ixtiyoriy: Asinxron ishlov berish uchun
pip install celery redis
```

---

## Loyiha Strukturasi

```
notifications/
├── __init__.py
├── apps.py
├── models.py                    # NotificationLog, DeviceToken, UserPreferences
├── serializers.py               # API serializerlar
├── views.py                     # API endpointlar
├── urls.py                      # URL marshrutlash
├── admin.py                     # Django admin
├── services/
│   ├── __init__.py
│   ├── sms_service.py          # Twilio SMS integratsiyasi
│   ├── push_service.py         # Firebase FCM integratsiyasi
│   └── notification_manager.py  # Yagona bildirishnoma xizmati
├── templates/
│   └── notifications/
│       ├── sms/
│       │   ├── welcome.txt
│       │   ├── book_borrowed.txt
│       │   └── book_reminder.txt
│       └── push/
│           └── templates.json
└── tests/
    ├── test_sms.py
    ├── test_push.py
    └── test_manager.py
```

---

## Konfiguratsiya

### Muhit O'zgaruvchilari (.env)

```env
# Twilio Konfiguratsiyasi
TWILIO_ACCOUNT_SID=sizning_account_sid
TWILIO_AUTH_TOKEN=sizning_auth_token
TWILIO_PHONE_NUMBER=+998901234567

# Firebase Konfiguratsiyasi
FIREBASE_CREDENTIALS_PATH=serviceAccountKey.json ga yo'l

# Bildirishnoma Sozlamalari
NOTIFICATIONS_ENABLED=True
SMS_ENABLED=True
PUSH_ENABLED=True
DEFAULT_COUNTRY_CODE=UZ
```

### Django Settings

```python
# library_project/settings.py

# Twilio Konfiguratsiyasi
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')

# Firebase Konfiguratsiyasi
FIREBASE_CREDENTIALS = config('FIREBASE_CREDENTIALS_PATH')

# Bildirishnoma Sozlamalari
NOTIFICATION_SETTINGS = {
    'SMS_ENABLED': config('SMS_ENABLED', default=True, cast=bool),
    'PUSH_ENABLED': config('PUSH_ENABLED', default=True, cast=bool),
    'DEFAULT_COUNTRY_CODE': config('DEFAULT_COUNTRY_CODE', default='UZ'),
}
```

---

## Amalga Oshirish Bosqichlari

### 1-Bosqich: Sozlash va Konfiguratsiya
1. Twilio akkaunti yaratish va ma'lumotlarni olish
2. Firebase loyihasini yaratish va kredensiallarni yuklab olish
3. Kerakli paketlarni o'rnatish
4. Muhit o'zgaruvchilarini sozlash
5. notifications Django app yaratish

### 2-Bosqich: SMS Integratsiyasi
1. Twilio SMS xizmatini amalga oshirish
2. SMS shablonlarini yaratish
3. Telefon raqamlarini tekshirish
4. SMS API endpointlarini yaratish
5. SMS funksionalligini test qilish

### 3-Bosqich: Push Bildirishnomalar
1. Firebase FCM xizmatini amalga oshirish
2. Qurilma token boshqaruvini yaratish
3. Push bildirishnoma shablonlarini loyihalash
4. Push API endpointlarini yaratish
5. Push funksionalligini test qilish

### 4-Bosqich: Yagona Tizim
1. Bildirishnoma menejerini yaratish
2. Foydalanuvchi sozlamalarini amalga oshirish
3. Yetkazilishni kuzatishni qo'shish
4. Mavjud signallar bilan integratsiya qilish
5. To'liq end-to-end test o'tkazish

---

## API Endpointlar

### SMS Endpointlar
```
POST   /api/notifications/sms/send/        - SMS yuborish
POST   /api/notifications/sms/test/        - Test SMS
GET    /api/notifications/sms/status/{id}/ - SMS holati
```

### Push Bildirishnoma Endpointlar
```
POST   /api/notifications/push/send/           - Push yuborish
POST   /api/notifications/push/test/           - Test push
POST   /api/notifications/devices/register/    - Qurilmani ro'yxatga olish
DELETE /api/notifications/devices/{token}/     - Qurilmani o'chirish
GET    /api/notifications/devices/             - Qurilmalar ro'yxati
```

### Foydalanuvchi Sozlamalari
```
GET    /api/notifications/preferences/     - Sozlamalarni olish
PUT    /api/notifications/preferences/     - Sozlamalarni yangilash
PATCH  /api/notifications/preferences/     - Qisman yangilash
```

### Bildirishnomalar Tarixi
```
GET    /api/notifications/history/        - Barcha bildirishnomalar
GET    /api/notifications/history/{id}/   - Bitta bildirishnoma
```

---

## Test Qilish

### Postman Kolleksiyasi
Taqdim etilgan Postman kolleksiyasini import qiling:
- SMS yuborish
- Push bildirishnoma yetkazish
- Qurilmani ro'yxatga olish
- Sozlamalarni boshqarish
- Bildirishnomalar tarixi

### Test Stsenariylari
1. Tasdiqlangan telefon raqamiga SMS yuborish
2. Ro'yxatdan o'tgan qurilmaga push yuborish
3. Bildirishnoma sozlamalarini test qilish
4. Yetkazilishni kuzatishni tekshirish
5. Xatolarni boshqarishni test qilish

---

## Xavfsizlik Masalalari

### API Kalitlari va Kredensiallar
- Hech qachon kredensiallarni Git'ga commit qilmang
- Muhit o'zgaruvchilaridan foydalaning
- Kalitlarni muntazam yangilang
- `.env` fayllaridan foydalaning

### Telefon Raqami Maxfiyligi
- Loglarda telefon raqamlarini hash qiling
- Ma'lumotlarni himoya qilish qoidalariga rioya qiling
- Opt-out mexanizmlarini amalga oshiring
- Foydalanuvchi sozlamalarini hurmat qiling

### Tezlikni Cheklash
- SMS spamning oldini oling
- Throttling'ni amalga oshiring
- Foydalanish shablonlarini monitoring qiling
- Oqilona chegaralar belgilang

---

## Xarajatlar

### Twilio SMS
- **Bepul Sinov**: $15 kredit
- **Narx**: ~$0.0075 har bir SMS uchun (mamlakatga qarab)
- **Oylik**: Foydalanuvchilar soniga qarab hisoblang
- **Optimallashtirish**: SMS'ni faqat muhim bildirishnomalar uchun ishlating

### Firebase FCM
- **Bepul Tarif**: Cheksiz xabarlar
- **Narx**: Asosiy foydalanish uchun $0
- **Cheklovlar**: Standart foydalanish uchun yo'q
- **Tavsiya**: Asosiy bildirishnoma kanali

---

## Eng Yaxshi Amaliyotlar

### Qachon Qaysi Kanalni Ishlatish

| Stsenariy | Email | SMS | Push |
|-----------|-------|-----|------|
| Foydalanuvchi Ro'yxatdan O'tish | ✅ | ✅ | ❌ |
| Kitob Olingan | ✅ | ❌ | ✅ |
| Muddati Eslatma | ✅ | ✅ | ✅ |
| Muddati O'tgan Ogohlantirish | ✅ | ✅ | ✅ |
| Yangi Kitoblar Mavjud | ✅ | ❌ | ✅ |
| Tizim Ta'mirlash | ✅ | ❌ | ✅ |

### Bildirishnoma Strategiyasi
1. **Muhim**: Email + SMS + Push
2. **Muhim**: Email + Push
3. **Ma'lumot**: Email yoki Push
4. **Marketing**: Faqat Email (rozilik bilan)

---

## Muammolarni Hal Qilish

### Keng Tarqalgan Muammolar

**SMS yuborilmayapti:**
- Twilio kredensiallarini tekshiring
- Telefon raqami formatini tekshiring
- Akkauntda kredit borligiga ishonch hosil qiling
- Twilio konsolida xatolarni ko'ring

**Push yetib bormayapti:**
- Firebase konfiguratsiyasini tekshiring
- Qurilma tokenining amal qilishini tekshiring
- Ilovada bildirishnoma ruxsatlari borligiga ishonch hosil qiling
- Firebase konsoli loglarini ko'rib chiqing

**Sozlamalar saqlanmayapti:**
- Foydalanuvchi autentifikatsiyasini tekshiring
- Model ruxsatlarini tekshiring
- Ma'lumotlar bazasi migratsiyalarini ko'rib chiqing
- Serializer validatsiyasini tekshiring

---

## Qo'shimcha Manbalar

### Rasmiy Hujjatlar
- [Twilio Python SDK](https://www.twilio.com/docs/libraries/python)
- [Firebase Admin Python SDK](https://firebase.google.com/docs/admin/setup)
- [Django Signals](https://docs.djangoproject.com/en/stable/topics/signals/)

### Qo'llanmalar
- [Twilio SMS Tezkor Boshlash](https://www.twilio.com/docs/sms/quickstart/python)
- [FCM Server Sozlash](https://firebase.google.com/docs/cloud-messaging/server)
- [Telefon Raqamini Tekshirish](https://github.com/daviddrysdale/python-phonenumbers)

### Hamjamiyat
- [Twilio Hamjamiyati](https://www.twilio.com/community)
- [Firebase Hamjamiyati](https://firebase.google.com/community)
- [Django Forum](https://forum.djangoproject.com/)

---

## Uy Vazifasi

Batafsil topshiriqlar va mashqlar uchun [homework.md](homework.md) ga qarang.

---

## Keyingi Qadamlar

Ushbu darsni tugatgandan so'ng:
1. Barcha kodni ko'rib chiqing va tushuning
2. Uy vazifalarini bajaring
3. Turli bildirishnoma stsenariylarini sinab ko'ring
4. O'z ehtiyojingiz uchun optimallashtiring
5. 31-Darsga o'ting

---

## Eslatmalar

- Twilio va Firebase kredensiallarini xavfsiz saqlang
- Productiondan oldin yaxshilab test qiling
- Bildirishnomalar yetkazilish tezligini monitoring qiling
- Foydalanuvchi sozlamalarini hurmat qiling
- SMS va push bildirishnomalar eng yaxshi amaliyotlariga amal qiling

---

**Baxtli Kodlash!**