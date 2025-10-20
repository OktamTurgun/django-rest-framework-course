"""
Dars 02 - HTTP Methods va Status Kodlar
Misol 1: CRUD operatsiyalari (Create, Read, Update, Delete)

Bu dastur JSONPlaceholder API bilan barcha HTTP metodlarni
amalda ko'rsatadi.
"""

import requests
import json


BASE_URL = "https://jsonplaceholder.typicode.com/posts"


def create_post(title, body, user_id=1):
    """
    POST - Yangi post yaratish
    Status: 201 Created
    """
    print("\n" + "="*70)
    print("🆕 POST - Yangi post yaratish")
    print("="*70)
    
    new_post = {
        "title": title,
        "body": body,
        "userId": user_id
    }
    
    try:
        response = requests.post(BASE_URL, json=new_post, timeout=10)
        
        print(f"📤 So'rov yuborildi: POST {BASE_URL}")
        print(f"📦 Ma'lumot: {json.dumps(new_post, indent=2)}")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 201:
            created_post = response.json()
            print(f"✅ Muvaffaqiyatli yaratildi!")
            print(f"🆔 Yangi ID: {created_post['id']}")
            print(f"📝 Sarlavha: {created_post['title']}")
            return created_post
        else:
            print(f"❌ Xato: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Xato: {e}")
        return None


def read_post(post_id):
    """
    GET - Post o'qish
    Status: 200 OK yoki 404 Not Found
    """
    print("\n" + "="*70)
    print(f"📖 GET - Post #{post_id} o'qish")
    print("="*70)
    
    url = f"{BASE_URL}/{post_id}"
    
    try:
        response = requests.get(url, timeout=10)
        
        print(f"📤 So'rov: GET {url}")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            post = response.json()
            print(f"✅ Post topildi!")
            print(f"📝 Sarlavha: {post['title']}")
            print(f"📄 Matn: {post['body'][:50]}...")
            print(f"👤 User ID: {post['userId']}")
            return post
        elif response.status_code == 404:
            print(f"❌ 404: Post topilmadi!")
            return None
        else:
            print(f"❌ Xato: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Xato: {e}")
        return None


def read_all_posts(limit=5):
    """
    GET - Barcha postlarni o'qish
    Status: 200 OK
    """
    print("\n" + "="*70)
    print("📚 GET - Barcha postlarni o'qish")
    print("="*70)
    
    try:
        response = requests.get(BASE_URL, timeout=10)
        
        print(f"📤 So'rov: GET {BASE_URL}")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            posts = response.json()
            print(f"✅ {len(posts)} ta post topildi!")
            print(f"\nBirinchi {limit} ta post:\n")
            
            for post in posts[:limit]:
                print(f"  [{post['id']}] {post['title']}")
            
            return posts
        else:
            print(f"❌ Xato: {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Xato: {e}")
        return []


def update_post_put(post_id, title, body, user_id):
    """
    PUT - Postni to'liq yangilash
    Status: 200 OK
    
    PUT barcha fieldlarni yuborish kerak!
    """
    print("\n" + "="*70)
    print(f"🔄 PUT - Post #{post_id} to'liq yangilash")
    print("="*70)
    
    url = f"{BASE_URL}/{post_id}"
    
    updated_post = {
        "id": post_id,
        "title": title,
        "body": body,
        "userId": user_id
    }
    
    try:
        response = requests.put(url, json=updated_post, timeout=10)
        
        print(f"📤 So'rov: PUT {url}")
        print(f"📦 Ma'lumot: {json.dumps(updated_post, indent=2)}")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Muvaffaqiyatli yangilandi!")
            print(f"📝 Yangi sarlavha: {result['title']}")
            return result
        else:
            print(f"❌ Xato: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Xato: {e}")
        return None


def update_post_patch(post_id, **kwargs):
    """
    PATCH - Postni qisman yangilash
    Status: 200 OK
    
    PATCH faqat o'zgartirilgan fieldlarni yuborish kifoya!
    """
    print("\n" + "="*70)
    print(f"✏️  PATCH - Post #{post_id} qisman yangilash")
    print("="*70)
    
    url = f"{BASE_URL}/{post_id}"
    
    try:
        response = requests.patch(url, json=kwargs, timeout=10)
        
        print(f"📤 So'rov: PATCH {url}")
        print(f"📦 O'zgargan fieldlar: {json.dumps(kwargs, indent=2)}")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Muvaffaqiyatli yangilandi!")
            return result
        else:
            print(f"❌ Xato: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Xato: {e}")
        return None


def delete_post(post_id):
    """
    DELETE - Postni o'chirish
    Status: 200 OK yoki 204 No Content
    """
    print("\n" + "="*70)
    print(f"🗑️  DELETE - Post #{post_id} o'chirish")
    print("="*70)
    
    url = f"{BASE_URL}/{post_id}"
    
    try:
        response = requests.delete(url, timeout=10)
        
        print(f"📤 So'rov: DELETE {url}")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code in [200, 204]:
            print(f"✅ Post o'chirildi!")
            return True
        elif response.status_code == 404:
            print(f"❌ 404: Post topilmadi!")
            return False
        else:
            print(f"❌ Xato: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Xato: {e}")
        return False


def main():
    """Asosiy funksiya - CRUD operatsiyalarini demo qilish"""
    
    print("\n" + "="*70)
    print("🚀 CRUD OPERATSIYALARI DEMO")
    print("="*70)
    
    # 1. CREATE - POST
    new_post = create_post(
        title="Mening yangi postim",
        body="Bu Django REST Framework kursi uchun test post.",
        user_id=1
    )
    
    if new_post:
        post_id = new_post['id']
        
        # 2. READ - GET (bitta)
        read_post(post_id)
        
        # 3. READ - GET (barcha)
        read_all_posts(limit=3)
        
        # 4. UPDATE - PUT (to'liq)
        update_post_put(
            post_id,
            title="Yangilangan sarlavha (PUT)",
            body="To'liq yangilangan matn",
            user_id=1
        )
        
        # 5. UPDATE - PATCH (qisman)
        update_post_patch(
            post_id,
            title="Faqat sarlavha o'zgardi (PATCH)"
        )
        
        # 6. DELETE
        delete_post(post_id)
        
        # 7. O'chirilganini tekshirish
        read_post(post_id)
    
    print("\n" + "="*70)
    print("✅ DEMO TUGADI!")
    print("="*70 + "\n")
    
    # PUT vs PATCH farqi
    print("\n" + "="*70)
    print("💡 PUT vs PATCH FARQI")
    print("="*70)
    print("""
PUT - To'liq yangilash:
  ✅ Barcha fieldlarni yuborish kerak
  ✅ Yuborilmagan fieldlar yo'qoladi/default bo'ladi
  ✅ Idempotent (bir xil natija)

PATCH - Qisman yangilash:
  ✅ Faqat o'zgargan fieldlarni yuborish
  ✅ Qolgan fieldlar o'zgarmaydi
  ✅ Ko'proq ishlatiladi

Misol:
  PUT:   {"id": 1, "title": "...", "body": "...", "userId": 1}
  PATCH: {"title": "..."}  # Faqat title
    """)


if __name__ == "__main__":
    main()