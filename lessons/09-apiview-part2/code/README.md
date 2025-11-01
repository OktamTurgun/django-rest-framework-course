# Library Project - BookDetailAPIView

Bu loyihada bitta kitob bilan ishlash uchun `BookDetailAPIView` yaratilgan.

## 🎯 Nima qo'shildi?

### 1. BookDetailAPIView (books/views.py)
Bitta kitob bilan ishlash uchun APIView:
- ✅ GET - kitobni olish
- ✅ PUT - to'liq yangilash
- ✅ PATCH - qisman yangilash
- ✅ DELETE - o'chirish

### 2. URL routing (books/urls.py)
```python
path('books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail')
```

## 🚀 Ishga tushirish

```bash
# Virtual muhitni faollashtirish
cd code/library-project
pipenv shell  # yoki source venv/bin/activate

# Serverni ishga tushirish
python manage.py runserver
```

## 📝 API Endpoints

### 1. Barcha kitoblar (List)
```
GET http://127.0.0.1:8000/api/books/
POST http://127.0.0.1:8000/api/books/
```

### 2. Bitta kitob (Detail)
```
GET    http://127.0.0.1:8000/api/books/1/
PUT    http://127.0.0.1:8000/api/books/1/
PATCH  http://127.0.0.1:8000/api/books/1/
DELETE http://127.0.0.1:8000/api/books/1/
```

## 🧪 Sinash misollari

### 1️⃣ Kitobni olish (GET)
```bash
# HTTPie
http GET http://127.0.0.1:8000/api/books/1/

# curl
curl http://127.0.0.1:8000/api/books/1/
```

**Response:**
```json
{
    "id": 1,
    "title": "Python dasturlash",
    "author": "John Doe",
    "isbn": "978-3-16-148410-0",
    "price": "50000.00",
    "published_date": "2024-01-15"
}
```

### 2️⃣ Faqat narxni yangilash (PATCH)
```bash
# HTTPie
http PATCH http://127.0.0.1:8000/api/books/1/ price="60000.00"

# curl
curl -X PATCH http://127.0.0.1:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -d '{"price": "60000.00"}'
```

### 3️⃣ To'liq yangilash (PUT)
```bash
# HTTPie
http PUT http://127.0.0.1:8000/api/books/1/ \
  title="Django REST Framework" \
  author="Jane Smith" \
  isbn="978-1-23-456789-0" \
  price="75000.00" \
  published_date="2024-12-01"

# curl
curl -X PUT http://127.0.0.1:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Django REST Framework",
    "author": "Jane Smith",
    "isbn": "978-1-23-456789-0",
    "price": "75000.00",
    "published_date": "2024-12-01"
  }'
```

### 4️⃣ Kitobni o'chirish (DELETE)
```bash
# HTTPie
http DELETE http://127.0.0.1:8000/api/books/1/

# curl
curl -X DELETE http://127.0.0.1:8000/api/books/1/
```

**Response:**
```json
{
    "message": "Kitob muvaffaqiyatli o'chirildi"
}
```

## 📊 Postman Collection

### GET Request
```
Method: GET
URL: http://127.0.0.1:8000/api/books/1/
Headers: (yo'q)
Body: (yo'q)
```

### PATCH Request
```
Method: PATCH
URL: http://127.0.0.1:8000/api/books/1/
Headers: Content-Type: application/json
Body (raw JSON):
{
    "price": "60000.00"
}
```

### PUT Request
```
Method: PUT
URL: http://127.0.0.1:8000/api/books/1/
Headers: Content-Type: application/json
Body (raw JSON):
{
    "title": "Yangi kitob",
    "author": "Yangi muallif",
    "isbn": "978-9-99-999999-9",
    "price": "80000.00",
    "published_date": "2024-12-15"
}
```

### DELETE Request
```
Method: DELETE
URL: http://127.0.0.1:8000/api/books/1/
Headers: (yo'q)
Body: (yo'q)
```

## ⚠️ Muhim eslatmalar

### PUT vs PATCH
- **PUT** - barcha maydonlar majburiy
- **PATCH** - faqat kerakli maydonlar (tavsiya etiladi)

### get_object_or_404
- Agar kitob topilmasa avtomatik 404 qaytaradi
- try-except yozish shart emas

### Status kodlar
- `200 OK` - muvaffaqiyatli GET, PUT, PATCH
- `204 No Content` - muvaffaqiyatli DELETE
- `400 Bad Request` - validatsiya xatoligi
- `404 Not Found` - kitob topilmadi

## 📁 Fayl tuzilishi

```
library-project/
├── books/
│   ├── views.py          # BookListAPIView va BookDetailAPIView
│   ├── urls.py           # API URL'lar
│   ├── models.py         # Book modeli
│   ├── serializers.py    # BookSerializer
│   └── ...
├── library_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── manage.py
└── ...
```

## 🔧 Troubleshooting

### Xatolik: 404 Not Found
```bash
# Ma'lumotlar bazasida kitoblar borligini tekshiring
python manage.py shell
>>> from books.models import Book
>>> Book.objects.all()
```

### Xatolik: Method Not Allowed
URL to'g'ri ekanligini tekshiring:
- ✅ `http://127.0.0.1:8000/api/books/1/`
- ❌ `http://127.0.0.1:8000/api/books/1`

### Xatolik: Validation Error (PUT)
PUT uchun barcha maydonlar kerakligini eslang:
```json
{
    "title": "Kitob nomi",
    "author": "Muallif",
    "isbn": "123-456-789",
    "price": "50000.00",
    "published_date": "2024-01-01"
}
```

## 📚 Qo'shimcha o'rganish

Batafsil misol kodlar uchun `../examples/` papkasiga qarang:
- `put_vs_patch.py` - PUT va PATCH farqi
- `detail_apiview_example.py` - To'liq shablon kod

## 🎓 Homework

Vazifalar `../homework.md` faylida mavjud.