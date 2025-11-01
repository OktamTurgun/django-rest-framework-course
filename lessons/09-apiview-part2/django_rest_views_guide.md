# Django REST Framework — View'lar bo'yicha to'liq qo'llanma

> **Maqsad:** Django REST Framework'dagi barcha view turlarini noldan professional darajagacha o'rganish

---

## 📑 Mundarija

1. [Django REST Framework nima?](#django-rest-framework-nima)
2. [Django'da View nima?](#djangoda-view-nima)
3. [DRF View'lar — turlari va darajalari](#drf-viewlar--turlari-va-darajalari)
4. [View'larning to'liq taqqoslovchi jadvali](#viewlarning-toliq-taqqoslovchi-jadvali)
5. [Amaliy misollar - Kitoblar API](#amaliy-misollar---kitoblar-api)
6. [Keng tarqalgan xatolar va yechimlar](#keng-tarqalgan-xatolar-va-yechimlar)
7. [Best Practices](#best-practices)
8. [Xulosa va tavsiyalar](#xulosa-va-tavsiyalar)

---

## Django REST Framework nima?

**Django REST Framework (DRF)** — bu Django framework'ining kengaytmasi bo'lib, RESTful API'larni yaratishni soddalashtiradi.  
U serializerlar, view'lar, autentifikatsiya, ruxsatlar (permissions) va routing kabi ko'plab kuchli imkoniyatlarni taqdim etadi.

### Nima uchun o'rganish kerak?

- **Modern arxitektura:** Web ilovalar endi **frontend + backend** tarzida bo'linadi. DRF backend uchun REST API yaratadi.
- **Ko'p platformali:** **Mobile app**, **React/Vue frontend**, yoki **tashqi API'lar** DRF orqali backend bilan aloqa qiladi.
- **Sifatli kod:** Kod **modulli, xavfsiz va testlash oson** bo'ladi.
- **Django integratsiyasi:** Django'ning qulay ORM tizimi bilan to'liq integratsiyalangan.

### REST API nima?

**REST (Representational State Transfer)** — bu HTTP protokoli orqali ma'lumot almashish uchun arxitektura uslubi.

**Asosiy tamoyillar:**
- **Resurslar:** Har bir obyekt (kitob, foydalanuvchi) URL orqali ko'rsatiladi
- **HTTP metodlari:** GET (o'qish), POST (yaratish), PUT/PATCH (yangilash), DELETE (o'chirish)
- **Stateless:** Har bir so'rov mustaqil
- **JSON format:** Ma'lumotlar odatda JSON formatida uzatiladi

---

## Django'da View nima?

**View** — bu foydalanuvchidan (yoki API so'rovdan) kelgan ma'lumotni qabul qilib, unga javob qaytaruvchi qismdir.  
U Django arxitekturasida `MVT` (Model–View–Template) yoki `MVC` (Model–View–Controller) tizimining "View" qismiga to'g'ri keladi.

### Django View vs DRF View

| Django View | DRF View |
|-------------|----------|
| HTML sahifa qaytaradi | JSON/XML ma'lumot qaytaradi |
| Template render qiladi | Serializer ishlatadi |
| Web brauzer uchun | API client'lar uchun |

DRF'da View'lar API'lar uchun ishlaydi, ya'ni JSON (yoki XML) formatda javob beradi.

---

## DRF View'lar — turlari va darajalari

```
BOSHLANG'ICH ──────────► O'RTA ──────────► PROFESSIONAL ──────────► ILG'OR
    │                      │                    │                      │
    ▼                      ▼                    ▼                      ▼
  FBV                 GenericAPIView        Generic Views          ViewSet
APIView               + Mixins            (ListCreateAPIView)   ModelViewSet
                                          (RetrieveUpdateAPIView)
```

| **Daraja** | **Turi** | **Qisqacha tavsif** | **Kod miqdori** |
|-------------|-----------|----------------------|-----------------|
| 🟢 Boshlang'ich | FBV / APIView | CRUD'ni qo'lda yozish | 50-100 qator |
| 🟡 O'rta | GenericAPIView + Mixins | CRUD'ni soddalashtirish | 20-40 qator |
| 🟠 Professional | Generic Views (Concrete) | Tayyor CRUD'lar bilan ishlash | 5-15 qator |
| 🔴 Ilg'or | ModelViewSet / ViewSet | Avtomatik routing va to'liq CRUD | 3-10 qator |

---

## View'larning to'liq taqqoslovchi jadvali

| **Turi** | **Asosi** | **Tavsif (nima qiladi)** | **Afzalliklari** | **Kamchiliklari** | **Qachon ishlatish kerak** |
| -------- | --------- | ------------------------ | ---------------- | ----------------- | -------------------------- |
| **1. Function-Based View (FBV)** | `django.http` | Oddiy funksiya orqali view yoziladi, `request.method` orqali GET, POST, PUT, DELETE ajratiladi. | ✅ Soddaligi<br>✅ Tushunarli logika<br>✅ Tez yoziladi | ❌ Katta loyihada kod ko'payadi<br>❌ Qayta ishlatish qiyin<br>❌ Kod takrorlanadi | 📌 Kichik loyihalar<br>📌 O'rganish bosqichi<br>📌 Oddiy endpoint'lar |
| **2. Class-Based View (CBV)** | `django.views` | View sinf ko'rinishida yoziladi, metodlar orqali (get, post, put, delete) amallar belgilanadi. | ✅ Kod qayta ishlatiladi<br>✅ Aniq tuzilma<br>✅ OOP tamoyillari | ❌ Boshlang'ichlar uchun murakkabroq<br>❌ API uchun emas | 📌 Django web sahifalar uchun<br>📌 Murakkab logika kerak bo'lsa |
| **3. APIView** | `rest_framework.views.APIView` | CBV'ning REST versiyasi. Har bir HTTP metod uchun metod yoziladi (`get`, `post`, `put`, `delete`) | ✅ DRF Response bilan ishlaydi<br>✅ Serializer qo'llanadi<br>✅ To'liq nazorat | ❌ CRUD'ni qo'lda yozish kerak<br>❌ Kod takrorlanishi | 📌 REST API boshlang'ich loyihalar<br>📌 Maxsus logika kerak bo'lsa |
| **4. GenericAPIView** | `rest_framework.generics.GenericAPIView` | APIView'dan voris olgan, qo'shimcha qulayliklar (queryset, serializer_class, lookup_field) bor | ✅ DRY tamoyili<br>✅ Serializer integratsiyasi<br>✅ Queryset boshqaruvi | ❌ CRUD metodlar yo'q<br>❌ Mixins bilan birga ishlatiladi | 📌 Mixins bilan CRUD qilish uchun<br>📌 Asosiy view yaratish uchun |
| **5. Mixins** | `rest_framework.mixins` | CRUD amallarini alohida sinflar sifatida taqdim etadi (`ListModelMixin`, `CreateModelMixin` va h.k.) | ✅ Qayta ishlatish oson<br>✅ DRY tamoyili<br>✅ Modulli | ❌ Alohida ishlatib bo'lmaydi<br>❌ GenericAPIView bilan kerak | 📌 CRUD metodlarini avtomatik qo'shish<br>📌 Moslashuvchan CRUD |
| **6. Generic Views (Concrete)** | `rest_framework.generics` | Mixins va GenericAPIView birlashtirilgan holda tayyor CRUD view'lar | ✅ CRUD avtomatik<br>✅ Minimal kod<br>✅ Tez ishga tushadi | ❌ Moslashuvchanligi cheklangan<br>❌ Murakkab logika qo'shish qiyin | 📌 Standart CRUD endpoint'lar<br>📌 Tez prototiplash |
| **7. ViewSet** | `rest_framework.viewsets.ViewSet` | APIView'ga o'xshaydi, lekin router orqali URL avtomatik generatsiya qiladi | ✅ URL yozishni kamaytiradi<br>✅ Soddalashtiradi<br>✅ Bir nechta action | ❌ Ba'zida ortiqcha moslashuvchanlik<br>❌ Router tushunchasi kerak | 📌 O'rta darajadagi REST API<br>📌 Custom action'lar kerak bo'lsa |
| **8. ModelViewSet** | `rest_framework.viewsets.ModelViewSet` | Generic Views + ViewSet birlashmasi — to'liq CRUD avtomatik | ✅ CRUD, routing, serializer — barchasi bitta joyda<br>✅ Eng kam kod<br>✅ Professional | ❌ Juda yirik loyihada ba'zida noqulay<br>❌ Ortiqcha funksiyalar | 📌 Tez API yaratish<br>📌 CRUD'ni to'liq avtomatlashtirish<br>📌 Professional loyihalar |
| **9. ReadOnlyModelViewSet** | `rest_framework.viewsets.ReadOnlyModelViewSet` | Faqat `list` va `retrieve` (ya'ni o'qish) imkonini beradi | ✅ Faqat o'qish uchun ideal<br>✅ Xavfsiz<br>✅ Minimal kod | ❌ CRUD kerak bo'lsa ishlamaydi<br>❌ Faqat GET | 📌 Faqat "GET" API'lar uchun<br>📌 Public ma'lumotlar |

---

## Amaliy misollar - Kitoblar API

Keling, bir xil "Kitoblar API"ni barcha view turlari bilan yozamiz va farqlarni ko'ramiz.

### 📦 Loyihani tayyorlash

#### 1. Model yaratish (`models.py`)

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Kitob nomi")
    author = models.CharField(max_length=100, verbose_name="Muallif")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    published_date = models.DateField(verbose_name="Nashr sanasi")
    pages = models.IntegerField(verbose_name="Sahifalar soni")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    description = models.TextField(blank=True, verbose_name="Ta'rif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Kitob"
        verbose_name_plural = "Kitoblar"

    def __str__(self):
        return f"{self.title} - {self.author}"
```

#### 2. Serializer yaratish (`serializers.py`)

```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """Kitoblar uchun serializer"""
    
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_isbn(self, value):
        """ISBN validatsiyasi"""
        if len(value) != 13:
            raise serializers.ValidationError("ISBN 13 ta belgidan iborat bo'lishi kerak")
        return value
    
    def validate_pages(self, value):
        """Sahifalar soni validatsiyasi"""
        if value <= 0:
            raise serializers.ValidationError("Sahifalar soni musbat bo'lishi kerak")
        return value
```

---

### 1️⃣ Function-Based View (FBV)

**Xususiyatlari:**
- Eng oddiy usul
- Har bir HTTP metodini `if` bilan tekshirish
- Ko'p kod yozish kerak

```python
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

@api_view(['GET', 'POST'])
def book_list(request):
    """Barcha kitoblarni ko'rsatish yoki yangi kitob qo'shish"""
    
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    """Bitta kitobni ko'rsatish, yangilash yoki o'chirish"""
    
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'error': 'Kitob topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book-list'),
    path('books/<int:pk>/', views.book_detail, name='book-detail'),
]
```

**Test qilish (curl):**

```bash
# Barcha kitoblarni olish
curl http://localhost:8000/api/books/

# Yangi kitob qo'shish
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Python dasturlash","author":"John Doe","isbn":"9781234567890","published_date":"2024-01-01","pages":350,"price":"150000"}'

# Bitta kitobni olish
curl http://localhost:8000/api/books/1/

# Kitobni yangilash
curl -X PUT http://localhost:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Python dasturlash (yangilangan)","author":"John Doe","isbn":"9781234567890","published_date":"2024-01-01","pages":400,"price":"180000"}'

# Kitobni o'chirish
curl -X DELETE http://localhost:8000/api/books/1/
```

---

### 2️⃣ APIView

**Xususiyatlari:**
- Class-based yondashuv
- Har bir HTTP metod uchun alohida metod
- DRF'ning to'liq imkoniyatlari

```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Book
from .serializers import BookSerializer

class BookListAPIView(APIView):
    """Barcha kitoblar ro'yxati va yangi kitob yaratish"""
    
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

#### GenericAPIView + Mixins (15+ qator)
```python
class BookListView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

#### Generic View (3 qator)
```python
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

#### ModelViewSet (3 qator)
```python
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Xulosa:** 50 qatordan 3 qatorgacha kamaytirdik! 🎉

---

## 🔧 Keng tarqalgan xatolar va yechimlar

### 1. **Xato: "You do not have permission to perform this action"**

**Sabab:** Permission sozlanmagan

**Yechim:**
```python
from rest_framework.permissions import AllowAny

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Hamma uchun ochiq
```

### 2. **Xato: "Method not allowed"**

**Sabab:** ViewSet'da kerakli metod yo'q

**Yechim:**
```python
# ReadOnlyModelViewSet faqat GET
# ModelViewSet to'liq CRUD
# ViewSet'da metodni qo'lda yozish kerak

class BookViewSet(viewsets.ViewSet):
    def list(self, request):  # GET /books/
        pass
    
    def create(self, request):  # POST /books/
        pass
```

### 3. **Xato: "Object with this field already exists"**

**Sabab:** Unique field takrorlangan (masalan, ISBN)

**Yechim:**
```python
class BookSerializer(serializers.ModelSerializer):
    def validate_isbn(self, value):
        if Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("Bu ISBN allaqachon mavjud")
        return value
```

### 4. **Xato: "Field is required"**

**Sabab:** Ma'lumot to'liq yuborilmagan

**Yechim:**
```python
# Serializer'da default qiymat berish
class BookSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False, default="")
```

### 5. **Xato: Router URL ishlamayapti**

**Sabab:** Router noto'g'ri ulangan

**Yechim:**
```python
# urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('books', BookViewSet, basename='book')

urlpatterns = [
    path('api/', include(router.urls)),
]
```

### 6. **Xato: Queryset qaytmayapti**

**Sabab:** `get_queryset()` yoki `queryset` noto'g'ri

**Yechim:**
```python
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        queryset = Book.objects.all()
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author__icontains=author)
        return queryset
```

### 7. **Xato: Serializer xatolari aniq ko'rinmayapti**

**Yechim:**
```python
# settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'NON_FIELD_ERRORS_KEY': 'errors',
}

# views.py
def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        print(serializer.errors)  # Debug uchun
        return Response(serializer.errors, status=400)
```

---

## 🎯 Best Practices

### 1. **Queryset optimallashtirish**

```python
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        # select_related / prefetch_related - N+1 muammosini hal qiladi
        return Book.objects.select_related('author').prefetch_related('tags')
```

### 2. **Pagination qo'shish**

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# yoki viewda
from rest_framework.pagination import PageNumberPagination

class BookPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookViewSet(viewsets.ModelViewSet):
    pagination_class = BookPagination
```

### 3. **Filter, Search, Ordering qo'shish**

```python
# settings.py
INSTALLED_APPS = [
    ...
    'django_filters',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# views.py
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_fields = ['author', 'published_date']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price']
```

**Foydalanish:**
```
GET /api/books/?author=John               # Filter
GET /api/books/?search=Python             # Search
GET /api/books/?ordering=-created_at      # Ordering
GET /api/books/?author=John&ordering=price # Kombinatsiya
```

### 4. **Permission va Authentication**

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """Action'ga qarab permission berish"""
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated()]
        elif self.action == 'destroy':
            return [IsAdminUser()]
        return super().get_permissions()
```

### 5. **Custom Serializer - Action'ga qarab**

```python
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    
    def get_serializer_class(self):
        """Action'ga qarab turli serializer"""
        if self.action == 'list':
            return BookListSerializer  # Qisqa ma'lumot
        elif self.action == 'retrieve':
            return BookDetailSerializer  # To'liq ma'lumot
        return BookSerializer
```

### 6. **Error Handling - To'liq**

```python
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except NotFound:
            return Response({'error': 'Kitob topilmadi'}, status=404)
```

### 7. **Logging qo'shish**

```python
import logging

logger = logging.getLogger(__name__)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def create(self, request, *args, **kwargs):
        logger.info(f"Yangi kitob yaratilmoqda: {request.data.get('title')}")
        response = super().create(request, *args, **kwargs)
        logger.info(f"Kitob yaratildi: ID {response.data.get('id')}")
        return response
```

### 8. **Testing yozish**

```python
# tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        """Har bir test oldidan ishlaydi"""
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            published_date="2024-01-01",
            pages=100,
            price=50000
        )
    
    def test_get_books_list(self):
        """Barcha kitoblarni olish testi"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_book(self):
        """Yangi kitob yaratish testi"""
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '9876543210123',
            'published_date': '2024-02-01',
            'pages': 200,
            'price': 75000
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_get_single_book(self):
        """Bitta kitobni olish testi"""
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
```

---

## 📚 Qo'shimcha imkoniyatlar

### 1. **Custom Action'lar**

```python
from rest_framework.decorators import action

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @action(detail=False, methods=['get'])
    def bestsellers(self, request):
        """Eng ko'p sotiladigan kitoblar"""
        books = self.queryset.filter(sales__gte=1000)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        """Kitobga sharh qo'shish"""
        book = self.get_object()
        # Sharh qo'shish logikasi
        return Response({'status': 'Sharh qo\'shildi'})
    
    @action(detail=True, methods=['get'], url_path='download-pdf')
    def download_pdf(self, request, pk=None):
        """Kitobni PDF formatda yuklab olish"""
        book = self.get_object()
        # PDF yaratish va qaytarish logikasi
        return Response({'download_url': f'/media/books/{book.id}.pdf'})
```

**URL'lar:**
```
GET  /api/books/bestsellers/           - detail=False
POST /api/books/{id}/add_review/       - detail=True
GET  /api/books/{id}/download-pdf/     - custom url_path
```

### 2. **Throttling (So'rovlarni cheklash)**

```python
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'user': '100/hour',  # Login qilganlar uchun
        'anon': '20/hour',   # Mehmon uchun
    }
}
```

### 3. **Versioning**

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
}

# urls.py
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v2/', include(router_v2.urls)),
]

# views.py
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return BookSerializerV1
        return BookSerializerV2
```

### 4. **Caching**

```python
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @method_decorator(cache_page(60 * 15))  # 15 daqiqa
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
```

---

## 🎓 O'rganish yo'lxaritasi

### **1-bosqich: Asoslar (1 hafta)**
- ✅ FBV bilan oddiy CRUD yozish
- ✅ APIView bilan tanishish
- ✅ Serializer yaratish va ishlatish
- ✅ Postman/curl bilan test qilish

### **2-bosqich: O'rta daraja (1 hafta)**
- ✅ GenericAPIView + Mixins bilan ishlash
- ✅ Generic Views (Concrete) ishlatish
- ✅ Pagination qo'shish
- ✅ Filter va Search qo'shish

### **3-bosqich: Professional (1 hafta)**
- ✅ ViewSet va ModelViewSet
- ✅ Router bilan ishlash
- ✅ Custom action'lar yaratish
- ✅ Permission va Authentication

### **4-bosqich: Ilg'or (1 hafta)**
- ✅ Custom pagination
- ✅ Throttling
- ✅ Versioning
- ✅ Caching
- ✅ Testing yozish

---

## 📖 Xulosa va tavsiyalar

### **Qaysi View turini tanlash?**

```
┌─────────────────────────────────────┐
│  Loyihangiz qanday?                 │
└─────────────────────────────────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
Kichik        Katta
Oddiy         Murakkab
    │             │
    │         ┌───┴────┐
    │         │        │
    ▼         ▼        ▼
  FBV      Generic   ModelViewSet
APIView    Views
```

### **Tavsiyalar:**

1. **Boshlang'ichlar uchun:**
   - FBV yoki APIView bilan boshlang
   - Har bir qatorni tushuning
   - Qo'lda yozib ko'ring

2. **O'rta daraja:**
   - Generic Views ishlatishni o'rganing
   - Mixins bilan tanishing
   - Pagination va Filter qo'shing

3. **Professional daraja:**
   - ModelViewSet asosiy qurol
   - Custom action'lar qo'shing
   - Testing yozing
   - Documentation yarating

4. **Best Practice:**
   - DRY tamoyiliga amal qiling
   - Kod qayta ishlatilsin
   - Error handling unutmang
   - Logging qo'shing
   - Test yozing

### **Yodda tuting:**

> **"Kod yozish oson, lekin yaxshi kod yozish — san'at!"**

- ✅ Har doim eng oddiy yechimdan boshlang
- ✅ Kerak bo'lgandagina murakkablashtiring
- ✅ Kodingizni boshqalar o'qiy olishi kerak
- ✅ Test yozishni unutmang
- ✅ Documentation muhim

---

## 🔗 Foydali havolalar

### **Rasmiy dokumentatsiya:**
- 📘 [Django REST Framework](https://www.django-rest-framework.org/)
- 📘 [DRF - Views](https://www.django-rest-framework.org/api-guide/views/)
- 📘 [DRF - Generic Views](https://www.django-rest-framework.org/api-guide/generic-views/)
- 📘 [DRF - ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)
- 📘 [DRF - Routers](https://www.django-rest-framework.org/api-guide/routers/)

### **Tutorial va qo'llanmalar:**
- 🎥 [DRF Crash Course](https://www.youtube.com/results?search_query=django+rest+framework+tutorial)
- 📚 [Django REST Framework Tutorial](https://testdriven.io/blog/drf-views-part-1/)
- 📚 [Real Python - DRF](https://realpython.com/tutorials/django-rest-framework/)

### **Amaliyot uchun:**
- 💻 [GitHub - DRF Examples](https://github.com/topics/django-rest-framework)
- 💻 [DRF Playground](https://www.django-rest-framework.org/tutorial/quickstart/)

---

## 📝 Qo'shimcha misollar

### **To'liq loyiha strukturasi:**

```
myproject/
├── manage.py
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── books/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   ├── pagination.py
│   ├── filters.py
│   └── tests.py
└── requirements.txt
```

### **requirements.txt:**

```
Django==4.2.0
djangorestframework==3.14.0
django-filter==23.1
django-cors-headers==4.0.0
```

### **settings.py - to'liq konfiguratsiya:**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'django_filters',
    'corsheaders',
    
    # Local apps
    'books',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    },
    
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
]
```

---

## 🎯 Amaliy mashqlar

### **Mashq 1: Oddiy blog API**
Quyidagi modellar uchun to'liq CRUD API yarating:
- Post (title, content, author, created_at)
- Comment (post, text, author, created_at)

### **Mashq 2: E-commerce API**
Quyidagi funksiyalarni qo'shing:
- Product listing va filtering
- Shopping cart
- Order management
- Product search

### **Mashq 3: Social media API**
Quyidagi imkoniyatlarni qo'shing:
- User profiles
- Posts va comments
- Like/Unlike
- Follow/Unfollow
- Feed generation

---

✍️ **Muallif:** Uktam Turgun (takomillashtirilgan versiya)  
🗓 **Tayyorlangan sana:** 2025-11-01  
📦 **Versiya:** 2.0 (To'liq amaliy qo'llanma)  
🏷 **Bo'lim:** Django REST Framework — Views  
📧 **Savollar uchun:** GitHub Issues yoki Telegram

---

> **Omad tilaymiz! Happy Coding! 🚀**self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(APIView):
    """Bitta kitob bilan ishlash"""
    
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookListAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailAPIView.as_view(), name='book-detail'),
]
```

---

### 3️⃣ GenericAPIView + Mixins

**Xususiyatlari:**
- Kamroq kod
- Mixins orqali CRUD metodlar
- Moslashuvchan

```python
# views.py
from rest_framework import generics, mixins
from .models import Book
from .serializers import BookSerializer

class BookListView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookDetailView(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]
```

**Mavjud Mixins:**

| Mixin | Metod | Vazifasi |
|-------|-------|----------|
| `ListModelMixin` | `list()` | Barcha obyektlarni ro'yxatini qaytarish |
| `CreateModelMixin` | `create()` | Yangi obyekt yaratish |
| `RetrieveModelMixin` | `retrieve()` | Bitta obyektni olish |
| `UpdateModelMixin` | `update()` | Obyektni yangilash |
| `DestroyModelMixin` | `destroy()` | Obyektni o'chirish |

---

### 4️⃣ Generic Views (Concrete Views)

**Xususiyatlari:**
- Eng kam kod
- Tayyor kombinatsiyalar
- Standart CRUD uchun ideal

```python
# views.py
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

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
]
```

**Barcha Generic Views:**

| View Class | HTTP metodlar | Vazifasi |
|------------|---------------|----------|
| `ListAPIView` | GET | Ro'yxatni ko'rsatish |
| `CreateAPIView` | POST | Yangi obyekt yaratish |
| `RetrieveAPIView` | GET | Bitta obyektni ko'rsatish |
| `UpdateAPIView` | PUT, PATCH | Obyektni yangilash |
| `DestroyAPIView` | DELETE | Obyektni o'chirish |
| `ListCreateAPIView` | GET, POST | Ro'yxat va yaratish |
| `RetrieveUpdateAPIView` | GET, PUT, PATCH | Ko'rish va yangilash |
| `RetrieveDestroyAPIView` | GET, DELETE | Ko'rish va o'chirish |
| `RetrieveUpdateDestroyAPIView` | GET, PUT, PATCH, DELETE | To'liq CRUD (yaratishdan tashqari) |

---

### 5️⃣ ViewSet

**Xususiyatlari:**
- Action-based yondashuv
- Router bilan avtomatik URL
- Custom action'lar qo'shish mumkin

```python
# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ViewSet):
    
    def list(self, request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def retrieve(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({'error': 'Topilmadi'}, status=404)
    
    def update(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Book.DoesNotExist:
            return Response({'error': 'Topilmadi'}, status=404)
    
    def destroy(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response(status=204)
        except Book.DoesNotExist:
            return Response({'error': 'Topilmadi'}, status=404)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_books = Book.objects.all()[:5]
        serializer = BookSerializer(recent_books, many=True)
        return Response(serializer.data)
```

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]
```

---

### 6️⃣ ModelViewSet (ENG PROFESSIONAL)

**Xususiyatlari:**
- Eng kam kod (3-10 qator)
- To'liq CRUD avtomatik
- Professional loyihalar uchun

```python
# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Book
from .serializers import BookSerializer

class BookModelViewSet(viewsets.ModelViewSet):
    """
    To'liq CRUD operatsiyalar uchun ViewSet.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Oxirgi 10 ta kitob"""
        recent_books = self.queryset.order_by('-created_at')[:10]
        serializer = self.get_serializer(recent_books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_author(self, request):
        """Muallif bo'yicha kitoblar"""
        author = request.query_params.get('author', None)
        if author:
            books = self.queryset.filter(author__icontains=author)
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)
        return Response({'error': 'author parametri kerak'}, status=400)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Bitta kitob statistikasi"""
        book = self.get_object()
        return Response({
            'title': book.title,
            'pages': book.pages,
            'price': book.price,
            'age_days': (timezone.now().date() - book.published_date).days
        })
```

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books', views.BookModelViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

**Yaratilgan URL'lar:**

```
GET     /api/books/                    - Barcha kitoblar
POST    /api/books/                    - Yangi kitob yaratish
GET     /api/books/{id}/               - Bitta kitob
PUT     /api/books/{id}/               - Kitobni to'liq yangilash
PATCH   /api/books/{id}/               - Kitobni qisman yangilash
DELETE  /api/books/{id}/               - Kitobni o'chirish
GET     /api/books/recent/             - Oxirgi kitoblar
GET     /api/books/by_author/?author=X - Muallif bo'yicha
GET     /api/books/{id}/stats/         - Kitob statistikasi
```

---

### 7️⃣ ReadOnlyModelViewSet

**Xususiyatlari:**
- Faqat o'qish (GET)
- O'zgartirish mumkin emas
- Public API'lar uchun

```python
# views.py
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Faqat o'qish uchun ViewSet.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books', views.BookReadOnlyViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

---

## 📊 View turlarini taqqoslash - Amaliy misol

### **Vazifa:** Barcha kitoblarni olish va yangi kitob yaratish

#### FBV (50+ qator)
```python
@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

#### APIView (30+ qator)
```python
class BookListAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

#### 3️⃣ GenericAPIView + Mixins (15+ qator)

```python
from rest_framework import generics, mixins

class BookListView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

#### 4️⃣ Generic Views (3 qator)

```python
from rest_framework import generics

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

#### 5️⃣ ModelViewSet (3 qator)

```python
from rest_framework import viewsets

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**🎉 Xulosa:** 50 qatordan 3 qatorgacha!

---

## 6. Keng tarqalgan xatolar va yechimlar

### Xato 1: Permission denied

```python
from rest_framework.permissions import AllowAny

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
```

### Xato 2: Method not allowed

```python
# ViewSet'da metodlarni qo'lda yozish kerak
class BookViewSet(viewsets.ViewSet):
    def list(self, request):
        pass
```

### Xato 3: Field already exists

```python
class BookSerializer(serializers.ModelSerializer):
    def validate_isbn(self, value):
        if Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("Bu ISBN mavjud")
        return value
```

---

## 7. Best Practices

### 1. Pagination

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

### 2. Filter va Search

```python
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_fields = ['author', 'published_date']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price']
```

### 3. Permission

```python
from rest_framework.permissions import IsAuthenticated

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
```

### 4. Testing

```python
from rest_framework.test import APITestCase

class BookAPITestCase(APITestCase):
    def test_get_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)
```

---

## 8. Qo'shimcha imkoniyatlar

### Custom Action

```python
from rest_framework.decorators import action

class BookViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'])
    def recent(self, request):
        books = Book.objects.all()[:10]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
```

### Throttling

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'user': '100/hour',
        'anon': '20/hour',
    }
}
```

---

## 9. O'rganish yo'lxaritasi

**1-hafta:** FBV, APIView, Serializer  
**2-hafta:** GenericAPIView, Mixins, Generic Views  
**3-hafta:** ViewSet, ModelViewSet, Router  
**4-hafta:** Permission, Testing, Best Practices

---

## 10. Xulosa va tavsiyalar

### Qaysi View turini tanlash?

- **Kichik loyiha** → FBV yoki APIView
- **O'rta loyiha** → Generic Views
- **Katta loyiha** → ModelViewSet

### Tavsiyalar:

✅ Oddiy yechimdan boshlang  
✅ Kerak bo'lganda murakkablashtiring  
✅ Test yozing  
✅ Documentation yarating  

---

## 🔗 Foydali havolalar

- [Django REST Framework](https://www.django-rest-framework.org/)
- [DRF Views](https://www.django-rest-framework.org/api-guide/views/)
- [DRF ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)

---

## 📝 To'liq loyiha strukturasi

```
myproject/
├── manage.py
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── books/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
└── requirements.txt
```

### requirements.txt

```
Django==4.2.0
djangorestframework==3.14.0
django-filter==23.1
```

### settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'books',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

---

## 🎯 Amaliy mashqlar

**Mashq 1:** Blog API (Post, Comment)  
**Mashq 2:** E-commerce API (Product, Order)  
**Mashq 3:** Social media API (User, Post, Like)

---

✍️ **Muallif:** Uktam Turgun  
🗓 **Sana:** 2025-11-01  
📦 **Versiya:** 2.0  
🏷 **Bo'lim:** Django REST Framework — Views

---

> **Omad tilaymiz! Happy Coding! 🚀**
