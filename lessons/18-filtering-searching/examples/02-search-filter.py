"""
SearchFilter Example

DRF'ning tayyor SearchFilter'i bilan ishlash.
Turli xil search operators.
"""

from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from books.serializers import BookSerializer, BookListSerializer
from books.models import Book


# ==================== 1. BASIC SEARCH ====================

class BookSearchView(generics.ListAPIView):
    """
    Basic search - barcha search_fields ichida qidiradi
    
    Examples:
    /api/books/?search=django         # "django" so'zini qidirish
    /api/books/?search=john doe       # "john doe" ni qidirish
    /api/books/?search=python guide   # "python" VA "guide" ni qidirish
    """
    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [SearchFilter]
    search_fields = ['title', 'subtitle', 'author__name']


"""
SearchFilter qanday ishlaydi?

1. Har bir search field bo'yicha OR qidiradi:
   title ILIKE '%django%' OR 
   subtitle ILIKE '%django%' OR 
   author__name ILIKE '%django%'

2. Ko'p so'zlar uchun AND qidiradi:
   search=python guide
   
   (title ILIKE '%python%' OR subtitle ILIKE '%python%') AND
   (title ILIKE '%guide%' OR subtitle ILIKE '%guide%')
"""


# ==================== 2. SEARCH OPERATORS ====================

class BookAdvancedSearchView(generics.ListAPIView):
    """
    Search operators bilan aniq qidirish
    
    Operators:
    '^' - Starts with (boshidan boshlanishi kerak)
    '=' - Exact match (aniq mos kelishi kerak)
    '@' - Full-text search (PostgreSQL full-text)
    '$' - Regex search
    
    Examples:
    /api/books/?search=django    # Title "django" bilan boshlanadi
    """
    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [SearchFilter]
    search_fields = [
        '^title',           # Title boshidan boshlanishi kerak
        'subtitle',         # Subtitle ichida bo'lsa yetarli
        'author__name',     # Author nomi ichida
        '=isbn_number'      # ISBN aniq mos kelishi kerak
    ]


"""
Operator tushuntirishlari:

1. '^' - STARTS WITH:
   '^title' -> title ILIKE 'django%'
   Faqat boshidan boshlanganlarni topadi

2. '=' - EXACT MATCH:
   '=isbn_number' -> isbn_number = '9781234567890'
   Aniq mos kelishi kerak

3. '@' - FULL-TEXT SEARCH (PostgreSQL):
   '@description' -> Full-text search index ishlatadi
   Faqat PostgreSQL'da ishlaydi

4. '$' - REGEX:
   '$title' -> title ~* 'pattern'
   Regex pattern'lar bilan qidirish
"""


# ==================== 3. MULTIPLE FIELDS ====================

class BookMultiFieldSearchView(generics.ListAPIView):
    """
    Ko'p fieldlar bo'yicha qidirish
    
    Examples:
    /api/books/?search=django        # Barcha fieldlarda qidiradi
    /api/books/?search=978           # ISBN ichida ham qidiradi
    /api/books/?search=tech books    # Publisher ichida ham qidiradi
    """
    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [SearchFilter]
    search_fields = [
        'title',
        'subtitle',
        'author__name',
        'isbn_number',
        'publisher',
        'language'
    ]


# ==================== 4. RELATED FIELD SEARCH ====================

class BookRelatedSearchView(generics.ListAPIView):
    """
    Related model fieldlari bo'yicha qidirish
    
    ForeignKey: author__name, author__email
    ManyToMany: genres__name
    
    Examples:
    /api/books/?search=john@example.com    # Author email bo'yicha
    /api/books/?search=programming         # Genre nomi bo'yicha
    """
    queryset = Book.objects.select_related('author').prefetch_related('genres')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [SearchFilter]
    search_fields = [
        'title',
        'author__name',
        'author__email',
        'genres__name',      # ManyToMany field
        'genres__description'
    ]


# ==================== 5. CUSTOM SEARCH ====================

class CustomSearchFilter(SearchFilter):
    """
    Custom search filter - search parameter nomini o'zgartirish
    """
    search_param = 'q'  # Default: 'search' -> 'q' ga o'zgartirdik


class BookCustomSearchView(generics.ListAPIView):
    """
    Custom search parameter
    
    Examples:
    /api/books/?q=django        # 'search' o'rniga 'q' ishlatamiz
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [CustomSearchFilter]
    search_fields = ['title', 'subtitle']


# ==================== 6. SEARCH + PERFORMANCE ====================

class BookOptimizedSearchView(generics.ListAPIView):
    """
    Performance optimized search
    
    - select_related() - ForeignKey uchun
    - prefetch_related() - ManyToMany uchun
    - only() - Faqat kerakli fieldlar
    """
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [SearchFilter]
    search_fields = [
        'title',
        'subtitle',
        'author__name'
    ]
    
    def get_queryset(self):
        # Optimized queryset
        return Book.objects.select_related('author').prefetch_related('genres').only(
            'id', 'title', 'subtitle', 'price', 
            'author__id', 'author__name'
        )


# ==================== 7. CASE SENSITIVITY ====================

"""
SearchFilter default ravishda CASE-INSENSITIVE:

search=DJANGO == search=django == search=Django

Django ORM'da:
- ILIKE (PostgreSQL) - case-insensitive
- LIKE (MySQL) - default case-insensitive (depends on collation)
- UPPER/LOWER (SQLite) - case-insensitive

Agar case-sensitive kerak bo'lsa, custom filter yozish kerak.
"""


# ==================== REAL WORLD EXAMPLE ====================

class BookGlobalSearchView(generics.ListAPIView):
    """
    Global search - barcha muhim fieldlar bo'yicha
    
    Features:
    - Title, subtitle, author, publisher bo'yicha
    - ISBN aniq qidirish
    - Genre nomi bo'yicha
    - Performance optimized
    
    Examples:
    /api/books/search/?search=django rest
    /api/books/search/?search=john doe
    /api/books/search/?search=9781234567890
    """
    serializer_class = BookListSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [SearchFilter]
    search_fields = [
        '^title',              # Priority 1: Title boshidan
        'subtitle',            # Priority 2: Subtitle ichida
        'author__name',        # Priority 3: Author nomi
        'publisher',           # Priority 4: Publisher
        '=isbn_number',        # Aniq ISBN
        'genres__name'         # Genre nomi
    ]
    
    def get_queryset(self):
        return Book.objects.select_related(
            'author', 'owner'
        ).prefetch_related(
            'genres'
        ).filter(
            published=True  # Faqat published kitoblar
        )


# ==================== URLS ====================

from django.urls import path

urlpatterns = [
    # Basic search
    path('books/search/', BookSearchView.as_view(), name='book-search'),
    
    # Advanced search (operators)
    path('books/advanced-search/', BookAdvancedSearchView.as_view(), name='book-advanced-search'),
    
    # Multi-field search
    path('books/multi-search/', BookMultiFieldSearchView.as_view(), name='book-multi-search'),
    
    # Related field search
    path('books/related-search/', BookRelatedSearchView.as_view(), name='book-related-search'),
    
    # Custom search parameter
    path('books/custom-search/', BookCustomSearchView.as_view(), name='book-custom-search'),
    
    # Optimized search
    path('books/optimized-search/', BookOptimizedSearchView.as_view(), name='book-optimized-search'),
    
    # Global search
    path('books/global-search/', BookGlobalSearchView.as_view(), name='book-global-search'),
]


# ==================== SEARCH TIPS ====================

"""
1. PERFORMANCE:
   ✅ Index qo'shish: db_index=True
   ✅ select_related() / prefetch_related()
   ✅ only() / defer() - faqat kerakli fieldlar
   ❌ Search fieldlarni ko'p qilmaslik

2. USER EXPERIENCE:
   ✅ Relevant fieldlarni search'ga qo'shish
   ✅ Priority berish (^, =)
   ✅ Related fieldlarni qo'shish
   ❌ Barcha fieldlarni search'ga qo'shmaslik

3. SECURITY:
   ✅ Django ORM avtomatik SQL injection'dan himoya qiladi
   ✅ search_fields listini nazorat qilish
   ❌ Raw SQL ishlatmaslik

4. TESTING:
   ✅ Turli xil search query'larni test qilish
   ✅ Performance test (ko'p ma'lumotlar bilan)
   ✅ Edge cases (empty search, special characters)
"""


# ==================== COMMON PATTERNS ====================

"""
Pattern 1: Title priority search
search_fields = ['^title', 'subtitle', 'author__name']

Pattern 2: Exact + contains
search_fields = ['=isbn_number', 'title', 'author__name']

Pattern 3: Full coverage
search_fields = [
    '^title',
    'subtitle', 
    'author__name',
    'publisher',
    'genres__name'
]

Pattern 4: Minimal (fast)
search_fields = ['title', 'author__name']
"""


# ==================== SWAGGER INTEGRATION ====================

"""
SearchFilter avtomatik ravishda Swagger UI'da ko'rinadi:

Parameters:
- search (query, optional): Search term

Example:
{
  "name": "search",
  "in": "query",
  "required": false,
  "schema": {
    "type": "string"
  }
}
"""