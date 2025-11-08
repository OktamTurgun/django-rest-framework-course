"""
Token Authentication Example
DRF'da Token Authentication qanday ishlashini ko'rsatadi
"""

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# ============================================
# 1. FOYDALANUVCHI YARATISH
# ============================================

def create_user_with_token():
    """
    Yangi foydalanuvchi yaratish va unga token berish
    """
    # Foydalanuvchi yaratish
    user = User.objects.create_user(
        username='john_doe',
        email='john@example.com',
        password='securepass123',
        first_name='John',
        last_name='Doe'
    )
    
    # Token yaratish
    token = Token.objects.create(user=user)
    
    print(f"✅ Foydalanuvchi yaratildi: {user.username}")
    print(f"🔑 Token: {token.key}")
    
    return user, token


# ============================================
# 2. TOKEN OLISH
# ============================================

def get_user_token(username):
    """
    Mavjud foydalanuvchining tokenini olish
    """
    try:
        user = User.objects.get(username=username)
        token, created = Token.objects.get_or_create(user=user)
        
        if created:
            print(f"🆕 Yangi token yaratildi: {token.key}")
        else:
            print(f"📋 Mavjud token: {token.key}")
        
        return token
    except User.DoesNotExist:
        print(f"❌ Foydalanuvchi topilmadi: {username}")
        return None


# ============================================
# 3. TOKEN BILAN AUTENTIFIKATSIYA
# ============================================

def authenticate_with_token(token_key):
    """
    Token orqali foydalanuvchini aniqlash
    """
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
        
        print(f"✅ Autentifikatsiya muvaffaqiyatli")
        print(f"👤 Foydalanuvchi: {user.username}")
        print(f"📧 Email: {user.email}")
        
        return user
    except Token.DoesNotExist:
        print("❌ Token noto'g'ri yoki mavjud emas")
        return None


# ============================================
# 4. TOKEN O'CHIRISH (LOGOUT)
# ============================================

def logout_user(user):
    """
    Foydalanuvchining tokenini o'chirish
    """
    try:
        token = Token.objects.get(user=user)
        token.delete()
        print(f"✅ {user.username} muvaffaqiyatli logout qilindi")
    except Token.DoesNotExist:
        print(f"⚠️  {user.username} uchun token topilmadi")


# ============================================
# 5. BARCHA TOKENLARNI KO'RISH
# ============================================

def list_all_tokens():
    """
    Tizimda mavjud barcha tokenlarni ko'rsatish
    """
    tokens = Token.objects.all()
    
    print(f"\n📊 Jami tokenlar: {tokens.count()}\n")
    
    for token in tokens:
        print(f"Username: {token.user.username}")
        print(f"Token: {token.key}")
        print(f"Yaratilgan: {token.created}")
        print("-" * 50)


# ============================================
# 6. TOKEN YANGILASH
# ============================================

def regenerate_token(user):
    """
    Foydalanuvchi uchun yangi token yaratish (eski tokenni o'chirish)
    """
    try:
        # Eski tokenni o'chirish
        Token.objects.filter(user=user).delete()
        
        # Yangi token yaratish
        new_token = Token.objects.create(user=user)
        
        print(f"🔄 Token yangilandi")
        print(f"🔑 Yangi token: {new_token.key}")
        
        return new_token
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return None


# ============================================
# TEST FUNKSIYASI
# ============================================

def run_examples():
    """
    Barcha misollarni ketma-ket ishga tushirish
    """
    print("=" * 60)
    print("TOKEN AUTHENTICATION EXAMPLES")
    print("=" * 60)
    
    # 1. Foydalanuvchi yaratish
    print("\n1️⃣  FOYDALANUVCHI YARATISH")
    print("-" * 60)
    user, token = create_user_with_token()
    
    # 2. Token olish
    print("\n2️⃣  TOKEN OLISH")
    print("-" * 60)
    retrieved_token = get_user_token('john_doe')
    
    # 3. Token bilan autentifikatsiya
    print("\n3️⃣  TOKEN BILAN AUTENTIFIKATSIYA")
    print("-" * 60)
    authenticated_user = authenticate_with_token(token.key)
    
    # 4. Barcha tokenlarni ko'rish
    print("\n4️⃣  BARCHA TOKENLAR")
    print("-" * 60)
    list_all_tokens()
    
    # 5. Token yangilash
    print("\n5️⃣  TOKEN YANGILASH")
    print("-" * 60)
    new_token = regenerate_token(user)
    
    # 6. Logout
    print("\n6️⃣  LOGOUT")
    print("-" * 60)
    logout_user(user)
    
    print("\n" + "=" * 60)
    print("EXAMPLES TUGADI ✅")
    print("=" * 60)


# Django shell'da ishlatish uchun:
# exec(open('examples/token_auth_example.py').read())
# run_examples()