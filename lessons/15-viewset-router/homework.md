# 15-Dars: ViewSet va Router - Uy Vazifasi

## Maqsad
ViewSet va Router konsepsiyalarini mustahkamlash va amaliy qo'llash.

---

## Vazifa 1: Author ViewSet yaratish
**Qiyinlik:** Oson

### Topshiriq:
1. `accounts` app'ida `Author` modeli yarating:
```python
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.user.username
```

2. `AuthorSerializer` yarating
3. `AuthorViewSet` yarating (ModelViewSet)
4. Router orqali URL'larni ulang

### Tekshirish:
- `GET /api/authors/` - barcha authorlar
- `POST /api/authors/` - yangi author yaratish
- `GET /api/authors/{id}/` - bitta author

---

## Vazifa 2: Custom Actions
**Qiyinlik:** O'rta

### Topshiriq:
`BookViewSet`ga quyidagi custom action'larni qo'shing:

1. **search** (detail=False, GET)
   - URL: `/api/books/search/?q=django`
   - Query parameter orqali kitob izlash
   
2. **top_rated** (detail=False, GET)
   - URL: `/api/books/top_rated/`
   - Eng yuqori baholangan 5 ta kitob
   
3. **set_price** (detail=True, POST)
   - URL: `/api/books/{id}/set_price/`
   - Kitob narxini o'zgartirish
   - Request body: `{"price": 25.99}`

### Tekshirish:
- Har bir endpoint ishlashini test qiling
- Postman yoki browsable API'dan test qiling

---

## Vazifa 3: ReadOnly ViewSet
**Qiyinlik:** O'rta

### Topshiriq:
1. `PublicBookViewSet` yarating (ReadOnlyModelViewSet)
2. Faqat published kitoblarni ko'rsatsin
3. Alohida router yarating va `/api/public/` prefix bilan ulang

### Talablar:
```python
class PublicBookViewSet(viewsets.ReadOnlyModelViewSet):
    # Faqat published kitoblar
    # Hech qanday permission kerak emas
    # GET operatsiyalari faqat
```

### Tekshirish:
- `GET /api/public/books/` - ishlaydi
- `POST /api/public/books/` - 405 Method Not Allowed

---

## Vazifa 4: Multiple Routers
**Qiyinlik:** Qiyin

### Topshiriq:
Ikki xil API versiyasini yarating:

**Version 1:**
- URL: `/api/v1/books/`
- Barcha kitoblar
- To'liq CRUD

**Version 2:**
- URL: `/api/v2/books/`
- Faqat published kitoblar
- ReadOnly

### Kod:
```python
# v1 router
router_v1 = DefaultRouter()
router_v1.register(r'books', BookViewSet)

# v2 router
router_v2 = DefaultRouter()
router_v2.register(r'books', PublicBookViewSet)

# urls.py
urlpatterns = [
    path('api/v1/', include(router_v1.urls)),
    path('api/v2/', include(router_v2.urls)),
]
```

---

## Vazifa 5: Custom Action with Serializer
**Qiyinlik:** Qiyin

### Topshiriq:
Kitobga review qo'shish uchun action yarating:

1. `Review` modeli:
```python
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

2. `ReviewSerializer` yarating

3. Custom action:
```python
@action(detail=True, methods=['post'])
def add_review(self, request, pk=None):
    # Review qo'shish logikasi
    pass
```

### Tekshirish:
```bash
POST /api/books/1/add_review/
{
    "rating": 5,
    "comment": "Ajoyib kitob!"
}
```

---

## Bonus Vazifa: Statistics Dashboard
**Qiyinlik:** Juda qiyin

### Topshiriq:
Admin uchun statistics endpoint yarating:

```python
@action(detail=False, 
        methods=['get'],
        permission_classes=[IsAdminUser])
def dashboard(self, request):
    return Response({
        'total_books': ...,
        'published_books': ...,
        'total_authors': ...,
        'total_reviews': ...,
        'average_rating': ...,
        'books_by_month': [...],  # Last 6 months
    })
```

---

## Topshirish
1. Barcha kod ishlaydigan bo'lishi kerak
2. Postman collection yoki screenshot'lar
3. GitHub'ga push qiling
4. README.md'ga endpoint'lar ro'yxatini qo'shing

---

## Yordam
Agar qiyinchilik tug'ilsa:
1. DRF documentation: https://www.django-rest-framework.org/api-guide/viewsets/
2. Darsda keltirilgan misollar
3. `examples/` papkasidagi kod namunalar

**Omad!**