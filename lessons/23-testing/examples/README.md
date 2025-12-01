# Testing Examples - Misollar qo'llanmasi

Bu papkada Django REST Framework'da testlar yozishning turli usullari ko'rsatilgan.

## Fayllar

### 01-basic-tests.py
**Mavzu:** APITestCase bilan oddiy testlar

**Nimani o'rganasiz:**
- APITestCase'dan foydalanish
- GET, POST, PUT, PATCH, DELETE so'rovlari
- Autentifikatsiya
- Assertion metodlari
- Response tekshirish

**Ishlatish:**
```bash
python manage.py test path.to.test.class
```

---

### 02-test-fixtures.py
**Mavzu:** setUp va setUpTestData metodlari

**Nimani o'rganasiz:**
- setUp metodi - har test uchun
- setUpTestData - barcha testlar uchun
- tearDown metodlari
- Test ma'lumotlarini qayta ishlatish
- Fixtures'lar bilan ishlash

**Ishlatish:**
```bash
python manage.py test path.to.fixtures.test
```

---

### 03-factory-boy.py
**Mavzu:** Factory Boy bilan test ma'lumotlari yaratish

**Nimani o'rganasiz:**
- Factory Boy o'rnatish
- Factory'lar yaratish
- Faker integration
- SubFactory - bog'langan obyektlar
- Trait'lar - turli variantlar

**O'rnatish:**
```bash
pip install factory-boy faker
```

**Ishlatish:**
```bash
python manage.py test path.to.factory.test
```

---

### 04-coverage.py
**Mavzu:** Code coverage o'lchash

**Nimani o'rganasiz:**
- Coverage.py o'rnatish va sozlash
- Coverage hisobotlari
- HTML hisobotlar
- Coverage yaxshilash strategiyalari
- Qaysi kod test qilinmagan?

**O'rnatish:**
```bash
pip install coverage
```

**Ishlatish:**
```bash
# Coverage bilan testni ishga tushirish
coverage run --source='.' manage.py test

# Terminal'da hisobot
coverage report

# HTML hisobot yaratish
coverage html

# Hisobotni ochish
# htmlcov/index.html faylini brauzerda oching
```

---

### 05-integration-tests.py
**Mavzu:** Integration testlar

**Nimani o'rganasiz:**
- Unit vs Integration testlar farqi
- Multi-step testlar
- Full workflow testlari
- Database state tekshirish
- Real-world scenario'lar

**Ishlatish:**
```bash
python manage.py test path.to.integration.test
```

---

### 06-mocking.py
**Mavzu:** Mocking va Mock obyektlar

**Nimani o'rganasiz:**
- unittest.mock
- @patch decorator
- Mock return_value
- Mock side_effect
- External API'larni mock qilish
- Email yuborishni mock qilish

**Ishlatish:**
```bash
python manage.py test path.to.mock.test
```

---

## O'rganish tartibi

Fayllarni **tartib bilan** o'qing:

1. **01-basic-tests.py** - Test yozishga kirish
2. **02-test-fixtures.py** - Ma'lumotlarni qayta ishlatish
3. **03-factory-boy.py** - Professional test ma'lumotlari
4. **04-coverage.py** - Kod qamrovini o'lchash
5. **05-integration-tests.py** - Kompleks testlar
6. **06-mocking.py** - Mock'lardan foydalanish

---

## Har bir misolda:

 **To'liq kod** - Copy-paste qilish mumkin
 **Tushuntirishlar** - Har qator izohli
 **Natijalar** - Kutilayotgan output
 **Keng tarqalgan xatolar** - Nima qilmaslik kerak
 **Best practices** - Professional yondashuv

---

## Testlarni ishga tushirish

### Barcha testlar
```bash
python manage.py test
```

### Muayyan app
```bash
python manage.py test books
```

### Muayyan test fayli
```bash
python manage.py test books.tests.test_models
```

### Muayyan test klassi
```bash
python manage.py test books.tests.test_models.BookModelTest
```

### Muayyan test metodi
```bash
python manage.py test books.tests.test_models.BookModelTest.test_book_creation
```

### Verbose output
```bash
python manage.py test --verbosity=2
```

### Parallel testlar (tezroq)
```bash
python manage.py test --parallel
```

### Muayyan testlarni o'tkazib yuborish
```bash
python manage.py test --exclude-tag=slow
```

---

## Foydali buyruqlar

### Coverage bilan
```bash
# Run tests with coverage
coverage run --source='.' manage.py test

# Show report in terminal
coverage report

# Show missing lines
coverage report -m

# Generate HTML report
coverage html

# Open HTML report
# Open htmlcov/index.html in browser
```

### Pytest bilan (opsional)
```bash
# Install pytest-django
pip install pytest pytest-django

# Run all tests
pytest

# Run with verbose
pytest -v

# Run specific file
pytest books/tests/test_models.py

# Run with coverage
pytest --cov=books

# HTML coverage report
pytest --cov=books --cov-report=html
```

---

## Muhim tushunchalar

### AAA Pattern
Har bir test 3 qismdan iborat:

```python
def test_example(self):
    # Arrange - tayyorgarlik
    user = User.objects.create(username='test')
    
    # Act - harakat
    response = self.client.get('/api/books/')
    
    # Assert - tekshirish
    self.assertEqual(response.status_code, 200)
```

### Test izolatsiyasi
Har bir test mustaqil bo'lishi kerak:

```python
# ❌ Yomon - testlar bog'liq
def test_create_book(self):
    Book.objects.create(title='Book 1')

def test_book_exists(self):
    self.assertEqual(Book.objects.count(), 1)  # Birinchi testga bog'liq!

# ✅ Yaxshi - har test mustaqil
def test_create_book(self):
    Book.objects.create(title='Book 1')
    self.assertEqual(Book.objects.count(), 1)

def test_book_exists(self):
    Book.objects.create(title='Book 2')
    self.assertEqual(Book.objects.count(), 1)
```

### Naming conventions
Test nomlari descriptive bo'lsin:

```python
# ❌ Yomon
def test_1(self):
def test_book(self):
def test_api(self):

# ✅ Yaxshi
def test_book_creation_with_valid_data(self):
def test_book_creation_without_authentication_fails(self):
def test_api_returns_404_for_nonexistent_book(self):
```

---

## Keyingi qadam

Fayllarni tartib bilan o'qing va har birini amalda sinab ko'ring!

**Omad!**