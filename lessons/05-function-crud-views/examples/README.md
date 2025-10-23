# Examples - Function-based Views

> Bu papkada turli xil advanced misollar mavjud.

---

## 📁 Fayllar

| Fayl | Tavsif | Qiyinlik |
|------|---------|----------|
| `filtering_example.py` | Filterlash, qidiruv, sorting, pagination | ⭐⭐⭐ |
| `validation_example.py` | Field-level, object-level, custom validation | ⭐⭐⭐ |
| `error_handling_example.py` | Try-except, custom errors, logging | ⭐⭐⭐⭐ |
| `partial_update_example.py` | PATCH, qisman yangilash, toggle | ⭐⭐⭐ |

---

## 🎯 Har bir fayldan nima o'rganish mumkin

### 1. filtering_example.py

**O'rganasiz:**
- Oddiy filterlash (bitta maydon)
- Ko'p maydonli filterlash
- Q object bilan murakkab qidiruv
- Sorting (tartiblash)
- Manual pagination
- Date range filter
- Complex filters

**Misol:**
```python
# Ko'p maydonli filterlash
GET /api/books/?author=John&language=English&available=true

# Narx oralig'i
GET /api/books/?min_price=20&max_price=50

# Qidiruv
GET /api/books/search/?q=python

# Sorting
GET /api/books/sorted/?order_by=-price

# Pagination
GET /api/books/paginated/?page=2&page_size=10
```

---

### 2. validation_example.py

**O'rganasiz:**
- Field-level validation (har bir maydon uchun)
- Object-level validation (bir nechta maydon birga)
- Custom validators
- Dynamic validation (context asosida)
- View'da qo'shimcha validation
- Error formatting

**Misol:**
```python
class BookSerializer(serializers.Serializer):
    title = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Juda qisqa")
        return value
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Musbat bo'lishi kerak")
        return value
    
    def validate(self, data):
        # Bir nechta maydonlarni birga tekshirish
        if data['price'] > 1000000 and len(data['title']) < 10:
            raise serializers.ValidationError("Logic error")
        return data
```

---

### 3. error_handling_example.py

**O'rganasiz:**
- Basic try-except
- get_object_or_404 usage
- Multiple exception handling
- Custom error messages
- Logging errors
- Detailed error responses
- Graceful degradation
- Transaction with rollback
- Custom exception classes
- Retry mechanism
- Error response helpers

**Misol:**
```python
@api_view(['POST'])
def safe_create(request):
    try:
        # ... kod
        return Response(data, status=201)
    
    except ValidationError as e:
        logger.warning(f'Validation error: {e}')
        return Response(
            {'error': 'Validation failed', 'details': str(e)},
            status=400
        )
    
    except IntegrityError:
        return Response(
            {'error': 'Unique constraint violation'},
            status=400
        )
    
    except Exception as e:
        logger.error(f'Unexpected error: {e}', exc_info=True)
        return Response(
            {'error': 'Server error'},
            status=500
        )
```

---

### 4. partial_update_example.py

**O'rganasiz:**
- Basic PATCH (partial update)
- PUT vs PATCH farqi
- Conditional updates (faqat muayyan maydonlar)
- Multiple fields update
- Nested partial updates
- Bulk partial updates
- Incremental updates (o'sish/kamayish)
- Toggle fields
- Timestamp updates
- Validated partial updates

**Misol:**
```python
# Faqat narxni yangilash
PATCH /api/books/1/
{
    "price": "49.99"
}

# Bir nechta maydon
PATCH /api/books/1/
{
    "price": "49.99",
    "is_available": false,
    "language": "Uzbek"
}

# Bulk update
PATCH /api/books/bulk/
{
    "ids": [1, 2, 3],
    "updates": {
        "is_available": false
    }
}

# Incremental
PATCH /api/books/1/increment/
{
    "price_increase": 10.00
}

# Toggle
PATCH /api/books/1/toggle/
{
    "field": "is_available"
}
```

---

## 🚀 Qanday ishlatish

### 1. Faylni ochish va nusxalash

Har bir faylda to'liq ishlaydigan kod mavjud. Views'larni o'z loyihangizga nusxalang:

```python
# books/views.py ga qo'shish
from .filtering_example import simple_filter, multiple_filters, advanced_search
from .validation_example import validate_book_data
from .error_handling_example import basic_error_handling
from .partial_update_example import basic_partial_update
```

### 2. URL'larni qo'shish

```python
# books/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Filtering
    path('filter/', views.simple_filter),
    path('filter/multiple/', views.multiple_filters),
    path('search/', views.advanced_search),
    path('sorted/', views.sorted_list),
    path('paginated/', views.paginated_list),
    
    # Validation
    path('validate/', views.validate_book_data),
    
    # Error handling
    path('<int:pk>/safe/', views.basic_error_handling),
    
    # Partial update
    path('<int:pk>/partial/', views.basic_partial_update),
    path('<int:pk>/toggle/', views.toggle_field),
]
```

### 3. Test qilish

Postman yoki cURL bilan test qiling:

```bash
# Filterlash
curl "http://localhost:8000/api/books/filter/?author=John&available=true"

# Qidiruv
curl "http://localhost:8000/api/books/search/?q=python"

# Partial update
curl -X PATCH http://localhost:8000/api/books/1/partial/ \
  -H "Content-Type: application/json" \
  -d '{"price": "49.99"}'

# Toggle
curl -X PATCH http://localhost:8000/api/books/1/toggle/ \
  -H "Content-Type: application/json" \
  -d '{"field": "is_available"}'
```

---

## 💡 O'rganish tartibi (Boshlang'ich → Murakkab)

### Level 1: Boshlang'ich ⭐
1. `filtering_example.py` - `simple_filter`
2. `filtering_example.py` - `multiple_filters`
3. `partial_update_example.py` - `basic_partial_update`

### Level 2: O'rta ⭐⭐
4. `filtering_example.py` - `advanced_search` (Q objects)
5. `filtering_example.py` - `sorted_list`
6. `validation_example.py` - Field-level validation
7. `partial_update_example.py` - `put_vs_patch`

### Level 3: Murakkab ⭐⭐⭐
8. `filtering_example.py` - `paginated_list`
9. `filtering_example.py` - `complex_filter`
10. `validation_example.py` - Object-level validation
11. `error_handling_example.py` - Multiple exceptions
12. `partial_update_example.py` - `bulk_partial_update`

### Level 4: Professional ⭐⭐⭐⭐
13. `validation_example.py` - Custom validators
14. `validation_example.py` - Dynamic validation
15. `error_handling_example.py` - Logging
16. `error_handling_example.py` - Transaction with rollback
17. `error_handling_example.py` - Custom exceptions
18. `partial_update_example.py` - `validated_partial_update`

---

## 🎓 Har bir misolni o'rganish yo'li

### 1. Kodni o'qing
- Funksiya nomini tushunib oling
- Docstring'ni o'qing
- Parametrlarni ko'ring

### 2. Test qiling
- Postman'da test qiling
- Turli input'lar bilan sinab ko'ring
- Xatolarni ko'ring va tushunib oling

### 3. O'zgartiring
- O'z loyihangizga moslashtiring
- Qo'shimcha logika qo'shing
- Yangi features yarating

### 4. Kombinatsiya qiling
- Bir nechta misollarni birlashtiring
- Murakkab funksiyalar yarating

---

## 📊 Har bir texnika qachon ishlatiladi

| Texnika | Qachon ishlatish | Misol |
|---------|------------------|-------|
| Simple Filter | Bitta maydon bo'yicha | `?author=John` |
| Multiple Filters | Bir nechta shart | `?author=John&price_min=20` |
| Q Objects | OR/NOT shartlar | Title YOKI Author |
| Sorting | Tartibda ko'rish | Arzondan qimmatga |
| Pagination | Ko'p ma'lumot | 1000+ kitoblar |
| Field Validation | Maydon to'g'riligini tekshirish | ISBN 13 raqam |
| Object Validation | Bir nechta maydon birga | Narx va Yil bog'liq |
| Custom Validators | Qayta ishlatish | ISBN validator |
| Try-Except | Xatolarni tutish | Database errors |
| Logging | Debug qilish | Production'da |
| Transaction | Atomik operatsiyalar | Bulk create |
| PATCH | Qisman yangilash | Faqat narx |
| PUT | To'liq yangilash | Barcha maydonlar |
| Toggle | Boolean o'zgartirish | is_available |
| Bulk Update | Ko'plab o'zgartirish | 100+ ta kitob |

---

## 🔥 Pro Tips

### 1. Filterlash uchun
```python
# ✅ Yaxshi
books = books.filter(author__icontains=author)  # Case-insensitive

# ❌ Yomon
books = [b for b in books if author in b.author]  # Slow, no DB optimization
```

### 2. Validation uchun
```python
# ✅ Yaxshi - Serializer'da
def validate_price(self, value):
    if value <= 0:
        raise serializers.ValidationError("Price must be positive")
    return value

# ❌ Yomon - View'da
if price <= 0:
    return Response({'error': 'Bad price'}, status=400)
```

### 3. Error handling uchun
```python
# ✅ Yaxshi - Specific exceptions
try:
    book.save()
except IntegrityError:
    return Response({'error': 'Duplicate ISBN'}, status=400)
except ValidationError as e:
    return Response({'error': str(e)}, status=400)

# ❌ Yomon - Generic catch
try:
    book.save()
except Exception as e:
    return Response({'error': str(e)}, status=500)
```

### 4. Partial update uchun
```python
# ✅ Yaxshi - partial=True
serializer = BookSerializer(book, data=request.data, partial=True)

# ❌ Yomon - partial=False (default)
serializer = BookSerializer(book, data=request.data)  # Requires all fields
```

---

## 🎯 Amaliy mashqlar

### Mashq 1: Murakkab filter yarating
Quyidagi filterlash imkoniyatini yarating:
- Price range: min va max
- Author bo'yicha qidiruv
- Language filtri
- Availability filtri
- Sorting: price, title, created_at
- Pagination: page, page_size

### Mashq 2: To'liq validation
Book uchun to'liq validatsiya qiling:
- Title: 3-200 belgi, unique
- ISBN: 13 raqam, unique, checksum
- Price: 0-10,000,000
- Pages: 1-10,000
- Published date: 1450-hozir

### Mashq 3: Error handling
Quyidagi xatolarni handle qiling:
- Book.DoesNotExist → 404
- ValidationError → 400 + details
- IntegrityError → 400 + message
- PermissionDenied → 403
- Exception → 500 + log

### Mashq 4: Advanced PATCH
Yarating:
- Single field update
- Multiple fields update
- Conditional update (faqat admin)
- Bulk update (ko'p kitoblar)
- Incremental update (price += 10)
- Toggle boolean fields

---

## 🔗 Qo'shimcha resurslar

- **Django ORM Queries:** https://docs.djangoproject.com/en/stable/topics/db/queries/
- **DRF Serializers:** https://www.django-rest-framework.org/api-guide/serializers/
- **DRF Validation:** https://www.django-rest-framework.org/api-guide/validators/
- **Python Logging:** https://docs.python.org/3/library/logging.html

---

## ❓ Savol-Javoblar

**Q: Qachon Q objects ishlataman?**  
A: OR, NOT yoki murakkab shartlar kerak bo'lganda.

**Q: partial=True qachon ishlatiladi?**  
A: PATCH metodida, faqat berilgan maydonlarni yangilash uchun.

**Q: Validation serializer'da yoki view'da?**  
A: Asosiy validation serializer'da, biznes logika view'da.

**Q: Xatolarni qanday log qilaman?**  
A: `import logging; logger = logging.getLogger(__name__)`

**Q: Bulk update'da xato bo'lsa?**  
A: Transaction ishlatib rollback qiling.

---

**Omad yor bo'lsin o'rganishda! 🚀**

Savollar bo'lsa, GitHub Issues'ga yozing yoki community'da so'rang.