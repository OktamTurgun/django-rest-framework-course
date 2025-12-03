"""
Cache Invalidation - Cache'ni tozalash strategiyalari
"""
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import time

# Dummy models
class Book:
    def __init__(self, id, title, author, price):
        self.id = id
        self.title = title
        self.author = author
        self.price = price
    
    def save(self):
        """Simulatsiya: Model.save()"""
        print(f"  💾 Saving book {self.id} to database...")
        time.sleep(0.05)
    
    def __repr__(self):
        return f"Book({self.id}, '{self.title}')"


# === 1. MANUAL INVALIDATION ===
print("=== 1. Manual Cache Invalidation ===")

def create_book_with_cache(book_id, title, author, price):
    """Book yaratish va cache'ga qo'shish"""
    book = Book(book_id, title, author, price)
    book.save()
    
    # Cache'ga qo'shish
    cache_key = f'book_{book_id}'
    cache.set(cache_key, book, timeout=300)
    print(f"  ✅ Book cached: {cache_key}")
    
    return book

def update_book_with_invalidation(book_id, **updates):
    """Book yangilash va cache'ni tozalash"""
    print(f"\n📝 Updating book {book_id}...")
    
    # Cache'dan o'chirish (invalidation)
    cache_key = f'book_{book_id}'
    cache.delete(cache_key)
    print(f"  🗑️ Cache invalidated: {cache_key}")
    
    # Ma'lumotni yangilash
    book = Book(book_id, updates.get('title'), updates.get('author'), updates.get('price'))
    book.save()
    print(f"  ✅ Book updated in database")
    
    return book

# Test
print("Book yaratish:")
book = create_book_with_cache(1, "Django Guide", "John Doe", 29.99)

print("\nBook yangilash:")
update_book_with_invalidation(1, title="Django Complete Guide", author="John Doe", price=39.99)


# === 2. PATTERN-BASED INVALIDATION ===
print("\n\n=== 2. Pattern-Based Invalidation ===")

def invalidate_pattern(pattern):
    """Pattern bo'yicha barcha keylarni o'chirish"""
    print(f"  🔍 Searching for keys matching: {pattern}")
    
    # Redis'da keys() ishlatish (production'da scan() ishlatish kerak!)
    from django_redis import get_redis_connection
    try:
        redis_conn = get_redis_connection("default")
        keys = redis_conn.keys(pattern)
        
        if keys:
            redis_conn.delete(*keys)
            print(f"  🗑️ Deleted {len(keys)} keys: {keys}")
        else:
            print(f"  ℹ️ No keys found")
    except:
        print("  ⚠️ Redis not available, using cache.delete_pattern")
        # Fallback
        cache.delete_pattern(pattern)

# Test
cache.set('book_1', 'Book 1', timeout=300)
cache.set('book_2', 'Book 2', timeout=300)
cache.set('book_3', 'Book 3', timeout=300)
cache.set('author_1', 'Author 1', timeout=300)

print("\nBarcha book keylarni o'chirish:")
invalidate_pattern('book_*')


# === 3. TIME-BASED INVALIDATION (TTL) ===
print("\n\n=== 3. Time-Based Invalidation ===")

def cache_with_smart_ttl(key, value, data_type='static'):
    """
    Data turiga qarab TTL belgilash
    - static: 1 soat (3600s)
    - semi-static: 15 daqiqa (900s)
    - dynamic: 5 daqiqa (300s)
    - realtime: 1 daqiqa (60s)
    """
    ttl_map = {
        'static': 3600,
        'semi-static': 900,
        'dynamic': 300,
        'realtime': 60
    }
    
    timeout = ttl_map.get(data_type, 300)
    cache.set(key, value, timeout=timeout)
    print(f"  💾 Cached '{key}' with TTL: {timeout}s ({data_type})")

# Test
cache_with_smart_ttl('site_config', {'name': 'MyApp'}, 'static')
cache_with_smart_ttl('book_list', ['Book1', 'Book2'], 'semi-static')
cache_with_smart_ttl('user_profile_123', {'name': 'Ali'}, 'dynamic')
cache_with_smart_ttl('stock_price', 150.5, 'realtime')


# === 4. SIGNAL-BASED INVALIDATION ===
print("\n\n=== 4. Signal-Based Invalidation ===")

@receiver(post_save, sender=Book)
def invalidate_book_cache_on_save(sender, instance, created, **kwargs):
    """
    Book save qilinganda cache'ni avtomatik tozalash
    """
    cache_key = f'book_{instance.id}'
    cache.delete(cache_key)
    
    if created:
        print(f"  🆕 New book created, cache invalidated: {cache_key}")
    else:
        print(f"  ♻️ Book updated, cache invalidated: {cache_key}")
    
    # Related cache'larni ham tozalash
    cache.delete('book_list')
    cache.delete(f'author_{instance.author}_books')

@receiver(post_delete, sender=Book)
def invalidate_book_cache_on_delete(sender, instance, **kwargs):
    """
    Book o'chirilganda cache'ni avtomatik tozalash
    """
    cache_key = f'book_{instance.id}'
    cache.delete(cache_key)
    print(f"  🗑️ Book deleted, cache invalidated: {cache_key}")
    
    # Related cache'larni ham tozalash
    cache.delete('book_list')

print("Signal-based invalidation sozlandi!")
print("Book save/delete paytida avtomatik ishga tushadi")


# === 5. CACHE VERSIONING ===
print("\n\n=== 5. Cache Versioning ===")

CACHE_VERSION = 1

def get_versioned_key(base_key, version=None):
    """Version bilan cache key yaratish"""
    v = version or CACHE_VERSION
    return f'v{v}:{base_key}'

def cache_with_version(base_key, value, timeout=300):
    """Version bilan cache'ga saqlash"""
    key = get_versioned_key(base_key)
    cache.set(key, value, timeout=timeout)
    print(f"  💾 Cached: {key}")

def invalidate_by_version_bump():
    """Version'ni oshirish orqali butun cache'ni invalidate qilish"""
    global CACHE_VERSION
    CACHE_VERSION += 1
    print(f"  🔄 Cache version bumped to v{CACHE_VERSION}")
    print(f"  ℹ️ Old cached data automatically ignored")

# Test
print("V1 cache:")
cache_with_version('book_list', ['Book1', 'Book2'])
cache_with_version('user_list', ['User1', 'User2'])

print("\nVersion bump (barcha cache invalidate):")
invalidate_by_version_bump()

print("\nV2 cache:")
cache_with_version('book_list', ['Book1', 'Book2', 'Book3'])


# === 6. DEPENDENCY-BASED INVALIDATION ===
print("\n\n=== 6. Dependency-Based Invalidation ===")

class CacheDependency:
    """Cache dependencies boshqarish"""
    
    @staticmethod
    def get_dependencies(key):
        """Cache key dependencies'ni olish"""
        deps_key = f'deps:{key}'
        return cache.get(deps_key, [])
    
    @staticmethod
    def set_dependencies(key, dependencies):
        """Cache key uchun dependencies belgilash"""
        deps_key = f'deps:{key}'
        cache.set(deps_key, dependencies, timeout=3600)
    
    @staticmethod
    def invalidate_with_dependencies(key):
        """Key va uning dependencies'larini o'chirish"""
        print(f"  🗑️ Invalidating: {key}")
        cache.delete(key)
        
        # Dependencies'larni ham o'chirish
        dependencies = CacheDependency.get_dependencies(key)
        for dep_key in dependencies:
            print(f"  🗑️ Invalidating dependency: {dep_key}")
            cache.delete(dep_key)

# Test
# Book detail page book_list'ga bog'liq
cache.set('book_detail_1', 'Book 1 Details', timeout=300)
CacheDependency.set_dependencies('book_detail_1', ['book_list', 'author_1_books'])

cache.set('book_list', ['Book1', 'Book2'], timeout=300)
cache.set('author_1_books', ['Book1'], timeout=300)

print("Book detail va dependencies yaratildi")
print("\nBook detail'ni dependencies bilan o'chirish:")
CacheDependency.invalidate_with_dependencies('book_detail_1')


# === 7. SOFT vs HARD INVALIDATION ===
print("\n\n=== 7. Soft vs Hard Invalidation ===")

def soft_invalidate(key, new_value=None):
    """
    Soft invalidation: Key'ni o'chirmasdan yangi qiymat bilan almashtirish
    """
    if new_value is not None:
        cache.set(key, new_value, timeout=300)
        print(f"  ♻️ Soft invalidation: {key} yangilandi")
    else:
        cache.delete(key)
        print(f"  🗑️ Hard invalidation: {key} o'chirildi")

def hard_invalidate(key):
    """
    Hard invalidation: Key'ni butunlay o'chirish
    """
    cache.delete(key)
    print(f"  🗑️ Hard invalidation: {key} o'chirildi")

# Test
cache.set('config', {'theme': 'light'}, timeout=300)

print("Soft invalidation (yangi qiymat bilan):")
soft_invalidate('config', {'theme': 'dark'})

print("\nHard invalidation (butunlay o'chirish):")
hard_invalidate('config')


# === 8. BATCH INVALIDATION ===
print("\n\n=== 8. Batch Invalidation ===")

def batch_invalidate(keys):
    """Ko'p keylarni bir vaqtda o'chirish"""
    print(f"  🗑️ Batch invalidating {len(keys)} keys...")
    cache.delete_many(keys)
    print(f"  ✅ Deleted: {', '.join(keys)}")

# Test
cache.set_many({
    'temp_1': 'Data 1',
    'temp_2': 'Data 2',
    'temp_3': 'Data 3',
    'temp_4': 'Data 4',
})

print("Batch o'chirish:")
batch_invalidate(['temp_1', 'temp_2', 'temp_3', 'temp_4'])


# === 9. CONDITIONAL INVALIDATION ===
print("\n\n=== 9. Conditional Invalidation ===")

def conditional_invalidate(key, condition_func):
    """
    Shart asosida invalidate qilish
    """
    value = cache.get(key)
    
    if value and condition_func(value):
        cache.delete(key)
        print(f"  🗑️ Condition met, invalidated: {key}")
        return True
    else:
        print(f"  ℹ️ Condition not met, kept: {key}")
        return False

# Test
cache.set('product_price', 100, timeout=300)

print("Narx 50'dan katta bo'lsa o'chirish:")
conditional_invalidate('product_price', lambda price: price > 50)

cache.set('product_price', 30, timeout=300)
print("\nNarx 50'dan katta bo'lsa o'chirish:")
conditional_invalidate('product_price', lambda price: price > 50)


print("\n\n✅ Barcha cache invalidation strategiyalari ko'rib chiqildi!")