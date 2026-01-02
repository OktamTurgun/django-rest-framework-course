# Homework - Lesson 32: Two-Factor Authentication

## Maqsad
Ushbu topshiriqda siz Two-Factor Authentication (2FA) tizimini o'z loyihangizga qo'shishni o'rganasiz.

---

## Topshiriq 1: TOTP (Google Authenticator) ni qo'shish ⭐⭐⭐

### Vazifa:
`library-project` loyihangizga TOTP 2FA qo'shing.

### Talablar:
1. ✅ User modeli yangilangan (two_factor_enabled, two_factor_method)
2. ✅ TOTP setup endpoint yaratilgan
3. ✅ QR code generatsiya qilish
4. ✅ TOTP verify endpoint yaratilgan
5. ✅ Backup codes yaratilgan (10 ta)

### API Endpoints:
```
POST /api/v1/users/2fa/totp/setup/
POST /api/v1/users/2fa/totp/verify-setup/
POST /api/v1/users/2fa/totp/verify/
```

### Test qilish:
1. Postman'da user login qiling
2. TOTP setup qiling
3. QR code'ni Google Authenticator ilovasida skanerlang
4. 6 xonali kodni kiriting va verify qiling
5. Backup codes saqlang

### Qabul qilish mezonlari:
- [ ] QR code to'g'ri generatsiya qilinadi
- [ ] Google Authenticator ishlab turadi
- [ ] Verify muvaffaqiyatli o'tadi
- [ ] 10 ta backup kod beriladi

---

## Topshiriq 2: Backup Codes tizimi ⭐⭐

### Vazifa:
Backup codes bilan login qilish imkoniyatini qo'shing.

### Talablar:
1. ✅ BackupCode modeli yaratilgan
2. ✅ Backup code verify endpoint
3. ✅ Backup codes regenerate endpoint
4. ✅ Ishlatilgan kodlar belgilanadi

### API Endpoints:
```
GET /api/v1/users/2fa/backup-codes/
POST /api/v1/users/2fa/backup-codes/regenerate/
POST /api/v1/users/2fa/backup-codes/verify/
```

### Test qilish:
1. TOTP setup'dan keyin backup codes oling
2. Bitta backup code bilan verify qiling
3. O'sha code qayta ishlatishga harakat qiling (xato bo'lishi kerak)
4. Yangi backup codes regenerate qiling

### Qabul qilish mezonlari:
- [ ] Backup code bir marta ishlatiladi
- [ ] Ishlatilgan code qayta ishlamaydi
- [ ] Regenerate qilganda eski kodlar o'chadi
- [ ] Qolgan kodlar soni ko'rsatiladi

---

## Topshiriq 3: SMS Verification (Bonus) ⭐⭐⭐⭐

### Vazifa:
SMS orqali 2FA qo'shing (Twilio'siz - console'ga chiqarish bilan).

### Talablar:
1. ✅ SMSVerification modeli yaratilgan
2. ✅ Telefon raqami validatsiyasi
3. ✅ 6 xonali kod generatsiyasi
4. ✅ 10 daqiqa muddati
5. ✅ SMS kod verify endpoint

### API Endpoints:
```
POST /api/v1/users/2fa/sms/setup/
POST /api/v1/users/2fa/sms/verify-setup/
```

### Test qilish:
1. Telefon raqami bilan SMS setup qiling
2. Console'dan 6 xonali kodni oling
3. Kodni verify qiling
4. 10 daqiqadan keyin eski kod ishlamaydi

### Qabul qilish mezonlari:
- [ ] Telefon raqami to'g'ri validatsiya qilinadi
- [ ] 6 xonali kod generatsiya qilinadi
- [ ] Console'da kod ko'rinadi
- [ ] 10 daqiqadan keyin kod yaroqsiz bo'ladi

---

## Topshiriq 4: 2FA Status va O'chirish ⭐

### Vazifa:
2FA holatini ko'rish va o'chirish imkoniyatini qo'shing.

### Talablar:
1. ✅ 2FA status endpoint
2. ✅ 2FA disable endpoint
3. ✅ Barcha 2FA ma'lumotlarini o'chirish

### API Endpoints:
```
GET /api/v1/users/2fa/status/
POST /api/v1/users/2fa/disable/
```

### Test qilish:
1. 2FA status'ni oling
2. 2FA'ni o'chiring
3. Barcha TOTP, SMS, backup codes o'chirilganini tekshiring

### Qabul qilish mezonlari:
- [ ] Status to'liq ma'lumot beradi
- [ ] Disable barcha 2FA ma'lumotlarini o'chiradi
- [ ] User modeli yangilanadi

---

## Topshiriq 5: Login bilan 2FA Integration (Qo'shimcha) ⭐⭐⭐⭐⭐

### Vazifa:
Mavjud login sistemangizga 2FA qo'shing.

### Talablar:
1. ✅ Login qilganda 2FA tekshiriladi
2. ✅ 2FA yoqilgan bo'lsa, kod so'raladi
3. ✅ 2FA o'tkazilmasa, token berilmaydi
4. ✅ Backup code bilan ham login qilish mumkin

### Login Flow:
```
1. POST /api/v1/users/login/
   Body: {username, password}
   Response: {message: "2FA required", temp_token: "..."}

2. POST /api/v1/users/2fa/verify/
   Body: {temp_token, token}
   Response: {token: "actual_auth_token"}
```

### Test qilish:
1. 2FA yoqilmagan user bilan login qiling (oddiy)
2. 2FA yoqilgan user bilan login qiling (2FA so'raladi)
3. TOTP kod bilan verify qiling
4. Backup code bilan ham test qiling

### Qabul qilish mezonlari:
- [ ] 2FA yoqilgan user uchun kod so'raladi
- [ ] To'g'ri kod kiritilganda token beriladi
- [ ] Noto'g'ri kod rad etiladi
- [ ] Backup code ham ishlaydi

---

## Qo'shimcha Topshiriqlar (Extra Credit)

### 1. Rate Limiting ⭐⭐⭐
- 2FA kodlarni 5 marta noto'g'ri kiritganda 15 daqiqa block qiling
- `django-ratelimit` ishlatish mumkin

### 2. Email Notification ⭐⭐
- 2FA yoqilganda email yuborish
- Yangi device'dan login bo'lganda email xabarnoma

### 3. Trusted Devices ⭐⭐⭐⭐
- 30 kun ichida 2FA so'ramaydigan trusted devices
- Device fingerprinting

### 4. Recovery Email ⭐⭐⭐
- Backup codes'ni emailga yuborish
- Authenticator yo'qolganda tiklanish

---

## Topshiriqni topshirish

### 1. GitHub Repository:
```bash
# Branch yarating
git checkout -b feature/lesson-32-homework

# Commit qiling
git add .
git commit -m "feat: Add 2FA system with TOTP, SMS and backup codes"

# Push qiling
git push origin feature/lesson-32-homework
```

### 2. Pull Request yarating:
- **Title:** `[Homework 32] Two-Factor Authentication Implementation`
- **Description:** 
  ```
  ## Qilingan ishlar
  - [ ] TOTP (Google Authenticator)
  - [ ] Backup Codes
  - [ ] SMS Verification (bonus)
  - [ ] 2FA Status
  - [ ] Login Integration (bonus)
  
  ## Test qilingan
  - Postman collection attached
  - QR codes tested with Google Authenticator
  - Backup codes verified
  
  ## Screenshots
  [QR code screenshot]
  [Postman tests screenshot]
  ```

### 3. Postman Collection:
- Export qiling va repository'ga qo'shing
- `postman/Lesson-32-2FA.postman_collection.json`

### 4. README.md:
Loyihangizda `2FA_SETUP.md` yarating:
```markdown
# Two-Factor Authentication Setup

## O'rnatish
1. pip install -r requirements.txt
2. python manage.py migrate
3. python manage.py runserver

## Ishlatish
1. User yarating
2. Login qiling
3. 2FA setup qiling
4. Google Authenticator'da skanerlang
5. Verify qiling

## Test
- Postman collection: postman/Lesson-32-2FA.postman_collection.json
```

---

## Baholash mezonlari

| Topshiriq | Ball | Talablar |
|-----------|------|----------|
| TOTP Setup | 30 | QR code, verify, backup codes |
| Backup Codes | 20 | Generate, verify, regenerate |
| SMS Verification | 20 | Setup, verify, expiration |
| Status & Disable | 10 | Status endpoint, disable |
| Login Integration | 20 | 2FA flow, token handling |
| **Jami** | **100** | |

### Qo'shimcha balllar:
- Rate limiting: +10
- Email notifications: +5
- Trusted devices: +15
- Documentation: +5

---

## Yordam resurslari

### Documentation:
- [django-otp docs](https://django-otp-official.readthedocs.io/)
- [pyotp docs](https://pyauth.github.io/pyotp/)
- [Google Authenticator](https://support.google.com/accounts/answer/1066447)

### Video tutorials:
- YouTube: "Django Two-Factor Authentication"
- YouTube: "TOTP Implementation"

### Savol-javoblar:
- Telegram guruh: @django_rest_framework_uz
- GitHub Discussions

---

## Deadline
**Topshirish muddati:** Darsdan keyingi 7 kun ichida

## Omad!

2FA - bu zamonaviy web ilovalarning muhim qismi. Ushbu topshiriqni tugatganingizdan so'ng, siz professional darajadagi xavfsizlik tizimlarini yaratishni bilasiz!