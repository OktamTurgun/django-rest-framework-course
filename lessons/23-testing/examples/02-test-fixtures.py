"""
Lesson 23: Test Fixtures - setUp, setUpTestData, tearDown
==========================================================

Bu faylda test fixtures'larni o'rganamiz:
- setUp() - har bir test oldidan
- setUpTestData() - barcha testlar oldidan (bir marta)
- tearDown() - har bir test keyin
- tearDownClass() - barcha testlar keyin

Fixtures - bu testlar uchun kerakli ma'lumotlarni tayyorlash usuli.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from books.models import Book, Author, Category
from decimal import Decimal


# =============================================================================
# 1. setUp vs setUpTestData - FARQI
# =============================================================================

class SetUpVsSetUpTestDataExample(APITestCase):
    """
    setUp() va setUpTestData() orasidagi farqni tushunish
    
    setUp() - har bir test oldidan qayta ishga tushadi
    setUpTestData() - faqat bir marta (barcha testlar uchun)
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Bu metod FAQAT BIR MARTA ishga tushadi (barcha testlar uchun)
        
        Qachon ishlatiladi:
        - Read-only ma'lumotlar uchun
        - O'zgarmaydigan ma'lumotlar uchun
        - Tezroq testlar uchun (database'ga kamroq murojaat)
        
        MUHIM: Bu yerda yaratilgan obyektlarni testlarda o'zgartirmang!
        """
        print("\n🔵 setUpTestData() ishga tushdi")
        
        # Bu user barcha testlar uchun
        cls.readonly_user = User.objects.create_user(
            username='readonly',
            password='password123'
        )
        
        # Bu category barcha testlar uchun
        cls.readonly_category = Category.objects.create(
            name='Fiction',
            description='Fiction books'
        )
        
    def setUp(self):
        """
        Bu metod HAR BIR TEST OLDIDAN ishga tushadi
        
        Qachon ishlatiladi:
        - Test'da o'zgaradigan ma'lumotlar uchun
        - Har test uchun yangi holatda ma'lumot kerak bo'lsa
        - Authentication setup
        
        MUHIM: Bu yerda yaratilgan obyektlar har test uchun yangi!
        """
        print("🟢 setUp() ishga tushdi")
        
        # Har test uchun yangi user
        self.user = User.objects.create_user(
            username=f'user_{id(self)}',  # Har safar yangi username
            password='password123'
        )
        
        # Har test uchun yangi kitob
        self.book = Book.objects.create(
            title=f'Test Book {id(self)}',
            author='Test Author',
            isbn=f'123456789{id(self)}',
            category=self.readonly_category
        )
    
    def tearDown(self):
        """
        Bu metod HAR BIR TEST KEYIN ishga tushadi
        
        Qachon ishlatiladi:
        - Temporary fayllarni o'chirish
        - Cache'ni tozalash
        - External service'larni disconnect qilish
        """
        print("🔴 tearDown() ishga tushdi")
        # Bu yerda cleanup ishlarini qilish mumkin
        pass
    
    @classmethod
    def tearDownClass(cls):
        """
        Bu metod FAQAT BIR MARTA ishga tushadi (barcha testlar keyin)
        """
        print("🟣 tearDownClass() ishga tushdi\n")
        super().tearDownClass()
    
    def test_first_test(self):
        """Birinchi test"""
        print("  ➡️  test_first_test() bajarilmoqda")
        self.assertTrue(True)
    
    def test_second_test(self):
        """Ikkinchi test"""
        print("  ➡️  test_second_test() bajarilmoqda")
        self.assertTrue(True)
    
    def test_third_test(self):
        """Uchinchi test"""
        print("  ➡️  test_third_test() bajarilmoqda")
        self.assertTrue(True)


"""
KONSOL OUTPUT:
--------------
🔵 setUpTestData() ishga tushdi
🟢 setUp() ishga tushdi
  ➡️  test_first_test() bajarilmoqda
🔴 tearDown() ishga tushdi
🟢 setUp() ishga tushdi
  ➡️  test_second_test() bajarilmoqda
🔴 tearDown() ishga tushdi
🟢 setUp() ishga tushdi
  ➡️  test_third_test() bajarilmoqda
🔴 tearDown() ishga tushdi
🟣 tearDownClass() ishga tushdi

Ko'ryapsizmi?
- setUpTestData: 1 marta
- setUp: 3 marta (har test uchun)
- tearDown: 3 marta (har test keyin)
- tearDownClass: 1 marta
"""


# =============================================================================
# 2. setUpTestData - READ-ONLY MA'LUMOTLAR
# =============================================================================

class ReadOnlyDataTest(APITestCase):
    """
    setUpTestData() faqat o'qish uchun kerakli ma'lumotlar uchun
    """
    
    @classmethod
    def setUpTestData(cls):
        """Bir marta ma'lumot yaratamiz"""
        # Categories (o'zgarmaydi)
        cls.fiction = Category.objects.create(name='Fiction')
        cls.science = Category.objects.create(name='Science')
        cls.history = Category.objects.create(name='History')
        
        # Authors (o'zgarmaydi)
        cls.author1 = Author.objects.create(
            name='John Doe',
            bio='Famous author'
        )
        cls.author2 = Author.objects.create(
            name='Jane Smith',
            bio='Award winning author'
        )
        
        # Books (o'zgarmaydi)
        cls.book1 = Book.objects.create(
            title='Book One',
            author=cls.author1,
            category=cls.fiction,
            isbn='1111111111111'
        )
        cls.book2 = Book.objects.create(
            title='Book Two',
            author=cls.author2,
            category=cls.science,
            isbn='2222222222222'
        )
    
    def test_categories_count(self):
        """Categories sonini tekshirish"""
        self.assertEqual(Category.objects.count(), 3)
    
    def test_authors_count(self):
        """Authors sonini tekshirish"""
        self.assertEqual(Author.objects.count(), 2)
    
    def test_books_count(self):
        """Books sonini tekshirish"""
        self.assertEqual(Book.objects.count(), 2)
    
    def test_book_has_category(self):
        """Kitobda category borligini tekshirish"""
        self.assertEqual(self.book1.category, self.fiction)
    
    def test_book_has_author(self):
        """Kitobda author borligini tekshirish"""
        self.assertEqual(self.book1.author, self.author1)


# =============================================================================
# 3. setUp - HAR TEST UCHUN YANGI MA'LUMOT
# =============================================================================

class DynamicDataTest(APITestCase):
    """
    setUp() har test uchun yangi ma'lumot yaratadi
    """
    
    @classmethod
    def setUpTestData(cls):
        """Umumiy read-only ma'lumotlar"""
        cls.category = Category.objects.create(name='Test Category')
    
    def setUp(self):
        """Har test uchun yangi ma'lumot"""
        # Har test uchun yangi user
        self.user = User.objects.create_user(
            username=f'testuser_{id(self)}',
            password='testpass123'
        )
        
        # Har test uchun yangi kitob
        self.book = Book.objects.create(
            title=f'Test Book {id(self)}',
            author='Test Author',
            isbn=f'ISBN{id(self)}',
            category=self.category,
            price=Decimal('10.00')
        )
        
        # Authentication
        self.client.force_authenticate(user=self.user)
    
    def test_update_book_price(self):
        """Kitob narxini o'zgartirish"""
        # Narxni o'zgartirish
        self.book.price = Decimal('20.00')
        self.book.save()
        
        # Tekshirish
        self.book.refresh_from_db()
        self.assertEqual(self.book.price, Decimal('20.00'))
    
    def test_update_book_title(self):
        """Kitob nomini o'zgartirish"""
        # Nomni o'zgartirish
        self.book.title = 'Updated Title'
        self.book.save()
        
        # Tekshirish
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')
    
    def test_delete_book(self):
        """Kitobni o'chirish"""
        book_id = self.book.id
        self.book.delete()
        
        # Kitob o'chirilganini tekshirish
        self.assertFalse(Book.objects.filter(id=book_id).exists())


# =============================================================================
# 4. COMPLEX FIXTURES - MURAKKAB MA'LUMOTLAR
# =============================================================================

class ComplexFixturesTest(APITestCase):
    """
    Murakkab bog'langan ma'lumotlar bilan ishlash
    """
    
    @classmethod
    def setUpTestData(cls):
        """Murakkab ma'lumotlar strukturasi"""
        # Categories
        cls.fiction = Category.objects.create(name='Fiction')
        cls.science = Category.objects.create(name='Science')
        
        # Authors
        cls.authors = []
        for i in range(3):
            author = Author.objects.create(
                name=f'Author {i+1}',
                bio=f'Bio for author {i+1}'
            )
            cls.authors.append(author)
        
        # Books for each author
        cls.books = []
        for i, author in enumerate(cls.authors):
            for j in range(2):  # Har author uchun 2 ta kitob
                book = Book.objects.create(
                    title=f'Book {i+1}-{j+1}',
                    author=author,
                    category=cls.fiction if i % 2 == 0 else cls.science,
                    isbn=f'{i}{j}1234567890',
                    price=Decimal(f'{10 + i + j}.99')
                )
                cls.books.append(book)
    
    def setUp(self):
        """Har test uchun authentication"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_total_authors(self):
        """Umumiy authors soni"""
        self.assertEqual(Author.objects.count(), 3)
    
    def test_total_books(self):
        """Umumiy books soni"""
        self.assertEqual(Book.objects.count(), 6)  # 3 authors * 2 books
    
    def test_books_per_author(self):
        """Har bir author'ning kitoblari soni"""
        for author in self.authors:
            self.assertEqual(author.books.count(), 2)
    
    def test_fiction_books_count(self):
        """Fiction kategoriyasidagi kitoblar"""
        fiction_books = Book.objects.filter(category=self.fiction)
        self.assertEqual(fiction_books.count(), 4)  # 2 authors * 2 books
    
    def test_get_books_api(self):
        """API orqali kitoblar ro'yxatini olish"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)


# =============================================================================
# 5. FIXTURE FILES - JSON/YAML FIXTURES
# =============================================================================

class FixtureFilesExample(APITestCase):
    """
    JSON yoki YAML fixtures fayllaridan foydalanish
    
    Fixtures fayllar - bu ma'lumotlarni JSON/YAML formatda saqlash
    va testlarda yuklash imkonini beradi.
    """
    
    # Fixtures faylni ko'rsatish
    fixtures = ['test_data.json']
    
    def test_data_loaded_from_fixture(self):
        """
        Fixtures fayldan ma'lumot yuklanganini tekshirish
        
        test_data.json fayli quyidagicha bo'lishi mumkin:
        [
            {
                "model": "books.category",
                "pk": 1,
                "fields": {
                    "name": "Fiction",
                    "description": "Fiction books"
                }
            },
            {
                "model": "books.book",
                "pk": 1,
                "fields": {
                    "title": "Test Book",
                    "author": "Test Author",
                    "category": 1,
                    "isbn": "1234567890123"
                }
            }
        ]
        """
        # Fixtures'dan yuklangan ma'lumotlarni tekshirish
        self.assertTrue(Category.objects.filter(name='Fiction').exists())
        self.assertTrue(Book.objects.filter(title='Test Book').exists())


# =============================================================================
# 6. BEST PRACTICES
# =============================================================================

class BestPracticesTest(APITestCase):
    """
    Test fixtures uchun best practices
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        ✅ BEST PRACTICE #1: setUpTestData uchun read-only ma'lumotlar
        """
        cls.category = Category.objects.create(name='Test Category')
        cls.author = Author.objects.create(name='Test Author')
    
    def setUp(self):
        """
        ✅ BEST PRACTICE #2: setUp uchun test-specific ma'lumotlar
        """
        self.user = User.objects.create_user(
            username=f'user_{id(self)}',
            password='password'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_with_minimal_data(self):
        """
        ✅ BEST PRACTICE #3: Minimal kerakli ma'lumot yarating
        
        Faqat test uchun kerakli ma'lumotlarni yarating
        """
        book = Book.objects.create(
            title='Minimal Book',
            author=self.author,
            category=self.category,
            isbn='1234567890123'
        )
        self.assertIsNotNone(book.id)
    
    def test_with_helper_method(self):
        """
        ✅ BEST PRACTICE #4: Helper metodlardan foydalaning
        """
        book = self._create_test_book()
        self.assertIsNotNone(book)
    
    def _create_test_book(self, **kwargs):
        """
        Helper metod: Testlar uchun kitob yaratish
        
        Bu metodni turli testlarda qayta ishlatish mumkin
        """
        defaults = {
            'title': 'Default Title',
            'author': self.author,
            'category': self.category,
            'isbn': f'ISBN{id(self)}'
        }
        defaults.update(kwargs)
        return Book.objects.create(**defaults)
    
    def test_isolation(self):
        """
        ✅ BEST PRACTICE #5: Test izolatsiyasi
        
        Har bir test mustaqil bo'lishi kerak
        """
        # Bu test boshqa testlarga ta'sir qilmasligi kerak
        Book.objects.all().delete()
        self.assertEqual(Book.objects.count(), 0)


# =============================================================================
# 7. ANTI-PATTERNS - NIMA QILMASLIK KERAK
# =============================================================================

class AntiPatternsExample(APITestCase):
    """
    ❌ Nima qilmaslik kerak - Anti-patterns
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(
            title='Shared Book',
            author='Author',
            category=Category.objects.create(name='Cat'),
            isbn='1234567890123'
        )
    
    def test_anti_pattern_1_modifying_shared_data(self):
        """
        ❌ ANTI-PATTERN #1: setUpTestData'dagi ma'lumotni o'zgartirish
        
        Bu boshqa testlarga ta'sir qiladi!
        """
        # ❌ YOMON - shared data'ni o'zgartirish
        # self.book.title = 'Changed Title'
        # self.book.save()
        
        # ✅ YAXSHI - yangi obyekt yaratish
        new_book = Book.objects.create(
            title='New Book',
            author='Author',
            category=self.book.category,
            isbn='9999999999999'
        )
        new_book.title = 'Changed Title'
        new_book.save()
    
    def test_anti_pattern_2_depending_on_other_tests(self):
        """
        ❌ ANTI-PATTERN #2: Boshqa testlarga bog'liq bo'lish
        
        Testlar tartibsiz ishga tushishi mumkin!
        """
        # ❌ YOMON - oldingi test yaratgan ma'lumotga ishonch
        # book = Book.objects.get(title='Created in previous test')
        
        # ✅ YAXSHI - o'zingiz yaratish
        book = Book.objects.create(
            title='My Own Book',
            author='Author',
            category=self.book.category,
            isbn='8888888888888'
        )
        self.assertIsNotNone(book)


# =============================================================================
# XULOSA VA QOIDALAR
# =============================================================================

"""
FIXTURES - ASOSIY QOIDALAR:
===========================

1️⃣ setUpTestData():
   - Faqat READ-ONLY ma'lumotlar
   - Bir marta ishga tushadi
   - Tezroq testlar
   - @classmethod decorator kerak

2️⃣ setUp():
   - Har test uchun yangi ma'lumot
   - O'zgaradigan ma'lumotlar
   - Authentication setup
   - Har test oldidan ishga tushadi

3️⃣ tearDown():
   - Har test keyin cleanup
   - Temporary fayllar o'chirish
   - Cache tozalash

4️⃣ Fixtures fayllari:
   - JSON/YAML formatda
   - Qayta ishlatiladigan ma'lumotlar
   - fixtures = ['file.json'] bilan yuklash

5️⃣ Best Practices:
   ✅ Minimal kerakli ma'lumot
   ✅ Test izolatsiyasi
   ✅ Helper metodlar
   ✅ Aniq nomlar
   ✅ Shared data'ni o'zgartirmaslik

6️⃣ Anti-Patterns:
   ❌ Shared data'ni o'zgartirish
   ❌ Testlar orasida bog'liqlik
   ❌ Ortiqcha ma'lumot yaratish
   ❌ Global state'ga bog'liqlik


TESTLARNI ISHGA TUSHIRISH:
==========================
python manage.py test path.to.this.file --verbosity=2
"""