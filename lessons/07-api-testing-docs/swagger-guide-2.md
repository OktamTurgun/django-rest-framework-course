# Swagger/OpenAPI - Complete Guide

## 📋 Mundarija

1. [Swagger nima?](#1-swagger-nima)
2. [drf-spectacular o'rnatish](#2-drf-spectacular-ornatish)
3. [Swagger UI sozlash](#3-swagger-ui-sozlash)
4. [Schema customization](#4-schema-customization)
5. [Endpoints dokumentatsiya](#5-endpoints-dokumentatsiya)
6. [Advanced features](#6-advanced-features)

---

## 1. Swagger nima?

### 🤔 Muammo: API dokumentatsiyasi

Siz API yaratdingiz. Endi uni qanday dokumentatsiya qilasiz?

**❌ Yomon usullar:**
```markdown
# API Documentation

## Get Books
URL: /books/
Method: GET
Response: List of books

## Create Book  
URL: /books/
Method: POST
Body: {title, author, price}
```

**Muammolar:**
- ⏱️ Qo'lda yozish - vaqt ketadi
- 🔄 Kod o'zgarganda - docs yangilanmaydi
- 🧪 Test qilib bo'lmaydi
- 👥 Interactive emas

---

**✅ Yaxshi usul: Swagger (OpenAPI)!**

```python
# Kod yozasiz...
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Dokumentatsiya avtomatik yaratiladi! 🎉
```

**Natija:**
- ✅ Avtomatik dokumentatsiya
- ✅ Kod o'zgarganda - docs avtomatik yangilanadi
- ✅ Interactive - brauzerda test qilish mumkin
- ✅ Professional ko'rinish

---

### 📊 Swagger vs Postman

| Feature | Postman | Swagger |
|---------|---------|---------|
| **Testing** | ✅ A'lo | ✅ Yaxshi |
| **Dokumentatsiya** | ⚠️ Qo'lda | ✅ Avtomatik |
| **Interactive** | ✅ Desktop app | ✅ Brauzerda |
| **Auto-update** | ❌ Yo'q | ✅ Ha |
| **Public docs** | ⚠️ Share link | ✅ Website'da |
| **Team** | ✅ Workspace | ✅ URL ulashish |

**Xulosa:** Ikkalasi ham kerak! 🎯
- **Postman** - Development testing
- **Swagger** - Dokumentatsiya va quick testing

---

### 🎯 Swagger nima beradi?

1. **Avtomatik dokumentatsiya** - Kod yozing, docs yaratiladi
2. **Interactive UI** - Brauzerda test qiling
3. **Try it out** - Request yuborish
4. **Schema** - OpenAPI 3.0 format
5. **Code generation** - Client code yaratish (frontend uchun)
6. **Standard** - Industry standard (Google, Amazon, Microsoft)

---

### 📚 OpenAPI nima?

**OpenAPI** - API'ni tavsiflovchi standart format.

**Qisqa tarix:**
- 2011: Swagger yaratildi
- 2015: OpenAPI Specification'ga o'zgardi
- 2017: OpenAPI 3.0
- 2021: OpenAPI 3.1

**OpenAPI Specification = API'ning JSON/YAML tavsifi**

---

## 2. drf-spectacular o'rnatish

### 📦 Installation

#### Qadam 1: Package o'rnatish

```bash
# Pipenv bilan
pipenv install drf-spectacular

# Yoki pip bilan
pip install drf-spectacular
```

---

#### Qadam 2: settings.py'ga qo'shish

```python
# library_project/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'drf_spectacular',  # ← Qo'shildi
    
    # Local apps
    'books',
]
```

---

#### Qadam 3: REST_FRAMEWORK settings

```python
# library_project/settings.py

REST_FRAMEWORK = {
    # Pagination (oldingi darsdan)
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    
    # Schema ← YANGI
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

---

#### Qadam 4: drf-spectacular settings (ixtiyoriy)

```python
# library_project/settings.py

SPECTACULAR_SETTINGS = {
    'TITLE': 'Library API',
    'DESCRIPTION': 'REST API for Library Management System',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    
    # UI sozlamalari
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
    
    # Schema sozlamalari
    'COMPONENT_SPLIT_REQUEST': True,
}
```

---

## 3. Swagger UI sozlash

### 🔗 URLs qo'shish

```python
# library_project/urls.py

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Books app
    path('', include('books.urls')),
    
    # API Schema (JSON/YAML) ← Raw schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI ← Interactive docs
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # ReDoc ← Alternative docs
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

---

### 🚀 Server ishga tushirish

```bash
# Server'ni ishga tushiring
python manage.py runserver
```

---

### 🌐 Swagger UI ochish

**Brauzerda oching:**
```
http://localhost:8000/api/schema/swagger-ui/
```

**Ko'rinishi:**
```
┌─────────────────────────────────────────────┐
│  Library API                          v1.0.0│
│  REST API for Library Management System     │
├─────────────────────────────────────────────┤
│  📚 books                                    │
│    GET    /books/              List Books   │
│    POST   /books/              Create Book  │
│    GET    /books/{id}/         Get Book     │
│    PUT    /books/{id}/         Update Book  │
│    PATCH  /books/{id}/         Partial      │
│    DELETE /books/{id}/         Delete Book  │
├─────────────────────────────────────────────┤
│  Schemas                                     │
│    📄 Book                                   │
└─────────────────────────────────────────────┘
```

**Tabriklayman! Swagger UI ishlayapti! 🎉**

---

### 🧪 "Try it out" funksiyasi

#### GET /books/ ni test qilish

1. **GET /books/** tugmasini bosing
2. **"Try it out"** tugmasini bosing
3. **"Execute"** tugmasini bosing

**Natija:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Django for Beginners",
      "author": "William Vincent",
      "price": 75000,
      ...
    }
  ]
}
```

---

#### POST /books/ ni test qilish

1. **POST /books/** tugmasini bosing
2. **"Try it out"** tugmasini bosing
3. **Request body** to'ldiring:

```json
{
  "title": "Python Crash Course",
  "author": "Eric Matthes",
  "price": 95000,
  "pages": 544,
  "publish_date": "2024-01-15",
  "isbn": "978-1593279288",
  "available": true,
  "description": "A hands-on introduction to programming"
}
```

4. **"Execute"** tugmasini bosing

**Natija:** `201 Created` ✅

---

## 4. Schema Customization

### 📝 View'larga description qo'shish

```python
# books/views.py

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics

class BookListCreateView(generics.ListCreateAPIView):
    """
    List all books or create a new book.
    
    Use query parameters for filtering:
    - search: Search in title, author, description
    - ordering: Order by price, publish_date, title
    - page: Pagination page number
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Swagger'da ko'rinadi:**
```
GET /books/
List all books or create a new book.
Use query parameters for filtering:
- search: Search in title, author, description
- ordering: Order by price, publish_date, title
- page: Pagination page number
```

---

### 🎨 @extend_schema decorator

```python
from drf_spectacular.utils import extend_schema, OpenApiExample

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @extend_schema(
        summary="List all books",
        description="Get paginated list of all books with optional filtering",
        tags=["Books"],
        responses={200: BookSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create a new book",
        description="Add a new book to the library",
        tags=["Books"],
        responses={201: BookSerializer},
        examples=[
            OpenApiExample(
                'Example 1',
                value={
                    "title": "Django REST Framework",
                    "author": "Tom Christie",
                    "price": 85000,
                    "pages": 400,
                    "publish_date": "2024-01-01",
                    "isbn": "978-1234567890",
                    "available": true,
                    "description": "Complete guide to DRF"
                }
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
```

---

### 📊 Query Parameters dokumentatsiya

```python
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Search in title, author, description',
                required=False,
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Order by: price, -price, publish_date, -publish_date',
                required=False,
            ),
            OpenApiParameter(
                name='page',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Page number',
                required=False,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
```

**Swagger'da:**
```
Query Parameters:
- search (string): Search in title, author, description
- ordering (string): Order by: price, -price, publish_date
- page (integer): Page number
```

---

### 🏷️ Tags (Guruhlash)

```python
# books/views.py

@extend_schema(tags=["Books - CRUD"])
class BookListCreateView(generics.ListCreateAPIView):
    pass

@extend_schema(tags=["Books - CRUD"])
class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    pass

@extend_schema(tags=["Books - Filters"])
class AvailableBooksView(generics.ListAPIView):
    pass

@extend_schema(tags=["Books - Filters"])
class ExpensiveBooksView(generics.ListAPIView):
    pass
```

**Swagger'da:**
```
📚 Books - CRUD
  GET    /books/
  POST   /books/
  GET    /books/{id}/
  ...

🔍 Books - Filters
  GET    /books/available/
  GET    /books/expensive/
  ...
```

---

## 5. Endpoints dokumentatsiya

### 📖 Serializer'ga description

```python
# books/serializers.py

from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model.
    
    Fields:
    - id: Unique identifier (auto-generated)
    - title: Book title (max 200 characters)
    - author: Author name (max 200 characters)
    - price: Price in UZS (positive integer)
    - pages: Number of pages (optional)
    - publish_date: Publication date (optional)
    - isbn: ISBN number (optional)
    - available: Availability status (default: true)
    - description: Book description (optional)
    """
    
    class Meta:
        model = Book
        fields = '__all__'
        
    def validate_price(self, value):
        """Price must be positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value
```

---

### 🎯 Field-level documentation

```python
class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=200,
        help_text="Book title (max 200 characters)"
    )
    author = serializers.CharField(
        max_length=200,
        help_text="Author full name"
    )
    price = serializers.IntegerField(
        help_text="Price in UZS (positive number)",
        min_value=0
    )
    pages = serializers.IntegerField(
        required=False,
        help_text="Number of pages (optional)",
        min_value=1
    )
    
    class Meta:
        model = Book
        fields = '__all__'
```

**Swagger'da:**
```json
{
  "title": "string (max 200 chars) - Book title",
  "author": "string (max 200 chars) - Author full name",
  "price": "integer (min: 0) - Price in UZS",
  "pages": "integer (min: 1, optional) - Number of pages"
}
```

---

### 📝 Response examples

```python
from drf_spectacular.utils import extend_schema, OpenApiExample

@extend_schema(
    examples=[
        OpenApiExample(
            'Success response',
            value={
                "id": 1,
                "title": "Django for Beginners",
                "author": "William Vincent",
                "price": 75000,
                "pages": 350,
                "publish_date": "2024-01-01",
                "isbn": "978-1735467221",
                "available": True,
                "description": "A beginner-friendly guide to Django"
            },
            response_only=True,
            status_codes=['200'],
        ),
    ]
)
def get(self, request, *args, **kwargs):
    return super().get(request, *args, **kwargs)
```

---

### ⚠️ Error responses

```python
@extend_schema(
    responses={
        200: BookSerializer,
        400: OpenApiExample(
            'Validation error',
            value={
                "title": ["This field is required."],
                "price": ["Price must be positive."]
            }
        ),
        404: OpenApiExample(
            'Not found',
            value={"detail": "Not found."}
        ),
    }
)
def retrieve(self, request, *args, **kwargs):
    return super().retrieve(request, *args, **kwargs)
```

---

## 6. Advanced Features

### 🔐 Authentication dokumentatsiya

```python
# library_project/settings.py

SPECTACULAR_SETTINGS = {
    # ... other settings ...
    
    'SECURITY': [
        {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
    ],
}
```

**Swagger'da:**
```
Authorization: Bearer <token>
```

---

### 📦 Schema versioning

```python
# library_project/settings.py

SPECTACULAR_SETTINGS = {
    'TITLE': 'Library API',
    'VERSION': '1.0.0',  # ← Version
    
    # Version URL
    'SCHEMA_PATH_PREFIX': '/api/v1/',
}
```

---

### 🎨 Custom theme (Swagger UI)

```python
SPECTACULAR_SETTINGS = {
    'SWAGGER_UI_SETTINGS': {
        # Theme
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
        'docExpansion': 'none',  # 'list', 'full', 'none'
        'filter': True,  # Search box
        'showExtensions': True,
        'showCommonExtensions': True,
        
        # Custom CSS (ixtiyoriy)
        # 'customCss': '.swagger-ui .topbar { display: none }',
    }
}
```

---

### 📄 Schema file export

```bash
# Schema'ni fayl sifatida olish
python manage.py spectacular --file schema.yml

# Yoki JSON format
python manage.py spectacular --format openapi-json --file schema.json
```

**Nima uchun kerak?**
- ✅ Frontend developers'ga berish
- ✅ Code generation (TypeScript, Swift)
- ✅ Version control (Git)
- ✅ Postman'ga import qilish

---

### 🔄 Multiple serializers

```python
class BookListSerializer(serializers.ModelSerializer):
    """Minimal book info for list view"""
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price']

class BookDetailSerializer(serializers.ModelSerializer):
    """Complete book info for detail view"""
    class Meta:
        model = Book
        fields = '__all__'

@extend_schema(responses=BookListSerializer(many=True))
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer

@extend_schema(responses=BookDetailSerializer)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
```

---

### 🌍 Environment-specific settings

```python
# library_project/settings.py

# Development
if DEBUG:
    SPECTACULAR_SETTINGS = {
        'SERVE_INCLUDE_SCHEMA': True,  # Schema'ni ko'rsatish
    }
else:
    # Production
    SPECTACULAR_SETTINGS = {
        'SERVE_INCLUDE_SCHEMA': False,  # Schema'ni yashirish
    }
```

---

## ✅ Real Example - Complete View

```python
# books/views.py

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework import generics, filters
from .models import Book
from .serializers import BookSerializer

@extend_schema(tags=["Books"])
class BookListCreateView(generics.ListCreateAPIView):
    """
    List all books or create a new book.
    
    Supports pagination, search, and ordering.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'description']
    ordering_fields = ['price', 'publish_date', 'title']
    
    @extend_schema(
        summary="List all books",
        description="Get paginated list of books with optional search and ordering",
        parameters=[
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Search in title, author, description',
                required=False,
                examples=[
                    OpenApiExample('Django search', value='django'),
                    OpenApiExample('Python search', value='python'),
                ]
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Order by field (use - for descending)',
                required=False,
                examples=[
                    OpenApiExample('Price ascending', value='price'),
                    OpenApiExample('Price descending', value='-price'),
                    OpenApiExample('Date descending', value='-publish_date'),
                ]
            ),
        ],
        responses={
            200: BookSerializer(many=True),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create a new book",
        description="Add a new book to the library database",
        request=BookSerializer,
        responses={
            201: BookSerializer,
            400: OpenApiExample(
                'Validation error',
                value={
                    "title": ["This field is required."],
                    "price": ["Ensure this value is greater than 0."]
                }
            ),
        },
        examples=[
            OpenApiExample(
                'Complete book',
                value={
                    "title": "Django REST Framework Guide",
                    "author": "John Doe",
                    "price": 85000,
                    "pages": 420,
                    "publish_date": "2024-01-15",
                    "isbn": "978-1234567890",
                    "available": True,
                    "description": "Comprehensive guide to DRF"
                }
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
```

---

## ✅ Xulosa

### Siz nimalarni o'rgandingiz:

1. ✅ **Swagger nima** - Avtomatik API dokumentatsiya
2. ✅ **drf-spectacular** - DRF uchun Swagger tool
3. ✅ **Swagger UI** - Interactive dokumentatsiya
4. ✅ **@extend_schema** - Customization decorator
5. ✅ **Parameters** - Query params dokumentatsiya
6. ✅ **Examples** - Request/Response examples
7. ✅ **Tags** - Endpoint'larni guruhlash
8. ✅ **Try it out** - Brauzerda test qilish

---

### 🎯 Keyingi qadamlar

1. ✅ Library project'ga drf-spectacular o'rnating
2. ✅ Barcha view'larga @extend_schema qo'shing
3. ✅ Swagger UI'ni brauzerda ochib ko'ring
4. ✅ "Try it out" bilan test qiling
5. ✅ `redoc-guide.md`'ni o'qing

---

**Keyingi:** [redoc-guide.md](redoc-guide.md) - ReDoc dokumentatsiya

Happy documenting! 📖