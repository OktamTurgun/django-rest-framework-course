"""
Pagination Examples
===================

Django REST Framework'ning turli pagination turlari.
"""
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
    CursorPagination
)

# from .models import Book
# from .serializers import BookSerializer


# =============================================================================
# 1. PageNumberPagination - Eng ko'p ishlatiladigan!
# =============================================================================

class StandardPagination(PageNumberPagination):
    """
    Standard pagination - sahifa raqami bo'yicha
    
    Examples:
    - GET /books/?page=1
    - GET /books/?page=2
    - GET /books/?page=3
    
    Response:
    {
        "count": 100,
        "next": "http://localhost:8000/books/?page=2",
        "previous": null,
        "results": [...]
    }
    """
    page_size = 10  # Har bir sahifada 10 ta element
    page_size_query_param = 'page_size'  # User page_size o'zgartirishi mumkin
    max_page_size = 100  # Maksimum 100 ta element


class BookListView(generics.ListAPIView):
    """
    Standard pagination bilan books
    
    Examples:
    - GET /books/?page=1
    - GET /books/?page=2&page_size=20
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    pagination_class = StandardPagination


# =============================================================================
# 2. Small Pagination - Kichik sahifalar
# =============================================================================

class SmallPagination(PageNumberPagination):
    """
    Kichik pagination - 5 ta element
    Mobile apps uchun yaxshi
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


class BookSmallListView(generics.ListAPIView):
    """GET /books/small/?page=1"""
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    pagination_class = SmallPagination


# =============================================================================
# 3. Large Pagination - Katta sahifalar
# =============================================================================

class LargePagination(PageNumberPagination):
    """
    Katta pagination - 50 ta element
    Admin panel uchun yaxshi
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class BookLargeListView(generics.ListAPIView):
    """GET /books/large/?page=1"""
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    pagination_class = LargePagination


# =============================================================================
# 4. LimitOffsetPagination - Limit va Offset
# =============================================================================

class LimitOffsetPaginationExample(LimitOffsetPagination):
    """
    Limit-Offset pagination
    
    Examples:
    - GET /books/?limit=10&offset=0   (birinchi 10 ta)
    - GET /books/?limit=10&offset=10  (keyingi 10 ta)
    - GET /books/?limit=20&offset=40  (40-60 oralig'i)
    
    Response:
    {
        "count": 100,
        "next": "http://localhost:8000/books/?limit=10&offset=10",
        "previous": null,
        "results": [...]
    }
    """
    default_limit = 10  # Default limit
    max_limit = 100  # Maksimum limit


class BookLimitOffsetView(generics.ListAPIView):
    """GET /books/limit-offset/?limit=20&offset=40"""
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    pagination_class = LimitOffsetPaginationExample


# =============================================================================
# 5. CursorPagination - Eng tez va xavfsiz
# =============================================================================

class CursorPaginationExample(CursorPagination):
    """
    Cursor pagination - eng tez va xavfsiz
    
    Afzalliklari:
    - Juda tez (database index ishlatadi)
    - User sahifa raqamini ko'ra olmaydi (xavfsizroq)
    - Yangi ma'lumotlar qo'shilganda muammo yo'q
    
    Kamchiligi:
    - Faqat next/previous (sahifa raqamiga o'tib bo'lmaydi)
    
    Examples:
    - GET /books/
    - GET /books/?cursor=cD0yMDIz...  (next cursor)
    
    Response:
    {
        "next": "http://localhost:8000/books/?cursor=cD0yMDIz...",
        "previous": null,
        "results": [...]
    }
    """
    page_size = 10
    ordering = '-publish_date'  # Ordering majburiy!
    cursor_query_param = 'cursor'


class BookCursorView(generics.ListAPIView):
    """
    GET /books/cursor/
    
    User faqat next/previous tugmasini bosadi
    Sahifa raqamini ko'rmaydi
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    pagination_class = CursorPaginationExample


# =============================================================================
# 6. No Pagination - Barcha ma'lumotlar
# =============================================================================

class BookNoPaginationView(generics.ListAPIView):
    """
    Pagination yo'q - barcha kitoblar bir safar qaytariladi
    
    DIQQAT: Faqat kichik ma'lumotlar uchun!
    1000+ ta kitob bo'lsa, juda sekin ishlaydi!
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    pagination_class = None  # Pagination o'chirish


# =============================================================================
# 7. Custom Pagination - Maxsus sozlamalar
# =============================================================================

class CustomPagination(PageNumberPagination):
    """
    Custom pagination - response formatini o'zgartirish
    
    Response:
    {
        "total": 100,
        "page": 1,
        "page_size": 10,
        "total_pages": 10,
        "data": [...]
    }
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'page': self.page.number,
            'page_size': self.page_size,
            'total_pages': self.page.paginator.num_pages,
            'data': data
        })


# =============================================================================
# REAL FULL EXAMPLE
# =============================================================================

"""
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Book
from .serializers import BookSerializer

class BookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

# URL examples:
# GET /books/                      → 1-10
# GET /books/?page=2               → 11-20
# GET /books/?page=3&page_size=20  → 41-60 (20 ta element)
"""


# =============================================================================
# SETTINGS.PY - Global Pagination
# =============================================================================

"""
# settings.py

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Agar global qo'shsangiz, barcha ListAPIView'larda pagination ishlaydi
# Agar faqat bitta view'da kerak bo'lsa, view'da pagination_class qo'shing
"""


# =============================================================================
# PAGINATION TYPES - Qachon qaysi birini ishlatish?
# =============================================================================

"""
1. PageNumberPagination - ENG KO'P ISHLATILADIGAN ✅
   Afzalliklari:
   - User sahifa raqamiga o'tishi mumkin (page=5)
   - Tushunarli va oddiy
   - Barcha holatlar uchun yaxshi
   
   Qachon ishlatish:
   - Web application'lar
   - Admin panel'lar
   - Default tanlov
   
   Example: ?page=3&page_size=20

2. LimitOffsetPagination
   Afzalliklari:
   - Flexible - istalgan offset'ga o'tish mumkin
   - SQL LIMIT OFFSET'ga o'xshaydi
   
   Qachon ishlatish:
   - API client'lar
   - Developer-friendly API'lar
   
   Example: ?limit=20&offset=40

3. CursorPagination - ENG TEZ ✅
   Afzalliklari:
   - Juda tez (database index)
   - Xavfsiz (sahifa raqami yo'q)
   - Yangi ma'lumotlar qo'shilganda muammo yo'q
   
   Kamchiliklari:
   - Faqat next/previous
   - Sahifa raqamiga o'tib bo'lmaydi
   
   Qachon ishlatish:
   - Ko'p ma'lumot (1,000,000+ records)
   - Real-time feed'lar (Instagram, Twitter)
   - Mobile apps
   
   Example: ?cursor=cD0yMDIz...

4. No Pagination
   Qachon ishlatish:
   - Juda kam ma'lumot (< 100 ta)
   - Dropdown'lar uchun
   
   DIQQAT: Ko'p ma'lumot bilan ISHLATMANG!
"""


# =============================================================================
# PAGINATION RESPONSE FORMAT
# =============================================================================

"""
PageNumberPagination response:
{
    "count": 100,                                        # Jami elementlar soni
    "next": "http://localhost:8000/books/?page=3",      # Keyingi sahifa
    "previous": "http://localhost:8000/books/?page=1",  # Oldingi sahifa
    "results": [                                         # Hozirgi sahifa ma'lumotlari
        {"id": 11, "title": "Book 11", ...},
        {"id": 12, "title": "Book 12", ...},
        ...
    ]
}

LimitOffsetPagination response:
{
    "count": 100,
    "next": "http://localhost:8000/books/?limit=10&offset=20",
    "previous": "http://localhost:8000/books/?limit=10&offset=0",
    "results": [...]
}

CursorPagination response:
{
    "next": "http://localhost:8000/books/?cursor=cD0yMDIzLT...",
    "previous": "http://localhost:8000/books/?cursor=cj0xJnA...",
    "results": [...]
}
"""


# =============================================================================
# FRONTEND INTEGRATION
# =============================================================================

"""
JavaScript example (PageNumberPagination):

async function getBooks(page = 1, pageSize = 10) {
    const response = await fetch(
        `http://localhost:8000/books/?page=${page}&page_size=${pageSize}`
    );
    const data = await response.json();
    
    console.log('Total:', data.count);
    console.log('Current page:', page);
    console.log('Books:', data.results);
    console.log('Next page:', data.next);
    console.log('Previous page:', data.previous);
    
    return data;
}

// Usage:
getBooks(1, 20);  // Birinchi sahifa, 20 ta kitob
"""


# =============================================================================
# PERFORMANCE TIPS
# =============================================================================

"""
1. Database Index qo'shing:
   class Book(models.Model):
       publish_date = models.DateField(db_index=True)  # ← Index!
       
2. Katta ma'lumot uchun CursorPagination ishlatiladi
   - 1,000,000+ records
   - Real-time feeds

3. Select_related / Prefetch_related ishlatiladi:
   queryset = Book.objects.select_related('author').all()
   
4. Page size'ni cheklang:
   max_page_size = 100  # User 1000 ta so'ramasin!

5. Count query'ni cache'lang (agar mumkin bo'lsa)
"""


# =============================================================================
# MASLAHATLAR
# =============================================================================

"""
1. Default: PageNumberPagination ishlatiladi ✅
   Eng oddiy va eng tushunarli

2. page_size_query_param qo'shing:
   User o'zi page_size o'zgartirishi mumkin

3. max_page_size qo'ying:
   User 10000 ta element so'ramasin

4. Default ordering qo'ying:
   ordering = ['-publish_date']

5. Frontend'da pagination UI qo'shing:
   - Previous/Next tugmalari
   - Sahifa raqamlari
   - "10 / 20 / 50" tanlovlar

6. Mobile uchun kichik page_size:
   page_size = 5-10

7. Desktop uchun katta page_size:
   page_size = 20-50
"""


# =============================================================================
# KEYINGI QADAMLAR
# =============================================================================

"""
1. O'z loyihangizda pagination qo'shing
2. Turli page_size'larni sinab ko'ring
3. Brauzerda next/previous'ni test qiling
4. Frontend'da pagination UI yarating
5. CursorPagination'ni sinab ko'ring (performance uchun)
"""