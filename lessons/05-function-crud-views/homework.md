# Uy vazifasi - 05: Function va CRUD Views

> **Qiyinlik darajasi:** ⭐⭐⭐☆☆ (3/5)  
> **Taxminiy vaqt:** 90-120 daqiqa

## 🎯 Maqsad

Function-based view'lar yordamida to'liq CRUD operatsiyalarini mustaqil amalga oshirish, HTTP metodlar va status kodlar bilan ishlashni o'rganish.

---

## 📋 Vazifalar

### Vazifa 1: Movie API yaratish ⭐⭐

**Tavsif:** Film ma'lumotlarini boshqarish uchun REST API yarating.

**Model talablari:**
```python
class Movie(models.Model):
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=100)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # 0.0 - 10.0
    duration = models.IntegerField(help_text="Daqiqalarda")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**API Endpoints:**
- [ ] `GET /api/movies/` - Barcha filmlar ro'yxati
- [ ] `POST /api/movies/` - Yangi film qo'shish
- [ ] `GET /api/movies/{id}/` - Bitta filmni ko'rish
- [ ] `PUT /api/movies/{id}/` - Filmni yangilash
- [ ] `DELETE /api/movies/{id}/` - Filmni o'chirish

**Qo'shimcha talablar:**
- Serializer yarating
- Xatoliklarni to'g'ri handle qiling (404, 400)
- To'g'ri status kodlardan foydalaning

---

### Vazifa 2: Filterlash va Qidiruv ⭐⭐⭐

**Tavsif:** Movie API'ga qidiruv va filterlash funksiyasini qo'shing.

**Talablar:**

**1. Genre bo'yicha filterlash:**
```http
GET /api/movies/?genre=Action
```

**2. Yil bo'yicha filterlash:**
```http
GET /api/movies/?year=2024
```

**3. Nom bo'yicha qidiruv:**
```http
GET /api/movies/?search=Avengers
```

**Maslahat:**
```python
# Query parametrlarni olish
genre = request.query_params.get('genre', None)
search = request.query_params.get('search', None)

# Filterlash
if genre:
    movies = movies.filter(genre=genre)
if search:
    movies = movies.filter(title__icontains=search)
```

---

### Vazifa 3: Partial Update (PATCH) ⭐⭐⭐

**Tavsif:** Filmning faqat bir nechta maydonlarini yangilash imkoniyatini qo'shing.

**Endpoint:**
```http
PATCH /api/movies/{id}/
Content-Type: application/json

{
    "rating": 9.5,
    "is_available": false
}
```

**Talablar:**
- Faqat yuborilgan maydonlar yangilansin
- Qolgan maydonlar o'zgarmaydi
- `partial=True` parametridan foydalaning

**Kod namunasi:**
```python
@api_view(['PATCH'])
def movie_partial_update(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(
            {'error': 'Film topilmadi'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = MovieSerializer(movie, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

---

### Vazifa 4: Custom Validation ⭐⭐⭐⭐ (Bonus)

**Tavsif:** Serializer'ga custom validation qo'shing.

**Validatsiya qoidalari:**
1. Rating 0.0 dan 10.0 gacha bo'lishi kerak
2. Release year 1900 dan hozirgi yilgacha bo'lishi kerak
3. Duration 1 daqiqadan ko'p bo'lishi kerak
4. Title kamida 2 ta harf bo'lishi kerak

**Kod namunasi:**
```python
from rest_framework import serializers
from datetime import datetime

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
    
    def validate_rating(self, value):
        if value < 0.0 or value > 10.0:
            raise serializers.ValidationError(
                "Rating 0.0 dan 10.0 gacha bo'lishi kerak"
            )
        return value
    
    def validate_release_year(self, value):
        current_year = datetime.now().year
        if value < 1900 or value > current_year:
            raise serializers.ValidationError(
                f"Yil 1900 dan {current_year} gacha bo'lishi kerak"
            )
        return value
    
    def validate_duration(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Davomiylik 1 daqiqadan ko'p bo'lishi kerak"
            )
        return value
    
    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "Sarlavha kamida 2 ta belgidan iborat bo'lishi kerak"
            )
        return value
```

**Qo'shimcha ball:** +15

---

### Vazifa 5: Statistika API ⭐⭐⭐⭐ (Bonus)

**Tavsif:** Filmlar statistikasini qaytaradigan endpoint yarating.

**Endpoint:**
```http
GET /api/movies/stats/
```

**Javob formati:**
```json
{
    "total_movies": 100,
    "available_movies": 85,
    "genres": {
        "Action": 30,
        "Drama": 25,
        "Comedy": 20,
        "Sci-Fi": 15,
        "Horror": 10
    },
    "average_rating": 7.5,
    "highest_rated": {
        "id": 5,
        "title": "The Shawshank Redemption",
        "rating": 9.8
    },
    "latest_added": {
        "id": 100,
        "title": "Dune Part 2",
        "created_at": "2024-10-23T10:30:00Z"
    }
}
```

**Maslahat:**
```python
from django.db.models import Count, Avg, Max

@api_view(['GET'])
def movie_stats(request):
    total = Movie.objects.count()
    available = Movie.objects.filter(is_available=True).count()
    
    # Genre bo'yicha count
    genres = Movie.objects.values('genre').annotate(count=Count('id'))
    
    # O'rtacha rating
    avg_rating = Movie.objects.aggregate(Avg('rating'))['rating__avg']
    
    # Eng yuqori rating
    highest = Movie.objects.order_by('-rating').first()
    
    # Oxirgi qo'shilgan
    latest = Movie.objects.order_by('-created_at').first()
    
    # Response yaratish
    data = {
        'total_movies': total,
        'available_movies': available,
        'genres': {item['genre']: item['count'] for item in genres},
        'average_rating': round(avg_rating, 1) if avg_rating else 0,
        'highest_rated': MovieSerializer(highest).data if highest else None,
        'latest_added': MovieSerializer(latest).data if latest else None,
    }
    
    return Response(data)
```

**Qo'shimcha ball:** +20

---

## 📦 Topshirish

### 1. Repository yarating
```bash
git init
git add .
git commit -m "Add Movie CRUD API"
```

### 2. GitHub'ga yuklang
```bash
git remote add origin <your-repo-url>
git push -u origin main
```

### 3. README.md yarating

Loyihangizda `README.md` bo'lishi kerak:

```markdown
# Movie API

Django REST Framework yordamida yaratilgan Movie CRUD API

## Features
- ✅ CRUD operatsiyalari
- ✅ Filterlash va qidiruv
- ✅ Partial update
- ✅ Custom validation
- ✅ Statistika API

## Setup
1. Virtual environment yarating
2. Dependencylarni o'rnating: `pip install -r requirements.txt`
3. Migrate qiling: `python manage.py migrate`
4. Serverni ishga tushiring: `python manage.py runserver`

## API Endpoints
- GET /api/movies/ - Barcha filmlar
- POST /api/movies/ - Yangi film
- GET /api/movies/{id}/ - Bitta film
- PUT /api/movies/{id}/ - Filmni yangilash
- PATCH /api/movies/{id}/ - Qisman yangilash
- DELETE /api/movies/{id}/ - Filmni o'chirish
- GET /api/movies/stats/ - Statistika

## Testing
Postman yoki cURL bilan test qiling
```

---

## ✅ Baholash mezonlari

| Vazifa | Ball | Tavsif |
|--------|------|--------|
| Vazifa 1 | 30 | CRUD operatsiyalari to'g'ri ishlaydi |
| Vazifa 2 | 20 | Filterlash va qidiruv qo'shilgan |
| Vazifa 3 | 20 | Partial update ishlaydi |
| Vazifa 4 | 15 | Custom validation qo'shilgan |
| Vazifa 5 | 20 | Statistika API yaratilgan |
| README | 5 | To'liq va tushunarli |
| **Jami** | **110** | A+ uchun 100+ ball yetarli |

---

## 💡 Maslahatlar

1. **Kichik qadamlar bilan boshlang** - Birinchi CRUD'ni yarating, keyin qolganlarini qo'shing
2. **Postman'da test qiling** - Har bir endpoint'ni yozganingizdan keyin test qiling
3. **Git commit'lar qiling** - Har bir vazifadan keyin commit qiling
4. **Xatoliklardan qo'rqmang** - Xato - bu o'rganishning bir qismi!
5. **Dokumentatsiyani o'qing** - DRF docs juda foydali

---

## 🆘 Yordam kerakmi?

- DRF Documentation: https://www.django-rest-framework.org/
- Django Aggregation: https://docs.djangoproject.com/en/stable/topics/db/aggregation/
- HTTP Status Codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

---

## 📅 Topshirish muddati

**3 kun ichida** (darsdan keyin)

---

**Omad yor bo'lsin! 🚀**