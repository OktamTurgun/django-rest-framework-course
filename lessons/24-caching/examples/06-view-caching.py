"""
View Caching - Django REST Framework view'larni cache qilish
"""
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time
import hashlib
import json

# === DUMMY DATA ===
BOOKS_DATA = [
    {'id': 1, 'title': 'Django for Beginners', 'author': 'William Vincent', 'price': 29.99},
    {'id': 2, 'title': 'Django for APIs', 'author': 'William Vincent', 'price': 34.99},
    {'id': 3, 'title': 'Two Scoops of Django', 'author': 'Daniel Roy', 'price': 49.99},
]


# === 1. METHOD DECORATOR CACHING ===
print("=== 1. Method Decorator Caching ===\n")

@method_decorator(cache_page(60 * 15), name='dispatch')  # 15 daqiqa
class BookListView(APIView):
    """
    Butun view'ni cache qilish
    """
    def get(self, request):
        print("  ❌ CACHE MISS: Fetching books from database...")
        time.sleep(0.1)
        return Response({'results': BOOKS_DATA})

# Simulatsiya
print("View decorator bilan cache qilish misoli:")
print("@method_decorator(cache_page(60 * 15), name='dispatch')")
print("Bu butun view'ni 15 daqiqaga cache qiladi\n")


# === 2. MANUAL VIEW CACHING ===
print("=== 2. Manual View Caching ===\n")

class ManualCachedBookListView(APIView):
    """
    Manual cache bilan view
    """
    def get(self, request):
        cache_key = 'api:books:list'
        
        # Cache'dan olish
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            print("  ✅ CACHE HIT: Returning cached data")
            return Response(cached_data)
        
        # Cache miss
        print("  ❌ CACHE MISS: Fetching from database...")
        time.sleep(0.1)
        data = {'results': BOOKS_DATA}
        
        # Cache'ga saqlash
        cache.set(cache_key, data, timeout=900)  # 15 daqiqa
        print("  💾 Cached response data")
        
        return Response(data)

print("Manual cache misoli ko'rsatildi\n")


# === 3. QUERY PARAMETERS AWARE CACHING ===
print("=== 3. Query Parameters Aware Caching ===\n")

class FilteredBookListView(APIView):
    """
    Query params'ga qarab cache qilish
    """
    def get_cache_key(self, request):
        """Query parameters'dan cache key yaratish"""
        # Query params'ni tartiblab hash qilamiz
        query_params = dict(request.GET.items())
        params_str = json.dumps(query_params, sort_keys=True)
        params_hash = hashlib.md5(params_str.encode()).hexdigest()
        return f'api:books:filtered:{params_hash}'
    
    def get(self, request):
        cache_key = self.get_cache_key(request)
        
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            print(f"  ✅ CACHE HIT: {cache_key[:40]}...")
            return Response(cached_data)
        
        # Filter logic
        print(f"  ❌ CACHE MISS: Filtering books...")
        time.sleep(0.1)
        
        books = BOOKS_DATA.copy()
        
        # Min price filter
        min_price = request.GET.get('min_price')
        if min_price:
            books = [b for b in books if b['price'] >= float(min_price)]
        
        # Max price filter
        max_price = request.GET.get('max_price')
        if max_price:
            books = [b for b in books if b['price'] <= float(max_price)]
        
        data = {'results': books}
        cache.set(cache_key, data, timeout=300)
        print(f"  💾 Cached filtered results")
        
        return Response(data)

print("Query params aware caching misoli\n")


# === 4. USER-SPECIFIC CACHING ===
print("=== 4. User-Specific Caching ===\n")

class UserSpecificView(APIView):
    """
    Har bir user uchun alohida cache
    """
    def get_cache_key(self, request):
        """User ID'ga qarab cache key"""
        user_id = getattr(request.user, 'id', 'anonymous')
        return f'api:user:{user_id}:profile'
    
    def get(self, request):
        cache_key = self.get_cache_key(request)
        
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            print(f"  ✅ CACHE HIT: User profile from cache")
            return Response(cached_data)
        
        print(f"  ❌ CACHE MISS: Fetching user profile...")
        time.sleep(0.1)
        
        # Fake user data
        data = {
            'user_id': getattr(request.user, 'id', 'anonymous'),
            'name': 'Ali Valiyev',
            'email': 'ali@example.com'
        }
        
        cache.set(cache_key, data, timeout=300)
        print(f"  💾 Cached user profile")
        
        return Response(data)

print("User-specific caching misoli\n")


# === 5. CONDITIONAL CACHING ===
print("=== 5. Conditional Caching ===\n")

class ConditionalCachedView(APIView):
    """
    Shart asosida cache qilish
    """
    def should_cache(self, request):
        """Cache qilish kerakmi?"""
        # GET requests cache qilinadi
        if request.method != 'GET':
            return False
        
        # Authenticated users uchun cache qilmaymiz
        if hasattr(request, 'user') and request.user.is_authenticated:
            return False
        
        return True
    
    def get(self, request):
        cache_key = 'api:books:public'
        
        # Cache qilish kerakmi?
        if not self.should_cache(request):
            print("  ⚠️ Caching skipped (conditional)")
            time.sleep(0.1)
            return Response({'results': BOOKS_DATA})
        
        # Cache'dan olish
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            print("  ✅ CACHE HIT: Public books list")
            return Response(cached_data)
        
        print("  ❌ CACHE MISS: Fetching books...")
        time.sleep(0.1)
        data = {'results': BOOKS_DATA}
        
        cache.set(cache_key, data, timeout=600)
        print("  💾 Cached public books")
        
        return Response(data)

print("Conditional caching misoli\n")


# === 6. CACHE WITH ETAG ===
print("=== 6. Cache with ETag ===\n")

class ETagCachedView(APIView):
    """
    ETag bilan cache validation
    """
    def generate_etag(self, data):
        """Ma'lumotdan ETag yaratish"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def get(self, request):
        cache_key = 'api:books:etag'
        
        # Cache'dan olish
        cached_response = cache.get(cache_key)
        
        if cached_response is not None:
            etag = cached_response['etag']
            data = cached_response['data']
            
            # Client ETag bilan taqqoslash
            client_etag = request.META.get('HTTP_IF_NONE_MATCH')
            
            if client_etag == etag:
                print("  ✅ ETag match: 304 Not Modified")
                return Response(status=status.HTTP_304_NOT_MODIFIED)
            
            print("  ✅ CACHE HIT: Returning cached data with ETag")
            return Response(data, headers={'ETag': etag})
        
        # Cache miss
        print("  ❌ CACHE MISS: Generating response...")
        time.sleep(0.1)
        data = {'results': BOOKS_DATA}
        etag = self.generate_etag(data)
        
        # Cache'ga saqlash
        cache.set(cache_key, {'data': data, 'etag': etag}, timeout=600)
        print(f"  💾 Cached with ETag: {etag[:16]}...")
        
        return Response(data, headers={'ETag': etag})

print("ETag cache validation misoli\n")


# === 7. CACHE INVALIDATION ON WRITE ===
print("=== 7. Cache Invalidation on Write ===\n")

class BookCreateView(APIView):
    """
    POST request'da cache'ni invalidate qilish
    """
    def invalidate_caches(self):
        """Tegishli cache'larni tozalash"""
        print("  🗑️ Invalidating related caches...")
        cache.delete('api:books:list')
        cache.delete_pattern('api:books:filtered:*')
        cache.delete('api:books:public')
    
    def post(self, request):
        # Yangi book yaratish
        print("  📝 Creating new book...")
        time.sleep(0.1)
        
        new_book = {
            'id': len(BOOKS_DATA) + 1,
            'title': request.data.get('title'),
            'author': request.data.get('author'),
            'price': request.data.get('price')
        }
        
        BOOKS_DATA.append(new_book)
        
        # Cache'ni tozalash
        self.invalidate_caches()
        
        return Response(new_book, status=status.HTTP_201_CREATED)

print("Write operations'da cache invalidation misoli\n")


# === 8. TIERED CACHING ===
print("=== 8. Tiered Caching (View Level) ===\n")

# Local memory cache
local_cache = {}

class TieredCachedView(APIView):
    """
    Multi-tier caching: Memory -> Redis -> Database
    """
    def get(self, request):
        cache_key = 'api:books:tiered'
        
        # Tier 1: Local memory
        if cache_key in local_cache:
            print("  ⚡ TIER 1 HIT (Memory)")
            return Response(local_cache[cache_key])
        
        # Tier 2: Redis
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            print("  ✅ TIER 2 HIT (Redis)")
            local_cache[cache_key] = cached_data  # Promote to tier 1
            return Response(cached_data)
        
        # Tier 3: Database
        print("  ❌ MISS: Fetching from database...")
        time.sleep(0.1)
        data = {'results': BOOKS_DATA}
        
        # Cache in both tiers
        cache.set(cache_key, data, timeout=300)  # Redis
        local_cache[cache_key] = data  # Memory
        print("  💾 Cached in both tiers")
        
        return Response(data)

print("Tiered caching strategy misoli\n")


# === 9. CACHE MONITORING ===
print("=== 9. Cache Monitoring ===\n")

class CacheMonitoringMixin:
    """
    Cache hit/miss monitoring
    """
    def log_cache_hit(self, cache_key):
        """Cache hit log"""
        hits_key = 'cache:stats:hits'
        cache.incr(hits_key)
        print(f"  📊 Cache hit logged: {cache_key[:40]}...")
    
    def log_cache_miss(self, cache_key):
        """Cache miss log"""
        misses_key = 'cache:stats:misses'
        cache.incr(misses_key)
        print(f"  📊 Cache miss logged: {cache_key[:40]}...")
    
    def get_cache_stats(self):
        """Cache statistikasi"""
        hits = cache.get('cache:stats:hits', 0)
        misses = cache.get('cache:stats:misses', 0)
        total = hits + misses
        hit_rate = (hits / total * 100) if total > 0 else 0
        
        return {
            'hits': hits,
            'misses': misses,
            'total': total,
            'hit_rate': f'{hit_rate:.2f}%'
        }

class MonitoredView(APIView, CacheMonitoringMixin):
    """View with cache monitoring"""
    
    def get(self, request):
        cache_key = 'api:books:monitored'
        
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            self.log_cache_hit(cache_key)
            return Response(cached_data)
        
        self.log_cache_miss(cache_key)
        time.sleep(0.1)
        data = {'results': BOOKS_DATA}
        
        cache.set(cache_key, data, timeout=300)
        return Response(data)

# Stats endpoint
class CacheStatsView(APIView, CacheMonitoringMixin):
    """Cache statistikasini ko'rsatish"""
    
    def get(self, request):
        stats = self.get_cache_stats()
        print(f"\n📊 Cache Statistics:")
        print(f"  Hits: {stats['hits']}")
        print(f"  Misses: {stats['misses']}")
        print(f"  Hit Rate: {stats['hit_rate']}")
        return Response(stats)

print("Cache monitoring misoli\n")


# === 10. BEST PRACTICES ===
print("=== 10. View Caching Best Practices ===\n")

class BestPracticeView(APIView):
    """
    Best practices qo'llanilgan view
    """
    
    # Cache timeout constants
    CACHE_TIMEOUT_SHORT = 300      # 5 min - tez o'zgaradigan
    CACHE_TIMEOUT_MEDIUM = 900     # 15 min - o'rtacha
    CACHE_TIMEOUT_LONG = 3600      # 1 soat - sekin o'zgaradigan
    
    def get_cache_key(self, request):
        """Standart cache key yaratish"""
        path = request.path
        query_string = request.META.get('QUERY_STRING', '')
        user_id = getattr(request.user, 'id', 'anon')
        
        key_parts = [path, query_string, str(user_id)]
        key_string = ':'.join(key_parts)
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        
        return f'api:v1:{key_hash}'
    
    def get_cache_timeout(self, request):
        """Request turiga qarab timeout"""
        # Authenticated users - qisqa timeout
        if hasattr(request, 'user') and request.user.is_authenticated:
            return self.CACHE_TIMEOUT_SHORT
        
        # Public data - uzun timeout
        return self.CACHE_TIMEOUT_LONG
    
    def get(self, request):
        # Step 1: Cache key yaratish
        cache_key = self.get_cache_key(request)
        
        # Step 2: Cache'dan olish
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            print("  ✅ Cached response returned")
            return Response(cached_data)
        
        # Step 3: Ma'lumot olish
        print("  ❌ Generating fresh response...")
        time.sleep(0.1)
        data = {'results': BOOKS_DATA}
        
        # Step 4: Cache'ga saqlash
        timeout = self.get_cache_timeout(request)
        cache.set(cache_key, data, timeout=timeout)
        print(f"  💾 Cached for {timeout}s")
        
        return Response(data)

print("Best practices misoli tugallandi\n")

print("\n✅ View caching strategiyalari tugallandi!")
print("\nAsosiy xulosa:")
print("1. Decorator - oddiy view'lar uchun")
print("2. Manual caching - murakkab logic uchun")
print("3. Query params aware - filter'lar uchun")
print("4. User-specific - shaxsiy ma'lumotlar uchun")
print("5. Conditional - shart asosida")
print("6. ETag - client-side validation")
print("7. Invalidation - write operations'da")
print("8. Tiered - yuqori performance")
print("9. Monitoring - statistika va optimization")
print("10. Best practices - barcha yondashuvlar birga")