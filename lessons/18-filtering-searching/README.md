# 18 - Filtering & Searching

## Maqsad

Ushbu darsda biz Django REST Framework'da **filtering**, **searching**, va **ordering** funksiyalarini o'rganamiz. Foydalanuvchilarga kerakli ma'lumotlarni tez va qulay topish imkonini beramiz.

---

## Nima o'rganamiz?

1. **Basic Filtering** - URL parametrlari bilan filtrlash
2. **SearchFilter** - Matn bo'yicha qidirish
3. **OrderingFilter** - Ma'lumotlarni tartiblash
4. **DjangoFilterBackend** - Murakkab filtrlash
5. **Custom Filters** - O'z filterlarimizni yaratish

---

## 1. Basic Filtering (Manual)

### Override `get_queryset()`

Eng oddiy usul - `get_queryset()` metodini override qilish:

```python
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        queryset = Book.objects.all()
        
        # URL parametrlarini olish
        author_id = self.request.query_params.get('author')
        published = self.request.query_params.get('published')
        
        # Filtrlash
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        if published:
            queryset = queryset.filter(published=published)
        
        return queryset
```

**Foydalanish:**
```
GET /api/books/?author=1
GET /api/books/?published=true
GET /api/books/?author=1&published=true
```

---

## 2. SearchFilter - Qidirish

DRF'da tayyor **SearchFilter** mavjud:

```python
from rest_framework import generics
from rest_framework.filters import SearchFilter
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'subtitle', 'author__name']
```

**Foydalanish:**
```
GET /api/books/?search=django
GET /api/books/?search=python guide
GET /api/books/?search=john
```

**Search operators:**
- `^` - Boshidan boshlanishi kerak: `search_fields = ['^title']`
- `=` - Aniq mos kelishi kerak: `search_fields = ['=isbn_number']`
- `@` - Full-text search (PostgreSQL): `search_fields = ['@description']`
- `$` - Regex search: `search_fields = ['$title']`

**Misol:**
```python
search_fields = [
    '^title',           # Title boshidan
    'subtitle',         # Subtitle ichida
    'author__name',     # Author nomi ichida
    '=isbn_number'      # ISBN aniq mos kelishi
]
```

---

## 3. OrderingFilter - Tartiblash

```python
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['price', 'published_date', 'title']
    ordering = ['-published_date']  # Default ordering
```

**Foydalanish:**
```
GET /api/books/?ordering=price          # Narx bo'yicha o'sish
GET /api/books/?ordering=-price         # Narx bo'yicha kamayish
GET /api/books/?ordering=title          # Nom bo'yicha A-Z
GET /api/books/?ordering=-published_date # Yangilaridan eskisiga
```

**Multiple ordering:**
```
GET /api/books/?ordering=-published_date,price
```

---

## 4. DjangoFilterBackend - Murakkab filtrlash

### O'rnatish:

```bash
pip install django-filter
```

### Settings.py ga qo'shish:

```python
INSTALLED_APPS = [
    ...
    'django_filters',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ]
}
```

### Oddiy foydalanish:

```python
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'published', 'language']
```

**Foydalanish:**
```
GET /api/books/?author=1
GET /api/books/?published=true
GET /api/books/?language=English
GET /api/books/?author=1&published=true
```

### Murakkab FilterSet:

```python
from django_filters import rest_framework as filters
from .models import Book

class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    published_year = filters.NumberFilter(field_name='published_date', lookup_expr='year')
    
    class Meta:
        model = Book
        fields = ['author', 'published', 'language']

# View
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
```

**Foydalanish:**
```
GET /api/books/?title=django
GET /api/books/?min_price=20&max_price=50
GET /api/books/?published_year=2024
GET /api/books/?author=1&min_price=30
```

---

## 5. Barcha filterlarni birga ishlatish

```python
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Barcha filterlar
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    
    # DjangoFilter
    filterset_class = BookFilter
    
    # SearchFilter
    search_fields = ['title', 'subtitle', 'author__name']
    
    # OrderingFilter
    ordering_fields = ['price', 'published_date', 'title']
    ordering = ['-published_date']
```

**Foydalanish:**
```
GET /api/books/?author=1&search=django&ordering=-price&min_price=20
```

---

## 6. Custom Filter

O'z filteringizni yaratish:

```python
from rest_framework import filters

class IsPublishedFilterBackend(filters.BaseFilterBackend):
    """
    Faqat published kitoblarni qaytarish
    """
    def filter_queryset(self, request, queryset, view):
        # Admin userlar uchun hamma kitoblar
        if request.user.is_staff:
            return queryset
        
        # Oddiy userlar uchun faqat published
        return queryset.filter(published=True)

# View
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [IsPublishedFilterBackend]
```

---

## 7. Real Misol: Library API

```python
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookListSerializer
from .filters import BookFilter

class BookListView(generics.ListAPIView):
    """
    Kitoblar ro'yxati - filtrlash, qidirish, tartiblash bilan
    
    Filters:
    - author: Author ID bo'yicha
    - published: True/False
    - language: Til bo'yicha
    - min_price: Minimal narx
    - max_price: Maksimal narx
    - published_year: Yil bo'yicha
    
    Search:
    - title, subtitle, author__name ichida qidirish
    
    Ordering:
    - price, published_date, title bo'yicha
    
    Examples:
    /api/books/?author=1&published=true
    /api/books/?search=django&ordering=-published_date
    /api/books/?min_price=20&max_price=50
    /api/books/?published_year=2024&language=English
    """
    queryset = Book.objects.select_related('author').prefetch_related('genres')
    serializer_class = BookListSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'subtitle', 'author__name', 'publisher']
    ordering_fields = ['price', 'published_date', 'title', 'pages']
    ordering = ['-published_date']
```

---

## Lookup Types (Django Filter)

```python
class BookFilter(filters.FilterSet):
    # Exact match
    isbn = filters.CharFilter(field_name='isbn_number', lookup_expr='exact')
    
    # Contains (case-insensitive)
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    
    # Greater than or equal
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    
    # Less than or equal
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    # Date range
    published_after = filters.DateFilter(field_name='published_date', lookup_expr='gte')
    published_before = filters.DateFilter(field_name='published_date', lookup_expr='lte')
    
    # Year
    published_year = filters.NumberFilter(field_name='published_date', lookup_expr='year')
    
    # In list
    authors = filters.ModelMultipleChoiceFilter(
        field_name='author',
        queryset=Author.objects.all()
    )
```

**Lookup expressions:**
- `exact` - Aniq mos kelish
- `iexact` - Case-insensitive exact
- `contains` - Ichida bor
- `icontains` - Case-insensitive contains
- `startswith` / `istartswith` - Boshidan boshlansa
- `endswith` / `iendswith` - Oxirida bo'lsa
- `gt` / `gte` - Greater than / Greater than or equal
- `lt` / `lte` - Less than / Less than or equal
- `year` / `month` / `day` - Date components

---

## Performance Tips

### 1. Indexlar qo'shish

```python
class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True)  # Index
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    published_date = models.DateField(db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['author', 'published']),
            models.Index(fields=['-published_date']),
        ]
```

### 2. select_related va prefetch_related

```python
def get_queryset(self):
    return Book.objects.select_related('author').prefetch_related('genres')
```

### 3. Count limitlash

```python
filter_backends = [DjangoFilterBackend]
filterset_fields = {
    'author': ['exact'],  # Faqat exact, in yo'q
}
```

---

## Xulosa

### Qachon qaysi usulni ishlatish?

| Usul | Qachon ishlatish |
|------|------------------|
| Manual `get_queryset()` | Oddiy, custom logic kerak bo'lsa |
| `SearchFilter` | Matn bo'yicha qidirish kerak bo'lsa |
| `OrderingFilter` | Tartiblash kerak bo'lsa |
| `DjangoFilterBackend` | Ko'p fieldlar bo'yicha filtrlash |
| Custom Filter | Murakkab business logic |

### Best Practices:

1. ✅ Performance uchun indexlar qo'shing
2. ✅ select_related/prefetch_related ishlatishing
3. ✅ Filter fieldlarni limitlang
4. ✅ Documentatsiya yozing (docstring)
5. ✅ Search fieldlarni ehtiyotkorlik bilan tanlang

---

## Keyingi Dars

19-darsda **Pagination** mavzusini o'rganamiz va API'da sahifalashni qo'shamiz.

---

## Resurslar

- [DRF Filtering](https://www.django-rest-framework.org/api-guide/filtering/)
- [Django Filter Documentation](https://django-filter.readthedocs.io/)
- [Search & Ordering](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)