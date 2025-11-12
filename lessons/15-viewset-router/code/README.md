# Code - Library Project

Bu papkada **15-Viewset va Router** darsi uchun amaliy loyiha joylashgan.

## Loyiha struktura

```
library-project/
├── manage.py
├── db.sqlite3
├── .env
├── Pipfile
├── Pipfile.lock
│
├── library_project/          # Asosiy sozlamalar
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── books/                    # Books app
│   ├── models.py            # Book modeli
│   ├── serializers.py       # BookSerializer
│   ├── views.py             # BookViewSet (YANGI!)
│   ├── urls.py              # Router (YANGI!)
│   ├── admin.py
│   └── validators.py
│
├── accounts/                 # Accounts app
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
└── static/                   # Static fayllar
```

---

## Loyihani ishga tushirish

### 1. Virtual muhitni faollashtiring
```bash
cd library-project
pipenv shell
```

### 2. Migratsiyalarni bajaring (agar kerak bo'lsa)
```bash
python manage.py migrate
```

### 3. Serverni ishga tushiring
```bash
python manage.py runserver
```

### 4. API'ni ochib ko'ring
```
http://127.0.0.1:8000/api/
```

---

## Darsda o'zgartirilgan fayllar

### books/views.py
**Eski:**
```python
# APIView yoki Generic View'lar
class BookListView(APIView):
    ...
class BookDetailView(APIView):
    ...
```

**Yangi:**
```python
# ViewSet
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Custom actions
    @action(detail=False, methods=['get'])
    def published(self, request):
        ...
```

**Farq:**
-  Kamroq kod (3 qator vs 50+ qator)
-  Avtomatik CRUD
-  Custom actions qo'shish oson
-  Router bilan integratsiya

---

### books/urls.py
**Eski:**
```python
urlpatterns = [
    path('books/', BookListView.as_view()),
    path('books/<int:pk>/', BookDetailView.as_view()),
    path('books/create/', BookCreateView.as_view()),
    # ... va h.k.
]
```

**Yangi:**
```python
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

**Farq:**
-  Avtomatik URL generatsiya
-  Kamroq kod
-  API Root sahifasi
-  Custom actions avtomatik qo'shiladi

---

## Mavjud Endpoint'lar

### Standard CRUD
```
GET    /api/books/                  # Barcha kitoblar
POST   /api/books/                  # Yangi kitob yaratish
GET    /api/books/{id}/             # Bitta kitob
PUT    /api/books/{id}/             # Kitobni yangilash
PATCH  /api/books/{id}/             # Qisman yangilash
DELETE /api/books/{id}/             # Kitobni o'chirish
```

### Custom Actions
```
GET    /api/books/published/        # Published kitoblar
GET    /api/books/statistics/       # Statistika
POST   /api/books/{id}/publish/     # Kitobni publish qilish
POST   /api/books/{id}/unpublish/   # Kitobni unpublish qilish
```

### API Root
```
GET    /api/                        # Barcha endpoint'lar ro'yxati
```

---

## Test qilish

### 1. Browsable API orqali
Brauzerda ochib, UI orqali test qiling:
```
http://127.0.0.1:8000/api/books/
```

### 2. cURL orqali
```bash
# GET request
curl http://127.0.0.1:8000/api/books/

# POST request
curl -X POST http://127.0.0.1:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "New Book", "author": "John Doe"}'
```

### 3. Postman orqali
Import qiling va test qiling.

---

## Asosiy konseptlar

### ViewSet
ViewSet - bu bir nechta bog'liq view'larni bitta class'da birlashtirish.

**Afzalliklar:**
- Kod takrorlanishini kamaytiradi
- CRUD operatsiyalarini avtomatlashtiradi
- Maintainability yaxshilanadi

### Router
Router - URL'larni avtomatik generatsiya qiladi.

**Afzalliklar:**
- URL patterns yozish shart emas
- Custom actions avtomatik qo'shiladi
- API Root sahifasi

### Custom Actions
Custom actions - standard CRUD'dan tashqari qo'shimcha endpoint'lar.

**Ishlatilish:**
- Business logic endpoint'lari
- Special operations (publish, archive, etc.)
- Statistika va hisobotlar

---

## Konfiguratsiya

### Database
SQLite (`db.sqlite3`)

### Environment Variables
`.env` faylida:
```
SECRET_KEY=your-secret-key
DEBUG=True
```

### Dependencies
`Pipfile` da:
```
django = "*"
djangorestframework = "*"
python-decouple = "*"
```

---

## Keyingi qadamlar

1.  ViewSet va Router'ni tushunding
2.  Pagination qo'shish (Keyingi dars)
3.  Filtering va Search (Keyingi dars)
4.  Throttling (Keyingi dars)

---

## Foydali buyruqlar

```bash
# Serverni ishga tushirish
python manage.py runserver

# Yangi app yaratish
python manage.py startapp app_name

# Migratsiyalar
python manage.py makemigrations
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Shell
python manage.py shell
```

---

## Muammolar va yechimlar

### Muammo 1: Server ishlamayapti
```bash
# Xato: Port band
# Yechim: Boshqa port ishlatish
python manage.py runserver 8080
```

### Muammo 2: Module not found
```bash
# Xato: ModuleNotFoundError
# Yechim: Dependencies'ni o'rnatish
pipenv install
```

### Muammo 3: Migration errors
```bash
# Yechim: Database'ni reset qilish
rm db.sqlite3
python manage.py migrate
```

---

## Foydali havolalar

- [Django Documentation](https://docs.djangoproject.com/)
- [DRF Documentation](https://www.django-rest-framework.org/)
- [ViewSets Guide](https://www.django-rest-framework.org/api-guide/viewsets/)
- [Routers Guide](https://www.django-rest-framework.org/api-guide/routers/)

---

**Loyiha tayyor!** Test qiling va o'rganing!