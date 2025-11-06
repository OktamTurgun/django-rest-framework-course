"""
Token Authentication Misoli

Bu fayl Token Authentication qanday ishlashini ko'rsatadi.
"""

import requests


class TokenAuthExample:
    """Token Authentication bilan ishlash misoli"""
    
    def __init__(self, base_url='http://127.0.0.1:8000'):
        self.base_url = base_url
        self.token = None
    
    def login(self, username, password):
        """
        Login qilish va token olish
        
        Args:
            username: Foydalanuvchi nomi
            password: Parol
            
        Returns:
            Token yoki None
        """
        url = f'{self.base_url}/api/accounts/login/'
        data = {
            'username': username,
            'password': password
        }
        
        try:
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                result = response.json()
                self.token = result['token']
                print(f"✅ Login muvaffaqiyatli!")
                print(f"Token: {self.token}")
                return self.token
            else:
                print(f"❌ Login xato: {response.json()}")
                return None
                
        except Exception as e:
            print(f"❌ Xatolik: {e}")
            return None
    
    def get_protected_data(self):
        """
        Token bilan himoyalangan endpoint'ga murojaat
        
        Returns:
            Ma'lumotlar yoki None
        """
        if not self.token:
            print("❌ Avval login qiling!")
            return None
        
        url = f'{self.base_url}/api/books/protected/'
        headers = {
            'Authorization': f'Token {self.token}'
        }
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Ma'lumot olindi:")
                print(f"   User: {data['user']}")
                print(f"   Email: {data['email']}")
                print(f"   Auth method: {data['auth_method']}")
                return data
            else:
                print(f"❌ Xato: {response.json()}")
                return None
                
        except Exception as e:
            print(f"❌ Xatolik: {e}")
            return None
    
    def logout(self):
        """
        Logout qilish va tokenni o'chirish
        
        Returns:
            True yoki False
        """
        if not self.token:
            print("❌ Token mavjud emas!")
            return False
        
        url = f'{self.base_url}/api/accounts/logout/'
        headers = {
            'Authorization': f'Token {self.token}'
        }
        
        try:
            response = requests.post(url, headers=headers)
            
            if response.status_code == 200:
                print(f"✅ Logout muvaffaqiyatli!")
                self.token = None
                return True
            else:
                print(f"❌ Logout xato: {response.json()}")
                return False
                
        except Exception as e:
            print(f"❌ Xatolik: {e}")
            return False


def main():
    """Asosiy test funksiyasi"""
    
    print("=" * 80)
    print("TOKEN AUTHENTICATION MISOLI")
    print("=" * 80)
    print()
    
    # Instance yaratish
    auth = TokenAuthExample()
    
    # 1. Login qilish
    print("\n1️⃣ Login qilish...")
    print("-" * 80)
    auth.login('admin', 'admin123')
    
    # 2. Himoyalangan ma'lumotni olish
    print("\n2️⃣ Himoyalangan ma'lumotni olish...")
    print("-" * 80)
    auth.get_protected_data()
    
    # 3. Logout qilish
    print("\n3️⃣ Logout qilish...")
    print("-" * 80)
    auth.logout()
    
    # 4. Logout'dan keyin ma'lumot olishga harakat
    print("\n4️⃣ Token o'chirilgandan keyin ma'lumot olish...")
    print("-" * 80)
    auth.get_protected_data()
    
    print("\n" + "=" * 80)
    print("TEST TUGADI")
    print("=" * 80)


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