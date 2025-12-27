# Dars 31: OAuth2 & Social Authentication

## Maqsad
Ushbu darsda OAuth2 protokoli va social authentication (Google, GitHub, Facebook) ni DRF loyihasiga qo'shishni o'rganamiz.

## Nazariy qism

### 1. OAuth2 nima?

**OAuth2** - bu foydalanuvchilarga uchinchi tomon ilovalarga o'z ma'lumotlariga kirish huquqini berish uchun ochiq standart protokol.

**Asosiy tushunchalar:**
- **Resource Owner** - Foydalanuvchi (siz)
- **Client** - Sizning ilovangiz
- **Authorization Server** - Google, GitHub, Facebook serveri
- **Resource Server** - Foydalanuvchi ma'lumotlari joylashgan server
- **Access Token** - Resurslarga kirish uchun token
- **Refresh Token** - Access tokenni yangilash uchun token

**OAuth2 Flow:**
```
1. Foydalanuvchi "Login with Google" tugmasini bosadi
2. Google login sahifasiga yo'naltiriladi
3. Foydalanuvchi login qiladi va ruxsat beradi
4. Google Authorization code beradi
5. Sizning backend Authorization code ni Access Token ga almashtiradi
6. Access Token yordamida foydalanuvchi ma'lumotlarini oladi
7. Foydalanuvchini ro'yxatdan o'tkazadi yoki tizimga kiritadi
```

### 2. Social Authentication afzalliklari

**Foydalanuvchilar uchun:**
- ✅ Yangi parol yaratish shart emas
- ✅ Tez va oson ro'yxatdan o'tish
- ✅ Xavfsiz (Google/GitHub autentifikatsiyasi)

**Dasturchilar uchun:**
- ✅ Parol saqlash va xavfsizlik muammolari yo'q
- ✅ Email tasdiqlash avtomatik
- ✅ Foydalanuvchi tajribasini yaxshilaydi

### 3. django-allauth kutubxonasi

`django-allauth` - Django uchun eng mashhur social authentication kutubxonasi.

**Qo'llab-quvvatlanadigan providerlar:**
- Google
- GitHub
- Facebook
- Twitter
- Instagram
- LinkedIn
- va boshqa 50+ provider

---

## Amaliy qism

### 1-qism: django-allauth o'rnatish

#### 1. Kerakli paketlarni o'rnatish

```bash
pip install django-allauth
pip install dj-rest-auth[with_social]
```

#### 2. settings.py sozlash

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Yangi
    
    # Third party
    'rest_framework',
    'rest_framework.authtoken',
    
    # allauth
    'allauth',  # Yangi
    'allauth.account',  # Yangi
    'allauth.socialaccount',  # Yangi
    'allauth.socialaccount.providers.google',  # Yangi
    'allauth.socialaccount.providers.github',  # Yangi
    
    # dj-rest-auth
    'dj_rest_auth',  # Yangi
    'dj_rest_auth.registration',  # Yangi
    
    # Your apps
    'books',
    'api',
]

# SITE_ID kerak
SITE_ID = 1

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default
    'allauth.account.auth_backends.AuthenticationBackend',  # allauth
]

# allauth sozlamalari
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # yoki 'mandatory'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Social auth sozlamalari (keyinroq to'ldiramiz)
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    }
}
```

#### 3. URL sozlash

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    
    # allauth URLs
    path('accounts/', include('allauth.urls')),
    
    # dj-rest-auth URLs
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # Social auth URLs
    path('api/v1/auth/social/', include('allauth.socialaccount.urls')),
]
```

#### 4. Migration qilish

```bash
python manage.py migrate
```

---

### 2-qism: Google OAuth2 sozlash

#### 1. Google Cloud Console da loyiha yaratish

1. [Google Cloud Console](https://console.cloud.google.com/) ga kiring
2. Yangi loyiha yarating: "Library API"
3. **APIs & Services** > **Credentials** ga o'ting
4. **OAuth consent screen** ni sozlang:
   - User Type: External
   - App name: Library API
   - User support email: sizning emailingiz
   - Developer contact: sizning emailingiz

5. **Credentials** yarating:
   - Create Credentials > OAuth 2.0 Client ID
   - Application type: Web application
   - Name: Library API Web Client
   - Authorized JavaScript origins:
     ```
     http://localhost:3000
     http://127.0.0.1:8000
     ```
   - Authorized redirect URIs:
     ```
     http://127.0.0.1:8000/accounts/google/login/callback/
     http://localhost:3000/auth/google/callback
     ```

6. **Client ID** va **Client Secret** ni nusxalang

#### 2. Django admin da sozlash

```bash
python manage.py createsuperuser  # agar yo'q bo'lsa
python manage.py runserver
```

1. Admin panelga kiring: http://127.0.0.1:8000/admin/
2. **Sites** > **example.com** ni tahrirlang:
   - Domain name: `127.0.0.1:8000`
   - Display name: `Library API`

3. **Social applications** > **Add social application**:
   - Provider: Google
   - Name: Google OAuth
   - Client id: (Google dan olgan Client ID)
   - Secret key: (Google dan olgan Client Secret)
   - Sites: `127.0.0.1:8000` ni tanlang

#### 3. Test qilish

**Frontend dan test (Postman bilan mumkin emas, browser kerak):**

```html
<!-- test.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Google Login Test</title>
</head>
<body>
    <h1>Google OAuth Test</h1>
    <a href="http://127.0.0.1:8000/accounts/google/login/?process=login">
        Login with Google
    </a>
</body>
</html>
```

Browser da ochsangiz, Google login sahifasiga yo'naltirilasiz.

---

### 3-qism: GitHub OAuth sozlash

#### 1. GitHub da OAuth App yaratish

1. GitHub > Settings > Developer settings > OAuth Apps
2. **New OAuth App**:
   - Application name: Library API
   - Homepage URL: `http://127.0.0.1:8000`
   - Authorization callback URL: `http://127.0.0.1:8000/accounts/github/login/callback/`
3. **Client ID** va **Client Secret** ni oling

#### 2. Django admin da sozlash

1. **Social applications** > **Add social application**:
   - Provider: GitHub
   - Name: GitHub OAuth
   - Client id: (GitHub dan olgan)
   - Secret key: (GitHub dan olgan)
   - Sites: `127.0.0.1:8000` ni tanlang

#### 3. Test qilish

```html
<a href="http://127.0.0.1:8000/accounts/github/login/?process=login">
    Login with GitHub
</a>
```

---

### 4-qism: Custom Social Auth View yaratish

Ba'zan default allauth flowni o'zgartirish kerak bo'ladi. Masalan, foydalanuvchi social login qilganda qo'shimcha ma'lumotlar saqlash.

#### Custom Adapter yaratish

```python
# api/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Social login dan oldin chaqiriladi
        """
        # Email orqali mavjud foydalanuvchini topish
        if sociallogin.is_existing:
            return
        
        if 'email' in sociallogin.account.extra_data:
            email = sociallogin.account.extra_data['email']
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass
    
    def save_user(self, request, sociallogin, form=None):
        """
        Yangi foydalanuvchi yaratilganda chaqiriladi
        """
        user = super().save_user(request, sociallogin, form)
        
        # Qo'shimcha ma'lumotlar saqlash
        data = sociallogin.account.extra_data
        if 'picture' in data:
            user.profile_picture = data['picture']
        if 'name' in data:
            parts = data['name'].split(' ', 1)
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
        
        user.save()
        return user

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Oddiy registratsiyada chaqiriladi
        """
        user = super().save_user(request, user, form, commit=False)
        
        # Qo'shimcha mantiq
        user.is_active = True  # Email tasdiqsiz faollashtirish
        
        if commit:
            user.save()
        return user
```

#### settings.py ga qo'shish

```python
# Custom adapters
SOCIALACCOUNT_ADAPTER = 'api.adapters.CustomSocialAccountAdapter'
ACCOUNT_ADAPTER = 'api.adapters.CustomAccountAdapter'
```

---

### 5-qism: REST API uchun Social Auth

Agar frontend alohida bo'lsa (React, Vue, Flutter), u holda REST API uchun maxsus endpoint kerak.

#### Google OAuth REST endpoint

```python
# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/auth/google/callback"
    client_class = OAuth2Client

class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://localhost:3000/auth/github/callback"
    client_class = OAuth2Client
```

#### URL sozlash

```python
# api/urls.py
from django.urls import path
from .views import GoogleLogin, GitHubLogin

urlpatterns = [
    # ... boshqa URLlar
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/github/', GitHubLogin.as_view(), name='github_login'),
]
```

#### Frontend dan foydalanish (React misoli)

```javascript
// Google OAuth flow
const loginWithGoogle = async () => {
  // 1. Google OAuth URL ga yo'naltirish
  const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth';
  const params = {
    client_id: 'YOUR_GOOGLE_CLIENT_ID',
    redirect_uri: 'http://localhost:3000/auth/google/callback',
    response_type: 'code',
    scope: 'profile email',
  };
  
  const url = `${googleAuthUrl}?${new URLSearchParams(params)}`;
  window.location.href = url;
};

// 2. Callback sahifada (http://localhost:3000/auth/google/callback)
const handleGoogleCallback = async () => {
  const code = new URLSearchParams(window.location.search).get('code');
  
  // 3. Backend ga code yuborish
  const response = await fetch('http://127.0.0.1:8000/api/v1/auth/google/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ code }),
  });
  
  const data = await response.json();
  // 4. Token ni saqlash
  localStorage.setItem('token', data.key);
};
```

---

## Testing

### 1. Manual testing (Browser)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Social Auth Test</title>
</head>
<body>
    <h1>Social Authentication Test</h1>
    
    <h2>Login Options:</h2>
    <ul>
        <li>
            <a href="http://127.0.0.1:8000/accounts/google/login/?process=login">
                Login with Google
            </a>
        </li>
        <li>
            <a href="http://127.0.0.1:8000/accounts/github/login/?process=login">
                Login with GitHub
            </a>
        </li>
    </ul>
    
    <h2>Current Status:</h2>
    <p id="status">Not logged in</p>
    
    <script>
        // Token borligini tekshirish
        fetch('http://127.0.0.1:8000/api/v1/auth/user/', {
            headers: {
                'Authorization': 'Token ' + localStorage.getItem('token')
            }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('status').textContent = 
                'Logged in as: ' + data.email;
        })
        .catch(() => {
            document.getElementById('status').textContent = 'Not logged in';
        });
    </script>
</body>
</html>
```

### 2. Unit testing

```python
# api/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount, SocialApp
from django.contrib.sites.models import Site

User = get_user_model()

class SocialAuthTestCase(TestCase):
    def setUp(self):
        # Site yaratish
        self.site = Site.objects.create(
            domain='testserver',
            name='Test Site'
        )
        
        # Google Social App yaratish
        self.google_app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id='test-client-id',
            secret='test-secret',
        )
        self.google_app.sites.add(self.site)
    
    def test_social_account_creation(self):
        """Social account yaratilishini tekshirish"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        
        social_account = SocialAccount.objects.create(
            user=user,
            provider='google',
            uid='123456789',
            extra_data={'email': 'test@example.com'}
        )
        
        self.assertEqual(user.socialaccount_set.count(), 1)
        self.assertEqual(social_account.provider, 'google')
    
    def test_social_account_email_matching(self):
        """Email orqali foydalanuvchini topish"""
        # Mavjud foydalanuvchi
        existing_user = User.objects.create_user(
            username='existing',
            email='existing@example.com'
        )
        
        # Social account yaratish
        social_account = SocialAccount.objects.create(
            user=existing_user,
            provider='google',
            uid='987654321',
            extra_data={'email': 'existing@example.com'}
        )
        
        # Email orqali topish
        found_accounts = SocialAccount.objects.filter(
            extra_data__email='existing@example.com'
        )
        
        self.assertEqual(found_accounts.count(), 1)
        self.assertEqual(found_accounts.first().user, existing_user)
```

---

## Xavfsizlik masalalari

### 1. State parametri

OAuth2 da CSRF hujumlaridan himoyalanish uchun `state` parametri ishlatiladi:

```python
# settings.py
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'AUTH_PARAMS': {
            'access_type': 'online',
            'state': 'random-string',  # CSRF protection
        }
    }
}
```

### 2. HTTPS majburiy

Production da har doim HTTPS ishlatish kerak:

```python
# settings.py
if not DEBUG:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

### 3. Scope cheklash

Faqat kerakli ma'lumotlarni so'rang:

```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
            # 'https://www.googleapis.com/auth/drive'  # Kerak bo'lsa
        ],
    }
}
```

### 4. Token xavfsizligi

```python
# Access token ni secure cookie da saqlash
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'auth-token'
JWT_AUTH_SECURE = True  # HTTPS da
JWT_AUTH_HTTPONLY = True  # JavaScript dan o'qib bo'lmaydi
```

---

## Best Practices

### 1. Email tasdiqni yoqish

```python
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
```

### 2. Username ixtiyoriy qilish

```python
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
```

### 3. Auto-signup ni boshqarish

```python
SOCIALACCOUNT_AUTO_SIGNUP = True  # Avtomatik ro'yxatdan o'tkazish

# Yoki manual
SOCIALACCOUNT_AUTO_SIGNUP = False  # Qo'shimcha ma'lumot so'rash
```

### 4. Duplicate account prevention

```python
# api/adapters.py
def pre_social_login(self, request, sociallogin):
    if sociallogin.is_existing:
        return
    
    email = sociallogin.account.extra_data.get('email')
    if not email:
        return
    
    try:
        user = User.objects.get(email=email)
        sociallogin.connect(request, user)
    except User.DoesNotExist:
        pass
```

---

## Keng tarqalgan xatolar

### 1. Redirect URI mismatch

```
Error: redirect_uri_mismatch
```

**Sabab:** Google Console da ko'rsatilgan URL bilan haqiqiy URL mos kelmaydi

**Yechim:**
- Google Console da to'g'ri URL ni tekshiring
- `http://` vs `https://` farqini tekshiring
- Trailing slash (`/`) borligini tekshiring

### 2. Site matching query does not exist

```
Site matching query does not exist.
```

**Yechim:**
```python
python manage.py shell
>>> from django.contrib.sites.models import Site
>>> site = Site.objects.get_current()
>>> site.domain = '127.0.0.1:8000'
>>> site.name = 'Library API'
>>> site.save()
```

### 3. SocialApp not found

```
SocialApp matching query does not exist.
```

**Yechim:**
Admin panelda Social Application yaratishni unutmang va Sites ni to'g'ri tanlang.

---

## Qo'shimcha providerlar

### Facebook OAuth

```python
# settings.py
INSTALLED_APPS += [
    'allauth.socialaccount.providers.facebook',
]

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
        ],
    }
}
```

### Twitter OAuth

```python
INSTALLED_APPS += [
    'allauth.socialaccount.providers.twitter',
]

SOCIALACCOUNT_PROVIDERS = {
    'twitter': {
        'SCOPE': ['email'],
    }
}
```

---

## Xulosa

Ushbu darsda biz o'rgandik:

1. ✅ OAuth2 protokoli va uning ishlash prinsipi
2. ✅ django-allauth kutubxonasini o'rnatish va sozlash
3. ✅ Google OAuth2 integratsiyasi
4. ✅ GitHub OAuth integratsiyasi
5. ✅ Custom adapter va REST API endpoints yaratish
6. ✅ Xavfsizlik va best practices

**Keyingi dars:** Two-Factor Authentication (2FA)

---

## Foydali resurslar

- [django-allauth Documentation](https://django-allauth.readthedocs.io/)
- [Google OAuth2 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [GitHub OAuth Documentation](https://docs.github.com/en/developers/apps/building-oauth-apps)
- [dj-rest-auth Documentation](https://dj-rest-auth.readthedocs.io/)