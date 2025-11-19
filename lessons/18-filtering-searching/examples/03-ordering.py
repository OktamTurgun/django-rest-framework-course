"""
OrderingFilter Example

DRF'ning OrderingFilter'i bilan tartiblash.
Single va multiple ordering.
"""

from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from books.serializers import BookSerializer, AuthorSerializer, BookListSerializer
from books.models import Book, Author


# ==================== 1. BASIC ORDERING ====================

class BookOrderingView(generics.ListAPIView):
    """
    Basic ordering
    
    Examples:
    /api/books/?ordering=price            # Narx bo'yicha o'sish (arzon -> qimmat)
    /api/books/?ordering=-price           # Narx bo'yicha kamayish (qimmat -> arzon)
    /api/books/?ordering=title            # Nom bo'yicha A-Z
    /api/books/?ordering=-title           # Nom bo'yicha Z-A
    """
    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [OrderingFilter]
    ordering_fields = ['price', 'title', 'published_date']
    ordering = ['title']  # Default ordering


"""
Ordering qanday ishlaydi?

1. ordering_fields - qaysi fieldlar bo'yicha tartiblash mumkin
2. ordering - default ordering (URL'da param bo'lmasa)
3. URL param: ordering=field_name

Ascending (o'sish):   ordering=price
Descending (kamayish): ordering=-price
"""


# ==================== 2. MULTIPLE ORDERING ====================

class BookMultipleOrderingView(generics.ListAPIView):
    """
    Multiple ordering - bir nechta field bo'yicha
    
    Examples:
    /api/books/?ordering=-published_date,price    # Avval sana, keyin narx
    /api/books/?ordering=author__name,title       # Avval muallif, keyin nom
    /api/books/?ordering=-price,title             # Avval narx kamayish, keyin nom o'sish
    """
    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [OrderingFilter]
    ordering_fields = ['price', 'title', 'published_date', 'pages', 'author__name']
    ordering = ['-published_date', 'title']  # Default: yangilaridan, keyin nom


# ==================== 3. RELATED FIELD ORDERING ====================

class BookRelatedOrderingView(generics.ListAPIView):
    """
    Related field bo'yicha tartiblash
    
    ForeignKey: author__name, author__birth_date
    
    Examples:
    /api/books/?ordering=author__name          # Author nomi bo'yicha A-Z
    /api/books/?ordering=-author__birth_date   # Author yoshi bo'yicha
    """
    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [OrderingFilter]
    ordering_fields = [
        'title',
        'price',
        'published_date',
        'author__name',
        'author__birth_date'
    ]


# ==================== 4. ALL FIELDS ORDERING ====================

class BookAllFieldsOrderingView(generics.ListAPIView):
    """
    Barcha fieldlar bo'yicha tartiblash
    
    ordering_fields = '__all__' - barcha fieldlar
    
    Examples:
    /api/books/?ordering=isbn_number
    /api/books/?ordering=language
    /api/books/?ordering=publisher
    """
    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [OrderingFilter]
    ordering_fields = '__all__'  # Barcha model fieldlari
    ordering = ['-created_at']


# ==================== 5. CUSTOM ORDERING ====================

from rest_framework.filters import OrderingFilter as BaseOrderingFilter

class CustomOrderingFilter(BaseOrderingFilter):
    """
    Custom ordering filter
    
    ordering_param - parameter nomini o'zgartirish
    """
    ordering_param = 'sort'  # Default: 'ordering' -> 'sort' ga o'zgartirdik


class BookCustomOrderingView(generics.ListAPIView):
    """
    Custom ordering parameter
    
    Examples:
    /api/books/?sort=price        # 'ordering' o'rniga 'sort'
    /api/books/?sort=-price
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [CustomOrderingFilter]
    ordering_fields = ['price', 'title']


# ==================== 6. CASE-INSENSITIVE ORDERING ====================

from django.db.models.functions import Lower

class BookCaseInsensitiveOrderingView(generics.ListAPIView):
    """
    Case-insensitive ordering (title uchun)
    
    Examples:
    /api/books/?ordering=title_lower    # A-Z (case-insensitive)
    """
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [OrderingFilter]
    ordering_fields = ['title_lower', 'price']
    
    def get_queryset(self):
        return Book.objects.annotate(
            title_lower=Lower('title')
        ).select_related('author')


# ==================== 7. COMPUTED FIELD ORDERING ====================

from django.db.models import Count, Avg

class AuthorOrderingView(generics.ListAPIView):
    """
    Computed field bo'yicha tartiblash
    
    Examples:
    /api/authors/?ordering=-book_count      # Kitoblar soni bo'yicha
    /api/authors/?ordering=avg_price        # O'rtacha narx bo'yicha
    """
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [OrderingFilter]
    ordering_fields = ['name', 'book_count', 'avg_price']
    ordering = ['-book_count']
    
    def get_queryset(self):
        return Author.objects.annotate(
            book_count=Count('books'),
            avg_price=Avg('books__price')
        )


# ==================== 8. COMBINING WITH SEARCH ====================

from rest_framework.filters import SearchFilter

class BookSearchAndOrderingView(generics.ListAPIView):
    """
    Search va Ordering birga
    
    Examples:
    /api/books/?search=django&ordering=price
    /api/books/?search=python&ordering=-published_date
    """
    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'subtitle', 'author__name']
    ordering_fields = ['price', 'published_date', 'title']
    ordering = ['-published_date']


# ==================== 9. PERFORMANCE OPTIMIZED ====================

class BookOptimizedOrderingView(generics.ListAPIView):
    """
    Performance optimized ordering
    
    - select_related() - ForeignKey uchun
    - Index qo'shilgan fieldlar bo'yicha ordering
    """
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [OrderingFilter]
    ordering_fields = [
        'price',            # Index bor
        'published_date',   # Index bor
        'title'             # Index bor
    ]
    ordering = ['-published_date']
    
    def get_queryset(self):
        return Book.objects.select_related('author').only(
            'id', 'title', 'price', 'published_date',
            'author__id', 'author__name'
        )


# ==================== REAL WORLD EXAMPLE ====================

class BookAdvancedView(generics.ListAPIView):
    """
    Advanced view - Search + Ordering + Filtering
    
    Examples:
    /api/books/advanced/?search=django&ordering=-price&published=true
    /api/books/advanced/?author=1&ordering=published_date
    /api/books/advanced/?search=python&ordering=-published_date,title
    """
    serializer_class = BookListSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [SearchFilter, OrderingFilter]
    
    # Search
    search_fields = ['title', 'subtitle', 'author__name']
    
    # Ordering
    ordering_fields = [
        'price',
        'published_date',
        'title',
        'pages',
        'author__name'
    ]
    ordering = ['-published_date', 'title']
    
    def get_queryset(self):
        queryset = Book.objects.select_related('author').prefetch_related('genres')
        
        # Manual filtering
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author_id=author)
        
        published = self.request.query_params.get('published')
        if published:
            is_published = published.lower() == 'true'
            queryset = queryset.filter(published=is_published)
        
        return queryset


# ==================== URLS ====================

from django.urls import path

urlpatterns = [
    # Basic ordering
    path('books/ordering/', BookOrderingView.as_view(), name='book-ordering'),
    
    # Multiple ordering
    path('books/multi-ordering/', BookMultipleOrderingView.as_view(), name='book-multi-ordering'),
    
    # Related field ordering
    path('books/related-ordering/', BookRelatedOrderingView.as_view(), name='book-related-ordering'),
    
    # All fields ordering
    path('books/all-ordering/', BookAllFieldsOrderingView.as_view(), name='book-all-ordering'),
    
    # Custom ordering
    path('books/custom-ordering/', BookCustomOrderingView.as_view(), name='book-custom-ordering'),
    
    # Case-insensitive
    path('books/case-ordering/', BookCaseInsensitiveOrderingView.as_view(), name='book-case-ordering'),
    
    # Authors with computed fields
    path('authors/ordering/', AuthorOrderingView.as_view(), name='author-ordering'),
    
    # Search + Ordering
    path('books/search-ordering/', BookSearchAndOrderingView.as_view(), name='book-search-ordering'),
    
    # Optimized
    path('books/optimized-ordering/', BookOptimizedOrderingView.as_view(), name='book-optimized-ordering'),
    
    # Advanced
    path('books/advanced/', BookAdvancedView.as_view(), name='book-advanced'),
]


# ==================== ORDERING TIPS ====================

"""
1. PERFORMANCE:
   ✅ Index qo'shish: 
      - db_index=True
      - Meta.indexes
   ✅ Faqat indexed fieldlar bo'yicha ordering
   ✅ select_related() / prefetch_related()
   ❌ Computed fieldlar bo'yicha ordering (sekin)

2. USER EXPERIENCE:
   ✅ Sensible default ordering
   ✅ Most common fields uchun ordering
   ✅ Clear field names
   ❌ Barcha fieldlarni __all__ qilmaslik

3. DATABASE INDEXES:
   ```python
   class Book(models.Model):
       price = models.DecimalField(db_index=True)
       published_date = models.DateField(db_index=True)
       
       class Meta:
           indexes = [
               models.Index(fields=['author', '-published_date']),
               models.Index(fields=['-price']),
           ]
   ```

4. COMMON PATTERNS:
   - Default: ordering = ['-created_at']
   - Alphabetical: ordering = ['title']
   - Popularity: ordering = ['-view_count', '-created_at']
   - Price: ordering = ['price']
"""


# ==================== NULL HANDLING ====================

"""
Django'da NULL qiymatlar ordering'da:

ASCENDING (o'sish):
- NULL values LAST (oxirida)
- 1, 2, 3, ..., NULL

DESCENDING (kamayish):
- NULL values FIRST (boshida)
- NULL, ..., 3, 2, 1

Custom NULL ordering:
from django.db.models import F

queryset.order_by(F('price').asc(nulls_last=True))
queryset.order_by(F('price').desc(nulls_first=False))
"""


# ==================== SWAGGER INTEGRATION ====================

"""
OrderingFilter avtomatik Swagger UI'da ko'rinadi:

Parameters:
- ordering (query, optional): Field name(s) to order by

Example:
{
  "name": "ordering",
  "in": "query",
  "required": false,
  "schema": {
    "type": "string"
  },
  "description": "Which field to use when ordering the results"
}

Available fields:
- price
- title
- published_date
- pages
"""