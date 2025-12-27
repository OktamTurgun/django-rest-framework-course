"""
Google OAuth2 Integration bilan Django
========================================

Bu fayl django-allauth yordamida Google OAuth2 ni
qanday sozlash va ishlatishni ko'rsatadi.
"""

# ============================================================================
# 1. Google Cloud Console Setup
# ============================================================================

"""
Google Cloud Console da OAuth2 sozlash:
========================================

QADAM 1: Loyiha yaratish
-----------------------
1. console.cloud.google.com ga kiring
2. Yangi loyiha yarating: "Library API"

QADAM 2: OAuth Consent Screen
-----------------------------
1. APIs & Services > OAuth consent screen
2. User Type: External
3. App Information:
   - App name: Library API
   - User support email: your-email@example.com
   - Developer contact: your-email@example.com
4. Scopes: Add or remove scopes
   - .../auth/userinfo.email
   - .../auth/userinfo.profile
   - openid
5. Test users: Add your email

QADAM 3: Credentials yaratish
-----------------------------
1. APIs & Services > Credentials
2. Create Credentials > OAuth 2.0 Client ID
3. Application type: Web application
4. Name: Library API Web Client
5. Authorized JavaScript origins:
   - http://localhost:3000
   - http://127.0.0.1:8000
6. Authorized redirect URIs:
   - http://127.0.0.1:8000/accounts/google/login/callback/
   - http://localhost:3000/auth/google/callback
7. Save

QADAM 4: Credentials ni olish
-----------------------------
Client ID: 123456789-abc.apps.googleusercontent.com
Client Secret: GOCSPX-abc123def456ghi789
"""


# ============================================================================
# 2. Django Settings Configuration
# ============================================================================

# settings.py
GOOGLE_OAUTH_SETTINGS = """
# ============================================================================
# GOOGLE OAUTH2 SETTINGS
# ============================================================================

import os
from pathlib import Path

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required for allauth
    
    # Third party
    'rest_framework',
    'rest_framework.authtoken',
    
    # django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # Google provider
    
    # dj-rest-auth
    'dj_rest_auth',
    'dj_rest_auth.registration',
    
    # Your apps
    'books',
    'api',
]

# ============================================================================
# SITE CONFIGURATION
# ============================================================================

SITE_ID = 1

# ============================================================================
# AUTHENTICATION BACKENDS
# ============================================================================

AUTHENTICATION_BACKENDS = [
    # Django default
    'django.contrib.auth.backends.ModelBackend',
    
    # django-allauth
    'allauth.account.auth_backends.AuthenticationBackend',
]

# ============================================================================
# ALLAUTH SETTINGS
# ============================================================================

# Email settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # 'mandatory', 'optional', 'none'
ACCOUNT_UNIQUE_EMAIL = True

# Authentication
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # 'username', 'email', 'username_email'
ACCOUNT_USERNAME_REQUIRED = False

# Signup
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True

# Login/Logout
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = False

# Password
ACCOUNT_PASSWORD_MIN_LENGTH = 8

# Session
ACCOUNT_SESSION_REMEMBER = True

# ============================================================================
# SOCIAL ACCOUNT SETTINGS
# ============================================================================

SOCIALACCOUNT_AUTO_SIGNUP = True  # Avtomatik signup
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = True

# Google provider sozlamalari
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'key': ''
        },
        'VERIFIED_EMAIL': True,
    }
}

# ============================================================================
# REST FRAMEWORK
# ============================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

# ============================================================================
# DJ-REST-AUTH SETTINGS
# ============================================================================

REST_USE_JWT = False  # Token authentication ishlatamiz
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False
"""

print("Google OAuth2 Settings:")
print(GOOGLE_OAUTH_SETTINGS)


# ============================================================================
# 3. URL Configuration
# ============================================================================

# config/urls.py
GOOGLE_OAUTH_URLS = """
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Your API
    path('api/v1/', include('api.urls')),
    
    # django-allauth URLs (browser-based social auth)
    path('accounts/', include('allauth.urls')),
    
    # dj-rest-auth URLs (REST API auth)
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),
]
"""

print("\n" + "="*70)
print("URL Configuration:")
print("="*70)
print(GOOGLE_OAUTH_URLS)


# ============================================================================
# 4. Environment Variables
# ============================================================================

# .env file
ENV_EXAMPLE = """
# Google OAuth2 Credentials
GOOGLE_CLIENT_ID=123456789-abc.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abc123def456ghi789

# Django Settings
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
"""

print("\n" + "="*70)
print(".env file example:")
print("="*70)
print(ENV_EXAMPLE)


# ============================================================================
# 5. Admin Panel Setup
# ============================================================================

def setup_admin_panel():
    """
    Django Admin panelda Google OAuth sozlash qadamlari
    """
    print("\n" + "="*70)
    print("ADMIN PANEL SETUP")
    print("="*70)
    
    steps = """
1. Migratsiyalarni bajarish:
   python manage.py migrate

2. Superuser yaratish:
   python manage.py createsuperuser

3. Server ishga tushirish:
   python manage.py runserver

4. Admin panelga kirish:
   http://127.0.0.1:8000/admin/

5. Sites ni sozlash:
   - Sites > example.com ni tahrirlang
   - Domain name: 127.0.0.1:8000
   - Display name: Library API
   - Save

6. Social Applications yaratish:
   - Social applications > Add social application
   - Provider: Google
   - Name: Google OAuth2
   - Client id: (Google Console dan)
   - Secret key: (Google Console dan)
   - Sites: 127.0.0.1:8000 ni tanlang
   - Save
    """
    
    print(steps)


# ============================================================================
# 6. Google Login View (Browser-based)
# ============================================================================

# Test HTML file
TEST_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google OAuth Test</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            background: white;
            color: #333;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            color: #667eea;
        }
        .google-btn {
            display: block;
            width: 100%;
            padding: 15px;
            background: #4285f4;
            color: white;
            text-decoration: none;
            text-align: center;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            margin: 20px 0;
            transition: background 0.3s;
        }
        .google-btn:hover {
            background: #357ae8;
        }
        .info {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .info h3 {
            margin-top: 0;
            color: #667eea;
        }
        .status {
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .success {
            background: #d4edda;
            color: #155724;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
        }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            color: #e83e8c;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Google OAuth2 Test</h1>
        
        <div class="info">
            <h3>Qanday ishlaydi?</h3>
            <ol>
                <li>Login tugmasini bosing</li>
                <li>Google login sahifasiga yo'naltirilasiz</li>
                <li>Google accountingizni tanlang</li>
                <li>Ilovaga ruxsat bering</li>
                <li>Callback URL ga qaytasiz</li>
            </ol>
        </div>
        
        <a href="http://127.0.0.1:8000/accounts/google/login/?process=login" 
           class="google-btn">
            🔐 Login with Google
        </a>
        
        <div id="status" class="status">
            <strong>Status:</strong> Not logged in
        </div>
        
        <div class="info">
            <h3>Callback URL:</h3>
            <code>http://127.0.0.1:8000/accounts/google/login/callback/</code>
        </div>
    </div>
    
    <script>
        // URL dan error parametrini tekshirish
        const urlParams = new URLSearchParams(window.location.search);
        const error = urlParams.get('error');
        const statusDiv = document.getElementById('status');
        
        if (error) {
            statusDiv.className = 'status error';
            statusDiv.innerHTML = '<strong>Error:</strong> ' + error;
        }
        
        // Token borligini tekshirish
        const token = localStorage.getItem('auth_token');
        if (token) {
            statusDiv.className = 'status success';
            statusDiv.innerHTML = '<strong>Status:</strong> ✅ Logged in';
        }
    </script>
</body>
</html>
"""

print("\n" + "="*70)
print("TEST HTML FILE (save as test.html):")
print("="*70)
print(TEST_HTML)


# ============================================================================
# 7. REST API View (for Frontend apps)
# ============================================================================

# api/views.py
REST_API_VIEW = """
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLoginView(SocialLoginView):
    '''
    Google OAuth2 login endpoint for REST API clients
    
    Frontend (React, Vue, Flutter) dan foydalanish uchun.
    
    Flow:
    1. Frontend foydalanuvchini Google ga yo'naltiradi
    2. Google callback URL ga code yuboradi
    3. Frontend code ni backend ga POST qiladi
    4. Backend code ni token ga almashtiradi
    5. Backend user yaratadi/login qiladi va token qaytaradi
    '''
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/auth/google/callback"
    client_class = OAuth2Client

# api/urls.py
from django.urls import path
from .views import GoogleLoginView

urlpatterns = [
    # ... other URLs
    path('auth/google/', GoogleLoginView.as_view(), name='google_login'),
]
"""

print("\n" + "="*70)
print("REST API VIEW:")
print("="*70)
print(REST_API_VIEW)


# ============================================================================
# 8. Frontend Integration Example (React)
# ============================================================================

REACT_EXAMPLE = """
// React component for Google OAuth

import React from 'react';

const GoogleLoginButton = () => {
  const handleGoogleLogin = () => {
    // 1. Google OAuth URL yaratish
    const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth';
    const redirectUri = 'http://localhost:3000/auth/google/callback';
    
    const params = new URLSearchParams({
      client_id: process.env.REACT_APP_GOOGLE_CLIENT_ID,
      redirect_uri: redirectUri,
      response_type: 'code',
      scope: 'profile email openid',
      access_type: 'online',
    });
    
    // 2. Google ga yo'naltirish
    window.location.href = `${googleAuthUrl}?${params}`;
  };
  
  return (
    <button onClick={handleGoogleLogin}>
      Login with Google
    </button>
  );
};

// Callback component
const GoogleCallback = () => {
  React.useEffect(() => {
    const handleCallback = async () => {
      // 3. URL dan code olish
      const params = new URLSearchParams(window.location.search);
      const code = params.get('code');
      
      if (!code) {
        console.error('No authorization code found');
        return;
      }
      
      try {
        // 4. Backend ga code yuborish
        const response = await fetch('http://127.0.0.1:8000/api/v1/auth/google/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            code: code,
          }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
          // 5. Token ni saqlash
          localStorage.setItem('auth_token', data.key);
          
          // 6. Dashboard ga yo'naltirish
          window.location.href = '/dashboard';
        } else {
          console.error('Login failed:', data);
        }
      } catch (error) {
        console.error('Error during login:', error);
      }
    };
    
    handleCallback();
  }, []);
  
  return <div>Processing login...</div>;
};

export { GoogleLoginButton, GoogleCallback };
"""

print("\n" + "="*70)
print("REACT INTEGRATION EXAMPLE:")
print("="*70)
print(REACT_EXAMPLE)


# ============================================================================
# 9. Testing with Postman (Manual)
# ============================================================================

def postman_testing_guide():
    """
    Postman bilan test qilish qo'llanmasi
    
    Eslatma: OAuth2 flow uchun browser kerak, lekin
    agar code ni qo'lda olgan bo'lsangiz, Postman dan test qilish mumkin.
    """
    print("\n" + "="*70)
    print("POSTMAN TESTING GUIDE")
    print("="*70)
    
    guide = """
Postman bilan to'liq OAuth2 flowni test qilish qiyin, chunki
Google login sahifasi browser da ochilishi kerak.

Lekin agar sizda authorization code bo'lsa, Postman dan 
Token ga almashtirish mumkin:

1. Authorization code olish (Browser da):
   http://127.0.0.1:8000/accounts/google/login/?process=login
   
   Callback URL dan code ni nusxalang:
   http://127.0.0.1:8000/accounts/google/login/callback/?code=4/0AY0e...

2. Postman da POST request:
   URL: http://127.0.0.1:8000/api/v1/auth/google/
   Method: POST
   Headers: Content-Type: application/json
   Body (raw JSON):
   {
       "code": "4/0AY0e-g7X..."
   }

3. Response:
   {
       "key": "your-auth-token-here",
       "user": {
           "id": 1,
           "username": "john_doe",
           "email": "john@example.com"
       }
   }

4. Keyingi requestlarda token ishlatish:
   Headers: Authorization: Token your-auth-token-here
    """
    
    print(guide)


# ============================================================================
# 10. Common Issues and Solutions
# ============================================================================

def common_issues():
    """
    Google OAuth bilan ishlashda uchraydigan muammolar
    """
    print("\n" + "="*70)
    print("COMMON ISSUES AND SOLUTIONS")
    print("="*70)
    
    issues = [
        {
            "issue": "redirect_uri_mismatch",
            "cause": "Callback URL Google Console da ko'rsatilgan bilan mos kelmaydi",
            "solution": "Google Console > Credentials > Edit > Authorized redirect URIs ni tekshiring\n"
                       "To'g'ri format: http://127.0.0.1:8000/accounts/google/login/callback/\n"
                       "Trailing slash (/) ni unutmang!"
        },
        {
            "issue": "Site matching query does not exist",
            "cause": "django.contrib.sites to'g'ri sozlanmagan",
            "solution": "python manage.py shell\n"
                       ">>> from django.contrib.sites.models import Site\n"
                       ">>> site = Site.objects.get_current()\n"
                       ">>> site.domain = '127.0.0.1:8000'\n"
                       ">>> site.name = 'Library API'\n"
                       ">>> site.save()"
        },
        {
            "issue": "SocialApp matching query does not exist",
            "cause": "Admin panelda Google Social Application yaratilmagan",
            "solution": "Admin > Social applications > Add social application\n"
                       "Provider: Google, Client ID va Secret ni kiriting\n"
                       "Sites: 127.0.0.1:8000 ni tanlang"
        },
        {
            "issue": "Invalid client error",
            "cause": "Client ID yoki Secret noto'g'ri",
            "solution": "Google Console dan Client credentials ni qayta nusxalang\n"
                       ".env faylni tekshiring"
        },
    ]
    
    for idx, issue in enumerate(issues, 1):
        print(f"\n{idx}. {issue['issue']}")
        print(f"   Cause: {issue['cause']}")
        print(f"   Solution:\n   {issue['solution']}")
    
    print("\n" + "="*70)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "🔐" * 35)
    print("GOOGLE OAUTH2 INTEGRATION GUIDE")
    print("🔐" * 35)
    
    setup_admin_panel()
    postman_testing_guide()
    common_issues()
    
    print("\n" + "✅" * 35)
    print("SETUP COMPLETE!")
    print("✅" * 35)
    
    print("\nNext steps:")
    print("1. Google Cloud Console da OAuth2 sozlang")
    print("2. .env faylda credentials kiriting")
    print("3. python manage.py migrate")
    print("4. Admin panelda Social Application yarating")
    print("5. test.html faylni browser da oching")
    print("6. Login tugmasini bosing va test qiling!")


"""
XULOSA:
=======

Google OAuth2 Integration qadamlari:
1. Google Cloud Console da OAuth2 app yaratish
2. django-allauth o'rnatish va sozlash
3. Admin panelda Social Application yaratish
4. Browser da test qilish yoki REST API orqali
5. Frontend (React) dan integration

MUHIM FAYLLAR:
- settings.py: INSTALLED_APPS, SOCIALACCOUNT_PROVIDERS
- urls.py: allauth URLs
- .env: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
- Admin panel: Social Applications

CALLBACK URLs:
- Browser: /accounts/google/login/callback/
- REST API: Frontend dan o'zingiz belgilaysiz
"""