# Code Examples - Function-based Views CRUD

> Bu papkada Function-based views bilan CRUD operatsiyalarining to'liq kod namunalari mavjud.

---

## 📁 Fayllar

| Fayl | Tavsif |
|------|---------|
| `models.py` | Book modeli - to'liq versiya |
| `serializers.py` | 3 xil serializer (List, Create, Detail) |
| `views.py` | CRUD + Search + Stats views |
| `urls.py` | URL routing va dokumentatsiya |

---

## 🚀 Qanday ishlatish

### 1. Modelni yaratish

`models.py` ni o'z Django app'ingizga nusxalang va migrate qiling:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Serializer'larni qo'shish

`serializers.py` ni nusxalang va kerakli import'larni tekshiring.

### 3. Views'larni qo'shish

`views.py` ni nusxalang.

### 4. URL'larni sozlash

**App's urls.py:**
```python
# books/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book-list'),
    path('search/', views.book_search, name='book-search'),
    path('stats/', views.book_stats, name='book-stats'),
    path('<int:pk>/', views.book_detail, name='book-detail'),
    path('<int:pk>/toggle/', views.toggle_availability, name='book-toggle'),
]
```

**Project's urls.py:**
```python
# library_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/books/', include('books.urls')),
]
```

---

## 📚 API Endpoints

### **List & Create**

**GET /api/books/**
```bash
curl http://localhost:8000/api/books/
```

**Response:**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "title": "Python Programming",
      "author": "John Doe",
      "price": "29.99",
      "is_available": true
    }
  ]
}
```

---

**POST /api/books/**
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Django for Beginners",
    "author": "William Vincent",
    "isbn": "9876543210123",
    "price": "39.99",
    "published_date": "2024-01-15",
    "pages": 300,
    "language": "English"
  }'
```

---

### **Search**

**GET /api/books/search/?q=python**
```bash
curl http://localhost:8000/api/books/search/?q=python
```

**Response:**
```json
{
  "query": "python",
  "count": 1,
  "results": [...]
}
```

---

### **Filter**

**GET /api/books/?author=John&available=true**
```bash
curl http://localhost:8000/api/books/?author=John&available=true
```

---

### **Detail Operations**

**GET /api/books/1/**
```bash
curl http://localhost:8000/api/books/1/
```

**PUT /api/books/1/**
```bash
curl -X PUT http://localhost:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Programming (Updated)",
    "author": "John Doe",
    "isbn": "1234567890123",
    "price": "34.99",
    "published_date": "2024-01-15",
    "pages": 350,
    "language": "English",
    "is_available": true
  }'
```

**PATCH /api/books/1/**
```bash
curl -X PATCH http://localhost:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -d '{"price": "34.99"}'
```

**DELETE /api/books/1/**
```bash
curl -X DELETE http://localhost:8000/api/books/1/
```

---

### **Stats**

**GET /api/books/stats/**
```bash
curl http://localhost:8000/api/books/stats/
```

**Response:**
```json
{
  "total_books": 10,
  "available_books": 8,
  "unavailable_books": 2,
  "price_stats": {
    "average": 35.50,
    "max": 99.99,
    "min": 15.00
  },
  "languages": {
    "English": 6,
    "O'zbek": 4
  },
  "most_expensive": {...},
  "cheapest": {...},
  "latest_added": {...}
}
```

---

### **Toggle Availability**

**POST /api/books/1/toggle/**
```bash
curl -X POST http://localhost:8000/api/books/1/toggle/
```

**Response:**
```json
{
  "id": 1,
  "title": "Python Programming",
  "is_available": false,
  "message": "Kitob endi mavjud emas"
}
```

---

## 🎯 Asosiy Features

### ✅ CRUD Operations
- Create (POST)
- Read (GET)
- Update (PUT/PATCH)
- Delete (DELETE)

### ✅ Filtering & Search
- Author bo'yicha filterlash
- Til bo'yicha filterlash
- Mavjudlik bo'yicha filterlash
- Title/Author bo'yicha qidiruv

### ✅ Validation
- ISBN 13 raqam
- Narx musbat
- Sahifalar soni to'g'ri
- Sana kelajakda emas

### ✅ Statistics
- Jami kitoblar
- O'rtacha narx
- Tillar bo'yicha statistika
- Eng qimmat/arzon kitoblar

### ✅ Extra Features
- Mavjudlikni toggle qilish
- Custom serializer'lar
- Query parameters support

---

## 📊 Status Codes

| Code | Ma'nosi | Qachon |
|------|---------|---------|
| 200 | OK | GET, PUT, PATCH success |
| 201 | Created | POST success |
| 204 | No Content | DELETE success |
| 400 | Bad Request | Validation error |
| 404 | Not Found | Resource not found |

---

## 💡 Best Practices

1. **get_object_or_404** - 404 xatoni avtomatik qaytaradi
2. **partial=True** - PATCH uchun muhim
3. **Query params** - filterlash uchun
4. **Multiple serializers** - turli vazifalar uchun
5. **Clear error messages** - foydalanuvchi uchun tushunarli

---

## 🔗 Qo'shimcha

**library-project/** papkasida to'liq ishlaydigan Django loyihasi mavjud.

```bash
cd library-project
python manage.py runserver
```

**Admin panel:**
- URL: http://localhost:8000/admin
- Superuser yarating: `python manage.py createsuperuser`

---

## 📝 Eslatma

Bu kod namunalari ta'lim maqsadida yaratilgan. Production uchun:
- Authentication qo'shing
- Pagination qo'shing
- Throttling sozlang
- Testing yozing
- Documentation qo'shing (Swagger/Redoc)