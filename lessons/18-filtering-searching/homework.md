# Homework: Filtering & Searching

## Maqsad

Ushbu vazifada siz API'ga **filtering**, **searching**, va **ordering** funksiyalarini qo'shasiz va turli xil filtrlash metodlarini o'rganasiz.

---

## Vazifa 1: Basic Search Filter

### Topshiriq

1. `BookListView` ga **SearchFilter** qo'shing
2. Quyidagi fieldlar bo'yicha qidirish:
   - `title` - kitob nomi ichida
   - `subtitle` - subtitle ichida
   - `author__name` - muallif nomi ichida
   - `publisher` - nashriyot ichida

### Kod:

```python
from rest_framework.filters import SearchFilter

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'subtitle', 'author__name', 'publisher']
```

### Test:

```
GET /api/books/?search=django
GET /api/books/?search=john doe
GET /api/books/?search=python guide
```

### Kutilgan natija:

Qidiruv so'zi mavjud barcha kitoblar ro'yxati.

---

## Vazifa 2: Ordering Filter

### Topshiriq

1. `BookListView` ga **OrderingFilter** qo'shing
2. Quyidagi fieldlar bo'yicha tartiblash:
   - `price` - narx bo'yicha
   - `published_date` - nashr sanasi bo'yicha
   - `title` - nom bo'yicha
   - `pages` - sahifalar soni bo'yicha

3. Default ordering: `-published_date` (yangilaridan eskisiga)

### Kod:

```python
from rest_framework.filters import OrderingFilter

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['price', 'published_date', 'title', 'pages']
    ordering = ['-published_date']
```

### Test:

```
GET /api/books/?ordering=price
GET /api/books/?ordering=-price
GET /api/books/?ordering=title
GET /api/books/?ordering=-published_date,price
```

### Kutilgan natija:

Kitoblar belgilangan tartibda qaytadi.

---

## Vazifa 3: Django Filter Backend

### Topshiriq

1. `django-filter` ni o'rnating:
```bash
pipenv install django-filter
```

2. `settings.py` ga qo'shing:
```python
INSTALLED_APPS = [
    ...
    'django_filters',
]
```

3. `books/filters.py` fayli yarating:

```python
from django_filters import rest_framework as filters
from .models import Book

class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_pages = filters.NumberFilter(field_name='pages', lookup_expr='gte')
    max_pages = filters.NumberFilter(field_name='pages', lookup_expr='lte')
    published_year = filters.NumberFilter(field_name='published_date', lookup_expr='year')
    published_after = filters.DateFilter(field_name='published_date', lookup_expr='gte')
    published_before = filters.DateFilter(field_name='published_date', lookup_expr='lte')
    
    class Meta:
        model = Book
        fields = ['author', 'published', 'language']
```

4. `BookListView` ni yangilang:

```python
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
```

### Test:

```
GET /api/books/?author=1
GET /api/books/?published=true
GET /api/books/?min_price=20&max_price=50
GET /api/books/?published_year=2024
GET /api/books/?language=English&published=true
```

### Kutilgan natija:

Barcha filterlar ishlaydi va to'g'ri natija qaytaradi.

---

## Vazifa 4: Combined Filters

### Topshiriq

Barcha filterlarni birga qo'shing: **DjangoFilter**, **SearchFilter**, **OrderingFilter**

```python
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter

class BookListView(generics.ListAPIView):
    queryset = Book.objects.select_related('author').prefetch_related('genres')
    serializer_class = BookListSerializer
    
    # Barcha filter backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # DjangoFilter
    filterset_class = BookFilter
    
    # SearchFilter
    search_fields = ['title', 'subtitle', 'author__name', 'publisher']
    
    # OrderingFilter
    ordering_fields = ['price', 'published_date', 'title', 'pages']
    ordering = ['-published_date']
```

### Test:

Murakkab query'lar:

```
GET /api/books/?author=1&search=django&ordering=-price
GET /api/books/?min_price=20&max_price=50&search=python&ordering=title
GET /api/books/?published_year=2024&published=true&language=English&ordering=-published_date
GET /api/books/?search=guide&min_price=25&ordering=price
```

### Kutilgan natija:

Barcha filterlar birga ishlaydi va to'g'ri natija qaytaradi.

---

## Bonus Vazifa 1: Author Filter

### Topshiriq

`AuthorListView` uchun ham filtering qo'shing:

1. Search: `name`, `email`, `bio` bo'yicha
2. Ordering: `name`, `birth_date`, `created_at` bo'yicha
3. Filter: `books__published` (published kitoblari bor mualliflar)

```python
class AuthorFilter(filters.FilterSet):
    has_published_books = filters.BooleanFilter(
        field_name='books__published',
        lookup_expr='exact'
    )
    min_books = filters.NumberFilter(
        method='filter_min_books'
    )
    
    def filter_min_books(self, queryset, name, value):
        from django.db.models import Count
        return queryset.annotate(
            book_count=Count('books')
        ).filter(book_count__gte=value)
    
    class Meta:
        model = Author
        fields = []

class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AuthorFilter
    search_fields = ['name', 'email', 'bio']
    ordering_fields = ['name', 'birth_date', 'created_at']
    ordering = ['name']
```

### Test:

```
GET /api/authors/?search=john
GET /api/authors/?has_published_books=true
GET /api/authors/?min_books=2
GET /api/authors/?ordering=birth_date
```

---

## Bonus Vazifa 2: Custom Filter Backend

### Topshiriq

Custom filter yarating - faqat user'ning o'z kitoblarini ko'rsatish:

```python
from rest_framework import filters

class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Faqat authenticated user'ning o'z kitoblarini qaytarish
    """
    def filter_queryset(self, request, queryset, view):
        # Anonymous userlar uchun faqat published
        if not request.user.is_authenticated:
            return queryset.filter(published=True)
        
        # Staff userlar uchun hamma kitoblar
        if request.user.is_staff:
            return queryset
        
        # Oddiy user uchun o'z kitoblari + published kitoblar
        return queryset.filter(
            models.Q(owner=request.user) | models.Q(published=True)
        )

# My Books View
class MyBooksView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [IsOwnerFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'subtitle']
    ordering_fields = ['created_at', 'price']
```

### Test:

```
GET /api/my-books/
GET /api/my-books/?search=django
GET /api/my-books/?ordering=-created_at
```

---

## Topshirish

1. Barcha kodingizni Git'ga commit qiling:
```bash
git add .
git commit -m "feat: add filtering and searching functionality"
git push origin lesson-18
```

2. Pull Request yarating:
   - Title: `Lesson 18: Filtering & Searching`
   - Description: Qanday o'zgarishlar kiritganingizni yozing

3. **screenshots** papkasiga quyidagi rasmlarni qo'shing:
   - Search filter natijasi (Postman/Browser)
   - Ordering filter natijasi
   - Combined filters natijasi
   - Swagger UI'da filter parametrlari

---

## Muhim Eslatmalar

1. Barcha filterlar Swagger UI'da ko'rinishi kerak
2. Performance uchun `select_related` va `prefetch_related` ishlatishing
3. Filter fieldlarni ehtiyotkorlik bilan tanlang
4. Har bir filter uchun test yozing
5. Code style'ga e'tibor bering (PEP 8)

---

## Yordam Kerak Bo'lsa

- [DRF Filtering Docs](https://www.django-rest-framework.org/api-guide/filtering/)
- [Django Filter Docs](https://django-filter.readthedocs.io/)
- `examples` papkasidagi kod misollarni ko'ring

**Omad!**