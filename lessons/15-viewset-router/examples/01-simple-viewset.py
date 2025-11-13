"""
01 - Simple ViewSet misoli
ModelViewSet - barcha CRUD operatsiyalarini ta'minlaydi
"""

from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer


# 1. Eng oddiy ModelViewSet
class BookViewSet(viewsets.ModelViewSet):
    """
    Faqat 3 qator kod bilan to'liq CRUD API!
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes qo'shishni unutmang!


# 2. Queryset'ni override qilish
class PublishedBookViewSet(viewsets.ModelViewSet):
    """
    Faqat published kitoblarni ko'rsatadi
    """
    serializer_class = BookSerializer
    
    def get_queryset(self):
        return Book.objects.filter(published=True)


# 3. Serializer'ni dinamik tanlash
class DynamicBookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookDetailSerializer


# URLs.py da:
"""
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
"""