# Homework 24: Caching in Django REST Framework

##  Umumiy Talablar

Library Management tizimiga caching mexanizmlarini qo'shing va performance'ni yaxshilang.

---

##  Vazifa 1: Redis Sozlash (10 ball)

### Topshiriq:
1. Redis'ni o'rnating va ishga tushiring
2. `django-redis` paketini o'rnating
3. `settings.py`'da Redis cache'ni sozlang
4. Cache connection'ni test qiling

### Kutilayotgan Natija:
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'library',
        'TIMEOUT': 300,
    }
}
```

### Test:
```python
from django.core.cache import cache

cache.set('test_key', 'Hello Redis!')
assert cache.get('test_key') == 'Hello Redis!'
print("✅ Redis ishlayapti")
```

---

##  Vazifa 2: Model Cache (15 ball)

### Topshiriq:
Book modeliga cache qo'shing:
1. `get_cached()` - bitta kitobni cache bilan olish
2. `get_all_cached()` - barcha kitoblarni cache qilish
3. Signal'lar orqali automatic cache invalidation

### Kutilayotgan Kod:
```python
# books/models.py
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete

class Book(models.Model):
    # ... mavjud fieldlar ...
    
    @classmethod
    def get_cached(cls, book_id):
        cache_key = f'book:{book_id}'
        book = cache.get(cache_key)
        
        if book is None:
            book = cls.objects.select_related('author', 'category').get(id=book_id)
            cache.set(cache_key, book, timeout=300)
        
        return book
    
    @classmethod
    def get_all_cached(cls):
        cache_key = 'books:all'
        books = cache.get(cache_key)
        
        if books is None:
            books = list(cls.objects.select_related('author', 'category').all())
            cache.set(cache_key, books, timeout=600)
        
        return books

# Signal handlers
@receiver(post_save, sender=Book)
def invalidate_book_cache_on_save(sender, instance, **kwargs):
    cache.delete(f'book:{instance.id}')
    cache.delete('books:all')

@receiver(post_delete, sender=Book)
def invalidate_book_cache_on_delete(sender, instance, **kwargs):
    cache.delete(f'book:{instance.id}')
    cache.delete('books:all')
```

### Test:
```bash
python manage.py shell

>>> from books.models import Book
>>> book = Book.get_cached(1)  # DB'dan
>>> book = Book.get_cached(1)  # Cache'dan
```

---

##  Vazifa 3: View Caching (20 ball)

### Topshiriq:
API view'lariga caching qo'shing:

#### a) BookListView - Manual Caching
```python
class BookListView(APIView):
    def get(self, request):
        # Query params'dan cache key yasash
        cache_key = self.get_cache_key(request)
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # Filter, pagination
        queryset = self.get_queryset()
        serializer = BookSerializer(queryset, many=True)
        data = serializer.data
        
        cache.set(cache_key, data, timeout=300)
        return Response(data)
```

#### b) BookDetailView - Decorator Caching
```python
@method_decorator(cache_page(60 * 5), name='dispatch')
class BookDetailView(APIView):
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
```

#### c) BookStatisticsView - Aggregation Caching
```python
class BookStatisticsView(APIView):
    def get(self, request):
        cache_key = 'books:statistics'
        stats = cache.get(cache_key)
        
        if stats is None:
            stats = {
                'total_books': Book.objects.count(),
                'total_authors': Author.objects.count(),
                'avg_price': Book.objects.aggregate(Avg('price'))['price__avg'],
                'books_by_category': Book.objects.values('category__name').annotate(count=Count('id'))
            }
            cache.set(cache_key, stats, timeout=900)  # 15 min
        
        return Response(stats)
```

### Test:
```bash
# Birinchi request - cache miss
curl http://localhost:8000/api/books/

# Ikkinchi request - cache hit (tez)
curl http://localhost:8000/api/books/
```

---

##  Vazifa 4: Cache Invalidation (15 ball)

### Topshiriq:
Write operations'da cache'ni to'g'ri tozalang:

```python
class BookCreateView(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            
            # Cache invalidation
            self.invalidate_caches()
            
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def invalidate_caches(self):
        # List cache
        cache.delete('books:all')
        
        # Filtered cache
        cache.delete_pattern('books:filtered:*')
        
        # Statistics cache
        cache.delete('books:statistics')
        
        # Related caches
        cache.delete('authors:with_books')
```

### Qo'shimcha Vazifa:
UPDATE va DELETE operations uchun ham invalidation qo'shing.

---

##  Vazifa 5: Cache Strategies (20 ball)

### Topshiriq:
Turli cache strategiyalarini implement qiling:

#### a) Search Query Caching
```python
class BookSearchView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        
        # Search query'dan cache key
        cache_key = f'search:{hashlib.md5(query.encode()).hexdigest()}'
        
        results = cache.get(cache_key)
        if results is None:
            results = Book.objects.filter(
                Q(title__icontains=query) | 
                Q(author__name__icontains=query)
            )
            serializer = BookSerializer(results, many=True)
            results = serializer.data
            
            cache.set(cache_key, results, timeout=600)
        
        return Response(results)
```

#### b) User-Specific Caching
```python
class UserBorrowHistoryView(APIView):
    def get(self, request):
        cache_key = f'user:{request.user.id}:borrows'
        
        history = cache.get(cache_key)
        if history is None:
            borrows = BorrowRecord.objects.filter(
                user=request.user
            ).select_related('book')
            
            serializer = BorrowRecordSerializer(borrows, many=True)
            history = serializer.data
            
            cache.set(cache_key, history, timeout=300)
        
        return Response(history)
```

#### c) Pagination Caching
```python
class PaginatedBookListView(APIView):
    def get(self, request):
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        
        cache_key = f'books:page:{page}:size:{page_size}'
        
        data = cache.get(cache_key)
        if data is None:
            # Pagination logic
            paginator = Paginator(Book.objects.all(), page_size)
            page_obj = paginator.get_page(page)
            
            serializer = BookSerializer(page_obj, many=True)
            data = {
                'results': serializer.data,
                'count': paginator.count,
                'total_pages': paginator.num_pages
            }
            
            cache.set(cache_key, data, timeout=300)
        
        return Response(data)
```

---

##  Vazifa 6: Cache Monitoring (10 ball)

### Topshiriq:
Cache monitoring system yarating:

```python
# monitoring/middleware.py
class CacheMonitoringMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Request oldidan
        start_time = time.time()
        
        response = self.get_response(request)
        
        # Response keyin
        duration = time.time() - start_time
        
        # Cache stats
        if hasattr(response, 'cache_hit'):
            cache.incr('cache:stats:hits')
        else:
            cache.incr('cache:stats:misses')
        
        # Response time tracking
        cache.lpush('cache:response_times', duration)
        cache.ltrim('cache:response_times', 0, 99)  # Last 100
        
        return response

# Cache stats endpoint
class CacheStatsView(APIView):
    def get(self, request):
        hits = cache.get('cache:stats:hits', 0)
        misses = cache.get('cache:stats:misses', 0)
        total = hits + misses
        hit_rate = (hits / total * 100) if total > 0 else 0
        
        response_times = cache.lrange('cache:response_times', 0, -1)
        avg_response = sum(response_times) / len(response_times) if response_times else 0
        
        return Response({
            'cache_hits': hits,
            'cache_misses': misses,
            'hit_rate': f'{hit_rate:.2f}%',
            'avg_response_time': f'{avg_response:.3f}s'
        })
```

---

##  Vazifa 7: Cache Management Commands (10 ball)

### Topshiriq:
Management commands yarating:

```python
# books/management/commands/cache_stats.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Show cache statistics'
    
    def handle(self, *args, **options):
        from django_redis import get_redis_connection
        con = get_redis_connection("default")
        
        info = con.info()
        
        self.stdout.write(f"Redis Version: {info['redis_version']}")
        self.stdout.write(f"Used Memory: {info['used_memory_human']}")
        self.stdout.write(f"Total Keys: {con.dbsize()}")
        self.stdout.write(f"Connected Clients: {info['connected_clients']}")

# books/management/commands/warm_cache.py
class Command(BaseCommand):
    help = 'Warm up cache with frequently accessed data'
    
    def handle(self, *args, **options):
        # Books cache
        books = Book.objects.all()
        cache.set('books:all', list(books), timeout=3600)
        
        # Statistics
        stats = {
            'total_books': books.count(),
            # ...
        }
        cache.set('books:statistics', stats, timeout=3600)
        
        self.stdout.write(self.style.SUCCESS('Cache warmed successfully!'))

# books/management/commands/clear_cache.py
class Command(BaseCommand):
    help = 'Clear all cache'
    
    def handle(self, *args, **options):
        cache.clear()
        self.stdout.write(self.style.SUCCESS('Cache cleared!'))
```

### Test:
```bash
python manage.py cache_stats
python manage.py warm_cache
python manage.py clear_cache
```

---

##  Testing (Bonus +10 ball)

### Topshiriq:
Cache functionality uchun testlar yozing:

```python
# books/tests/test_caching.py
from django.test import TestCase
from django.core.cache import cache

class BookCachingTestCase(TestCase):
    def setUp(self):
        cache.clear()
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            isbn='1234567890'
        )
    
    def tearDown(self):
        cache.clear()
    
    def test_book_get_cached(self):
        # First call - cache miss
        book1 = Book.get_cached(self.book.id)
        
        # Second call - cache hit
        book2 = Book.get_cached(self.book.id)
        
        self.assertEqual(book1.id, book2.id)
    
    def test_cache_invalidation_on_update(self):
        cache_key = f'book:{self.book.id}'
        
        # Cache'ga qo'yamiz
        cache.set(cache_key, self.book)
        
        # Update qilamiz
        self.book.title = 'Updated Title'
        self.book.save()
        
        # Cache tozalanganmi?
        self.assertIsNone(cache.get(cache_key))
    
    def test_list_view_caching(self):
        response1 = self.client.get('/api/books/')
        response2 = self.client.get('/api/books/')
        
        # Ikkinchisi tezroq bo'lishi kerak
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
```

---

##  Baholash Mezonlari

| Vazifa | Ballar | Tavsif |
|--------|--------|--------|
| Redis sozlash | 10 | Redis o'rnatish va konfiguratsiya |
| Model cache | 15 | Model-level caching |
| View caching | 20 | API view'larni cache qilish |
| Cache invalidation | 15 | Write operations'da invalidation |
| Cache strategies | 20 | Turli strategiyalar |
| Monitoring | 10 | Cache monitoring system |
| Management commands | 10 | CLI commands |
| **Jami** | **100** | |
| Bonus (Testing) | +10 | Cache testlari |

---

##  Qo'shimcha Topshiriqlar (Ixtiyoriy)

### 1. Multi-Tier Caching
Local memory + Redis cache implement qiling

### 2. Cache Warming Script
Dastur ishga tushganda avtomatik cache warming

### 3. Cache Analytics Dashboard
Cache performance'ni ko'rsatuvchi dashboard

### 4. Distributed Cache Invalidation
Multiple server'larda cache invalidation

---

##  Topshirish

1. Barcha o'zgarishlarni commit qiling
2. GitHub'ga push qiling
3. Pull Request yarating
4. PR description'da quyidagilarni yozing:
   - Qaysi vazifalar bajarildi
   - Cache hit rate (agar monitoring qo'shgan bo'lsangiz)
   - Performance improvement (response time)
   - Screenshot'lar (agar monitoring dashboard qo'shgan bo'lsangiz)

---

## Deadline

**3 kun** (72 soat)

**Omad!**