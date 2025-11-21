# Examples: Pagination

Ushbu papkada **Pagination** mavzusi bo'yicha amaliy misollar keltirilgan.

---

## Fayllar

### 1. `01-page-number-pagination.py`
- PageNumberPagination (eng oddiy)
- Custom page size
- Different page sizes for different views
- Pagination + filters
- Best practices va testing

**Qachon ishlatish:**
- Standard web UI
- Admin panels
- Page numbers kerak bo'lsa

### 2. `02-limit-offset-pagination.py`
- LimitOffsetPagination (SQL-style)
- Custom limits
- Batch processing
- Range-based pagination
- Advantages & disadvantages

**Qachon ishlatish:**
- Data export
- SQL-like API
- Flexible pagination kerak

### 3. `03-cursor-pagination.py`
- CursorPagination (most efficient)
- Real-time feeds
- Infinite scroll
- Bidirectional navigation
- Performance comparison

**Qachon ishlatish:**
- Large datasets (100K+)
- Social media feeds
- Real-time updates
- Performance critical

### 4. `04-custom-pagination.py`
- Custom response formats
- Metadata pagination
- Header-based pagination
- Lazy count optimization
- GraphQL-style pagination
- Pagination class factory

**Qachon ishlatish:**
- Custom requirements
- Specific response format kerak
- Advanced use cases

---

## Qanday ishlatish

Har bir faylda to'liq ishlaydigan kod misollari keltirilgan. Ularni o'z projectingizga copy-paste qilishingiz mumkin:

```python
# pagination.py ga qo'shing
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# views.py da ishlating
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = StandardPagination
```

---

## Pagination Turlari Qiyoslash

| Type | URL Format | Best For | Performance |
|------|------------|----------|-------------|
| PageNumber | `?page=2` | UI, page numbers | Good |
| LimitOffset | `?limit=10&offset=20` | SQL-like, export | Degrades with offset |
| Cursor | `?cursor=xxx` | Feeds, infinite scroll | Excellent |
| Custom | Custom | Specific needs | Varies |

---

## Qo'shimcha resurslar

- [DRF Pagination Docs](https://www.django-rest-framework.org/api-guide/pagination/)
- [Performance Guide](https://www.django-rest-framework.org/api-guide/pagination/#modifying-the-pagination-style)