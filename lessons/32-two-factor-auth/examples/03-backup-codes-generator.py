"""
Backup Codes Generator Example

Bu misolda:
- Backup codes nima va nima uchun kerak
- Xavfsiz tasodifiy kod yaratish
- secrets moduli (cryptographically secure)
- Kod formatlarini tanlash
- Backup codes best practices
"""

import secrets
import string
import random
from datetime import datetime

print("=" * 60)
print("BACKUP CODES GENERATOR EXAMPLE")
print("=" * 60)

# ==================== 1. Backup Codes Nima? ====================
print("\n1. BACKUP CODES NIMA?")
print("-" * 60)

print("""
Backup Codes - bu zaxira kodlar:

📱 Authenticator app yo'qolganda
📱 Telefon buzilganda
📱 Secret key yo'qolganda
📱 2FA'ga kirish imkoni bo'lmaganda

Bu kodlar YORDAMGA KELADI! 🆘

Xususiyatlari:
- Bir martalik (one-time use)
- 10 ta kod beriladi
- Xavfsiz joyda saqlanadi
- Ishlatilgandan keyin o'chiriladi
""")

# ==================== 2. secrets vs random ====================
print("\n\n2. secrets vs random")
print("-" * 60)

print("""
Python'da 2 xil random bor:

1. random moduli:
   - Oddiy tasodifiy sonlar
   - Predictable (bashorat qilish mumkin)
   - ❌ Xavfsizlik uchun YAROQSIZ!

2. secrets moduli:
   - Cryptographically secure
   - Unpredictable (bashorat qilib bo'lmaydi)
   - ✅ Xavfsizlik uchun PERFECT!

💡 2FA uchun FAQAT secrets ishlatiladi!
""")

# Misol - farqni ko'rsatish
print("\nMisol ko'rsatish:")
print(f"random (oddiy):  {random.randint(100000, 999999)}")
print(f"secrets (secure): {secrets.randbelow(1000000):06d}")
print("\n⚠️ Ikkalasi ham raqam, lekin secrets XAVFSIZ!")

# ==================== 3. Oddiy Backup Code ====================
print("\n\n3. ODDIY BACKUP CODE YARATISH")
print("-" * 60)

def generate_simple_code():
    """6 xonali oddiy backup code"""
    return secrets.randbelow(1000000)

print("6 xonali oddiy kodlar:\n")
for i in range(5):
    code = generate_simple_code()
    print(f"  {i+1}. {code:06d}")

print("\n💡 :06d - 6 xonali format (0 bilan to'ldiradi)")

# ==================== 4. Alfanumerik Backup Code ====================
print("\n\n4. ALFANUMERIK BACKUP CODE (Harflar + Raqamlar)")
print("-" * 60)

def generate_alphanumeric_code(length=10):
    """Harflar va raqamlardan iborat kod"""
    characters = string.ascii_uppercase + string.digits
    code = ''.join(secrets.choice(characters) for _ in range(length))
    return code

print(f"Ishlatiladigan belgilar: {string.ascii_uppercase + string.digits}")
print(f"Jami: {len(string.ascii_uppercase + string.digits)} ta belgi\n")

print("10 belgili alfanumerik kodlar:\n")
for i in range(5):
    code = generate_alpanumeric_code()
    print(f"  {i+1}. {code}")

# ==================== 5. Formatted Backup Codes ====================
print("\n\n5. FORMATTED BACKUP CODES (To'rttalik formatda)")
print("-" * 60)

def generate_formatted_code():
    """4-4-4 formatdagi kod (masalan: ABCD-EFGH-IJKL)"""
    characters = string.ascii_uppercase + string.digits
    
    # 3 ta 4 belgili segment
    segments = []
    for _ in range(3):
        segment = ''.join(secrets.choice(characters) for _ in range(4))
        segments.append(segment)
    
    return '-'.join(segments)

print("4-4-4 formatdagi kodlar:\n")
for i in range(5):
    code = generate_formatted_code()
    print(f"  {i+1}. {code}")

print("\n💡 Tire bilan ajratish o'qishni osonlashtiradi!")

# ==================== 6. Production-Ready Generator ====================
print("\n\n6. PRODUCTION-READY GENERATOR")
print("-" * 60)

class BackupCodeGenerator:
    """Professional backup code generator"""
    
    @staticmethod
    def generate_code(length=10):
        """10 belgili unique kod"""
        characters = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    @staticmethod
    def generate_codes(count=10, length=10):
        """Bir nechta unique kodlar"""
        codes = set()  # Unique bo'lishi uchun
        
        while len(codes) < count:
            code = BackupCodeGenerator.generate_code(length)
            codes.add(code)
        
        return list(codes)
    
    @staticmethod
    def format_code(code, chunk_size=4):
        """Kodni formatlash (4-4-4)"""
        chunks = [code[i:i+chunk_size] for i in range(0, len(code), chunk_size)]
        return '-'.join(chunks)
    
    @staticmethod
    def generate_formatted_codes(count=10):
        """Formatted kodlar generatsiya"""
        codes = BackupCodeGenerator.generate_codes(count, length=12)
        return [BackupCodeGenerator.format_code(code) for code in codes]

# Test
print("BackupCodeGenerator test:\n")
codes = BackupCodeGenerator.generate_formatted_codes(10)

for i, code in enumerate(codes, 1):
    print(f"  {i:2d}. {code}")

# ==================== 7. Database Model Simulyatsiyasi ====================
print("\n\n7. DATABASE MODEL SIMULYATSIYASI")
print("-" * 60)

class BackupCode:
    """Django model simulyatsiyasi"""
    
    def __init__(self, user_id, code):
        self.id = secrets.randbelow(10000)
        self.user_id = user_id
        self.code = code
        self.used = False
        self.used_at = None
        self.created_at = datetime.now()
    
    def mark_as_used(self):
        """Kodni ishlatilgan deb belgilash"""
        self.used = True
        self.used_at = datetime.now()
    
    def __str__(self):
        status = "✓ Used" if self.used else "○ Active"
        return f"{status} | {self.code} | User: {self.user_id}"
    
    @classmethod
    def create_for_user(cls, user_id, count=10):
        """User uchun backup kodlar yaratish"""
        codes = BackupCodeGenerator.generate_codes(count)
        backup_codes = [cls(user_id, code) for code in codes]
        return backup_codes

# Test
print("\nUser #123 uchun backup kodlar yaratish:\n")
user_id = 123
backup_codes = BackupCode.create_for_user(user_id, count=10)

for bc in backup_codes:
    print(f"  {bc}")

# Bitta kodni ishlatish
print("\n\nKod ishlatish simulyatsiyasi:")
print(f"Oldin: {backup_codes[0]}")
backup_codes[0].mark_as_used()
print(f"Keyin: {backup_codes[0]}")

# ==================== 8. Backup Code Verification ====================
print("\n\n8. BACKUP CODE VERIFICATION")
print("-" * 60)

def verify_backup_code(user_codes, input_code):
    """
    Backup code'ni tekshirish
    
    Args:
        user_codes: User'ning backup kodlari list
        input_code: User'dan kelgan kod
        
    Returns:
        tuple: (is_valid, message)
    """
    # Kodni uppercase qilish
    input_code = input_code.upper().replace('-', '').replace(' ', '')
    
    for bc in user_codes:
        # Formatsiz taqqoslash
        bc_clean = bc.code.replace('-', '').replace(' ', '')
        
        if bc_clean == input_code:
            if bc.used:
                return False, "❌ Bu kod allaqachon ishlatilgan!"
            else:
                bc.mark_as_used()
                return True, "✅ Kod to'g'ri! 2FA tasdiqlandi!"
    
    return False, "❌ Kod topilmadi yoki noto'g'ri!"

# Test
print("\nBackup code verification test:\n")

test_code = backup_codes[1].code
print(f"To'g'ri kod: {test_code}")

# Test 1: To'g'ri kod
valid, msg = verify_backup_code(backup_codes, test_code)
print(f"Test 1: {msg}")

# Test 2: Qayta ishlatish
valid, msg = verify_backup_code(backup_codes, test_code)
print(f"Test 2: {msg}")

# Test 3: Noto'g'ri kod
valid, msg = verify_backup_code(backup_codes, "WRONGCODE123")
print(f"Test 3: {msg}")

# ==================== 9. Statistics ====================
print("\n\n9. STATISTICS (Qolgan kodlar)")
print("-" * 60)

def get_backup_codes_stats(backup_codes):
    """Backup kodlar statistikasi"""
    total = len(backup_codes)
    used = sum(1 for bc in backup_codes if bc.used)
    remaining = total - used
    
    return {
        'total': total,
        'used': used,
        'remaining': remaining,
        'percentage_used': (used / total * 100) if total > 0 else 0
    }

stats = get_backup_codes_stats(backup_codes)

print(f"\nBackup Codes Statistics:")
print(f"  Total:     {stats['total']}")
print(f"  Used:      {stats['used']}")
print(f"  Remaining: {stats['remaining']}")
print(f"  Used %:    {stats['percentage_used']:.1f}%")

# Warning agar kam qolgan bo'lsa
if stats['remaining'] <= 2:
    print(f"\n⚠️  WARNING: Faqat {stats['remaining']} ta kod qoldi!")
    print(f"💡 Yangi kodlar generatsiya qiling!")

# ==================== 10. Best Practices ====================
print("\n\n10. BEST PRACTICES")
print("-" * 60)

print("""
✅ Backup Codes Best Practices:

1. Kod uzunligi:
   - Minimal 10 belgi
   - 12-16 optimal
   
2. Kod soni:
   - 10 ta standard
   - Minimal 8 ta
   
3. Format:
   - Uppercase (katta harflar)
   - Tire bilan ajratish (4-4-4)
   - Probel yoki tire'siz ham ishlashi kerak
   
4. Xavfsizlik:
   - secrets moduli (FAQAT!)
   - Unique kodlar
   - Database'da hash'lash (ixtiyoriy)
   
5. Foydalanish:
   - Bir martalik
   - Ishlatilgandan keyin o'chirish
   - Yangi kodlar generatsiya qilish
   
6. Saqlash:
   - User download qilishi kerak
   - Xavfsiz joyda (password manager)
   - Print qilish opsiyasi
   
7. Ogohlantirish:
   - 2-3 ta qolganda xabar berish
   - Regenerate option ko'rsatish
   
8. Logging:
   - Qachon yaratilgan
   - Qachon ishlatilgan
   - Kim ishlatgan
""")

# ==================== 11. Complete Example ====================
print("\n\n11. COMPLETE EXAMPLE - 2FA Setup Flow")
print("-" * 60)

def complete_2fa_setup_flow(user_id, username):
    """To'liq 2FA setup jarayoni"""
    print(f"\n--- 2FA Setup for User #{user_id} ({username}) ---\n")
    
    # 1. TOTP Setup
    import pyotp
    secret = pyotp.random_base32()
    print(f"1. ✓ TOTP secret key yaratildi")
    
    # 2. QR Code (simulyatsiya)
    print(f"2. ✓ QR code yaratildi")
    
    # 3. User verify qildi (simulyatsiya)
    print(f"3. ✓ User TOTP'ni verify qildi")
    
    # 4. Backup codes yaratish
    backup_codes = BackupCode.create_for_user(user_id, count=10)
    print(f"4. ✓ {len(backup_codes)} ta backup kod yaratildi\n")
    
    # Backup kodlarni ko'rsatish
    print("📋 BACKUP CODES (Xavfsiz joyda saqlang!):")
    print("=" * 40)
    for i, bc in enumerate(backup_codes, 1):
        formatted = BackupCodeGenerator.format_code(bc.code)
        print(f"  {i:2d}. {formatted}")
    print("=" * 40)
    
    print("\n⚠️  MUHIM:")
    print("   - Bu kodlarni xavfsiz joyda saqlang")
    print("   - Har bir kod faqat 1 marta ishlatiladi")
    print("   - Authenticator yo'qolganda kerak bo'ladi")
    
    return backup_codes

# Test
complete_2fa_setup_flow(123, "johndoe")

# ==================== 12. Xulosa ====================
print("\n\n" + "=" * 60)
print("XULOSA")
print("=" * 60)

print("""
✅ Backup codes - zaxira kodlar (1 martalik)
✅ secrets moduli - cryptographically secure
✅ 10 ta kod - standard
✅ 4-4-4 format - o'qish uchun qulay
✅ Mark as used - ishlatilganini belgilash
✅ Statistics - qolgan kodlarni kuzatish

BACKUP CODES WORKFLOW:
1. User 2FA setup qilganda yaratiladi
2. User download/print qiladi
3. Xavfsiz joyda saqlanadi
4. Authenticator yo'qolganda ishlatiladi
5. Ishlatilgandan keyin o'chiriladi
6. Kam qolganda yangilanadi

KEYINGI QADAM:
04-sms-code-generator.py - SMS verifikatsiya!
""")

print("=" * 60)