"""
Lesson 24: Caching Views (OPTIMIZED VERSION)
Sizning mavjud Book modeliga moslashtirilgan
"""
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Avg

import hashlib
import json
import time

from books.models import Book, Author
from books.serializers import BookSerializer


# ==========================================
# 1. OPTIMIZED MANUAL CACHING - BookListAPIView
# ==========================================
class CachedBookListAPIView(generics.ListAPIView):
    """
    Barcha kitoblar ro'yxati - Manual caching + Query Optimization
    """
    serializer_class = BookSerializer
    
    def get_queryset(self):
        """
        OPTIMIZED QUERYSET:
        Faqat mavjud fieldlar bilan ishlash
        """
        return Book.objects.select_related(
            'author',
        ).prefetch_related(
            'genres'
        )
    
    def get_cache_key(self, request):
        """Query params'dan unique cache key yasash"""
        query_params = dict(request.GET.items())
        params_str = json.dumps(query_params, sort_keys=True)
        params_hash = hashlib.md5(params_str.encode()).hexdigest()
        return f'books:list:optimized:{params_hash}'
    
    def list(self, request, *args, **kwargs):
        # Cache key yaratish
        cache_key = self.get_cache_key(request)
        
        # Cache'dan olishga urinish
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response({
                'cached': True,
                'count': len(cached_data),
                'results': cached_data
            })
        
        # Cache miss - OPTIMIZED QUERY
        queryset = self.filter_queryset(self.get_queryset())
        
        # Count qilish
        count = queryset.count()
        
        # Serialize qilish
        serializer = self.get_serializer(queryset, many=True)
        
        # Cache'ga saqlash (5 daqiqa)
        cache.set(cache_key, serializer.data, timeout=300)
        
        return Response({
            'cached': False,
            'count': count,
            'results': serializer.data
        })


# ==========================================
# 2. OPTIMIZED DECORATOR CACHING - BookDetailAPIView
# ==========================================
@method_decorator(cache_page(60 * 5), name='dispatch')  # 5 daqiqa
class CachedBookDetailAPIView(generics.RetrieveAPIView):
    """
    Bitta kitob detali - Decorator caching + Optimized Query
    """
    serializer_class = BookSerializer
    
    def get_queryset(self):
        """OPTIMIZED: select_related"""
        return Book.objects.select_related('author')


# ==========================================
# 3. OPTIMIZED SEARCH WITH CACHING
# ==========================================
class BookSearchAPIView(APIView):
    """
    Kitoblarni qidirish - Optimized search query + cache
    """
    
    def get(self, request):
        search_query = request.GET.get('q', '').strip()
        
        if not search_query:
            return Response(
                {'error': 'Search query is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Search query'dan cache key
        query_hash = hashlib.md5(search_query.encode()).hexdigest()
        cache_key = f'books:search:optimized:{query_hash}'
        
        # Cache'dan olish
        cached_results = cache.get(cache_key)
        if cached_results is not None:
            return Response({
                'cached': True,
                'query': search_query,
                'count': len(cached_results),
                'results': cached_results
            })
        
        # OPTIMIZED SEARCH QUERY
        from django.db.models import Q
        books = Book.objects.select_related('author').filter(
            Q(title__icontains=search_query) |
            Q(author__name__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )[:50]  # Limit results
        
        serializer = BookSerializer(books, many=True)
        
        # Cache'ga saqlash (10 daqiqa)
        cache.set(cache_key, serializer.data, timeout=600)
        
        return Response({
            'cached': False,
            'query': search_query,
            'count': books.count(),
            'results': serializer.data
        })


# ==========================================
# 4. OPTIMIZED STATISTICS WITH CACHING
# ==========================================
class BookStatisticsAPIView(APIView):
    """
    Kitoblar statistikasi - Optimized aggregation + cache
    """
    
    def get(self, request):
        cache_key = 'books:statistics:optimized'
        
        # Cache'dan olish
        stats = cache.get(cache_key)
        
        if stats is not None:
            return Response({
                'cached': True,
                'data': stats
            })
        
        # OPTIMIZED STATISTICS QUERIES
        book_stats = Book.objects.aggregate(
            total_books=Count('id'),
            average_price=Avg('price') if hasattr(Book, 'price') else None,
        )
        
        total_authors = Author.objects.count()
        
        # Books by author (Top 10)
        books_by_author = list(
            Book.objects.values('author__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        
        stats = {
            'total_books': book_stats['total_books'],
            'total_authors': total_authors,
            'books_by_author': books_by_author,
        }
        
        # Agar price field'i bor bo'lsa
        if hasattr(Book, 'price') and book_stats.get('average_price'):
            stats['average_price'] = float(book_stats['average_price'])
        
        # Cache'ga saqlash (15 daqiqa)
        cache.set(cache_key, stats, timeout=900)
        
        return Response({
            'cached': False,
            'data': stats
        })


# ==========================================
# 5. OPTIMIZED PAGINATION WITH CACHING
# ==========================================
class PaginatedBookListAPIView(APIView):
    """
    Pagination bilan kitoblar - Optimized + har bir page alohida cache
    """
    
    def get(self, request):
        from django.core.paginator import Paginator
        
        # Pagination parametrlari
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # Limit page_size (DoS prevention)
        page_size = min(page_size, 100)
        
        # Cache key
        cache_key = f'books:page:optimized:{page}:size:{page_size}'
        
        # Cache'dan olish
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response({
                'cached': True,
                **cached_data
            })
        
        # OPTIMIZED QUERYSET
        books = Book.objects.select_related('author').all()
        
        # Pagination
        paginator = Paginator(books, page_size)
        page_obj = paginator.get_page(page)
        
        serializer = BookSerializer(page_obj, many=True)
        
        data = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': page,
            'page_size': page_size,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'results': serializer.data,
        }
        
        # Cache'ga saqlash (5 daqiqa)
        cache.set(cache_key, data, timeout=300)
        
        return Response({
            'cached': False,
            **data
        })


# ==========================================
# 6-8. CACHE INVALIDATION ON CREATE/UPDATE/DELETE
# ==========================================
class BookCreateAPIView(generics.CreateAPIView):
    """Yangi kitob yaratish - Avtomatik cache invalidation"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def perform_create(self, serializer):
        book = serializer.save()
        self.invalidate_related_caches(book)
        return book
    
    def invalidate_related_caches(self, book):
        """Tegishli cache'larni tozalash"""
        try:
            from django_redis import get_redis_connection
            redis_conn = get_redis_connection("default")
            
            patterns = ['books:list:optimized:*', 'books:page:optimized:*']
            for pattern in patterns:
                keys = redis_conn.keys(pattern)
                if keys:
                    redis_conn.delete(*keys)
            
            cache.delete('books:statistics:optimized')
        except:
            cache.clear()


class BookUpdateAPIView(generics.UpdateAPIView):
    """Kitobni yangilash - Cache invalidation"""
    serializer_class = BookSerializer
    
    def get_queryset(self):
        return Book.objects.select_related('author')
    
    def perform_update(self, serializer):
        book = serializer.save()
        cache.delete(f'book:optimized:{book.id}')
        self.invalidate_caches()
        return book
    
    def invalidate_caches(self):
        try:
            from django_redis import get_redis_connection
            redis_conn = get_redis_connection("default")
            
            patterns = ['books:list:optimized:*', 'books:page:optimized:*']
            for pattern in patterns:
                keys = redis_conn.keys(pattern)
                if keys:
                    redis_conn.delete(*keys)
            
            cache.delete('books:statistics:optimized')
        except:
            cache.clear()


class BookDeleteAPIView(generics.DestroyAPIView):
    """Kitobni o'chirish - Cache invalidation"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def perform_destroy(self, instance):
        book_id = instance.id
        instance.delete()
        
        cache.delete(f'book:optimized:{book_id}')
        
        try:
            from django_redis import get_redis_connection
            redis_conn = get_redis_connection("default")
            
            patterns = ['books:list:optimized:*', 'books:page:optimized:*']
            for pattern in patterns:
                keys = redis_conn.keys(pattern)
                if keys:
                    redis_conn.delete(*keys)
        except:
            pass


# ==========================================
# 9-11. MONITORING & MANAGEMENT
# ==========================================
class CacheStatsAPIView(APIView):
    """Cache statistikasini ko'rsatish"""
    
    def get(self, request):
        from django_redis import get_redis_connection
        
        try:
            redis_conn = get_redis_connection("default")
            info = redis_conn.info()
            all_keys = redis_conn.keys('*')
            
            stats = {
                'redis_version': info.get('redis_version'),
                'used_memory': info.get('used_memory_human'),
                'connected_clients': info.get('connected_clients'),
                'total_keys': len(all_keys),
                'uptime_days': info.get('uptime_in_days'),
            }
            
            # Group keys by prefix
            key_groups = {}
            for key in all_keys:
                key_str = key.decode('utf-8')
                prefix = key_str.split(':')[0] if ':' in key_str else 'other'
                key_groups[prefix] = key_groups.get(prefix, 0) + 1
            
            stats['keys_by_prefix'] = key_groups
            
            return Response(stats)
            
        except Exception as e:
            return Response(
                {'error': f'Redis error: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CacheClearAPIView(APIView):
    """Cache'ni tozalash"""
    
    def post(self, request):
        cache_type = request.data.get('type', 'all')
        
        try:
            from django_redis import get_redis_connection
            redis_conn = get_redis_connection("default")
            
            if cache_type == 'all':
                cache.clear()
                message = 'All cache cleared successfully'
            
            elif cache_type == 'books':
                patterns = ['books:*', 'book:*']
                for pattern in patterns:
                    keys = redis_conn.keys(pattern)
                    if keys:
                        redis_conn.delete(*keys)
                message = 'Books cache cleared successfully'
            
            elif cache_type == 'statistics':
                cache.delete('books:statistics:optimized')
                message = 'Statistics cache cleared successfully'
            
            else:
                return Response(
                    {'error': 'Invalid cache type'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response({
                'success': True,
                'message': message
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class ConditionalCachedBookListAPIView(APIView):
    """Shartli cache"""
    
    def should_cache(self, request):
        if request.method != 'GET':
            return False
        if hasattr(request, 'user') and request.user.is_authenticated:
            return False
        return True
    
    def get(self, request):
        queryset = Book.objects.select_related('author').all()
        
        if not self.should_cache(request):
            serializer = BookSerializer(queryset, many=True)
            return Response({
                'cached': False,
                'reason': 'Caching disabled for authenticated users',
                'count': queryset.count(),
                'results': serializer.data
            })
        
        cache_key = 'books:public:list:optimized'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response({
                'cached': True,
                'count': len(cached_data),
                'results': cached_data
            })
        
        serializer = BookSerializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=600)
        
        return Response({
            'cached': False,
            'count': queryset.count(),
            'results': serializer.data
        })