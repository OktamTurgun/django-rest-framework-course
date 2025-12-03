"""
Cache Strategies - Cache strategiyalari
"""
from django.core.cache import cache
from datetime import datetime
import time

# Dummy models (simulatsiya uchun)
class Book:
    def __init__(self, id, title, author):
        self.id = id
        self.title = title
        self.author = author
    
    def __repr__(self):
        return f"Book({self.id}, '{self.title}', '{self.author}')"


# Database simulatsiyasi
DATABASE = {
    1: Book(1, "Django for Beginners", "William Vincent"),
    2: Book(2, "Two Scoops of Django", "Daniel Roy Greenfeld"),
    3: Book(3, "Django REST Framework", "John Smith"),
}


# === 1. CACHE-ASIDE (LAZY LOADING) ===
print("=== 1. Cache-Aside Strategy ===")

def get_book_cache_aside(book_id):
    """
    Cache-Aside: Birinchi cache'ga qarash, yo'q bo'lsa DB'dan olish
    """
    cache_key = f'book_{book_id}'
    
    # 1. Cache'ga qarash
    book = cache.get(cache_key)
    
    if book is not None:
        print(f"CACHE HIT: Book {book_id} cache'dan olindi")
        return book
    
    # 2. Cache'da yo'q, DB'dan olamiz
    print(f"CACHE MISS: Book {book_id} DB'dan yuklanmoqda...")
    time.sleep(0.1)  # DB query simulatsiyasi
    book = DATABASE.get(book_id)
    
    if book:
        # 3. Cache'ga saqlaymiz
        cache.set(cache_key, book, timeout=300)
        print(f"Cache'ga saqlandi: {cache_key}")
    
    return book

# Test
print("Birinchi marta (DB'dan):")
book = get_book_cache_aside(1)
print(f"Natija: {book}\n")

print("Ikkinchi marta (cache'dan):")
book = get_book_cache_aside(1)
print(f"Natija: {book}\n")


# === 2. WRITE-THROUGH STRATEGY ===
print("=== 2. Write-Through Strategy ===")

def update_book_write_through(book_id, title):
    """
    Write-Through: DB va cache'ga bir vaqtda yozish
    """
    cache_key = f'book_{book_id}'
    
    # 1. DB'ni yangilash
    print(f"DB'ni yangilash...")
    time.sleep(0.1)
    if book_id in DATABASE:
        DATABASE[book_id].title = title
        book = DATABASE[book_id]
        
        # 2. Cache'ni yangilash (sinxron)
        print(f"Cache'ni yangilash...")
        cache.set(cache_key, book, timeout=300)
        
        print(f"Book {book_id} yangilandi (DB + Cache)")
        return book
    return None

# Test
print("Book'ni yangilash:")
book = update_book_write_through(1, "Django for Professionals")
print(f"Yangilangan: {book}\n")


# === 3. WRITE-BEHIND (WRITE-BACK) STRATEGY ===
print("=== 3. Write-Behind Strategy ===")

# Yozish uchun queue
write_queue = []

def update_book_write_behind(book_id, title):
    """
    Write-Behind: Avval cache'ga yozish, keyin DB'ga
    """
    cache_key = f'book_{book_id}'
    
    # 1. Cache'ni darhol yangilash
    if book_id in DATABASE:
        book = DATABASE[book_id]
        book.title = title
        cache.set(cache_key, book, timeout=300)
        print(f"  ⚡ Cache darhol yangilandi: {cache_key}")
        
        # 2. DB yozish uchun queue'ga qo'shish
        write_queue.append((book_id, title))
        print(f"  📋 DB queue'ga qo'shildi")
        
        return book
    return None

def flush_write_queue():
    """Queue'dagi o'zgarishlarni DB'ga yozish"""
    print(f"\n  🔄 Queue'ni DB'ga yozish ({len(write_queue)} ta)...")
    for book_id, title in write_queue:
        time.sleep(0.1)  # DB write simulatsiyasi
        if book_id in DATABASE:
            DATABASE[book_id].title = title
        print(f"  ✅ Book {book_id} DB'ga yozildi")
    write_queue.clear()

# Test
print("Book'larni yangilash (Write-Behind):")
update_book_write_behind(2, "Two Scoops of Django 3.x")
update_book_write_behind(3, "REST APIs with Django")
flush_write_queue()
print()


# === 4. REFRESH-AHEAD STRATEGY ===
print("=== 4. Refresh-Ahead Strategy ===")

def get_book_refresh_ahead(book_id, ttl_threshold=0.8):
    """
    Refresh-Ahead: TTL tugashidan oldin yangilash
    """
    cache_key = f'book_{book_id}'
    
    # Cache'dan olish
    book = cache.get(cache_key)
    
    if book:
        # TTL tekshirish
        ttl = cache.ttl(cache_key) if hasattr(cache, 'ttl') else None
        if ttl and ttl < 300 * ttl_threshold:  # 80% o'tgan
            print(f"  🔄 TTL past ({ttl}s), proactive yangilash...")
            book = DATABASE.get(book_id)
            cache.set(cache_key, book, timeout=300)
        else:
            print(f"Cache'dan olindi (TTL: {ttl}s)")
        return book
    
    # Cache miss
    print(f"  ❌ Cache miss, DB'dan yuklash...")
    book = DATABASE.get(book_id)
    if book:
        cache.set(cache_key, book, timeout=300)
    return book

# Test
cache.set('book_1', DATABASE[1], timeout=60)
book = get_book_refresh_ahead(1)
print(f"Natija: {book}\n")


# === 5. CACHE WARMING ===
print("=== 5. Cache Warming ===")

def warm_cache():
    """
    Cache Warming: Dastur ishga tushganda cache'ni to'ldirish
    """
    print("Cache warming boshlandi...")
    
    for book_id, book in DATABASE.items():
        cache_key = f'book_{book_id}'
        cache.set(cache_key, book, timeout=3600)  # 1 soat
        print(f"  💾 Cached: {cache_key}")

print("Cache warming tugadi")

# Test
warm_cache()
print()

# === 6. MULTI-TIER CACHING ===
print("=== 6. Multi-Tier Caching ===")
# L1: Local in-memory cache
local_cache = {}

def get_book_multi_tier(book_id):
    """
    Multi-tier: Local cache -> Redis cache -> Database
    """
    # L1: Local cache
    if book_id in local_cache:
        print(f"  ⚡ L1 HIT (Memory): Book {book_id}")
        return local_cache[book_id]

    # L2: Redis cache
    cache_key = f'book_{book_id}'
    book = cache.get(cache_key)

    if book:
        print(f"  ✅ L2 HIT (Redis): Book {book_id}")
        local_cache[book_id] = book  # warm L1 as well
        return book

    # L3: Database
    print(f"  ❌ MISS: Book {book_id} DB'dan yuklanmoqda...")
    book = DATABASE.get(book_id)

    if book:
        cache.set(cache_key, book, timeout=300)
        local_cache[book_id] = book

    return book


# Test
print("Birinchi marta:")
get_book_multi_tier(1)
print("\nIkkinchi marta:")
get_book_multi_tier(1)
print()
print("Barcha cache strategiyalari ko'rib chiqildi!")