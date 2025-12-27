# Homework 31: OAuth2 & Social Authentication

## Maqsad
Library API loyihasiga Google va GitHub orqali login qilish imkoniyatini qo'shish va maxsus social auth flow yaratish.

---

## Vazifa 1: Google OAuth2 integratsiyasi (30 ball)

### 1.1 Google Cloud Console sozlash (10 ball)

**Topshiriq:**
1. Google Cloud Console da yangi loyiha yarating
2. OAuth consent screen ni to'liq sozlang
3. OAuth 2.0 Client ID yarating
4. Redirect URI larni to'g'ri sozlang

**Tekshirish:**
- [ ] Google Cloud loyihasi yaratilgan
- [ ] OAuth consent screen to'ldirilgan
- [ ] Client ID va Secret olindi
- [ ] Redirect URI lar qo'shilgan:
  ```
  http://127.0.0.1:8000/accounts/google/login/callback/
  http://localhost:3000/auth/google/callback
  ```

### 1.2 Django sozlash (10 ball)

**Topshiriq:**
1. `django-allauth` va `dj-rest-auth` ni o'rnating
2. `settings.py` ni to'liq sozlang
3. Kerakli migratsiyalarni bajaring
4. Admin panelda Social Application yarating

**Tekshirish:**
```python
# settings.py
INSTALLED_APPS = [
    # ...
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth',
    'dj_rest_auth.registration',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
```

### 1.3 Google Login test (10 ball)

**Topshiriq:**
1. Test HTML sahifa yarating
2. Google login tugmasi qo'shing
3. Login flowni to'liq test qiling

**Test HTML:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Google Login Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
        }
        .button {
            display: inline-block;
            padding: 10px 20px;
            background: #4285f4;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 10px 0;
        }
        .button:hover {
            background: #357ae8;
        }
    </style>
</head>
<body>
    <h1>Library API - Social Login</h1>
    <a href="http://127.0.0.1:8000/accounts/google/login/?process=login" class="button">
        🔐 Login with Google
    </a>
    <div id="status"></div>
</body>
</html>
```

**Tekshirish:**
- [ ] Google login sahifasiga redirect bo'ladi
- [ ] Login qilgandan keyin callback URL ga qaytadi
- [ ] Foydalanuvchi yaratiladi yoki tizimga kiradi
- [ ] Token olinadi

---

## Vazifa 2: GitHub OAuth integratsiyasi (25 ball)

### 2.1 GitHub OAuth App yaratish (10 ball)

**Topshiriq:**
1. GitHub Settings > Developer settings > OAuth Apps ga o'ting
2. Yangi OAuth App yarating
3. Callback URL ni to'g'ri sozlang

**Tekshirish:**
- [ ] GitHub OAuth App yaratilgan
- [ ] Client ID va Secret olindi
- [ ] Callback URL: `http://127.0.0.1:8000/accounts/github/login/callback/`

### 2.2 Django ga qo'shish (10 ball)

**Topshiriq:**
1. GitHub provider ni `INSTALLED_APPS` ga qo'shing
2. Admin panelda GitHub Social Application yarating
3. URL larni sozlang

```python
# settings.py
INSTALLED_APPS += [
    'allauth.socialaccount.providers.github',
]

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    }
}
```

### 2.3 GitHub Login test (5 ball)

**Topshiriq:**
Test HTML sahifaga GitHub tugmasini qo'shing:

```html
<a href="http://127.0.0.1:8000/accounts/github/login/?process=login" class="button">
    🐙 Login with GitHub
</a>
```

**Tekshirish:**
- [ ] GitHub login ishlaydi
- [ ] Foydalanuvchi ma'lumotlari to'g'ri olinadi
- [ ] Email va username saqlandi

---

## Vazifa 3: Custom Social Adapter (25 ball)

### 3.1 Custom Adapter yaratish (15 ball)

**Topshiriq:**
`api/adapters.py` faylida custom adapter yarating:

```python
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

class LibrarySocialAccountAdapter(DefaultSocialAccountAdapter):
    
    def pre_social_login(self, request, sociallogin):
        """
        Social login dan oldin:
        - Agar email bo'yicha foydalanuvchi bor bo'lsa, ulang
        - Agar yo'q bo'lsa, yangi yaratilsin
        """
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
    
    def save_user(self, request, sociallogin, form=None):
        """
        Yangi foydalanuvchi yaratilganda:
        - Profile picture ni saqlang
        - First name va Last name ni ajrating
        - Bio ga social provider nomini yozing
        """
        user = super().save_user(request, sociallogin, form)
        
        data = sociallogin.account.extra_data
        
        # Profile picture
        if 'picture' in data:
            user.profile_picture = data['picture']
        elif 'avatar_url' in data:  # GitHub
            user.profile_picture = data['avatar_url']
        
        # Name
        if 'name' in data and data['name']:
            parts = data['name'].split(' ', 1)
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
        
        # Bio
        provider = sociallogin.account.provider
        user.bio = f"Registered via {provider.capitalize()}"
        
        user.save()
        return user
```

**Tekshirish:**
- [ ] Adapter yaratilgan
- [ ] `pre_social_login` metodi ishlaydi
- [ ] `save_user` metodi qo'shimcha ma'lumotlarni saqlaydi
- [ ] settings.py da adapter ulangan:
  ```python
  SOCIALACCOUNT_ADAPTER = 'api.adapters.LibrarySocialAccountAdapter'
  ```

### 3.2 Test qilish (10 ball)

**Topshiriq:**
Unit test yozing:

```python
# api/tests/test_social_auth.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount, SocialApp
from django.contrib.sites.models import Site

User = get_user_model()

class SocialAuthAdapterTestCase(TestCase):
    
    def setUp(self):
        self.site = Site.objects.get_current()
        self.site.domain = 'testserver'
        self.site.save()
        
        self.google_app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id='test-id',
            secret='test-secret',
        )
        self.google_app.sites.add(self.site)
    
    def test_existing_email_linking(self):
        """
        Agar email mavjud bo'lsa, social account ulanishi kerak
        """
        # Mavjud user
        user = User.objects.create_user(
            username='existing',
            email='test@example.com'
        )
        
        # Social account yaratish
        social = SocialAccount.objects.create(
            user=user,
            provider='google',
            uid='123456',
            extra_data={'email': 'test@example.com'}
        )
        
        self.assertEqual(user.socialaccount_set.count(), 1)
    
    def test_new_user_with_picture(self):
        """
        Yangi user uchun picture va name saqlashi kerak
        """
        user = User.objects.create_user(
            username='newuser',
            email='new@example.com'
        )
        
        social = SocialAccount.objects.create(
            user=user,
            provider='google',
            uid='789',
            extra_data={
                'email': 'new@example.com',
                'picture': 'https://example.com/pic.jpg',
                'name': 'John Doe'
            }
        )
        
        # Adapter save_user metodini chaqirish kerak edi
        # Bu yerda manual test qiling
        self.assertIsNotNone(user)
```

**Tekshirish:**
```bash
python manage.py test api.tests.test_social_auth
```

- [ ] Barcha testlar o'tdi
- [ ] Email linking ishlaydi
- [ ] Picture va name saqlanadi

---

## Vazifa 4: REST API endpoints (20 ball)

### 4.1 Social Login Views (10 ball)

**Topshiriq:**
`api/views.py` da REST API views yarating:

```python
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/auth/google/callback"
    client_class = OAuth2Client

class GitHubLoginView(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://localhost:3000/auth/github/callback"
    client_class = OAuth2Client
```

**URL:**
```python
# api/urls.py
urlpatterns += [
    path('auth/social/google/', GoogleLoginView.as_view(), name='google_login'),
    path('auth/social/github/', GitHubLoginView.as_view(), name='github_login'),
]
```

### 4.2 User Profile endpoint (10 ball)

**Topshiriq:**
Social login qilgan foydalanuvchi ma'lumotlarini ko'rsatish:

```python
# api/serializers.py
class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ['provider', 'uid', 'extra_data']

class UserProfileSerializer(serializers.ModelSerializer):
    social_accounts = SocialAccountSerializer(many=True, read_only=True, source='socialaccount_set')
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'bio', 'profile_picture', 'social_accounts'
        ]

# api/views.py
class CurrentUserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
```

**Tekshirish Postman da:**
```
GET http://127.0.0.1:8000/api/v1/users/me/
Authorization: Token <your-token>
```

**Kutilgan javob:**
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Registered via Google",
    "profile_picture": "https://lh3.googleusercontent.com/...",
    "social_accounts": [
        {
            "provider": "google",
            "uid": "123456789",
            "extra_data": {
                "email": "john@example.com",
                "picture": "https://lh3.googleusercontent.com/..."
            }
        }
    ]
}
```

**Tekshirish:**
- [ ] Endpoint yaratilgan
- [ ] Foydalanuvchi ma'lumotlari to'g'ri qaytadi
- [ ] Social accounts ko'rinadi

---

## Bonus Vazifa: Facebook OAuth (20 ball)

### Topshiriq:
Facebook OAuth ni ham qo'shing:

1. Facebook Developers da app yarating
2. Django ga Facebook provider qo'shing
3. Test qiling

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
            'id', 'email', 'name', 'first_name', 'last_name', 'picture'
        ],
    }
}
```

**Tekshirish:**
- [ ] Facebook app yaratilgan
- [ ] Django da sozlangan
- [ ] Login ishlaydi
- [ ] Ma'lumotlar to'g'ri olinadi

---

## Topshirish

1. **GitHub repository:**
   - Branch: `feature/lesson-31-oauth2-social-auth`
   - Commit message: `feat: add OAuth2 social authentication with Google, GitHub`

2. **Kerakli fayllar:**
   ```
   library-project/
   ├── api/
   │   ├── adapters.py          # Custom adapters
   │   ├── views.py              # Social login views
   │   ├── serializers.py        # User profile serializer
   │   └── tests/
   │       └── test_social_auth.py
   ├── config/
   │   ├── settings.py           # Social auth sozlamalari
   │   └── urls.py               # Social auth URL lar
   └── test.html                 # Manual test uchun
   ```

3. **README.md ga qo'shing:**
   ```markdown
   ## Social Authentication

   ### Supported Providers
   - Google OAuth2
   - GitHub OAuth
   - Facebook OAuth (bonus)

   ### Setup
   1. Install dependencies: `pip install django-allauth dj-rest-auth`
   2. Create Google/GitHub OAuth apps
   3. Add credentials to admin panel
   4. Test: Open test.html in browser

   ### Endpoints
   - `POST /api/v1/auth/social/google/` - Google login
   - `POST /api/v1/auth/social/github/` - GitHub login
   - `GET /api/v1/users/me/` - Current user profile
   ```

4. **Screenshots:**
   - Google OAuth consent screen
   - GitHub OAuth app settings
   - Django admin Social Applications
   - Test HTML ishlayotgan holat
   - Postman da user profile

---

## Baholash mezoni

| Vazifa | Ball | Mezon |
|--------|------|-------|
| Google OAuth sozlash | 30 | Console sozlash (10) + Django (10) + Test (10) |
| GitHub OAuth | 25 | App yaratish (10) + Django (10) + Test (5) |
| Custom Adapter | 25 | Adapter (15) + Unit tests (10) |
| REST API | 20 | Views (10) + Profile endpoint (10) |
| **Bonus:** Facebook | 20 | To'liq integratsiya |
| **Jami** | **100** | **Bonus bilan 120** |

---

## Keng tarqalgan xatolar

### 1. redirect_uri_mismatch
**Sabab:** URL lar mos kelmaydi

**Yechim:**
- Console da URL ni tekshiring
- `http://` vs `https://`
- Trailing slash `/`

### 2. Site matching query does not exist
**Yechim:**
```bash
python manage.py shell
>>> from django.contrib.sites.models import Site
>>> site = Site.objects.get_current()
>>> site.domain = '127.0.0.1:8000'
>>> site.save()
```

### 3. SocialApp not found
**Yechim:**
Admin panelda Social Application yaratishni unutmang.

---

## Qo'shimcha resurslar

- [Google OAuth2 Playground](https://developers.google.com/oauthplayground/)
- [django-allauth Documentation](https://django-allauth.readthedocs.io/)
- [GitHub OAuth Guide](https://docs.github.com/en/developers/apps/building-oauth-apps)

---

**Deadline:** Keyingi darsga qadar

**Omad tilaymiz!**