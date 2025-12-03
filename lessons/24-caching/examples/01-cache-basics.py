"""
Cache Basics - Cache asoslari
"""
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

# === 1. ODDIY SET/GET ===
print("=== Oddiy Cache Operatsiyalari ===")

# Ma'lumot saqlash
cache.set('my_key', 'Hello, Cache!', timeout=60)
print(f"Saqlandi: my_key = Hello, Cache!")

# Ma'lumot olish
value = cache.get('my_key')
print(f"Olingan qiymat: {value}")

# Default qiymat bilan olish
value = cache.get('not_exists', default='Default Value')
print(f"Mavjud bo'lmagan key: {value}")


# === 2. TIMEOUT (TTL) ===
print("\n=== Timeout (TTL) ===")

# 10 soniya uchun saqlash
cache.set('temp_key', 'Temporary value', timeout=10)
print("temp_key 10 soniya uchun saqlandi")

# Cheksiz vaqt uchun saqlash (None)
cache.set('permanent_key', 'Permanent value', timeout=None)
print("permanent_key abadiy saqlandi")

# Default timeout (settings'dan)
cache.set('default_key', 'Default timeout value')  # DEFAULT_TIMEOUT ishlatiladi


# === 3. ADD - FAQAT YO'Q BO'LSA QOSHISH ===
print("\n=== Add (faqat yo'q bo'lsa qo'shish) ===")

# Birinchi marta - qo'shiladi
result = cache.add('unique_key', 'First value', timeout=60)
print(f"Birinchi add: {result}")  # True

# Ikkinchi marta - qo'shilmaydi (mavjud)
result = cache.add('unique_key', 'Second value', timeout=60)
print(f"Ikkinchi add: {result}")  # False

value = cache.get('unique_key')
print(f"Hozirgi qiymat: {value}")  # First value


# === 4. GET_OR_SET - OL YOKI QO'SH ===
print("\n=== Get or Set ===")

def expensive_operation():
    """Qimmat operatsiya simulatsiyasi"""
    print("  -> Qimmat operatsiya bajarilmoqda...")
    return "Expensive Result"

# Birinchi chaqiruv - operatsiya bajariladi
result = cache.get_or_set('expensive_key', expensive_operation, timeout=60)
print(f"Birinchi chaqiruv: {result}")

# Ikkinchi chaqiruv - cache'dan olinadi
result = cache.get_or_set('expensive_key', expensive_operation, timeout=60)
print(f"Ikkinchi chaqiruv: {result}")


# === 5. MULTIPLE KEYS ===
print("\n=== Multiple Keys ===")

# Bir nechta key'larni birga saqlash
data = {
    'user_1': {'name': 'Ali', 'age': 25},
    'user_2': {'name': 'Vali', 'age': 30},
    'user_3': {'name': 'Gani', 'age': 35},
}
cache.set_many(data, timeout=60)
print("3 ta user saqlandi")

# Bir nechta key'larni birga olish
users = cache.get_many(['user_1', 'user_2', 'user_3'])
for key, value in users.items():
    print(f"{key}: {value}")


# === 6. DELETE ===
print("\n=== Delete ===")

cache.set('delete_me', 'I will be deleted')
print("Key yaratildi: delete_me")

# Bir key o'chirish
cache.delete('delete_me')
print("Key o'chirildi")

value = cache.get('delete_me')
print(f"O'chirilgan key: {value}")  # None

# Ko'p key'larni o'chirish
cache.set_many({'key1': 1, 'key2': 2, 'key3': 3})
cache.delete_many(['key1', 'key2', 'key3'])
print("Ko'p key'lar o'chirildi")


# === 7. INCREMENT/DECREMENT ===
print("\n=== Increment/Decrement ===")

# Counter
cache.set('page_views', 0)
print(f"Dastlabki: {cache.get('page_views')}")

cache.incr('page_views')  # +1
print(f"1 marta incr: {cache.get('page_views')}")

cache.incr('page_views', delta=5)  # +5
print(f"5 marta incr: {cache.get('page_views')}")

cache.decr('page_views', delta=2)  # -2
print(f"2 marta decr: {cache.get('page_views')}")


# === 8. CLEAR - HAMMA CACHE'NI TOZALASH ===
print("\n=== Clear All Cache ===")

cache.set_many({'a': 1, 'b': 2, 'c': 3})
print("Bir nechta key'lar yaratildi")

cache.clear()
print("Hamma cache tozalandi")

value = cache.get('a')
print(f"Tozalanganidan keyin: {value}")  # None


# === 9. TOUCH - TTL YANGILASH ===
print("\n=== Touch (TTL yangilash) ===")

cache.set('touch_me', 'Original value', timeout=10)
print("Key 10 soniya uchun yaratildi")

# TTL'ni 60 soniyaga oshiramiz
cache.touch('touch_me', timeout=60)
print("TTL 60 soniyaga yangilandi")


# === 10. CUSTOM KEY FUNCTIONS ===
print("\n=== Custom Key Functions ===")

def make_key(prefix, obj_id, version=1):
    """Custom key generator"""
    return f"{prefix}:v{version}:{obj_id}"

# Foydalanish
book_key = make_key('book', 123, version=2)
cache.set(book_key, {'title': 'Django Book'}, timeout=60)
print(f"Custom key: {book_key}")

book = cache.get(book_key)
print(f"Olingan ma'lumot: {book}")


print("\n✅ Cache basics to'liq o'rganildi!")