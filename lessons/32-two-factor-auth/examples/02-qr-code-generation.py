"""
QR Code Generation Example

Bu misolda:
- QR code nima va nima uchun kerak
- qrcode kutubxonasi bilan ishlash
- TOTP URI dan QR code yaratish
- PNG fayl sifatida saqlash
- Base64 encoding (API uchun)
"""

import pyotp
import qrcode
import io
import base64
from PIL import Image

print("=" * 60)
print("QR CODE GENERATION EXAMPLE")
print("=" * 60)

# ==================== 1. TOTP Setup ====================
print("\n1. TOTP SETUP")
print("-" * 60)

# Secret key yaratish
secret_key = pyotp.random_base32()
print(f"Secret Key: {secret_key}")

# TOTP object
totp = pyotp.TOTP(secret_key)
print(f"TOTP Object: {totp}")

# ==================== 2. Provisioning URI ====================
print("\n\n2. PROVISIONING URI YARATISH")
print("-" * 60)

# URI yaratish
username = "johndoe@example.com"
app_name = "Library Project"

uri = totp.provisioning_uri(
    name=username,
    issuer_name=app_name
)

print(f"Username: {username}")
print(f"App Name: {app_name}")
print(f"\nProvisioning URI:")
print(f"{uri}")
print(f"\n💡 Bu URI'ni Google Authenticator tushunadi!")

# URI formatini tushuntirish
print("\nURI Format:")
print("otpauth://totp/{issuer}:{account}?secret={secret}&issuer={issuer}")
print("\nQismlar:")
print("- otpauth://totp - Protocol")
print(f"- {app_name} - Issuer (App nomi)")
print(f"- {username} - Account (User)")
print(f"- secret={secret_key[:10]}... - Secret key")

# ==================== 3. QR Code Yaratish (Oddiy) ====================
print("\n\n3. QR CODE YARATISH (Oddiy usul)")
print("-" * 60)

# Oddiy QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

qr.add_data(uri)
qr.make(fit=True)

# Rasm yaratish
img = qr.make_image(fill_color="black", back_color="white")

# Faylga saqlash
filename = "qr_code_simple.png"
img.save(filename)
print(f"✅ QR code saqlandi: {filename}")
print(f"📱 Bu faylni Google Authenticator bilan skanerlang!")

# ==================== 4. QR Code (Advanced) ====================
print("\n\n4. QR CODE (Advanced parametrlar)")
print("-" * 60)

# Advanced settings
qr_advanced = qrcode.QRCode(
    version=1,  # 1-40, kattaroq = ko'proq ma'lumot
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # H = High (30% tiklash)
    box_size=10,  # Har bir box'ning pixel o'lchami
    border=5,  # Border kengligi (minimal 4)
)

qr_advanced.add_data(uri)
qr_advanced.make(fit=True)

# Custom ranglar bilan
img_advanced = qr_advanced.make_image(
    fill_color="darkblue",
    back_color="lightblue"
)

filename_advanced = "qr_code_advanced.png"
img_advanced.save(filename_advanced)
print(f"✅ Advanced QR code saqlandi: {filename_advanced}")

# QR code parametrlarini chop etish
print("\nQR Code parametrlari:")
print(f"- Version: {qr_advanced.version}")
print(f"- Error Correction: HIGH (30% tiklash)")
print(f"- Box Size: {qr_advanced.box_size}px")
print(f"- Border: {qr_advanced.border} box")
print(f"- Modules: {len(qr_advanced.modules)} x {len(qr_advanced.modules)}")

# ==================== 5. Base64 Encoding (API uchun) ====================
print("\n\n5. BASE64 ENCODING (API Response)")
print("-" * 60)

# QR code'ni memory'da yaratish (faylsiz)
qr_api = qrcode.QRCode(
    version=1,
    box_size=10,
    border=5
)

qr_api.add_data(uri)
qr_api.make(fit=True)

img_api = qr_api.make_image(fill_color="black", back_color="white")

# BytesIO buffer'da saqlash
buffer = io.BytesIO()
img_api.save(buffer, format='PNG')
buffer.seek(0)

# Base64 ga aylantirish
img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

print(f"Base64 string uzunligi: {len(img_base64)} belgi")
print(f"\nBase64 string (birinchi 100 belgi):")
print(f"{img_base64[:100]}...")
print(f"\n💡 Bu stringni API response'da yuboramiz!")

# Data URI format
data_uri = f"data:image/png;base64,{img_base64}"
print(f"\nData URI (frontend uchun):")
print(f"{data_uri[:100]}...")

# ==================== 6. Real API Response Simulyatsiyasi ====================
print("\n\n6. REAL API RESPONSE SIMULYATSIYASI")
print("-" * 60)

def generate_2fa_setup_response(username, app_name):
    """
    Real API endpoint response simulyatsiyasi
    POST /api/v1/users/2fa/totp/setup/
    """
    # Secret key yaratish
    secret = pyotp.random_base32()
    
    # TOTP object
    totp = pyotp.TOTP(secret)
    
    # Provisioning URI
    uri = totp.provisioning_uri(name=username, issuer_name=app_name)
    
    # QR code generatsiya
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Base64 encoding
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # API Response
    response = {
        "secret_key": secret,
        "qr_code": f"data:image/png;base64,{qr_code_base64}",
        "manual_entry_key": secret,
        "message": "QR kodni Google Authenticator ilovasida skanerlang yoki manual kiriting"
    }
    
    return response

# Test
print("\nAPI Response simulyatsiyasi:")
api_response = generate_2fa_setup_response("testuser@example.com", "Library Project")

print(f"\nResponse keys: {list(api_response.keys())}")
print(f"\nSecret Key: {api_response['secret_key']}")
print(f"QR Code (Base64): {api_response['qr_code'][:80]}...")
print(f"Manual Entry: {api_response['manual_entry_key']}")
print(f"Message: {api_response['message']}")

# ==================== 7. QR Code O'lchamlarini Hisoblash ====================
print("\n\n7. QR CODE O'LCHAMLARINI HISOBLASH")
print("-" * 60)

def calculate_qr_size(version, box_size, border):
    """QR code'ning pixel o'lchamini hisoblash"""
    # Modules soni = (version * 4) + 17
    modules = (version * 4) + 17
    
    # To'liq o'lcham = (modules + 2*border) * box_size
    total_size = (modules + 2 * border) * box_size
    
    return modules, total_size

# Turli versiyalar uchun
print("\nQR Code o'lchamlari (box_size=10, border=5):\n")
for version in [1, 2, 3, 4, 5]:
    modules, size = calculate_qr_size(version, 10, 5)
    print(f"Version {version}: {modules}x{modules} modules = {size}x{size}px")

# ==================== 8. Error Correction Levels ====================
print("\n\n8. ERROR CORRECTION LEVELS")
print("-" * 60)

print("""
QR Code'da 4 ta error correction darajasi bor:

1. ERROR_CORRECT_L (Low)    - 7% tiklash
   └─ Tez, kichik, lekin kam himoyalangan

2. ERROR_CORRECT_M (Medium) - 15% tiklash
   └─ Standart tanlov

3. ERROR_CORRECT_Q (Quartile) - 25% tiklash
   └─ Yaxshi himoya

4. ERROR_CORRECT_H (High)   - 30% tiklash
   └─ Eng yaxshi himoya, lekin kattaroq

💡 2FA uchun MEDIUM yoki HIGH tavsiya etiladi!
""")

# ==================== 9. Best Practices ====================
print("\n\n9. BEST PRACTICES")
print("-" * 60)

print("""
✅ QR Code Best Practices:

1. Version: 
   - 1-2 yetarli (TOTP URI qisqa)
   
2. Error Correction:
   - M yoki H (15-30% tiklash)
   
3. Box Size:
   - 10px optimal (mobile uchun)
   
4. Border:
   - Minimal 4 (standart)
   
5. Ranglar:
   - Qora-oq (eng yaxshi kontrast)
   - Tushunarli ranglar tanlang
   
6. API Response:
   - Base64 encoding
   - Data URI format
   - PNG format tavsiya etiladi
   
7. Frontend:
   - <img src="data:image/png;base64,..." />
   - Responsive qiling
   - Print button qo'shing
""")

# ==================== 10. Xulosa ====================
print("\n\n" + "=" * 60)
print("XULOSA")
print("=" * 60)

print(f"""
✅ QR Code yaratildi: qr_code_simple.png
✅ Advanced QR Code: qr_code_advanced.png
✅ Base64 encoding o'rganildi
✅ API response simulyatsiyasi ko'rildi

QR CODE WORKFLOW:
1. Secret key yaratish
2. Provisioning URI yaratish
3. URI dan QR code generatsiya
4. Base64 ga aylantirish
5. API response'da yuborish
6. Frontend'da ko'rsatish
7. User Google Authenticator'da skanerlaydi

KEYINGI QADAM:
03-backup-codes-generator.py - Backup kodlar yaratish!
""")

print("=" * 60)