# Lesson 07: API Testing & Documentation - Uyga Vazifa

## 🎯 Maqsad

Library API uchun to'liq dokumentatsiya va testing yaratish:
1. ✅ Swagger/OpenAPI dokumentatsiya
2. ✅ ReDoc dokumentatsiya
3. ✅ Postman Collection
4. ✅ Automated tests

---

## 📋 Vazifa 1: drf-spectacular o'rnatish va sozlash (25 ball)

### 1.1 Installation (5 ball)

```bash
# Virtual environment'da
cd lessons/07-api-testing-docs/code/library-project

# Package o'rnatish
pipenv install drf-spectacular

# Yoki pip bilan
pip install drf-spectacular
```

**Tekshirish:**
```bash
pipenv graph | grep drf-spectacular
# yoki
pip list | grep drf-spectacular
```

---

### 1.2 settings.py sozlash (10 ball)

#### INSTALLED_APPS

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
    'drf_spectacular',  # ← Qo'shing
    
    # Local apps
    'books',
]
```

#### REST_FRAMEWORK settings

```python
REST_FRAMEWORK = {
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    
    # Schema ← QOSHING
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

#### SPECTACULAR_SETTINGS

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'Library API',
    'DESCRIPTION': 'Complete REST API for Library Management System',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    
    # Swagger UI settings
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
        'filter': True,
    },
    
    # Schema settings
    'COMPONENT_SPLIT_REQUEST': True,
}
```

---

### 1.3 URLs sozlash (10 ball)

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
    
    # API Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI
    path('api/docs/', 
         SpectacularSwaggerView.as_view(url_name='schema'), 
         name='swagger-ui'
    ),
    
    # ReDoc
    path('api/documentation/', 
         SpectacularRedocView.as_view(url_name='schema'), 
         name='redoc'
    ),
]
```

**Test qiling:**
```
http://localhost:8000/api/docs/          ← Swagger UI
http://localhost:8000/api/documentation/  ← ReDoc
http://localhost:8000/api/schema/        ← Raw schema (JSON)
```

---

## 📋 Vazifa 2: Views'larni dokumentatsiya qilish (30 ball)

### 2.1 BookListCreateView dokumentatsiya (10 ball)

```python
# books/views.py

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

@extend_schema(tags=["Books"])
class BookListCreateView(generics.ListCreateAPIView):
    """
    List all books or create a new book.
    
    Supports pagination, search, and ordering.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
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
        ],
        responses={200: BookSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create a new book",
        description="Add a new book to the library",
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
                'Complete book example',
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

### 2.2 BookRetrieveUpdateDestroyView dokumentatsiya (10 ball)

```python
@extend_schema(tags=["Books"])
class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @extend_schema(
        summary="Get a book",
        description="Retrieve a single book by ID",
        responses={
            200: BookSerializer,
            404: OpenApiExample('Not found', value={"detail": "Not found."}),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update a book (full)",
        description="Update all fields of a book",
        request=BookSerializer,
        responses={
            200: BookSerializer,
            400: "Validation error",
            404: "Not found",
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update a book (partial)",
        description="Update some fields of a book",
        request=BookSerializer,
        responses={
            200: BookSerializer,
            400: "Validation error",
            404: "Not found",
        },
        examples=[
            OpenApiExample(
                'Update price only',
                value={"price": 95000}
            ),
            OpenApiExample(
                'Update availability',
                value={"available": False}
            ),
        ]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete a book",
        description="Permanently delete a book",
        responses={
            204: None,
            404: "Not found",
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
```

---

### 2.3 Custom views dokumentatsiya (10 ball)

```python
@extend_schema(tags=["Books - Filters"])
class AvailableBooksView(generics.ListAPIView):
    """Get only available books."""
    serializer_class = BookSerializer
    
    @extend_schema(
        summary="List available books",
        description="Get all books where available=True",
        responses={200: BookSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return Book.objects.filter(available=True)


@extend_schema(tags=["Books - Filters"])
class ExpensiveBooksView(generics.ListAPIView):
    """Get expensive books (price > 100000)."""
    serializer_class = BookSerializer
    
    @extend_schema(
        summary="List expensive books",
        description="Get books with price greater than 100,000 UZS",
        responses={200: BookSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return Book.objects.filter(price__gt=100000)
```

---

## 📋 Vazifa 3: Serializer dokumentatsiya (15 ball)

### 3.1 Field help_text qo'shish (10 ball)

```python
# books/serializers.py

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model.
    
    Provides complete book information with validation.
    """
    
    title = serializers.CharField(
        max_length=200,
        help_text="Book title (max 200 characters)"
    )
    author = serializers.CharField(
        max_length=200,
        help_text="Author full name"
    )
    price = serializers.IntegerField(
        help_text="Price in UZS (must be positive)",
        min_value=0
    )
    pages = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Number of pages (optional)",
        min_value=1
    )
    publish_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="Publication date (YYYY-MM-DD format)"
    )
    isbn = serializers.CharField(
        max_length=13,
        required=False,
        allow_blank=True,
        help_text="ISBN-13 number (13 digits)"
    )
    available = serializers.BooleanField(
        default=True,
        help_text="Book availability status"
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Book description or summary"
    )
    
    class Meta:
        model = Book
        fields = '__all__'
```

---

### 3.2 Validation xabarlari (5 ball)

```python
class BookSerializer(serializers.ModelSerializer):
    # ... fields ...
    
    def validate_price(self, value):
        """Price must be positive"""
        if value <= 0:
            raise serializers.ValidationError(
                "Narx musbat son bo'lishi kerak"
            )
        return value
    
    def validate_isbn(self, value):
        """Validate ISBN format"""
        if value and not value.replace('-', '').isdigit():
            raise serializers.ValidationError(
                "ISBN faqat raqamlardan iborat bo'lishi kerak"
            )
        if value and len(value.replace('-', '')) != 13:
            raise serializers.ValidationError(
                "ISBN 13 ta raqamdan iborat bo'lishi kerak"
            )
        return value
    
    def validate_pages(self, value):
        """Pages must be positive"""
        if value and value <= 0:
            raise serializers.ValidationError(
                "Sahifalar soni musbat bo'lishi kerak"
            )
        return value
```

---

## 📋 Vazifa 4: Postman Collection (30 ball)

### 4.1 Collection yaratish (5 ball)

1. **Postman'ni oching**
2. **New Collection** tugmasini bosing
3. **Nom:** `Library API`
4. **Description:**
```markdown
# Library API Collection

Complete REST API for Library Management System.

## Base URL
http://localhost:8000

## Endpoints
- Books CRUD operations
- Search and filtering
- Pagination support
```

5. **Variables:**
   - `base_url`: `http://localhost:8000`

---

### 4.2 Folders yaratish (5 ball)

Collection ichida folderlar yarating:

```
Library API
├── 📁 Books - CRUD
│   ├── List Books
│   ├── Create Book
│   ├── Get Book
│   ├── Update Book (PUT)
│   ├── Partial Update (PATCH)
│   └── Delete Book
├── 📁 Books - Search & Filter
│   ├── Search Books
│   ├── Order by Price
│   ├── Available Books
│   └── Expensive Books
└── 📁 Pagination
    ├── Page 1
    └── Page 2 with size
```

---

### 4.3 Requests yaratish (15 ball)

#### GET - List Books
```
Method: GET
URL: {{base_url}}/books/
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has pagination", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('count');
    pm.expect(jsonData).to.have.property('results');
});

pm.test("Response time < 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

---

#### POST - Create Book
```
Method: POST
URL: {{base_url}}/books/
Headers:
  Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "title": "Test Book from Postman",
    "author": "Postman Tester",
    "price": 75000,
    "pages": 300,
    "publish_date": "2024-01-15",
    "isbn": "9781234567890",
    "available": true,
    "description": "This is a test book created from Postman"
}
```

**Tests:**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Book has ID", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
    // Save ID for later use
    pm.environment.set("book_id", jsonData.id);
});

pm.test("Title is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.title).to.eql("Test Book from Postman");
});
```

---

#### GET - Single Book
```
Method: GET
URL: {{base_url}}/books/{{book_id}}/
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Book exists", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
    pm.expect(jsonData).to.have.property('title');
});
```

---

#### PATCH - Partial Update
```
Method: PATCH
URL: {{base_url}}/books/{{book_id}}/
Headers:
  Content-Type: application/json
```

**Body:**
```json
{
    "price": 85000,
    "available": false
}
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Price updated", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.price).to.eql(85000);
});
```

---

#### DELETE - Delete Book
```
Method: DELETE
URL: {{base_url}}/books/{{book_id}}/
```

**Tests:**
```javascript
pm.test("Status code is 204", function () {
    pm.response.to.have.status(204);
});
```

---

#### GET - Search Books
```
Method: GET
URL: {{base_url}}/books/?search=django
```

**Tests:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Results contain search term", function () {
    var jsonData = pm.response.json();
    var results = jsonData.results;
    var found = results.some(book => 
        book.title.toLowerCase().includes('django') ||
        book.author.toLowerCase().includes('django') ||
        book.description.toLowerCase().includes('django')
    );
    pm.expect(found).to.be.true;
});
```

---

### 4.4 Collection export (5 ball)

1. Collection'ga o'ng click
2. **Export**
3. **Collection v2.1** format
4. **Export** tugmasini bosing
5. Faylni saqlang: `postman/Library-API.postman_collection.json`

---

## 📋 Bonus Vazifalar (+20 ball)

### Bonus 1: Custom ReDoc template (+5 ball)

`templates/redoc.html` yarating:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Library API - Documentation</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { margin: 0; padding: 0; }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 Library API Documentation</h1>
        <p>Complete REST API for Library Management System</p>
    </div>
    <redoc spec-url='{% url "schema" %}'></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js"></script>
</body>
</html>
```

---

### Bonus 2: Environment variables (+5 ball)

Postman'da 2 ta environment yarating:

**Development:**
```json
{
  "name": "Development",
  "values": [
    {
      "key": "base_url",
      "value": "http://localhost:8000",
      "enabled": true
    },
    {
      "key": "book_id",
      "value": "",
      "enabled": true
    }
  ]
}
```

**Production:**
```json
{
  "name": "Production",
  "values": [
    {
      "key": "base_url",
      "value": "https://api.yourdomain.com",
      "enabled": true
    }
  ]
}
```

---

### Bonus 3: Advanced Postman tests (+5 ball)

```javascript
// Schema validation
pm.test("Response schema is valid", function () {
    var schema = {
        "type": "object",
        "required": ["id", "title", "author", "price"],
        "properties": {
            "id": {"type": "number"},
            "title": {"type": "string"},
            "author": {"type": "string"},
            "price": {"type": "number"}
        }
    };
    pm.response.to.have.jsonSchema(schema);
});

// Data type validation
pm.test("Price is a number", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.price).to.be.a('number');
});

// Chaining requests
pm.test("Save data for next request", function () {
    var jsonData = pm.response.json();
    pm.environment.set("last_book_title", jsonData.title);
    pm.environment.set("last_book_author", jsonData.author);
});
```

---

### Bonus 4: README.md to'liq qilish (+5 ball)

`lessons/07-api-testing-docs/code/README.md` yarating:

```markdown
# Library API - Complete Documentation

## 🚀 Quick Start

### Installation

```bash
cd library-project
pipenv install
pipenv shell
python manage.py migrate
python manage.py runserver
```

### API Documentation

- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/documentation/
- **OpenAPI Schema:** http://localhost:8000/api/schema/

## 📚 API Endpoints

### Books - CRUD

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/books/` | List all books |
| POST | `/books/` | Create new book |
| GET | `/books/{id}/` | Get single book |
| PUT | `/books/{id}/` | Update book (full) |
| PATCH | `/books/{id}/` | Update book (partial) |
| DELETE | `/books/{id}/` | Delete book |

### Books - Filters

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/books/?search=django` | Search books |
| GET | `/books/?ordering=-price` | Order by price |
| GET | `/books/available/` | Available books only |
| GET | `/books/expensive/` | Expensive books |

### Query Parameters

- `search`: Search in title, author, description
- `ordering`: Order by field (`price`, `-price`, `publish_date`, `-publish_date`)
- `page`: Pagination page number
- `page_size`: Items per page (default: 10, max: 100)

## 🧪 Testing with Postman

Import collection: `postman/Library-API.postman_collection.json`

### Running tests

1. Open Postman
2. Import collection
3. Select environment (Development/Production)
4. Run collection

## 📸 Screenshots

### Swagger UI
![Swagger UI](screenshots/swagger.png)

### ReDoc
![ReDoc](screenshots/redoc.png)

### Postman
![Postman](screenshots/postman.png)

## 🛠️ Technologies

- Django 5.x
- Django REST Framework
- drf-spectacular
- PostgreSQL / SQLite

## 📄 License

MIT License
```

---

## 📊 Topshirish formati

### 1. GitHub Repository struktura

```
lessons/07-api-testing-docs/
├── README.md ✅
├── postman-guide.md ✅
├── swagger-guide.md ✅
├── redoc-guide.md ✅
├── homework.md ✅
├── code/
│   ├── README.md
│   └── library-project/
│       ├── books/
│       │   ├── views.py ← @extend_schema bilan
│       │   ├── serializers.py ← help_text bilan
│       │   └── ...
│       ├── library_project/
│       │   ├── settings.py ← drf-spectacular
│       │   └── urls.py ← Swagger/ReDoc URLs
│       └── templates/
│           └── redoc.html (bonus)
├── postman/
│   ├── Library-API.postman_collection.json
│   ├── Development.postman_environment.json (bonus)
│   └── Production.postman_environment.json (bonus)
└── screenshots/
    ├── swagger.png
    ├── redoc.png
    └── postman.png
```

---

### 2. Git commit

```bash
cd lessons/07-api-testing-docs

git add .
git commit -m "Complete Lesson 07 homework

- Setup drf-spectacular
- Add Swagger UI and ReDoc
- Document all views with @extend_schema
- Add help_text to all serializer fields
- Create Postman collection with tests
- Add screenshots
- Bonus: Custom ReDoc template, environments, advanced tests"

git push origin lesson-07
```

---

### 3. Pull Request

**Title:** `Lesson 07: API Testing & Documentation - Homework Complete`

**Description:**
```markdown
## ✅ Homework Complete

### Completed tasks:
- [x] drf-spectacular setup (25 points)
- [x] Views documentation (30 points)
- [x] Serializer documentation (15 points)
- [x] Postman collection (30 points)

### Bonus tasks:
- [x] Custom ReDoc template (+5)
- [x] Environment variables (+5)
- [x] Advanced tests (+5)
- [x] Complete README (+5)

### Files:
- `code/library-project/` - Updated with drf-spectacular
- `postman/Library-API.postman_collection.json` - Complete collection
- `screenshots/` - Swagger, ReDoc, Postman

### Testing:
All endpoints tested in:
- ✅ Swagger UI: http://localhost:8000/api/docs/
- ✅ ReDoc: http://localhost:8000/api/documentation/
- ✅ Postman: Collection with 10+ requests

**Total: 120/100 points** 🎉
```

---

## 📊 Baholash mezonlari

| Vazifa | Ball | Minimal | Yaxshi | A'lo |
|--------|------|---------|--------|------|
| **1. drf-spectacular** | 25 | O'rnatilgan | Sozlangan | To'liq sozlangan |
| **2. Views docs** | 30 | 3+ view | Barcha views | @extend_schema + examples |
| **3. Serializer docs** | 15 | help_text | help_text + validation | To'liq docs |
| **4. Postman** | 30 | 5 requests | 10 requests + tests | Full collection |
| **Jami** | **100** | **60** | **80** | **100** |
| **Bonus** | +20 | - | - | +20 |

---

### Minimal talablar (60 ball) - Pass ✅

- ✅ drf-spectacular o'rnatilgan va ishlaydi
- ✅ Swagger UI ochiladi
- ✅ Kamida 3 ta view dokumentatsiya qilingan
- ✅ Postman collection (5+ requests)

---

### Yaxshi natija (80 ball) - Good ⭐

- ✅ Barcha views dokumentatsiya qilingan
- ✅ Serializer'larda help_text bor
- ✅ Postman collection to'liq (10+ requests)
- ✅ Tests ishlaydi

---

### A'lo natija (100 ball) - Excellent ⭐⭐⭐

- ✅ To'liq va batafsil dokumentatsiya
- ✅ @extend_schema + parameters + examples
- ✅ Advanced Postman tests
- ✅ README va screenshots
- ✅ Professional code

---

### Perfect natija (120 ball) - Outstanding 🏆

- ✅ A'lo natija + Bonus tasks
- ✅ Custom ReDoc template
- ✅ Environment variables
- ✅ Schema validation
- ✅ Production-ready

---

## ❓ Savollar va javoblar

### Swagger ochilmayapti?

```bash
# Server ishga tushiringmi?
python manage.py runserver

# URL to'g'ri?
http://localhost:8000/api/docs/  # ← Slash kerak!
```

---

### @extend_schema ishlamayapti?

```python
# Import'ni tekshiring
from drf_spectacular.utils import extend_schema

# View'da to'g'ri joylashtiring
@extend_schema(tags=["Books"])  # ← Class tepasida
class BookListView(generics.ListAPIView):
    pass
```

---

### Postman test xato beradi?

```javascript
// Console'ni oching
console.log(pm.response.json());

// Response'ni tekshiring
pm.test("Check response", function () {
    console.log(pm.response.text());
});
```

---

### Collection export qila olmayapman?

1. Collection'ga **o'ng click**
2. **Export** tugmasini bosing
3. **v2.1** format tanlang
4. **Export** bosing
5. Fayl saqlang

---

## 📅 Muddat

**Topshirish:** Darsdan keyin **7 kun**

---

## 🎓 O'rganish resurslari

### Documentation:
- [drf-spectacular docs](https://drf-spectacular.readthedocs.io/)
- [OpenAPI 3.0 Spec](https://swagger.io/specification/)
- [Postman Learning](https://learning.postman.com/)

### Video tutorials:
- drf-spectacular setup
- Postman collections
- API testing best practices

### Kurs materiallari:
- `README.md` - Umumiy ma'lumot
- `postman-guide.md` - Postman to'liq guide
- `swagger-guide.md` - Swagger to'liq guide
- `redoc-guide.md` - ReDoc guide

---

## 💡 Pro Tips

1. ✅ **Ketma-ket bajaring** - Avval setup, keyin docs, oxirida Postman
2. ✅ **Har qadamni test qiling** - Har bir o'zgarishdan keyin test qiling
3. ✅ **Commit qiling** - Har bir vazifadan keyin commit
4. ✅ **Screenshot oling** - Har safar ishlagan kod uchun
5. ✅ **README yozing** - Boshqalar tushunishi uchun
6. ✅ **Tests yozing** - Postman'da har bir request uchun
7. ✅ **Clean code** - Code clean va organized bo'lsin
8. ✅ **Ask for help** - Qiyin bo'lsa, so'rang!

---

## 🎁 Bonus challenge (Extra +10 ball)

### Challenge 1: API Versioning (+5 ball)

```python
# urls.py
urlpatterns = [
    # V1
    path('api/v1/', include('books.urls.v1')),
    path('api/v1/schema/', SpectacularAPIView.as_view(urlconf='books.urls.v1'), name='schema-v1'),
    
    # V2 (future)
    # path('api/v2/', include('books.urls.v2')),
]
```

---

### Challenge 2: Rate Limiting docs (+5 ball)

```python
SPECTACULAR_SETTINGS = {
    # ...
    'EXTENSIONS_INFO': {
        'x-rate-limit': '100 requests per hour',
        'x-contact': 'support@library.com',
    }
}
```

---

## 🏆 Hall of Fame

Eng yaxshi homework'lar bu yerda ko'rsatiladi! 🌟

**Requirements:**
- ✅ 100+ ball
- ✅ Clean code
- ✅ Professional documentation
- ✅ Creative bonus tasks

---

## 📞 Yordam

### Telegram:
- Guruh: [Library API Students]
- Mentor: [@your_mentor]

### Office hours:
- Dushanba: 18:00-19:00
- Juma: 18:00-19:00

### Email:
- support@library-course.com

---

## ✅ Checklist

Topshirishdan oldin tekshiring:

### Setup (25 ball)
- [ ] drf-spectacular o'rnatilgan
- [ ] settings.py to'liq sozlangan
- [ ] URLs ishlayapti
- [ ] Swagger UI ochiladi
- [ ] ReDoc ochiladi

### Documentation (45 ball)
- [ ] Barcha views dokumentatsiya qilingan
- [ ] @extend_schema ishlatilgan
- [ ] Parameters qo'shilgan
- [ ] Examples qo'shilgan
- [ ] Serializer'larda help_text bor
- [ ] Validation messages tushunarli

### Postman (30 ball)
- [ ] Collection yaratilgan
- [ ] Folders organized
- [ ] 10+ requests bor
- [ ] Tests yozilgan
- [ ] Environment variables
- [ ] Collection exported

### Files
- [ ] README.md to'liq
- [ ] Screenshots olindi
- [ ] Code clean
- [ ] Git commit qilindi
- [ ] PR yaratildi

### Bonus (+20 ball)
- [ ] Custom ReDoc template
- [ ] Environment variables (Dev/Prod)
- [ ] Advanced tests
- [ ] README to'liq qilindi

---

## 🎉 Oxirgi so'z

Bu vazifa sizga quyidagilarni beradi:
1. ✅ **Professional skill** - Real loyihalarda ishlatiladigan tool'lar
2. ✅ **Portfolio** - GitHub'da professional loyiha
3. ✅ **Experience** - API dokumentatsiya tajribasi
4. ✅ **Confidence** - O'z API'ngizni yaratish va hujjatlash

**Omad tilaymiz!** 🚀

---

**Keyingi dars:** Lesson 08 - APIView (Part 1)
