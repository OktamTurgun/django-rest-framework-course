"""
Dars 01 - API bilan tanishuv
Misol 1: Oddiy GET so'rov va JSON ma'lumotni qayta ishlash

Bu dastur JSONPlaceholder API'dan foydalanuvchilar ro'yxatini oladi
va ularni chiroyli formatda chiqaradi.
"""

import requests


def get_users():
    """Barcha foydalanuvchilarni olish"""
    url = "https://jsonplaceholder.typicode.com/users"
    
    try:
        # GET so'rov yuborish
        response = requests.get(url, timeout=10)
        
        # Status kodini tekshirish
        if response.status_code == 200:
            users = response.json()
            return users
        else:
            print(f"Xato: Status kod {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"So'rov yuborishda xato: {e}")
        return None


def display_users(users):
    """Foydalanuvchilarni chiroyli ko'rinishda chiqarish"""
    if not users:
        print("Foydalanuvchilar topilmadi!")
        return
    
    print(f"\n{'='*60}")
    print(f"Jami foydalanuvchilar: {len(users)}")
    print(f"{'='*60}\n")
    
    for user in users:
        print(f"ID: {user['id']}")
        print(f"Ism: {user['name']}")
        print(f"Username: {user['username']}")
        print(f"Email: {user['email']}")
        print(f"Telefon: {user['phone']}")
        print(f"Website: {user['website']}")
        print(f"Shahar: {user['address']['city']}")
        print("-" * 60)


def get_user_by_id(user_id):
    """ID bo'yicha bitta foydalanuvchini olish"""
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"ID={user_id} bo'lgan foydalanuvchi topilmadi!")
            return None
        else:
            print(f"Xato: Status kod {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"So'rov yuborishda xato: {e}")
        return None


def main():
    """Asosiy funksiya"""
    print("\n🚀 API bilan ishlash - Birinchi dastur\n")
    
    # 1. Barcha foydalanuvchilarni olish
    print("1️⃣ Barcha foydalanuvchilarni olish...")
    users = get_users()
    
    if users:
        # Faqat birinchi 3 tasini ko'rsatish
        display_users(users[:3])
    
    # 2. Bitta foydalanuvchini olish
    print("\n\n2️⃣ ID=1 bo'lgan foydalanuvchini olish...")
    user = get_user_by_id(1)
    
    if user:
        print(f"\n{'='*60}")
        print(f"Foydalanuvchi ma'lumotlari:")
        print(f"{'='*60}")
        print(f"Ism: {user['name']}")
        print(f"Email: {user['email']}")
        print(f"Kompaniya: {user['company']['name']}")
        print(f"Shahar: {user['address']['city']}")
        print(f"{'='*60}\n")
    
    # 3. Mavjud bo'lmagan foydalanuvchi
    print("3️⃣ Mavjud bo'lmagan foydalanuvchini so'rash...")
    get_user_by_id(999)
    
    print("\n✅ Dastur tugadi!\n")


if __name__ == "__main__":
    main()