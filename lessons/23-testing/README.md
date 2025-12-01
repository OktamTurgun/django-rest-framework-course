# Lesson 23: Unit Testing in Django REST Framework

## Dars haqida

Bu darsda Django REST Framework'da professional darajada testlar yozishni o'rganamiz.

## O'rganish natijalari

Ushbu darsni tugatgandan so'ng siz:

✅ APITestCase bilan API endpoint'larini test qila olasiz
✅ setUp va setUpTestData metodlaridan foydalana olasiz
✅ Factory Boy yordamida test ma'lumotlarini yarata olasiz
✅ Coverage.py bilan kod qamrovini o'lchay olasiz
✅ Integration testlar yoza olasiz
✅ Mock obyektlardan foydalana olasiz
✅ Testing best practices'larni qo'llay olasiz

## Dars strukturasi

```
23-testing/
├── README.md              # Asosiy qo'llanma (siz shu faylni o'qiyapsiz)
├── homework.md            # Uy vazifasi
├── code/
│   └── library-project/   # Amaliy loyiha
│       └── books/
│           └── tests/
│               ├── __init__.py
│               ├── test_models.py
│               ├── test_views.py
│               ├── test_serializers.py
│               └── test_integration.py
└── examples/
    ├── README.md
    ├── 01-basic-tests.py
    ├── 02-test-fixtures.py
    ├── 03-factory-boy.py
    ├── 04-coverage.py
    ├── 05-integration-tests.py
    └── 06-mocking.py
```

## Mavzular

### 1 APITestCase Basics
- Test yozishga kirish
- APIClient metodlari
- Assertion'lar
- Test ma'lumotlari yaratish

### 2 Test Fixtures
- setUp metodi
- setUpTestData metodi
- tearDown metodlari
- Test ma'lumotlarini qayta ishlatish

### 3 Factory Boy
- O'rnatish va sozlash
- Factory'lar yaratish
- Faker bilan integratsiya
- SubFactory va RelatedFactory

### 4 Test Coverage
- Coverage.py o'rnatish
- Coverage hisobotlari
- HTML hisobotlar
- Coverage yaxshilash

### 5 Integration Tests
- Integration vs Unit testlar
- API workflow testlari
- Multi-step testlar
- Database state tekshirish

### 6 Mocking
- unittest.mock
- patch decorator
- Mock return_value
- Mock side_effect
- External API'larni mock qilish

### 7 Best Practices
- Test nomlash
- Test strukturasi
- Test izolatsiyasi
- CI/CD integratsiya

## 🛠 Kerakli kutubxonalar

```bash
pip install pytest
pip install pytest-django
pip install factory-boy
pip install coverage
pip install faker
```

## Testlarni ishga tushirish

```bash
# Barcha testlar
python manage.py test

# Muayyan app
python manage.py test books

# Muayyan test fayli
python manage.py test books.tests.test_models

# Muayyan test metodi
python manage.py test books.tests.test_models.BookModelTest.test_book_creation

# Verbose output
python manage.py test --verbosity=2

# Parallel testlar
python manage.py test --parallel
```

## 📊 Coverage hisoblash

```bash
# Coverage bilan testlarni ishga tushirish
coverage run --source='.' manage.py test

# Hisobot ko'rish
coverage report

# HTML hisobot yaratish
coverage html

# HTML hisobotni ochish
# htmlcov/index.html faylini brauzerda oching
```

## 📝 Test yozish qoidalari

1. **Test nomlari aniq bo'lsin**
   ```python
   # ❌ Yomon
   def test_1(self):
   
   # ✅ Yaxshi
   def test_book_creation_with_valid_data(self):
   ```

2. **Har bir test bitta narsani tekshirsin**
   ```python
   # ❌ Yomon
   def test_book_crud(self):
       # create, read, update, delete - barchasi bitta testda
   
   # ✅ Yaxshi
   def test_book_creation(self):
   def test_book_retrieval(self):
   def test_book_update(self):
   def test_book_deletion(self):
   ```

3. **AAA pattern: Arrange, Act, Assert**
   ```python
   def test_book_creation(self):
       # Arrange - tayyorgarlik
       data = {'title': 'Test Book', 'author': 'Test Author'}
       
       # Act - harakat
       response = self.client.post('/api/books/', data)
       
       # Assert - tekshirish
       self.assertEqual(response.status_code, 201)
   ```

4. **Test ma'lumotlarini izolatsiya qiling**
   - Har bir test o'z ma'lumotlarini yaratsin
   - Testlar bir-biriga bog'liq bo'lmasin

5. **Mock'lardan o'rinli foydalaning**
   - Tashqi servislarni mock qiling
   - Database query'larni kamaytiring

## 🎓 O'rganish tartibi

1. **examples/README.md** - Misollar qo'llanmasini o'qing
2. **examples/01-basic-tests.py** - Oddiy testlar bilan boshlang
3. **examples/02-test-fixtures.py** - Fixtures'larni o'rganing
4. **examples/03-factory-boy.py** - Factory Boy'ni o'rganing
5. **examples/04-coverage.py** - Coverage'ni o'lchashni o'rganing
6. **examples/05-integration-tests.py** - Integration testlarni yozing
7. **examples/06-mocking.py** - Mocking'ni o'rganing
8. **code/library-project/** - Amaliy loyihada mashq qiling

## Qo'shimcha resurslar

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [DRF Testing Documentation](https://www.django-rest-framework.org/api-guide/testing/)
- [Factory Boy Documentation](https://factoryboy.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)

## ❓ Savol-javoblar

**Q: Unit test va Integration test orasidagi farq nima?**
A: Unit test - bitta funksiya/metodni test qiladi. Integration test - bir nechta komponentlarning birgalikda ishlashini tekshiradi.

**Q: Qancha test coverage bo'lishi kerak?**
A: Kamida 80% bo'lishi tavsiya etiladi, lekin 100% bo'lishi shart emas. Muhim qismlar test qilingan bo'lishi kerak.

**Q: Mock qachon ishlatiladi?**
A: Tashqi servislar (email, payment, API), database query'larni kamaytirish, yoki katta ma'lumotlar bilan ishlashda.

## Keyingi qadam

Ushbu darsni tugatgandan so'ng, **Lesson 24: Deployment** ga o'ting.

---

**Muvaffaqiyatlar!**