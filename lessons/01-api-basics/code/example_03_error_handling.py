"""
Dars 01 - API bilan tanishuv
Misol 3: Xatolarni to'g'ri boshqarish (Error Handling)

Bu dastur API bilan ishlashda yuzaga kelishi mumkin bo'lgan
barcha xatoliklarni to'g'ri handle qilishni ko'rsatadi.
"""

import requests
from requests.exceptions import (
    RequestException,
    ConnectionError,
    Timeout,
    HTTPError
)


def make_request_with_error_handling(url, timeout=5):
    """
    Xatolarni to'liq handle qiluvchi so'rov funksiyasi
    
    Args:
        url (str): API endpoint
        timeout (int): Timeout vaqti (soniyalarda)
    
    Returns:
        dict or None: API javob ma'lumotlari yoki None
    """
    try:
        print(f"📡 So'rov yuborilmoqda: {url}")
        response = requests.get(url, timeout=timeout)
        
        # HTTP xatolarini tekshirish (4xx, 5xx)
        response.raise_for_status()
        
        print(f"✅ Muvaffaqiyatli! Status: {response.status_code}")
        return response.json()
        
    except ConnectionError:
        print("❌ Internet bilan bog'lanishda xato!")
        print("   Internetni tekshiring va qayta urinib ko'ring.")
        return None
        
    except Timeout:
        print(f"⏱️  Timeout! {timeout} soniyada javob kelmadi.")
        print("   Server sekin ishlayotgan bo'lishi mumkin.")
        return None
        
    except HTTPError as e:
        status_code = e.response.status_code
        
        if status_code == 404:
            print("❌ 404: Ma'lumot topilmadi!")
        elif status_code == 401:
            print("❌ 401: Autentifikatsiya talab qilinadi!")
        elif status_code == 403:
            print("❌ 403: Ruxsat yo'q!")
        elif status_code >= 500:
            print(f"❌ {status_code}: Server xatosi!")
        else:
            print(f"❌ HTTP xato: {status_code}")
        
        return None
        
    except ValueError:
        print("❌ JSON parse qilishda xato!")
        print("   Server noto'g'ri format qaytardi.")
        return None
        
    except RequestException as e:
        print(f"❌ Kutilmagan xato: {e}")
        return None


def safe_get_user(user_id):
    """Xavfsiz foydalanuvchi ma'lumotini olish"""
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    return make_request_with_error_handling(url)


def test_various_errors():
    """Turli xatolarni test qilish"""
    
    print("\n" + "="*70)
    print("XATOLARNI TEST QILISH")
    print("="*70 + "\n")
    
    # Test 1: Muvaffaqiyatli so'rov
    print("Test 1: ✅ To'g'ri so'rov")
    print("-" * 70)
    data = safe_get_user(1)
    if data:
        print(f"👤 Foydalanuvchi: {data['name']}")
    print()
    
    # Test 2: 404 xato (mavjud emas)
    print("\nTest 2: ❌ 404 - Topilmadi")
    print("-" * 70)
    data = safe_get_user(999)
    print()
    
    # Test 3: Noto'g'ri URL
    print("\nTest 3: ❌ Noto'g'ri URL")
    print("-" * 70)
    url = "https://jsonplaceholder.typicode.com/invalid-endpoint"
    make_request_with_error_handling(url)
    print()
    
    # Test 4: Timeout (juda qisqa timeout)
    print("\nTest 4: ⏱️  Timeout test")
    print("-" * 70)
    url = "https://jsonplaceholder.typicode.com/posts"
    make_request_with_error_handling(url, timeout=0.001)
    print()
    
    # Test 5: Mavjud bo'lmagan domen
    print("\nTest 5: ❌ Mavjud bo'lmagan domen")
    print("-" * 70)
    url = "https://this-domain-definitely-does-not-exist-12345.com/api"
    make_request_with_error_handling(url, timeout=3)
    print()


def retry_with_exponential_backoff(url, max_retries=3):
    """
    Exponential backoff bilan qayta urinish
    
    Agar so'rov muvaffaqiyatsiz bo'lsa, bir necha marta qayta urinadi.
    Har safar kutish vaqti 2 barobar ortadi.
    """
    import time
    
    for attempt in range(1, max_retries + 1):
        print(f"\n🔄 Urinish {attempt}/{max_retries}...")
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            print(f"✅ Muvaffaqiyatli! (Urinish: {attempt})")
            return response.json()
            
        except RequestException as e:
            if attempt == max_retries:
                print(f"❌ Barcha urinishlar muvaffaqiyatsiz! Xato: {e}")
                return None
            
            wait_time = 2 ** attempt  # 2, 4, 8 soniya
            print(f"⏳ {wait_time} soniya kutilmoqda...")
            time.sleep(wait_time)
    
    return None


def main():
    """Asosiy funksiya"""
    print("\n🛡️  API Xatolarni Boshqarish - Error Handling\n")
    
    # Turli xatolarni test qilish
    test_various_errors()
    
    # Retry mexanizmi demo
    print("\n" + "="*70)
    print("RETRY MEXANIZMI (Qayta urinish)")
    print("="*70)
    
    # Bu URL timeout berishi uchun juda qisqa timeout beramiz
    url = "https://jsonplaceholder.typicode.com/posts/1"
    result = retry_with_exponential_backoff(url, max_retries=3)
    
    if result:
        print(f"\n✅ Ma'lumot olindi: {result['title'][:50]}...")
    
    print("\n" + "="*70)
    print("✅ Dastur tugadi!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()