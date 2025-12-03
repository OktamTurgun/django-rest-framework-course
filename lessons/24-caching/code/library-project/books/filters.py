"""
Books app filters
FilterSet classes for Book, Author, and Genre models
"""

from django_filters import rest_framework as filters
from django.db.models import Count, Avg
from .models import Book, Author, Genre


# ==================== BOOK FILTERS ====================

class BookFilter(filters.FilterSet):
    """
    Book FilterSet - murakkab filtrlash
    
    Filters:
    - title: Kitob nomi bo'yicha (icontains)
    - min_price / max_price: Narx oralig'i
    - min_pages / max_pages: Sahifalar soni oralig'i
    - published_year: Yil bo'yicha
    - published_after / published_before: Sana oralig'i
    - author: Author ID
    - author_name: Author nomi (icontains)
    - genres: Genre ID'lar (multiple)
    - published: Published status
    - language: Til
    
    Examples:
    /api/books/?title=django
    /api/books/?min_price=20&max_price=50
    /api/books/?published_year=2024
    /api/books/?author=1&published=true
    /api/books/?genres=1,2,3
    """
    
    # Text filters
    title = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Title contains'
    )
    
    subtitle = filters.CharFilter(
        field_name='subtitle',
        lookup_expr='icontains',
        label='Subtitle contains'
    )
    
    # Price range filters
    min_price = filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Minimum price'
    )
    
    max_price = filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Maximum price'
    )
    
    price_range = filters.RangeFilter(
        field_name='price',
        label='Price range'
    )
    
    # Pages range filters
    min_pages = filters.NumberFilter(
        field_name='pages',
        lookup_expr='gte',
        label='Minimum pages'
    )
    
    max_pages = filters.NumberFilter(
        field_name='pages',
        lookup_expr='lte',
        label='Maximum pages'
    )
    
    # Date filters
    published_year = filters.NumberFilter(
        field_name='published_date',
        lookup_expr='year',
        label='Published year'
    )
    
    published_after = filters.DateFilter(
        field_name='published_date',
        lookup_expr='gte',
        label='Published after'
    )
    
    published_before = filters.DateFilter(
        field_name='published_date',
        lookup_expr='lte',
        label='Published before'
    )
    
    # Author filters
    author = filters.ModelChoiceFilter(
        queryset=Author.objects.all(),
        label='Author'
    )
    
    author_name = filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        label='Author name contains'
    )
    
    # Genre filters
    genres = filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(),
        label='Genres'
    )
    
    genre_name = filters.CharFilter(
        field_name='genres__name',
        lookup_expr='icontains',
        label='Genre name contains'
    )
    
    # Other filters
    published = filters.BooleanFilter(
        field_name='published',
        label='Published status'
    )
    
    language = filters.ChoiceFilter(
        field_name='language',
        choices=[
            ('English', 'English'),
            ('Uzbek', 'Uzbek'),
            ('Russian', 'Russian'),
        ],
        label='Language'
    )
    
    # ISBN filter (exact match)
    isbn = filters.CharFilter(
        field_name='isbn_number',
        lookup_expr='exact',
        label='ISBN'
    )
    
    # Publisher filter
    publisher = filters.CharFilter(
        field_name='publisher',
        lookup_expr='icontains',
        label='Publisher contains'
    )
    
    class Meta:
        model = Book
        fields = []
    
    @property
    def qs(self):
        """
        Custom queryset with optimizations
        """
        parent = super().qs
        return parent.select_related('author', 'owner').prefetch_related('genres')


# ==================== AUTHOR FILTERS ====================

class AuthorFilter(filters.FilterSet):
    """
    Author FilterSet
    
    Filters:
    - name: Author nomi (icontains)
    - email: Email (icontains)
    - has_published_books: Published kitoblari bor/yo'q
    - min_books: Minimal kitoblar soni
    - birth_year: Tug'ilgan yil
    
    Examples:
    /api/authors/?name=john
    /api/authors/?has_published_books=true
    /api/authors/?min_books=2
    """
    
    # Text filters
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Name contains'
    )
    
    email = filters.CharFilter(
        field_name='email',
        lookup_expr='icontains',
        label='Email contains'
    )
    
    # Birth date filters
    birth_year = filters.NumberFilter(
        field_name='birth_date',
        lookup_expr='year',
        label='Birth year'
    )
    
    birth_after = filters.DateFilter(
        field_name='birth_date',
        lookup_expr='gte',
        label='Born after'
    )
    
    birth_before = filters.DateFilter(
        field_name='birth_date',
        lookup_expr='lte',
        label='Born before'
    )
    
    # Custom method filters
    has_published_books = filters.BooleanFilter(
        method='filter_has_published_books',
        label='Has published books'
    )
    
    min_books = filters.NumberFilter(
        method='filter_min_books',
        label='Minimum books count'
    )
    
    def filter_has_published_books(self, queryset, name, value):
        """
        Filter authors who have published books
        """
        if value:
            return queryset.filter(books__published=True).distinct()
        return queryset.filter(books__published=False).distinct()
    
    def filter_min_books(self, queryset, name, value):
        """
        Filter authors with minimum number of books
        """
        return queryset.annotate(
            book_count=Count('books')
        ).filter(book_count__gte=value)
    
    class Meta:
        model = Author
        fields = []


# ==================== GENRE FILTERS ====================

class GenreFilter(filters.FilterSet):
    """
    Genre FilterSet
    
    Filters:
    - name: Genre nomi (icontains)
    - min_books: Minimal kitoblar soni
    
    Examples:
    /api/genres/?name=programming
    /api/genres/?min_books=5
    """
    
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Name contains'
    )
    
    min_books = filters.NumberFilter(
        method='filter_min_books',
        label='Minimum books count'
    )
    
    def filter_min_books(self, queryset, name, value):
        """
        Filter genres with minimum number of books
        """
        return queryset.annotate(
            book_count=Count('books')
        ).filter(book_count__gte=value)
    
    class Meta:
        model = Genre
        fields = []