"""
DjangoFilterBackend Example

django-filter package bilan murakkab filtrlash.
FilterSet class va turli xil filter turlari.
"""

from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from books.serializers import BookSerializer, BookListSerializer
from books.models import Book, Author, Genre

# ==================== INSTALLATION ====================

"""
1. Install django-filter:
   pip install django-filter
   
   yoki
   
   pipenv install django-filter

2. Add to INSTALLED_APPS:
   INSTALLED_APPS = [
       ...
       'django_filters',
   ]

3. (Optional) Add to REST_FRAMEWORK settings:
   REST_FRAMEWORK = {
       'DEFAULT_FILTER_BACKENDS': [
           'django_filters.rest_framework.DjangoFilterBackend',
       ]
   }
"""


# ==================== 1. BASIC DJANGO FILTER ====================

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

class BookBasicFilterView(generics.ListAPIView):
    """
    Basic django-filter - oddiy fieldlar
    
    Examples:
    /api/books/?author=1
    /api/books/?published=true
    /api/books/?language=English
    /api/books/?author=1&published=true
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'published', 'language']


"""
filterset_fields - oddiy filtering:
- Faqat exact match
- author=1 -> author_id=1
- published=true -> published=True
"""


# ==================== 2. FILTERSET CLASS ====================

from django_filters import rest_framework as filters

class BookFilter(filters.FilterSet):
    """
    Custom FilterSet - murakkab filtrlash
    """
    
    # Title - case-insensitive contains
    title = filters.CharFilter(lookup_expr='icontains')
    
    # Price range
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    # Pages range
    min_pages = filters.NumberFilter(field_name='pages', lookup_expr='gte')
    max_pages = filters.NumberFilter(field_name='pages', lookup_expr='lte')
    
    # Date filters
    published_year = filters.NumberFilter(field_name='published_date', lookup_expr='year')
    published_after = filters.DateFilter(field_name='published_date', lookup_expr='gte')
    published_before = filters.DateFilter(field_name='published_date', lookup_expr='lte')
    
    class Meta:
        model = Book
        fields = ['author', 'published', 'language']


class BookFilterView(generics.ListAPIView):
    """
    FilterSet class bilan
    
    Examples:
    /api/books/?title=django
    /api/books/?min_price=20&max_price=50
    /api/books/?published_year=2024
    /api/books/?published_after=2024-01-01&published_before=2024-12-31
    /api/books/?author=1&min_price=25
    """
    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter


# ==================== 3. LOOKUP EXPRESSIONS ====================

class AdvancedBookFilter(filters.FilterSet):
    """
    Barcha lookup expressions
    """
    
    # EXACT (default)
    isbn = filters.CharFilter(field_name='isbn_number', lookup_expr='exact')
    
    # IEXACT - case-insensitive exact
    language = filters.CharFilter(field_name='language', lookup_expr='iexact')
    
    # CONTAINS - ichida bor
    title_contains = filters.CharFilter(field_name='title', lookup_expr='contains')
    
    # ICONTAINS - case-insensitive contains
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    
    # STARTSWITH / ISTARTSWITH
    title_starts = filters.CharFilter(field_name='title', lookup_expr='istartswith')
    
    # ENDSWITH / IENDSWITH
    title_ends = filters.CharFilter(field_name='title', lookup_expr='iendswith')
    
    # GT / GTE / LT / LTE
    price_gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_gte = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lt = filters.NumberFilter(field_name='price', lookup_expr='lt')
    price_lte = filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    # IN - ro'yxatdan birortasi
    authors = filters.ModelMultipleChoiceFilter(
        field_name='author',
        queryset=Author.objects.all()
    )
    
    # RANGE
    price_range = filters.RangeFilter(field_name='price')
    
    class Meta:
        model = Book
        fields = []


"""
Examples:
/api/books/?title=django                    # icontains
/api/books/?isbn=9781234567890              # exact
/api/books/?price_range_min=20&price_range_max=50  # range
/api/books/?authors=1,2,3                   # in [1,2,3]
"""


# ==================== 4. FILTER TYPES ====================

class FilterTypesExample(filters.FilterSet):
    """
    Turli xil filter turlari
    """
    
    # CharFilter - text fields
    title = filters.CharFilter(lookup_expr='icontains')
    
    # NumberFilter - numeric fields
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    
    # BooleanFilter - boolean fields
    published = filters.BooleanFilter(field_name='published')
    
    # DateFilter - date fields
    published_after = filters.DateFilter(field_name='published_date', lookup_expr='gte')
    
    # DateTimeFilter - datetime fields
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    
    # DateRangeFilter - predefined ranges
    published_range = filters.DateRangeFilter(field_name='published_date')
    
    # DateFromToRangeFilter - custom range
    published_date_range = filters.DateFromToRangeFilter(field_name='published_date')
    
    # ChoiceFilter - limited choices
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('uz', 'Uzbek'),
        ('ru', 'Russian'),
    ]
    language = filters.ChoiceFilter(choices=LANGUAGE_CHOICES)
    
    # MultipleChoiceFilter
    languages = filters.MultipleChoiceFilter(
        field_name='language',
        choices=LANGUAGE_CHOICES
    )
    
    # ModelChoiceFilter - ForeignKey
    author = filters.ModelChoiceFilter(queryset=Author.objects.all())
    
    # ModelMultipleChoiceFilter - ForeignKey (multiple)
    authors = filters.ModelMultipleChoiceFilter(
        field_name='author',
        queryset=Author.objects.all()
    )
    
    # RangeFilter - min va max
    price_range = filters.RangeFilter(field_name='price')
    
    # OrderingFilter - FilterSet ichida
    ordering = filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('published_date', 'date'),
        )
    )
    
    class Meta:
        model = Book
        fields = []


"""
Examples:

DateRangeFilter choices:
/api/books/?published_range=today
/api/books/?published_range=yesterday
/api/books/?published_range=week
/api/books/?published_range=month
/api/books/?published_range=year

DateFromToRangeFilter:
/api/books/?published_date_range_after=2024-01-01
/api/books/?published_date_range_before=2024-12-31

RangeFilter:
/api/books/?price_range_min=20&price_range_max=50
"""


# ==================== 5. CUSTOM METHOD FILTER ====================

class CustomMethodFilter(filters.FilterSet):
    """
    Custom method filter - murakkab logic
    """
    
    # Simple method filter
    has_author = filters.BooleanFilter(method='filter_has_author')
    
    # Method filter with parameter
    min_title_length = filters.NumberFilter(method='filter_min_title_length')
    
    # Author books count
    author_min_books = filters.NumberFilter(method='filter_author_min_books')
    
    def filter_has_author(self, queryset, name, value):
        """Muallifi bor/yo'q kitoblar"""
        if value:
            return queryset.filter(author__isnull=False)
        return queryset.filter(author__isnull=True)
    
    def filter_min_title_length(self, queryset, name, value):
        """Title uzunligi bo'yicha"""
        from django.db.models import Length
        return queryset.annotate(
            title_length=Length('title')
        ).filter(title_length__gte=value)
    
    def filter_author_min_books(self, queryset, name, value):
        """Author'ning kitoblar soni bo'yicha"""
        from django.db.models import Count
        return queryset.annotate(
            author_books=Count('author__books')
        ).filter(author_books__gte=value)
    
    class Meta:
        model = Book
        fields = []


"""
Examples:
/api/books/?has_author=true
/api/books/?min_title_length=20
/api/books/?author_min_books=3
"""


# ==================== 6. RELATED FIELD FILTERING ====================

class RelatedFieldFilter(filters.FilterSet):
    """
    Related model fieldlari bo'yicha filtrlash
    """
    
    # ForeignKey fields
    author_name = filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains'
    )
    author_email = filters.CharFilter(
        field_name='author__email',
        lookup_expr='iexact'
    )
    
    # ManyToMany fields
    genre_name = filters.CharFilter(
        field_name='genres__name',
        lookup_expr='icontains'
    )
    
    # Multiple related filters
    genres = filters.ModelMultipleChoiceFilter(
        field_name='genres',
        queryset=Genre.objects.all()
    )
    
    class Meta:
        model = Book
        fields = []


"""
Examples:
/api/books/?author_name=john
/api/books/?author_email=john@example.com
/api/books/?genre_name=programming
/api/books/?genres=1,2,3
"""


# ==================== 7. COMBINING FILTERS ====================

from rest_framework.filters import SearchFilter, OrderingFilter

class CombinedBookFilter(filters.FilterSet):
    """
    Barcha filter turlari birgalikda
    """
    
    # Text filters
    title = filters.CharFilter(lookup_expr='icontains')
    
    # Number filters
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    # Date filters
    published_year = filters.NumberFilter(field_name='published_date', lookup_expr='year')
    published_after = filters.DateFilter(field_name='published_date', lookup_expr='gte')
    
    # Boolean filter
    published = filters.BooleanFilter()
    
    # Choice filter
    language = filters.ChoiceFilter(choices=[
        ('English', 'English'),
        ('Uzbek', 'Uzbek'),
        ('Russian', 'Russian'),
    ])
    
    # Related filters
    author_name = filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    
    class Meta:
        model = Book
        fields = ['author']


class BookCombinedView(generics.ListAPIView):
    """
    DjangoFilter + SearchFilter + OrderingFilter
    
    Examples:
    /api/books/all/?title=django&min_price=20&search=guide&ordering=-price
    /api/books/all/?author=1&published=true&published_year=2024&search=python
    """
    queryset = Book.objects.select_related('author').prefetch_related('genres')
    serializer_class = BookSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # DjangoFilter
    filterset_class = CombinedBookFilter
    
    # SearchFilter
    search_fields = ['title', 'subtitle', 'author__name']
    
    # OrderingFilter
    ordering_fields = ['price', 'published_date', 'title']
    ordering = ['-published_date']


# ==================== 8. FILTERSET FORM ====================

class FormFilterSet(filters.FilterSet):
    """
    FilterSet'ni HTML form sifatida ko'rsatish
    """
    
    title = filters.CharFilter(
        lookup_expr='icontains',
        label='Kitob nomi',
        help_text='Kitob nomini kiriting'
    )
    
    price = filters.RangeFilter(
        label='Narx oralig\'i',
        help_text='Min va max narx'
    )
    
    published_date = filters.DateFromToRangeFilter(
        label='Nashr sanasi',
        help_text='Sanalar oralig\'i'
    )
    
    class Meta:
        model = Book
        fields = ['title', 'price', 'published_date']


"""
HTML form:
{% load django_filters %}

<form method="get">
    {{ filter.form.as_p }}
    <button type="submit">Filter</button>
</form>
"""


# ==================== 9. REAL WORLD EXAMPLE ====================

class ProductionBookFilter(filters.FilterSet):
    """
    Production-ready filter
    
    Features:
    - Text search
    - Price range
    - Date range
    - Author filter
    - Genre filter
    - Language filter
    - Published status
    """
    
    # Text search
    title = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Title'
    )
    
    # Price range
    min_price = filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Minimum Price'
    )
    max_price = filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Maximum Price'
    )
    price_range = filters.RangeFilter(
        field_name='price',
        label='Price Range'
    )
    
    # Pages range
    min_pages = filters.NumberFilter(
        field_name='pages',
        lookup_expr='gte',
        label='Minimum Pages'
    )
    max_pages = filters.NumberFilter(
        field_name='pages',
        lookup_expr='lte',
        label='Maximum Pages'
    )
    
    # Date filters
    published_year = filters.NumberFilter(
        field_name='published_date',
        lookup_expr='year',
        label='Published Year'
    )
    published_after = filters.DateFilter(
        field_name='published_date',
        lookup_expr='gte',
        label='Published After'
    )
    published_before = filters.DateFilter(
        field_name='published_date',
        lookup_expr='lte',
        label='Published Before'
    )
    
    # Author
    author = filters.ModelChoiceFilter(
        queryset=Author.objects.all(),
        label='Author'
    )
    author_name = filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        label='Author Name'
    )
    
    # Genres
    genres = filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(),
        label='Genres'
    )
    
    # Language
    language = filters.ChoiceFilter(
        choices=[
            ('English', 'English'),
            ('Uzbek', 'Uzbek'),
            ('Russian', 'Russian'),
        ],
        label='Language'
    )
    
    # Published status
    published = filters.BooleanFilter(
        field_name='published',
        label='Published'
    )
    
    class Meta:
        model = Book
        fields = []


class BookProductionView(generics.ListAPIView):
    """
    Production-ready book list with all filters
    """
    queryset = Book.objects.select_related('author').prefetch_related('genres')
    serializer_class = BookListSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductionBookFilter
    search_fields = ['title', 'subtitle', 'author__name', 'publisher']
    ordering_fields = ['price', 'published_date', 'title', 'pages']
    ordering = ['-published_date']


# ==================== URLS ====================

from django.urls import path

urlpatterns = [
    # Basic django-filter
    path('books/basic-filter/', BookBasicFilterView.as_view(), name='book-basic-filter'),
    
    # FilterSet class
    path('books/filter/', BookFilterView.as_view(), name='book-filter'),
    
    # Combined filters
    path('books/all/', BookCombinedView.as_view(), name='book-all'),
    
    # Production
    path('books/production/', BookProductionView.as_view(), name='book-production'),
]


# ==================== BEST PRACTICES ====================

"""
1. PERFORMANCE:
   ✅ select_related() - ForeignKey
   ✅ prefetch_related() - ManyToMany
   ✅ Database indexes
   ✅ Limit filter fields
   ❌ Too many filters

2. USER EXPERIENCE:
   ✅ Clear filter names
   ✅ Helpful labels
   ✅ Sensible defaults
   ✅ Documentation

3. SECURITY:
   ✅ Validate inputs
   ✅ Limit queryset
   ✅ Permissions
   ❌ Expose sensitive fields

4. TESTING:
   ✅ Unit tests
   ✅ Integration tests
   ✅ Edge cases
"""


# ==================== COMMON PATTERNS ====================

"""
Pattern 1: Simple filtering
filterset_fields = ['author', 'published', 'language']

Pattern 2: Range filters
class Filter(FilterSet):
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

Pattern 3: Date filtering
class Filter(FilterSet):
    year = NumberFilter(field_name='date', lookup_expr='year')
    after = DateFilter(field_name='date', lookup_expr='gte')
    before = DateFilter(field_name='date', lookup_expr='lte')

Pattern 4: Text search
class Filter(FilterSet):
    title = CharFilter(lookup_expr='icontains')
    author = CharFilter(field_name='author__name', lookup_expr='icontains')
"""


# ==================== SWAGGER INTEGRATION ====================

"""
django-filter avtomatik Swagger UI'da ko'rinadi:

Parameters ko'rinishi:
- title (query, optional, string)
- min_price (query, optional, number)
- max_price (query, optional, number)
- published (query, optional, boolean)
- author (query, optional, integer)

drf-spectacular bilan:
from drf_spectacular.utils import extend_schema, OpenApiParameter

@extend_schema(
    parameters=[
        OpenApiParameter(
            name='min_price',
            type=float,
            description='Minimum price',
            required=False
        )
    ]
)
class BookView(generics.ListAPIView):
    ...
"""