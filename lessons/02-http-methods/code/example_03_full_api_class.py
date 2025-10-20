"""
Dars 02 - HTTP Methods va Status Kodlar
Misol 3: To'liq API Client Class

Bu dastur professional darajadagi API client classini ko'rsatadi.
Real loyihalarda shunday yoziladi.
"""

import requests
from typing import Optional, Dict, List
import json


class JSONPlaceholderAPI:
    """JSONPlaceholder API uchun to'liq client"""
    
    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com"):
        """
        API client'ni initialize qilish
        
        Args:
            base_url: API'ning asosiy URL'i
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "DRF-Course-API-Client/1.0",
            "Accept": "application/json"
        })
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Umumiy so'rov funksiyasi
        
        Args:
            method: HTTP metod (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint
            data: Request body ma'lumotlari
            params: Query parameters
        
        Returns:
            API javobi yoki None
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=10
            )
            
            # Status kodlarni handle qilish
            if response.status_code in [200, 201]:
                return response.json()
            elif response.status_code == 204:
                return {"success": True, "message": "Deleted"}
            elif response.status_code == 404:
                print(f"❌ 404: {endpoint} topilmadi")
                return None
            else:
                print(f"❌ Xato: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ So'rov xatosi: {e}")
            return None
    
    # ========== POST CRUD METHODS ==========
    
    def get_all_posts(self, limit: Optional[int] = None) -> List[Dict]:
        """Barcha postlarni olish"""
        params = {"_limit": limit} if limit else None
        result = self._make_request("GET", "posts", params=params)
        return result if result else []
    
    def get_post(self, post_id: int) -> Optional[Dict]:
        """Bitta postni olish"""
        return self._make_request("GET", f"posts/{post_id}")
    
    def create_post(self, title: str, body: str, user_id: int = 1) -> Optional[Dict]:
        """Yangi post yaratish"""
        data = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        return self._make_request("POST", "posts", data=data)
    
    def update_post(self, post_id: int, title: str, body: str, user_id: int) -> Optional[Dict]:
        """Postni to'liq yangilash (PUT)"""
        data = {
            "id": post_id,
            "title": title,
            "body": body,
            "userId": user_id
        }
        return self._make_request("PUT", f"posts/{post_id}", data=data)
    
    def partial_update_post(self, post_id: int, **kwargs) -> Optional[Dict]:
        """Postni qisman yangilash (PATCH)"""
        return self._make_request("PATCH", f"posts/{post_id}", data=kwargs)
    
    def delete_post(self, post_id: int) -> bool:
        """Postni o'chirish"""
        result = self._make_request("DELETE", f"posts/{post_id}")
        return result is not None
    
    # ========== USER METHODS ==========
    
    def get_all_users(self) -> List[Dict]:
        """Barcha foydalanuvchilarni olish"""
        result = self._make_request("GET", "users")
        return result if result else []
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Bitta foydalanuvchini olish"""
        return self._make_request("GET", f"users/{user_id}")
    
    def get_user_posts(self, user_id: int) -> List[Dict]:
        """Foydalanuvchining barcha postlari"""
        params = {"userId": user_id}
        result = self._make_request("GET", "posts", params=params)
        return result if result else []
    
    # ========== COMMENT METHODS ==========
    
    def get_post_comments(self, post_id: int) -> List[Dict]:
        """Post'ning barcha commentlari"""
        params = {"postId": post_id}
        result = self._make_request("GET", "comments", params=params)
        return result if result else []
    
    def __del__(self):
        """Session'ni yopish"""
        self.session.close()


def demo_basic_usage():
    """Oddiy ishlatish"""
    print("\n" + "="*70)
    print("1️⃣ ODDIY ISHLATISH")
    print("="*70)
    
    api = JSONPlaceholderAPI()
    
    # Postlarni olish
    posts = api.get_all_posts(limit=3)
    print(f"\n✅ {len(posts)} ta post topildi:")
    for post in posts:
        print(f"  - [{post['id']}] {post['title']}")


def demo_full_crud():
    """To'liq CRUD operatsiyalari"""
    print("\n" + "="*70)
    print("2️⃣ TO'LIQ CRUD OPERATSIYALARI")
    print("="*70)
    
    api = JSONPlaceholderAPI()
    
    # CREATE
    print("\n📝 Yangi post yaratish...")
    new_post = api.create_post(
        title="API Client bilan yaratildi",
        body="Bu professional API client yordamida yaratildi"
    )
    
    if new_post:
        post_id = new_post['id']
        print(f"✅ Yaratildi! ID: {post_id}")
        
        # READ
        print(f"\n📖 Post #{post_id} ni o'qish...")
        post = api.get_post(post_id)
        if post:
            print(f"✅ Topildi: {post['title']}")
        
        # UPDATE (PUT)
        print(f"\n🔄 Post #{post_id} ni to'liq yangilash...")
        updated = api.update_post(
            post_id,
            title="Yangilangan sarlavha",
            body="To'liq yangilangan matn",
            user_id=1
        )
        if updated:
            print(f"✅ Yangilandi!")
        
        # UPDATE (PATCH)
        print(f"\n✏️  Post #{post_id} ni qisman yangilash...")
        patched = api.partial_update_post(
            post_id,
            title="Faqat sarlavha o'zgardi"
        )
        if patched:
            print(f"✅ Yangilandi!")
        
        # DELETE
        print(f"\n🗑️  Post #{post_id} ni o'chirish...")
        deleted = api.delete_post(post_id)
        if deleted:
            print(f"✅ O'chirildi!")


def demo_advanced_usage():
    """Murakkab ishlatish"""
    print("\n" + "="*70)
    print("3️⃣ MURAKKAB ISHLATISH")
    print("="*70)
    
    api = JSONPlaceholderAPI()
    
    # User va uning postlari
    print("\n👤 User va uning postlari...")
    user = api.get_user(1)
    
    if user:
        print(f"✅ User: {user['name']} (@{user['username']})")
        
        posts = api.get_user_posts(1)
        print(f"📝 {len(posts)} ta post:")
        
        for post in posts[:3]:
            print(f"  - {post['title']}")
            
            # Har bir postning commentlari
            comments = api.get_post_comments(post['id'])
            print(f"    💬 {len(comments)} ta comment")


def demo_error_handling():
    """Xatolarni handle qilish"""
    print("\n" + "="*70)
    print("4️⃣ XATOLARNI HANDLE QILISH")
    print("="*70)
    
    api = JSONPlaceholderAPI()
    
    # Mavjud bo'lmagan post
    print("\n❌ Mavjud bo'lmagan postni so'rash...")
    post = api.get_post(99999)
    
    if post is None:
        print("⚠️  Post topilmadi, lekin dastur ishda davom etmoqda!")
    
    # Mavjud bo'lmagan user
    print("\n❌ Mavjud bo'lmagan user...")
    user = api.get_user(99999)
    
    if user is None:
        print("⚠️  User topilmadi!")


def main():
    """Asosiy funksiya"""
    
    print("\n" + "="*70)
    print("🚀 PROFESSIONAL API CLIENT DEMO")
    print("="*70)
    
    # 1. Oddiy ishlatish
    demo_basic_usage()
    
    # 2. To'liq CRUD
    demo_full_crud()
    
    # 3. Murakkab ishlatish
    demo_advanced_usage()
    
    # 4. Error handling
    demo_error_handling()
    
    print("\n" + "="*70)
    print("✅ DEMO TUGADI!")
    print("="*70)
    
    # Class afzalliklari
    print("\n💡 API CLASS AFZALLIKLARI:")
    print("""
1. Kod qayta ishlatiladi (reusable)
   - Bir marta yoziladi, ko'p joyda ishlatiladi
   
2. Toza va tushunarli
   - api.get_post(1) - juda sodda!
   
3. Error handling bir joyda
   - Har safar try-except yozish shart emas
   
4. Kengaytirish oson
   - Yangi metodlar qo'shish oson
   
5. Testing uchun qulay
   - Mock qilish oson

Real loyihalarda doim shunday yoziladi! 🎯
    """)


if __name__ == "__main__":
    main()