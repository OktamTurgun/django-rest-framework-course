"""
SMS Code Generator Example

Bu misolda:
- SMS verifikatsiya kodlari
- 6 xonali tasodifiy kod
- Telefon raqam validatsiya
- Kod muddati (expiration)
- SMS yuborish simulyatsiyasi
"""

import secrets
import string
from datetime import datetime, timedelta
import re

print("=" * 60)
print("SMS VERIFICATION CODE GENERATOR")
print("=" * 60)

# ==================== 1. SMS Code Nima? ====================
print("\n1. SMS CODE NIMA?")
print("-" * 60)

print("""
SMS Verification Code - bu SMS orqali yuboriladigan tasdiqlash kodi:

📱 User telefon raqamini kiritadi
📱 Sistema 6 xonali kod yuboradi
📱 User kodni kiritadi
📱 Sistema tekshiradi

Xususiyatlari:
- 6 xonali (standart)
- Faqat raqamlar
- 5-10 daqiqa muddati
- Bir martalik
- SMS orqali yuboriladi

💡 TOTP'dan farqi: Internet kerak, SMS xarajati bor
""")

# ==================== 2. Oddiy 6 Xonali Kod ====================
print("\n\n2. ODDIY 6 XONALI KOD")
print("-" * 60)

def generate_simple_sms_code():
    """Oddiy 6 xonali kod"""
    return secrets.randbelow(1000000)

print("Oddiy 6 xonali kodlar:\n")
for i in range(10):
    code = generate_simple_sms_code()
    print(f"  {i+1:2d}. {code:06d}")

print("\n💡 :06d formatda - 000123 kabi 0 bilan to'ldiriladi")

# ==================== 3. String Format ====================
print("\n\n3. STRING FORMAT (String sifatida)")
print("-" * 60)

def generate_sms_code_string():
    """String formatdagi 6 xonali kod"""
    return ''.join(secrets.choice(string.digits) for _ in range(6))

print("String format kodlar:\n")
for i in range(10):
    code = generate_sms_code_string()
    print(f"  {i+1:2d}. {code}")

print("\n💡 String format - database'da saqlashda qulay")

# ==================== 4. Production-Ready Generator ====================
print("\n\n4. PRODUCTION-READY SMS CODE GENERATOR")
print("-" * 60)

class SMSCodeGenerator:
    """Professional SMS kod generator"""
    
    @staticmethod
    def generate(length=6):
        """
        SMS kod generatsiya qilish
        
        Args:
            length: Kod uzunligi (default: 6)
            
        Returns:
            str: SMS kod
        """
        return ''.join(secrets.choice(string.digits) for _ in range(length))
    
    @staticmethod
    def generate_with_prefix(prefix="SMS", length=6):
        """Prefix bilan kod (debugging uchun)"""
        code = SMSCodeGenerator.generate(length)
        return f"{prefix}-{code}"
    
    @staticmethod
    def is_valid_format(code, length=6):
        """Kod formatini tekshirish"""
        if not code:
            return False
        if not code.isdigit():
            return False
        if len(code) != length:
            return False
        return True

# Test
print("\nSMSCodeGenerator test:\n")

for i in range(5):
    code = SMSCodeGenerator.generate()
    is_valid = SMSCodeGenerator.is_valid_format(code)
    print(f"  {i+1}. {code} - Valid: {is_valid}")

print("\nPrefix bilan:")
for i in range(3):
    code = SMSCodeGenerator.generate_with_prefix("DEV")
    print(f"  {i+1}. {code}")

# ==================== 5. Telefon Raqam Validatsiya ====================
print("\n\n5. TELEFON RAQAM VALIDATSIYA")
print("-" * 60)

class PhoneValidator:
    """Telefon raqam validatori"""
    
    @staticmethod
    def clean_phone(phone):
        """Telefon raqamni tozalash"""
        # Faqat raqamlar va + belgisini qoldirish
        return re.sub(r'[^\d+]', '', phone)
    
    @staticmethod
    def is_valid_uzbek_phone(phone):
        """O'zbekiston telefon raqami"""
        clean = PhoneValidator.clean_phone(phone)
        
        # O'zbekiston: +998XXXXXXXXX (9 xonali)
        pattern = r'^\+998\d{9}$'
        return bool(re.match(pattern, clean))
    
    @staticmethod
    def format_uzbek_phone(phone):
        """O'zbekiston formatida ko'rsatish"""
        clean = PhoneValidator.clean_phone(phone)
        
        if len(clean) == 12 and clean.startswith('+998'):
            # +998 90 123 45 67
            return f"{clean[:4]} {clean[4:6]} {clean[6:9]} {clean[9:11]} {clean[11:]}"
        
        return clean
    
    @staticmethod
    def is_valid_international(phone):
        """Xalqaro format"""
        clean = PhoneValidator.clean_phone(phone)
        
        # + bilan boshlanadi va 10-15 xonali
        if clean.startswith('+') and 10 <= len(clean) <= 15:
            return True
        return False

# Test
print("\nTelefon raqam validatsiya:\n")

test_phones = [
    "+998901234567",
    "+998 90 123 45 67",
    "998901234567",
    "+99890-123-45-67",
    "+1234567890",
    "901234567",  # Invalid
]

for phone in test_phones:
    clean = PhoneValidator.clean_phone(phone)
    is_uzbek = PhoneValidator.is_valid_uzbek_phone(phone)
    is_intl = PhoneValidator.is_valid_international(phone)
    formatted = PhoneValidator.format_uzbek_phone(phone)
    
    print(f"Phone: {phone}")
    print(f"  Clean: {clean}")
    print(f"  Uzbek: {is_uzbek}")
    print(f"  International: {is_intl}")
    print(f"  Formatted: {formatted}\n")

# ==================== 6. SMS Verification Model ====================
print("\n\n6. SMS VERIFICATION MODEL (Django simulyatsiya)")
print("-" * 60)

class SMSVerification:
    """SMS verifikatsiya modeli"""
    
    def __init__(self, user_id, phone_number):
        self.id = secrets.randbelow(10000)
        self.user_id = user_id
        self.phone_number = phone_number
        self.code = SMSCodeGenerator.generate()
        self.verified = False
        self.created_at = datetime.now()
        self.expires_at = datetime.now() + timedelta(minutes=10)
        self.attempts = 0
        self.max_attempts = 3
    
    def is_expired(self):
        """Muddati o'tganmi?"""
        return datetime.now() > self.expires_at
    
    def verify(self, input_code):
        """Kodni tekshirish"""
        self.attempts += 1
        
        # Muddati tekshirish
        if self.is_expired():
            return False, "⏰ Kod muddati o'tgan. Yangi kod so'rang"
        
        # Max attempts
        if self.attempts > self.max_attempts:
            return False, "🚫 Maksimal urinishlar soni oshdi"
        
        # Allaqachon verify qilingan
        if self.verified:
            return False, "✓ Bu kod allaqachon ishlatilgan"
        
        # Kodni tekshirish
        if input_code == self.code:
            self.verified = True
            return True, "✅ Telefon raqami tasdiqlandi!"
        else:
            remaining = self.max_attempts - self.attempts
            return False, f"❌ Kod noto'g'ri. Qolgan urinishlar: {remaining}"
    
    def time_remaining(self):
        """Qancha vaqt qoldi"""
        if self.is_expired():
            return "Muddati o'tgan"
        
        remaining = self.expires_at - datetime.now()
        minutes = int(remaining.total_seconds() / 60)
        seconds = int(remaining.total_seconds() % 60)
        
        return f"{minutes}:{seconds:02d}"
    
    def __str__(self):
        status = "✓ Verified" if self.verified else "○ Pending"
        return f"{status} | {self.phone_number} | Code: {self.code} | Expires: {self.time_remaining()}"

# Test
print("\nSMSVerification model test:\n")

# Verification yaratish
user_id = 123
phone = "+998901234567"
verification = SMSVerification(user_id, phone)

print(f"Created: {verification}")
print(f"\nDetails:")
print(f"  User ID: {verification.user_id}")
print(f"  Phone: {verification.phone_number}")
print(f"  Code: {verification.code}")
print(f"  Expires at: {verification.expires_at.strftime('%H:%M:%S')}")
print(f"  Time remaining: {verification.time_remaining()}")

# ==================== 7. Verification Testing ====================
print("\n\n7. VERIFICATION TESTING")
print("-" * 60)

print("\nTest 1: To'g'ri kod")
success, message = verification.verify(verification.code)
print(f"Result: {message}")
print(f"Verified: {verification.verified}")

print("\nTest 2: Qayta ishlatish")
success, message = verification.verify(verification.code)
print(f"Result: {message}")

# Yangi verification
print("\n\nYangi verification:")
verification2 = SMSVerification(456, "+998911234567")
print(f"Code: {verification2.code}")

print("\nTest 3: Noto'g'ri kod")
for i in range(4):
    success, message = verification2.verify("000000")
    print(f"  Attempt {i+1}: {message}")

# ==================== 8. SMS Yuborish Simulyatsiyasi ====================
print("\n\n8. SMS YUBORISH SIMULYATSIYASI")
print("-" * 60)

class SMSService:
    """SMS yuborish service (Twilio simulyatsiyasi)"""
    
    @staticmethod
    def send_verification_code(phone_number, code):
        """
        SMS yuborish
        
        Real production'da:
        - Twilio, Vonage, AWS SNS
        - Eskiz.uz, PlayMobile.uz (O'zbekiston)
        """
        message = f"Sizning tasdiqlash kodingiz: {code}\n\nKod 10 daqiqa amal qiladi."
        
        # Simulyatsiya - console'ga chiqarish
        print(f"\n📱 SMS SENT TO: {phone_number}")
        print(f"=" * 50)
        print(message)
        print(f"=" * 50)
        
        return True
    
    @staticmethod
    def send_welcome_sms(phone_number, username):
        """Xush kelibsiz SMS"""
        message = f"Assalomu alaykum, {username}!\n\nTelefon raqamingiz tasdiqlandi. Xush kelibsiz!"
        
        print(f"\n📱 SMS SENT TO: {phone_number}")
        print(f"=" * 50)
        print(message)
        print(f"=" * 50)
        
        return True

# Test
print("\nSMS yuborish test:\n")

# Verification SMS
verification3 = SMSVerification(789, "+998901234567")
SMSService.send_verification_code(verification3.phone_number, verification3.code)

# Welcome SMS
SMSService.send_welcome_sms("+998901234567", "John Doe")

# ==================== 9. Complete SMS Flow ====================
print("\n\n9. COMPLETE SMS VERIFICATION FLOW")
print("-" * 60)

def complete_sms_verification_flow(user_id, phone_number):
    """To'liq SMS verifikatsiya jarayoni"""
    
    print(f"\n{'='*50}")
    print(f"SMS VERIFICATION FLOW")
    print(f"{'='*50}")
    
    # Step 1: Telefon validatsiya
    print(f"\nStep 1: Telefon raqam validatsiya")
    if not PhoneValidator.is_valid_international(phone_number):
        print(f"❌ Telefon raqami noto'g'ri formatda")
        return False
    print(f"✓ Telefon raqami to'g'ri: {phone_number}")
    
    # Step 2: Verification yaratish
    print(f"\nStep 2: SMS kod generatsiya")
    verification = SMSVerification(user_id, phone_number)
    print(f"✓ Kod yaratildi: {verification.code}")
    print(f"✓ Muddati: {verification.time_remaining()}")
    
    # Step 3: SMS yuborish
    print(f"\nStep 3: SMS yuborish")
    SMSService.send_verification_code(phone_number, verification.code)
    print(f"✓ SMS yuborildi")
    
    # Step 4: User kodni kiritadi (simulyatsiya)
    print(f"\nStep 4: User kodni kiritadi")
    print(f"[Waiting for user input...]")
    
    # Simulyatsiya - to'g'ri kod
    user_input = verification.code
    print(f"User kirdi: {user_input}")
    
    # Step 5: Verifikatsiya
    print(f"\nStep 5: Kod tekshirish")
    success, message = verification.verify(user_input)
    print(f"{message}")
    
    if success:
        # Step 6: Welcome SMS
        print(f"\nStep 6: Welcome SMS")
        SMSService.send_welcome_sms(phone_number, f"User{user_id}")
        print(f"✓ SMS verification completed!")
        return True
    
    return False

# Test
complete_sms_verification_flow(999, "+998901234567")

# ==================== 10. Best Practices ====================
print("\n\n10. BEST PRACTICES")
print("-" * 60)

print("""
✅ SMS Verification Best Practices:

1. Kod uzunligi:
   - 6 xonali (standart)
   - 4 xonali - kam xavfsiz
   - 8 xonali - ko'p xavfsiz

2. Kod muddati:
   - 5-10 daqiqa optimal
   - Juda qisqa - user uchun qiyin
   - Juda uzun - xavfsizlik riski

3. Urinishlar soni:
   - 3-5 marta maksimal
   - Ortiq urinish - block qilish
   - IP tracking qo'shish

4. SMS xabar:
   - Qisqa va tushunarli
   - Kod aniq ko'rinadi
   - Muddatni eslatish
   - Branding qo'shish

5. Telefon validatsiya:
   - International format (+...)
   - O'zbekiston: +998XXXXXXXXX
   - Xato formatlarni rad etish

6. Rate Limiting:
   - 1 SMS / 1 daqiqa
   - 5 SMS / 1 soat
   - DDoS himoya

7. Cost Optimization:
   - SMS cache (testing uchun)
   - Fake numbers detect
   - Bulk SMS providers

8. Security:
   - SMS interception
   - SIM swap attack
   - TOTP yaxshiroq (SMS'dan)

9. User Experience:
   - Auto-fill code (iOS/Android)
   - Resend option
   - Timer ko'rsatish
   - Clear error messages

10. Logging:
    - SMS yuborilgan vaqt
    - Verification attempts
    - Success/failure
    - Cost tracking
""")

# ==================== 11. SMS vs TOTP ====================
print("\n\n11. SMS vs TOTP COMPARISON")
print("-" * 60)

comparison = """
┌──────────────────┬──────────────────┬──────────────────┐
│     Feature      │       SMS        │      TOTP        │
├──────────────────┼──────────────────┼──────────────────┤
│ Internet kerak   │       ✓          │        ✗         │
│ Xarajat          │     Bor          │       Yo'q       │
│ Setup qiyin      │       ✗          │        ✓         │
│ Xavfsizlik       │      O'rta       │      Yuqori      │
│ User-friendly    │       ✓          │        ✗         │
│ Offline          │       ✗          │        ✓         │
│ SIM swap risk    │       ✓          │        ✗         │
│ Phone kerak      │       ✓          │        ✗         │
└──────────────────┴──────────────────┴──────────────────┘

💡 TAVSIYA:
   - Primary: TOTP (Google Authenticator)
   - Backup: SMS (fallback option)
   - Best: Ikkalasini ham qo'llash
"""

print(comparison)

# ==================== 12. Xulosa ====================
print("\n\n" + "=" * 60)
print("XULOSA")
print("=" * 60)

print("""
✅ SMS kod - 6 xonali tasodifiy raqam
✅ secrets moduli - xavfsiz generatsiya
✅ 10 daqiqa muddati - optimal
✅ 3 urinish - rate limiting
✅ Telefon validatsiya - muhim
✅ SMS service - Twilio, Vonage, Eskiz

SMS VERIFICATION WORKFLOW:
1. User telefon raqamini kiritadi
2. Sistema kod yuboradi
3. User kodni kiritadi
4. Sistema verifikatsiya qiladi
5. Muvaffaqiyatli bo'lsa tasdiqlaydi

REAL PRODUCTION:
- Twilio / Vonage / AWS SNS (xalqaro)
- Eskiz.uz / PlayMobile.uz (O'zbekiston)
- Rate limiting muhim!
- Cost optimization kerak!

KEYINGI QADAM:
05-complete-2fa-flow.py - To'liq 2FA jarayoni!
""")

print("=" * 60)