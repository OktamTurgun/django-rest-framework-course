# 06 - Generic Views - Code Examples

## 📁 Struktura

```
code/
└── library-project/     ← Updated library project with Generic Views
    ├── manage.py
    ├── db.sqlite3
    ├── Pipfile
    ├── books/
    │   ├── models.py
    │   ├── serializers.py
    │   ├── views.py         ← 🆕 Generic Views!
    │   ├── urls.py          ← 🆕 Updated URLs!
    │   ├── admin.py
    │   ├── apps.py
    │   ├── tests.py
    │   └── migrations/
    ├── library_project/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    └── static/
```

## 🚀 Ishga tushirish

```bash
# 1. library-project papkasiga kiring
cd library-project

# 2. Virtual environment yaratish (agar yo'q bo'lsa)
pipenv install
pipenv shell

# 3. Migrations
python manage.py makemigrations
python manage.py migrate

# 4. Admin user yaratish (ixtiyoriy)
python manage.py createsuperuser

# 5. Server'ni ishga tushirish
python manage.py runserver
```

## 🧪 Test qilish

### 1. Brauzerda DRF Interface:

Quyidagi URL'larni brauzerda oching:

- `http://localhost:8000/books/` - **List + Create**
- `http://localhost:8000/books/1/` - **Single book (Retrieve + Update + Delete)**

### 2. Pagination:

- `http://localhost:8000/books/?page=1`
- `http://localhost:8000/books/?page=2&page_size=5`

### 3. Search (qidirish):

- `http://localhost:8000/books/?search=django`
- `http://localhost:8000/books/?search=python`

### 4. Ordering (tartiblash):

- `http://localhost:8000/books/?ordering=price` - Arzon → Qimmat
- `http://localhost:8000/books/?ordering=-price` - Qimmat → Arzon
- `http://localhost:8000/books/?ordering=publish_date` - Eski → Yangi
- `http://localhost:8000/books/?ordering=-publish_date` - Yangi → Eski

### 5. Combined (birgalikda):

- `http://localhost:8000/books/?search=django&ordering=-price&page=1&page_size=5`

### 6. Custom endpoints:

- `http://localhost:8000/books/available/` - Faqat mavjud kitoblar
- `http://localhost:8000/books/expensive/` - Qimmat kitoblar (price > 100000)
- `http://localhost:8000/books/by-author/Alisher/` - Muallif bo'yicha

### 7. Advanced filtering:

- `http://localhost:8000/books/advanced/?available=true`
- `http://localhost:8000/books/advanced/?min_price=50000&max_price=200000`

## 📊 API Endpoints

### Main Endpoints:

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/books/` | List all books |
| POST | `/books/` | Create new book |
| GET | `/books/{id}/` | Get single book |
| PUT | `/books/{id}/` | Full update |
| PATCH | `/books/{id}/` | Partial update |
| DELETE | `/books/{id}/` | Delete book |

### Query Parameters:

| Parameter | Example | Description |
|-----------|---------|-------------|
| `page` | `?page=2` | Pagination |
| `page_size` | `?page_size=20` | Items per page |
| `search` | `?search=django` | Search in title, author, description |
| `ordering` | `?ordering=price` | Sort ascending |
| `ordering` | `?ordering=-price` | Sort descending |

## 📝 05-dars bilan taqqoslash

### ❌ Eski usul (Function-based views):

```python
# 05-dars: books/views.py (70+ lines)

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
        # ... 10 more lines
    
    elif request.method == 'PATCH':
        # ... 10 more lines
    
    elif request.method == 'DELETE':
        # ... 5 more lines

# Total: 70+ lines
```

### Yangi usul (Generic Views):

```python
# 06-dars: books/views.py (6 lines!)

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Total: 6 lines! 🎉
```

## Asosiy farqlar

| Feature | 05-dars (Function-based) | 06-dars (Generic Views) |
|---------|-------------------------|------------------------|
| **Code lines** | 70+ | 6 |
| **Error handling** | Manual | Automatic |
| **Validation** | Manual | Automatic |
| **Pagination** | Manual (if needed) | 1 line |
| **Filtering** | Manual | 2 lines |
| **Ordering** | Manual | 2 lines |
| **Readability** | Complex | Simple |
| **Maintenance** | Hard | Easy |
| **DRY principle** | ❌ Repetitive | ✅ No repetition |

## Generic Views afzalliklari

1. ✅ **10 barobar kam kod** - 70 qator → 6 qator
2. ✅ **Avtomatik error handling** - 404, 400, 201, 204 avtomatik
3. ✅ **Avtomatik validation** - Serializer validation ishlaydi
4. ✅ **Built-in features** - Pagination, filtering, ordering tayyor
5. ✅ **DRF standart** - Professional loyihalarda ishlatiladi
6. ✅ **Oson customize** - Kerak bo'lsa method override qiling
7. ✅ **O'qish oson** - Kod tushunarliroq

## views.py'da nimalar bor?

### 1. Main Views (Asosiy):
- `BookListCreateView` - List + Create
- `BookRetrieveUpdateDestroyView` - Retrieve + Update + Delete

### 2. Separate Views (Alohida):
- `BookListView` - Faqat list
- `BookCreateView` - Faqat create
- `BookRetrieveView` - Faqat retrieve
- `BookUpdateView` - Faqat update
- `BookDestroyView` - Faqat delete

### 3. Custom Queryset Views:
- `AvailableBooksView` - Faqat mavjud kitoblar
- `ExpensiveBooksView` - Qimmat kitoblar
- `BooksByAuthorView` - Muallif bo'yicha

### 4. Advanced View:
- `BookAdvancedView` - Custom filtering logic

### 5. Custom Classes:
- `BookPagination` - Custom pagination settings

## O'rganish uchun

1. ✅ `views.py` faylini o'qing - har bir view'ga comment yozilgan
2. ✅ `urls.py` faylini o'qing - barcha endpoint'lar tushuntirilgan
3. ✅ Brauzerda sinab ko'ring - DRF interface bilan o'ynang
4. ✅ 05-dars bilan taqqoslang - farqni his qiling
5. ✅ Custom views yozing - `get_queryset()` override qiling

## 🎓 Keyingi qadamlar

1. ✅ Barcha endpoint'larni brauzerda sinab ko'ring
2. ✅ Postman'da test qiling (7-darsda o'rganasiz)
3. ✅ Custom view yozing (masalan, "New Books" - oxirgi 30 kun ichida chiqgan)
4. ✅ Homework'ni bajaring
5. ✅ 07-darsga o'ting (Postman, Swagger, Testing)

## Savollar?

Agar savol bo'lsa:
- views.py'dagi comment'larni o'qing
- README.md'ni qayta o'qing
- examples/ papkasidagi misollarni ko'ring
- Telegram'da savol bering

Happy coding! 