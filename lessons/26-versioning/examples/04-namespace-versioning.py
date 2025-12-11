"""
Namespace Versioning - Django URL namespaces
Django-specific, code organization uchun eng yaxshi
"""

# ==========================================
# DJANGO REST FRAMEWORK SETUP
# ==========================================

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2', 'v3'],
}

"""
NamespaceVersioning:
- Version URL namespace'dan olinadi
- Django's URL namespace system ishlatadi
- Clean code organization
"""


# ==========================================
# MAIN URLs with Namespaces
# ==========================================

# library_project/urls.py
from django.contrib import admin
from django.urls import path, include

from books import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API with namespaces
    path('api/v1/', include(('books.api.v1.urls', 'books'), namespace='v1')),
    path('api/v2/', include(('books.api.v2.urls', 'books'), namespace='v2')),
    path('api/v3/', include(('books.api.v3.urls', 'books'), namespace='v3')),
]

"""
Namespace format:
include((module, app_name), namespace='version')

request.version will be: 'v1', 'v2', or 'v3'
"""


# ==========================================
# FILE STRUCTURE
# ==========================================

"""
books/
├── __init__.py
├── models.py
├── admin.py
└── api/
    ├── __init__.py
    ├── v1/
    │   ├── __init__.py
    │   ├── serializers.py
    │   ├── views.py
    │   └── urls.py
    ├── v2/
    │   ├── __init__.py
    │   ├── serializers.py
    │   ├── views.py
    │   └── urls.py
    └── v3/
        ├── __init__.py
        ├── serializers.py
        ├── views.py
        └── urls.py
"""


# ==========================================
# V1 API Implementation
# ==========================================

# books/api/v1/serializers.py
from rest_framework import serializers
from books.models import Book, Author

class AuthorSerializerV1(serializers.ModelSerializer):
    """V1: Simple author"""
    class Meta:
        model = Author
        fields = ['id', 'name']

class BookSerializerV1(serializers.ModelSerializer):
    """V1: Author as string"""
    author = serializers.CharField(source='author.name', read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_id', 'price']


# books/api/v1/views.py
from rest_framework import generics
from books.models import Book, Author
from books.serializers import BookSerializerV1, AuthorSerializerV1

class BookListCreateView(generics.ListCreateAPIView):
    """V1: List and Create Books"""
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializerV1

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """V1: Retrieve, Update, Delete Book"""
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializerV1

class AuthorListView(generics.ListCreateAPIView):
    """V1: List and Create Authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializerV1


# books/api/v1/urls.py
from django.urls import path
from books.views import BookListCreateView, BookDetailView, AuthorListView

app_name = 'books'  # Application namespace

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
]


# ==========================================
# V2 API Implementation
# ==========================================

# books/api/v2/serializers.py
from rest_framework import serializers
from books.models import Book, Author

class AuthorSerializerV2(serializers.ModelSerializer):
    """V2: Author with email"""
    books_count = serializers.IntegerField(
        source='books.count',
        read_only=True
    )
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'books_count']

class BookSerializerV2(serializers.ModelSerializer):
    """V2: Author as nested object"""
    author = AuthorSerializerV2(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'author_id',
            'price',
            'published_date',
        ]


# books/api/v2/views.py
from rest_framework import generics
from books.models import Book, Author
from books.serializers import BookSerializerV2, AuthorSerializerV2

class BookListCreateView(generics.ListCreateAPIView):
    """V2: List and Create Books"""
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializerV2

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """V2: Retrieve, Update, Delete Book"""
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializerV2

class AuthorListView(generics.ListCreateAPIView):
    """V2: List and Create Authors"""
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializerV2

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """V2: Author Detail (new in v2)"""
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializerV2


# books/api/v2/urls.py
from django.urls import path
from books.views import BookListCreateView, BookDetailView, AuthorListView, AuthorDetailView

app_name = 'books'

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),  # NEW
]


# ==========================================
# V3 API Implementation
# ==========================================

# books/api/v3/serializers.py
from rest_framework import serializers
from books.models import Book, Author

class AuthorSerializerV3(serializers.ModelSerializer):
    """V3: Full author info"""
    books_count = serializers.IntegerField(source='books.count', read_only=True)
    recent_books = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'bio', 'books_count', 'recent_books']
    
    def get_recent_books(self, obj):
        """Last 3 books"""
        books = obj.books.order_by('-published_date')[:3]
        return [{'id': b.id, 'title': b.title} for b in books]

class BookSerializerV3(serializers.ModelSerializer):
    """V3: With ISBN and description"""
    author = AuthorSerializerV3(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'isbn',  # NEW in V3
            'description',  # NEW in V3
            'author',
            'author_id',
            'price',
            'published_date',
            'created_at',
            'updated_at',
        ]


# books/api/v3/views.py
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from books.models import Book, Author
from books.serializers import BookSerializerV3, AuthorSerializerV3

class BookListCreateView(generics.ListCreateAPIView):
    """V3: With filtering and search"""
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializerV3
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author', 'price']
    search_fields = ['title', 'isbn']

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """V3: Book Detail"""
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializerV3

class AuthorListView(generics.ListCreateAPIView):
    """V3: Authors with search"""
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializerV3
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """V3: Author Detail"""
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializerV3


# books/api/v3/urls.py
from django.urls import path
from books.views import BookListCreateView, BookDetailView, AuthorListView, AuthorDetailView

app_name = 'books'

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]


# ==========================================
# REVERSE URL GENERATION
# ==========================================

from django.urls import reverse
from rest_framework.response import Response

# Version-aware URL generation
def get_book_url(book_id, version='v1'):
    """Generate versioned URL"""
    return reverse(f'{version}:book-detail', kwargs={'pk': book_id})

# Usage
url_v1 = get_book_url(1, 'v1')  # /api/v1/books/1/
url_v2 = get_book_url(1, 'v2')  # /api/v2/books/1/
url_v3 = get_book_url(1, 'v3')  # /api/v3/books/1/


# In view
class BookDetailView(generics.RetrieveAPIView):
    def get(self, request, pk):
        version = request.version
        
        # Generate URL for next version
        if version == 'v1':
            v2_url = reverse('v2:book-detail', kwargs={'pk': pk})
            # Add to response headers
            response = Response(...)
            response['Link'] = f'<{v2_url}>; rel="alternate"; version="v2"'
            return response


# ==========================================
# SHARED CODE BETWEEN VERSIONS
# ==========================================

# books/api/common/mixins.py
class VersionMixin:
    """Common functionality for all versions"""
    
    def get_version(self):
        """Get current API version"""
        return self.request.version
    
    def is_version_or_higher(self, target_version):
        """Check if current version >= target"""
        version_map = {'v1': 1, 'v2': 2, 'v3': 3}
        current = version_map.get(self.get_version(), 1)
        target = version_map.get(target_version, 1)
        return current >= target


# books/api/common/permissions.py
from rest_framework.permissions import BasePermission

class V3OnlyPermission(BasePermission):
    """Only allow V3 API"""
    
    def has_permission(self, request, view):
        return request.version == 'v3'


# Usage in v3 views
from books.api.common.permissions import V3OnlyPermission

class AdvancedFeatureView(generics.ListAPIView):
    """Feature only available in V3"""
    permission_classes = [V3OnlyPermission]
    # ...


# ==========================================
# ADVANTAGES & DISADVANTAGES
# ==========================================

"""
✅ ADVANTAGES:

1. Code Organization - Har bir version alohida papkada
2. Maintainability - Oson maintain qilish
3. Clear separation - Version'lar aralashmaydi
4. Django native - Django URL system ishlatadi
5. Reverse URLs - reverse() function ishlaydi
6. Testing easy - Har bir version'ni alohida test qilish

❌ DISADVANTAGES:

1. Setup complexity - Ko'proq setup kerak
2. Code duplication - Ba'zi kod'lar duplicate
3. Django specific - Faqat Django uchun
4. File structure - Ko'p fayllar va papkalar

WHEN TO USE:

- Django project
- Long-term maintenance
- Team collaboration
- Clear code organization kerak
- Multiple versions parallel support

BEST FOR:

- Large Django projects
- Enterprise applications
- Team-based development
- Long API lifecycle
"""


# ==========================================
# TESTING NAMESPACE VERSIONING
# ==========================================

"""
Test commands:

# V1 API
curl http://localhost:8000/api/v1/books/
curl http://localhost:8000/api/v1/authors/

# V2 API
curl http://localhost:8000/api/v2/books/
curl http://localhost:8000/api/v2/authors/
curl http://localhost:8000/api/v2/authors/1/  # New in V2

# V3 API
curl http://localhost:8000/api/v3/books/
curl http://localhost:8000/api/v3/books/?search=django  # New in V3
"""


# ==========================================
# MIGRATION UTILITIES
# ==========================================

# books/api/utils.py
def migrate_book_v1_to_v2(v1_data):
    """Migrate book data from V1 to V2 format"""
    return {
        'id': v1_data['id'],
        'title': v1_data['title'],
        'author': {
            'id': v1_data['author_id'],
            'name': v1_data['author'],
        },
        'price': v1_data['price'],
    }

def migrate_book_v2_to_v3(v2_data):
    """Migrate book data from V2 to V3 format"""
    return {
        **v2_data,
        'isbn': '',  # New required field
        'description': '',  # New field
    }


print("✅ Namespace Versioning examples to'liq!")
print("\nKeyingi qadam:")
print("→ 05-migration-strategies.md'ni o'qing")