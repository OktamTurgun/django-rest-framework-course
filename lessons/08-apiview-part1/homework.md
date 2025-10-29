# Uy vazifasi - APIView Part 1

## Maqsad

APIView bilan CRUD operatsiyalarni mustaqil ravishda amalga oshirish va HTTP metodlari hamda status kodlar bilan to'g'ri ishlashni o'rganish.

---

## 📋 Vazifalar

### Vazifa 1: Author API yaratish (Boshlang'ich daraja)

Mualliflar uchun to'liq CRUD API yarating.

#### 1.1. Model yaratish

```python
# books/models.py da Author modelini yarating
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
```

#### 1.2. Serializer yaratish

```python
# books/serializers.py da AuthorSerializer yarating
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
```

#### 1.3. APIView yozish

**a) Author ro'yxati va yaratish:**

```python
class AuthorListCreateView(APIView):
    def get(self, request):
        """Barcha mualliflarni olish"""
        # Bu yerda kod yozing
        pass
    
    def post(self, request):
        """Yangi muallif yaratish"""
        # Bu yerda kod yozing
        pass
```

**b) Author detallarini boshqarish:**

```python
class AuthorDetailView(APIView):
    def get(self, request, pk):
        """Bitta muallifni olish"""
        # Bu yerda kod yozing
        pass
    
    def put(self, request, pk):
        """Muallifni to'liq yangilash"""
        # Bu yerda kod yozing
        pass
    
    def delete(self, request, pk):
        """Muallifni o'chirish"""
        # Bu yerda kod yozing
        pass
```

#### 1.4. URLs sozlash

```python
# books/urls.py
urlpatterns = [
    # ... mavjud URLlar
    path('authors/', AuthorListCreateView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]
```

#### Tekshirish:

- [ ] Barcha mualliflarni ko'rish mumkin
- [ ] Yangi muallif yaratish mumkin
- [ ] Bitta muallifni ko'rish mumkin
- [ ] Muallifni yangilash mumkin
- [ ] Muallifni o'chirish mumkin
- [ ] To'g'ri status kodlar qaytariladi

---

### Vazifa 2: Book-Author bog'lash (O'rta daraja)

Book modeliga Author maydonini qo'shing va APIni yangilang.

#### 2.1. Book modelini yangilash

```python
# books/models.py
class Book(models.Model):
    # Mavjud maydonlar...
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
```

#### 2.2. Serializer yangilash

```python
class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author.first_name',
        read_only=True
    )
    
    class Meta:
        model = Book
        fields = '__all__'
```

#### 2.3. APIView yaratish

Muallif kitoblarini ko'rsatadigan endpoint yarating:

```python
class AuthorBooksView(APIView):
    """
    Muallif barcha kitoblarini olish
    GET /api/authors/1/books/
    """
    def get(self, request, pk):
        # Bu yerda kod yozing
        pass
```

#### Tekshirish:

- [ ] Kitob yaratishda muallif ID kiritish mumkin
- [ ] Kitob ma'lumotlarida muallif nomi ko'rinadi
- [ ] Muallif barcha kitoblarini ko'rish mumkin

---

### Vazifa 3: Custom filterlash (Yuqori daraja)

Kitoblarni turli parametrlar bo'yicha filterlash imkoniyatini qo'shing.

#### 3.1. BookSearchView yaratish

```python
class BookSearchView(APIView):
    """
    Kitoblarni qidirish
    GET /api/books/search/?title=django&author=1&min_price=10&max_price=100
    """
    def get(self, request):
        books = Book.objects.all()
        
        # Query parametrlarni olish
        title = request.query_params.get('title')
        author_id = request.query_params.get('author')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        
        # Filterlash logikasini yozing
        # Maslahat: if title: books = books.filter(title__icontains=title)
        
        # Natijani qaytaring
        pass
```

#### Tekshirish:

- [ ] Kitob nomini qidirib topish mumkin
- [ ] Muallif bo'yicha filterlash mumkin
- [ ] Narx oralig'i bo'yicha filterlash mumkin
- [ ] Bir nechta filtrni birga ishlatish mumkin
- [ ] Agar parametr berilmasa, barcha kitoblar qaytadi

---

### Vazifa 4: Statistika API (Bonus)

Kitoblar va mualliflar statistikasini ko'rsatadigan API yarating.

```python
class BookStatsView(APIView):
    """
    Kitoblar statistikasi
    GET /api/books/stats/
    """
    def get(self, request):
        stats = {
            'total_books': Book.objects.count(),
            'total_authors': Author.objects.count(),
            'avg_price': Book.objects.aggregate(Avg('price'))['price__avg'],
            'most_expensive': Book.objects.order_by('-price').first(),
            'cheapest': Book.objects.order_by('price').first(),
        }
        
        # Serializer kerak bo'lishi mumkin
        return Response(stats)
```

#### Tekshirish:

- [ ] Jami kitoblar soni ko'rinadi
- [ ] Jami mualliflar soni ko'rinadi
- [ ] O'rtacha narx hisoblanadi
- [ ] Eng qimmat kitob ma'lumoti qaytadi
- [ ] Eng arzon kitob ma'lumoti qaytadi

---

## 🧪 Test qilish

### Postman orqali test qilish:

1. **Author yaratish:**
```json
POST http://127.0.0.1:8000/api/authors/
Content-Type: application/json

{
    "first_name": "Abdulla",
    "last_name": "Qodiriy",
    "bio": "O'zbek yozuvchisi",
    "birth_date": "1894-06-10"
}
```

2. **Mualliflarni olish:**
```
GET http://127.0.0.1:8000/api/authors/
```

3. **Kitob qidirish:**
```
GET http://127.0.0.1:8000/api/books/search/?title=django&min_price=10
```

4. **Statistika:**
```
GET http://127.0.0.1:8000/api/books/stats/
```

---

## Topshirish talablari

### Minimum talablar:

1. ✅ Vazifa 1 to'liq bajarilgan
2. ✅ Vazifa 2 to'liq bajarilgan
3. ✅ Barcha endpointlar ishlaydi
4. ✅ To'g'ri status kodlar qaytariladi
5. ✅ Migration fayllar yaratilgan va qo'llanilgan

### Qo'shimcha ball uchun:

1. ✅ Vazifa 3 bajarilgan (filterlash)
2. ✅ Vazifa 4 bajarilgan (statistika)
3. ✅ Xatolarni to'g'ri qaytarish
4. ✅ Kod toza va tushunarli
5. ✅ Commentlar yozilgan

---

## Maslahatlar

### 1. get_object_or_404 dan foydalaning

```python
from django.shortcuts import get_object_or_404

def get(self, request, pk):
    author = get_object_or_404(Author, pk=pk)
    # Agar topilmasa, avtomatik 404 qaytaradi
```

### 2. Validation xatolarini qaytaring

```python
if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
else:
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### 3. Try-except ishlatish

```python
try:
    author = Author.objects.get(pk=pk)
except Author.DoesNotExist:
    return Response(
        {'error': 'Muallif topilmadi'},
        status=status.HTTP_404_NOT_FOUND
    )
```

### 4. Query parametrlarni tekshirish

```python
price = request.query_params.get('price')
if price and price.isdigit():
    books = books.filter(price=int(price))
```

---

## Savol-javob

### Savol: APIView va GenericView qachon ishlatiladi?

**Javob:**
- **GenericView** - oddiy CRUD operatsiyalar uchun (tez va oson)
- **APIView** - murakkab logika va maxsus xatti-harakatlar uchun (to'liq nazorat)

### Savol: partial=True nima qiladi?

**Javob:**
PATCH metodi bilan faqat bir nechta maydonlarni yangilash imkonini beradi:

```python
serializer = BookSerializer(book, data=request.data, partial=True)
```

### Savol: many=True nima uchun kerak?

**Javob:**
Bir nechta obyektlarni serialize qilish uchun:

```python
books = Book.objects.all()
serializer = BookSerializer(books, many=True)  # Ro'yxat uchun
```

---

## 🎓 Baholash mezonlari

| Mezon | Ball |
|-------|------|
| Vazifa 1 to'liq bajarilgan | 40 |
| Vazifa 2 to'liq bajarilgan | 30 |
| Vazifa 3 bajarilgan | 15 |
| Vazifa 4 bajarilgan | 10 |
| Kod sifati va tartib | 5 |
| **Jami** | **100** |

---

## Topshirish muddati

Darsdan keyin **3 kun** ichida topshiring.

## Yordam

Agar qiynalsangiz, quyidagi manbalardan foydalaning:

1. Dars materiali (`README.md`)
2. Examples papkadagi misollar
3. [DRF Documentation](https://www.django-rest-framework.org/)

---

**Omad yor bo'lsin!**