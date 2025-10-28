# Swagger UI bilan ishlash

Swagger UI - bu API dokumentatsiyasini interaktiv ko'rinishda ko'rsatadigan va test qilish imkonini beruvchi vosita.

## Sozlash

### 1. drf-yasg o'rnatish

```bash
pip install drf-yasg
```

### 2. settings.py da sozlash

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'drf_yasg',  # Swagger
    
    # Local apps
    'books',
]

# Swagger sozlamalari
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'SUPPORTED_SUBMIT_METHODS': [
        'get',
        'post',
        'put',
        'delete',
        'patch'
    ],
}
```

### 3. urls.py da yo'llarni sozlash

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version='v1',
        description="Kutubxona tizimi uchun REST API",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@library.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/books/', include('books.urls')),
    
    # Swagger URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

## Swagger UI dan foydalanish

### API sahifasiga kirish

Brauzerda quyidagi manzilga kiring:
```
http://localhost:8000/swagger/
```

### Interfeysni tushunish

1. **API Info Section**: API haqida umumiy ma'lumot
2. **Endpoints List**: Barcha mavjud endpointlar
3. **Schemas**: Ma'lumot modellari

### Endpointlarni test qilish

#### GET so'rovini yuborish

1. Endpoint nomini bosing (masalan, `/api/books/`)
2. "Try it out" tugmasini bosing
3. Parametrlarni kiriting (agar kerak bo'lsa)
4. "Execute" tugmasini bosing
5. Natijani ko'ring

**Misol:**
```
GET /api/books/
```

Response:
```json
[
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert Martin",
        "isbn": "9780132350884",
        "price": "45.00"
    }
]
```

#### POST so'rovini yuborish

1. POST endpointni oching
2. "Try it out" tugmasini bosing
3. Request body ni to'ldiring:

```json
{
    "title": "Design Patterns",
    "author": "Gang of Four",
    "isbn": "9780201633610",
    "price": "54.99",
    "published_date": "1994-10-31"
}
```

4. "Execute" tugmasini bosing

#### PUT so'rovini yuborish

```json
{
    "id": 1,
    "title": "Clean Code (Updated)",
    "author": "Robert C. Martin",
    "isbn": "9780132350884",
    "price": "49.99"
}
```

#### PATCH so'rovini yuborish

```json
{
    "price": "39.99"
}
```

#### DELETE so'rovini yuborish

1. DELETE endpointni oching
2. "Try it out" tugmasini bosing
3. ID ni kiriting
4. "Execute" tugmasini bosing

## Viewlarda dokumentatsiya qo'shish

### drf_yasg.utils.swagger_auto_schema dekorator

```python
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @swagger_auto_schema(
        operation_description="Barcha kitoblarni olish",
        operation_summary="Kitoblar ro'yxati",
        tags=['Books'],
        responses={
            200: BookSerializer(many=True),
            400: "Bad Request"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Yangi kitob qo'shish",
        operation_summary="Kitob yaratish",
        tags=['Books'],
        request_body=BookSerializer,
        responses={
            201: BookSerializer,
            400: "Bad Request"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
```

### Parametrlarni belgilash

```python
from drf_yasg import openapi

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @swagger_auto_schema(
        operation_description="Kitoblarni filterlash va qidirish",
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Kitob nomi yoki muallif bo'yicha qidirish",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'min_price',
                openapi.IN_QUERY,
                description="Minimal narx",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'max_price',
                openapi.IN_QUERY,
                description="Maksimal narx",
                type=openapi.TYPE_NUMBER
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
```

### Response misollarini qo'shish

```python
@swagger_auto_schema(
    responses={
        200: openapi.Response(
            description="Muvaffaqiyatli",
            examples={
                "application/json": {
                    "id": 1,
                    "title": "Clean Code",
                    "author": "Robert Martin",
                    "isbn": "9780132350884",
                    "price": "45.00"
                }
            }
        ),
        404: openapi.Response(
            description="Topilmadi",
            examples={
                "application/json": {
                    "detail": "Not found."
                }
            }
        )
    }
)
def get(self, request, *args, **kwargs):
    return super().get(request, *args, **kwargs)
```

## Serializerlarda dokumentatsiya

### Field help_text

```python
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=200,
        help_text="Kitob nomi"
    )
    author = serializers.CharField(
        max_length=100,
        help_text="Muallif ismi"
    )
    isbn = serializers.CharField(
        max_length=13,
        help_text="ISBN raqami (13 ta raqam)"
    )
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Kitob narxi (USD)"
    )
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'price', 'published_date']
```

## Advanced sozlamalar

### Custom Schema

```python
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version='v1',
        description="""
        # Library Management System API
        
        Bu API kutubxona tizimini boshqarish uchun mo'ljallangan.
        
        ## Asosiy imkoniyatlar:
        - Kitoblarni boshqarish (CRUD)
        - Mualliflar bilan ishlash
        - Qidiruv va filterlash
        - Pagination
        
        ## Autentifikatsiya
        Token-based autentifikatsiya ishlatiladi.
        """,
        terms_of_service="https://www.library.com/terms/",
        contact=openapi.Contact(email="support@library.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
```

### Security schemes

```python
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Token-based authentication. Example: "Bearer <token>"'
        },
        'Basic': {
            'type': 'basic',
            'description': 'Basic authentication'
        }
    },
    'USE_SESSION_AUTH': True,
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
}
```

## Swagger va ReDoc farqlari

| Xususiyat | Swagger UI | ReDoc |
|-----------|-----------|--------|
| Interaktiv test | ✓ | ✗ |
| Dizayn | Standart | Modern |
| Tezlik | O'rtacha | Tez |
| Mobil | Yaxshi | A'lo |
| Qidiruv | Asosiy | Kengaytirilgan |

## Foydali maslahatlar

1. **Aniq tavsiflar yozing**: Har bir endpoint uchun tushunarli tavsif bering
2. **Misollar qo'shing**: Request va response misollari juda foydali
3. **Xatolarni hujjatlang**: Barcha mumkin bo'lgan xatolarni ko'rsating
4. **Versiyalash**: API versiyalarini aniq belgilang
5. **Tags ishlatilng**: Endpointlarni guruhlash uchun taglardan foydalaning

## Keng tarqalgan muammolar

### Swagger sahifa ochilmaydi

```python
# settings.py da static fayllar sozlamalarini tekshiring
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

```bash
python manage.py collectstatic
```

### Swagger autentifikatsiya ishlamayapti

```python
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
```

### Schema yaratilmayapti

```python
# urls.py da schema_view to'g'ri sozlanganligini tekshiring
schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
```

## Qo'shimcha resurslar

- [drf-yasg Documentation](https://drf-yasg.readthedocs.io/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)

---

**Eslatma**: Swagger UI sizga API ni real vaqtda test qilish imkonini beradi, lekin production muhitda faqat o'qish rejimida ishlatish yoki autentifikatsiya qo'shish tavsiya etiladi.