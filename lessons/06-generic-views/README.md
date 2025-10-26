# Lesson 06: Generic Views - REST API'larni professional darajada yozish

## 📋 Dars maqsadi

Siz bu darsda Django REST Framework'ning **Generic Views**'ini o'rganasiz. Bu - professional REST API yaratishning eng samarali usuli!

### 🎯 Nima o'rganamiz:
- ✅ Generic Views nima va nima uchun kerak
- ✅ Function-based views vs Generic Views
- ✅ 9 xil Generic View turlarini ishlatish
- ✅ Mixins orqali custom views yaratish
- ✅ Filtering, Ordering, Pagination qo'shish
- ✅ Custom methods bilan views'ni maxsus sozlash

---

## 🤔 Nega Generic Views kerak?

### Muammo: Function-based views'da kod takrorlanadi

5-darsda biz function-based views yozdik. Ular ishlaydi, lekin:

```python
# book_list - 30 qator kod
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# book_detail - yana 40 qator kod
@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
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

**Jami: 70+ qator kod!** 😰

### ✨ Yechim: Generic Views

Xuddi shu funktsionallik Generic Views bilan:

```python
from rest_framework import generics

# Faqat 3 qator! 🎉
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Jami: 6 qator kod!** 🚀

---

## 📚 Generic Views turlari

DRF'da 9 ta tayyor Generic View bor:

### 1. **ListAPIView** - Ro'yxatni ko'rsatish (GET)

```python
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Endpoint:** `GET /books/`  
**Vazifasi:** Barcha kitoblar ro'yxatini qaytaradi

---

### 2. **CreateAPIView** - Yangi obyekt yaratish (POST)

```python
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Endpoint:** `POST /books/create/`  
**Vazifasi:** Yangi kitob yaratadi

---

### 3. **RetrieveAPIView** - Bitta obyektni olish (GET)

```python
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Endpoint:** `GET /books/1/`  
**Vazifasi:** ID bo'yicha bitta kitobni qaytaradi

---

### 4. **UpdateAPIView** - Obyektni yangilash (PUT, PATCH)

```python
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Endpoint:** `PUT /books/1/update/` yoki `PATCH /books/1/update/`  
**Vazifasi:** Kitobni yangilaydi

---

### 5. **DestroyAPIView** - Obyektni o'chirish (DELETE)

```python
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Endpoint:** `DELETE /books/1/delete/`  
**Vazifasi:** Kitobni o'chiradi

---

### 6. **ListCreateAPIView** - List + Create (GET, POST)

```python
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Endpoints:**
- `GET /books/` - Ro'yxat
- `POST /books/` - Yangi kitob

---

### 7. **RetrieveUpdateAPIView** - Retrieve + Update (GET, PUT, PATCH)

```python
class BookRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Endpoints:**
- `GET /books/1/` - Bitta kitob
- `PUT /books/1/` - To'liq yangilash
- `PATCH /books/1/` - Qisman yangilash

---

### 8. **RetrieveDestroyAPIView** - Retrieve + Destroy (GET, DELETE)

```python
class BookRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Endpoints:**
- `GET /books/1/` - Bitta kitob
- `DELETE /books/1/` - Kitobni o'chirish

---

### 9. **RetrieveUpdateDestroyAPIView** - Retrieve + Update + Destroy (GET, PUT, PATCH, DELETE)

```python
class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Endpoints:**
- `GET /books/1/` - Bitta kitob
- `PUT /books/1/` - To'liq yangilash
- `PATCH /books/1/` - Qisman yangilash
- `DELETE /books/1/` - O'chirish

---

## 🎨 Qaysi Generic View'ni tanlash?

| Vazifa | Generic View | HTTP Methods |
|--------|-------------|--------------|
| Faqat ro'yxat | `ListAPIView` | GET |
| Faqat yaratish | `CreateAPIView` | POST |
| Faqat ko'rish | `RetrieveAPIView` | GET |
| Faqat yangilash | `UpdateAPIView` | PUT, PATCH |
| Faqat o'chirish | `DestroyAPIView` | DELETE |
| Ro'yxat + Yaratish | `ListCreateAPIView` | GET, POST |
| Ko'rish + Yangilash | `RetrieveUpdateAPIView` | GET, PUT, PATCH |
| Ko'rish + O'chirish | `RetrieveDestroyAPIView` | GET, DELETE |
| Ko'rish + Yangilash + O'chirish | `RetrieveUpdateDestroyAPIView` | GET, PUT, PATCH, DELETE |

---

## 🧩 Mixins - Generic Views'ning qurilish bloklari

Generic Views ichida **Mixins** ishlatiladi. Har bir Mixin bitta vazifani bajaradi:

```python
from rest_framework import mixins, generics

# 1. ListModelMixin - Ro'yxatni qaytaradi
class BookListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# 2. CreateModelMixin - Yangi obyekt yaratadi
class BookCreateView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# 3. RetrieveModelMixin - Bitta obyektni qaytaradi
class BookDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# 4. UpdateModelMixin - Obyektni yangilaydi
class BookUpdateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

# 5. DestroyModelMixin - Obyektni o'chiradi
class BookDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

### 🔥 Mixins'larni birlashtirib custom view yaratish

```python
# Custom view: List + Create + Retrieve
class BookListCreateRetrieveView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

---

## ⚙️ Generic Views'ni customize qilish

### 1. `get_queryset()` - QuerySet'ni sozlash

```python
class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        # Faqat mavjud kitoblarni qaytarish
        return Book.objects.filter(available=True)
```

**Real misol: User'ning o'z kitoblarini ko'rsatish**

```python
class MyBooksView(generics.ListAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        # Faqat login qilgan user'ning kitoblari
        user = self.request.user
        return Book.objects.filter(owner=user)
```

---

### 2. `get_serializer_class()` - Serializer'ni dinamik tanlash

```python
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    
    def get_serializer_class(self):
        # Admin uchun batafsil, oddiy user uchun qisqa
        if self.request.user.is_staff:
            return BookDetailSerializer
        return BookSerializer
```

---

### 3. `get_object()` - Obyektni olish logikasini o'zgartirish

```python
class BookDetailView(generics.RetrieveAPIView):
    serializer_class = BookSerializer
    
    def get_object(self):
        # ID o'rniga slug bo'yicha qidirish
        slug = self.kwargs.get('slug')
        return Book.objects.get(slug=slug)
```

---

### 4. `perform_create()` - Yaratish jarayonini customize qilish

```python
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def perform_create(self, serializer):
        # Avtomatik owner qo'shish
        serializer.save(owner=self.request.user)
```

---

### 5. `perform_update()` - Yangilash jarayonini customize qilish

```python
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def perform_update(self, serializer):
        # Yangilangan vaqtni avtomatik qo'shish
        serializer.save(updated_by=self.request.user)
```

---

### 6. `perform_destroy()` - O'chirish jarayonini customize qilish

```python
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def perform_destroy(self, instance):
        # To'liq o'chirish o'rniga "soft delete"
        instance.is_deleted = True
        instance.save()
```

---

## 🔍 Filtering - Qidirish va filterlash

### 1. URL orqali filtering

```python
from rest_framework import generics

class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        queryset = Book.objects.all()
        
        # URL'dan parametrlarni olish
        author = self.request.query_params.get('author')
        min_price = self.request.query_params.get('min_price')
        
        # Filterlash
        if author:
            queryset = queryset.filter(author__icontains=author)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        return queryset
```

**Foydalanish:**
```
GET /books/?author=Alisher
GET /books/?min_price=50000
GET /books/?author=Alisher&min_price=50000
```

---

### 2. DRF Filter Backends

```python
from rest_framework import generics, filters

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'description']
    ordering_fields = ['price', 'publish_date', 'title']
```

**Foydalanish:**
```
# Qidirish
GET /books/?search=django

# Tartiblash
GET /books/?ordering=price          # Arzon → Qimmat
GET /books/?ordering=-price         # Qimmat → Arzon
GET /books/?ordering=publish_date   # Eski → Yangi

# Birgalikda
GET /books/?search=python&ordering=-price
```

---

## 📄 Pagination - Sahifalash

### 1. settings.py'da global pagination

```python
# library_project/settings.py

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

**Natija:**
```json
{
    "count": 100,
    "next": "http://localhost:8000/books/?page=2",
    "previous": null,
    "results": [
        // 10 ta kitob
    ]
}
```

---

### 2. View'da maxsus pagination

```python
from rest_framework.pagination import PageNumberPagination

class BookPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
```

**Foydalanish:**
```
GET /books/?page=1
GET /books/?page=2&page_size=20
```

---

## 🚀 Amaliy misol: Library Project'ni yangilash

### Eski kod (05-dars):

```python
# books/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### Yangi kod (06-dars):

```python
# books/views.py
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from .models import Book
from .serializers import BookSerializer

# Custom Pagination
class BookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# List + Create
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'description']
    ordering_fields = ['price', 'publish_date', 'title']
    ordering = ['-publish_date']  # Default ordering

# Retrieve + Update + Destroy
class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

### URL'lar:

```python
# books/urls.py
from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDestroyView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
]
```

---

## 📊 Taqqoslash

| Xususiyat | Function-based | Generic Views |
|-----------|----------------|---------------|
| Kod hajmi | 70+ qator | 6 qator |
| Error handling | Qo'lda yozish | Avtomatik |
| Validation | Qo'lda yozish | Avtomatik |
| Pagination | Qo'lda yozish | 1 qator |
| Filtering | Qo'lda yozish | 2 qator |
| Ordering | Qo'lda yozish | 2 qator |
| O'qilishi | Murakkab | Oson |
| Texnik xizmat | Qiyin | Oson |

---

## ✅ Xulosa

### Generic Views afzalliklari:
1. ✅ **Kam kod** - 10 marta kam yozasiz
2. ✅ **DRY (Don't Repeat Yourself)** - Takrorlanish yo'q
3. ✅ **Professional** - Real loyihalarda ishlatiladi
4. ✅ **Oson o'qiladi** - Boshqalar tezda tushunadi
5. ✅ **DRF standart** - DRF'ning best practice'si
6. ✅ **Customize qilish oson** - Kerak bo'lsa method override qiling
7. ✅ **Filtering, Pagination tayyor** - Faqat yoqing

### Qachon Function-based views ishlatamiz?
- ❌ Standart CRUD uchun - **ISHLATMANG**
- ✅ Juda custom logic kerak bo'lsa - Function-based
- ✅ Bir nechta model bilan ishlash - Function-based
- ✅ Non-standard endpoints - Function-based

---

## 🎯 Keyingi qadam

Endi `code/library-project` papkasida amaliy qismni ko'ramiz! 🚀

**Qo'llanma:**
1. ✅ README.md'ni o'qidingiz
2. ⏭️ `code/library-project` papkasidagi kodlarni ko'ring
3. ⏭️ `examples/` papkasidagi qisqa misollarni o'rganing
4. ⏭️ `homework.md`'dagi vazifani bajaring

---

**Savol-javoblar uchun telegram: [@your_username]**  
**GitHub: [course repo linki]**

Happy coding! 🎉