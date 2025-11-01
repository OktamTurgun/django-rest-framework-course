"""
BookDetailAPIView - To'liq shablon
Bitta kitob bilan barcha amallar: GET, PUT, PATCH, DELETE
"""

import sys
import os
import django

# Django loyihaning to‘liq yo‘lini aniqlash
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, 'code', 'library-project')

# code/library-project papkasini Python path'ga qo‘shish
sys.path.append(PROJECT_DIR)

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

# DRF importlari
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Endi bu importlar to‘g‘ri ishlaydi ✅
from books.models import Book
from books.serializers import BookSerializer



class BookDetailAPIView(APIView):
    """
    Bitta kitob bilan ishlashS
    
    Endpoints:
    - GET /api/books/<id>/ - Kitobni olish
    - PUT /api/books/<id>/ - To'liq yangilash
    - PATCH /api/books/<id>/ - Qisman yangilash
    - DELETE /api/books/<id>/ - O'chirish
    """
    
    def get(self, request, pk):
        """
        Bitta kitobni olish
        
        Misol:
        GET /api/books/1/
        
        Response:
        {
            "id": 1,
            "title": "Python dasturlash",
            "author": "John Doe",
            "isbn": "978-3-16-148410-0",
            "price": "50000.00",
            "published_date": "2024-01-15"
        }
        """
        # get_object_or_404 - agar topilmasa 404 qaytaradi
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    
    def put(self, request, pk):
        """
        Kitobni to'liq yangilash (barcha maydonlar kerak)
        
        Misol:
        PUT /api/books/1/
        {
            "title": "Django REST Framework",
            "author": "Jane Smith",
            "isbn": "978-1-23-456789-0",
            "price": "75000.00",
            "published_date": "2024-12-01"
        }
        
        ❌ Agar biror maydon yo'q bo'lsa - xatolik qaytaradi!
        """
        book = get_object_or_404(Book, pk=pk)
        
        # partial=False - barcha maydonlar majburiy (default)
        serializer = BookSerializer(book, data=request.data, partial=False)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        # Xatoliklarni qaytarish
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, pk):
        """
        Kitobni qisman yangilash (faqat kerakli maydonlar)
        
        Misol 1: Faqat narxni yangilash
        PATCH /api/books/1/
        {
            "price": "60000.00"
        }
        
        Misol 2: Nom va narxni yangilash
        PATCH /api/books/1/
        {
            "title": "Yangi nom",
            "price": "60000.00"
        }
        
        ✅ Faqat yuborilgan maydonlar yangilanadi!
        """
        book = get_object_or_404(Book, pk=pk)
        
        # partial=True - faqat yuborilgan maydonlar tekshiriladi
        serializer = BookSerializer(book, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        """
        Kitobni o'chirish
        
        Misol:
        DELETE /api/books/1/
        
        Response:
        {
            "message": "Kitob muvaffaqiyatli o'chirildi"
        }
        Status: 204 No Content
        """
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        
        return Response(
            {"message": "Kitob muvaffaqiyatli o'chirildi"},
            status=status.HTTP_204_NO_CONTENT
        )


# =====================================
# URLS.PY DA RO'YXATDAN O'TKAZISH
# =====================================
"""
from django.urls import path
from .views import BookListAPIView, BookDetailAPIView

urlpatterns = [
    path('books/', BookListAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
]
"""


# =====================================
# POSTMAN/HTTPIE BILAN SINASH
# =====================================
"""
# 1️⃣ Kitobni olish
GET http://127.0.0.1:8000/api/books/1/

# 2️⃣ Faqat narxni yangilash (PATCH)
PATCH http://127.0.0.1:8000/api/books/1/
{
    "price": "60000.00"
}

# 3️⃣ To'liq yangilash (PUT)
PUT http://127.0.0.1:8000/api/books/1/
{
    "title": "Yangi kitob",
    "author": "Yangi muallif",
    "isbn": "978-9-99-999999-9",
    "price": "80000.00",
    "published_date": "2024-12-15"
}

# 4️⃣ Kitobni o'chirish
DELETE http://127.0.0.1:8000/api/books/1/
"""


# =====================================
# MUHIM ESLATMALAR
# =====================================
"""
✅ get_object_or_404:
- Avtomatik 404 xatolik qaytaradi
- try-except yozish shart emas
- Kod tozaroq va qisqaroq

✅ partial parametri:
- partial=False (PUT) - barcha maydonlar kerak
- partial=True (PATCH) - faqat yuborilgan maydonlar

✅ Status kodlar:
- 200 OK - muvaffaqiyatli GET, PUT, PATCH
- 204 No Content - muvaffaqiyatli DELETE
- 400 Bad Request - validatsiya xatoligi
- 404 Not Found - topilmadi

✅ PATCH vs PUT:
- PATCH - ko'proq ishlatiladi (xavfsizroq)
- PUT - kamroq ishlatiladi (to'liq yangilash)
"""