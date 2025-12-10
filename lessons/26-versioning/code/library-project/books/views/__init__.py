"""
Books app views
Import barcha viewlarni bu yerda qilamiz
"""

# Book views
from .book_views import BookListCreateView, BookDetailView, BookFeedView

# Author views
from .author_views import (
    AuthorListView,
    AuthorDetailView,
    AuthorCreateView,
    AuthorUpdateView,
    AuthorDeleteView
)

# Genre views
from .genre_views import GenreListCreateView, GenreDetailView

# Lesson 24 - Caching views (YANGI!)
from .lesson24_views import (
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

__all__ = [
    # Book views
    'BookListCreateView',
    'BookDetailView',
    'BookFeedView',
    
    # Author views
    'AuthorListView',
    'AuthorDetailView',
    'AuthorCreateView',
    'AuthorUpdateView',
    'AuthorDeleteView',
    
    # Genre views
    'GenreListCreateView',
    'GenreDetailView',
    
    # Lesson 24 - Caching views
    'CachedBookListAPIView',
    'CachedBookDetailAPIView',
    'BookSearchAPIView',
    'BookStatisticsAPIView',
    'PaginatedBookListAPIView',
    'BookCreateAPIView',
    'BookUpdateAPIView',
    'BookDeleteAPIView',
    'CacheStatsAPIView',
    'CacheClearAPIView',
    'ConditionalCachedBookListAPIView',
]