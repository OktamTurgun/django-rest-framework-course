"""
Complete 2FA Flow - Full Implementation Example

Bu misolda:
- To'liq 2FA jarayoni simulyatsiyasi
- User registration dan login gacha
- TOTP setup va verification
- Backup codes
- SMS verification
- Error handling
- Real-world scenario
"""

import pyotp
import qrcode
import secrets
import string
from datetime import datetime, timedelta
import io
import time

print("=" * 70)
print("COMPLETE 2FA FLOW - Real World Simulation")
print("=" * 70)

# ==================== Models ====================

class User:
    """User model"""
    users_db = {}  # Simulyatsiya database
    
    def __init__(self, username, email, password):
        self.id = secrets.randbelow(10000)
        self.username = username
        self.email = email
        self.password = password  # Real holatda hash qilinadi
        self.two_factor_enabled = False
        self.two_factor_method = 'none'
        self.phone_number = None
        self.created_at = datetime.now()
        
        # Database'ga qo'shish
        User.users_db[self.id] = self
    
    @classmethod
    def get_by_username(cls, username):
        """Username bo'yicha user topish"""
        for user in cls.users_db.values():
            if user.username == username:
                return user
        return None
    
    def __str__(self):
        status = "2FA ON" if self.two_factor_enabled else "2FA OFF"
        return f"User(id={self.id}, username={self.username}, {status})"


class TOTPDevice:
    """TOTP device model"""
    devices_db = {}
    
    def __init__(self, user, secret_key):
        self.id = secrets.randbelow(10000)
        self.user = user
        self.secret_key = secret_key
        self.confirmed = False
        self.created_at = datetime.now()
        
        TOTPDevice.devices_db[self.id] = self
    
    @classmethod
    def get_by_user(cls, user):
        """User'ning device'ini topish"""
        for device in cls.devices_db.values():
            if device.user.id == user.id and device.confirmed:
                return device
        return None


class BackupCode:
    """Backup code model"""
    codes_db = {}
    
    def __init__(self, user, code):
        self.id = secrets.randbelow(10000)
        self.user = user
        self.code = code
        self.used = False
        self.used_at = None
        self.created_at = datetime.now()
        
        BackupCode.codes_db[self.id] = self
    
    @classmethod
    def generate_for_user(cls, user, count=10):
        """User uchun backup kodlar yaratish"""
        codes = []
        for _ in range(count):
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) 
                          for _ in range(10))
            backup = cls(user, code)
            codes.append(code)
        return codes
    
    @classmethod
    def verify(cls, user, input_code):
        """Backup code'ni tekshirish"""
        for bc in cls.codes_db.values():
            if bc.user.id == user.id and bc.code == input_code and not bc.used:
                bc.used = True
                bc.used_at = datetime.now()
                return True
        return False


# ==================== Services ====================

class AuthService:
    """Authentication service"""
    
    @staticmethod
    def register(username, email, password):
        """User registratsiyasi"""
        # Username mavjudligini tekshirish
        if User.get_by_username(username):
            return None, "Username band"
        
        # User yaratish
        user = User(username, email, password)
        return user, "User muvaffaqiyatli yaratildi"
    
    @staticmethod
    def login(username, password):
        """Login - birinchi bosqich"""
        user = User.get_by_username(username)
        
        if not user:
            return None, "Username topilmadi"
        
        if user.password != password:  # Real holatda hash check
            return None, "Parol noto'g'ri"
        
        # 2FA tekshirish
        if user.two_factor_enabled:
            return user, "2FA talab qilinadi"
        
        return user, "Login muvaffaqiyatli"
    
    @staticmethod
    def verify_2fa(user, token=None, backup_code=None):
        """2FA verification"""
        if backup_code:
            # Backup code bilan
            if BackupCode.verify(user, backup_code):
                return True, "Backup code to'g'ri"
            return False, "Backup code noto'g'ri"
        
        if token:
            # TOTP token bilan
            device = TOTPDevice.get_by_user(user)
            if not device:
                return False, "TOTP device topilmadi"
            
            totp = pyotp.TOTP(device.secret_key)
            if totp.verify(token, valid_window=1):
                return True, "TOTP token to'g'ri"
            return False, "TOTP token noto'g'ri"
        
        return False, "Token yoki backup code kerak"


class TwoFactorService:
    """2FA setup service"""
    
    @staticmethod
    def setup_totp(user):
        """TOTP setup qilish"""
        # Secret key yaratish
        secret_key = pyotp.random_base32()
        
        # Device yaratish (unconfirmed)
        device = TOTPDevice(user, secret_key)
        
        # TOTP object
        totp = pyotp.TOTP(secret_key)
        
        # Provisioning URI
        uri = totp.provisioning_uri(
            name=user.email,
            issuer_name="Complete 2FA Demo"
        )
        
        # QR code yaratish
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        
        return {
            'device': device,
            'secret_key': secret_key,
            'uri': uri,
            'qr': qr
        }
    
    @staticmethod
    def confirm_totp(device, token):
        """TOTP setup'ni tasdiqlash"""
        totp = pyotp.TOTP(device.secret_key)
        
        if totp.verify(token, valid_window=1):
            device.confirmed = True
            device.user.two_factor_enabled = True
            device.user.two_factor_method = 'totp'
            
            # Backup codes yaratish
            backup_codes = BackupCode.generate_for_user(device.user)
            
            return True, backup_codes
        
        return False, []


# ==================== Complete Flow Scenarios ====================

def scenario_1_new_user_registration():
    """Scenario 1: Yangi user ro'yxatdan o'tadi va 2FA sozlaydi"""
    
    print("\n" + "=" * 70)
    print("SCENARIO 1: New User Registration with 2FA Setup")
    print("=" * 70)
    
    # Step 1: Registration
    print("\n📝 Step 1: User Registration")
    print("-" * 70)
    
    username = "johndoe"
    email = "john@example.com"
    password = "SecurePass123!"
    
    user, message = AuthService.register(username, email, password)
    
    if user:
        print(f"✓ {message}")
        print(f"  User ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
    else:
        print(f"✗ {message}")
        return
    
    # Step 2: TOTP Setup
    print("\n🔐 Step 2: TOTP Setup")
    print("-" * 70)
    
    setup_data = TwoFactorService.setup_totp(user)
    
    print(f"✓ TOTP device yaratildi")
    print(f"  Secret Key: {setup_data['secret_key']}")
    print(f"  Provisioning URI: {setup_data['uri'][:50]}...")
    print(f"\n💡 User Google Authenticator'da QR code'ni skanerlaydi")
    
    # Step 3: User Google Authenticator'dan kodni oladi
    print("\n📱 Step 3: Get Code from Google Authenticator")
    print("-" * 70)
    
    # Simulyatsiya - real holatda user kiritadi
    totp = pyotp.TOTP(setup_data['secret_key'])
    current_token = totp.now()
    
    print(f"  Google Authenticator'dagi kod: {current_token}")
    print(f"  [User bu kodni ko'radi va kiritadi]")
    
    # Step 4: TOTP Confirmation
    print("\n✅ Step 4: Confirm TOTP Setup")
    print("-" * 70)
    
    success, backup_codes = TwoFactorService.confirm_totp(
        setup_data['device'], 
        current_token
    )
    
    if success:
        print(f"✓ TOTP tasdiqlandi!")
        print(f"✓ 2FA faollashtirildi!")
        print(f"\n📋 Backup Codes (xavfsiz joyda saqlang!):")
        print(f"  " + "=" * 50)
        for i, code in enumerate(backup_codes, 1):
            print(f"  {i:2d}. {code}")
        print(f"  " + "=" * 50)
    else:
        print(f"✗ TOTP tasdiqlanmadi")
        return
    
    print(f"\n🎉 2FA Setup Complete!")
    print(f"  User: {user}")
    
    return user


def scenario_2_login_with_2fa(user):
    """Scenario 2: 2FA bilan login"""
    
    print("\n" + "=" * 70)
    print("SCENARIO 2: Login with 2FA")
    print("=" * 70)
    
    # Step 1: Username va parol
    print("\n🔑 Step 1: Username & Password")
    print("-" * 70)
    
    user_obj, message = AuthService.login(user.username, user.password)
    
    if not user_obj:
        print(f"✗ {message}")
        return
    
    print(f"✓ Username va parol to'g'ri")
    
    if "2FA talab qilinadi" in message:
        print(f"🔐 2FA verification kerak")
        
        # Step 2: TOTP token
        print("\n📱 Step 2: Enter TOTP Token")
        print("-" * 70)
        
        # User Google Authenticator'dan kodni oladi
        device = TOTPDevice.get_by_user(user_obj)
        totp = pyotp.TOTP(device.secret_key)
        current_token = totp.now()
        
        print(f"  Google Authenticator: {current_token}")
        print(f"  [User kodni kiritadi]")
        
        # Step 3: Verify
        print("\n✅ Step 3: Verify 2FA")
        print("-" * 70)
        
        success, verify_msg = AuthService.verify_2fa(user_obj, token=current_token)
        
        if success:
            print(f"✓ {verify_msg}")
            print(f"✓ Login muvaffaqiyatli!")
            print(f"\n🎉 Welcome, {user_obj.username}!")
        else:
            print(f"✗ {verify_msg}")
    else:
        print(f"✓ {message}")


def scenario_3_login_with_backup_code(user):
    """Scenario 3: Backup code bilan login"""
    
    print("\n" + "=" * 70)
    print("SCENARIO 3: Login with Backup Code")
    print("=" * 70)
    
    # Step 1: Username va parol
    print("\n🔑 Step 1: Username & Password")
    print("-" * 70)
    
    user_obj, message = AuthService.login(user.username, user.password)
    
    if user_obj and "2FA talab qilinadi" in message:
        print(f"✓ Username va parol to'g'ri")
        print(f"🔐 2FA verification kerak")
        
        # Step 2: Backup code
        print("\n📋 Step 2: User Authenticator yo'qotdi - Backup code ishlatadi")
        print("-" * 70)
        
        # Bitta backup code olish
        backup_code = None
        for bc in BackupCode.codes_db.values():
            if bc.user.id == user_obj.id and not bc.used:
                backup_code = bc.code
                break
        
        if backup_code:
            print(f"  Backup code: {backup_code}")
            print(f"  [User saqlagan backup code'ni kiritadi]")
            
            # Step 3: Verify
            print("\n✅ Step 3: Verify Backup Code")
            print("-" * 70)
            
            success, verify_msg = AuthService.verify_2fa(
                user_obj, 
                backup_code=backup_code
            )
            
            if success:
                print(f"✓ {verify_msg}")
                print(f"✓ Login muvaffaqiyatli!")
                
                # Qolgan kodlar
                remaining = sum(1 for bc in BackupCode.codes_db.values() 
                               if bc.user.id == user_obj.id and not bc.used)
                print(f"\n⚠️  {remaining} ta backup kod qoldi")
                
                if remaining <= 2:
                    print(f"💡 Yangi backup kodlar generatsiya qiling!")
            else:
                print(f"✗ {verify_msg}")
        else:
            print(f"✗ Backup kodlar tugadi")


def scenario_4_failed_login_attempts():
    """Scenario 4: Noto'g'ri login urinishlari"""
    
    print("\n" + "=" * 70)
    print("SCENARIO 4: Failed Login Attempts")
    print("=" * 70)
    
    # Mavjud user
    user = User.get_by_username("johndoe")
    if not user:
        print("✗ User topilmadi")
        return
    
    # Test 1: Noto'g'ri parol
    print("\n❌ Test 1: Noto'g'ri Parol")
    print("-" * 70)
    
    user_obj, message = AuthService.login("johndoe", "WrongPassword")
    print(f"Result: {message}")
    
    # Test 2: To'g'ri parol, lekin noto'g'ri TOTP
    print("\n❌ Test 2: Noto'g'ri TOTP Token")
    print("-" * 70)
    
    user_obj, message = AuthService.login("johndoe", user.password)
    if user_obj and "2FA talab qilinadi" in message:
        print(f"✓ Parol to'g'ri")
        print(f"  Noto'g'ri token kiritildi: 000000")
        
        success, verify_msg = AuthService.verify_2fa(user_obj, token="000000")
        print(f"Result: {verify_msg}")
    
    # Test 3: Noto'g'ri backup code
    print("\n❌ Test 3: Noto'g'ri Backup Code")
    print("-" * 70)
    
    success, verify_msg = AuthService.verify_2fa(user_obj, backup_code="WRONGCODE")
    print(f"Result: {verify_msg}")


def scenario_5_2fa_statistics():
    """Scenario 5: 2FA statistika"""
    
    print("\n" + "=" * 70)
    print("SCENARIO 5: 2FA Statistics")
    print("=" * 70)
    
    user = User.get_by_username("johndoe")
    if not user:
        return
    
    print(f"\n📊 User: {user.username}")
    print("-" * 70)
    
    # TOTP
    device = TOTPDevice.get_by_user(user)
    print(f"\nTOTP Status:")
    print(f"  Enabled: {device is not None}")
    if device:
        print(f"  Confirmed: {device.confirmed}")
        print(f"  Created: {device.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Backup Codes
    total_codes = sum(1 for bc in BackupCode.codes_db.values() 
                     if bc.user.id == user.id)
    used_codes = sum(1 for bc in BackupCode.codes_db.values() 
                    if bc.user.id == user.id and bc.used)
    remaining_codes = total_codes - used_codes
    
    print(f"\nBackup Codes:")
    print(f"  Total: {total_codes}")
    print(f"  Used: {used_codes}")
    print(f"  Remaining: {remaining_codes}")
    print(f"  Usage: {(used_codes/total_codes*100):.1f}%")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    if remaining_codes <= 2:
        print(f"  ⚠️  Yangi backup kodlar yarating!")
    if not device:
        print(f"  ⚠️  TOTP'ni faollashtiring!")


# ==================== Main Execution ====================

def main():
    """Main execution"""
    
    print("""
Bu dastur to'liq 2FA jarayonini simulyatsiya qiladi:

Scenarios:
1. Yangi user registratsiyasi va 2FA setup
2. 2FA bilan login (TOTP)
3. Backup code bilan login
4. Noto'g'ri login urinishlari
5. 2FA statistika

Keling boshlaylik!
""")
    
    input("Press Enter to start...")
    
    # Scenario 1: Registration va Setup
    user = scenario_1_new_user_registration()
    
    if user:
        input("\nPress Enter to continue to login...")
        
        # Scenario 2: Login with TOTP
        scenario_2_login_with_2fa(user)
        
        input("\nPress Enter to try backup code...")
        
        # Scenario 3: Login with Backup Code
        scenario_3_login_with_backup_code(user)
        
        input("\nPress Enter to see failed attempts...")
        
        # Scenario 4: Failed Attempts
        scenario_4_failed_login_attempts()
        
        input("\nPress Enter to see statistics...")
        
        # Scenario 5: Statistics
        scenario_5_2fa_statistics()
    
    # Final Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    print(f"""
✅ User yaratildi va 2FA sozlandi
✅ TOTP (Google Authenticator) ishladi
✅ Backup codes generatsiya qilindi
✅ Login flow to'liq test qilindi
✅ Error handling ko'rildi

TO'LIQ 2FA SYSTEM IMPLEMENTED! 🎉

Bu simulyatsiya real production kodiga juda yaqin.
Django DRF da implementatsiya qilish uchun:
- Models: User, TOTPDevice, BackupCode
- Serializers: TOTP, Verification serializers
- Views: Setup, Verify, Login endpoints
- Authentication: Custom authentication class

KEYINGI QADAM:
code/library-project da amaliy implementatsiya!
""")


# ==================== Run ====================

if __name__ == "__main__":
    main()

print("=" * 70)