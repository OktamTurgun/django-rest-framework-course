"""
Basic Filtering Example

Manual filtering with get_queryset() override.
URL parameters bilan filtrlash.
"""

from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.db import models
from books.serializers import BookSerializer


# ==================== MODELS ====================

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    published = models.BooleanField(default=False)
    language = models.CharField(max_length=50, default='English')
    pages = models.IntegerField()
    published_date = models.DateField()


# ==================== 1. ODDIY FILTERING ====================

class BookListView(generics.ListAPIView):
    """
    Basic filtering - get_queryset() override
    
    Examples:
    /api/books/                       # Barcha kitoblar
    /api/books/?author=1              # Author ID=1 ning kitoblari
    /api/books/?published=true        # Published kitoblar
    /api/books/?language=English      # English kitoblar
    """
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Book.objects.all()
        
        # URL parametrlarini olish
        author_id = self.request.query_params.get('author')
        published = self.request.query_params.get('published')
        language = self.request.query_params.get('language')
        
        # Filtrlash
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        if published is not None:
            # String'ni boolean'ga convert qilish
            is_published = published.lower() == 'true'
            queryset = queryset.filter(published=is_published)
        
        if language:
            queryset = queryset.filter(language=language)
        
        return queryset


# ==================== 2. RANGE FILTERING ====================

class BookPriceRangeView(generics.ListAPIView):
    """
    Narx oralig'i bo'yicha filtrlash
    
    Examples:
    /api/books/price-range/?min_price=20           # 20 dan yuqori
    /api/books/price-range/?max_price=50           # 50 dan past
    /api/books/price-range/?min_price=20&max_price=50  # 20-50 orasida
    """
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Book.objects.all()
        
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset


# ==================== 3. DATE FILTERING ====================

class BookDateRangeView(generics.ListAPIView):
    """
    Sana oralig'i bo'yicha filtrlash
    
    Examples:
    /api/books/date-range/?year=2024                    # 2024 yilda nashr etilgan
    /api/books/date-range/?after=2024-01-01             # 2024-01-01 dan keyin
    /api/books/date-range/?before=2024-12-31            # 2024-12-31 dan oldin
    /api/books/date-range/?after=2024-01-01&before=2024-06-30  # Q1-Q2 2024
    """
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Book.objects.all()
        
        year = self.request.query_params.get('year')
        after = self.request.query_params.get('after')
        before = self.request.query_params.get('before')
        
        if year:
            queryset = queryset.filter(published_date__year=year)
        
        if after:
            queryset = queryset.filter(published_date__gte=after)
        
        if before:
            queryset = queryset.filter(published_date__lte=before)
        
        return queryset


# ==================== 4. MULTIPLE FILTERS ====================

class BookAdvancedFilterView(generics.ListAPIView):
    """
    Ko'p filterlarni birga ishlatish
    
    Examples:
    /api/books/advanced/?author=1&published=true&language=English
    /api/books/advanced/?min_price=20&max_price=50&published=true
    /api/books/advanced/?year=2024&author=1
    """
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Book.objects.select_related('author')
        
        # Author filter
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        # Published filter
        published = self.request.query_params.get('published')
        if published is not None:
            is_published = published.lower() == 'true'
            queryset = queryset.filter(published=is_published)
        
        # Language filter
        language = self.request.query_params.get('language')
        if language:
            queryset = queryset.filter(language__iexact=language)
        
        # Price range
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Pages range
        min_pages = self.request.query_params.get('min_pages')
        if min_pages:
            queryset = queryset.filter(pages__gte=min_pages)
        
        max_pages = self.request.query_params.get('max_pages')
        if max_pages:
            queryset = queryset.filter(pages__lte=max_pages)
        
        # Date filters
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(published_date__year=year)
        
        after = self.request.query_params.get('after')
        if after:
            queryset = queryset.filter(published_date__gte=after)
        
        before = self.request.query_params.get('before')
        if before:
            queryset = queryset.filter(published_date__lte=before)
        
        return queryset


# ==================== 5. RELATED FIELD FILTERING ====================

class BookAuthorFilterView(generics.ListAPIView):
    """
    Related field bo'yicha filtrlash (Author nomi)
    
    Examples:
    /api/books/by-author/?author_name=John
    /api/books/by-author/?author_email=john@example.com
    """
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Book.objects.select_related('author')
        
        # Author nomi bo'yicha (case-insensitive)
        author_name = self.request.query_params.get('author_name')
        if author_name:
            queryset = queryset.filter(author__name__icontains=author_name)
        
        # Author email bo'yicha
        author_email = self.request.query_params.get('author_email')
        if author_email:
            queryset = queryset.filter(author__email__iexact=author_email)
        
        return queryset


# ==================== 6. Q OBJECTS (OR FILTERING) ====================

from django.db.models import Q

class BookSearchView(generics.ListAPIView):
    """
    Q objects bilan OR filtering
    
    Examples:
    /api/books/search/?q=django     # Title yoki subtitle da "django"
    """
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Book.objects.select_related('author')
        
        q = self.request.query_params.get('q')
        if q:
            # Title yoki subtitle da qidirish
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(subtitle__icontains=q)
            )
        
        return queryset


# ==================== URLS ====================

from django.urls import path

urlpatterns = [
    # Basic filtering
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Price range
    path('books/price-range/', BookPriceRangeView.as_view(), name='book-price-range'),
    
    # Date range
    path('books/date-range/', BookDateRangeView.as_view(), name='book-date-range'),
    
    # Advanced filtering
    path('books/advanced/', BookAdvancedFilterView.as_view(), name='book-advanced'),
    
    # Author filter
    path('books/by-author/', BookAuthorFilterView.as_view(), name='book-by-author'),
    
    # Search (Q objects)
    path('books/search/', BookSearchView.as_view(), name='book-search'),
]


# ==================== DJANGO LOOKUP TYPES ====================

"""
Django ORM Lookup Types:

EXACT MATCH:
- field__exact='value'              # Aniq mos kelish
- field__iexact='value'             # Case-insensitive exact

CONTAINS:
- field__contains='value'           # Ichida bor
- field__icontains='value'          # Case-insensitive contains

STARTS/ENDS WITH:
- field__startswith='value'         # Boshidan boshlanadi
- field__istartswith='value'        # Case-insensitive starts
- field__endswith='value'           # Oxirida tugaydi
- field__iendswith='value'          # Case-insensitive ends

COMPARISONS:
- field__gt=value                   # Greater than
- field__gte=value                  # Greater than or equal
- field__lt=value                   # Less than
- field__lte=value                  # Less than or equal

NULL CHECKS:
- field__isnull=True                # NULL
- field__isnull=False               # NOT NULL

IN LIST:
- field__in=[1, 2, 3]               # IN (1, 2, 3)

RANGE:
- field__range=(start, end)         # BETWEEN start AND end

DATE/TIME:
- field__year=2024                  # Year
- field__month=1                    # Month
- field__day=15                     # Day
- field__week=1                     # Week
- field__quarter=1                  # Quarter
- field__date=date_obj              # Date part

RELATED FIELDS:
- related_field__field=value        # ForeignKey lookup
- related_field__field__icontains   # Nested lookup
"""


# ==================== BEST PRACTICES ====================

"""
1. PERFORMANCE:
   - select_related() - ForeignKey uchun
   - prefetch_related() - ManyToMany uchun
   - Indexlar qo'shish

2. VALIDATION:
   - URL parametrlarni validate qilish
   - Try-except bilan xatoliklarni ushlash
   - Sensible defaults

3. DOCUMENTATION:
   - Docstring yozish
   - Examples berish
   - API docs'da ko'rsatish

4. SECURITY:
   - SQL injection'dan himoya (Django ORM buni avtomatik qiladi)
   - Input validation
   - Permissions

Example:

def get_queryset(self):
    queryset = Book.objects.select_related('author')
    
    # Validate and convert
    try:
        author_id = int(self.request.query_params.get('author', 0))
        if author_id > 0:
            queryset = queryset.filter(author_id=author_id)
    except (ValueError, TypeError):
        pass  # Invalid input, ignore
    
    return queryset
"""