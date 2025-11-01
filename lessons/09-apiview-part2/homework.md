# 09-dars: Uyga vazifa

APIView bilan CRUD operatsiyalarini mustaqil bajaring.

## 🎯 Maqsad

Bitta obyekt bilan ishlashni mustaqil amalga oshirish:
- Detail view yaratish
- GET, PUT, PATCH, DELETE metodlarini qo'llash
- URL routing sozlash
- API'ni sinash

---

## 📝 Vazifa 1: Author Detail API (Asosiy)

Author modeli uchun detail API yarating.

### 1.1. Model (tayyor bo'lishi kerak)

```python
# books/models.py
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()
    birth_date = models.DateField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
```

### 1.2. Serializer yaratish

```python
# books/serializers.py
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
```

### 1.3. Detail View yaratish

`books/views.py` faylida yarating:

```python
class AuthorDetailAPIView(APIView):
    """
    Bitta muallifni olish, yangilash va o'chirish
    
    TODO:
    - get() metodini yozing
    - put() metodini yozing
    - patch() metodini yozing
    - delete() metodini yozing
    """
    
    def get(self, request, pk):
        # Muallifni oling va qaytaring
        pass
    
    def put(self, request, pk):
        # To'liq yangilang
        pass
    
    def patch(self, request, pk):
        # Qisman yangilang
        pass
    
    def delete(self, request, pk):
        # O'chiring
        pass
```

### 1.4. URL qo'shish

```python
# books/urls.py
urlpatterns = [
    # ... mavjud URL'lar
    path('authors/<int:pk>/', AuthorDetailAPIView.as_view(), name='author-detail'),
]
```

### ✅ Tekshirish

```bash
# 1. Muallifni olish
http GET http://127.0.0.1:8000/api/authors/1/

# 2. Bio'ni yangilash (PATCH)
http PATCH http://127.0.0.1:8000/api/authors/1/ bio="Yangi biografiya"

# 3. To'liq yangilash (PUT)
http PUT http://127.0.0.1:8000/api/authors/1/ \
  first_name="Alisher" \
  last_name="Navoiy" \
  bio="O'zbek shoiri" \
  birth_date="1441-02-09"

# 4. O'chirish
http DELETE http://127.0.0.1:8000/api/authors/1/
```

---

## 📝 Vazifa 2: Category Detail API (O'rta)

Kitob kategoriyalari uchun detail API yarating.

### 2.1. Model

```python
# books/models.py
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
```

### 2.2. Vazifalar

1. ✅ CategorySerializer yarating
2. ✅ CategoryDetailAPIView yarating (GET, PUT, PATCH, DELETE)
3. ✅ URL routing qo'shing
4. ✅ Postman/HTTPie orqali sinang

### ✅ Tekshirish kriteriylari

- [ ] GET - kategoriyani olish ishlaydi
- [ ] PUT - to'liq yangilash ishlaydi
- [ ] PATCH - qisman yangilash ishlaydi
- [ ] DELETE - o'chirish ishlaydi
- [ ] 404 xatolik to'g'ri qaytadi
- [ ] Validatsiya xatoliklari to'g'ri qaytadi

---

## 📝 Vazifa 3: BookReview Detail API (Qiyin)

Kitob sharhlari uchun detail API yarating.

### 3.1. Model

```python
# books/models.py
class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reviewer_name} - {self.book.title}"
```

### 3.2. Vazifalar

1. ✅ BookReviewSerializer yarating
2. ✅ BookReviewDetailAPIView yarating
3. ✅ URL routing qo'shing
4. ✅ Validatsiya qo'shing:
   - rating 1 dan 5 gacha bo'lishi kerak
   - comment bo'sh bo'lmasligi kerak
5. ✅ Sinab ko'ring

### 3.3. Qo'shimcha talablar

**Custom response qaytaring:**

```python
def delete(self, request, pk):
    review = get_object_or_404(BookReview, pk=pk)
    book_title = review.book.title
    reviewer = review.reviewer_name
    review.delete()
    
    return Response({
        "message": f"{reviewer} tomonidan {book_title} kitobiga yozilgan sharh o'chirildi",
        "deleted_at": timezone.now()
    }, status=status.HTTP_204_NO_CONTENT)
```

---

## 🎁 Bonus vazifalar (Ixtiyoriy)

### Bonus 1: Filtering
GET so'rovida filtering qo'shing:

```python
def get(self, request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    # Query parametrlarni olish
    include_reviews = request.query_params.get('include_reviews', 'false')
    
    if include_reviews.lower() == 'true':
        # Serializer'da reviews ham qaytarish
        pass
    
    serializer = BookSerializer(book)
    return Response(serializer.data)
```

### Bonus 2: Permissions
Faqat authenticated foydalanuvchilar yangilash va o'chirish qila olsin:

```python
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class BookDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # ...
```

### Bonus 3: Logging
Har bir amalda log yozish:

```python
import logging

logger = logging.getLogger(__name__)

class BookDetailAPIView(APIView):
    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        logger.info(f"Book '{book.title}' deleted by user")
        book.delete()
        return Response({"message": "Deleted"}, status=204)
```

---

## 📋 Topshirish formati

### 1. Kod fayllari
```
homework/
├── models.py          # Yangi modellar
├── serializers.py     # Serializer'lar
├── views.py           # APIView'lar
├── urls.py            # URL routing
└── README.md          # Qisqa tavsif
```

### 2. README.md namunasi

```markdown
# 09-dars Homework

## Bajarilgan vazifalar

- [x] Vazifa 1: Author Detail API
- [x] Vazifa 2: Category Detail API
- [x] Vazifa 3: BookReview Detail API
- [ ] Bonus 1: Filtering
- [ ] Bonus 2: Permissions
- [ ] Bonus 3: Logging

## Endpoint'lar

### Author API
- GET /api/authors/<id>/
- PUT /api/authors/<id>/
- PATCH /api/authors/<id>/
- DELETE /api/authors/<id>/

### Category API
- GET /api/categories/<id>/
- PUT /api/categories/<id>/
- PATCH /api/categories/<id>/
- DELETE /api/categories/<id>/

### BookReview API
- GET /api/reviews/<id>/
- PUT /api/reviews/<id>/
- PATCH /api/reviews/<id>/
- DELETE /api/reviews/<id>/

## Sinash misollari

(HTTPie yoki curl misollari)

## Qiyinchiliklar

(Qanday muammolarga duch keldingiz va qanday hal qildingiz)
```

### 3. Postman Collection (ixtiyoriy)
Export qiling va `postman_collection.json` sifatida qo'shing.

---

## ✅ Baholash mezonlari

| Mezon | Ball |
|-------|------|
| Vazifa 1 (Author API) | 40% |
| Vazifa 2 (Category API) | 30% |
| Vazifa 3 (BookReview API) | 30% |
| Bonus vazifalar | +10% har biri |
| Kod sifati va tartib | Majburiy |

### Kod sifati talablari:
- ✅ Tozalilik va tartib
- ✅ Izohlar mavjud
- ✅ DRY prinsipi (Don't Repeat Yourself)
- ✅ To'g'ri nomlar (variable, function)
- ✅ Error handling
- ✅ Validatsiya

---

## 🤔 Yordam kerakmi?

### Qayerdan boshlash kerakligini bilmayapsizmi?

1. `examples/detail_apiview_example.py` faylini o'qing
2. `code/library-project/books/views.py` dagi BookDetailAPIView ni ko'ring
3. Shuni Author uchun takrorlang

### Xatolarga duch kelayapsizmi?

**404 Error:**
```python
# get_object_or_404 ishlatganingizni tekshiring
author = get_object_or_404(Author, pk=pk)
```

**Validation Error:**
```python
# partial parametrini to'g'ri o'rnatganingizni tekshiring
serializer = AuthorSerializer(author, data=request.data, partial=True)  # PATCH uchun
```

**Import Error:**
```python
# Nisbiy import ishlatganingizni tekshiring
from .models import Author  # To'g'ri
# from books.models import Author  # Ham ishlaydi
```

---

## 📅 Topshirish muddati

**Deadline:** Keyingi darsdan oldin

**Format:** GitHub repository yoki ZIP fayl

**Eslatma:** Kechiktirilgan topshiriqlar 50% ball olib tashlanadi.

---

## 🎯 Muvaffaqiyat tilaymiz!

Agar savollar bo'lsa, o'qituvchidan so'rang. Happy coding! 🚀