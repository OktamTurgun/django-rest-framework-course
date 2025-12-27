"""
GitHub OAuth Integration bilan Django
======================================

Bu fayl GitHub OAuth ni django-allauth bilan
qanday sozlash va ishlatishni ko'rsatadi.
"""

# ============================================================================
# 1. GitHub OAuth App yaratish
# ============================================================================

"""
GitHub OAuth App yaratish qadamlari:
====================================

QADAM 1: GitHub Settings
------------------------
1. GitHub profilingizga kiring
2. Settings > Developer settings > OAuth Apps
3. "New OAuth App" tugmasini bosing

QADAM 2: OAuth App ma'lumotlari
-------------------------------
Application name: Library API
Homepage URL: http://127.0.0.1:8000
Application description: Library management API with social authentication

Authorization callback URL:
http://127.0.0.1:8000/accounts/github/login/callback/

MUHIM: Callback URL to'g'ri bo'lishi kerak!

QADAM 3: App yaratish
--------------------
"Register application" tugmasini bosing

QADAM 4: Credentials olish
-------------------------
Client ID: Iv1.abc123def456
Client Secret: "Generate a new client secret" tugmasini bosing
                abc123def456ghi789jkl012mno345pqr678stu

⚠️ Client Secret faqat bir marta ko'rsatiladi, yaxshi saqlang!
"""


# ============================================================================
# 2. Django Settings
# ============================================================================

GITHUB_SETTINGS = """
# ============================================================================
# GITHUB OAUTH SETTINGS
# ============================================================================

import os

INSTALLED_APPS = [
    # ... Django defaults
    'django.contrib.sites',
    
    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',  # GitHub provider
    
    # dj-rest-auth
    'dj_rest_auth',
    'dj_rest_auth.registration',
    
    # Your apps
    'api',
]

# ============================================================================
# GITHUB PROVIDER SOZLAMALARI
# ============================================================================

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',           # Basic user info
            'user:email',     # Email addresses
            'read:org',       # Organization membership
        ],
        'APP': {
            'client_id': os.getenv('GITHUB_CLIENT_ID'),
            'secret': os.getenv('GITHUB_CLIENT_SECRET'),
        },
    }
}

# ============================================================================
# GITHUB SCOPE TUSHUNTIRISHLARI
# ============================================================================

# Available GitHub scopes:
# - user: Read/write access to profile info
# - user:email: Read access to user email addresses
# - read:org: Read-only access to organization membership
# - repo: Full control of private repositories
# - public_repo: Access to public repositories
# - gist: Create gists
# - notifications: Access notifications
# - read:user: Read all user profile data
# - user:follow: Follow and unfollow users

# Faqat kerakli scope larni so'rang!
"""

print("GitHub OAuth Settings:")
print(GITHUB_SETTINGS)


# ============================================================================
# 3. Environment Variables
# ============================================================================

ENV_FILE = """
# .env file

# GitHub OAuth Credentials
GITHUB_CLIENT_ID=Iv1.abc123def456
GITHUB_CLIENT_SECRET=abc123def456ghi789jkl012mno345pqr678stu

# Django
SECRET_KEY=your-secret-key
DEBUG=True
"""

print("\n" + "="*70)
print(".env file:")
print("="*70)
print(ENV_FILE)


# ============================================================================
# 4. Admin Panel Setup
# ============================================================================

def admin_setup():
    """
    Django Admin da GitHub OAuth sozlash
    """
    print("\n" + "="*70)
    print("ADMIN PANEL SETUP")
    print("="*70)
    
    steps = """
1. Migration qilish:
   python manage.py migrate

2. Admin panelga kirish:
   http://127.0.0.1:8000/admin/

3. Social applications > Add social application:
   
   Provider: GitHub
   Name: GitHub OAuth
   Client id: Iv1.abc123def456 (GitHub dan)
   Secret key: abc123def456... (GitHub dan)
   Sites: 127.0.0.1:8000 ni tanlang
   
   Save

4. Sites ni tekshirish:
   Sites > example.com > Edit
   Domain name: 127.0.0.1:8000
   Display name: Library API
   Save
    """
    
    print(steps)


# ============================================================================
# 5. GitHub Login Test HTML
# ============================================================================

GITHUB_TEST_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub OAuth Test</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 700px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #24292e 0%, #586069 100%);
            color: white;
        }
        .container {
            background: white;
            color: #24292e;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            color: #24292e;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        .github-logo {
            font-size: 40px;
        }
        .github-btn {
            display: block;
            width: 100%;
            padding: 15px;
            background: #24292e;
            color: white;
            text-decoration: none;
            text-align: center;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            margin: 25px 0;
            transition: all 0.3s;
            border: 2px solid #24292e;
        }
        .github-btn:hover {
            background: #2ea44f;
            border-color: #2ea44f;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(46,164,79,0.3);
        }
        .info-box {
            background: #f6f8fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #0366d6;
        }
        .info-box h3 {
            margin-top: 0;
            color: #0366d6;
        }
        .info-box ol {
            margin: 10px 0;
            padding-left: 25px;
        }
        .info-box li {
            margin: 8px 0;
            line-height: 1.6;
        }
        .status-box {
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0;
            font-weight: 500;
        }
        .status-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .status-waiting {
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeeba;
        }
        code {
            background: #f6f8fa;
            padding: 3px 8px;
            border-radius: 4px;
            color: #e83e8c;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }
        .permissions {
            background: #fff;
            padding: 15px;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            margin: 15px 0;
        }
        .permissions h4 {
            margin-top: 0;
            color: #586069;
        }
        .permissions ul {
            list-style: none;
            padding: 0;
        }
        .permissions li {
            padding: 8px 0;
            border-bottom: 1px solid #e1e4e8;
        }
        .permissions li:last-child {
            border-bottom: none;
        }
        .permission-icon {
            color: #2ea44f;
            margin-right: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>
            <span class="github-logo">🐙</span>
            GitHub OAuth Test
        </h1>
        
        <div class="info-box">
            <h3>📋 Test Qilish Jarayoni</h3>
            <ol>
                <li>Quyidagi "Login with GitHub" tugmasini bosing</li>
                <li>GitHub login sahifasiga yo'naltirilasiz</li>
                <li>GitHub accountingiz bilan kiring</li>
                <li>Ilovaga quyidagi ruxsatlarni bering</li>
                <li>Callback URL ga avtomatik qaytasiz</li>
            </ol>
        </div>
        
        <div class="permissions">
            <h4>🔐 So'raladigan ruxsatlar:</h4>
            <ul>
                <li>
                    <span class="permission-icon">✓</span>
                    <strong>Profile ma'lumotlari:</strong> Ism, username, avatar
                </li>
                <li>
                    <span class="permission-icon">✓</span>
                    <strong>Email addresslar:</strong> Primary va verified emails
                </li>
                <li>
                    <span class="permission-icon">✓</span>
                    <strong>Organizations:</strong> A'zolik ma'lumotlari
                </li>
            </ul>
        </div>
        
        <a href="http://127.0.0.1:8000/accounts/github/login/?process=login" 
           class="github-btn">
            🐙 Login with GitHub
        </a>
        
        <div id="status" class="status-box status-waiting">
            <strong>⏳ Status:</strong> Login qilish kutilmoqda...
        </div>
        
        <div class="info-box">
            <h3>🔗 Callback URL:</h3>
            <code>http://127.0.0.1:8000/accounts/github/login/callback/</code>
        </div>
        
        <div id="user-info" style="display: none;" class="info-box">
            <h3>👤 Foydalanuvchi ma'lumotlari:</h3>
            <div id="user-details"></div>
        </div>
    </div>
    
    <script>
        // URL dan parametrlarni tekshirish
        const urlParams = new URLSearchParams(window.location.search);
        const error = urlParams.get('error');
        const code = urlParams.get('code');
        const statusDiv = document.getElementById('status');
        
        // Error handling
        if (error) {
            statusDiv.className = 'status-box status-error';
            statusDiv.innerHTML = '<strong>❌ Error:</strong> ' + error;
        }
        
        // Success handling
        if (code) {
            statusDiv.className = 'status-box status-success';
            statusDiv.innerHTML = '<strong>✅ Success:</strong> Authorization code olindi!';
        }
        
        // LocalStorage dan token tekshirish
        const token = localStorage.getItem('github_auth_token');
        if (token) {
            // User ma'lumotlarini olish
            fetch('http://127.0.0.1:8000/api/v1/auth/user/', {
                headers: {
                    'Authorization': 'Token ' + token
                }
            })
            .then(response => response.json())
            .then(data => {
                statusDiv.className = 'status-box status-success';
                statusDiv.innerHTML = '<strong>✅ Logged in as:</strong> ' + data.username;
                
                // User details ko'rsatish
                document.getElementById('user-info').style.display = 'block';
                document.getElementById('user-details').innerHTML = `
                    <p><strong>Username:</strong> ${data.username}</p>
                    <p><strong>Email:</strong> ${data.email}</p>
                    <p><strong>Name:</strong> ${data.first_name} ${data.last_name}</p>
                `;
            })
            .catch(error => {
                console.error('Error fetching user info:', error);
            });
        }
    </script>
</body>
</html>
"""

print("\n" + "="*70)
print("GITHUB TEST HTML (save as github_test.html):")
print("="*70)
print(GITHUB_TEST_HTML)


# ============================================================================
# 6. REST API View
# ============================================================================

REST_API_CODE = """
# api/views.py
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

class GitHubLoginView(SocialLoginView):
    '''
    GitHub OAuth2 login endpoint
    
    POST /api/v1/auth/github/
    Body: {
        "code": "authorization_code_from_github"
    }
    
    Response: {
        "key": "auth_token",
        "user": {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com"
        }
    }
    '''
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://localhost:3000/auth/github/callback"
    client_class = OAuth2Client

# api/urls.py
from django.urls import path
from .views import GitHubLoginView

urlpatterns = [
    path('auth/github/', GitHubLoginView.as_view(), name='github_login'),
]
"""

print("\n" + "="*70)
print("REST API VIEW:")
print("="*70)
print(REST_API_CODE)


# ============================================================================
# 7. GitHub API bilan qo'shimcha ma'lumotlar olish
# ============================================================================

GITHUB_API_EXAMPLE = """
# GitHub API dan qo'shimcha ma'lumotlar olish

import requests

def get_github_user_repos(access_token):
    '''
    Foydalanuvchi repositoriylarini olish
    '''
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(
        'https://api.github.com/user/repos',
        headers=headers,
        params={'sort': 'updated', 'per_page': 10}
    )
    
    if response.status_code == 200:
        repos = response.json()
        return [
            {
                'name': repo['name'],
                'description': repo['description'],
                'stars': repo['stargazers_count'],
                'language': repo['language'],
                'url': repo['html_url']
            }
            for repo in repos
        ]
    return []

def get_github_user_organizations(access_token):
    '''
    Foydalanuvchi organizationlarini olish
    '''
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(
        'https://api.github.com/user/orgs',
        headers=headers
    )
    
    if response.status_code == 200:
        orgs = response.json()
        return [
            {
                'login': org['login'],
                'name': org.get('name', org['login']),
                'avatar': org['avatar_url'],
                'url': org['url']
            }
            for org in orgs
        ]
    return []

def get_github_user_followers(access_token):
    '''
    Foydalanuvchi followerlarini olish
    '''
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(
        'https://api.github.com/user/followers',
        headers=headers,
        params={'per_page': 100}
    )
    
    if response.status_code == 200:
        return len(response.json())
    return 0

# Custom adapter da ishlatish
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class GitHubSocialAccountAdapter(DefaultSocialAccountAdapter):
    
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        
        # GitHub ma'lumotlarini olish
        if sociallogin.account.provider == 'github':
            token = sociallogin.token.token
            
            # Repositories
            repos = get_github_user_repos(token)
            user.github_repos_count = len(repos)
            
            # Organizations
            orgs = get_github_user_organizations(token)
            user.github_orgs = ', '.join([org['login'] for org in orgs])
            
            # Followers
            followers = get_github_user_followers(token)
            user.github_followers = followers
            
            user.save()
        
        return user
"""

print("\n" + "="*70)
print("GITHUB API INTEGRATION:")
print("="*70)
print(GITHUB_API_EXAMPLE)


# ============================================================================
# 8. Common Issues
# ============================================================================

def common_issues():
    """
    GitHub OAuth bilan ishlashda uchraydigan muammolar
    """
    print("\n" + "="*70)
    print("COMMON ISSUES")
    print("="*70)
    
    issues = [
        {
            "issue": "redirect_uri_mismatch",
            "solution": "GitHub OAuth App settings da callback URL ni tekshiring:\n"
                       "http://127.0.0.1:8000/accounts/github/login/callback/"
        },
        {
            "issue": "Bad verification code",
            "solution": "Authorization code faqat 1 marta ishlatiladi.\n"
                       "Agar qaytadan test qilsangiz, yangi code olish kerak."
        },
        {
            "issue": "Email not available",
            "solution": "GitHub profilingizda email public qilishingiz kerak:\n"
                       "GitHub Settings > Emails > Keep my email addresses private (OFF)"
        },
        {
            "issue": "Insufficient permissions",
            "solution": "OAuth App da kerakli scope lar berilganini tekshiring:\n"
                       "user, user:email, read:org"
        },
    ]
    
    for idx, issue in enumerate(issues, 1):
        print(f"\n{idx}. {issue['issue']}")
        print(f"   Solution: {issue['solution']}")


# ============================================================================
# 9. Testing Guide
# ============================================================================

def testing_guide():
    """
    GitHub OAuth ni test qilish bo'yicha qo'llanma
    """
    print("\n" + "="*70)
    print("TESTING GUIDE")
    print("="*70)
    
    guide = """
1. Browser da test:
   - github_test.html faylni oching
   - "Login with GitHub" tugmasini bosing
   - GitHub da login qiling va authorize qiling
   - Callback URL ga qaytiladi

2. Postman da test (Manual):
   
   Step 1: Authorization code olish (Browser da)
   http://127.0.0.1:8000/accounts/github/login/?process=login
   
   Callback URL dan code ni nusxalang:
   http://127.0.0.1:8000/accounts/github/login/callback/?code=abc123
   
   Step 2: Postman da code ni token ga almashtirish
   POST http://127.0.0.1:8000/api/v1/auth/github/
   Headers: Content-Type: application/json
   Body: {
       "code": "abc123..."
   }
   
   Response: {
       "key": "your-token-here"
   }
   
   Step 3: Token bilan API dan foydalanish
   GET http://127.0.0.1:8000/api/v1/books/
   Headers: Authorization: Token your-token-here

3. Integration test:
   - Frontend (React) dan to'liq flow test qiling
   - Authorization, token olish, API calls
    """
    
    print(guide)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "🐙" * 35)
    print("GITHUB OAUTH2 INTEGRATION GUIDE")
    print("🐙" * 35)
    
    admin_setup()
    common_issues()
    testing_guide()
    
    print("\n" + "✅" * 35)
    print("SETUP READY!")
    print("✅" * 35)
    
    print("\nQuick Start:")
    print("1. GitHub da OAuth App yarating")
    print("2. .env faylda credentials kiriting")
    print("3. Admin panelda Social Application yarating")
    print("4. github_test.html ni browser da oching")
    print("5. Test qiling!")


"""
XULOSA:
=======

GitHub OAuth vs Google OAuth:
- GitHub: Developer-friendly, ko'proq tech ma'lumotlar
- Google: User-friendly, ko'proq personal ma'lumotlar

GitHub OAuth Scope lar:
- user: Basic profile info
- user:email: Email addresses
- read:org: Organization membership
- repo: Repository access (ehtiyotkorlik bilan!)

GitHub API dan qo'shimcha:
- Repositories
- Organizations
- Followers/Following
- Contributions
- Gists

MUHIM:
Authorization code faqat 1 marta ishlatiladi!
Har safar yangi code kerak.
"""