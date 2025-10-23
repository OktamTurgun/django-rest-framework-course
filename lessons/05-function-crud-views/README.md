# 05. Function va CRUD Views

> Function-based view'lar yordamida to'liq CRUD operatsiyalarini amalga oshirish

## 🎯 Dars maqsadlari

Ushbu darsdan keyin siz quyidagilarni bilib olasiz:
- [x] Function-based views (FBV) nima va qanday ishlashi
- [x] @api_view dekoratori va uning vazifasi
- [x] To'liq CRUD operatsiyalarini yozish
- [x] HTTP status kodlar bilan to'g'ri ishlash
- [x] Xatoliklarni to'g'ri handle qilish

**Qiyinlik darajasi:** ⭐⭐⭐☆☆ (3/5)  
**Taxminiy vaqt:** 60-90 daqiqa

---

## 📚 Nazariya

### Function-based views (FBV) nima?

Function-based views - bu oddiy Python funksiyalari bo'lib, HTTP so'rovlarini qabul qilib, javob qaytaradi.

**Oddiy Django view:**
```python
def my_view(request):
    return HttpResponse("Hello")
```

**DRF Function-based view:**
```python
@api_view(['GET'])
def my_view(request):
    return Response({"message": "Hello"})
```

### @api_view dekoratori

`@api_view` dekoratori oddiy funksiyani DRF view'ga aylantiradi:

```python
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def book_list(request):
    # Bu yerda GET va POST so'rovlarni qabul qilasiz
    pass
```

**Afzalliklari:**
- ✅ Oddiy va tushunarli
- ✅ Tez yozish mumkin
- ✅ Kichik loyihalar uchun ideal
- ✅ Request obyektiga to'g'ridan-to'g'ri kirish

---

## 🔥 CRUD operatsiyalari

### CRUD nima?

| Operatsiya | HTTP Method | Vazifa |
|------------|-------------|---------|
| **C**reate | POST | Yangi ma'lumot yaratish |
| **R**ead | GET | Ma'lumotlarni o'qish |
| **U**pdate | PUT/PATCH | Ma'lumotni yangilash |
| **D**elete | DELETE | Ma'lumotni o'chirish |

---

## 💻 Amaliyot

### 1-qadam: Loyihani tayyorlash

#### Model yaratamiz (`models.py`)

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    published_date = models.DateField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
```

#### Serializer yaratamiz (`serializers.py`)

```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['created_at']
```

---

### 2-qadam: List va Create (GET va POST)

**views.py:**

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

@api_view(['GET', 'POST'])
def book_list(request):
    """
    GET: Barcha kitoblarni qaytaradi
    POST: Yangi kitob yaratadi
    """
    
    if request.method == 'GET':
        # Barcha kitoblarni olish
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Yangi kitob yaratish
        serializer = BookSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
```

**Tushuntirish:**
- `many=True` - bir nechta obyektlarni serializer qilish
- `is_valid()` - ma'lumotlar validatsiyasi
- `status.HTTP_201_CREATED` - yangi resurs yaratildi (201)
- `status.HTTP_400_BAD_REQUEST` - noto'g'ri so'rov (400)

---

### 3-qadam: Detail operatsiyalari (GET, PUT, DELETE)

```python
@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    """
    GET: Bitta kitobni qaytaradi
    PUT: Kitobni yangilaydi
    DELETE: Kitobni o'chiradi
    """
    
    # Kitobni topish
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(
            {'error': 'Kitob topilmadi'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        # Bitta kitobni qaytarish
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Kitobni yangilash
        serializer = BookSerializer(book, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    elif request.method == 'DELETE':
        # Kitobni o'chirish
        book.delete()
        return Response(
            {'message': 'Kitob muvaffaqiyatli o'chirildi'},
            status=status.HTTP_204_NO_CONTENT
        )
```

**Tushuntirish:**
- `pk` - primary key (ID)
- `try-except` - xatoliklarni ushlash
- PUT - to'liq yangilash
- `status.HTTP_204_NO_CONTENT` - muvaffaqiyatli, kontent yo'q

---

### 4-qadam: URL'larni sozlash

**urls.py:**

```python
from django.urls import path
from .views import book_list, book_detail

urlpatterns = [
    path('books/', book_list, name='book-list'),
    path('books/<int:pk>/', book_detail, name='book-detail'),
]
```

---

## 🧪 Testlash

### 1. Barcha kitoblarni olish

```http
GET http://127.0.0.1:8000/api/books/
```

**Javob:**
```json
[
    {
        "id": 1,
        "title": "Python Programming",
        "author": "John Doe",
        "isbn": "1234567890123",
        "price": "29.99",
        "published_date": "2024-01-15",
        "is_available": true,
        "created_at": "2024-10-23T10:30:00Z"
    }
]
```

---

### 2. Yangi kitob yaratish

```http
POST http://127.0.0.1:8000/api/books/
Content-Type: application/json

{
    "title": "Django for Beginners",
    "author": "William Vincent",
    "isbn": "9876543210987",
    "price": "39.99",
    "published_date": "2024-02-20",
    "is_available": true
}
```

**Javob (201 Created):**
```json
{
    "id": 2,
    "title": "Django for Beginners",
    "author": "William Vincent",
    "isbn": "9876543210987",
    "price": "39.99",
    "published_date": "2024-02-20",
    "is_available": true,
    "created_at": "2024-10-23T10:35:00Z"
}
```

---

### 3. Bitta kitobni olish

```http
GET http://127.0.0.1:8000/api/books/2/
```

---

### 4. Kitobni yangilash

```http
PUT http://127.0.0.1:8000/api/books/2/
Content-Type: application/json

{
    "title": "Django for Beginners (Updated)",
    "author": "William Vincent",
    "isbn": "9876543210987",
    "price": "44.99",
    "published_date": "2024-02-20",
    "is_available": true
}
```

---

### 5. Kitobni o'chirish

```http
DELETE http://127.0.0.1:8000/api/books/2/
```

**Javob (204 No Content):**
```json
{
    "message": "Kitob muvaffaqiyatli o'chirildi"
}
```

---

## 📊 HTTP Status Kodlar

| Kod | Ma'nosi | Qachon ishlatiladi |
|-----|---------|-------------------|
| 200 | OK | Muvaffaqiyatli GET, PUT |
| 201 | Created | Yangi resurs yaratildi (POST) |
| 204 | No Content | Muvaffaqiyatli DELETE |
| 400 | Bad Request | Noto'g'ri ma'lumot yuborildi |
| 404 | Not Found | Resurs topilmadi |
| 500 | Server Error | Server xatosi |

---

## 🎨 Yaxshi amaliyotlar

### ✅ 1. Xatoliklarni to'g'ri handle qilish

```python
try:
    book = Book.objects.get(pk=pk)
except Book.DoesNotExist:
    return Response(
        {'error': 'Kitob topilmadi'}, 
        status=status.HTTP_404_NOT_FOUND
    )
```

### ✅ 2. Tushunarli xato xabarlari

```python
if not serializer.is_valid():
    return Response(
        {
            'error': 'Ma\'lumotlar noto\'g\'ri',
            'details': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )
```

### ✅ 3. Docstring yozish

```python
@api_view(['GET', 'POST'])
def book_list(request):
    """
    Barcha kitoblarni ko'rish yoki yangi kitob yaratish
    
    GET: Barcha kitoblarni qaytaradi
    POST: Yangi kitob yaratadi
    """
    pass
```

---

## 🆚 FBV vs CBV

| Function-based Views | Class-based Views |
|---------------------|-------------------|
| ✅ Oddiy va tushunarli | ✅ Qayta ishlatish oson |
| ✅ Tez yozish mumkin | ✅ Kod takrorlanmaydi |
| ✅ Kichik loyihalar uchun | ✅ Katta loyihalar uchun |
| ❌ Kod takrorlanadi | ❌ Murakkab |

---

## 🚀 Keyingi qadam

Keyingi darsda **Generic Views** bilan tanishamiz - bu kod yozishni yanada osonlashtiradi!

**Misollar:**
- `ListCreateAPIView` - List va Create bitta view'da
- `RetrieveUpdateDestroyAPIView` - Detail operatsiyalar

---

## 📝 Xulosa

Ushbu darsda biz:
- ✅ Function-based view'larni o'rgandik
- ✅ @api_view dekoratori bilan ishladik
- ✅ To'liq CRUD operatsiyalarini yozdik
- ✅ HTTP status kodlar bilan ishladik
- ✅ Xatoliklarni handle qilishni o'rgandik

---

## 🔗 Foydali havolalar

- [DRF Function-based Views](https://www.django-rest-framework.org/api-guide/views/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [REST API Best Practices](https://restfulapi.net/http-status-codes/)

---

**Keyingi dars:** [06 - Generic Views](../06-generic-views/README.md)

**Uy vazifasi:** [Homework](./homework.md)