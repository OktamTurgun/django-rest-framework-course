# Homework 26: API Versioning

##  Umumiy Talablar

Library Management tizimiga API versioning qo'shing va v1'dan v2'ga migration rejasini yarating.

---

##  Vazifa 1: URL Path Versioning (20 ball)

### Topshiriq:
URL path versioning'ni implement qiling

### Settings sozlash:

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'VERSION_PARAM': 'version',
}
```

### URL Structure:

```python
# library_project/urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('books.api.v1.urls')),
    path('api/v2/', include('books.api.v2.urls')),
]
```

### File Structure:

```
books/
├── api/
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   └── v2/
│       ├── __init__.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
```

### Test:

```bash
# V1 API
curl http://localhost:8000/api/v1/books/

# V2 API
curl http://localhost:8000/api/v2/books/
```

---

##  Vazifa 2: V1 API (15 ball)

### Topshiriq:
V1 API'ni yarating (current format)

### books/api/v1/serializers.py:

```python
from rest_framework import serializers
from books.models import Book, Author

class BookSerializerV1(serializers.ModelSerializer):
    """
    V1 Serializer: Author as string
    """
    author = serializers.CharField(source='author.name', read_only=True)
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
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class AuthorSerializerV1(serializers.ModelSerializer):
    """V1 Author Serializer"""
    class Meta:
        model = Author
        fields = ['id', 'name', 'email']
```

### books/api/v1/views.py:

```python
from rest_framework import generics
from books.models import Book, Author
from .serializers import BookSerializerV1, AuthorSerializerV1

class BookListAPIView(generics.ListCreateAPIView):
    """V1: Book List/Create"""
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializerV1

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """V1: Book Detail/Update/Delete"""
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializerV1

class AuthorListAPIView(generics.ListCreateAPIView):
    """V1: Author List/Create"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializerV1
```

### books/api/v1/urls.py:

```python
from django.urls import path
from . import views

app_name = 'v1'

urlpatterns = [
    path('books/', views.BookListAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailAPIView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListAPIView.as_view(), name='author-list'),
]
```

---

##  Vazifa 3: V2 API (25 ball)

### Topshiriq:
V2 API yarating - Author as nested object, ISBN field qo'shing

### Breaking Changes:
1. `author` string'dan object'ga o'zgardi
2. Yangi field: `isbn` (required)
3. Yangi field: `description`

### books/api/v2/serializers.py:

```python
from rest_framework import serializers
from books.models import Book, Author

class AuthorSerializerV2(serializers.ModelSerializer):
    """V2 Author Serializer - Full object"""
    books_count = serializers.IntegerField(
        source='books.count',
        read_only=True
    )
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'bio', 'books_count']

class BookSerializerV2(serializers.ModelSerializer):
    """
    V2 Serializer: Author as nested object
    Breaking changes:
    - author is now object (was string)
    - isbn is required (new field)
    """
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
            'isbn',
            'description',
            'price',
            'published_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class BookListSerializerV2(serializers.ModelSerializer):
    """V2 List - minimal fields"""
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author_name', 'price']
```

### books/api/v2/views.py:

```python
from rest_framework import generics, status
from rest_framework.response import Response
from books.models import Book, Author
from .serializers import (
    BookSerializerV2,
    BookListSerializerV2,
    AuthorSerializerV2
)

class BookListAPIView(generics.ListCreateAPIView):
    """V2: Book List/Create with nested author"""
    queryset = Book.objects.select_related('author').all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookListSerializerV2
        return BookSerializerV2

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """V2: Book Detail with nested author"""
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializerV2

class AuthorListAPIView(generics.ListCreateAPIView):
    """V2: Author List with books count"""
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializerV2

class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """V2: Author Detail"""
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializerV2
```

### books/api/v2/urls.py:

```python
from django.urls import path
from . import views

app_name = 'v2'

urlpatterns = [
    path('books/', views.BookListAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailAPIView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListAPIView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailAPIView.as_view(), name='author-detail'),
]
```

---

##  Vazifa 4: Deprecation Warning Middleware (15 ball)

### Topshiriq:
V1 uchun deprecation warning qo'shing

### books/middleware.py:

```python
from datetime import datetime

class APIVersionDeprecationMiddleware:
    """
    V1 API deprecation warning qo'shish
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if V1 API
        if request.path.startswith('/api/v1/'):
            # Add deprecation headers
            response['Warning'] = (
                '299 - "API v1 is deprecated. '
                'Please migrate to v2 by 2024-12-31. '
                'See https://docs.example.com/api/migration"'
            )
            response['Sunset'] = 'Sat, 31 Dec 2024 23:59:59 GMT'
            response['Link'] = '<https://api.example.com/v2/>; rel="successor-version"'
        
        return response
```

### settings.py:

```python
MIDDLEWARE = [
    # ...
    'books.middleware.APIVersionDeprecationMiddleware',
]
```

### Test:

```bash
curl -I http://localhost:8000/api/v1/books/

# Response:
# Warning: 299 - "API v1 is deprecated..."
# Sunset: Sat, 31 Dec 2024 23:59:59 GMT
```

---

##  Vazifa 5: Version Documentation (10 ball)

### Topshiriq:
API version'lar uchun documentation yarating

### books/api/docs.py:

```python
"""
API Version Documentation
"""

API_VERSIONS = {
    'v1': {
        'release_date': '2023-01-15',
        'status': 'deprecated',
        'sunset_date': '2024-12-31',
        'changes': [
            'Initial release',
            'Basic CRUD operations',
            'Author as string field',
        ],
        'breaking_changes': [],
    },
    'v2': {
        'release_date': '2023-07-01',
        'status': 'active',
        'sunset_date': None,
        'changes': [
            'Author as nested object',
            'Added ISBN field (required)',
            'Added description field',
            'Added author books_count',
            'Better pagination',
        ],
        'breaking_changes': [
            'author field changed from string to object',
            'isbn field is now required',
        ],
        'migration_guide': 'https://docs.example.com/api/v1-to-v2',
    },
}

def get_version_info(version):
    """Get version information"""
    return API_VERSIONS.get(version, {})
```

### API Endpoint:

```python
# books/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .docs import API_VERSIONS

class APIVersionInfoView(APIView):
    """API version information"""
    
    def get(self, request, version=None):
        if version:
            info = API_VERSIONS.get(version)
            if not info:
                return Response(
                    {'error': f'Version {version} not found'},
                    status=404
                )
            return Response(info)
        
        return Response(API_VERSIONS)
```

---

##  Vazifa 6: Migration Guide (10 ball)

### Topshiriq:
V1 → V2 migration guide yarating

### MIGRATION_GUIDE.md:

```markdown
# API Migration Guide: V1 → V2

## Breaking Changes

### 1. Author Field Structure

**V1:**
```json
{
    "id": 1,
    "title": "Django Book",
    "author": "John Doe",
    "author_id": 1
}
```

**V2:**
```json
{
    "id": 1,
    "title": "Django Book",
    "author": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "bio": "...",
        "books_count": 5
    },
    "author_id": 1
}
```

**Migration Code:**
```javascript
// V1 client code
const authorName = book.author;

// V2 client code
const authorName = book.author.name;
```

### 2. ISBN Field (Required)

**V2:** `isbn` field is now required

**Migration:**
```javascript
// V1 POST
fetch('/api/v1/books/', {
    body: JSON.stringify({
        title: "Book",
        author_id: 1,
        price: 29.99
    })
})

// V2 POST
fetch('/api/v2/books/', {
    body: JSON.stringify({
        title: "Book",
        author_id: 1,
        isbn: "1234567890123",  // REQUIRED!
        price: 29.99
    })
})
```

## Timeline

- **2024-06-01:** V2 released (beta)
- **2024-07-01:** V2 stable
- **2024-12-31:** V1 sunset

## Support

- Email: api-support@example.com
- Slack: #api-migration
```

---

##  Vazifa 7: Testing (Bonus +15 ball)

### Topshiriq:
API versioning testlari yozing

### books/tests/test_versioning.py:

```python
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from books.models import Book, Author

class APIVersioningTestCase(TestCase):
    """API versioning test"""
    
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(
            name='Test Author',
            email='test@example.com'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            isbn='1234567890123',
            price=29.99
        )
    
    def test_v1_author_as_string(self):
        """V1: Author string formatda"""
        response = self.client.get('/api/v1/books/')
        
        self.assertEqual(response.status_code, 200)
        book_data = response.data[0]
        
        # V1'da author string
        self.assertIsInstance(book_data['author'], str)
        self.assertEqual(book_data['author'], 'Test Author')
    
    def test_v2_author_as_object(self):
        """V2: Author object formatda"""
        response = self.client.get('/api/v2/books/')
        
        self.assertEqual(response.status_code, 200)
        book_data = response.data[0]
        
        # V2'da author object
        self.assertIsInstance(book_data['author_name'], str)
    
    def test_v1_deprecation_headers(self):
        """V1: Deprecation headers borligini tekshirish"""
        response = self.client.get('/api/v1/books/')
        
        self.assertIn('Warning', response)
        self.assertIn('Sunset', response)
        self.assertIn('deprecated', response['Warning'])
    
    def test_v2_no_deprecation(self):
        """V2: Deprecation headers yo'qligi"""
        response = self.client.get('/api/v2/books/')
        
        self.assertNotIn('Warning', response)
    
    def test_invalid_version(self):
        """Invalid version 404 qaytarishi kerak"""
        response = self.client.get('/api/v99/books/')
        
        self.assertEqual(response.status_code, 404)
```

### Run tests:

```bash
python manage.py test books.tests.test_versioning
```

---

## 📊 Baholash Mezonlari

| Vazifa | Ballar | Tavsif |
|--------|--------|--------|
| URL Path Versioning | 20 | Settings va URL structure |
| V1 API | 15 | Existing API as V1 |
| V2 API | 25 | Breaking changes bilan yangi API |
| Deprecation Middleware | 15 | Warning headerlar |
| Documentation | 10 | Version info endpoint |
| Migration Guide | 10 | V1→V2 migration doc |
| **Jami** | **95** | |
| Testing (Bonus) | +15 | Versioning testlari |
| **Maksimal** | **110** | |

---

##  Topshirish Talablari

1.  V1 va V2 API'lar ishlayapti
2.  URL path versioning sozlangan
3.  V1'da deprecation warning bor
4.  Breaking changes dokumentatsiyalangan
5.  Migration guide yozilgan
6.  Testlar o'tayapti

---

##  Topshirish Formati

```
homework-26-versioning/
├── books/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   ├── v2/
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   └── docs.py
│   ├── middleware.py
│   └── tests/test_versioning.py
├── library_project/
│   ├── settings.py
│   └── urls.py
├── MIGRATION_GUIDE.md
└── README.md
```

---

## Deadline

**3 kun** (72 soat)

**Omad!**