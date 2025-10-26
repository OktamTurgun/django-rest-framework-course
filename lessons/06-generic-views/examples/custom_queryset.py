"""
Custom QuerySet Examples
=========================

get_queryset() method'ini override qilib, custom filtering qilish.
"""

from rest_framework import generics
from datetime import datetime, timedelta
from django.db.models import Q

# from .models import Book
# from .serializers import BookSerializer


# =============================================================================
# 1. Faqat mavjud kitoblar
# =============================================================================

class AvailableBooksView(generics.ListAPIView):
    """
    Faqat available=True bo'lgan kitoblar
    
    Endpoint: GET /books/available/
    """
    # serializer_class = BookSerializer
    
    def get_queryset(self):
        # return Book.objects.filter(available=True)
        pass


# =============================================================================
# 2. User'ning o'z kitoblari
# =============================================================================

class MyBooksView(generics.ListAPIView):
    """
    Faqat login qilgan user'ning kitoblari
    (Authentication kerak!)
    
    Endpoint: GET /books/my-books/
    """
    # serializer_class = BookSerializer
    
    def get_queryset(self):
        # user = self.request.user
        # return Book.objects.filter(owner=user)
        pass


# =============================================================================
# 3. Qimmat kitoblar (narx > 100000)
# =============================================================================

class ExpensiveBooksView(generics.ListAPIView):
    """
    Narxi 100000 so'mdan yuqori kitoblar
    
    Endpoint: GET /books/expensive/
    """
    # serializer_class = BookSerializer
    
    def get_queryset(self):
        # return Book.objects.filter(price__gt=100000)
        pass


# =============================================================================
# 4. Arzon kitoblar (narx < 50000)
# =============================================================================

class CheapBooksView(generics.ListAPIView):
    """
    Narxi 50000 so'mdan past kitoblar
    
    Endpoint: GET /books/cheap/
    """
    # serializer_class = BookSerializer
    
    def get_queryset(self):
        # return Book.objects.filter(price__lt=50000)
        pass


# =============================================================================
# 5. Yangi kitoblar (oxirgi 30 kun)
# =============================================================================

class NewBooksView(generics.ListAPIView):
    """
    Oxirgi 30 kun ichida chiqgan kitoblar
    
    Endpoint: GET /books/new/
    """
    # serializer_class = BookSerializer
    
    def get_queryset(self):
        # thirty_days_ago = datetime.now() - timedelta(days=30)
        # return Book.objects.filter(publish_date__gte=thirty_days_ago)
        pass


# =============================================================================
# 6. Muallif bo'yicha (URL parameter)
# =============================================================================

class BooksByAuthorView(generics.ListAPIView):
    """
    Ma'lum bir muallif kitoblari
    URL'dan muallif nomini oladi
    
    Endpoint: GET /books/by-author/{author}/
    Example: GET /books/by-author/Alisher/
    """
    # serializer_class = BookSerializer
    
    def get_queryset(self):
        # author_name = self.kwargs.get('author')
        # return Book.objects.filter(author__icontains=author_name)
        pass


# =============================================================================
# 7. Kategoriya bo'yicha (URL parameter)
# =============================================================================

class BooksByCategoryView(generics.ListAPIView):
    """
    Ma'lum bir kategoriya kitoblari
    
    Endpoint: GET /books/by-category/{category_id}/
    Example: GET /books/by-category/1/
    """
    # serializer_class = BookSerializer
    
    def get_queryset(self):
        # category_id = self.kwargs.get('category_id')
        # return Book.objects.filter(category_id=category_id)
        pass


# =============================================================================
# 8. URL Query Parameters bilan filtering
# =============================================================================

class BooksFilterView(generics.ListAPIView):
    """
    URL query parameters orqali dinamik filtering
    
    Examples:
    - GET /books/filter/?available=true
    - GET /books/filter/?min_price=50000
    - GET /books/filter/?max_price=200000
    - GET /books/filter/?author=Alisher
    - GET /books/filter/?available=true&min_price=50000&max_price=150000
    """
    # serializer_class = BookSerializer
    
    def get_queryset(self):
        # queryset = Book.objects.all()
        
        # Available filter
        # available = self.request.query_params.get('available')
        # if available and available.lower() == 'true':
        #     queryset = queryset.filter(available=True)
        
        # Minimum price
        # min_price = self.request.query_params.get('min_price')
        # if min_price:
        #     queryset = queryset.filter(price__gte=min_price)
        
        # Maximum price
        # max_price = self.request.query_params.get('max_price')
        # if max_price:
        #     queryset = queryset.filter(price__lte=max_price)
        
        # Author filter
        # author = self.request.query_params.get('author')
        # if author:
        #     queryset = queryset.filter(author__icontains=author)
        
        # return queryset
        pass


# =============================================================================
# 9. Murakkab filtering (Q objects)
# =============================================================================

class AdvancedSearchView(generics.ListAPIView):
    """
    Murakkab qidirish: title YOKI author YOKI description'da so'z bor
    
    Example: GET /books/search/?q=django
    """
    # serializer_class = BookSerializer
    
    def get_queryset(self):
        # query = self.request.query_params.get('q', '')
        
        # if query:
        #     return Book.objects.filter(
        #         Q(title__icontains=query) |
        #         Q(author__icontains=query) |
        #         Q(description__icontains=query)
        #     )
        
        # return Book.objects.all()
        pass


# =============================================================================
# 10. Narx oralig'i bo'yicha (URL parameters)
# =============================================================================

class BooksByPriceRangeView(generics.ListAPIView):
    """
    Narx oralig'i bo'yicha kitoblar
    
    Endpoint: GET /books/price-range/{min_price}/{max_price}/
    Example: GET /books/price-range/50000/150000/
    """
    # serializer_class = BookSerializer
    
    def get_queryset(self):
        # min_price = self.kwargs.get('min_price')
        # max_price = self.kwargs.get('max_price')
        
        # return Book.objects.filter(
        #     price__gte=min_price,
        #     price__lte=max_price
        # )
        pass


# =============================================================================
# REAL FULL EXAMPLE
# =============================================================================

"""
from rest_framework import generics
from django.db.models import Q
from .models import Book
from .serializers import BookSerializer

class AdvancedBookFilterView(generics.ListAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        queryset = Book.objects.all()
        
        # URL parameters
        author = self.kwargs.get('author')
        if author:
            queryset = queryset.filter(author__icontains=author)
        
        # Query parameters
        available = self.request.query_params.get('available')
        if available and available.lower() == 'true':
            queryset = queryset.filter(available=True)
        
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset
"""


# =============================================================================
# URLs uchun
# =============================================================================

"""
from django.urls import path
from .views import (
    AvailableBooksView,
    MyBooksView,
    ExpensiveBooksView,
    NewBooksView,
    BooksByAuthorView,
    BooksFilterView,
    AdvancedSearchView,
)

urlpatterns = [
    # Simple filters
    path('books/available/', AvailableBooksView.as_view()),
    path('books/my-books/', MyBooksView.as_view()),
    path('books/expensive/', ExpensiveBooksView.as_view()),
    path('books/new/', NewBooksView.as_view()),
    
    # URL parameters
    path('books/by-author/<str:author>/', BooksByAuthorView.as_view()),
    
    # Query parameters
    path('books/filter/', BooksFilterView.as_view()),
    path('books/search/', AdvancedSearchView.as_view()),
]
"""


# =============================================================================
# MASLAHATLAR
# =============================================================================

"""
1. get_queryset() - eng muhim method!
   Bu method'da siz queryset'ni istalgancha customize qilishingiz mumkin.

2. URL parameters - self.kwargs orqali olasiz
   Example: /books/by-author/{author}/
   Code: author = self.kwargs.get('author')

3. Query parameters - self.request.query_params orqali olasiz
   Example: /books/?min_price=50000
   Code: min_price = self.request.query_params.get('min_price')

4. Murakkab filtering uchun Q objects ishlatiladi
   Example: Q(title__icontains=query) | Q(author__icontains=query)

5. Filter methodlar:
   - filter() - natijalarni qaytaradi
   - exclude() - teskari natijalar
   - get() - bitta obyekt (DoesNotExist xatolik berishi mumkin)

6. Lookups:
   - __icontains - case-insensitive contains
   - __gt - greater than (>)
   - __gte - greater than or equal (>=)
   - __lt - less than (<)
   - __lte - less than or equal (<=)
   - __exact - exact match
   - __startswith - boshlanishi
   - __endswith - tugashi
"""


# =============================================================================
# KEYINGI QADAMLAR
# =============================================================================

"""
1. filtering_example.py'ni o'qing - DRF filter backends
2. pagination_example.py'ni o'qing - Pagination
3. O'z loyihangizda custom get_queryset() yozing!
"""