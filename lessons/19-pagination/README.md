# 19 - Pagination

## Maqsad

Ushbu darsda biz Django REST Framework'da **pagination** (sahifalash) funksiyalarini o'rganamiz. Katta ma'lumotlar to'plamini kichik qismlarga bo'lib, samarali qaytarish usullarini bilib olamiz.

---

## Nima uchun Pagination kerak?

### Muammolar pagination'siz:

1. **Performance** - 10,000 ta kitobni bir vaqtda qaytarish sekin
2. **Memory** - Server va client xotirasi to'lib ketishi mumkin
3. **Network** - Katta response hajmi, sekin yuklash
4. **User Experience** - Foydalanuvchi 10,000 ta yozuvni ko'ra olmaydi

### Pagination bilan:

✅ Faqat 10-20-50 ta yozuv qaytariladi
✅ Tezkor yuklash
✅ Kam xotira
✅ Yaxshi UX

---

## DRF'da Pagination turlari

1. **PageNumberPagination** - Sahifa raqamlari (1, 2, 3...)
2. **LimitOffsetPagination** - Limit va offset (SQL LIMIT, OFFSET)
3. **CursorPagination** - Cursor-based (katta dataset uchun)
4. **Custom Pagination** - O'z pagination'ingizni yaratish

---

## 1. PageNumberPagination

Eng oddiy va ko'p ishlatiladigan pagination turi.

### Default configuration:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

### Foydalanish:

```
GET /api/books/                # Birinchi sahifa (1-10)
GET /api/books/?page=2         # Ikkinchi sahifa (11-20)
GET /api/books/?page=3         # Uchinchi sahifa (21-30)
```

### Response format:

```json
{
    "count": 100,
    "next": "http://localhost:8000/api/books/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Django Guide",
            "price": "29.99"
        },
        // ... 9 more items
    ]
}
```

### Custom PageNumberPagination:

```python
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  # ?page_size=20
    max_page_size = 100
```

**View:**
```python
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination
```

**Usage:**
```
GET /api/books/?page=2
GET /api/books/?page=2&page_size=20
GET /api/books/?page_size=50
```

---

## 2. LimitOffsetPagination

SQL LIMIT va OFFSET kabi ishlaydi.

### Configuration:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}
```

### Foydalanish:

```
GET /api/books/?limit=10                # Birinchi 10 ta
GET /api/books/?limit=10&offset=10      # 11-20
GET /api/books/?limit=10&offset=20      # 21-30
```

### Response format:

```json
{
    "count": 100,
    "next": "http://localhost:8000/api/books/?limit=10&offset=10",
    "previous": null,
    "results": [...]
}
```

### Custom LimitOffsetPagination:

```python
from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
```

**Usage:**
```
GET /api/books/?limit=20
GET /api/books/?limit=50&offset=100
```

---

## 3. CursorPagination

Katta dataset'lar uchun eng yaxshi variant. Cursor-based pagination.

### Afzalliklari:

- ✅ Juda tez (katta ma'lumotlar uchun)
- ✅ Consistent results (yangi ma'lumot qo'shilsa ham to'g'ri ishlaydi)
- ✅ Forward/backward navigation

### Kamchiliklari:

- ❌ Aniq sahifaga o'tib bo'lmaydi (page=5 yo'q)
- ❌ Faqat ordering field bo'yicha ishlaydi

### Configuration:

```python
from rest_framework.pagination import CursorPagination

class BookCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'  # Majburiy field
```

### Foydalanish:

```
GET /api/books/                                    # Birinchi 10 ta
GET /api/books/?cursor=cD0yMDI0LTAxLTE1            # Keyingi 10 ta
GET /api/books/?cursor=cj0xJnA9MjAyNC0wMS0xNA==    # Oldingi 10 ta
```

### Response format:

```json
{
    "next": "http://localhost:8000/api/books/?cursor=cD0yMDI0...",
    "previous": null,
    "results": [...]
}
```

**Muhim:** Cursor qiymatini o'zingiz yaratish kerak emas, DRF avtomatik generatsiya qiladi.

---

## 4. Custom Pagination

O'z pagination class'ingizni yaratish.

### Misol: Custom response format

```python
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'total': self.page.paginator.count,
                'page': self.page.number,
                'pages': self.page.paginator.num_pages,
                'page_size': self.page_size,
            },
            'data': data
        })
```

**Response:**
```json
{
    "pagination": {
        "total": 100,
        "page": 1,
        "pages": 10,
        "page_size": 10
    },
    "data": [...]
}
```

---

## View-level Pagination

Har bir view uchun alohida pagination:

```python
from rest_framework.pagination import PageNumberPagination

class SmallResultsSetPagination(PageNumberPagination):
    page_size = 5

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = SmallResultsSetPagination

class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = LargeResultsSetPagination
```

---

## Pagination'ni o'chirish

Ba'zi endpoint'lar uchun pagination kerak bo'lmasligi mumkin:

```python
class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = None  # Pagination o'chirildi
```

---

## Pagination + Filtering/Searching

Pagination filtering va searching bilan birga ishlaydi:

```python
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Filtering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['price', 'published_date']
    
    # Pagination
    pagination_class = StandardResultsSetPagination
```

**Usage:**
```
GET /api/books/?search=django&page=2
GET /api/books/?author=1&page_size=20
GET /api/books/?ordering=price&limit=50&offset=100
```

---

## Performance Tips

### 1. Count'ni optimize qilish:

Default pagination har safar `COUNT(*)` query qiladi. Katta dataset'larda bu sekin.

```python
class OptimizedPagination(PageNumberPagination):
    page_size = 10
    
    def get_paginated_response(self, data):
        # Count'ni faqat birinchi sahifada hisoblash
        if self.page.number == 1:
            count = self.page.paginator.count
        else:
            count = None  # Yoki cache'dan olish
        
        return Response({
            'count': count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
```

### 2. select_related / prefetch_related:

```python
def get_queryset(self):
    return Book.objects.select_related('author').prefetch_related('genres')
```

### 3. Database indexes:

Ordering field'ga index qo'shing:

```python
class Book(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
```

---

## Qachon qaysi pagination'ni ishlatish?

| Pagination Type | Qachon ishlatish |
|----------------|------------------|
| **PageNumberPagination** | Standart web UI, admin panel |
| **LimitOffsetPagination** | SQL-ga o'xshash API, flexible pagination |
| **CursorPagination** | Real-time feeds, infinite scroll, katta dataset |
| **Custom** | Maxsus requirements |

---

## Real World Example

```python
# pagination.py
from rest_framework.pagination import PageNumberPagination, CursorPagination

class StandardPagination(PageNumberPagination):
    """Standard pagination - 10 items per page"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class LargePagination(PageNumberPagination):
    """Large pagination - 50 items per page"""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200

class FeedPagination(CursorPagination):
    """Cursor pagination for feeds"""
    page_size = 20
    ordering = '-created_at'

# views.py
class BookListView(generics.ListAPIView):
    queryset = Book.objects.select_related('author').prefetch_related('genres')
    serializer_class = BookListSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter

class BookFeedView(generics.ListAPIView):
    """Real-time book feed"""
    queryset = Book.objects.filter(published=True)
    serializer_class = BookListSerializer
    pagination_class = FeedPagination
```

---

## Swagger Integration

Pagination parametrlari avtomatik Swagger'da ko'rinadi:

**PageNumberPagination:**
- `page` (query, integer)
- `page_size` (query, integer) - agar `page_size_query_param` sozlangan bo'lsa

**LimitOffsetPagination:**
- `limit` (query, integer)
- `offset` (query, integer)

**CursorPagination:**
- `cursor` (query, string)

---

## Xulosa

### Best Practices:

1. ✅ Har doim pagination ishlatish (katta dataset'lar uchun)
2. ✅ Sensible default `page_size` tanlash (10-50)
3. ✅ `max_page_size` limitini qo'yish
4. ✅ Performance uchun optimize qilish
5. ✅ User experience uchun to'g'ri pagination turini tanlash

### Common Mistakes:

1. ❌ Pagination'siz katta dataset qaytarish
2. ❌ `max_page_size` yo'q (user 10000 so'rashi mumkin)
3. ❌ Count query har safar (performance issue)
4. ❌ Noto'g'ri pagination turi tanlash

---

## Keyingi Dars

20-darsda biz **Throttling & Rate Limiting** mavzusini o'rganamiz va API'ni abuse'dan himoya qilishni bilib olamiz.

---

## Resurslar

- [DRF Pagination](https://www.django-rest-framework.org/api-guide/pagination/)
- [Cursor Pagination Guide](https://www.django-rest-framework.org/api-guide/pagination/#cursorpagination)
- [Performance Tips](https://www.django-rest-framework.org/api-guide/pagination/#modifying-the-pagination-style)