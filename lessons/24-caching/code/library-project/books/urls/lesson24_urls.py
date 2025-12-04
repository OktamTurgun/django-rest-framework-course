"""
Lesson 24: Caching URLs
Cache'langan view'lar uchun URL routing
"""
from django.urls import path
from books.views.lesson24_views import (
    CachedBookListAPIView,
    CachedBookDetailAPIView,
    BookSearchAPIView,
    BookStatisticsAPIView,
    PaginatedBookListAPIView,
    BookCreateAPIView,
    BookUpdateAPIView,
    BookDeleteAPIView,
    CacheStatsAPIView,
    CacheClearAPIView,
    ConditionalCachedBookListAPIView,
)

app_name = 'lesson24'

urlpatterns = [
    # 1. Cached Book List (Manual Caching)
    path('books/', 
         CachedBookListAPIView.as_view(), 
         name='cached-book-list'),
    
    # 2. Cached Book Detail (Decorator Caching)
    path('books/<int:pk>/', 
         CachedBookDetailAPIView.as_view(), 
         name='cached-book-detail'),
    
    # 3. Book Search (Search Query Caching)
    path('books/search/', 
         BookSearchAPIView.as_view(), 
         name='book-search'),
    
    # 4. Book Statistics (Aggregation Caching)
    path('books/statistics/', 
         BookStatisticsAPIView.as_view(), 
         name='book-statistics'),
    
    # 5. Paginated Book List (Pagination Caching)
    path('books/paginated/', 
         PaginatedBookListAPIView.as_view(), 
         name='paginated-book-list'),
    
    # 6. Book Create (with Cache Invalidation)
    path('books/create/', 
         BookCreateAPIView.as_view(), 
         name='book-create'),
    
    # 7. Book Update (with Cache Invalidation)
    path('books/<int:pk>/update/', 
         BookUpdateAPIView.as_view(), 
         name='book-update'),
    
    # 8. Book Delete (with Cache Invalidation)
    path('books/<int:pk>/delete/', 
         BookDeleteAPIView.as_view(), 
         name='book-delete'),
    
    # 9. Conditional Caching
    path('books/public/', 
         ConditionalCachedBookListAPIView.as_view(), 
         name='public-book-list'),
    
    # === CACHE MANAGEMENT ENDPOINTS ===
    
    # 10. Cache Statistics
    path('cache/stats/', 
         CacheStatsAPIView.as_view(), 
         name='cache-stats'),
    
    # 11. Cache Clear
    path('cache/clear/', 
         CacheClearAPIView.as_view(), 
         name='cache-clear'),
]