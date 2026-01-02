# Two-Factor Authentication - Examples

Bu papkada 2FA (Two-Factor Authentication) tizimini tushunish uchun amaliy misollar mavjud.

## Misollar ro'yxati

### 1. `01-totp-basic-example.py` ⭐
**Mavzu:** TOTP asoslari va pyotp bilan ishlash

**O'rganasiz:**
- TOTP nima va qanday ishlaydi
- pyotp kutubxonasi
- Secret key generatsiya
- Token yaratish va tekshirish

**Ishga tushirish:**
```bash
python 01-totp-basic-example.py
```

---

### 2. `02-qr-code-generation.py` ⭐⭐
**Mavzu:** QR code generatsiya qilish

**O'rganasiz:**
- QR code nima uchun kerak
- qrcode kutubxonasi
- OTP URI yaratish
- QR code'ni PNG fayl sifatida saqlash
- Base64 encoding

**Ishga tushirish:**
```bash
python 02-qr-code-generation.py
```

**Natija:** `qr_code.png` fayl yaratiladi

---

### 3. `03-backup-codes-generator.py` ⭐
**Mavzu:** Backup kodlar generatsiya

**O'rganasiz:**
- Xavfsiz tasodifiy kodlar yaratish
- secrets moduli
- Unique kodlar generatsiya
- Kod formatini belgilash

**Ishga tushirish:**
```bash
python 03-backup-codes-generator.py
```

---

### 4. `04-sms-code-generator.py` ⭐
**Mavzu:** SMS verifikatsiya kodlari

**O'rganasiz:**
- 6 xonali kod generatsiya
- Telefon raqam validatsiya
- Kod muddati (expiration)
- SMS kod formati

**Ishga tushirish:**
```bash
python 04-sms-code-generator.py
```

---

### 5. `05-complete-2fa-flow.py` ⭐⭐⭐
**Mavzu:** To'liq 2FA jarayoni simulyatsiyasi

**O'rganasiz:**
- TOTP setup jarayoni
- QR code skanerlash simulyatsiyasi
- Token verifikatsiya
- Backup codes bilan login
- Error handling

**Ishga tushirish:**
```bash
python 05-complete-2fa-flow.py
```

---

## Barcha misollarni ishlatish

### 1. Virtual environment yarating (pipenv)

```bash
# Papkaga kiring
cd examples

# Pipenv orqali dependencies o'rnating
pipenv install pyotp qrcode pillow phonenumbers

# Virtual environment'ga kiring
pipenv shell
```

### 2. Misollarni ishga tushiring

```bash
# Birma-bir ishga tushiring
python 01-totp-basic-example.py
python 02-qr-code-generation.py
python 03-backup-codes-generator.py
python 04-sms-code-generator.py
python 05-complete-2fa-flow.py
```

---

## Kerakli kutubxonalar

```txt
pyotp==2.9.0
qrcode==7.4.2
Pillow==10.1.0
phonenumbers==8.13.27
```

### O'rnatish:

**pipenv bilan:**
```bash
pipenv install pyotp qrcode pillow phonenumbers
```

**pip bilan:**
```bash
pip install pyotp qrcode pillow phonenumbers
```

---

## Har bir misol uchun maqsad

| Fayl | Qiyinlik | Vaqt | Maqsad |
|------|----------|------|--------|
| 01-totp-basic-example.py | ⭐ | 10 min | TOTP asoslari |
| 02-qr-code-generation.py | ⭐⭐ | 15 min | QR code yaratish |
| 03-backup-codes-generator.py | ⭐ | 10 min | Backup kodlar |
| 04-sms-code-generator.py | ⭐ | 10 min | SMS kodlar |
| 05-complete-2fa-flow.py | ⭐⭐⭐ | 20 min | To'liq jarayon |

---

## Misollardan keyin

Ushbu misollarni o'rganganingizdan so'ng:

1.  TOTP qanday ishlashini tushunasiz
2.  QR code generatsiya qila olasiz
3.  Xavfsiz backup kodlar yaratishni bilasiz
4.  SMS verifikatsiya tizimini tushunasiz
5.  To'liq 2FA flow'ni amalga oshirishga tayyorsiz

**Keyingi qadam:** `code/library-project` da amaliy implementatsiya!

---

## 🔍 Qo'shimcha resurslar

### TOTP haqida:
- [RFC 6238 - TOTP Specification](https://tools.ietf.org/html/rfc6238)
- [How TOTP Works](https://www.freecodecamp.org/news/how-time-based-one-time-passwords-work-and-why-you-should-use-them-in-your-app-fdd2b9ed43c3/)

### QR Code haqida:
- [QR Code Wikipedia](https://en.wikipedia.org/wiki/QR_code)
- [Python qrcode docs](https://github.com/lincolnloop/python-qrcode)

### Security best practices:
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [2FA Best Practices](https://authy.com/blog/security-best-practices-for-two-factor-authentication/)

---

## ❓ Savol-javoblar

**Q: TOTP va HOTP o'rtasidagi farq nima?**
A: TOTP - time-based (vaqtga bog'liq), HOTP - counter-based (hisoblagichga bog'liq)

**Q: QR code nima uchun kerak?**
A: Foydalanuvchi uchun oson - telefon bilan skanerlaydi va secret key avtomatik qo'shiladi

**Q: Backup kodlar nechta bo'lishi kerak?**
A: Odatda 10 ta. Har birini faqat 1 marta ishlatish mumkin.

**Q: SMS kodning muddati qancha?**
A: Odatda 5-10 daqiqa. Xavfsizlik uchun qisqa bo'lishi kerak.

---

## 🎓 O'rganish yo'lxaritasi

```
1. 01-totp-basic-example.py
   ↓
2. 02-qr-code-generation.py
   ↓
3. 03-backup-codes-generator.py
   ↓
4. 04-sms-code-generator.py
   ↓
5. 05-complete-2fa-flow.py
   ↓
6. library-project da amaliy qo'llash
```

---

**Omad! Happy Coding!**