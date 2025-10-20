"""
Dars 01 - API bilan tanishuv
Misol 2: API ma'lumotlarini filterlash va qidirish

Bu dastur JSONPlaceholder API'dan postlarni oladi va
turli usullar bilan filtrlab, qidiradi.
"""

import requests


def get_all_posts():
    """Barcha postlarni olish"""
    url = "https://jsonplaceholder.typicode.com/posts"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Xato: {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"Xato: {e}")
        return []


def filter_by_user(posts, user_id):
    """Foydalanuvchi ID'si bo'yicha filterlash"""
    filtered = [post for post in posts if post['userId'] == user_id]
    return filtered


def search_in_title(posts, keyword):
    """Sarlavhada kalit so'z bo'yicha qidirish"""
    keyword = keyword.lower()
    results = [
        post for post in posts 
        if keyword in post['title'].lower()
    ]
    return results


def get_posts_with_query_params(user_id=None):
    """Query parameters bilan filterlangan postlarni olish"""
    url = "https://jsonplaceholder.typicode.com/posts"
    
    params = {}
    if user_id:
        params['userId'] = user_id
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            print(f"📍 So'rov yuborildi: {response.url}")
            return response.json()
        else:
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"Xato: {e}")
        return []


def display_posts(posts, limit=5):
    """Postlarni chiqarish"""
    if not posts:
        print("❌ Hech narsa topilmadi!")
        return
    
    print(f"\n✅ {len(posts)} ta post topildi")
    print(f"{'='*70}\n")
    
    for i, post in enumerate(posts[:limit], 1):
        print(f"{i}. [{post['id']}] {post['title']}")
        print(f"   User ID: {post['userId']}")
        print(f"   {post['body'][:50]}...")
        print()


def main():
    """Asosiy funksiya"""
    print("\n🔍 API ma'lumotlarini filterlash va qidirish\n")
    
    # 1. Barcha postlarni olish
    print("1️⃣ Barcha postlarni yuklash...")
    all_posts = get_all_posts()
    print(f"✅ {len(all_posts)} ta post yuklandi\n")
    
    # 2. User ID bo'yicha filterlash (Python'da)
    print("2️⃣ User ID=1 bo'yicha filterlash (Python'da)...")
    user_posts = filter_by_user(all_posts, user_id=1)
    display_posts(user_posts, limit=3)
    
    # 3. Sarlavhada qidirish
    print("\n3️⃣ Sarlavhada 'qui' so'zini qidirish...")
    search_results = search_in_title(all_posts, "qui")
    display_posts(search_results, limit=3)
    
    # 4. Query parameters bilan filterlash (API'da)
    print("\n4️⃣ Query params bilan User ID=2 postlarini olish...")
    filtered_posts = get_posts_with_query_params(user_id=2)
    display_posts(filtered_posts, limit=3)
    
    # 5. Statistika
    print("\n📊 STATISTIKA")
    print(f"{'='*70}")
    print(f"Jami postlar: {len(all_posts)}")
    
    users_count = len(set(post['userId'] for post in all_posts))
    print(f"Nechta foydalanuvchi: {users_count}")
    
    avg_length = sum(len(post['body']) for post in all_posts) / len(all_posts)
    print(f"O'rtacha post uzunligi: {avg_length:.0f} belgi")
    print(f"{'='*70}\n")
    
    print("✅ Dastur tugadi!\n")


if __name__ == "__main__":
    main()