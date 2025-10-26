"""
Generic Views - Basic Examples
==============================

Bu faylda Generic Views'ning asosiy misollari keltirilgan.
Har bir misolni o'z loyihangizga copy-paste qilishingiz mumkin!
"""

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

# Modellar (misol uchun)
# from .models import Book, Author, Category
# from .serializers import BookSerializer, AuthorSerializer, CategorySerializer


# =============================================================================
# 1. ListAPIView - Faqat ro'yxat
# =============================================================================

class BookListView(generics.ListAPIView):
    """
    Faqat GET request
    Barcha kitoblarni qaytaradi
    
    Endpoint: GET /books/list/
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    pass


# =============================================================================
# 2. CreateAPIView - Faqat yaratish
# =============================================================================

class BookCreateView(generics.CreateAPIView):
    """
    Faqat POST request
    Yangi kitob yaratadi
    
    Endpoint: POST /books/create/
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    pass


# =============================================================================
# 3. RetrieveAPIView - Faqat bitta obyektni olish
# =============================================================================

class BookDetailView(generics.RetrieveAPIView):
    """
    Faqat GET request (bitta obyekt)
    ID bo'yicha kitobni qaytaradi
    
    Endpoint: GET /books/{id}/
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    pass


# =============================================================================
# 4. UpdateAPIView - Faqat yangilash
# =============================================================================

class BookUpdateView(generics.UpdateAPIView):
    """
    PUT va PATCH requests
    Kitobni yangilaydi
    
    Endpoints:
    - PUT /books/{id}/update/  (to'liq yangilash)
    - PATCH /books/{id}/update/  (qisman yangilash)
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    pass


# =============================================================================
# 5. DestroyAPIView - Faqat o'chirish
# =============================================================================

class BookDeleteView(generics.DestroyAPIView):
    """
    Faqat DELETE request
    Kitobni o'chiradi
    
    Endpoint: DELETE /books/{id}/delete/
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    pass


# =============================================================================
# 6. ListCreateAPIView - Ro'yxat + Yaratish (ENG KO'P ISHLATILADIGAN!)
# =============================================================================

class BookListCreateView(generics.ListCreateAPIView):
    """
    GET va POST requests
    
    Endpoints:
    - GET /books/  (ro'yxat)
    - POST /books/  (yangi kitob)
    
    Bu eng ko'p ishlatiladigan generic view!
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    pass


# =============================================================================
# 7. RetrieveUpdateAPIView - Olish + Yangilash
# =============================================================================

class BookRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    GET, PUT, PATCH requests
    
    Endpoints:
    - GET /books/{id}/  (bitta kitob)
    - PUT /books/{id}/  (to'liq yangilash)
    - PATCH /books/{id}/  (qisman yangilash)
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    pass


# =============================================================================
# 8. RetrieveDestroyAPIView - Olish + O'chirish
# =============================================================================

class BookRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    """
    GET va DELETE requests
    
    Endpoints:
    - GET /books/{id}/  (bitta kitob)
    - DELETE /books/{id}/  (o'chirish)
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    pass


# =============================================================================
# 9. RetrieveUpdateDestroyAPIView - Olish + Yangilash + O'chirish
#    (ENG KO'P ISHLATILADIGAN!)
# =============================================================================

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET, PUT, PATCH, DELETE requests
    
    Endpoints:
    - GET /books/{id}/  (bitta kitob)
    - PUT /books/{id}/  (to'liq yangilash)
    - PATCH /books/{id}/  (qisman yangilash)
    - DELETE /books/{id}/  (o'chirish)
    
    Bu ham eng ko'p ishlatiladigan generic view!
    Detail endpoint uchun barcha CRUD operatsiyalar.
    """
    # queryset = Book.objects.all()
    # serializer_class = BookSerializer
    pass


# =============================================================================
# REAL MISOL: To'liq kod
# =============================================================================

# Uncomment qiling va ishlatishingiz mumkin:

"""
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

# Ro'yxat + Yaratish
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Olish + Yangilash + O'chirish
class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
"""


# =============================================================================
# URLs.PY uchun
# =============================================================================

"""
from django.urls import path
from .views import BookListCreateView, BookRetrieveUpdateDestroyView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
]
"""


# =============================================================================
# QANDAY TANLASH?
# =============================================================================

"""
Vazifangizga qarab tanlang:

1. Faqat ro'yxat kerak:
   → ListAPIView

2. Faqat yaratish kerak:
   → CreateAPIView

3. Ro'yxat + Yaratish kerak (API list endpoint):
   → ListCreateAPIView ✅ (Ko'p ishlatiladi)

4. Bitta obyekt: Olish + Yangilash + O'chirish (API detail endpoint):
   → RetrieveUpdateDestroyAPIView ✅ (Ko'p ishlatiladi)

5. Maxsus kombinatsiya kerak:
   → Mixins'lardan foydalaning
"""


# =============================================================================
# KEYINGI QADAMLAR
# =============================================================================

"""
1. custom_queryset.py'ni o'qing - QuerySet'ni sozlash
2. filtering_example.py'ni o'qing - Filtering qo'shish
3. pagination_example.py'ni o'qing - Pagination qo'shish
4. O'z loyihangizda amalda qo'llang!
"""