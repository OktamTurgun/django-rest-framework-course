# Lesson 26: API Versioning

## Dars Maqsadi
Django REST Framework'da API versioning strategiyalarini o'rganish va amalda qo'llash.

## Mavzular

### 1. API Versioning Asoslari
- Versioning nima va nima uchun kerak?
- Breaking changes vs Non-breaking changes
- Semantic versioning
- Versioning strategies

### 2. URL Versioning
- Path parameter versioning
- Query parameter versioning
- Subdomain versioning
- Pros and cons

### 3. Header Versioning
- Accept header versioning
- Custom header versioning
- Content negotiation
- Advantages and disadvantages

### 4. Namespace Versioning
- Django URL namespaces
- ViewSet versioning
- App-based versioning
- Code organization

### 5. Migration Strategies
- Deprecation policy
- Backward compatibility
- Sunset headers
- Client migration

---

## API Versioning Nima?

**API Versioning** - bu API'ni o'zgartirganingizda eski client'lar ishlay berishini ta'minlash mexanizmi.

### Nima uchun kerak?

```
Scenario: Book API v1
{
    "title": "Django Book",
    "author": "John Doe",
    "price": 29.99
}

Yangi feature: Author'ni alohida object qilish kerak

Version 2:
{
    "title": "Django Book",
    "author": {              ← BREAKING CHANGE!
        "id": 1,
        "name": "John Doe"
    },
    "price": 29.99
}

❌ Muammo: Eski mobile app'lar buziladi!
```

**Yechim:** API Versioning

```
v1 API: /api/v1/books/  → Eski format (eski client'lar uchun)
v2 API: /api/v2/books/  → Yangi format (yangi client'lar uchun)
```

---

## Breaking vs Non-Breaking Changes

### ✅ Non-Breaking Changes (Safe)

```python
# ✅ Yangi field qo'shish (optional)
{
    "title": "Book",
    "author": "Author",
    "isbn": "123456789"  # YANGI, lekin optional
}

# ✅ Yangi endpoint qo'shish
GET /api/books/statistics/  # YANGI endpoint

# ✅ Response'ga qo'shimcha ma'lumot
{
    "title": "Book",
    "author": "Author",
    "meta": {  # YANGI, lekin eski fieldlar o'zgarishsiz
        "views": 100
    }
}
```

### ❌ Breaking Changes (Needs New Version)

```python
# ❌ Mavjud field'ni o'chirish
{
    "title": "Book",
    # "author": "Author"  ← O'CHIRILDI!
}

# ❌ Field type'ni o'zgartirish
{
    "price": "29.99"  # Eski: number, Yangi: string
}

# ❌ Field nomini o'zgartirish
{
    "book_title": "Book"  # Eski: "title"
}

# ❌ Endpoint'ni o'chirish yoki o'zgartirish
GET /api/books/  → 404 Not Found

# ❌ Required field qo'shish
POST /api/books/
{
    "title": "Book",
    "isbn": "123"  # YANGI va REQUIRED!
}
```

---

## Semantic Versioning

Format: **MAJOR.MINOR.PATCH** (masalan: 2.1.3)

```
v2.1.3
│ │ │
│ │ └─ PATCH: Bug fixes (backward compatible)
│ └─── MINOR: New features (backward compatible)
└───── MAJOR: Breaking changes
```

### Misollar:

```
v1.0.0 → v1.0.1  Bug fix (price calculation)
v1.0.1 → v1.1.0  New feature (book reviews endpoint)
v1.1.0 → v2.0.0  Breaking change (author as object)
```

**API Versioning'da ko'pincha faqat MAJOR version ishlatiladi:**
- v1, v2, v3...

---

## Versioning Strategies

### 1 URL Path Versioning (Most Common)

```
GET /api/v1/books/
GET /api/v2/books/
```

**✅ Pros:**
- Ko'rish oson
- Browser'da test qilish oson
- Documentation'da aniq
- Cache friendly

**❌ Cons:**
- URL'ni o'zgartirish kerak
- Ko'p version'lar - ko'p URL'lar

---

### 2 Query Parameter Versioning

```
GET /api/books/?version=1
GET /api/books/?version=2
```

**✅ Pros:**
- URL path o'zgarishsiz
- Optional versioning

**❌ Cons:**
- Unutish oson
- Cache muammolari
- Kam qo'llaniladi

---

### 3 Header Versioning

```http
GET /api/books/
Accept: application/json; version=1

GET /api/books/
Accept: application/json; version=2
```

**✅ Pros:**
- RESTful
- URL clean qoladi
- Multiple versioning schemes

**❌ Cons:**
- Ko'rinmas (hidden)
- Browser'da test qilish qiyin
- Documentation murakkab

---

### 4 Custom Header Versioning

```http
GET /api/books/
X-API-Version: 1

GET /api/books/
X-API-Version: 2
```

**✅ Pros:**
- Sodda
- Explicit

**❌ Cons:**
- Non-standard
- Client'da har safar header qo'shish kerak

---

### 5 Hostname/Subdomain Versioning

```
https://api-v1.example.com/books/
https://api-v2.example.com/books/
```

**✅ Pros:**
- Version'lar alohida
- Load balancing oson

**❌ Cons:**
- DNS sozlash kerak
- SSL certificate'lar
- Infrastructure murakkab

---

## Django REST Framework Versioning

DRF built-in versioning schemes:

### 1. URLPathVersioning

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}

# urls.py
urlpatterns = [
    path('api/<version>/books/', BookListView.as_view()),
]

# URLs:
# /api/v1/books/
# /api/v2/books/
```

### 2. NamespaceVersioning

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
}

# urls.py
urlpatterns = [
    path('api/v1/', include(('books.urls', 'v1'))),
    path('api/v2/', include(('books.urls', 'v2'))),
]
```

### 3. AcceptHeaderVersioning

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
}

# Request:
# Accept: application/json; version=v1
```

### 4. QueryParameterVersioning

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.QueryParameterVersioning',
}

# URLs:
# /api/books/?version=v1
```

### 5. HostNameVersioning

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.HostNameVersioning',
}

# Hostnames:
# v1.api.example.com
# v2.api.example.com
```

---

## 💻 View'da Versioning Ishlatish

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class BookListView(APIView):
    def get(self, request):
        # Version olish
        version = request.version
        
        if version == 'v1':
            # V1 logic
            return Response({
                'title': 'Book',
                'author': 'John Doe'  # String
            })
        
        elif version == 'v2':
            # V2 logic
            return Response({
                'title': 'Book',
                'author': {  # Object
                    'id': 1,
                    'name': 'John Doe'
                }
            })
```

---

## Serializer Versioning

```python
# v1/serializers.py
class BookSerializerV1(serializers.ModelSerializer):
    author = serializers.CharField(source='author.name')
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price']


# v2/serializers.py
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email']

class BookSerializerV2(serializers.ModelSerializer):
    author = AuthorSerializer()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'isbn']


# views.py
class BookListView(APIView):
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return BookSerializerV1
        return BookSerializerV2
```

---

## File Structure (Namespace Versioning)

```
books/
├── __init__.py
├── models.py
├── admin.py
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
└── urls.py
```

---

## Best Practices

### 1. Version Format

```python
# ✅ Good
/api/v1/books/
/api/v2/books/

# ❌ Bad
/api/version1/books/
/api/1.0/books/
/api/2023-01/books/
```

### 2. Default Version

```python
REST_FRAMEWORK = {
    'DEFAULT_VERSION': 'v1',  # Agar version ko'rsatilmasa
}
```

### 3. Version Documentation

```python
"""
API Versions:

v1 (2023-01-01): Initial release
- Basic CRUD operations
- Author as string

v2 (2023-06-01): Author as object
- Breaking: Author is now object
- New: ISBN field
- New: Book reviews endpoint

v3 (2024-01-01): Planned
- GraphQL support
- Real-time updates
"""
```

### 4. Deprecation Policy

```python
# Response headers
{
    "Warning": "299 - API v1 is deprecated. Please migrate to v2 by 2024-12-31",
    "Sunset": "Sat, 31 Dec 2024 23:59:59 GMT"
}
```

### 5. Version Support Timeline

```
v1: 2023-01 → 2024-12 (2 yil support)
v2: 2023-06 → Active
v3: 2024-01 → Active (yangi)
```

---

## Migration Strategy

### Phase 1: Announce (3-6 months before)

```
# Blog post, email, documentation
"API v3 coming soon! v1 will be sunset in 6 months"
```

### Phase 2: Dual Support (6-12 months)

```
v1: Maintained but deprecated
v2: Active
v3: Beta / Active
```

### Phase 3: Deprecation Warnings

```http
HTTP/1.1 200 OK
Warning: 299 - API v1 is deprecated
Sunset: 2024-12-31
```

### Phase 4: Sunset

```
v1: Returns 410 Gone
v2: Active
v3: Active
```

---

## Tools & Utilities

### Version Checking Middleware

```python
class VersionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        version = request.resolver_match.kwargs.get('version')
        
        if version == 'v1':
            # Add deprecation warning
            response = self.get_response(request)
            response['Warning'] = '299 - API v1 is deprecated'
            response['Sunset'] = 'Sat, 31 Dec 2024 23:59:59 GMT'
            return response
        
        return self.get_response(request)
```

### Version Decorator

```python
def version_required(versions):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.version not in versions:
                return Response(
                    {'error': f'API version {request.version} not supported'},
                    status=400
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@version_required(['v2', 'v3'])
def new_feature_view(request):
    return Response({'feature': 'Only in v2 and v3'})
```

---

## Comparison Table

| Strategy | URL Example | Pros | Cons | Use Case |
|----------|-------------|------|------|----------|
| URL Path | `/api/v1/books/` | Clear, Cacheable | URL changes | Most APIs |
| Query Param | `/api/books/?v=1` | Flexible | Easy to forget | Internal APIs |
| Header | `Accept: v=1` | RESTful | Hidden | Advanced APIs |
| Subdomain | `v1.api.com` | Isolated | Complex setup | Large scale |
| Namespace | Django namespaces | Organized | Setup complex | Django only |

---

## Real-World Examples

### GitHub API
```
https://api.github.com/repos/owner/repo
Accept: application/vnd.github.v3+json
```

### Stripe API
```
https://api.stripe.com/v1/customers
Stripe-Version: 2023-10-16
```

### Twitter API
```
https://api.twitter.com/2/tweets
```

### AWS API
```
https://ec2.amazonaws.com/?Version=2016-11-15
```

---

## Checklist

Planning new version:
- [ ] Document breaking changes
- [ ] Create migration guide
- [ ] Set deprecation date
- [ ] Update API documentation
- [ ] Notify clients (email, blog)
- [ ] Add deprecation warnings
- [ ] Monitor usage metrics
- [ ] Provide support period

---

## Keyingi Darslar

- Lesson 27: Error Handling
- Lesson 28: Signals & Webhooks
- Lesson 29: Environment Setup

---

## Resources

- [DRF Versioning](https://www.django-rest-framework.org/api-guide/versioning/)
- [API Versioning Best Practices](https://www.troyhunt.com/your-api-versioning-is-wrong/)
- [Semantic Versioning](https://semver.org/)