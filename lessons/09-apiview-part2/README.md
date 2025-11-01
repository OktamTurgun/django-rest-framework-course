# 09-dars: APIView Part 2 - Detail Operations

Bu darsda bitta obyekt bilan ishlashni o'rganamiz: GET, PUT, PATCH, DELETE metodlari.

## 📚 Dars maqsadi

- ✅ Bitta obyektni olish (Retrieve)
- ✅ To'liq yangilash (PUT)
- ✅ Qisman yangilash (PATCH)
- ✅ O'chirish (DELETE)
- ✅ PUT vs PATCH farqi
- ✅ get_object_or_404 ishlatish

## 📁 Fayl strukturasi

```
09-apiview-part2/
├── code/
│   ├── README.md                    # Loyiha bo'yicha yo'riqnoma
│   └── library-project/
│       ├── books/
│       │   ├── views.py             # BookDetailAPIView qo'shildi
│       │   ├── urls.py              # Detail endpoint qo'shildi
│       │   ├── models.py
│       │   ├── serializers.py
│       │   └── ...
│       ├── library_project/
│       ├── manage.py
│       └── ...
├── examples/
│   ├── put_vs_patch.py              # PUT va PATCH farqi
│   ├── detail_apiview_example.py    # To'liq kod namunasi
│   └── README.md                    # Examples bo'yicha yo'riqnoma
├── README.md                        # Siz hozir shu faylni o'qiyapsiz
└── homework.md                      # Uyga vazifa
```

## 🎯 Asosiy tushunchalar

### 1. BookDetailAPIView

Bitta kitob bilan ishlash uchun APIView:

```python
class BookDetailAPIView(APIView):
    def get(self, request, pk):
        """Bitta kitobni olish"""
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """To'liq yangilash (barcha maydonlar)"""
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, pk):
        """Qisman yangilash (faqat kerakli maydonlar)"""
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        """O'chirish"""
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response({"message": "Kitob o'chirildi"}, status=204)
```

### 2. URL routing

```python
# books/urls.py
urlpatterns = [
    path('books/', BookListAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
]
```

### 3. PUT vs PATCH

| Xususiyat | PUT | PATCH |
|-----------|-----|-------|
| Barcha maydonlar | ✅ Majburiy | ❌ Ixtiyoriy |
| partial parametri | False | True |
| Ishlatilishi | Kamroq | Ko'proq ✅ |
| Xavfsizlik | Past | Yuqori ✅ |

**Misol:**

```bash
# PATCH - faqat narxni yangilash ✅
PATCH /api/books/1/
{"price": "60000.00"}

# PUT - barcha maydonlar kerak ⚠️
PUT /api/books/1/
{
    "title": "Kitob",
    "author": "Muallif",
    "isbn": "123-456",
    "price": "50000.00",
    "published_date": "2024-01-01"
}
```

## 🚀 Ishga tushirish

### 1. Virtual muhitni faollashtirish
```bash
cd code/library-project
pipenv shell  # yoki: source venv/bin/activate
```

### 2. Serverni ishga tushirish
```bash
python manage.py runserver
```

### 3. API'ni sinash
```bash
# Kitobni olish
http GET http://127.0.0.1:8000/api/books/1/

# Narxni yangilash (PATCH)
http PATCH http://127.0.0.1:8000/api/books/1/ price="60000.00"

# To'liq yangilash (PUT)
http PUT http://127.0.0.1:8000/api/books/1/ \
  title="Yangi kitob" \
  author="Muallif" \
  isbn="123-456" \
  price="50000.00" \
  published_date="2024-01-01"

# O'chirish
http DELETE http://127.0.0.1:8000/api/books/1/
```

## 📖 O'rganish tartibi

1. **`examples/put_vs_patch.py`** - PUT va PATCH farqini tushunish
2. **`examples/detail_apiview_example.py`** - To'liq kod shablonini ko'rish
3. **`code/library-project/`** - Amaliyotda qo'llash
4. **`homework.md`** - Mustaqil amaliyot

## 🎓 Homework

Vazifalar `homework.md` faylida:
- ✅ Author modeli va API yaratish
- ✅ Category modeli va API yaratish
- ✅ BookReview modeli va API yaratish
- ✅ Barcha CRUD operatsiyalarini qo'llash

## 📚 Qo'shimcha materiallar

### Status kodlar
- `200 OK` - Muvaffaqiyatli GET, PUT, PATCH
- `201 Created` - Yangi obyekt yaratildi
- `204 No Content` - Muvaffaqiyatli DELETE
- `400 Bad Request` - Validatsiya xatoligi
- `404 Not Found` - Obyekt topilmadi

### get_object_or_404
```python
# Manual try-except
try:
    book = Book.objects.get(pk=pk)
except Book.DoesNotExist:
    return Response({'error': 'Topilmadi'}, status=404)

# get_object_or_404 (osonroq) ✅
book = get_object_or_404(Book, pk=pk)
```

### partial parametri
```python
# PUT uchun
serializer = BookSerializer(instance, data=data, partial=False)

# PATCH uchun
serializer = BookSerializer(instance, data=data, partial=True)
```

## ⚠️ Muhim eslatmalar

1. **PATCH ishlatish afzalroq** - foydalanuvchi barcha ma'lumotni yuborishi shart emas
2. **get_object_or_404** - avtomatik 404 qaytaradi, try-except kerak emas
3. **partial=True** - PATCH uchun majburiy!
4. **URL pattern** - `<int:pk>` parametrini unutmang

## 🔗 Foydali linklar

- [Django REST Framework - APIView](https://www.django-rest-framework.org/api-guide/views/)
- [HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- [Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

## 📞 Yordam

Agar savol yoki muammo bo'lsa:
1. `examples/` papkasidagi kod namunalarini ko'ring
2. `code/README.md` faylini o'qing
3. O'qituvchidan so'rang

---

**Keyingi dars:** 10-dars - Generics va ViewSets

**Oldingi dars:** 08-dars - APIView Part 1 - List & Create