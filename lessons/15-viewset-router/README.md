# 15-Dars: ViewSet va Router

## Mundarija
1. [Kirish](#kirish)
2. [ViewSet nima?](#viewset-nima)
3. [ViewSet turlari](#viewset-turlari)
4. [Router nima?](#router-nima)
5. [Custom Actions](#custom-actions)
6. [Amaliy mashg'ulot](#amaliy-mashgulot)
7. [To'liq misol](#toliq-misol)
8. [Xulosa](#xulosa)

---

## Kirish

Avvalgi darslarda biz DRF'da turli xil view'lar bilan ishladik:
- **APIView** - eng asosiy, barcha narsani qo'lda yozish
- **Generic Views** - ListAPIView, RetrieveAPIView, etc.
- **Mixins** - Qayta ishlatiladigan kod bloklari

Lekin bu yondashuvlarda muammolar bor:
- 😕 Har bir CRUD operatsiya uchun alohida view class
- 😕 Ko'p kod takrorlanishi
- 😕 URL'larni qo'lda yozish kerak
- 😕 Maintenance qiyin

**ViewSet va Router** bu muammolarni hal qiladi! 🎉

---

## ViewSet nima?

### Ta'rif
**ViewSet** - bu bir nechta bog'liq view'larni bitta class'da birlashtiradigan DRF komponenti.

### 🔄 Avvalgi yondashuv vs ViewSet

#### ❌ Eski usul (Generic Views):
```python
# 6 ta alohida class kerak!
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDestroyView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# URLs.py da:
urlpatterns = [
    path('books/', BookListView.as_view()),
    path('books/create/', BookCreateView.as_view()),
    path('books/<int:pk>/', BookRetrieveView.as_view()),
    path('books/<int:pk>/update/', BookUpdateView.as_view()),
    path('books/<int:pk>/delete/', BookDestroyView.as_view()),
]
```
**Kod:** ~50+ qator, 6 ta class, 5 ta URL pattern

---

#### Yangi usul (ViewSet):
```python
from rest_framework import viewsets

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# URLs.py da:
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```
**Kod:** ~10 qator, 1 ta class, avtomatik URL'lar! 🎉

---

### ViewSet qanday ishlaydi?

ViewSet ichida **action**lar bor:

```python
class BookViewSet(viewsets.ModelViewSet):
    # Bu 6 ta action avtomatik mavjud:
    
    def list(self, request):
        # GET /api/books/
        # Barcha kitoblarni qaytaradi
        pass
    
    def create(self, request):
        # POST /api/books/
        # Yangi kitob yaratadi
        pass
    
    def retrieve(self, request, pk=None):
        # GET /api/books/{id}/
        # Bitta kitobni qaytaradi
        pass
    
    def update(self, request, pk=None):
        # PUT /api/books/{id}/
        # Kitobni to'liq yangilaydi
        pass
    
    def partial_update(self, request, pk=None):
        # PATCH /api/books/{id}/
        # Kitobni qisman yangilaydi
        pass
    
    def destroy(self, request, pk=None):
        # DELETE /api/books/{id}/
        # Kitobni o'chiradi
        pass
```

**ModelViewSet** bu 6 ta action'ni avtomatik ta'minlaydi! Sizga faqat `queryset` va `serializer_class` ko'rsatish kifoya.

---

## ViewSet turlari

DRF'da 4 xil ViewSet mavjud:

### 1. ViewSet (asosiy)
```python
from rest_framework import viewsets

class BookViewSet(viewsets.ViewSet):
    """
    Eng asosiy ViewSet.
    Hech qanday avtomatik funksiyalar yo'q.
    Barcha action'larni qo'lda yozish kerak.
    """
    
    def list(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
```

**Qachon ishlatiladi:** Maxsus logic kerak bo'lganda, standard CRUD yetmaydi.

---

### 2. GenericViewSet
```python
from rest_framework import viewsets, mixins

class BookViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    Mixin'lar bilan kerakli action'larni tanlab olish.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Qachon ishlatiladi:** Faqat ba'zi CRUD operatsiyalar kerak bo'lganda.

**Mavjud Mixin'lar:**
- `ListModelMixin` - list action
- `CreateModelMixin` - create action
- `RetrieveModelMixin` - retrieve action
- `UpdateModelMixin` - update & partial_update
- `DestroyModelMixin` - destroy action

---

### 3. ModelViewSet (Eng ko'p ishlatiladigan)
```python
from rest_framework import viewsets

class BookViewSet(viewsets.ModelViewSet):
    """
    To'liq CRUD operatsiyalar avtomatik!
    Hammasi tayyor - faqat ishlatish qoladi.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
```

**Qachon ishlatiladi:** Standart CRUD API kerak bo'lganda (90% hollarda).

**Ta'minlaydigan action'lar:**
-  list (GET /api/books/)
-  create (POST /api/books/)
-  retrieve (GET /api/books/{id}/)
-  update (PUT /api/books/{id}/)
-  partial_update (PATCH /api/books/{id}/)
-  destroy (DELETE /api/books/{id}/)

---

### 4. ReadOnlyModelViewSet
```python
from rest_framework import viewsets

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Faqat o'qish uchun (GET).
    POST, PUT, DELETE mavjud emas.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**Qachon ishlatiladi:** 
- Public API (faqat ko'rish)
- Ma'lumotlar katalogi
- Reference data

**Ta'minlaydigan action'lar:**
- ✅ list (GET /api/books/)
- ✅ retrieve (GET /api/books/{id}/)
- ❌ create, update, destroy yo'q

---

### ViewSet Comparison

| ViewSet | CRUD | Mixin Support | Qiyinlik | Ishlatish |
|---------|------|---------------|----------|-----------|
| ViewSet | ❌ | ❌ | 🔴 Qiyin | Juda kam |
| GenericViewSet | Tanlash mumkin | ✅ | 🟡 O'rta | Ba'zan |
| ModelViewSet | ✅ To'liq | ✅ | 🟢 Oson | Ko'p |
| ReadOnlyModelViewSet | ✅ Faqat o'qish | ✅ | 🟢 Oson | O'rtacha |

---

## Router nima?

### Ta'rif
**Router** - ViewSet'lar uchun URL pattern'larni avtomatik yaratadigan DRF komponenti.

### 🔄 Qo'lda URL vs Router

#### ❌ Qo'lda URL yozish:
```python
urlpatterns = [
    path('books/', views.book_list),
    path('books/<int:pk>/', views.book_detail),
    path('books/create/', views.book_create),
    path('books/<int:pk>/update/', views.book_update),
    path('books/<int:pk>/delete/', views.book_delete),
]
```

#### Router bilan:
```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

Router avtomatik yaratadi:
```
GET    /api/books/           -> list()
POST   /api/books/           -> create()
GET    /api/books/{id}/      -> retrieve()
PUT    /api/books/{id}/      -> update()
PATCH  /api/books/{id}/      -> partial_update()
DELETE /api/books/{id}/      -> destroy()
```

---

### Router turlari

#### 1. SimpleRouter
```python
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'books', BookViewSet)
```

**Yaratadigan URL'lar:**
```
/books/
/books/{pk}/
/books/{pk}/custom-action/
```

**Xususiyatlari:**
- ✅ Minimal URL'lar
- ❌ API root yo'q
- ❌ Format suffix yo'q (.json, .xml)

---

#### 2. DefaultRouter (Tavsiya etiladi)
```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', BookViewSet)
```

**Yaratadigan URL'lar:**
```
/                         -> API root (barcha endpoint'lar)
/books/
/books.json              -> JSON format
/books/{pk}/
/books/{pk}.json         -> JSON format
/books/{pk}/custom-action/
```

**Xususiyatlari:**
-  API root sahifasi
-  Format suffix (.json, .xml)
-  Browsable API'da qulay
-  Development uchun ajoyib

---

### Router Comparison

| Feature | SimpleRouter | DefaultRouter |
|---------|-------------|---------------|
| CRUD URLs | ✅ | ✅ |
| Custom actions | ✅ | ✅ |
| API root | ❌ | ✅ |
| Format suffix | ❌ | ✅ |
| Hajmi | Kichik | Kattaroq |
| Production | ✅ | ✅ |
| Development | ⚠️ | ✅✅ |

---

## Custom Actions

### Ta'rif
**Custom Actions** - standard CRUD'dan tashqari qo'shimcha endpoint'lar yaratish.

### @action dekorator

```python
from rest_framework.decorators import action
from rest_framework.response import Response

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Custom action
    @action(detail=False, methods=['get'])
    def published(self, request):
        """GET /api/books/published/"""
        books = Book.objects.filter(published=True)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
```

---

### detail=True vs detail=False

#### detail=False (Collection level)
```python
@action(detail=False, methods=['get'])
def published(self, request):
    """URL: /api/books/published/"""
    # Barcha kitoblar ustida amal
    pass

@action(detail=False, methods=['get'])
def statistics(self, request):
    """URL: /api/books/statistics/"""
    # Umumiy statistika
    pass
```

**URL pattern:** `/api/books/ACTION_NAME/`

---

#### detail=True (Individual level)
```python
@action(detail=True, methods=['post'])
def publish(self, request, pk=None):
    """URL: /api/books/{id}/publish/"""
    # Bitta kitob ustida amal
    book = self.get_object()
    book.published = True
    book.save()
    return Response({'status': 'published'})

@action(detail=True, methods=['post'])
def unpublish(self, request, pk=None):
    """URL: /api/books/{id}/unpublish/"""
    book = self.get_object()
    book.published = False
    book.save()
    return Response({'status': 'unpublished'})
```

**URL pattern:** `/api/books/{id}/ACTION_NAME/`

---

### Multiple HTTP methods

```python
@action(detail=True, methods=['get', 'post', 'delete'])
def bookmark(self, request, pk=None):
    """
    GET    /api/books/{id}/bookmark/    - Tekshirish
    POST   /api/books/{id}/bookmark/    - Qo'shish
    DELETE /api/books/{id}/bookmark/    - O'chirish
    """
    book = self.get_object()
    
    if request.method == 'GET':
        bookmarked = request.user in book.bookmarks.all()
        return Response({'bookmarked': bookmarked})
    
    elif request.method == 'POST':
        book.bookmarks.add(request.user)
        return Response({'status': 'added'})
    
    elif request.method == 'DELETE':
        book.bookmarks.remove(request.user)
        return Response({'status': 'removed'})
```

---

### Custom permissions

```python
from rest_framework.permissions import IsAdminUser

@action(detail=False, 
        methods=['get'],
        permission_classes=[IsAdminUser])
def admin_stats(self, request):
    """Faqat admin ko'ra oladi"""
    return Response({
        'total_books': Book.objects.count(),
        'total_users': User.objects.count(),
    })
```

---

## Amaliy mashg'ulot

### Loyiha strukturasi
```
15-viewset-router/
├── code/
│   └── library-project/
│       ├── books/
│       │   ├── models.py
│       │   ├── serializers.py
│       │   ├── views.py          ← ViewSet'lar
│       │   └── urls.py           ← Router
│       ├── manage.py
│       └── ...
├── examples/
│   ├── 01-simple-viewset.py
│   ├── 02-readonly-viewset.py
│   ├── 03-custom-actions.py
│   └── 04-router-comparison.py
├── README.md
└── homework.md
```

---

## To'liq misol

### books/models.py
```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

### books/serializers.py
```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```

### books/views.py
```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book model
    Barcha CRUD + Custom actions
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Custom action: Published kitoblar
    @action(detail=False, methods=['get'])
    def published(self, request):
        """GET /api/books/published/"""
        published_books = Book.objects.filter(published=True)
        serializer = self.get_serializer(published_books, many=True)
        return Response(serializer.data)
    
    # Custom action: Statistika
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """GET /api/books/statistics/"""
        total = Book.objects.count()
        published = Book.objects.filter(published=True).count()
        
        return Response({
            'total_books': total,
            'published_books': published,
            'unpublished_books': total - published,
        })
    
    # Custom action: Kitobni publish qilish
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        """POST /api/books/{id}/publish/"""
        book = self.get_object()
        book.published = True
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    # Custom action: Kitobni unpublish qilish
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unpublish(self, request, pk=None):
        """POST /api/books/{id}/unpublish/"""
        book = self.get_object()
        book.published = False
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
```

### books/urls.py
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

# Router yaratish
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
]
```

### library_project/urls.py
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('books.urls')),
]
```

---

### Test qilish

Server ishga tushiring:
```bash
python manage.py runserver
```

Endpoint'lar:
```
# API Root
http://127.0.0.1:8000/api/

# Standard CRUD
GET    http://127.0.0.1:8000/api/books/
POST   http://127.0.0.1:8000/api/books/
GET    http://127.0.0.1:8000/api/books/1/
PUT    http://127.0.0.1:8000/api/books/1/
PATCH  http://127.0.0.1:8000/api/books/1/
DELETE http://127.0.0.1:8000/api/books/1/

# Custom Actions
GET    http://127.0.0.1:8000/api/books/published/
GET    http://127.0.0.1:8000/api/books/statistics/
POST   http://127.0.0.1:8000/api/books/1/publish/
POST   http://127.0.0.1:8000/api/books/1/unpublish/
```

---

## Xulosa

### Afzalliklar

1. **Kamroq kod**
   - 6 ta class → 1 ta ViewSet
   - 50+ qator → 10 qator
   - 57% kod qisqarishi!

2. **Avtomatik URL'lar**
   - Router avtomatik yaratadi
   - Xatolik ehtimoli kam
   - Maintenance oson

3. **Standartlashtirish**
   - REST standartlariga mos
   - Predictable API
   - Documentation oson

4. **Flexibility**
   - Custom actions qo'shish oson
   - Override qilish mumkin
   - Kengaytirish oson

---

### Kod qisqarishi

| Yondashuv | Lines | Classes | URL patterns |
|-----------|-------|---------|--------------|
| APIView | 150+ | 6+ | 5+ |
| Generic Views | 100+ | 5+ | 5+ |
| ViewSet | 50- | 1 | 0 (auto) |

---

### Qachon ViewSet ishlatish?

✅ **Ishlatish kerak:**
- Standard CRUD API
- RESTful endpoint'lar
- Tez development
- Maintainable kod

❌ **Ishlatmaslik kerak:**
- Juda maxsus logic
- Non-RESTful endpoint'lar
- Simple API (1-2 ta endpoint)

---

### Keyingi mavzular

Endi siz ViewSet va Router'ni bilasiz! Keyingi darslarda:
- 16-Pagination (sahifalash)
- 17-Filtering (filtrlash)
- 18-Search (qidiruv)
- 19-Ordering (tartiblash)

---

### Foydali havolalar

- [DRF ViewSets Documentation](https://www.django-rest-framework.org/api-guide/viewsets/)
- [DRF Routers Documentation](https://www.django-rest-framework.org/api-guide/routers/)
- [DRF Actions Documentation](https://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing)

---

**Omad! ViewSet va Router'dan foydalaning va kod yozishdan zavqlaning!**