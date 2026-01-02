"""
TOTP (Time-based One-Time Password) Basic Example

Bu misolda:
- TOTP nima ekanligini o'rganamiz
- pyotp kutubxonasi bilan tanishamiz
- Secret key yaratamiz
- Token generatsiya qilamiz va tekshiramiz
"""

import pyotp
import time

print("=" * 60)
print("TOTP Basic Example")
print("=" * 60)

# ==================== 1. Secret Key Yaratish ====================
print("\n1. SECRET KEY YARATISH")
print("-" * 60)

# Tasodifiy secret key generatsiya qilish (Base32 format)
secret_key = pyotp.random_base32()
print(f"Secret Key: {secret_key}")
print(f"Secret Key uzunligi: {len(secret_key)} belgi")
print(f"\n💡 Bu secret keyni DATABASE'da saqlaymiz!")

# ==================== 2. TOTP Object Yaratish ====================
print("\n\n2. TOTP OBJECT YARATISH")
print("-" * 60)

# TOTP object yaratish
totp = pyotp.TOTP(secret_key)
print(f"TOTP Object yaratildi: {totp}")
print(f"TOTP Interval: {totp.interval} sekund (standart 30)")
print(f"TOTP Digits: {totp.digits} xonali (standart 6)")

# ==================== 3. Token Generatsiya ====================
print("\n\n3. TOKEN GENERATSIYA")
print("-" * 60)

# Hozirgi vaqt uchun token
current_token = totp.now()
print(f"Hozirgi token: {current_token}")
print(f"Token turi: {type(current_token)}")
print(f"\n💡 Bu token Google Authenticator'da ko'rsatiladi!")
print(f"💡 Token har 30 sekundda yangilanadi!")

# ==================== 4. Token Verification ====================
print("\n\n4. TOKEN VERIFICATION")
print("-" * 60)

# To'g'ri token tekshirish
is_valid = totp.verify(current_token)
print(f"Token tekshiruvi: {is_valid}")

# Noto'g'ri token
fake_token = "123456"
is_valid_fake = totp.verify(fake_token)
print(f"Fake token tekshiruvi: {is_valid_fake}")

# ==================== 5. Time Window ====================
print("\n\n5. TIME WINDOW")
print("-" * 60)

print("TOTP time window tushunchasi:")
print("- valid_window=0: Faqat hozirgi token")
print("- valid_window=1: Oldingi, hozirgi, keyingi token (90 sekund)")
print("- valid_window=2: 5 ta token (150 sekund)")

# Oldingi tokenni tekshirish (1 window orqada)
print(f"\nHozirgi token: {current_token}")
is_valid_with_window = totp.verify(current_token, valid_window=1)
print(f"1 window bilan: {is_valid_with_window}")

# ==================== 6. Vaqt bilan Token O'zgarishi ====================
print("\n\n6. VAQT BILAN TOKEN O'ZGARISHI")
print("-" * 60)

print("Har 30 sekundda yangi token:")
print("(5 sekund kutamiz va tokenni qayta tekshiramiz)\n")

old_token = totp.now()
print(f"Boshlang'ich token: {old_token}")

# 5 sekund kutish
for i in range(5):
    time.sleep(1)
    new_token = totp.now()
    if new_token != old_token:
        print(f"✅ Token o'zgardi! Yangi token: {new_token}")
        break
    print(f"  {i+1} sekund... Token hali: {new_token}")

# ==================== 7. Provisioning URI ====================
print("\n\n7. PROVISIONING URI")
print("-" * 60)

# URI yaratish (QR code uchun)
uri = totp.provisioning_uri(
    name="user@example.com",
    issuer_name="My App"
)
print(f"Provisioning URI:")
print(f"{uri}\n")
print("💡 Bu URI QR code ga aylantiriladi!")
print("💡 Google Authenticator bu QR code'ni skanerlaydi!")

# ==================== 8. Multiple Tokens ====================
print("\n\n8. MULTIPLE TOKENS (Bir nechta vaqt uchun)")
print("-" * 60)

print("Turli vaqtlar uchun tokenlar:\n")

# Hozirgi vaqtdan 30 sekund oldin
past_token = totp.at(time.time() - 30)
print(f"30 sekund oldin: {past_token}")

# Hozirgi vaqt
current = totp.now()
print(f"Hozirgi vaqt:    {current}")

# 30 sekund keyin
future_token = totp.at(time.time() + 30)
print(f"30 sekund keyin: {future_token}")

# ==================== 9. Real Use Case ====================
print("\n\n9. REAL USE CASE - Login Flow")
print("-" * 60)

def simulate_2fa_login():
    """2FA login jarayonini simulyatsiya qilish"""
    
    print("\n--- User Registration ---")
    # 1. User registratsiya qilganda secret key yaratamiz
    user_secret = pyotp.random_base32()
    print(f"1. Secret key yaratildi: {user_secret}")
    print(f"2. Secret key DATABASE'ga saqlandi ✓")
    
    # 2. User Google Authenticator'ga qo'shadi
    user_totp = pyotp.TOTP(user_secret)
    qr_uri = user_totp.provisioning_uri("user@example.com", "MyApp")
    print(f"3. QR code URI yaratildi")
    print(f"4. User Google Authenticator'da skanerladi ✓\n")
    
    print("--- User Login ---")
    # 3. User login qilayotganda
    print("1. User username va password kiritdi ✓")
    print("2. Sistema 2FA kod so'rayapti...")
    
    # 4. User Google Authenticator'dan kodni oladi
    current_code = user_totp.now()
    print(f"3. User Google Authenticator'dan kodni ko'rdi: {current_code}")
    
    # 5. User kodni kiritadi va sistema tekshiradi
    user_input = current_code  # Real holatda user kiritadi
    is_verified = user_totp.verify(user_input, valid_window=1)
    
    if is_verified:
        print(f"4. Kod to'g'ri! ✅")
        print(f"5. User tizimga kirdi! 🎉")
    else:
        print(f"4. Kod noto'g'ri! ❌")
        print(f"5. Kirish rad etildi!")

simulate_2fa_login()

# ==================== 10. Xulosa ====================
print("\n\n" + "=" * 60)
print("XULOSA")
print("=" * 60)

print("""
✅ TOTP - Time-based One-Time Password
✅ Har 30 sekundda yangi 6 xonali kod
✅ Secret key - DATABASE'da saqlanadi
✅ Google Authenticator - user telefoni
✅ Token verification - login paytida tekshiriladi
✅ valid_window - qo'shimcha xavfsizlik

KEYINGI QADAM:
02-qr-code-generation.py - QR code yaratishni o'rganamiz!
""")

print("=" * 60)