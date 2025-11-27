# Homework: Query Optimization

## Maqsad
Mavjud library project'da query optimization texnikalarini qo'llash va performance'ini o'lchash.

---

## Topshiriq 1: N+1 Problem Detection (20 ball)

### 1.1 Django Debug Toolbar o'rnatish
```bash
pip install django-debug-toolbar
```

**settings.py** ga qo'shing:
```python
INSTALLED_APPS = [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']
```

**urls.py** ga qo'shing:
```python
from django.conf import settings

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

### 1.2 N+1 Problem aniqlash

**Test qilish:**
1. Server ishga tushiring
2. `/api/books/` endpoint'iga kiring
3. Debug Toolbar'da "SQL" bo'limini oching
4. Nechta query bo'lganini yozing

**Natijalar:**
- [ ] Screenshot oling (query count ko'rinsin)
- [ ] Duplicate query'lar borligini tekshiring
- [ ] N+1 problem bor yoki yo'qligini aniqlang

---

## Topshiriq 2: select_related() Implementation (25 ball)

### 2.1 Book Model Optimization

**books/views/book_views.py** da:
```python
class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        # TODO: select_related() qo'shing
        # Author va publisher fieldlarini optimize qiling
        return Book.objects.all()
```

**Talablar:**
- [ ] `author` relation uchun select_related()
- [ ] `publisher` relation uchun select_related() (agar bor bo'lsa)
- [ ] Query count kamaygani Debug Toolbar'da ko'rinsin

### 2.2 Serializer Optimization
```python
class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    # TODO: Qo'shimcha author ma'lumotlari qo'shing
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author_name', ...]
```

**Talablar:**
- [ ] Author name, bio, birth_date kabi fieldlarni qo'shing
- [ ] Serializer'da additional query'lar paydo bo'lmasligi kerak

---

## Topshiriq 3: prefetch_related() Implementation (25 ball)

### 3.1 Genres Optimization
```python
class BookListView(generics.ListAPIView):
    def get_queryset(self):
        return Book.objects.select_related('author').prefetch_related(
            # TODO: genres va boshqa ManyToMany fieldlarni qo'shing
        )
```

### 3.2 Reviews Optimization

Agar `Review` model bo'lsa:
```python
class BookDetailView(generics.RetrieveAPIView):
    def get_queryset(self):
        return Book.objects.select_related(
            'author'
        ).prefetch_related(
            'genres',
            # TODO: reviews va boshqa related fieldlarni qo'shing
        )
```

**Talablar:**
- [ ] Barcha ManyToMany relationships optimize qilingan
- [ ] Nested serializer'larda qo'shimcha query yo'q
- [ ] Query count minimal darajaga tushgan

---

## Topshiriq 4: Database Indexes (15 ball)

### 4.1 Book Model'ga index qo'shish
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13)
    
    class Meta:
        indexes = [
            # TODO: Index'lar qo'shing
        ]
```

**Qo'shish kerak bo'lgan indexlar:**
- [ ] `published_date` field (filtering uchun)
- [ ] `title` field (search uchun)
- [ ] `author` + `published_date` composite index
- [ ] `is_active` field (agar bor bo'lsa)

### 4.2 Migration yaratish
```bash
python manage.py makemigrations
python manage.py migrate
```

**Tekshirish:**
```sql
-- SQLite uchun
.schema books_book

-- PostgreSQL uchun
\d books_book
```

**Screenshot:**
- [ ] Migration fayli
- [ ] Database schema (indexlar ko'rinsin)

---

## Topshiriq 5: Optimization Mixin (15 ball)

### 5.1 Reusable Mixin yaratish

**books/mixins.py** (yangi fayl):
```python
class QueryOptimizationMixin:
    """
    ViewSet'lar uchun query optimization mixin
    """
    select_related_fields = []
    prefetch_related_fields = []
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # TODO: Implement optimization logic
        
        return queryset
```

### 5.2 ViewSet'larda ishlatish
```python
class BookViewSet(QueryOptimizationMixin, viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    select_related_fields = ['author', 'publisher']
    prefetch_related_fields = ['genres']
```

**Talablar:**
- [ ] Mixin barcha ViewSet'larda ishlashi kerak
- [ ] DRY principle'ga rioya qilingan
- [ ] Kodni reuse qilish oson

---

## Topshiriq 6: Performance Testing (Bonus 20 ball)

### 6.1 Test Script yozish

**performance_test.py** yarating:
```python
import time
import requests

def test_query_performance(url, iterations=10):
    """
    API endpoint performance test
    """
    times = []
    
    for _ in range(iterations):
        start = time.time()
        response = requests.get(url)
        end = time.time()
        times.append(end - start)
    
    avg_time = sum(times) / len(times)
    print(f"Average response time: {avg_time:.3f}s")
    return avg_time

# Test optimizatsiyasiz
# TODO: Implement tests
```

### 6.2 Before/After Comparison

**Natijalarni yozing:**
```markdown
## Performance Results

### Before Optimization:
- Query Count: ___
- Response Time: ___s
- Memory Usage: ___MB

### After Optimization:
- Query Count: ___
- Response Time: ___s
- Memory Usage: ___MB

### Improvement:
- Query Count: -___%
- Response Time: -___%
- Memory Usage: -___%
```

**Talablar:**
- [ ] 100+ ta kitob bilan test qilish
- [ ] Debug Toolbar screenshot'lari
- [ ] Performance comparison table
- [ ] Conclusion yozish

---

## Topshiriq 7: Advanced Optimization (Bonus 20 ball)

### 7.1 Custom Prefetch
```python
from django.db.models import Prefetch

class BookViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # TODO: Faqat active genrelarni prefetch qiling
        active_genres = Genre.objects.filter(is_active=True)
        
        return Book.objects.prefetch_related(
            Prefetch('genres', queryset=active_genres)
        )
```

### 7.2 Serializer Setup Method
```python
class BookSerializer(serializers.ModelSerializer):
    @staticmethod
    def setup_eager_loading(queryset):
        """
        Optimization setup method
        """
        # TODO: Implement
        return queryset
```

**Talablar:**
- [ ] Custom prefetch to'g'ri ishlaydi
- [ ] Serializer setup method reusable
- [ ] Documentation yaxshi yozilgan

---

## Topshiriq 8: Documentation (Bonus 10 ball)

### 8.1 README.md yaratish

**OPTIMIZATION.md** fayl yarating:
```markdown
# Query Optimization Documentation

## Overview
Bu loyihada qo'llangan optimization texnikalari

## Implemented Optimizations

### 1. select_related()
- Used for: ...
- Fields: ...
- Result: ...

### 2. prefetch_related()
- Used for: ...
- Fields: ...
- Result: ...

### 3. Database Indexes
- Indexed fields: ...
- Reasons: ...

## Performance Metrics
[Before/After comparison]

## Future Improvements
- ...
```

---

## Baholash Mezoni

| Topshiriq | Ball | Talab |
|-----------|------|-------|
| N+1 Detection | 20 | Debug Toolbar, screenshots |
| select_related() | 25 | To'g'ri implementation |
| prefetch_related() | 25 | ManyToMany optimization |
| Database Indexes | 15 | Migration, schema |
| Optimization Mixin | 15 | Reusable mixin |
| **Jami** | **100** | |
| Performance Testing | +20 | Bonus |
| Advanced Optimization | +20 | Bonus |
| Documentation | +10 | Bonus |
| **Maksimal** | **150** | |

---

## Topshirish

### Format:
```
homework/
├── screenshots/
│   ├── before-optimization.png
│   ├── after-optimization.png
│   └── debug-toolbar.png
├── code/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── mixins.py
├── OPTIMIZATION.md
└── performance_test.py
```

### GitHub:
- Branch nomi: `homework/lesson-22-optimization`
- Pull Request yarating
- README'da screenshot'lar bo'lishi kerak

---

## Deadline
**7 kun ichida topshiring**

## Qo'shimcha resurslar
- Django Debug Toolbar docs
- Django QuerySet API reference
- DRF Performance guide

**Good luck!**