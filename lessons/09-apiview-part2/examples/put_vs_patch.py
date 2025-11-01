"""
PUT vs PATCH farqi

Bu fayl faqat o'rganish uchun!
Amalda ishlatish uchun views.py ga qo'shing.

PUT - To'liq yangilash (barcha maydonlar kerak)
PATCH - Qisman yangilash (faqat kerakli maydonlar)
"""

# =====================================
# AGAR BU FAYLNI ISHGA TUSHIRMOQCHI BO'LSANGIZ:
# =====================================
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from books.models import Book  # agar books app'ida bo'lsa
# from books.serializers import BookSerializer


# =====================================
# HTTP SO'ROVLAR MISOLLARI
# =====================================

"""
❌ PUT bilan yangilash - NOTO'G'RI
Agar faqat title yuborilsa, qolgan maydonlar null bo'ladi

PUT /api/books/1/
{
    "title": "Yangi nom"
}

Natija: 
{
    "title": "Yangi nom",
    "author": null,      # ❌ O'chib ketdi!
    "price": null,       # ❌ O'chib ketdi!
    "published_date": null  # ❌ O'chib ketdi!
}
"""


"""
✅ PUT bilan yangilash - TO'G'RI
Barcha maydonlarni yuborish kerak

PUT /api/books/1/
{
    "title": "Yangi nom",
    "author": "Eski muallif",
    "price": "50000.00",
    "published_date": "2024-01-01"
}
"""


"""
✅ PATCH bilan yangilash - TO'G'RI
Faqat kerakli maydonlarni yuborish kifoya

PATCH /api/books/1/
{
    "title": "Yangi nom"
}

Natija: Faqat title yangilanadi, qolganlari o'zgarmaydi
{
    "title": "Yangi nom",
    "author": "Eski muallif",    # ✅ Saqlanadi
    "price": "50000.00",          # ✅ Saqlanadi
    "published_date": "2024-01-01"  # ✅ Saqlanadi
}
"""


# =====================================
# DJANGO REST FRAMEWORK DA AMALDA
# =====================================

"""
AMALIY KOD (views.py ga qo'shish uchun):

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer


class BookDetailAPIView(APIView):
    '''
    Bitta kitob bilan ishlash
    '''
    
    def put(self, request, pk):
        '''
        PUT - To'liq yangilash
        Barcha maydonlar majburiy
        '''
        book = get_object_or_404(Book, pk=pk)
        
        # partial=False - barcha maydonlar kerak (default)
        serializer = BookSerializer(book, data=request.data, partial=False)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, pk):
        '''
        PATCH - Qisman yangilash
        Faqat kerakli maydonlar
        '''
        book = get_object_or_404(Book, pk=pk)
        
        # partial=True - faqat yuborilgan maydonlar yangilanadi
        serializer = BookSerializer(book, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""


# =====================================
# FOYDALANISH MISOLLARI (HTTP)
# =====================================

"""
1️⃣ PATCH bilan narxni yangilash
----------------------------------
PATCH /api/books/1/
{
    "price": "60000.00"
}
# ✅ Faqat narx yangilanadi


2️⃣ PATCH bilan bir nechta maydonni yangilash
----------------------------------------------
PATCH /api/books/1/
{
    "title": "Yangi nom",
    "price": "60000.00"
}
# ✅ Faqat title va price yangilanadi


3️⃣ PUT bilan to'liq yangilash
-------------------------------
PUT /api/books/1/
{
    "title": "To'liq yangi kitob",
    "author": "Yangi muallif",
    "isbn": "978-3-16-148410-0",
    "price": "75000.00",
    "published_date": "2024-12-01"
}
# ✅ Barcha maydonlar yangilanadi


4️⃣ PUT bilan qisman yangilash - XATO
--------------------------------------
PUT /api/books/1/
{
    "title": "Yangi nom"
}
# ❌ Xatolik: author, isbn, price, published_date majburiy!
"""


# =====================================
# HTTPIE BILAN SINASH
# =====================================

"""
# PATCH misoli
http PATCH http://127.0.0.1:8000/api/books/1/ price="60000.00"

# PUT misoli
http PUT http://127.0.0.1:8000/api/books/1/ \
    title="Yangi kitob" \
    author="Muallif" \
    isbn="123-456-789" \
    price="50000.00" \
    published_date="2024-01-01"
"""


# =====================================
# CURL BILAN SINASH
# =====================================

"""
# PATCH misoli
curl -X PATCH http://127.0.0.1:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -d '{"price": "60000.00"}'

# PUT misoli
curl -X PUT http://127.0.0.1:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Yangi kitob",
    "author": "Muallif",
    "isbn": "123-456-789",
    "price": "50000.00",
    "published_date": "2024-01-01"
  }'
"""


# =====================================
# QACHON NIMA ISHLATISH KERAK?
# =====================================

"""
✅ PATCH ishlatish kerak:
------------------------
- Faqat bitta maydonni yangilash
- Bir nechta maydonni yangilash
- Foydalanuvchi barcha ma'lumotni yubormasa
- Ko'pchilik hollarda PATCH ishlatiladi
- Xavfsizroq va oddiyroq

✅ PUT ishlatish kerak:
-----------------------
- Butun resursni almashtirish
- Barcha ma'lumotlar mavjud
- To'liq yangilash kerak bo'lsa
- Kamroq ishlatiladi

🎯 Tavsiya: 
-----------
PATCH ishlatish osonroq va xavfsizroq!
Ko'pchilik loyihalarda PATCH ishlatiladi.
"""


# =====================================
# ASOSIY FARQLAR JADVALI
# =====================================

"""
┌─────────────────┬────────────────────┬─────────────────────┐
│     Xususiyat   │        PUT         │       PATCH         │
├─────────────────┼────────────────────┼─────────────────────┤
│ Barcha maydonlar│   Majburiy ✓      │   Ixtiyoriy         │
│ partial         │   False            │   True              │
│ Foydalanish     │   Kamroq           │   Ko'proq ✓         │
│ Xavfsizlik      │   Past             │   Yuqori ✓          │
│ Oddiylik        │   Murakkab         │   Oson ✓            │
└─────────────────┴────────────────────┴─────────────────────┘
"""


# =====================================
# MUHIM ESLATMALAR
# =====================================

"""
⚠️ ESLATMA 1: partial parametri
--------------------------------
# PUT uchun
serializer = BookSerializer(book, data=request.data, partial=False)

# PATCH uchun
serializer = BookSerializer(book, data=request.data, partial=True)


⚠️ ESLATMA 2: Validatsiya
--------------------------
PUT uchun barcha maydonlar tekshiriladi.
PATCH uchun faqat yuborilgan maydonlar tekshiriladi.


⚠️ ESLATMA 3: Amaliyot
-----------------------
Real loyihalarda ko'proq PATCH ishlatiladi,
chunki u oddiy va xavfsizroq.
"""