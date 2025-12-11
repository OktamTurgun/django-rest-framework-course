"""
URL Path Versioning - Eng ko'p ishlatiladigan usul
"""

# ==========================================
# DJANGO REST FRAMEWORK SETUP
# ==========================================

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2', 'v3'],
    'VERSION_PARAM': 'version',  # URL parameter nomi
}

"""
URLPathVersioning:
- Version URL path'dan olinadi
- Masalan: /api/v1/books/ → version='v1'
"""


# ==========================================
# METHOD 1: Single URL with Version Parameter
# ==========================================

# urls.py
from django.urls import path
from books.views import BookListView, BookDetailView

urlpatterns = [
    # Version parameter bilan
    path('api/<version>/books/', BookListView.as_view(), name='book-list'),
    path('api/<version>/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]

"""
URLs:
- /api/v1/books/
- /api/v2/books/
- /api/v3/books/
"""


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class BookListView(APIView):
    """Version-aware Book List"""
    
    def get(self, request, version):
        # Version avtomatik request.version'da
        print(f"API Version: {request.version}")  # 'v1', 'v2', 'v3'
        
        if request.version == 'v1':
            # V1 logic
            return Response({
                'version': 'v1',
                'data': self.get_v1_data()
            })
        
        elif request.version == 'v2':
            # V2 logic
            return Response({
                'version': 'v2',
                'data': self.get_v2_data()
            })
        
        elif request.version == 'v3':
            # V3 logic
            return Response({
                'version': 'v3',
                'data': self.get_v3_data()
            })
    
    def get_v1_data(self):
        """V1 format"""
        return [
            {
                'id': 1,
                'title': 'Django Book',
                'author': 'John Doe',  # String
            }
        ]
    
    def get_v2_data(self):
        """V2 format - author as object"""
        return [
            {
                'id': 1,
                'title': 'Django Book',
                'author': {  # Object
                    'id': 1,
                    'name': 'John Doe',
                    'email': 'john@example.com'
                }
            }
        ]
    
    def get_v3_data(self):
        """V3 format - with ISBN"""
        return [
            {
                'id': 1,
                'title': 'Django Book',
                'isbn': '1234567890123',  # New field
                'author': {
                    'id': 1,
                    'name': 'John Doe',
                    'email': 'john@example.com'
                }
            }
        ]


# ==========================================
# METHOD 2: Separate URL Patterns (Recommended)
# ==========================================

# urls.py
from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('books.api.v1.urls')),
    path('api/v2/', include('books.api.v2.urls')),
    path('api/v3/', include('books.api.v3.urls')),
]

"""
File Structure:
books/
├── api/
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── v2/
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   └── v3/
│       ├── __init__.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
"""


# ==========================================
# V1 API (books/api/v1/)
# ==========================================

# books/api/v1/serializers.py
from rest_framework import serializers
from books.models import Book

class BookSerializerV1(serializers.ModelSerializer):
    """V1: Author as string"""
    author = serializers.CharField(source='author.name')
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price']


# books/api/v1/views.py
from rest_framework import generics
from books.models import Book
from books.serializers import BookSerializerV1

class BookListView(generics.ListAPIView):
    """V1: Book List"""
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializerV1


# books/api/v1/urls.py
from django.urls import path
from . import views

app_name = 'v1'

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book-list'),
]


# ==========================================
# V2 API (books/api/v2/)
# ==========================================

# books/api/v2/serializers.py
from rest_framework import serializers
from books.models import Book, Author

class AuthorSerializer(serializers.ModelSerializer):
    """V2: Author serializer"""
    class Meta:
        model = Author
        fields = ['id', 'name', 'email']

class BookSerializerV2(serializers.ModelSerializer):
    """V2: Author as nested object"""
    author = AuthorSerializer(read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price']


# books/api/v2/views.py
from rest_framework import generics
from books.models import Book
from books.serializers import BookSerializerV2

class BookListView(generics.ListAPIView):
    """V2: Book List with nested author"""
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializerV2


# books/api/v2/urls.py
from django.urls import path
from . import views

app_name = 'v2'

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book-list'),
]


# ==========================================
# V3 API (books/api/v3/)
# ==========================================

# books/api/v3/serializers.py
from rest_framework import serializers
from books.models import Book, Author

class AuthorSerializerV3(serializers.ModelSerializer):
    books_count = serializers.IntegerField(
        source='books.count',
        read_only=True
    )
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'books_count']

class BookSerializerV3(serializers.ModelSerializer):
    """V3: With ISBN field"""
    author = AuthorSerializerV3(read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'author', 'price']


# books/api/v3/views.py
from rest_framework import generics
from books.models import Book
from books.serializers import BookSerializerV3

class BookListView(generics.ListAPIView):
    """V3: Book List with ISBN"""
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializerV3


# books/api/v3/urls.py
from django.urls import path
from . import views

app_name = 'v3'

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book-list'),
]


# ==========================================
# DYNAMIC SERIALIZER SELECTION
# ==========================================

# Alternative: Single view, dynamic serializer

class BookListView(generics.ListAPIView):
    """Dynamic version-based serializer"""
    queryset = Book.objects.select_related('author').all()
    
    def get_serializer_class(self):
        """Version'ga qarab serializer tanlash"""
        version = self.request.version
        
        if version == 'v1':
            from .v1.serializers import BookSerializerV1
            return BookSerializerV1
        elif version == 'v2':
            from .v2.serializers import BookSerializerV2
            return BookSerializerV2
        elif version == 'v3':
            from .v3.serializers import BookSerializerV3
            return BookSerializerV3
        
        # Default
        from .v1.serializers import BookSerializerV1
        return BookSerializerV1


# ==========================================
# VERSION DETECTION UTILITIES
# ==========================================
from rest_framework.views import APIView
from books.serializers import BookSerializer, ReviewSerializer

def get_api_version(request):
    """Get current API version"""
    return getattr(request, 'version', 'v1')

def is_version_or_higher(request, target_version):
    """Check if version is target or higher"""
    version_numbers = {
        'v1': 1,
        'v2': 2,
        'v3': 3,
    }
    
    current = version_numbers.get(request.version, 1)
    target = version_numbers.get(target_version, 1)
    
    return current >= target

# Usage
class BookDetailView(APIView):
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        
        # V2+ only feature
        if is_version_or_higher(request, 'v2'):
            # Include reviews (new in v2)
            reviews = book.reviews.all()
            return Response({
                'book': BookSerializer(book).data,
                'reviews': ReviewSerializer(reviews, many=True).data
            })
        
        # V1
        return Response(BookSerializer(book).data)


# ==========================================
# VERSION-SPECIFIC FEATURES
# ==========================================

class BookStatisticsView(APIView):
    """Version-specific features"""
    
    def get(self, request):
        version = request.version
        
        stats = {
            'total_books': Book.objects.count(),
        }
        
        # V2+ feature: Average price
        if is_version_or_higher(request, 'v2'):
            from django.db.models import Avg
            stats['average_price'] = Book.objects.aggregate(
                avg=Avg('price')
            )['avg']
        
        # V3+ feature: Books by category
        if is_version_or_higher(request, 'v3'):
            from django.db.models import Count
            stats['by_category'] = list(
                Book.objects.values('category__name')
                .annotate(count=Count('id'))
            )
        
        return Response(stats)


# ==========================================
# TESTING URL VERSIONING
# ==========================================

"""
Test commands:

# V1 API
curl http://localhost:8000/api/v1/books/

# V2 API
curl http://localhost:8000/api/v2/books/

# V3 API
curl http://localhost:8000/api/v3/books/

# Invalid version
curl http://localhost:8000/api/v99/books/
# Response: 404 Not Found or 400 Bad Request
"""


# ==========================================
# ADVANTAGES & DISADVANTAGES
# ==========================================

"""
✅ ADVANTAGES:

1. Visible - URL'da ko'rinadi
2. Easy to test - Browser'da test qilish oson
3. Documentation clear - Har bir version'ning URL'i bor
4. Cache friendly - Har bir version alohida cache
5. Standard - Ko'pchilik API'lar shu usuldan foydalanadi

❌ DISADVANTAGES:

1. URL changes - Har safar URL o'zgaradi
2. Multiple endpoints - Ko'p URL maintain qilish kerak
3. Routing complexity - URL routing murakkab bo'lishi mumkin
4. Client updates - Client'lar URL'ni update qilishi kerak

RECOMMENDATION: URL Path Versioning - Best choice for most APIs!
"""


print("✅ URL Versioning examples to'liq!")
print("\nKeyingi qadam:")
print("→ 03-header-versioning.py'ni o'qing")