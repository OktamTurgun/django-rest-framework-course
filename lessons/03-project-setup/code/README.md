# Dars 03 - Django REST API Loyihasi

Bu papkada to'liq ishlagan Django REST API loyihasi mavjud.

## 📦 Loyiha tuzilishi
```
simple_api/                 # Asosiy papka
├── api_project/            # Django project
│   ├── __init__.py
│   ├── settings.py         # Sozlamalar
│   ├── urls.py             # Asosiy URL routing
│   ├── wsgi.py
│   └── asgi.py
├── products/               # Products app
│   ├── migrations/         # Database migrations
│   ├── __init__.py
│   ├── admin.py            # Admin panel
│   ├── apps.py
│   ├── models.py           # Product modeli
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # API views
│   ├── urls.py             # App URL'lar
│   └── tests.py
├── manage.py               # Django CLI
└── db.sqlite3              # Database (avtomatik yaratiladi)
```

## 🚀 O'rnatish va ishga tushirish

### 1. Virtual muhit yaratish
```bash
# Windows (pipenv)
cd simple_api
pipenv install django djangorestframework
pipenv shell

# yoki venv
python -m venv venv
venv\Scripts\activate
pip install -r ../requirements.txt
```

### 2. Database yaratish
```bash
python manage.py migrate
```

### 3. Admin user yaratish (ixtiyoriy)
```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123
```

### 4. Serverni ishga tushirish
```bash
python manage.py runserver
```

Server ishga tushdi: `http://127.0.0.1:8000/`

---

## 🔗 API Endpoints

### Mahsulotlar (Products)

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/products/` | Barcha mahsulotlar |
| POST | `/api/products/` | Yangi mahsulot yaratish |
| GET | `/api/products/{id}/` | Bitta mahsulot |
| PUT | `/api/products/{id}/` | To'liq yangilash |
| PATCH | `/api/products/{id}/` | Qisman yangilash |
| DELETE | `/api/products/{id}/` | O'chirish |

---

## 🧪 Test qilish

### 1. Brauzerda
```
http://127.0.0.1:8000/api/products/
```

DRF'ning browsable API'sida to'g'ridan-to'g'ri test qilishingiz mumkin!

### 2. cURL orqali
```bash
# GET - Barcha mahsulotlar
curl http://127.0.0.1:8000/api/products/

# POST - Yangi mahsulot
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "Dell Latitude 5000",
    "price": "5000000.00",
    "stock": 10
  }'

# GET - Bitta mahsulot
curl http://127.0.0.1:8000/api/products/1/

# PUT - Yangilash
curl -X PUT http://127.0.0.1:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Laptop",
    "description": "Updated description",
    "price": "6000000.00",
    "stock": 5
  }'

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
    "name": "Mouse",
    "description": "Wireless mouse",
    "price": "150000.00",
    "stock": 50
}
response = requests.post(BASE_URL, json=new_product)
print(response.status_code)  # 201
```

---

## 📝 Muhim fayllar

### models.py
Product modelini o'z ichiga oladi:
- name (CharField)
- description (TextField)
- price (DecimalField)
- stock (IntegerField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

### serializers.py
ModelSerializer yordamida Product'ni JSON'ga aylantiradi.

### views.py
Generic views:
- `ListCreateAPIView` - List va Create
- `RetrieveUpdateDestroyAPIView` - Detail, Update, Delete

### urls.py
API routing.

---

## 🎯 O'rganish uchun topshiriqlar

1. **Admin panel**
   - `http://127.0.0.1:8000/admin/` ochib, mahsulotlar qo'shing

2. **Yangi field qo'shish**
   - `models.py`da yangi field qo'shing (masalan: `category`)
   - Migration yarating: `python manage.py makemigrations`
   - Apply qiling: `python manage.py migrate`

3. **Filter qo'shish**
   - `views.py`da filter qo'shing (price bo'yicha, stock bo'yicha)

4. **Yangi model yaratish**
   - `Category` modeli yarating
   - Product bilan ForeignKey bog'lang

---

## ⚠️ Keng tarqalgan xatolar

### 1. "No module named 'rest_framework'"
```bash
pip install djangorestframework
# yoki
pipenv install djangorestframework
```

### 2. "Table doesn't exist"
```bash
python manage.py migrate
```

### 3. Port band
```bash
# Boshqa port ishlatish
python manage.py runserver 8001
```

---

## 📚 Qo'shimcha

- Django admin: `http://127.0.0.1:8000/admin/`
- API root: `http://127.0.0.1:8000/api/`
- DRF hujjatlari: https://www.django-rest-framework.org/

## 📁 Ikkinchi loyiha - library_project

Bu papkada `library_project` ham bor - bu pipenv va python-decouple bilan yaratilgan. 
O'sha loyihani ham o'rganish uchun ishlatishingiz mumkin!

**Omad yor bo'lsin! 🚀**