"""
QuerySet Caching - Django QuerySet'larni cache qilish
"""
from django.core.cache import cache
from django.db import models
import time
import hashlib
import json

# === DUMMY MODELS ===
class Author:
    def __init__(self, id, name, country):
        self.id = id
        self.name = name
        self.country = country
    
    def __repr__(self):
        return f"Author({self.id}, '{self.name}')"

class Book:
    def __init__(self, id, title, author_id, price, published_year):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.price = price
        self.published_year = published_year
    
    def __repr__(self):
        return f"Book({self.id}, '{self.title}')"

# Fake database
AUTHORS_DB = [
    Author(1, "William Vincent", "USA"),
    Author(2, "Daniel Roy Greenfeld", "USA"),
    Author(3, "John Smith", "UK"),
]

BOOKS_DB = [
    Book(1, "Django for Beginners", 1, 29.99, 2020),
    Book(2, "Django for APIs", 1, 34.99, 2021),
    Book(3, "Two Scoops of Django", 2, 49.99, 2019),
    Book(4, "Django REST Framework", 3, 39.99, 2022),
    Book(5, "Python Web Development", 3, 44.99, 2023),
]


# === 1. BASIC QUERYSET CACHING ===
print("=== 1. Basic QuerySet Caching ===\n")

def get_all_books_cached():
    """Barcha kitoblarni cache bilan olish"""
    cache_key = 'books:all'
    
    # Cache'dan olib ko'ramiz
    books = cache.get(cache_key)
    
    if books is not None:
        print("  ✅ CACHE HIT: Books from cache")
        return books
    
    # DB query (simulatsiya)
    print("  ❌ CACHE MISS: Loading from database...")
    time.sleep(0.1)  # DB query simulatsiyasi
    books = BOOKS_DB.copy()
    
    # Cache'ga saqlaymiz
    cache.set(cache_key, books, timeout=600)  # 10 daqiqa
    print(f"  💾 Cached {len(books)} books")
    
    return books

# Test
print("First call:")
books = get_all_books_cached()
print(f"Result: {len(books)} books\n")

print("Second call:")
books = get_all_books_cached()
print(f"Result: {len(books)} books\n")


# === 2. FILTERED QUERYSET CACHING ===
print("=== 2. Filtered QuerySet Caching ===\n")

def get_books_by_author_cached(author_id):
    """Muallif bo'yicha kitoblarni cache bilan olish"""
    cache_key = f'books:author:{author_id}'
    
    books = cache.get(cache_key)
    
    if books is not None:
        print(f"  ✅ CACHE HIT: Books by author {author_id}")
        return books
    
    print(f"  ❌ CACHE MISS: Filtering books by author {author_id}...")
    time.sleep(0.1)
    books = [book for book in BOOKS_DB if book.author_id == author_id]
    
    cache.set(cache_key, books, timeout=300)
    print(f"  💾 Cached {len(books)} books")
    
    return books

# Test
print("Get books by author 1:")
books = get_books_by_author_cached(1)
print(f"Found: {books}\n")

print("Get books by author 1 again:")
books = get_books_by_author_cached(1)
print(f"Found: {books}\n")


# === 3. COMPLEX QUERY CACHING ===
print("=== 3. Complex Query Caching ===\n")

def generate_cache_key_from_params(**kwargs):
    """Query parametrlaridan cache key yaratish"""
    # Parametrlarni tartiblab, hash qilamiz
    params_str = json.dumps(kwargs, sort_keys=True)
    params_hash = hashlib.md5(params_str.encode()).hexdigest()
    return f'books:query:{params_hash}'

def get_books_filtered_cached(min_price=None, max_price=None, year=None):
    """Murakkab filter bilan kitoblarni olish"""
    # Dinamik cache key
    cache_key = generate_cache_key_from_params(
        min_price=min_price,
        max_price=max_price,
        year=year
    )
    
    books = cache.get(cache_key)
    
    if books is not None:
        print(f"  ✅ CACHE HIT: {cache_key[:30]}...")
        return books
    
    print(f"  ❌ CACHE MISS: Complex filtering...")
    time.sleep(0.15)
    
    # Filter logic
    books = BOOKS_DB.copy()
    
    if min_price is not None:
        books = [b for b in books if b.price >= min_price]
    
    if max_price is not None:
        books = [b for b in books if b.price <= max_price]
    
    if year is not None:
        books = [b for b in books if b.published_year == year]
    
    cache.set(cache_key, books, timeout=300)
    print(f"  💾 Cached {len(books)} books")
    
    return books

# Test
print("Filter: price 30-45:")
books = get_books_filtered_cached(min_price=30, max_price=45)
print(f"Found: {len(books)} books\n")

print("Same filter again:")
books = get_books_filtered_cached(min_price=30, max_price=45)
print(f"Found: {len(books)} books\n")


# === 4. PREFETCH RELATED CACHING ===
print("=== 4. Prefetch Related Caching ===\n")

def get_books_with_authors_cached():
    """Kitoblarni mualliflari bilan birga cache qilish"""
    cache_key = 'books:with_authors'
    
    cached_data = cache.get(cache_key)
    
    if cached_data is not None:
        print("  ✅ CACHE HIT: Books with authors")
        return cached_data
    
    print("  ❌ CACHE MISS: Loading books with authors...")
    time.sleep(0.2)  # Join query simulatsiyasi
    
    # Books va Authors'ni birlashtirish
    result = []
    for book in BOOKS_DB:
        author = next((a for a in AUTHORS_DB if a.id == book.author_id), None)
        result.append({
            'book': book,
            'author': author
        })
    
    cache.set(cache_key, result, timeout=600)
    print(f"  💾 Cached {len(result)} books with authors")
    
    return result

# Test
print("First call:")
data = get_books_with_authors_cached()
print(f"Loaded: {len(data)} items\n")

print("Second call:")
data = get_books_with_authors_cached()
print(f"Loaded: {len(data)} items\n")


# === 5. PAGINATION CACHING ===
print("=== 5. Pagination Caching ===\n")

def get_books_page_cached(page=1, page_size=2):
    """Pagination bilan kitoblarni cache qilish"""
    cache_key = f'books:page:{page}:size:{page_size}'
    
    cached_page = cache.get(cache_key)
    
    if cached_page is not None:
        print(f"  ✅ CACHE HIT: Page {page}")
        return cached_page
    
    print(f"  ❌ CACHE MISS: Loading page {page}...")
    time.sleep(0.1)
    
    # Pagination logic
    start = (page - 1) * page_size
    end = start + page_size
    
    books_page = BOOKS_DB[start:end]
    total_count = len(BOOKS_DB)
    
    result = {
        'results': books_page,
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'total_pages': (total_count + page_size - 1) // page_size
    }
    
    cache.set(cache_key, result, timeout=300)
    print(f"  💾 Cached page {page}")
    
    return result

# Test
print("Page 1:")
page_data = get_books_page_cached(page=1, page_size=2)
print(f"Results: {len(page_data['results'])} books")
print(f"Total pages: {page_data['total_pages']}\n")

print("Page 1 again:")
page_data = get_books_page_cached(page=1, page_size=2)
print(f"Results: {len(page_data['results'])} books\n")


# === 6. AGGREGATION CACHING ===
print("=== 6. Aggregation Caching ===\n")

def get_books_statistics_cached():
    """Aggregatsiya natijalarini cache qilish"""
    cache_key = 'books:statistics'
    
    stats = cache.get(cache_key)
    
    if stats is not None:
        print("  ✅ CACHE HIT: Statistics")
        return stats
    
    print("  ❌ CACHE MISS: Calculating statistics...")
    time.sleep(0.15)
    
    # Aggregation
    total_books = len(BOOKS_DB)
    avg_price = sum(b.price for b in BOOKS_DB) / total_books
    min_price = min(b.price for b in BOOKS_DB)
    max_price = max(b.price for b in BOOKS_DB)
    
    stats = {
        'total_books': total_books,
        'average_price': round(avg_price, 2),
        'min_price': min_price,
        'max_price': max_price,
        'price_range': max_price - min_price
    }
    
    cache.set(cache_key, stats, timeout=900)  # 15 daqiqa
    print("  💾 Cached statistics")
    
    return stats

# Test
print("First call:")
stats = get_books_statistics_cached()
print(f"Stats: {stats}\n")

print("Second call:")
stats = get_books_statistics_cached()
print(f"Stats: {stats}\n")


# === 7. CUSTOM MANAGER WITH CACHING ===
print("=== 7. Custom Manager with Caching ===\n")

class CachedBookManager:
    """Custom manager cache bilan"""
    
    @staticmethod
    def all_cached():
        """Barcha kitoblar (cached)"""
        return get_all_books_cached()
    
    @staticmethod
    def filter_by_author_cached(author_id):
        """Muallif bo'yicha filter (cached)"""
        return get_books_by_author_cached(author_id)
    
    @staticmethod
    def get_cached(book_id):
        """ID bo'yicha kitob (cached)"""
        cache_key = f'book:{book_id}'
        
        book = cache.get(cache_key)
        
        if book is not None:
            print(f"  ✅ CACHE HIT: Book {book_id}")
            return book
        
        print(f"  ❌ CACHE MISS: Loading book {book_id}...")
        book = next((b for b in BOOKS_DB if b.id == book_id), None)
        
        if book:
            cache.set(cache_key, book, timeout=300)
            print(f"  💾 Cached book {book_id}")
        
        return book
    
    @staticmethod
    def invalidate_all():
        """Barcha book cache'larini tozalash"""
        print("  🗑️ Invalidating all book caches...")
        cache.delete_pattern('books:*')
        cache.delete_pattern('book:*')

# Test
print("Using Custom Manager:")
books = CachedBookManager.all_cached()
print(f"All books: {len(books)}\n")

book = CachedBookManager.get_cached(1)
print(f"Single book: {book}\n")


# === 8. CACHE WARMING FOR QUERYSET ===
print("=== 8. Cache Warming for QuerySet ===\n")

def warm_books_cache():
    """Dastur ishga tushganda cache'ni to'ldirish"""
    print("  🔥 Warming books cache...")
    
    # All books
    cache.set('books:all', BOOKS_DB.copy(), timeout=3600)
    
    # Books by author
    for author in AUTHORS_DB:
        author_books = [b for b in BOOKS_DB if b.author_id == author.id]
        cache.set(f'books:author:{author.id}', author_books, timeout=3600)
    
    # Individual books
    for book in BOOKS_DB:
        cache.set(f'book:{book.id}', book, timeout=3600)
    
    # Statistics
    stats = get_books_statistics_cached()
    
    print("  ✅ Cache warming completed")
    return True

# Test
warm_books_cache()


# === 9. QUERYSET CACHE INVALIDATION ===
print("\n=== 9. QuerySet Cache Invalidation ===\n")

def invalidate_book_caches(book_id):
    """Kitob o'zgarganda tegishli cache'larni tozalash"""
    print(f"  🗑️ Invalidating caches for book {book_id}...")
    
    # Single book cache
    cache.delete(f'book:{book_id}')
    
    # All books cache
    cache.delete('books:all')
    
    # Books with authors cache
    cache.delete('books:with_authors')
    
    # Statistics cache
    cache.delete('books:statistics')
    
    # Author's books cache (agar kerak bo'lsa)
    book = next((b for b in BOOKS_DB if b.id == book_id), None)
    if book:
        cache.delete(f'books:author:{book.author_id}')
    
    print("  ✅ Caches invalidated")

# Test
invalidate_book_caches(1)


print("\n✅ QuerySet caching strategiyalari tugallandi!")