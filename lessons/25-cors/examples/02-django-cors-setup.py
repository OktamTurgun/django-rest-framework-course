"""
Django CORS Setup - Qadamma-qadam sozlash
"""

# ==========================================
# STEP 1: INSTALLATION
# ==========================================

"""
Terminal'da:

pip install django-cors-headers

# Yoki requirements.txt'ga qo'shing:
# django-cors-headers==4.3.1
"""


# ==========================================
# STEP 2: SETTINGS.PY - INSTALLED_APPS
# ==========================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',  # ← ADD THIS!
    
    # Local apps
    'books',
    'accounts',
]


# ==========================================
# STEP 3: SETTINGS.PY - MIDDLEWARE
# ==========================================

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ← ADD THIS AT THE TOP!
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

"""
⚠️ MUHIM: CorsMiddleware ENG YUQORIDA BO'LISHI KERAK!

Nima uchun?
- CorsMiddleware request'ni birinchi bo'lib handle qilishi kerak
- OPTIONS preflight request'larni to'g'ri ishlashi uchun
- Boshqa middleware'lardan oldin CORS headerlar qo'shilishi kerak
"""


# ==========================================
# STEP 4: SETTINGS.PY - BASIC CONFIGURATION
# ==========================================

# VARIANT 1: Development - Barcha origin'larni ruxsat berish
# ⚠️ FAQAT DEVELOPMENT UCHUN!

CORS_ALLOW_ALL_ORIGINS = True

"""
Bu quyidagi demakdir:
- Har qanday origin'dan so'rov qabul qilinadi
- ✅ http://localhost:3000
- ✅ http://localhost:5173
- ✅ http://example.com
- ✅ HAR QANDAY WEBSITE!

⚠️ Production'da HECH QACHON ishlatmang!
"""


# VARIANT 2: Production - Faqat kerakli origin'lar
# ✅ PRODUCTION UCHUN TAVSIYA ETILADI

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",       # React development
    "http://localhost:5173",       # Vite development
    "http://127.0.0.1:3000",       # Alternative localhost
    "https://example.com",         # Production frontend
    "https://www.example.com",     # www subdomain
    "https://app.example.com",     # app subdomain
]

"""
Bu aniq origin'lar ro'yxati.
Faqat shu ro'yxatdagi origin'lardan so'rovlar qabul qilinadi.
"""


# ==========================================
# STEP 5: ADDITIONAL SETTINGS (Optional)
# ==========================================

# Allow cookies and authorization headers
CORS_ALLOW_CREDENTIALS = True

"""
True bo'lsa:
- Cookies yuborilishi mumkin
- Authorization header yuborilishi mumkin
- Frontend'da credentials: 'include' ishlatish mumkin

⚠️ CORS_ALLOW_ALL_ORIGINS bilan birga ishlamaydi!
"""


# Allow specific HTTP methods
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

"""
Qaysi HTTP methodlar ruxsat berilgan.
Default qiymat yuqoridagi ro'yxat.
"""


# Allow specific headers in requests
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

"""
Request'da qo'shilishi mumkin bo'lgan headerlar.
Default qiymat yuqoridagi ro'yxat.
"""


# Expose specific headers to frontend
CORS_EXPOSE_HEADERS = [
    'Content-Length',
    'X-Total-Count',
    'X-Page-Number',
]

"""
Frontend'da JavaScript orqali o'qilishi mumkin bo'lgan 
response headerlar.

Masalan:
const totalCount = response.headers.get('X-Total-Count');
"""


# Preflight request cache duration
CORS_PREFLIGHT_MAX_AGE = 86400  # 24 hours in seconds

"""
Browser preflight response'ni qancha vaqt cache qiladi.
86400 = 24 soat
"""


# ==========================================
# STEP 6: COMPLETE EXAMPLE
# ==========================================

# Complete settings.py CORS configuration

# Development vs Production
import os

DEBUG = os.getenv('DEBUG', 'False') == 'True'

if DEBUG:
    # Development settings
    print("🔧 Development mode: CORS_ALLOW_ALL_ORIGINS = True")
    CORS_ALLOW_ALL_ORIGINS = True
else:
    # Production settings
    print("🔒 Production mode: Using CORS_ALLOWED_ORIGINS whitelist")
    CORS_ALLOWED_ORIGINS = os.getenv(
        'CORS_ALLOWED_ORIGINS',
        'https://example.com,https://www.example.com'
    ).split(',')

# Common settings for both
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_EXPOSE_HEADERS = [
    'Content-Length',
    'X-Total-Count',
]

CORS_PREFLIGHT_MAX_AGE = 86400


# ==========================================
# STEP 7: VERIFICATION
# ==========================================

"""
Server'ni ishga tushiring:

    python manage.py runserver

Boshqa terminalda test qiling:

    curl -H "Origin: http://localhost:3000" \\
         -H "Access-Control-Request-Method: GET" \\
         -X OPTIONS \\
         http://localhost:8000/api/books/

Kutilayotgan response:

    HTTP/1.1 200 OK
    Access-Control-Allow-Origin: http://localhost:3000
    Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
    Access-Control-Allow-Headers: accept, authorization, content-type, ...
    Access-Control-Max-Age: 86400
"""


# ==========================================
# TROUBLESHOOTING
# ==========================================

"""
❌ Problem 1: CORS errors hali ham bor

Yechim:
1. CorsMiddleware eng yuqorida ekanligini tekshiring
2. INSTALLED_APPS'da 'corsheaders' borligini tekshiring
3. Server'ni restart qiling
4. Browser cache'ni clear qiling


❌ Problem 2: Credentials error

Error: "Access-Control-Allow-Origin cannot be *"

Yechim:
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
CORS_ALLOW_CREDENTIALS = True


❌ Problem 3: OPTIONS request 403/405

Yechim:
CORS_ALLOW_METHODS'da 'OPTIONS' borligini tekshiring


❌ Problem 4: Custom headers blocked

Yechim:
CORS_ALLOW_HEADERS'ga custom header qo'shing:
CORS_ALLOW_HEADERS = [
    # ... default headers
    'x-my-custom-header',
]
"""


# ==========================================
# BEST PRACTICES
# ==========================================

"""
✅ DO (Qiling):

1. Production'da faqat kerakli origin'larni whitelist qiling
2. Environment variable'lardan foydalaning
3. HTTPS ishlatilishiga ishonch hosil qiling
4. Credentials kerak bo'lsagina CORS_ALLOW_CREDENTIALS = True qiling
5. Middleware ordering'ni to'g'ri saqlang


❌ DON'T (Qilmang):

1. Production'da CORS_ALLOW_ALL_ORIGINS = True
2. Wildcard (*) bilan credentials
3. HTTP origin'larni production'da whitelist qilish
4. Barcha custom headerlarni ruxsat berish
5. CorsMiddleware'ni noto'g'ri joyga qo'yish
"""


# ==========================================
# SUMMARY
# ==========================================

"""
Django CORS Setup - Qisqacha:

1. pip install django-cors-headers
2. INSTALLED_APPS'ga 'corsheaders' qo'shing
3. MIDDLEWARE'ning TOP'iga CorsMiddleware qo'shing
4. Development: CORS_ALLOW_ALL_ORIGINS = True
5. Production: CORS_ALLOWED_ORIGINS = [list]
6. Test qiling!

That's it! 
"""

print("✅ Django CORS sozlandi!")
print("\nKeyingi qadam:")
print("→ 03-cors-configuration.py'ni o'qing")