# Uyga vazifa: Serializer vs ModelSerializer

## Maqsad
Serializer va ModelSerializer o'rtasidagi farqlarni amalda o'rganish va turli vaziyatlarda qaysi birini ishlatish kerakligini tushunish.

---

## Vazifa 1: Author modeli va Serializer yaratish

### 1.1. Author modelini yaratish

`books/models.py` fayliga quyidagi modelni qo'shing:
```python
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    biography = models.TextField()
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['last_name', 'first_name']
```

**Bajarish:**
- Modelni yarating
- Migration qiling
- Admin panelga register qiling

### 1.2. Oddiy Serializer yaratish

`books/serializers.py` da `AuthorSerializer` yarating (oddiy Serializer):

**Talablar:**
- Barcha fieldlarni qo'lda yozing
- `create()` metodini yozing
- `update()` metodini yozing
- Custom validation qo'shing:
  - `birth_date` kelajakda bo'lmasligi kerak
  - `email` to'g'ri formatda bo'lishi kerak (DRF o'zi tekshiradi)

### 1.3. CRUD APIView'lar yaratish

`books/views.py` da quyidagi view'larni yarating:
```python
class AuthorListCreateView(APIView):
    """
    GET: Barcha mualliflar
    POST: Yangi muallif yaratish
    """
    pass

class AuthorDetailView(APIView):
    """
    GET: Bitta muallif
    PUT: Muallifni yangilash
    DELETE: Muallifni o'chirish
    """
    pass
```

**URL'lar:**
- `GET/POST /api/authors/`
- `GET/PUT/DELETE /api/authors/<int:pk>/`

---

## Vazifa 2: Category modeli va ModelSerializer

### 2.1. Category modelini yaratish
```python
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
```

### 2.2. ModelSerializer yaratish

`CategorySerializer` yarating (ModelSerializer):

**Talablar:**
- ModelSerializer'dan foydalaning
- `created_at` ni read-only qiling
- Qo'shimcha field qo'shing: `books_count` (bu kategoryadagi kitoblar soni)

### 2.3. View'lar yaratish (10 ball)

Generic view'lardan foydalaning:
```python
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
```

---

## Vazifa 3: Book modelini yangilash va Relationship

### 3.1. Book modeliga ForeignKey qo'shish
```python
class Book(models.Model):
    # ... mavjud fieldlar ...
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
```

**Eslatma:** Migration qilishda muammo bo'lsa:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3.2. Nested Serializer yaratish

`BookDetailSerializer` yarating:
```python
class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Book
        fields = '__all__'
```

---

## Vazifa 4: Custom Validation

### 4.1. Kitob narxi validatsiyasi

Kitobning narxi **10$** dan kam bo'lmasligi kerakligini ta'minlang:

- `BookSerializer` da
- `BookModelSerializer` da

### 4.2. ISBN uniqueness

Bir xil ISBN bilan ikkinchi kitob yaratilmasligi kerak:
```python
def validate_isbn(self, value):
    # Yangi kitob yaratilayotganda
    if not self.instance:  # yangi obyekt
        if Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("Bu ISBN allaqachon mavjud")
    # Mavjud kitob yangilanayotganda
    else:
        if Book.objects.filter(isbn=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Bu ISBN allaqachon mavjud")
    return value
```

---

## Bonus vazifa

### Search va Filter qo'shish

1. **Author qidiruv:**
   - Ism bo'yicha qidirish
   - Mamlakat bo'yicha filter

2. **Book qidiruv:**
   - Title bo'yicha qidirish
   - Author bo'yicha filter
   - Category bo'yicha filter
   - Narx oralig'i bo'yicha filter

**Masalan:**
```
GET /api/books/?author=1&category=2&min_price=10&max_price=50
```

---

## Topshirish tartibi

### 1. Kod yozish
- Barcha vazifalarni bajaring
- Har bir qismdan keyin test qiling

### 2. Test qilish
Postman yoki Swagger orqali:
-  Author CRUD
-  Category CRUD
-  Book CRUD
-  Validation'lar ishlayotganini tekshiring

### 3. Git Commit
```bash
git add .
git commit -m "feat: Complete homework 10 - Serializers comparison"
git push origin main
```

### 4. Screenshot'lar
Quyidagi screenshot'larni oling:
- Author list
- Author create (POST)
- Category list
- Book detail (nested serializers bilan)
- Validation error (narx 10$ dan kam bo'lganda)

### 5. Hisobot

`HOMEWORK_REPORT.md` fayl yarating:
```markdown
# Homework 10 Hisoboti

## Bajargan vazifalarim
- [x] Vazifa 1: Author modeli va Serializer
- [x] Vazifa 2: Category va ModelSerializer
- [x] Vazifa 3: Relationships
- [x] Vazifa 4: Validation
- [ ] Bonus: Search va Filter

## Qiyinchiliklar
1. ...
2. ...

## O'rgangan narsalarim
1. Serializer va ModelSerializer farqlari
2. Custom validation
3. Nested serializers

## Screenshot'lar
[Screenshot'larni qo'shing]
```

---

**Topshirish muddati:** Keyingi darsdan oldin

---

## Yordam
Agar qiyinchilik bo'lsa:
1. Django REST Framework dokumentatsiyasini o'qing
2. Oldingi darslarni qayta ko'ring
3. GitHub'dagi kod namunalarini ko'ring