# Uy Vazifasi: 30-Dars - SMS va Push Bildirishnomalari

## Maqsadlar

Amaliy topshiriqlarni bajarish orqali SMS va Push bildirishnoma tizimlarini qo'llashni mashq qiling.

---

## 1-Topshiriq: SMS Xizmati Amalga Oshirish

### Vazifa
Twilio yordamida to'liq SMS bildirishnoma tizimini amalga oshiring.

### Talablar
1. Twilio hisobi yarating va hisob ma'lumotlarini oling
2. Xato boshqaruvi bilan SMS xizmat klassini amalga oshiring
3. Telefon raqami tekshiruvini qo'shing
4. Quyidagi uchun SMS shablonlarini yarating:
   - Xush kelibsiz xabari
   - Kitob olinganligini tasdiqlash
   - Qaytarish sanasi eslatmasi
   - Muddati o'tgan bildirishnoma
5. O'z telefon raqamingiz bilan test qiling

### Topshiriladigan Materiallar
- `notifications/services/sms_service.py`
- `templates/notifications/sms/` da SMS shablonlari
- Test natijalari skrinshoti
- Twilio konsoli skrinshoti

### Qabul Qilish Mezonlari
-  SMS telefoningizga muvaffaqiyatli yuborildi
-  To'g'ri xato boshqaruvi amalga oshirilgan
-  Telefon raqamlari to'g'ri tekshirilgan
-  Shablonlar kontekst ma'lumotlari bilan ishlaydi
-  Yetkazib berish holati kuzatilgan

---

## 2-Topshiriq: FCM bilan Push Bildirishnomalari

### Vazifa
Push bildirishnomalari uchun Firebase Cloud Messaging'ni amalga oshiring.

### Talablar
1. Firebase loyiha yarating
2. Xizmat hisobi hisob ma'lumotlarini yuklab oling
3. FCM xizmat klassini amalga oshiring
4. Qurilma token boshqaruvini yarating
5. Push bildirishnoma shablonlarini loyihalang
6. Firebase konsoli bilan test qiling

### Topshiriladigan Materiallar
- `notifications/services/push_service.py`
- `notifications/models.py` (DeviceToken modeli)
- Push shablonlari sozlamasi
- Test natijalari skrinshoti
- Firebase konsoli skrinshoti

### Qabul Qilish Mezonlari
-  Push bildirishnomalar muvaffaqiyatli yuborildi
-  Qurilma tokenlari saqlangan va boshqarilmoqda
-  Bir nechta qurilmalar qo'llab-quvvatlanadi
-  Rasm/harakatlar bilan boy bildirishnomalar
-  Firebase konsolida yetkazib berish tasdiqlangan

---

## 3-Topshiriq: Yagona Bildirishnoma Boshqaruvchisi

### Vazifa
Email, SMS va Push bildirishnomalarini boshqaradigan yagona tizim yarating.

### Talablar
1. NotificationManager klassini yarating
2. Foydalanuvchi sozlamalari tizimini amalga oshiring
3. Bildirishnoma jurnali qo'shing
4. Bir vaqtda bir nechta kanallarni qo'llab-quvvatlang
5. Muvaffaqiyatsizliklarni to'g'ri boshqaring

### Topshiriladigan Materiallar
- `notifications/services/notification_manager.py`
- `notifications/models.py` (UserPreferences, NotificationLog)
- Sozlamalar uchun API endpointlar
- To'liq test to'plami

### Qabul Qilish Mezonlari
-  Bitta usul barcha kanallarga yuboradi
-  Foydalanuvchi sozlamalariga rioya qilinadi
-  Barcha bildirishnomalar jurnalga yozilgan
-  Muvaffaqiyatsiz bildirishnomalar qayta urinish
-  API endpointlar ishlaydi

---

## 4-Topshiriq: Signal Integratsiyasi

### Vazifa
Bildirishnomalarni mavjud Django signallari bilan birlashtiring.

### Talablar
1. Foydalanuvchi ro'yxatdan o'tganda xush kelibsiz SMS yuboring
2. Kitob olinganda push bildirishnoma yuboring
3. Qaytarish sanasidan 1 kun oldin SMS eslatma yuboring
4. Muddati o'tganda uchala turini yuboring
5. Foydalanuvchi sozlamalariga rioya qiling

### Topshiriladigan Materiallar
- Yangilangan `accounts/signals.py`
- Yangilangan `books/signals.py`
- Signal test holatlari
- Integratsiya test natijalari

### Qabul Qilish Mezonlari
-  Signallar bildirishnomalarni avtomatik ishga tushiradi
-  Barcha bildirishnoma turlari ishlaydi
-  Signal ishlovchilarida xato yo'q
-  Asinxron ishlov berish (agar Celery ishlatilsa)
-  Har tomonlama jurnal yozish

---

## 5-Topshiriq: API Endpointlar va Test

### Vazifa
Bildirishnoma boshqaruvi uchun RESTful API endpointlarini yarating.

### Talablar
1. Barcha bildirishnoma endpointlarini amalga oshiring
2. Autentifikatsiya va ruxsatlarni qo'shing
3. Postman to'plamini yarating
4. Barcha stsenariylarni test qiling
5. API javoblarini hujjatlashtiring

### Topshiriladigan Materiallar
- `notifications/views.py` - Barcha viewlar
- `notifications/urls.py` - URL sozlamasi
- `notifications/serializers.py` - Serializatorlar
- Postman to'plami (JSON eksport)
- API hujjatlari

### Test Ssenariylari
- [ ] Test SMS yuboring
- [ ] Test push bildirishnomasi yuboring
- [ ] Qurilma tokenini ro'yxatdan o'tkazing
- [ ] Foydalanuvchi sozlamalarini yangilang
- [ ] Bildirishnoma tarixini oling
- [ ] Xato holatlarini test qiling

### Qabul Qilish Mezonlari
-  Barcha endpointlar to'g'ri javoblar qaytaradi
-  Autentifikatsiya ishlaydi
-  Tekshirish amalga oshirilgan
-  Xato boshqaruvi to'liq
-  Postman testlari o'tadi

---

## Bonus 1-Topshiriq: Ilg'or Xususiyatlar

### Vazifa
Ilg'or bildirishnoma xususiyatlarini amalga oshiring.

### Talablar
1. **Rejalashtirilgan Bildirishnomalar**
   - Kelajakda yetkazib berish uchun bildirishnomalarni rejalashtirish
   - Rejalashtirilgan bildirishnomalarni bekor qilish
   - Kutayotgan bildirishnomalar ro'yxati

2. **Bildirishnoma Shablonlari**
   - Shablonlar uchun admin interfeysi
   - Shablon o'zgaruvchilari qo'llab-quvvatlashi
   - Oldindan ko'rish funksiyasi

3. **Tahlillar Dashboardi**
   - Yetkazib berish darajasini kuzatish
   - Kanal samaradorligini solishtirish
   - Xarajat tahlili

### Topshiriladigan Materiallar
- Rejalashtirilgan bildirishnoma tizimi
- Shablon boshqaruvi interfeysi
- Tahlil viewlari va diagrammalari

---

## Bonus 2-Topshiriq: Ko'p Til Qo'llab-Quvvatlashi

### Vazifa
Bildirishnomalar uchun ko'p til qo'llab-quvvatlashini qo'shing.

### Talablar
1. Bildirishnomalar uchun i18n ni amalga oshiring
2. O'zbek va Ingliz tillarini qo'llab-quvvatlang
3. Foydalanuvchi til sozlamalari
4. Avtomatik aniqlash

### Topshiriladigan Materiallar
- Tarjima qilingan shablonlar
- Til aniqlash mantiq
- Foydalanuvchi sozlamalari boshqaruvi

---

## Bonus 3-Topshiriq: Bildirishnoma Kanallari

### Vazifa
Qo'shimcha bildirishnoma kanallarini qo'shing.

### Talablar
1. **Telegram Bot Integratsiyasi**
   - Telegram orqali bildirishnomalar yuborish
   - Bot bilan foydalanuvchi ro'yxatdan o'tishi
   - Buyruq ishlov berish

2. **WhatsApp Business API**
   - WhatsApp xabar shablonlari
   - Xabar yetkazib berish kuzatuvi

3. **Slack Integratsiyasi**
   - Slack'ga admin bildirishnomalari
   - Tizim ogohlantirishlari
   - Xato hisoboti

### Topshiriladigan Materiallar
- Qo'shimcha xizmat klasslari
- Kanal sozlamasi
- Test natijalari

---

## Baholash Shkalasi

| Topshiriq | Ball | Talablar |
|-----------|------|----------|
| 1-Topshiriq | 20 | SMS xizmati ishlaydi |
| 2-Topshiriq | 20 | Push bildirishnomalar ishlaydi |
| 3-Topshiriq | 20 | Yagona boshqaruvchi to'liq |
| 4-Topshiriq | 20 | Signallar birlashtirilgan |
| 5-Topshiriq | 20 | API to'liq funksional |
| **Jami** | **100** | **Barcha asosiy topshiriqlar** |
| Bonus 1 | +10 | Ilg'or xususiyatlar |
| Bonus 2 | +5 | Ko'p til |
| Bonus 3 | +10 | Qo'shimcha kanallar |
| **Maksimal Jami** | **125** | **Barcha bonuslar bilan** |

---

## Topshirish Qoidalari

### Nima Topshirish Kerak
1. **Kod**
   - To'liq notifications ilovasi
   - Barcha xizmat klasslari
   - Modellar va migratsiyalar
   - Viewlar va serializatorlar
   - URL sozlamasi

2. **Hujjatlar**
   - O'rnatish ko'rsatmalari
   - Sozlash qo'llanmasi
   - API hujjatlari
   - Test natijalari

3. **Testlar**
   - Unit testlar
   - Integratsiya testlari
   - Postman to'plami
   - Test qamrovi hisoboti

4. **Skrinshotlar**
   - Telefonda olingan SMS
   - Qurilmada push bildirishnoma
   - Twilio konsoli
   - Firebase konsoli
   - Postman test natijalari
   - Admin interfeysi

### Format
- GitHub repozitoriya havolasi
- Batafsil tavsifli Pull Request
- O'rnatish ko'rsatmalari bilan README
- Video demo (ixtiyoriy lekin tavsiya etiladi)

### Muddat
- Dars tugaganidan 1 hafta ichida topshiring
- Kerak bo'lsa muddatni uzaytirish so'rang

---

## O'rganish Natijalari

Bu uy vazifasini tugatgandan so'ng, siz:

-  Twilio SMS integratsiyasini o'zlashtirasiz
-  Firebase Cloud Messaging'ni tushunasiz
-  Kengaytiriladigan bildirishnoma tizimlari yaratasiz
-  Foydalanuvchi sozlamalarini boshqarasiz
-  Bildirishnoma yetkazilishini kuzatasiz
-  Har tomonlama testlar yozasiz
-  API'larni professional hujjatlashtirasiz
-  Sanoat eng yaxshi amaliyotlariga amal qilasiz

---

## Muvaffaqiyat uchun Maslahatlar

1. **Oddiydan Boshlang**
   - Avval oddiy SMS'ni ishga tushiring
   - Keyin push bildirishnomalarni qo'shing
   - Nihoyat tizimni birlashtiring

2. **Tez-tez Test Qiling**
   - Har bir xususiyatdan keyin test qiling
   - API test uchun Postman'dan foydalaning
   - Test natijalarini yozib boring

3. **Xatolarni Boshqaring**
   - To'g'ri xato boshqaruvini amalga oshiring
   - Barcha xatolarni jurnalga yozing
   - Mazmunli xato xabarlarini taqdim eting

4. **Eng Yaxshi Amaliyotlarga Amal Qiling**
   - Hisob ma'lumotlarini xavfsiz saqlang
   - Toza kod yozing
   - Docstringlar qo'shing
   - DRF konvensiyalariga amal qiling

5. **Yordam So'rang**
   - Rasmiy hujjatlardan foydalaning
   - Jamiyat forumlarini tekshiring
   - O'qituvchiga savollar bering
   - Tengdoshlar bilan hamkorlik qiling

---

## Qo'shimcha Resurslar

### Twilio
- [SMS Eng Yaxshi Amaliyotlar](https://www.twilio.com/docs/sms/best-practices)
- [Xato Kodlari](https://www.twilio.com/docs/api/errors)
- [Python SDK Qo'llanmasi](https://www.twilio.com/docs/libraries/python)

### Firebase
- [FCM Qo'llanmasi](https://firebase.google.com/docs/cloud-messaging)
- [Server Amalga Oshirish](https://firebase.google.com/docs/cloud-messaging/server)
- [Eng Yaxshi Amaliyotlar](https://firebase.google.com/docs/cloud-messaging/concept-options)

### Django
- [Signallar Ma'lumotnomasi](https://docs.djangoproject.com/en/stable/ref/signals/)
- [Model Eng Yaxshi Amaliyotlar](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Test Qo'llanmasi](https://docs.djangoproject.com/en/stable/topics/testing/)

---

## O'z-O'zini Baholash Tekshiruv Ro'yxati

Topshirishdan oldin, quyidagilarni tekshiring:

### Asosiy Funksionallik
- [ ] Twilio SMS integratsiyasi ishlaydi
- [ ] Firebase FCM integratsiyasi ishlaydi
- [ ] Yagona bildirishnoma boshqaruvchisi amalga oshirilgan
- [ ] Foydalanuvchi sozlamalari tizimi to'liq
- [ ] Bildirishnoma jurnali faol
- [ ] Signal integratsiyasi ishlaydi
- [ ] API endpointlar funksional
- [ ] Autentifikatsiya amalga oshirilgan
- [ ] Xato boshqaruvi har tomonlama
- [ ] Testlar o'tmoqda

### Kod Sifati
- [ ] Kod toza va o'qilishi oson
- [ ] Funksiyalarda docstringlar bor
- [ ] O'zgaruvchilar yaxshi nomlangan
- [ ] Qattiq kodlangan hisob ma'lumotlari yo'q
- [ ] PEP 8 uslubiga amal qilingan
- [ ] DRY tamoyili qo'llanilgan
- [ ] SOLID tamoyillariga amal qilingan

### Hujjatlashtirish
- [ ] README to'liq
- [ ] API hujjatlashtirilgan
- [ ] O'rnatish ko'rsatmalari aniq
- [ ] Sozlash tushuntirilgan
- [ ] Misollar keltirilgan

### Test
- [ ] Unit testlar yozilgan
- [ ] Integratsiya testlari to'liq
- [ ] Postman to'plami yaratilgan
- [ ] Barcha testlar o'tmoqda
- [ ] Chekka holatlar qamrab olingan

---

## Qo'shimcha Kredit Imkoniyatlari

1. **Samaradorlik Optimizatsiyasi** (+5 ball)
   - Asinxron ishlov berish uchun Celery'ni amalga oshiring
   - Redis keshlashni qo'shing
   - Ma'lumotlar bazasi so'rovlarini optimallashtiring

2. **Xavfsizlik Yaxshilashlari** (+5 ball)
   - Tezlik cheklash
   - So'rov tekshiruvi
   - Audit jurnali

3. **Monitoring va Ogohlantirish** (+5 ball)
   - Sentry integratsiyasi
   - Yetkazib berish darajasi monitoringi
   - Xarajat kuzatuvi

---

**Omad!**

Esda tuting: Maqsad shunchaki tugatish emas, o'rganish. Vaqt ajrating, har bir tushunchani tushuning va faxrlanadigan narsa yarating!