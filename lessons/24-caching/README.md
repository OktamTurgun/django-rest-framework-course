# Lesson 24: Caching in Django REST Framework

## Dars Maqsadi
Django REST Framework'da caching mexanizmlarini o'rganish va amaliyotda qo'llash.

## Mavzular

### 1. Caching Asoslari
- Cache nima va nima uchun kerak?
- Cache turlari
- Cache backend'lar
- TTL (Time To Live) tushunchasi

### 2. Redis Cache
- Redis nima?
- Redis o'rnatish va sozlash
- Django bilan integratsiya
- Redis cache backend

### 3. Cache Strategies (Strategiyalar)
- **Cache-Aside (Lazy Loading)**: Ma'lumot kerak bo'lganda cache'ga yuklanadi
- **Write-Through**: Ma'lumot yozilganda bir vaqtda cache'ga ham yoziladi
- **Write-Behind**: Ma'lumot avval cache'ga yoziladi, keyin DB'ga
- **Refresh-Ahead**: TTL tugashidan oldin ma'lumot yangilanadi

### 4. Cache Invalidation
- Cache'ni tozalash strategiyalari
- Signal'lar orqali invalidation
- Manual invalidation
- Time-based invalidation

### 5. Django Cache Framework
- Per-site caching
- Per-view caching
- Template fragment caching
- Low-level cache API

---

## Redis O'rnatish

### Windows uchun:
```powershell
# WSL orqali Redis o'rnatish (tavsiya etiladi)
wsl --install
wsl -d Ubuntu
sudo apt update
sudo apt install redis-server
redis-server

# Yoki Memurai (Windows native Redis)
# https://www.memurai.com/get-memurai dan yuklab oling
```

### Linux/Mac uchun:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis

# Mac (Homebrew)
brew install redis
brew services start redis
```

### Docker orqali (barcha platformalar uchun):
```bash
docker run -d -p 6379:6379 --name redis redis:alpine
```

---

## Kerakli Paketlar
```bash
pip install redis django-redis hiredis
```

---

## Django Settings Konfiguratsiyasi

### settings.py
```python
# Cache Settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            },
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
        },
        'KEY_PREFIX': 'library',
        'TIMEOUT': 300,  # 5 daqiqa (default)
    }
}

# Session cache
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

---

## Cache Strategies Namunalari

### 1. Cache-Aside (Lazy Loading)
```python
from django.core.cache import cache

def get_book(book_id):
    cache_key = f'book_{book_id}'
    
    # Cache'dan olishga harakat qilamiz
    book = cache.get(cache_key)
    
    if book is None:
        # Cache'da yo'q, DB'dan olamiz
        book = Book.objects.get(id=book_id)
        # Cache'ga saqlaymiz
        cache.set(cache_key, book, timeout=300)
    
    return book
```

### 2. Write-Through
```python
def update_book(book_id, data):
    book = Book.objects.get(id=book_id)
    for key, value in data.items():
        setattr(book, key, value)
    
    # DB'ga yozamiz
    book.save()
    
    # Cache'ni yangilaymiz
    cache_key = f'book_{book_id}'
    cache.set(cache_key, book, timeout=300)
    
    return book
```

### 3. Cache Invalidation
```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Book)
def invalidate_book_cache(sender, instance, **kwargs):
    cache_key = f'book_{instance.id}'
    cache.delete(cache_key)
    # List cache'ni ham tozalaymiz
    cache.delete('books_list')

@receiver(post_delete, sender=Book)
def invalidate_book_cache_on_delete(sender, instance, **kwargs):
    cache_key = f'book_{instance.id}'
    cache.delete(cache_key)
    cache.delete('books_list')
```

---

## View-Level Caching

### Method 1: Decorator
```python
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 15), name='dispatch')
class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
```

### Method 2: Manual Caching
```python
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response

class BookListView(APIView):
    def get(self, request):
        cache_key = 'books_list'
        
        # Cache'dan olamiz
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        # Cache'da yo'q, DB'dan olamiz
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        data = serializer.data
        
        # Cache'ga saqlaymiz
        cache.set(cache_key, data, timeout=900)  # 15 daqiqa
        
        return Response(data)
```

---

## QuerySet Caching
```python
from django.core.cache import cache

class CachedBookManager(models.Manager):
    def get_all_cached(self):
        cache_key = 'all_books'
        books = cache.get(cache_key)
        
        if books is None:
            books = list(self.all().select_related('author'))
            cache.set(cache_key, books, timeout=600)
        
        return books

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    objects = CachedBookManager()
```

---

## Low-Level Cache API
```python
from django.core.cache import cache

# Oddiy set/get
cache.set('my_key', 'hello, world!', timeout=30)
value = cache.get('my_key')

# Default qiymat bilan
value = cache.get('key', default='default_value')

# Set if not exists
cache.add('key', 'value', timeout=30)

# Multiple keys
cache.set_many({'a': 1, 'b': 2, 'c': 3}, timeout=30)
values = cache.get_many(['a', 'b', 'c'])

# Delete
cache.delete('key')
cache.delete_many(['a', 'b', 'c'])

# Clear all
cache.clear()

# Increment/Decrement
cache.set('counter', 0)
cache.incr('counter')  # 1
cache.incr('counter', 5)  # 6
cache.decr('counter', 2)  # 4
```

---

## Cache Best Practices

1. **Cache faqat ko'p o'qiladigan ma'lumotlarni**
   - Read-heavy operations
   - Tez-tez o'zgarmaydigan data

2. **TTL to'g'ri tanlang**
   - Tez o'zgaradigan data: 1-5 daqiqa
   - Sekin o'zgaradigan data: 15-60 daqiqa
   - Deyarli static data: bir necha soat

3. **Cache invalidation strategiyasini rejalashtiring**
   - Signal'lar orqali avtomatik
   - Manual invalidation
   - TTL-based

4. **Cache key naming convention**
   - Tushunarli nomlar: `book_list`, `user_profile_123`
   - Prefix ishlatish: `library:books:123`
   - Versioning: `v1:book_list`

5. **Cache monitoring**
   - Hit/Miss ratio
   - Memory usage
   - Eviction rate

---

## Cache Testing
```python
from django.test import TestCase
from django.core.cache import cache

class CacheTestCase(TestCase):
    def setUp(self):
        cache.clear()
    
    def tearDown(self):
        cache.clear()
    
    def test_book_caching(self):
        book = Book.objects.create(title='Test Book')
        cache_key = f'book_{book.id}'
        
        # Cache'ga saqlaymiz
        cache.set(cache_key, book, timeout=300)
        
        # Cache'dan olamiz
        cached_book = cache.get(cache_key)
        self.assertIsNotNone(cached_book)
        self.assertEqual(cached_book.title, 'Test Book')
```

---

## Redis Monitoring
```python
# Redis info
from django_redis import get_redis_connection
con = get_redis_connection("default")
print(con.info())

# Keys count
print(con.dbsize())

# All keys
keys = con.keys('*')
print(keys)
```

---

## Xulosa

Cache - bu performanceni yaxshilashning eng samarali usullaridan biri. To'g'ri ishlatilgan cache:
- Response time'ni 10-100 marta tezlashtiradi
- Database load'ni kamaytiradi
- Scalability'ni oshiradi

Lekin esda tuting:
- Cache invalidation murakkab muammo
- Cache miss paytida overhead bo'lishi mumkin
- Memory boshqarish muhim

---

## Keyingi Darslar

- Lesson 25: CORS 
- Lesson 26: Versioning 
- Lesson 27: Error Handling 