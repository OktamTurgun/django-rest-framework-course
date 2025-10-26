# Lesson 06: Generic Views - Uyga Vazifa

## 🎯 Maqsad

Generic Views'ni amalda qo'llash va Library project'ni to'liq Generic Views'ga o'tkazish.

---

## 📋 Vazifa 1: Library Project'ni Generic Views'ga o'tkazish (Majburiy)

### ✅ 1.1 - Function-based views'ni o'chirish

**Vazifa:** `books/views.py` faylida barcha function-based views'ni o'chiring va Generic Views bilan almashtiring.

**Qadamlar:**
1. `@api_view` decorator'li barcha funksiyalarni o'chiring
2. 2 ta Generic View yarating:
   - `BookListCreateView` - List + Create
   - `BookRetrieveUpdateDestroyView` - Retrieve + Update + Destroy

**Natija:**
```python
# books/views.py (yangi)

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

---

### ✅ 1.2 - URLs'ni yangilash

**Vazifa:** `books/urls.py`'ni yangi views'lar bilan yangilang.

**Qadamlar:**
1. Import'larni yangilang: function'lar o'rniga class'lar
2. `.as_view()` qo'shing

**Natija:**
```python
# books/urls.py (yangi)

from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDestroyView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
]
```

---

### ✅ 1.3 - Pagination qo'shish

**Vazifa:** Custom pagination class yarating va `BookListCreateView`'ga qo'shing.

**Qadamlar:**
1. `BookPagination` class yarating
2. `page_size = 10` qo'ying
3. `page_size_query_param` va `max_page_size` qo'shing
4. `BookListCreateView`'ga `pagination_class` qo'shing

**Natija:**
```python
from rest_framework.pagination import PageNumberPagination

class BookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination  # ← Qo'shildi
```

**Test:**
- `http://localhost:8000/books/available/`

---

### ✅ 2.2 - Expensive Books View

**Vazifa:** Narxi 100,000 so'mdan yuqori kitoblarni ko'rsatadigan view yarating.

**Kod:**
```python
class ExpensiveBooksView(generics.ListAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        return Book.objects.filter(price__gt=100000)
```

**URL:**
```python
path('books/expensive/', ExpensiveBooksView.as_view(), name='book-expensive'),
```

**Test:**
- `http://localhost:8000/books/expensive/`

---

### ✅ 2.3 - Books by Author View

**Vazifa:** Muallif nomi bo'yicha kitoblarni ko'rsatadigan view yarating (URL parameter).

**Kod:**
```python
class BooksByAuthorView(generics.ListAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        author = self.kwargs.get('author')
        return Book.objects.filter(author__icontains=author)
```

**URL:**
```python
path('books/by-author/<str:author>/', BooksByAuthorView.as_view(), name='books-by-author'),
```

**Test:**
- `http://localhost:8000/books/by-author/Alisher/`
- `http://localhost:8000/books/by-author/Navoiy/`

---

## 📋 Vazifa 3: Advanced Filtering (Qo'shimcha - Ixtiyoriy)

### ✅ 3.1 - Advanced Filter View yaratish

**Vazifa:** Query parameters orqali murakkab filtering qilish.

**Kod:**
```python
class BookAdvancedFilterView(generics.ListAPIView):
    serializer_class = BookSerializer
    pagination_class = BookPagination
    
    def get_queryset(self):
        queryset = Book.objects.all()
        
        # Available filter
        available = self.request.query_params.get('available')
        if available and available.lower() == 'true':
            queryset = queryset.filter(available=True)
        
        # Minimum price
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        # Maximum price
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Author filter
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author__icontains=author)
        
        return queryset
```

**URL:**
```python
path('books/filter/', BookAdvancedFilterView.as_view(), name='book-filter'),
```

**Test:**
- `http://localhost:8000/books/filter/?available=true`
- `http://localhost:8000/books/filter/?min_price=50000&max_price=150000`
- `http://localhost:8000/books/filter/?author=Alisher&available=true`

---

### ✅ 3.2 - DjangoFilterBackend qo'shish

**Vazifa:** `django-filter` paketini o'rnatib, DjangoFilterBackend qo'shing.

**Qadamlar:**
```bash
# 1. Install
pipenv install django-filter

# 2. settings.py'ga qo'shish
INSTALLED_APPS = [
    ...
    'django_filters',
]

# 3. views.py'da ishlatish
from django_filters.rest_framework import DjangoFilterBackend

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['available', 'author']
    search_fields = ['title', 'author', 'description']
    ordering_fields = ['price', 'publish_date', 'title']
    ordering = ['-publish_date']
```

**Test:**
- `http://localhost:8000/books/?available=true`
- `http://localhost:8000/books/?author=Alisher`
- `http://localhost:8000/books/?available=true&search=django&ordering=-price`

---

## 📋 Vazifa 4: New Project - Author Management (Qo'shimcha - Ixtiyoriy)

**Vazifa:** Yangi `Author` modeli yaratib, uchun Generic Views yozish.

### ✅ 4.1 - Author modelini yaratish

**Kod:**
```python
# books/models.py

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Book modeliga ForeignKey qo'shish
class Book(models.Model):
    # ... existing fields ...
    author_model = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books', null=True, blank=True)
```

**Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### ✅ 4.2 - Author Serializer yaratish

**Kod:**
```python
# books/serializers.py

class AuthorSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'bio', 'birth_date', 'website', 'books_count']
    
    def get_books_count(self, obj):
        return obj.books.count()
```

---

### ✅ 4.3 - Author Views yaratish

**Kod:**
```python
# books/views.py

class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'bio']
    ordering_fields = ['first_name', 'last_name', 'birth_date']

class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
```

---

### ✅ 4.4 - Author URLs

**Kod:**
```python
# books/urls.py

urlpatterns = [
    # ... existing book URLs ...
    
    # Author URLs
    path('authors/', AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', AuthorRetrieveUpdateDestroyView.as_view(), name='author-detail'),
]
```

**Test:**
- `GET /authors/` - Barcha mualliflar
- `POST /authors/` - Yangi muallif
- `GET /authors/1/` - Bitta muallif
- `PUT /authors/1/` - Muallifni yangilash
- `DELETE /authors/1/` - Muallifni o'chirish

---

### ✅ 4.5 - Author'ning kitoblarini ko'rsatish

**Vazifa:** Ma'lum bir muallif yozgan barcha kitoblarni ko'rsatish.

**Kod:**
```python
class AuthorBooksView(generics.ListAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        author_id = self.kwargs.get('pk')
        return Book.objects.filter(author_model_id=author_id)
```

**URL:**
```python
path('authors/<int:pk>/books/', AuthorBooksView.as_view(), name='author-books'),
```

**Test:**
- `http://localhost:8000/authors/1/books/`

---

## 📋 Vazifa 5: Testing (Qo'shimcha - Ixtiyoriy)

### ✅ 5.1 - Manual testing Postman'da

**Vazifa:** Barcha endpoint'larni Postman'da test qiling.

**Test qilish kerak:**
1. ✅ GET /books/ - Pagination test
2. ✅ POST /books/ - Yangi kitob yaratish
3. ✅ GET /books/1/ - Bitta kitob
4. ✅ PUT /books/1/ - To'liq yangilash
5. ✅ PATCH /books/1/ - Qisman yangilash
6. ✅ DELETE /books/1/ - O'chirish
7. ✅ GET /books/?search=django - Qidirish
8. ✅ GET /books/?ordering=-price - Tartiblash
9. ✅ GET /books/available/ - Custom view
10. ✅ GET /books/filter/?min_price=50000 - Advanced filter

---

### ✅ 5.2 - Automated tests yozish

**Vazifa:** `books/tests.py`'da test yozish.

**Kod:**
```python
# books/tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book

class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            price=50000,
            available=True
        )
    
    def test_get_books_list(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_book(self):
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'price': 75000,
            'available': True
        }
        response = self.client.post('/books/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_single_book(self):
        response = self.client.get(f'/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
    
    def test_update_book(self):
        data = {'title': 'Updated Book'}
        response = self.client.patch(f'/books/{self.book.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book')
    
    def test_delete_book(self):
        response = self.client.delete(f'/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_search_books(self):
        response = self.client.get('/books/?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_ordering_books(self):
        response = self.client.get('/books/?ordering=-price')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

**Test ishga tushirish:**
```bash
python manage.py test
```

---

## 📊 Topshirish formati

### 1. GitHub Repository

**Qadamlar:**
```bash
# 1. Barcha o'zgarishlarni commit qiling
git add .
git commit -m "Complete Lesson 06: Generic Views homework

- Converted function-based views to Generic Views
- Added pagination (10 items per page)
- Added search and ordering filters
- Created custom views (AvailableBooksView, ExpensiveBooksView)
- Added advanced filtering
- Created Author model and views (optional)
- Added tests (optional)"

# 2. GitHub'ga push qiling
git push origin lesson-06
```

---

### 2. Skrinshotlar

**Kerakli skrinshotlar:**
1. ✅ `/books/` - Pagination bilan
2. ✅ `/books/?search=django` - Search natijasi
3. ✅ `/books/?ordering=-price` - Ordering natijasi
4. ✅ `/books/1/` - Bitta kitob
5. ✅ `/books/available/` - Custom view
6. ✅ Postman'da POST request (yangi kitob yaratish)

---

### 3. Kod review

**Tekshirish kerak:**
- ✅ Function-based views o'chirilgan
- ✅ Generic Views to'g'ri ishlayapti
- ✅ Pagination qo'shilgan
- ✅ Search va Ordering ishlayapti
- ✅ Custom views yaratilgan
- ✅ Kod tozalangan va comment'lar yozilgan

---

## ✅ Baholash mezonlari

### Majburiy qism (100 ball)

| Vazifa | Ball |
|--------|------|
| Function-based views → Generic Views | 30 |
| Pagination qo'shish | 15 |
| Search va Ordering | 20 |
| Custom views (Available, Expensive, ByAuthor) | 25 |
| Test qilish va skrinshotlar | 10 |

### Qo'shimcha qism (50 ball)

| Vazifa | Ball |
|--------|------|
| Advanced filtering | 15 |
| DjangoFilterBackend | 10 |
| Author Management System | 20 |
| Automated tests | 5 |

**Jami:** 150 ball

---

## 🎯 Muvaffaqiyat mezonlari

### ⭐ Minimum (60 ball)
- Function-based views Generic Views'ga o'tkazilgan
- Pagination ishlaydi
- Search va Ordering qo'shilgan

### ⭐⭐ O'rtacha (80 ball)
- Minimum + Custom views yaratilgan
- Code clean va tushunarliroq

### ⭐⭐⭐ Yaxshi (100 ball)
- O'rtacha + Advanced filtering
- DjangoFilterBackend qo'shilgan

### ⭐⭐⭐⭐ A'lo (120+ ball)
- Yaxshi + Author Management
- Automated tests yozilgan
- Kod professional darajada

---

## 💡 Maslahatlar

1. ✅ **Ketma-ket bajaring** - Birinchi 1-vazifa, keyin 2-vazifa
2. ✅ **Har bir qadamni test qiling** - Kod yozgandan keyin darhol test qiling
3. ✅ **README.md'ni o'qing** - Barcha tushuntirish u yerda
4. ✅ **examples/ papkasiga qarang** - Tayyor kod misollar bor
5. ✅ **Git commit qiling** - Har bir vazifadan keyin commit qiling
6. ✅ **Comment yozing** - Kodingizga izoh qo'shing
7. ✅ **DRY principle** - Kod takrorlanmasin
8. ✅ **Error handling** - Generic Views avtomatik qiladi, lekin tekshiring

---

## ❓ Savollar?

Agar qiyinchilik yuzaga kelsa:
1. ✅ README.md'ni qayta o'qing
2. ✅ examples/ papkasidagi kodlarni ko'ring
3. ✅ code/library-project'dagi tayyor kodga qarang
4. ✅ Telegram guruhida savol bering

---

## 📅 Topshirish muddati

**Muddat:** Darsdan keyin **7 kun**

**Topshirish:**
1. GitHub'da PR yarating
2. Skrinshotlarni Telegram'ga yuboring
3. Link yuboring

---

**Good luck! 🚀**

Keyingi dars: **Lesson 07 - Postman, Swagger, Redoc (Testing & Documentation)**
- `http://localhost:8000/books/?page=1`
- `http://localhost:8000/books/?page=2&page_size=5`

---

### ✅ 1.4 - Search va Ordering qo'shish

**Vazifa:** `BookListCreateView`'ga qidirish va tartiblash qo'shing.

**Qadamlar:**
1. `filter_backends` qo'shing: `SearchFilter` va `OrderingFilter`
2. `search_fields` qo'shing: `title`, `author`, `description`
3. `ordering_fields` qo'shing: `price`, `publish_date`, `title`
4. `ordering` qo'shing: default ordering

**Natija:**
```python
from rest_framework import generics, filters

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'description']
    ordering_fields = ['price', 'publish_date', 'title']
    ordering = ['-publish_date']  # Yangi kitoblar birinchi
```

**Test:**
- `http://localhost:8000/books/?search=django`
- `http://localhost:8000/books/?ordering=-price`
- `http://localhost:8000/books/?search=python&ordering=price`

---

### ✅ 1.5 - Server'ni ishga tushirish va test qilish

**Vazifa:** Barcha endpoint'lar ishlayotganini tekshiring.

**Qadamlar:**
```bash
python manage.py runserver
```

**Test:**
1. ✅ `GET /books/` - Ro'yxat (pagination bilan)
2. ✅ `POST /books/` - Yangi kitob yaratish
3. ✅ `GET /books/1/` - Bitta kitob
4. ✅ `PUT /books/1/` - To'liq yangilash
5. ✅ `PATCH /books/1/` - Qisman yangilash
6. ✅ `DELETE /books/1/` - O'chirish
7. ✅ `GET /books/?search=django` - Qidirish
8. ✅ `GET /books/?ordering=-price` - Tartiblash
9. ✅ `GET /books/?page=2` - Pagination

---

## 📋 Vazifa 2: Custom Views yaratish (Majburiy)

### ✅ 2.1 - Available Books View

**Vazifa:** Faqat mavjud kitoblarni ko'rsatadigan view yarating.

**Kod:**
```python
class AvailableBooksView(generics.ListAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        return Book.objects.filter(available=True)
```

**URL:**
```python
path('books/available/', AvailableBooksView.as_view(), name='book-available'),
```

**Test:**