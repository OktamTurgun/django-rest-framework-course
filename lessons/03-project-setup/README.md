# 03. Loyihani boshlash - Django va DRF

> Endi nazariyadan amaliyotga o'tamiz! Birinchi Django REST API loyihamizni yaratamiz!

## 🎯 Dars maqsadlari

Ushbu darsdan keyin siz quyidagilarni bilib olasiz:
- [ ] Django va Django REST Framework o'rnatishni
- [ ] Django loyihasi va app yaratishni
- [ ] Birinchi modelni yozishni
- [ ] Birinchi API endpoint yaratishni
- [ ] API'ni test qilishni

## ⏱ Taxminiy vaqt: 60-90 daqiqa

---

## 📚 Nazariya

### Django loyihasi tuzilishi

Django loyihasi 2 ta asosiy qismdan iborat:

1. **Project** - Butun loyiha (settings, urls, asgi, wsgi)
2. **App** - Loyihaning modullari (users, products, orders va h.k.)

```
myproject/              # Loyiha ildizi
├── myproject/          # Project settings
│   ├── __init__.py
│   ├── settings.py     # Asosiy sozlamalar
│   ├── urls.py         # URL routing
│   ├── wsgi.py         # Production uchun
│   └── asgi.py         # Async uchun
├── myapp/              # Birinchi app
│   ├── migrations/     # Database o'zgarishlari
│   ├── __init__.py
│   ├── admin.py        # Admin panel
│   ├── apps.py         # App konfiguratsiya
│   ├── models.py       # Database modellari
│   ├── serializers.py  # DRF serializers
│   ├── views.py        # API views
│   ├── urls.py         # App URL'lar
│   └── tests.py        # Testlar
├── manage.py           # Django CLI
└── requirements.txt    # Paketlar ro'yxati
```

---

### Django REST Framework nima?

**Django REST Framework (DRF)** - bu Django uchun qudratli REST API yaratish vositasi.

**Afzalliklari:**
- ✅ Tez va oson API yaratish
- ✅ Browsable API (brauzerda test qilish)
- ✅ Authentication va Permissions
- ✅ Serialization (Ma'lumotni JSON'ga aylantirish)
- ✅ ViewSets va Routers
- ✅ Katta community va hujjatlar

---

## 💻 Amaliyot

### 1-qadam: Virtual muhit yaratish

Virtual muhit - bu loyihaning alohida Python muhiti. Har bir loyiha o'z paketlariga ega bo'ladi.

```bash
# Virtual muhit yaratish
python -m venv venv

# Aktivlashtirish (Windows)
venv\Scripts\activate

# Aktivlashtirish (Mac/Linux)
source venv/bin/activate
```

**Aktivlangandan keyin:**
```bash
(venv) C:\Users\...>
```

`(venv)` ko'rinadi - bu virtual muhit ishga tushganini bildiradi.

---

### 2-qadam: Django va DRF o'rnatish

```bash
# Eng so'nggi versiyalarni o'rnatish
pip install django djangorestframework

# Yoki muayyan versiyani
pip install django==4.2 djangorestframework==3.14
```

**Tekshirish:**

```bash
python -m django --version
```

Natija: `4.2` yoki shunga o'xshash versiya

---

### 3-qadam: Django loyihasi yaratish

```bash
# Loyiha yaratish
django-admin startproject api_project .

# . (nuqta) - hozirgi papkada yaratish
```

**Natija:**

```
api_project/
├── api_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── manage.py
```

---

### 4-qadam: Birinchi app yaratish

```bash
# App yaratish
python manage.py startapp products

# Natija: products/ papkasi paydo bo'ladi
```

---

### 5-qadam: Django sozlamalari (settings.py)

`api_project/settings.py` faylini oching va quyidagilarni qo'shing:

```python
# api_project/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',           # ⬅️ DRF qo'shdik
    
    # Local apps
    'products',                 # ⬅️ O'z appimiz
]

# DRF sozlamalari (faylning oxiriga)
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

---

### 6-qadam: Birinchi model yaratish

Model - bu database jadvali.

`products/models.py` faylini oching:

```python
# products/models.py
from django.db import models

class Product(models.Model):
    """Mahsulot modeli"""
    name = models.CharField(max_length=200, verbose_name="Nomi")
    description = models.TextField(blank=True, verbose_name="Ta'rif")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    stock = models.IntegerField(default=0, verbose_name="Omborda")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")
    
    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created_at']  # Yangilar birinchi
    
    def __str__(self):
        return self.name
```

**Tushuntirish:**

- `CharField` - Matn (max 200 belgi)
- `TextField` - Uzun matn
- `DecimalField` - Decimal son (narx uchun)
- `IntegerField` - Butun son
- `DateTimeField` - Sana va vaqt
  - `auto_now_add=True` - Faqat yaratilganda
  - `auto_now=True` - Har safar yangilanganda

---

### 7-qadam: Migration yaratish

Migration - bu database'ga o'zgarishlarni qo'llash.

```bash
# Migration fayllarini yaratish
python manage.py makemigrations

# Natija:
# Migrations for 'products':
#   products/migrations/0001_initial.py
#     - Create model Product
```

```bash
# Database'ga qo'llash
python manage.py migrate

# Natija: OK
```

---

### 8-qadam: Serializer yaratish

Serializer - bu Python obyektini JSON'ga va aksincha aylantiradi.

`products/serializers.py` fayl yarating:

```python
# products/serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """Product modeli uchun serializer"""
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
```

**Tushuntirish:**

- `ModelSerializer` - Model asosida avtomatik serializer
- `fields` - Qaysi fieldlar JSON'da bo'lishi kerak
- `read_only_fields` - Faqat o'qish uchun (o'zgartirish mumkin emas)

---

### 9-qadam: View yaratish

View - bu API endpoint'ning mantiq qismi.

`products/views.py` faylini oching:

```python
# products/views.py
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    """
    GET: Barcha mahsulotlarni ko'rish
    POST: Yangi mahsulot yaratish
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Bitta mahsulotni ko'rish
    PUT/PATCH: Mahsulotni yangilash
    DELETE: Mahsulotni o'chirish
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

**Tushuntirish:**

- `ListCreateAPIView` - List (GET) va Create (POST)
- `RetrieveUpdateDestroyAPIView` - Retrieve (GET), Update (PUT/PATCH), Delete (DELETE)

---

### 10-qadam: URL routing

**App URL'lari** - `products/urls.py` yarating:

```python
# products/urls.py
from django.urls import path
from .views import ProductListCreateView, ProductDetailView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
```

**Project URL'lari** - `api_project/urls.py`:

```python
# api_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),  # ⬅️ Products app URL'lari
]
```

**Natija:**

- `http://localhost:8000/api/products/` - Barcha mahsulotlar
- `http://localhost:8000/api/products/1/` - ID=1 mahsulot

---

### 11-qadam: Serverni ishga tushirish

```bash
python manage.py runserver
```

**Natija:**

```
Starting development server at http://127.0.0.1:8000/
```

Brauzerda oching: `http://127.0.0.1:8000/api/products/`

🎉 **Tabriklayman! Birinchi API tayyor!**

---

### 12-qadam: Test ma'lumot qo'shish

Admin panel orqali yoki Django shell orqali ma'lumot qo'shamiz.

#### Variant 1: Admin panel

```bash
# Superuser yaratish
python manage.py createsuperuser

# Username: admin
# Email: admin@example.com
# Password: admin123
```

`products/admin.py` faylini oching:

```python
# products/admin.py
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
```

Admin panel: `http://127.0.0.1:8000/admin/`

#### Variant 2: Django shell

```bash
python manage.py shell
```

```python
from products.models import Product

# Mahsulot yaratish
Product.objects.create(
    name="Laptop",
    description="Dell Latitude 5000",
    price=5000000,
    stock=10
)

Product.objects.create(
    name="Phone",
    description="iPhone 15 Pro",
    price=12000000,
    stock=5
)

# Tekshirish
Product.objects.all()
# <QuerySet [<Product: Laptop>, <Product: Phone>]>
```

---

## 🔥 API'ni test qilish

### 1. Brauzerda (Browsable API)

```
http://127.0.0.1:8000/api/products/
```

DRF'ning o'zida chiroyli interfeys bor! Forma orqali POST qilish mumkin.

### 2. cURL orqali

```bash
# GET - Barcha mahsulotlar
curl http://127.0.0.1:8000/api/products/

# POST - Yangi mahsulot
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Mouse", "price": 50000, "stock": 20}'

# GET - Bitta mahsulot
curl http://127.0.0.1:8000/api/products/1/

# PUT - Yangilash
curl -X PUT http://127.0.0.1:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Gaming Mouse", "price": 75000, "stock": 15}'

# DELETE - O'chirish
curl -X DELETE http://127.0.0.1:8000/api/products/1/
```

### 3. Python requests orqali

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api/products/"

# GET
response = requests.get(BASE_URL)
print(response.json())

# POST
new_product = {
    "name": "Keyboard",
    "description": "Mechanical keyboard",
    "price": 350000,
    "stock": 30
}
response = requests.post(BASE_URL, json=new_product)
print(response.status_code)  # 201

# GET by ID
response = requests.get(f"{BASE_URL}1/")
print(response.json())
```

---

## 🎯 Muhim nuqtalar (Cheat Sheet)

### Django loyiha yaratish

```bash
# Virtual muhit
python -m venv venv
venv\Scripts\activate

# Django o'rnatish
pip install django djangorestframework

# Loyiha yaratish
django-admin startproject myproject .
python manage.py startapp myapp

# Server
python manage.py runserver
```

### Model → Serializer → View → URL

```python
# 1. Model (models.py)
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

# 2. Serializer (serializers.py)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

# 3. View (views.py)
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# 4. URL (urls.py)
path('products/', ProductListView.as_view())
```

### Migration

```bash
python manage.py makemigrations  # Yaratish
python manage.py migrate         # Qo'llash
python manage.py showmigrations  # Ko'rish
```

---

## ⚠️ Keng tarqalgan xatolar

### 1. App'ni INSTALLED_APPS'ga qo'shmaslik

❌ **Xato:**
```
django.core.exceptions.ImproperlyConfigured: 
Model class products.models.Product doesn't declare an explicit app_label
```

✅ **Yechim:** `settings.py`da INSTALLED_APPS'ga qo'shing

### 2. Migration qilmaslik

❌ **Xato:**
```
django.db.utils.OperationalError: no such table: products_product
```

✅ **Yechim:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. URL pattern'da vergul unutish

❌ **Noto'g'ri:**
```python
urlpatterns = [
    path('products/', ProductListView.as_view())  # Vergul yo'q!
]
```

✅ **To'g'ri:**
```python
urlpatterns = [
    path('products/', ProductListView.as_view()),  # Vergul bor
]
```

---

## 🧪 O'zingizni tekshiring

### Nazariy savollar:

1. **Django Project va App'ning farqi nima?**
   <details><summary>Javob</summary>
   Project - butun loyiha (settings, asosiy URL'lar).
   App - loyihaning moduli (users, products). Bir projectda ko'p app bo'lishi mumkin.
   </details>

2. **ModelSerializer nima qiladi?**
   <details><summary>Javob</summary>
   Model'ni avtomatik JSON formatga aylantiradi va aksincha. Model fieldlarini ko'rib, serializer yaratadi.
   </details>

3. **Migration nima uchun kerak?**
   <details><summary>Javob</summary>
   Database'dagi o'zgarishlarni versiyalash va qo'llash uchun. Model o'zgarganda migration yaratib, database'ga apply qilamiz.
   </details>

---

## 📚 Qo'shimcha o'qish

### Rasmiy hujjatlar:
- [Django Documentation](https://docs.djangoproject.com/) - To'liq Django guide
- [DRF Documentation](https://www.django-rest-framework.org/) - DRF rasmiy hujjatlari
- [DRF Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/) - Official tutorial

### Video darslar:
- [Django REST Framework - Full Course](https://www.youtube.com/watch?v=c708Nf0cHrs) - YouTube
- [Build an API with Django](https://www.youtube.com/watch?v=i5JykvxUk_A) - Traversy Media

---

## 🔗 Navigatsiya

- [⬅️ Oldingi dars - HTTP Methods](../02-http-methods/)
- [➡️ Keyingi dars - ListAPIView](../04-list-api-view/)
- [🏠 Bosh sahifa](../../)

---

## 📝 Eslatmalar

> **💡 Maslahat:** Virtual muhitni har doim aktivlashtiring! `(venv)` ko'rinishi kerak.

> **⚠️ Diqqat:** Migration qilmasdan server ishga tushmaydi yoki xatolar bo'ladi!

> **🔍 Chuqurroq:** Keyingi darslarda turli xil View'lar va Serializer'lar bilan tanishamiz.

---

**Keyingi darsda:** ListAPIView va turli filter'lar bilan ishlashni o'rganamiz!

**Tabriklayman! Birinchi Django REST API'ngizni yaratdingiz! 🎉**