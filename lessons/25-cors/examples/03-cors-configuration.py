"""
CORS Configuration - Turli holatlar uchun sozlash
"""

# ==========================================
# SCENARIO 1: Simple React App (Development)
# ==========================================

# React app: http://localhost:3000
# Django API: http://localhost:8000

# Minimal configuration
CORS_ALLOW_ALL_ORIGINS = True

"""
✅ Afzalliklari:
- Juda tez sozlash
- Hech qanday origin'larni qo'shish kerak emas
- Development'da qulay

❌ Kamchiliklari:
- Xavfli (har qanday website'ga ruxsat)
- Production uchun mos emas
"""


# ==========================================
# SCENARIO 2: Multiple Frontend Apps
# ==========================================

# React: http://localhost:3000
# Vue: http://localhost:8080
# Angular: http://localhost:4200

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React
    "http://localhost:8080",  # Vue
    "http://localhost:4200",  # Angular
    "http://127.0.0.1:3000",  # Alternative
]

"""
✅ Xavfsizroq
❌ Har safar yangi frontend qo'shsangiz update qilish kerak
"""


# ==========================================
# SCENARIO 3: Localhost Any Port (Development)
# ==========================================

# localhost:3000, localhost:5173, localhost:any_port

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://localhost:\d+$",       # localhost with any port
    r"^http://127\.0\.0\.1:\d+$",    # 127.0.0.1 with any port
]

"""
Regex pattern qo'llab-quvvatlaydi:
✅ http://localhost:3000
✅ http://localhost:5173
✅ http://localhost:8080
✅ http://127.0.0.1:3000
❌ https://localhost:3000 (HTTPS emas)
❌ http://malicious.com
"""


# ==========================================
# SCENARIO 4: Production with Subdomains
# ==========================================

# Main: https://example.com
# WWW: https://www.example.com
# App: https://app.example.com
# API: https://api.example.com

# Option A: Explicit list (Recommended)
CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://www.example.com",
    "https://app.example.com",
]

# Option B: Regex pattern
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://([a-z0-9-]+\.)?example\.com$",
]

"""
Regex matches:
✅ https://example.com
✅ https://www.example.com
✅ https://app.example.com
✅ https://dashboard.example.com
❌ http://example.com (HTTP)
❌ https://malicious-example.com
"""


# ==========================================
# SCENARIO 5: Mobile App + Web App
# ==========================================

# Web: https://app.example.com
# Mobile: capacitor://localhost (Capacitor)
#         ionic://localhost (Ionic)

CORS_ALLOWED_ORIGINS = [
    "https://app.example.com",
    "capacitor://localhost",
    "ionic://localhost",
]

# Yoki development'da
if DEBUG:
    CORS_ALLOWED_ORIGINS += [
        "http://localhost:3000",
        "http://localhost:8100",  # Ionic dev
    ]


# ==========================================
# SCENARIO 6: Third-Party Integration
# ==========================================

# Sizning API'ingizni boshqa kompaniyalar ishlatadi

CORS_ALLOWED_ORIGINS = [
    # O'zingizning frontend'laringiz
    "https://app.example.com",
    "https://dashboard.example.com",
    
    # Partner company'lar
    "https://partner1.com",
    "https://partner2.com",
    "https://client-app.partner3.com",
]

"""
⚠️ Muhim:
- Har bir partner uchun aniq origin
- Wildcard ishlatmang
- Contract'da origin'ni documented qiling
"""


# ==========================================
# SCENARIO 7: Environment-Based Configuration
# ==========================================

import os

# .env fayldan o'qish
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

if ENVIRONMENT == 'development':
    # Development - local testing
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
    
elif ENVIRONMENT == 'staging':
    # Staging - testing server
    CORS_ALLOWED_ORIGINS = [
        "https://staging-app.example.com",
        "https://staging-dashboard.example.com",
    ]
    CORS_ALLOW_CREDENTIALS = True
    
elif ENVIRONMENT == 'production':
    # Production - live server
    CORS_ALLOWED_ORIGINS = [
        "https://app.example.com",
        "https://www.example.com",
        "https://dashboard.example.com",
    ]
    CORS_ALLOW_CREDENTIALS = True
else:
    # Unknown environment - very restrictive
    CORS_ALLOWED_ORIGINS = []


# ==========================================
# SCENARIO 8: Dynamic Origin from Database
# ==========================================

# Multi-tenant application
# Har bir client o'z domain'iga ega

class CustomCORSMiddleware:
    """
    Database'dan dynamic origin check qilish
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        origin = request.META.get('HTTP_ORIGIN')
        
        if origin:
            # Database'da origin bormi tekshirish
            from myapp.models import AllowedOrigin
            if AllowedOrigin.objects.filter(origin=origin, active=True).exists():
                response = self.get_response(request)
                response['Access-Control-Allow-Origin'] = origin
                response['Access-Control-Allow-Credentials'] = 'true'
                return response
        
        return self.get_response(request)


# ==========================================
# SCENARIO 9: API Key Based Access
# ==========================================

# Faqat valid API key bilan so'rov yuborilganda CORS ruxsat berish

CORS_ALLOW_HEADERS = [
    'accept',
    'authorization',
    'content-type',
    'x-api-key',  # Custom header
]

# View'da check qilish
from rest_framework.views import APIView
from rest_framework.response import Response

class ProtectedAPIView(APIView):
    def get(self, request):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key or not is_valid_api_key(api_key):
            return Response(
                {'error': 'Invalid API key'}, 
                status=401
            )
        
        return Response({'data': 'Protected data'})


# ==========================================
# SCENARIO 10: CORS with Authentication
# ==========================================

# JWT token bilan authenticated requests

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'authorization',  # Bearer token uchun
    'content-type',
]

# Frontend (JavaScript)
"""
fetch('http://localhost:8000/api/books/', {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJh...',
    },
    credentials: 'include',  # MUHIM!
})
"""


# ==========================================
# SCENARIO 11: File Upload with CORS
# ==========================================

# File upload qilishda multipart/form-data

CORS_ALLOW_HEADERS = [
    'accept',
    'authorization',
    'content-type',
    'content-disposition',  # File upload uchun
]

CORS_EXPOSE_HEADERS = [
    'Content-Disposition',  # File download uchun
]


# ==========================================
# SCENARIO 12: WebSocket with CORS
# ==========================================

# Django Channels WebSocket connections

# CORS settings (HTTP uchun)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# Channels settings (WebSocket uchun)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# WebSocket'da CORS manual check kerak
# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            # ... your routes
        )
    ),
})


# ==========================================
# ADVANCED: Custom CORS Configuration
# ==========================================

# Per-endpoint CORS settings

from corsheaders.signals import check_request_enabled

def cors_allow_api_to_everyone(sender, request, **kwargs):
    """
    /api/public/* endpoint'lari uchun barcha origin'larni ruxsat berish
    """
    if request.path.startswith('/api/public/'):
        return True
    return False

check_request_enabled.connect(cors_allow_api_to_everyone)


# ==========================================
# CONFIGURATION TEMPLATE
# ==========================================

"""
Complete production-ready configuration:
"""

import os

# Environment
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# CORS Settings
if DEBUG:
    # Development - permissive
    CORS_ALLOW_ALL_ORIGINS = True
else:
    # Production - restrictive
    cors_origins_str = os.getenv('CORS_ALLOWED_ORIGINS', '')
    CORS_ALLOWED_ORIGINS = [
        origin.strip() 
        for origin in cors_origins_str.split(',') 
        if origin.strip()
    ]
    
    # Fallback to default if not set
    if not CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS = [
            'https://example.com',
            'https://www.example.com',
        ]

# Common settings
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

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
    'X-Page-Number',
]

CORS_PREFLIGHT_MAX_AGE = 86400  # 24 hours


# ==========================================
# .ENV FILE EXAMPLE
# ==========================================

"""
# .env

DEBUG=False
ENVIRONMENT=production
CORS_ALLOWED_ORIGINS=https://example.com,https://www.example.com,https://app.example.com

# Development
# DEBUG=True
# ENVIRONMENT=development
"""


print("✅ CORS configurations ko'rib chiqildi!")
print("\nKeyingi qadam:")
print("→ 04-security-best-practices.md'ni o'qing")