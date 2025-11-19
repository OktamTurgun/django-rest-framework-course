"""
Books app views
Import barcha viewlarni bu yerda qilamiz
"""

# Lesson 17 views
from .book_views import BookListCreateView, BookDetailView
from .author_views import (
    AuthorListView,
    AuthorDetailView,
    AuthorCreateView,
    AuthorUpdateView,
    AuthorDeleteView
)
from .genre_views import GenreListCreateView, GenreDetailView

# Old views (agar kerak bo'lsa)
# from .old_views import OldBookListView, OldBookDetailView

# ViewSet views (agar kerak bo'lsa)
# from .viewset_views import BookViewSet

__all__ = [
    # Book views
    'BookListCreateView',
    'BookDetailView',
    
    # Author views
    'AuthorListView',
    'AuthorDetailView',
    'AuthorCreateView',
    'AuthorUpdateView',
    'AuthorDeleteView',
    
    # Genre views
    'GenreListCreateView',
    'GenreDetailView',
]