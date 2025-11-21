# Homework: Pagination

## Maqsad

Ushbu vazifada siz API'ga **pagination** qo'shasiz va turli xil pagination turlarini amalda ishlatishni o'rganasiz.

---

## Vazifa 1: Standard PageNumberPagination

### Topshiriq

1. `books/pagination.py` faylini yarating

2. `StandardResultsSetPagination` class yarating:
```python
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
```

3. `BookListCreateView` ga pagination qo'shing:
```python
from books.pagination import StandardResultsSetPagination

class BookListCreateView(generics.ListCreateAPIView):
    ...
    pagination_class = StandardResultsSetPagination
```

### Test:

```
GET /api/books/                    # 1-10 kitoblar
GET /api/books/?page=2             # 11-20 kitoblar
GET /api/books/?page_size=20       # 20 ta kitob
GET /api/books/?page=2&page_size=5 # 2-chi sahifa, 5 ta
```

### Kutilgan Response:

```json
{
    "count": 100,
    "next": "http://localhost:8000/api/books/?page=2",
    "previous": null,
    "results": [
        // 10 ta kitob
    ]
}
```

---

## Vazifa 2: LimitOffsetPagination

### Topshiriq

1. `LargeResultsSetPagination` yarating:
```python
from rest_framework.pagination import LimitOffsetPagination

class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100
```

2. `AuthorListView` uchun ishlatish:
```python
class AuthorListView(generics.ListAPIView):
    ...
    pagination_class = LargeResultsSetPagination
```

### Test:

```
GET /api/authors/                      # Birinchi 20 ta
GET /api/authors/?limit=10             # Birinchi 10 ta
GET /api/authors/?limit=10&offset=10   # 11-20
GET /api/authors/?limit=50&offset=100  # 101-150
```

### Kutilgan Response:

```json
{
    "count": 150,
    "next": "http://localhost:8000/api/authors/?limit=20&offset=20",
    "previous": null,
    "results": [
        // 20 ta author
    ]
}
```

---

## Vazifa 3: CursorPagination

### Topshiriq

1. `BookFeedPagination` yarating:
```python
from rest_framework.pagination import CursorPagination

class BookFeedPagination(CursorPagination):
    page_size = 15
    ordering = '-created_at'
    cursor_query_param = 'cursor'
```

2. Yangi view yarating - `BookFeedView`:
```python
class BookFeedView(generics.ListAPIView):
    """
    Book feed - yangi qo'shilgan kitoblar
    Cursor pagination bilan
    """
    queryset = Book.objects.filter(published=True)
    serializer_class = BookListSerializer
    pagination_class = BookFeedPagination
    permission_classes = [AllowAny]
```

3. URL qo'shing:
```python
path('books/feed/', BookFeedView.as_view(), name='book-feed'),
```

### Test:

```
GET /api/books/feed/
GET /api/books/feed/?cursor=cD0yMDI0LTAxLTE1  # Next page
```

### Kutilgan Response:

```json
{
    "next": "http://localhost:8000/api/books/feed/?cursor=cD0yMDI0...",
    "previous": null,
    "results": [
        // 15 ta yangi kitob
    ]
}
```

---

## Vazifa 4: Custom Pagination

### Topshiriq

Custom pagination yarating - o'z response formatiz bilan:

```python
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('pagination', OrderedDict([
                ('total_items', self.page.paginator.count),
                ('total_pages', self.page.paginator.num_pages),
                ('current_page', self.page.number),
                ('page_size', len(data)),
                ('has_next', self.page.has_next()),
                ('has_previous', self.page.has_previous()),
            ])),
            ('links', OrderedDict([
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
            ])),
            ('data', data)
        ]))
```

### Test:

```
GET /api/books/?page=2&page_size=5
```

### Kutilgan Response:

```json
{
    "pagination": {
        "total_items": 100,
        "total_pages": 20,
        "current_page": 2,
        "page_size": 5,
        "has_next": true,
        "has_previous": true
    },
    "links": {
        "next": "http://localhost:8000/api/books/?page=3&page_size=5",
        "previous": "http://localhost:8000/api/books/?page=1&page_size=5"
    },
    "data": [
        // 5 ta kitob
    ]
}
```

---

## Bonus Vazifa 1: Pagination + Filtering

### Topshiriq

Pagination va filtering birga ishlatish:

```
GET /api/books/?search=django&page=2
GET /api/books/?author=1&page_size=20
GET /api/books/?min_price=20&ordering=price&page=3
```

### Test:

Barcha filter parametrlari pagination bilan ishlashi kerak.

### Kutilgan natija:

Filter qilingan natijalar to'g'ri sahifalangan.

---

## Bonus Vazifa 2: Pagination Class Factory

### Topshiriq

Pagination class factory yarating:

```python
def create_pagination_class(page_size=10, max_page_size=100):
    """
    Pagination class factory
    
    Usage:
    SmallPagination = create_pagination_class(page_size=5, max_page_size=50)
    """
    class DynamicPagination(PageNumberPagination):
        pass
    
    DynamicPagination.page_size = page_size
    DynamicPagination.page_size_query_param = 'page_size'
    DynamicPagination.max_page_size = max_page_size
    
    return DynamicPagination

# Usage
SmallPagination = create_pagination_class(page_size=5)
MediumPagination = create_pagination_class(page_size=25)
LargePagination = create_pagination_class(page_size=100)
```

### Test:

Turli xil page_size'lar bilan viewlar yaratish.

---

## Topshirish

1. Barcha kodingizni Git'ga commit qiling:
```bash
git add .
git commit -m "feat: add pagination functionality"
git push origin lesson-19
```

2. Pull Request yarating:
   - Title: `Lesson 19: Pagination`
   - Description: Qanday o'zgarishlar kiritganingizni yozing

3. **screenshots** papkasiga quyidagi rasmlarni qo'shing:
   - PageNumberPagination response (Postman/Browser)
   - LimitOffsetPagination response
   - CursorPagination response
   - Custom pagination response
   - Swagger UI'da pagination parametrlari

---

## Muhim Eslatmalar

1. **Performance:**
   - select_related va prefetch_related ishlatish
   - Database indexes
   - Count query optimization

2. **Testing:**
   - Barcha pagination turlarini test qiling
   - Edge cases (empty results, last page)
   - Large datasets

3. **Code Quality:**
   - DRY principle
   - Clear naming
   - Documentation
   - PEP 8

4. **User Experience:**
   - Sensible page_size defaults
   - max_page_size limits
   - Clear response format

---

## Test Scenariyalari

### Scenario 1: Empty Results
```
GET /api/books/?author=999&page=1
Expected: Empty array, count=0
```

### Scenario 2: Last Page
```
GET /api/books/?page=10&page_size=10
Expected: 
- count=100
- next=null
- previous exists
```

### Scenario 3: Invalid Page
```
GET /api/books/?page=999
Expected: 404 or empty results
```

### Scenario 4: Page Size Limit
```
GET /api/books/?page_size=1000
Expected: max_page_size enforced (100)
```

---

## Yordam Kerak Bo'lsa

- [DRF Pagination Docs](https://www.django-rest-framework.org/api-guide/pagination/)
- [PageNumberPagination](https://www.django-rest-framework.org/api-guide/pagination/#pagenumberpagination)
- [CursorPagination](https://www.django-rest-framework.org/api-guide/pagination/#cursorpagination)
- `examples` papkasidagi kod misollarni ko'ring

**Omad!**