"""
Lesson 23: Code Coverage - Test qamrovi o'lchash
================================================

Coverage - bu kodingizning qancha qismi testlar bilan qoplangani.

Nima uchun coverage muhim?
- Qaysi kod test qilinmaganini ko'rsatadi
- Code quality'ni yaxshilaydi
- Bug'larni kamaytirishga yordam beradi
- Confidence beradi

O'rnatish:
pip install coverage

Ishlatish:
coverage run --source='.' manage.py test
coverage report
coverage html
"""

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from books.models import Book, Author, Category
from decimal import Decimal


# =============================================================================
# 1. COVERAGE NIMA? - MISOL
# =============================================================================

class Calculator:
    """
    Oddiy calculator - coverage misolini ko'rsatish uchun
    """
    
    def add(self, a, b):
        """Qo'shish"""
        return a + b
    
    def subtract(self, a, b):
        """Ayirish"""
        return a - b
    
    def multiply(self, a, b):
        """Ko'paytirish"""
        return a * b
    
    def divide(self, a, b):
        """Bo'lish"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, a, b):
        """Darajaga ko'tarish"""
        return a ** b
    
    def modulo(self, a, b):
        """Qoldiqni topish"""
        if b == 0:
            raise ValueError("Cannot modulo by zero")
        return a % b


class CalculatorTestPartialCoverage(TestCase):
    """
    Qisman coverage - faqat ba'zi metodlar test qilingan
    
    Bu test faqat 3 ta metoddan 6 tasini test qiladi
    Coverage: ~50%
    """
    
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        """Add metodini test qilish"""
        result = self.calc.add(5, 3)
        self.assertEqual(result, 8)
    
    def test_subtract(self):
        """Subtract metodini test qilish"""
        result = self.calc.subtract(10, 4)
        self.assertEqual(result, 6)
    
    def test_multiply(self):
        """Multiply metodini test qilish"""
        result = self.calc.multiply(6, 7)
        self.assertEqual(result, 42)
    
    # ❌ divide, power, modulo metodlari test qilinmagan!


class CalculatorTestFullCoverage(TestCase):
    """
    To'liq coverage - barcha metodlar va edge case'lar test qilingan
    Coverage: 100%
    """
    
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        self.assertEqual(self.calc.add(5, 3), 8)
        self.assertEqual(self.calc.add(-5, 3), -2)
        self.assertEqual(self.calc.add(0, 0), 0)
    
    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 4), 6)
        self.assertEqual(self.calc.subtract(4, 10), -6)
        self.assertEqual(self.calc.subtract(0, 0), 0)
    
    def test_multiply(self):
        self.assertEqual(self.calc.multiply(6, 7), 42)
        self.assertEqual(self.calc.multiply(-6, 7), -42)
        self.assertEqual(self.calc.multiply(0, 7), 0)
    
    def test_divide(self):
        """Divide metodini test qilish"""
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(10, 3), 10/3)
    
    def test_divide_by_zero(self):
        """Divide by zero exception"""
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)
    
    def test_power(self):
        """Power metodini test qilish"""
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 0), 1)
    
    def test_modulo(self):
        """Modulo metodini test qilish"""
        self.assertEqual(self.calc.modulo(10, 3), 1)
        self.assertEqual(self.calc.modulo(10, 5), 0)
    
    def test_modulo_by_zero(self):
        """Modulo by zero exception"""
        with self.assertRaises(ValueError):
            self.calc.modulo(10, 0)


# =============================================================================
# 2. COVERAGE HISOBOTINI O'QISH
# =============================================================================

"""
COVERAGE HISOBOTI:
==================

Terminal'da ishga tushirish:
----------------------------
# 1. Coverage bilan testni ishga tushirish
coverage run --source='.' manage.py test books

# 2. Terminal'da hisobot ko'rish
coverage report

# 3. Qaysi qatorlar test qilinmaganini ko'rish
coverage report -m

# 4. HTML hisobot yaratish
coverage html

# 5. HTML hisobotni ochish (brauzerda)
# htmlcov/index.html faylini oching


MISOL HISOBOT:
--------------
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
books/__init__.py            0      0   100%
books/models.py            50     10    80%   45-54
books/views.py             75     15    80%   89-103
books/serializers.py       30      5    83%   25-29
books/tests/test_models.py 40      0   100%
-------------------------------------------------------
TOTAL                     195     30    85%


Tushuntirish:
-------------
- Stmts: Umumiy kod qatorlari
- Miss: Test qilinmagan qatorlar
- Cover: Coverage foizi
- Missing: Qaysi qatorlar test qilinmagan

YAXSHI COVERAGE:
- 80%+ - Yaxshi
- 90%+ - Juda yaxshi
- 100% - Ideal (lekin shart emas)
"""


# =============================================================================
# 3. COVERAGE YAXSHILASH - STRATEGIYALAR
# =============================================================================

class BookService:
    """
    Book service - turli xil metodlar bilan
    Coverage'ni yaxshilash strategiyalarini ko'rsatish uchun
    """
    
    @staticmethod
    def create_book(title, author, isbn, category):
        """Kitob yaratish"""
        if not title:
            raise ValueError("Title is required")
        if not isbn or len(isbn) != 13:
            raise ValueError("ISBN must be 13 characters")
        
        book = Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            category=category
        )
        return book
    
    @staticmethod
    def get_books_by_category(category_name):
        """Category bo'yicha kitoblarni olish"""
        try:
            category = Category.objects.get(name=category_name)
            return Book.objects.filter(category=category)
        except Category.DoesNotExist:
            return Book.objects.none()
    
    @staticmethod
    def update_book_price(book_id, new_price):
        """Kitob narxini yangilash"""
        try:
            book = Book.objects.get(id=book_id)
            if new_price < 0:
                raise ValueError("Price cannot be negative")
            book.price = new_price
            book.save()
            return book
        except Book.DoesNotExist:
            return None
    
    @staticmethod
    def delete_old_books(years=10):
        """Eski kitoblarni o'chirish"""
        from datetime import datetime, timedelta
        cutoff_date = datetime.now() - timedelta(days=years*365)
        old_books = Book.objects.filter(published_date__lt=cutoff_date)
        count = old_books.count()
        old_books.delete()
        return count
    
    @staticmethod
    def search_books(query):
        """Kitoblarni qidirish"""
        if not query:
            return Book.objects.all()
        
        return Book.objects.filter(
            title__icontains=query
        ) | Book.objects.filter(
            author__icontains=query
        )


class BookServiceTestLowCoverage(APITestCase):
    """
    PAST COVERAGE - faqat asosiy holatlar test qilingan
    Coverage: ~40%
    """
    
    def test_create_book(self):
        """Faqat muvaffaqiyatli holatni test qilish"""
        category = Category.objects.create(name='Test')
        book = BookService.create_book(
            title='Test Book',
            author='Test Author',
            isbn='1234567890123',
            category=category
        )
        self.assertIsNotNone(book)
    
    # ❌ Error case'lar test qilinmagan
    # ❌ Edge case'lar test qilinmagan
    # ❌ Boshqa metodlar test qilinmagan


class BookServiceTestHighCoverage(APITestCase):
    """
    YUQORI COVERAGE - barcha holatlar test qilingan
    Coverage: ~95%
    """
    
    def setUp(self):
        self.category = Category.objects.create(name='Fiction')
    
    # create_book metodining barcha holatlarini test qilish
    def test_create_book_success(self):
        """Muvaffaqiyatli yaratish"""
        book = BookService.create_book(
            title='Test Book',
            author='Author',
            isbn='1234567890123',
            category=self.category
        )
        self.assertIsNotNone(book.id)
    
    def test_create_book_without_title(self):
        """Title bo'lmasa"""
        with self.assertRaises(ValueError) as cm:
            BookService.create_book('', 'Author', '1234567890123', self.category)
        self.assertIn('Title is required', str(cm.exception))
    
    def test_create_book_invalid_isbn(self):
        """Noto'g'ri ISBN"""
        with self.assertRaises(ValueError) as cm:
            BookService.create_book('Title', 'Author', '123', self.category)
        self.assertIn('ISBN must be 13 characters', str(cm.exception))
    
    # get_books_by_category metodini test qilish
    def test_get_books_by_category_found(self):
        """Category topilgan holat"""
        Book.objects.create(
            title='Book',
            author='Author',
            isbn='1234567890123',
            category=self.category
        )
        books = BookService.get_books_by_category('Fiction')
        self.assertEqual(books.count(), 1)
    
    def test_get_books_by_category_not_found(self):
        """Category topilmagan holat"""
        books = BookService.get_books_by_category('NonExistent')
        self.assertEqual(books.count(), 0)
    
    # update_book_price metodini test qilish
    def test_update_book_price_success(self):
        """Narxni yangilash"""
        book = Book.objects.create(
            title='Book',
            author='Author',
            isbn='1234567890123',
            category=self.category,
            price=Decimal('10.00')
        )
        updated = BookService.update_book_price(book.id, Decimal('20.00'))
        self.assertEqual(updated.price, Decimal('20.00'))
    
    def test_update_book_price_negative(self):
        """Manfiy narx"""
        book = Book.objects.create(
            title='Book',
            author='Author',
            isbn='1234567890123',
            category=self.category
        )
        with self.assertRaises(ValueError):
            BookService.update_book_price(book.id, Decimal('-10.00'))
    
    def test_update_book_price_not_found(self):
        """Kitob topilmagan"""
        result = BookService.update_book_price(9999, Decimal('10.00'))
        self.assertIsNone(result)
    
    # delete_old_books metodini test qilish
    def test_delete_old_books(self):
        """Eski kitoblarni o'chirish"""
        from datetime import datetime, timedelta
        
        # Eski kitob
        old_date = datetime.now() - timedelta(days=11*365)
        Book.objects.create(
            title='Old Book',
            author='Author',
            isbn='1111111111111',
            category=self.category,
            published_date=old_date
        )
        
        # Yangi kitob
        Book.objects.create(
            title='New Book',
            author='Author',
            isbn='2222222222222',
            category=self.category,
            published_date=datetime.now()
        )
        
        count = BookService.delete_old_books(years=10)
        self.assertEqual(count, 1)
        self.assertEqual(Book.objects.count(), 1)
    
    # search_books metodini test qilish
    def test_search_books_by_title(self):
        """Title bo'yicha qidirish"""
        Book.objects.create(
            title='Python Programming',
            author='Author',
            isbn='1111111111111',
            category=self.category
        )
        results = BookService.search_books('Python')
        self.assertEqual(results.count(), 1)
    
    def test_search_books_by_author(self):
        """Author bo'yicha qidirish"""
        Book.objects.create(
            title='Book',
            author='John Smith',
            isbn='1111111111111',
            category=self.category
        )
        results = BookService.search_books('John')
        self.assertEqual(results.count(), 1)
    
    def test_search_books_empty_query(self):
        """Bo'sh query"""
        Book.objects.create(
            title='Book1',
            author='Author',
            isbn='1111111111111',
            category=self.category
        )
        results = BookService.search_books('')
        self.assertGreater(results.count(), 0)


# =============================================================================
# 4. COVERAGE CONFIGURATION - .coveragerc
# =============================================================================

"""
.coveragerc FAYLI:
==================

Loyihangiz root papkasida .coveragerc fayli yarating:

[run]
source = .
omit =
    */migrations/*
    */tests/*
    */test_*.py
    */__init__.py
    */venv/*
    */virtualenv/*
    */settings.py
    */manage.py
    */wsgi.py
    */asgi.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    def __str__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod

[html]
directory = htmlcov


Tushuntirish:
-------------
- source: Qaysi papkalarni tekshirish
- omit: Qaysi fayllarni o'tkazib yuborish
- exclude_lines: Qaysi qatorlarni hisobga olmaslik
- directory: HTML hisobot papkasi
"""


# =============================================================================
# 5. COVERAGE BEST PRACTICES
# =============================================================================

"""
COVERAGE BEST PRACTICES:
========================

1️⃣ Maqsad qo'ying:
   ✅ 80%+ - Minimal maqsad
   ✅ 90%+ - Yaxshi maqsad
   ✅ 100% - Ideal (lekin har doim ham kerak emas)

2️⃣ Muhim qismlarni birinchi test qiling:
   ✅ Business logic
   ✅ API endpoints
   ✅ Data validation
   ✅ Error handling
   ✅ Security-critical code

3️⃣ Coverage'ga ishonib qolmang:
   ❌ 100% coverage = bug yo'q degani EMAS
   ✅ Coverage - bu faqat kod bajarilganini ko'rsatadi
   ✅ Logic to'g'riligini test qilish muhim

4️⃣ Edge case'larni test qiling:
   ✅ Null/empty values
   ✅ Boundary values
   ✅ Error conditions
   ✅ Invalid input

5️⃣ Coverage'ni CI/CD'ga qo'shing:
   ✅ Har commit'da coverage hisoblang
   ✅ Coverage pasaysa, warning bering
   ✅ Minimal coverage talab qiling

6️⃣ Keraksiz code'ni ignore qiling:
   ✅ Migration fayllar
   ✅ Test fayllar
   ✅ Settings
   ✅ __init__.py fayllar

7️⃣ HTML hisobotdan foydalaning:
   ✅ Qaysi qatorlar test qilinmaganini ko'ring
   ✅ Qizil rangdagi qatorlarni test qiling
   ✅ Branch coverage'ni tekshiring


COVERAGE METRICS:
=================

Line Coverage:
- Necha qator kod bajarilgan?
- Eng oddiy metric

Branch Coverage:
- Barcha if/else shoxlari test qilinganmi?
- Muhimroq metric

Function Coverage:
- Barcha funksiyalar chaqirilganmi?

Statement Coverage:
- Barcha statement'lar bajarilganmi?


COVERAGE ISHLATISH:
===================

# 1. Coverage bilan test
coverage run --source='.' manage.py test

# 2. Terminal hisobot
coverage report

# 3. Missing lines bilan
coverage report -m

# 4. HTML hisobot
coverage html

# 5. Specific app
coverage run --source='books' manage.py test books

# 6. XML hisobot (CI/CD uchun)
coverage xml

# 7. Coverage ma'lumotlarini o'chirish
coverage erase


PYTEST BILAN:
=============

# O'rnatish
pip install pytest pytest-cov pytest-django

# Pytest bilan coverage
pytest --cov=books

# HTML hisobot
pytest --cov=books --cov-report=html

# Terminal va HTML
pytest --cov=books --cov-report=term --cov-report=html

# Missing lines ko'rsatish
pytest --cov=books --cov-report=term-missing
"""


# =============================================================================
# AMALIY MASHQ
# =============================================================================

"""
MASHQ: O'z loyihangiz uchun coverage tekshiring
================================================

1. Coverage o'rnating:
   pip install coverage

2. .coveragerc fayli yarating (yuqoridagi config)

3. Coverage hisoblang:
   coverage run --source='.' manage.py test

4. Hisobotni ko'ring:
   coverage report -m

5. HTML hisobot yarating:
   coverage html

6. htmlcov/index.html ni brauzerda oching

7. Qizil qatorlarni topib, testlar yozing

8. Coverage'ni 80%+ ga yetkazing


NATIJANI TAHLIL QILISH:
=======================

Coverage < 50%:
❌ Juda kam test
❌ Xavfli kod
→ Urgent: Ko'proq test yozing

Coverage 50-70%:
⚠️  Yetarli emas
⚠️  Muhim qismlar test qilinmagan bo'lishi mumkin
→ Test qo'shing

Coverage 70-80%:
✅ Yaxshi boshlandi
✅ Asosiy funksiyalar qoplangan
→ Edge case'larni qo'shing

Coverage 80-90%:
✅✅ Juda yaxshi
✅✅ Ishonchli kod
→ Qolgan qismlarni ham test qiling

Coverage 90%+:
✅✅✅ A'lo!
✅✅✅ Production-ready
→ Maintain qiling
"""