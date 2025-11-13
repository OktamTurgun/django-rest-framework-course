"""
04 - Router Comparison
SimpleRouter vs DefaultRouter farqi
"""

from rest_framework.routers import SimpleRouter, DefaultRouter
from .views import BookViewSet, AuthorViewSet, BookV2ViewSet
from django.urls import path, include
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer


# ============================================
# 1. SIMPLE ROUTER
# ============================================
simple_router = SimpleRouter()
simple_router.register(r'books', BookViewSet)

# Simple Router yaratadigan URL'lar:
"""
/books/                    -> list, create
/books/{pk}/              -> retrieve, update, destroy
/books/{pk}/publish/      -> custom action
"""


# ============================================
# 2. DEFAULT ROUTER
# ============================================
default_router = DefaultRouter()
default_router.register(r'books', BookViewSet)

# Default Router yaratadigan URL'lar:
"""
/                         -> API root view (QOSHIMCHA!)
/books/                   -> list, create
/books.json              -> list with .json format (QOSHIMCHA!)
/books/{pk}/             -> retrieve, update, destroy
/books/{pk}.json         -> retrieve with .json format (QOSHIMCHA!)
/books/{pk}/publish/     -> custom action
"""


# ============================================
# 3. FARQI
# ============================================
"""
SimpleRouter:
✅ Yengil
✅ Faqat kerakli URL'lar
❌ API root yo'q
❌ Format suffix yo'q

DefaultRouter:
✅ API root mavjud (barcha endpoint'lar ko'rinadi)
✅ Format suffix (.json, .xml)
✅ Browsable API'da qulay
❌ Bir oz og'irroq
"""


# ============================================
# 4. QACHON QAYSI BIRINI ISHLATISH
# ============================================
"""
SimpleRouter ishlatish:
- Production API
- Mobil app backend
- Format suffix kerak emas
- Minimal API

DefaultRouter ishlatish:
- Development
- Browsable API kerak
- API documentation ko'rsatish kerak
- Format suffix kerak (JSON, XML)
"""


# ============================================
# 5. MULTIPLE ROUTERS
# ============================================
# Bir nechta router'larni birlashtirish mumkin

router_v1 = DefaultRouter()
router_v1.register(r'books', BookViewSet)
router_v1.register(r'authors', AuthorViewSet)

router_v2 = DefaultRouter()
router_v2.register(r'books', BookV2ViewSet)

# urls.py da:
urlpatterns = [
    path('api/v1/', include(router_v1.urls)),
    path('api/v2/', include(router_v2.urls)),
]


# ============================================
# 6. CUSTOM BASENAME
# ============================================
# Agar queryset yo'q bo'lsa, basename kerak

class DynamicBookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        # Dinamik queryset
        user = self.request.user
        return Book.objects.filter(owner=user)

# Router'da basename ko'rsatish SHART:
router.register(r'my-books', 
                DynamicBookViewSet, 
                basename='mybook')  # basename KERAK!


# ============================================
# 7. URL PREFIX
# ============================================
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'api/books', BookViewSet)  # URL'da 'api/' bo'ladi

# Yoki:
urlpatterns = [
    path('api/', include(router.urls)),  # Barcha URL'larga 'api/' prefix
]


# ============================================
# 8. TRAILING SLASH
# ============================================
# URL oxiridagi / ni o'chirish
router = DefaultRouter(trailing_slash=False)
router.register(r'books', BookViewSet)

# URL'lar:
# /books (slash yo'q)
# /books/{pk} (slash yo'q)