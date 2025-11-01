# 09-dars: Kod namunalari

Bu papkada 09-dars uchun misol kodlar joylashgan.

## 📁 Fayllar

### 1. put_vs_patch.py
PUT va PATCH metodlari orasidagi farqni ko'rsatuvchi batafsil namunalar.

**O'rganish uchun mavzular:**
- PUT vs PATCH farqi
- Qachon PUT ishlatish
- Qachon PATCH ishlatish
- partial parametri
- Amaliy misollar

### 2. detail_apiview_example.py
BookDetailAPIView uchun to'liq shablon kod.

**Ichida mavjud:**
- GET metodi (bitta kitobni olish)
- PUT metodi (to'liq yangilash)
- PATCH metodi (qisman yangilash)
- DELETE metodi (o'chirish)
- Batafsil izohlar
- Ishlatish misollari

## 🚀 Ishlatish

### Fayllarni o'qish
```bash
# 1. PUT vs PATCH farqini o'rganish
cat examples/put_vs_patch.py

# 2. To'liq shablon kodini ko'rish
cat examples/detail_apiview_example.py
```

### Loyihaga ko'chirish
```bash
# Agar kerak bo'lsa, shablon kodini loyihaga ko'chirishingiz mumkin
cp examples/detail_apiview_example.py code/library-project/books/views.py
```

**⚠️ Eslatma:** Loyihada allaqachon views.py fayli mavjud bo'lishi mumkin. Shuning uchun avval zaxira nusxa oling:
```bash
# Zaxira nusxa
cp code/library-project/books/views.py code/library-project/books/views.py.backup

# Keyin shablon kodini ko'chiring
cp examples/detail_apiview_example.py code/library-project/books/views.py
```

## 📚 O'rganish tartibi

1. **put_vs_patch.py** - Avval PUT va PATCH farqini tushunish
2. **detail_apiview_example.py** - Keyin to'liq kod shablonini o'rganish
3. **../code/** papkasiga o'tish - Amaliyotda qo'llash

## 💡 Asosiy xulosalar

### PUT metodi
```python
# ❌ Barcha maydonlar kerak
PUT /api/books/1/
{
    "title": "Yangi nom",
    "author": "Muallif",
    "isbn": "123-456",
    "price": "50000.00",
    "published_date": "2024-01-01"
}
```

### PATCH metodi
```python
# ✅ Faqat kerakli maydonlar
PATCH /api/books/1/
{
    "price": "60000.00"
}
```

### get_object_or_404
```python
# Avtomatik 404 qaytaradi
book = get_object_or_404(Book, pk=pk)
```

### partial parametri
```python
# PUT - partial=False (barcha maydonlar)
serializer = BookSerializer(book, data=request.data, partial=False)

# PATCH - partial=True (faqat yuborilgan maydonlar)
serializer = BookSerializer(book, data=request.data, partial=True)
```

## 🎯 Keyingi qadam

Bu misollarni o'rgangandan so'ng `../code/library-project/` papkasiga o'ting va amaliyotda qo'llang:

```bash
cd ../code/library-project
python manage.py runserver
```

Keyin API'ni Postman yoki HTTPie orqali sinab ko'ring!