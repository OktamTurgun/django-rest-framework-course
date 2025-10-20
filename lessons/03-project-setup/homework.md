# Uy vazifasi - 03: Loyihani boshlash

> **Qiyinlik darajasi:** ⭐⭐⭐⭐☆ (4/5)  
> **Taxminiy vaqt:** 90-120 daqiqa

## 🎯 Maqsad

O'z Django REST API loyihangizni yaratish va to'liq CRUD funksionalligini qo'shish.

---

## 📋 Vazifalar

### Vazifa 1: Loyiha yaratish ⭐⭐

**Tavsif:** "Books API" loyihasi yarating.

**Talablar:**
- [ ] Virtual muhit yarating
- [ ] Django va DRF o'rnating
- [ ] `library_project` nomli loyiha yarating
- [ ] `books` nomli app yarating
- [ ] Settings.py'da to'g'ri sozlang

---

### Vazifa 2: Book modeli ⭐⭐⭐

**Tavsif:** Kitob modeli yarating.

**Talablar:**
- [ ] `Book` nomli model yarating
- [ ] Fieldlar: title, author, isbn, published_date, pages, price, description
- [ ] `__str__` metodini qo'shing
- [ ] Migration yarating va apply qiling

**Model namunasi:**
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

### Vazifa 3: API yaratish ⭐⭐⭐⭐

**Tavsif:** To'liq CRUD API yarating.

**Talablar:**
- [ ] BookSerializer yarating
- [ ] List va Create view
- [ ] Detail, Update, Delete view
- [ ] URL routing to'g'ri sozlang
- [ ] Kamida 5 ta kitob qo'shing

**Endpoint'lar:**
- `GET /api/books/` - Barcha kitoblar
- `POST /api/books/` - Yangi kitob
- `GET /api/books/<id>/` - Bitta kitob
- `PUT/PATCH /api/books/<id>/` - Yangilash
- `DELETE /api/books/<id>/` - O'chirish

---

### Vazifa 4: Admin panel ⭐⭐

**Tavsif:** Admin panel sozlang.

**Talablar:**
- [ ] Book modelini admin'ga register qiling
- [ ] list_display, list_filter, search_fields qo'shing
- [ ] Superuser yarating

---

### Bonus: Filter va Search ⭐⭐⭐⭐⭐

**Tavsif:** Author bo'yicha filter va search qo'shing.

**Qo'shimcha ball:** +15

---

## ✅ Topshirish

1. Loyihangizni GitHub'ga yuklang
2. README.md ga qanday ishlatish ko'rsatmasi yozing
3. requirements.txt yarating: `pip freeze > requirements.txt`

**Omad yor bo'lsin!**