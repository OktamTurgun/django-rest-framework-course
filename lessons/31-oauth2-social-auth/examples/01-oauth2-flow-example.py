"""
OAuth2 Flow va Asosiy Tushunchalar
===================================

Bu fayl OAuth2 protokolining qanday ishlashini ko'rsatadi.
"""

import json
import secrets

# ============================================================================
# 1. OAuth2 Asosiy Tushunchalar
# ============================================================================

"""
OAuth2 - bu uchinchi tomon ilovalarga resurslaringizga kirish 
huquqini berish uchun protokol.

ASOSIY ROLLAR:
-------------
1. Resource Owner (Foydalanuvchi) - Siz
2. Client (Ilovangiz) - Sizning Django app
3. Authorization Server - Google, GitHub, Facebook
4. Resource Server - Foydalanuvchi ma'lumotlari joylashgan server

ASOSIY TOKENLAR:
---------------
1. Authorization Code - Vaqtinchalik kod (bir marta ishlatiladi)
2. Access Token - Resurslarga kirish uchun token (1 soat)
3. Refresh Token - Access tokenni yangilash uchun (30 kun)
"""


# ============================================================================
# 2. OAuth2 Authorization Code Flow
# ============================================================================

class OAuth2Flow:
    """
    OAuth2 Authorization Code Flow simulation
    """
    
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorization_code = None
        self.access_token = None
        self.refresh_token = None
    
    def step1_redirect_to_authorization_server(self):
        """
        QADAM 1: Foydalanuvchini Authorization Server ga yo'naltirish
        
        Foydalanuvchi "Login with Google" tugmasini bosadi.
        Sizning backend Authorization URL yaratadi.
        """
        import secrets
        
        # CSRF protection uchun random state yaratish
        state = secrets.token_urlsafe(32)
        
        # Authorization URL
        authorization_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={self.client_id}&"
            f"redirect_uri={self.redirect_uri}&"
            "response_type=code&"
            "scope=openid email profile&"
            f"state={state}"
        )
        
        print("=" * 70)
        print("QADAM 1: Redirect to Authorization Server")
        print("=" * 70)
        print(f"Authorization URL:\n{authorization_url}\n")
        print(f"State (CSRF protection): {state}\n")
        print("Foydalanuvchi bu URL ga yo'naltiriladi.")
        print("=" * 70)
        
        return authorization_url, state
    
    def step2_user_grants_permission(self):
        """
        QADAM 2: Foydalanuvchi ruxsat beradi
        
        Foydalanuvchi Google ga login qiladi va
        "Allow access" tugmasini bosadi.
        """
        print("\n" + "=" * 70)
        print("QADAM 2: User Grants Permission")
        print("=" * 70)
        print("Foydalanuvchi Google da:")
        print("1. Email va parol kiritadi")
        print("2. Sizning ilovangizga ruxsat beradi")
        print("3. Permissions:\n   - View your email address")
        print("   - View your basic profile info")
        print("=" * 70)
    
    def step3_receive_authorization_code(self, code, state, original_state):
        """
        QADAM 3: Authorization Code olish
        
        Google foydalanuvchini redirect_uri ga qaytaradi.
        URL da code va state parametrlari bo'ladi.
        """
        print("\n" + "=" * 70)
        print("QADAM 3: Receive Authorization Code")
        print("=" * 70)
        
        # State validation (CSRF protection)
        if state != original_state:
            print("❌ ERROR: State mismatch! Possible CSRF attack!")
            return False
        
        print("✅ State validation passed")
        print(f"Authorization Code: {code}")
        print(f"\nCallback URL:\n{self.redirect_uri}?code={code}&state={state}")
        print("=" * 70)
        
        self.authorization_code = code
        return True
    
    def step4_exchange_code_for_tokens(self):
        """
        QADAM 4: Authorization Code ni Token ga almashtirish
        
        Backend Google ga POST request yuboradi va
        Access Token oladi.
        """
        print("\n" + "=" * 70)
        print("QADAM 4: Exchange Code for Tokens")
        print("=" * 70)
        
        # Bu yerda haqiqiy POST request bo'lishi kerak
        # Biz faqat simulation qilyapmiz
        
        token_request = {
            "grant_type": "authorization_code",
            "code": self.authorization_code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
        }
        
        print("POST request to: https://oauth2.googleapis.com/token")
        print(f"Request body: {token_request}\n")
        
        # Simulated response
        import secrets
        self.access_token = f"ya29.{secrets.token_urlsafe(100)}"
        self.refresh_token = f"1//{secrets.token_urlsafe(50)}"
        
        print("✅ Response received:")
        print(f"Access Token: {self.access_token[:50]}...")
        print(f"Refresh Token: {self.refresh_token[:50]}...")
        print("Token Type: Bearer")
        print("Expires In: 3600 seconds (1 hour)")
        print("=" * 70)
    
    def step5_get_user_info(self):
        """
        QADAM 5: Access Token bilan foydalanuvchi ma'lumotlarini olish
        """
        print("\n" + "=" * 70)
        print("QADAM 5: Get User Information")
        print("=" * 70)
        
        print("GET request to: https://www.googleapis.com/oauth2/v2/userinfo")
        print(f"Authorization: Bearer {self.access_token[:50]}...\n")
        
        # Simulated user info
        user_info = {
            "id": "123456789",
            "email": "john.doe@example.com",
            "verified_email": True,
            "name": "John Doe",
            "given_name": "John",
            "family_name": "Doe",
            "picture": "https://lh3.googleusercontent.com/a/default-user",
            "locale": "en"
        }
        
        print("✅ User Information received:")
        import json
        print(json.dumps(user_info, indent=2))
        print("=" * 70)
        
        return user_info
    
    def step6_create_or_login_user(self, user_info):
        """
        QADAM 6: Django da foydalanuvchini yaratish yoki login qilish
        """
        print("\n" + "=" * 70)
        print("QADAM 6: Create or Login User in Django")
        print("=" * 70)
        
        print("Django backend:")
        print("1. Email orqali foydalanuvchini qidirish")
        print(f"   User.objects.filter(email='{user_info['email']}')")
        print("\n2. Agar topilsa - login qilish")
        print("   Agar topilmasa - yangi user yaratish\n")
        
        print("User data to save:")
        print(f"   Username: {user_info['email'].split('@')[0]}")
        print(f"   Email: {user_info['email']}")
        print(f"   First name: {user_info['given_name']}")
        print(f"   Last name: {user_info['family_name']}")
        print(f"   Profile picture: {user_info['picture']}")
        
        print("\n3. SocialAccount yaratish:")
        print(f"   Provider: google")
        print(f"   UID: {user_info['id']}")
        print(f"   Extra data: {json.dumps(user_info, indent=6)}")
        
        print("\n4. Token yaratish va qaytarish")
        print("   ✅ User logged in successfully!")
        print("=" * 70)
    
    def refresh_access_token(self):
        """
        BONUS: Access Token muddati tugaganda yangilash
        """
        print("\n" + "=" * 70)
        print("BONUS: Refresh Access Token")
        print("=" * 70)
        
        print("Agar access token muddati tugasa (1 soatdan keyin):")
        print("Refresh token bilan yangi access token olish mumkin\n")
        
        refresh_request = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        
        print("POST request to: https://oauth2.googleapis.com/token")
        print(f"Request body: {refresh_request}\n")
        
        # New access token
        import secrets
        new_access_token = f"ya29.{secrets.token_urlsafe(100)}"
        
        print("✅ New Access Token received:")
        print(f"{new_access_token[:50]}...")
        print("=" * 70)


# ============================================================================
# 3. OAuth2 Flow ni ishlatish
# ============================================================================

def main():
    """
    OAuth2 flowni qadamma-qadamlik ko'rsatish
    """
    print("\n" + "🔐" * 35)
    print("OAuth2 AUTHORIZATION CODE FLOW DEMONSTRATION")
    print("🔐" * 35 + "\n")
    
    # OAuth2 client yaratish
    oauth_client = OAuth2Flow(
        client_id="123456789.apps.googleusercontent.com",
        client_secret="GOCSPX-abc123def456",
        redirect_uri="http://127.0.0.1:8000/accounts/google/login/callback/"
    )
    
    # QADAM 1: Authorization URL yaratish
    auth_url, state = oauth_client.step1_redirect_to_authorization_server()
    
    # QADAM 2: User ruxsat beradi (browser da)
    oauth_client.step2_user_grants_permission()
    
    # QADAM 3: Authorization code olish
    # Google callback URL: ?code=4/0AY0...&state=xyz
    authorization_code = "4/0AY0e-g7X..."  # Simulated
    oauth_client.step3_receive_authorization_code(
        code=authorization_code,
        state=state,
        original_state=state
    )
    
    # QADAM 4: Code ni Token ga almashtirish
    oauth_client.step4_exchange_code_for_tokens()
    
    # QADAM 5: User info olish
    user_info = oauth_client.step5_get_user_info()
    
    # QADAM 6: Django da user yaratish
    oauth_client.step6_create_or_login_user(user_info)
    
    # BONUS: Token yangilash
    oauth_client.refresh_access_token()
    
    print("\n" + "✅" * 35)
    print("OAuth2 FLOW COMPLETED SUCCESSFULLY!")
    print("✅" * 35 + "\n")


# ============================================================================
# 4. Security Best Practices
# ============================================================================

def security_notes():
    """
    OAuth2 xavfsizlik bo'yicha muhim eslatmalar
    """
    print("\n" + "🔒" * 35)
    print("SECURITY BEST PRACTICES")
    print("🔒" * 35 + "\n")
    
    practices = [
        {
            "title": "1. State Parameter (CSRF Protection)",
            "description": "Har bir request uchun unique state yarating",
            "code": "state = secrets.token_urlsafe(32)"
        },
        {
            "title": "2. HTTPS Only",
            "description": "Production da faqat HTTPS ishlatilsin",
            "code": "ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'"
        },
        {
            "title": "3. Client Secret xavfsizligi",
            "description": "Client secret ni hech qachon frontend ga yubormang",
            "code": "# Environment variable dan oling\nCLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')"
        },
        {
            "title": "4. Token Storage",
            "description": "Token larni secure cookie da saqlang",
            "code": "JWT_AUTH_COOKIE = 'auth'\nJWT_AUTH_SECURE = True\nJWT_AUTH_HTTPONLY = True"
        },
        {
            "title": "5. Scope Limitation",
            "description": "Faqat kerakli scope larni so'rang",
            "code": "SCOPE = ['profile', 'email']  # Minimal scope"
        },
        {
            "title": "6. Token Expiration",
            "description": "Access token muddatini cheklang",
            "code": "ACCESS_TOKEN_LIFETIME = timedelta(hours=1)"
        },
    ]
    
    for practice in practices:
        print(f"{practice['title']}")
        print(f"   {practice['description']}")
        print(f"   Code: {practice['code']}\n")
    
    print("🔒" * 35 + "\n")


# ============================================================================
# 5. Common Errors
# ============================================================================

def common_errors():
    """
    Keng tarqalgan xatolar va ularning yechimlari
    """
    print("\n" + "⚠️ " * 30)
    print("COMMON ERRORS AND SOLUTIONS")
    print("⚠️ " * 30 + "\n")
    
    errors = [
        {
            "error": "redirect_uri_mismatch",
            "cause": "Callback URL Google Console da ko'rsatilgan bilan mos kelmaydi",
            "solution": "Google Console > Credentials da URL ni tekshiring"
        },
        {
            "error": "invalid_grant",
            "cause": "Authorization code allaqachon ishlatilgan yoki muddati tugagan",
            "solution": "Authorization code faqat 1 marta ishlatiladi, yangi flow boshlang"
        },
        {
            "error": "invalid_client",
            "cause": "Client ID yoki Secret noto'g'ri",
            "solution": "Google Console dan Client credentials ni qayta tekshiring"
        },
        {
            "error": "access_denied",
            "cause": "Foydalanuvchi ruxsat bermaganini bildirdi",
            "solution": "Foydalanuvchiga ruxsat berish kerakligini tushuntiring"
        },
    ]
    
    for err in errors:
        print(f"❌ Error: {err['error']}")
        print(f"   Cause: {err['cause']}")
        print(f"   Solution: {err['solution']}\n")
    
    print("⚠️ " * 30 + "\n")


if __name__ == "__main__":
    main()
    security_notes()
    common_errors()


"""
XULOSA:
=======

OAuth2 Authorization Code Flow:
1. User ni Authorization Server ga yo'naltirish
2. User ruxsat beradi
3. Authorization Code olish
4. Code ni Access Token ga almashtirish
5. Access Token bilan user ma'lumotlarini olish
6. Django da user yaratish yoki login qilish

ASOSIY TOKENLAR:
- Authorization Code: 1 marta ishlatiladi (10 daqiqa)
- Access Token: Resurslarga kirish (1 soat)
- Refresh Token: Access token ni yangilash (30 kun)

XAVFSIZLIK:
- State parameter (CSRF protection)
- HTTPS only
- Client secret ni yashirish
- Secure token storage
- Minimal scope
"""