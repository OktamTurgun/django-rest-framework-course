"""
Dars 02 - HTTP Methods va Status Kodlar
Misol 2: Headers va Query Parameters bilan ishlash

Bu dastur HTTP headers va query parameters'ni qanday
ishlatishni ko'rsatadi.
"""

import requests
import json
from datetime import datetime


BASE_URL = "https://jsonplaceholder.typicode.com"


def demo_headers():
    """Headers bilan ishlash"""
    print("\n" + "="*70)
    print("📋 HEADERS BILAN ISHLASH")
    print("="*70)
    
    url = f"{BASE_URL}/posts/1"
    
    # Custom headers
    headers = {
        "User-Agent": "DRF-Course-Student/1.0",
        "Accept": "application/json",
        "Accept-Language": "uz-UZ,uz;q=0.9,en;q=0.8",
        "Custom-Header": "Test-Value"
    }
    
    print("\n📤 Yuborilayotgan headers:")
    print(json.dumps(headers, indent=2))
    
    response = requests.get(url, headers=headers, timeout=10)
    
    print(f"\n📊 Status: {response.status_code}")
    print("\n📥 Kelgan response headers:")
    
    # Muhim headerslarni ko'rsatish
    important_headers = [
        'Content-Type',
        'Content-Length',
        'Server',
        'Date',
        'Cache-Control'
    ]
    
    for header in important_headers:
        if header in response.headers:
            print(f"  {header}: {response.headers[header]}")


def demo_query_parameters():
    """Query parameters bilan filterlash"""
    print("\n" + "="*70)
    print("🔍 QUERY PARAMETERS BILAN FILTERLASH")
    print("="*70)
    
    url = f"{BASE_URL}/posts"
    
    # Variant 1: Dictionary
    print("\n1️⃣ Dictionary yordamida:")
    params = {
        "userId": 1,
        "_limit": 3
    }
    
    response = requests.get(url, params=params, timeout=10)
    print(f"📍 URL: {response.url}")
    print(f"📊 Status: {response.status_code}")
    print(f"📦 Natijalar: {len(response.json())} ta post")
    
    # Variant 2: To'g'ridan-to'g'ri URL'da
    print("\n2️⃣ To'g'ridan-to'g'ri URL'da:")
    url_with_params = f"{BASE_URL}/posts?userId=2&_limit=5"
    response = requests.get(url_with_params, timeout=10)
    print(f"📍 URL: {response.url}")
    print(f"📦 Natijalar: {len(response.json())} ta post")


def demo_multiple_filters():
    """Ko'p filterlar bilan ishlash"""
    print("\n" + "="*70)
    print("🎯 KO'P FILTERLAR")
    print("="*70)
    
    url = f"{BASE_URL}/comments"
    
    # Ko'p filterlar
    params = {
        "postId": 1,  # Post ID
        "_limit": 5,   # Limit
        "_page": 1     # Pagination
    }
    
    response = requests.get(url, params=params, timeout=10)
    
    print(f"📍 URL: {response.url}")
    print(f"📊 Status: {response.status_code}")
    
    if response.status_code == 200:
        comments = response.json()
        print(f"📦 {len(comments)} ta comment topildi\n")
        
        for i, comment in enumerate(comments, 1):
            print(f"{i}. {comment['name']}")
            print(f"   Email: {comment['email']}")
            print(f"   {comment['body'][:40]}...")
            print()


def demo_authentication_header():
    """Authentication header (Bearer token)"""
    print("\n" + "="*70)
    print("🔐 AUTHENTICATION HEADER")
    print("="*70)
    
    # Bu faqat demo - JSONPlaceholder token talab qilmaydi
    url = f"{BASE_URL}/posts/1"
    
    # Real API'larda shunday ishlatiladi
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # Fake token
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("📋 Headers:")
    print(f"  Authorization: Bearer {token[:30]}...")
    
    # JSONPlaceholder token tekshirmaydi, lekin real API'da kerak
    response = requests.get(url, headers=headers, timeout=10)
    
    print(f"\n📊 Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Autentifikatsiya muvaffaqiyatli (demo)")
    elif response.status_code == 401:
        print("❌ 401 Unauthorized - Token noto'g'ri yoki yo'q")
    elif response.status_code == 403:
        print("❌ 403 Forbidden - Ruxsat yo'q")


def demo_custom_request():
    """To'liq sozlangan so'rov"""
    print("\n" + "="*70)
    print("⚙️  TO'LIQ SOZLANGAN SO'ROV")
    print("="*70)
    
    url = f"{BASE_URL}/posts"
    
    # To'liq sozlamalar
    headers = {
        "User-Agent": "DRF-Course/1.0 (Learning)",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "uz-UZ,en-US",
        "X-Request-ID": f"req-{datetime.now().timestamp()}",
        "X-Client-Version": "1.0.0"
    }
    
    params = {
        "userId": 1,
        "_limit": 3,
        "_sort": "id",
        "_order": "desc"
    }
    
    print("📋 Headers:")
    for key, value in headers.items():
        print(f"  {key}: {value}")
    
    print("\n🔍 Query Parameters:")
    for key, value in params.items():
        print(f"  {key}: {value}")
    
    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )
    
    print(f"\n📍 Final URL: {response.url}")
    print(f"📊 Status: {response.status_code}")
    print(f"📦 Natijalar: {len(response.json())} ta post")
    
    # Response headerslarni ham ko'rish
    print("\n📥 Response Headers:")
    print(f"  Content-Type: {response.headers.get('Content-Type')}")
    print(f"  Content-Length: {response.headers.get('Content-Length')}")
    print(f"  Date: {response.headers.get('Date')}")


def demo_post_with_headers():
    """POST so'rov headerlar bilan"""
    print("\n" + "="*70)
    print("📮 POST SO'ROV + HEADERS")
    print("="*70)
    
    url = f"{BASE_URL}/posts"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "DRF-Course-Student/1.0"
    }
    
    data = {
        "title": "Headers bilan POST",
        "body": "Bu headers ishlatgan holda yaratildi",
        "userId": 1
    }
    
    print("📋 Headers:")
    for key, value in headers.items():
        print(f"  {key}: {value}")
    
    print("\n📦 Ma'lumot:")
    print(json.dumps(data, indent=2))
    
    response = requests.post(
        url,
        json=data,
        headers=headers,
        timeout=10
    )
    
    print(f"\n📊 Status: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Yaratildi! ID: {result['id']}")


def main():
    """Asosiy funksiya"""
    
    print("\n" + "="*70)
    print("🚀 HEADERS VA QUERY PARAMETERS DEMO")
    print("="*70)
    
    # 1. Headers
    demo_headers()
    
    # 2. Query parameters
    demo_query_parameters()
    
    # 3. Ko'p filterlar
    demo_multiple_filters()
    
    # 4. Authentication
    demo_authentication_header()
    
    # 5. To'liq sozlangan so'rov
    demo_custom_request()
    
    # 6. POST + Headers
    demo_post_with_headers()
    
    print("\n" + "="*70)
    print("✅ DEMO TUGADI!")
    print("="*70)
    
    # Xulosa
    print("\n💡 ESDA SAQLANG:")
    print("""
Headers:
  - User-Agent: Client haqida ma'lumot
  - Authorization: Token/kredensial
  - Content-Type: Yuborilayotgan ma'lumot turi
  - Accept: Qabul qilinadigan format

Query Parameters:
  - Filterlash: ?userId=1
  - Pagination: ?_page=2&_limit=10
  - Sorting: ?_sort=id&_order=desc
  - Multiple: ? bilan birlashadi, & bilan ajratiladi
    """)


if __name__ == "__main__":
    main()