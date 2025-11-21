"""
Books app views
Import barcha viewlarni bu yerda qilamiz
"""

# Book views
from .book_views import BookListCreateView, BookDetailView

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