# Lesson 22: Query Optimization in Django REST Framework

## Maqsad
Ushbu darsda Django va DRF'da ma'lumotlar bazasi so'rovlarini optimizatsiya qilish texnikalarini o'rganamiz. Bu API performance'ini sezilarli darajada oshiradi va server yukini kamaytiradi.

## Mavzular

### 1. N+1 Problem nima?

N+1 muammosi - bu ma'lumotlar bazasiga ortiqcha so'rovlar yuborilishi natijasida yuzaga keladigan performance muammosi.

**Misol:**
```python
# Yomon yondashuv - N+1 problem
books = Book.objects.all()
for book in books:
    print(book.author.name)  # Har bir kitob uchun alohida query
```

Bu kodda:
- 1 ta query barcha kitoblarni olish uchun
- N ta query har bir kitobning muallifini olish uchun
- **Jami: 1 + N ta query** ❌

---

### 2. `select_related()` - Foreign Key Optimization

`select_related()` SQL JOIN ishlatib, bog'langan obyektlarni bitta query'da oladi.

**Qachon ishlatiladi:**
- ForeignKey relationships
- OneToOneField relationships

**Sintaksis:**
```python
# Yaxshi yondashuv
books = Book.objects.select_related('author').all()
for book in books:
    print(book.author.name)  # Qo'shimcha query yo'q!
```

**SQL taqqoslash:**
```sql
-- select_related() ishlatmasdan
SELECT * FROM books;
SELECT * FROM authors WHERE id = 1;
SELECT * FROM authors WHERE id = 2;
-- ... N ta query

-- select_related() bilan
SELECT * FROM books 
INNER JOIN authors ON books.author_id = authors.id;
-- Faqat 1 ta query! ✅
```

**Bir nechta relation:**
```python
Book.objects.select_related('author', 'publisher', 'category').all()
```

**Nested relationships:**
```python
Book.objects.select_related('author__country').all()
```

---

### 3. `prefetch_related()` - Many-to-Many Optimization

`prefetch_related()` alohida query'lar ishlatadi, lekin ularni Python'da birlashtiradi.

**Qachon ishlatiladi:**
- ManyToManyField relationships
- Reverse ForeignKey relationships

**Sintaksis:**
```python
# Yaxshi yondashuv
books = Book.objects.prefetch_related('genres').all()
for book in books:
    for genre in book.genres.all():  # Qo'shimcha query yo'q!
        print(genre.name)
```

**Farqi:**
```python
# select_related - JOIN ishlatadi (ForeignKey)
Book.objects.select_related('author')

# prefetch_related - Alohida query'lar (ManyToMany)
Book.objects.prefetch_related('genres')
```

**Kombinatsiyalash:**
```python
Book.objects.select_related('author').prefetch_related('genres')
```

---

### 4. `Prefetch` obyekti - Advanced Optimization

Custom queryset bilan prefetch qilish:

```python
from django.db.models import Prefetch

# Faqat active genrelarni olish
active_genres = Genre.objects.filter(is_active=True)

books = Book.objects.prefetch_related(
    Prefetch('genres', queryset=active_genres)
)
```

**Nested prefetch:**
```python
authors = Author.objects.prefetch_related(
    Prefetch(
        'books',
        queryset=Book.objects.select_related('publisher')
    )
)
```

---

### 5. Database Indexes

Index - ma'lumotlar bazasida qidiruv tezligini oshiruvchi struktura.

**Qachon kerak:**
- Tez-tez filter qilinadigan fieldlar
- Tez-tez ordering qilinadigan fieldlar
- Unique constraintlar

**Model'da index qo'shish:**
```python
class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    isbn = models.CharField(max_length=13, unique=True)  # Auto index
    published_date = models.DateField(db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['author', 'published_date']),
            models.Index(fields=['title', 'author']),
            models.Index(fields=['-published_date']),  # Descending
        ]
```

**Composite index (Multi-column):**
```python
class Meta:
    indexes = [
        models.Index(fields=['author', 'genre', 'published_date'], 
                     name='author_genre_date_idx'),
    ]
```

**Migration yaratish:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. DRF Serializer Optimization

**Setup method ishlatish:**
```python
class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author_name', 'genres']
    
    def setup_eager_loading(queryset):
        """Optimizatsiya qilingan queryset"""
        return queryset.select_related('author').prefetch_related('genres')
```

**View'da ishlatish:**
```python
class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        queryset = Book.objects.all()
        return BookSerializer.setup_eager_loading(queryset)
```

---

### 7. `only()` va `defer()` - Field Selection

**`only()` - Faqat kerakli fieldlarni olish:**
```python
# Faqat id, title va author fieldlari
Book.objects.only('id', 'title', 'author')
```

**`defer()` - Katta fieldlarni keyinroq yuklash:**
```python
# description fieldini keyinroq yuklash
Book.objects.defer('description')
```

**Qachon ishlatiladi:**
- Katta text fieldlar bo'lganda
- API'da barcha fieldlar kerak bo'lmaganda

---

### 8. `values()` va `values_list()` - Dictionary/Tuple Return

**`values()` - Dictionary qaytaradi:**
```python
books = Book.objects.values('id', 'title', 'author__name')
# [{'id': 1, 'title': '...', 'author__name': '...'}, ...]
```

**`values_list()` - Tuple qaytaradi:**
```python
books = Book.objects.values_list('id', 'title')
# [(1, 'Book 1'), (2, 'Book 2'), ...]

# Flat list (bitta field)
titles = Book.objects.values_list('title', flat=True)
# ['Book 1', 'Book 2', ...]
```

---

### 9. Query Optimization Best Practices

#### ✅ **DO (Qiling):**

1. **select_related() ForeignKey uchun:**
```python
Book.objects.select_related('author', 'publisher')
```

2. **prefetch_related() ManyToMany uchun:**
```python
Book.objects.prefetch_related('genres', 'tags')
```

3. **Index muhim fieldlarga:**
```python
class Meta:
    indexes = [models.Index(fields=['published_date'])]
```

4. **Filter before ordering:**
```python
Book.objects.filter(is_active=True).order_by('-created_at')
```

5. **Use exists() for boolean checks:**
```python
if Book.objects.filter(author=author).exists():
    # ...
```

6. **Use count() correctly:**
```python
# Yaxshi
count = Book.objects.count()

# Yomon
count = len(Book.objects.all())  # Barcha obyektlarni yuklaydi!
```

#### ❌ **DON'T (Qilmang):**

1. **Loop ichida query:**
```python
# Yomon
for book in books:
    author = Author.objects.get(id=book.author_id)
```

2. **Kerakli bo'lmagan fieldlarni yuklash:**
```python
# Yomon - barcha fieldlar yuklanadi
Book.objects.all()

# Yaxshi
Book.objects.only('id', 'title')
```

3. **Ortiqcha JOIN:**
```python
# Yomon - publisher kerak emas lekin yuklanadi
Book.objects.select_related('author', 'publisher').values('title', 'author__name')
```

---

### 10. Django Debug Toolbar - Query Monitoring

**O'rnatish:**
```bash
pip install django-debug-toolbar
```

**settings.py:**
```python
INSTALLED_APPS = [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']
```

**urls.py:**
```python
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

**Foydalanish:**
- Brauzerda toolbar paydo bo'ladi
- "SQL" bo'limida barcha query'larni ko'rish mumkin
- Duplicate query'larni aniqlash
- Query vaqtini tekshirish

---

### 11. Amaliy Misol - Optimizatsiya Before/After

**Before (Yomon) ❌:**
```python
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()  # N+1 problem!
    serializer_class = BookSerializer

# Result: 1 + N + M ta query (N=authors, M=genres)
```

**After (Yaxshi) ✅:**
```python
class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        return Book.objects.select_related(
            'author', 'publisher'
        ).prefetch_related(
            'genres', 'reviews'
        ).filter(
            is_active=True
        ).order_by('-published_date')

# Result: Faqat 3 ta query!
# 1. Books + JOIN authors, publishers
# 2. Genres (prefetch)
# 3. Reviews (prefetch)
```

---

### 12. ViewSet uchun Optimization Mixin

```python
class OptimizedQuerysetMixin:
    """Queryset optimization uchun reusable mixin"""
    
    select_related_fields = []
    prefetch_related_fields = []
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        if self.select_related_fields:
            queryset = queryset.select_related(*self.select_related_fields)
        
        if self.prefetch_related_fields:
            queryset = queryset.prefetch_related(*self.prefetch_related_fields)
        
        return queryset


class BookViewSet(OptimizedQuerysetMixin, viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    select_related_fields = ['author', 'publisher']
    prefetch_related_fields = ['genres', 'reviews']
```

---

## Performance Comparison

### Test Setup:
- 1000 ta kitob
- Har bir kitobning 1 ta muallifi
- Har bir kitobning 3 ta janri

### Results:

| Yondashuv | Query Count | Time |
|-----------|-------------|------|
| Optimizatsiyasiz | 3001 query | 5.2s ❌ |
| select_related() | 1001 query | 2.1s ⚠️ |
| + prefetch_related() | 2 query | 0.3s ✅ |
| + Indexes | 2 query | 0.15s 🚀 |

---

## Xulosa

1. **N+1 problem** - Eng keng tarqalgan performance muammosi
2. **select_related()** - ForeignKey uchun JOIN
3. **prefetch_related()** - ManyToMany uchun alohida query'lar
4. **Database indexes** - Qidiruv tezligini oshiradi
5. **Django Debug Toolbar** - Query'larni monitoring qilish
6. **Best practices** - Filter, exists(), count() to'g'ri ishlatish

## Keyingi dars
**Lesson 23: Caching Strategies** - Redis, cache decorators, cache invalidation

---

## Foydali havolalar
- [Django Database Optimization](https://docs.djangoproject.com/en/stable/topics/db/optimization/)
- [DRF Performance Best Practices](https://www.django-rest-framework.org/topics/performance/)
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)
- [Database Indexes Explained](https://docs.djangoproject.com/en/stable/ref/models/indexes/)