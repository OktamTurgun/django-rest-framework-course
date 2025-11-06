"""
Session Authentication Misoli

Bu fayl Session Authentication qanday ishlashini ko'rsatadi.
"""

import requests


class SessionAuthExample:
    """Session Authentication bilan ishlash misoli"""
    
    def __init__(self, base_url='http://127.0.0.1:8000'):
        self.base_url = base_url
        self.session = requests.Session()
    
    def login_via_admin(self, username, password):
        """
        Django admin orqali login qilish
        
        Args:
            username: Foydalanuvchi nomi
            password: Parol
            
        Returns:
            True yoki False
        """
        # 1. Login sahifasidan CSRF token olish
        login_url = f'{self.base_url}/admin/login/'
        
        try:
            response = self.session.get(login_url)
            csrf_token = response.cookies.get('csrftoken')
            
            if not csrf_token:
                print("❌ CSRF token olinmadi!")
                return False
            
            # 2. Login qilish
            login_data = {
                'username': username,
                'password': password,
                'csrfmiddlewaretoken': csrf_token,
                'next': '/admin/'
            }
            
            response = self.session.post(
                login_url,
                data=login_data,
                headers={'Referer': login_url}
            )
            
            if response.status_code == 200 and 'sessionid' in self.session.cookies:
                print(f"✅ Session orqali login muvaffaqiyatli!")
                print(f"Session ID: {self.session.cookies.get('sessionid')}")
                return True
            else:
                print(f"❌ Login xato!")
                return False
                
        except Exception as e:
            print(f"❌ Xatolik: {e}")
            return False
    
    def get_protected_data(self):
        """
        Session bilan himoyalangan endpoint'ga murojaat
        
        Returns:
            Ma'lumotlar yoki None
        """
        url = f'{self.base_url}/api/books/protected/'
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Ma'lumot olindi:")
                print(f"   User: {data['user']}")
                print(f"   Email: {data['email']}")
                print(f"   Auth method: {data['auth_method']}")
                return data
            else:
                print(f"❌ Xato: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Xatolik: {e}")
            return None
    
    def logout(self):
        """
        Logout qilish
        
        Returns:
            True yoki False
        """
        logout_url = f'{self.base_url}/admin/logout/'
        
        try:
            response = self.session.get(logout_url)
            
            if response.status_code == 200:
                print(f"✅ Logout muvaffaqiyatli!")
                self.session.cookies.clear()
                return True
            else:
                print(f"❌ Logout xato!")
                return False
                
        except Exception as e:
            print(f"❌ Xatolik: {e}")
            return False


def main():
    """Asosiy test funksiyasi"""
    
    print("=" * 80)
    print("SESSION AUTHENTICATION MISOLI")
    print("=" * 80)
    print()
    
    # Instance yaratish
    auth = SessionAuthExample()
    
    # 1. Login qilish
    print("\n1️⃣ Django admin orqali login qilish...")
    print("-" * 80)
    auth.login_via_admin('admin', 'admin123')
    
    # 2. Himoyalangan ma'lumotni olish
    print("\n2️⃣ Session bilan himoyalangan ma'lumotni olish...")
    print("-" * 80)
    auth.get_protected_data()
    
    # 3. Logout qilish
    print("\n3️⃣ Logout qilish...")
    print("-" * 80)
    auth.logout()
    
    # 4. Logout'dan keyin ma'lumot olishga harakat
    print("\n4️⃣ Session o'chirilgandan keyin ma'lumot olish...")
    print("-" * 80)
    auth.get_protected_data()
    
    print("\n" + "=" * 80)
    print("TEST TUGADI")
    print("=" * 80)
    
    print("""
    📝 Session vs Token farqi:
    
    Session Authentication:
    - Browser'da cookie saqlanadi
    - Server'da session ma'lumotlari saqlanadi (stateful)
    - CSRF himoyasi talab qilinadi
    - Browser ilovalari uchun qulay
    
    Token Authentication:
    - Token client'da saqlanadi
    - Server'da session yo'q (stateless)
    - CSRF himoyasi kerak emas
    - Mobile ilovalar uchun qulay
    """)


if __name__ == "__main__":
    print("""
    ⚠️  DIQQAT: Ishlatishdan oldin:
    
    1. Server ishga tushirilgan bo'lishi kerak:
       cd code/library-project
       python manage.py runserver
    
    2. requests kutubxonasi o'rnatilgan bo'lishi kerak:
       pip install requests
    
    3. Superuser yaratilgan bo'lishi kerak:
       python manage.py createsuperuser
    """)
    
    answer = input("\nDavom ettirasizmi? (y/n): ")
    if answer.lower() == 'y':
        main()