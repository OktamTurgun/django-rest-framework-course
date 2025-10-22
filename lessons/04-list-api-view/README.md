# Lesson 04: Django REST Framework ListAPIView

## Maqsad
Ushbu darsda Django REST Framework'ning ListAPIView class-based view'ini o'rganamiz va kitoblar ro'yxatini API orqali olish uchun ishlatamiz.

## O'rganilishi kerak bo'lgan mavzular

### 1. Django REST Framework o'rnatish
- DRF ni pipenv orqali o'rnatish
- settings.py da konfiguratsiya qilish

### 2. Serializers
- Serializer nima va nima uchun kerak?
- ModelSerializer yaratish
- Book modeli uchun serializer yozish

### 3. ListAPIView
- Generic views nima?
- ListAPIView nima qiladi?
- queryset va serializer_class atributlari

### 4. URL routing
- API endpoint yaratish
- URL patterns konfiguratsiya

## Amaliy qism

### Boshlash
```bash
cd lessons/04-list-api-view/code/library-project
pipenv install djangorestframework
pipenv shell
python manage.py runserver
```

### Yaratilishi kerak bo'lgan fayllar
1. `books/serializers.py` - BookSerializer
2. `books/views.py` - BookListView (ListAPIView)
3. `books/urls.py` - API URL patterns
4. `library_project/urls.py` - Include books URLs

## API Endpoints
- `GET /api/books/` - Barcha kitoblar ro'yxati

## Resurslar
- [DRF Official Docs](https://www.django-rest-framework.org/)
- [Generic Views](https://www.django-rest-framework.org/api-guide/generic-views/)
- [Serializers](https://www.django-rest-framework.org/api-guide/serializers/)