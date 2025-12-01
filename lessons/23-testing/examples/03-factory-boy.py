"""
Lesson 23: Factory Boy - Professional Test Data Generation
===========================================================

Factory Boy - bu test ma'lumotlarini yaratish uchun qulaylik kutubxonasi.

Nima uchun Factory Boy?
- Test ma'lumotlarini oson yaratish
- Faker bilan integratsiya (fake data)
- Bog'langan obyektlarni avtomatik yaratish
- Qayta ishlatiladigan factory'lar
- Turli variantlar (traits)

O'rnatish:
pip install factory-boy faker
"""

import factory
from factory.django import DjangoModelFactory
from factory import Faker, SubFactory, post_generation, LazyAttribute
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from books.models import Book, Author, Category, Review
from decimal import Decimal
from datetime import datetime, timedelta
import random


# =============================================================================
# 1. ODDIY FACTORY - BASIC USAGE
# =============================================================================

class CategoryFactory(DjangoModelFactory):
    """
    Category modeli uchun Factory
    
    DjangoModelFactory - Django modellari uchun maxsus Factory
    """
    
    class Meta:
        model = Category
    
    # Oddiy qiymatlar
    name = "Fiction"
    description = "Fiction books category"
    
    # Faker'dan foydalanish
    # name = Faker('word')  # Random so'z
    # description = Faker('sentence')  # Random gap


class AuthorFactory(DjangoModelFactory):
    """
    Author modeli uchun Factory
    """
    
    class Meta:
        model = Author
    
    # Faker providers
    name = Faker('name')  # Random ism: "John Smith"
    email = Faker('email')  # Random email: "john@example.com"
    bio = Faker('text', max_nb_chars=200)  # Random text
    
    # Date
    birth_date = Faker('date_of_birth', minimum_age=25, maximum_age=80)


class BookFactory(DjangoModelFactory):
    """
    Book modeli uchun Factory
    """
    
    class Meta:
        model = Book
    
    # Faker'dan turli ma'lumotlar
    title = Faker('sentence', nb_words=3)  # "Great Book Title"
    isbn = Faker('isbn13')  # "978-0-12-345678-9"
    published_date = Faker('date_between', start_date='-10y', end_date='today')
    pages = Faker('random_int', min=50, max=1000)
    language = 'English'
    description = Faker('paragraph')
    
    # SubFactory - bog'langan obyektlarni avtomatik yaratish
    author = SubFactory(AuthorFactory)
    category = SubFactory(CategoryFactory)
    
    # LazyAttribute - dinamik qiymatlar
    price = LazyAttribute(lambda obj: Decimal(f'{random.randint(10, 100)}.99'))


class UserFactory(DjangoModelFactory):
    """
    User modeli uchun Factory
    """
    
    class Meta:
        model = User
    
    username = Faker('user_name')
    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    
    # post_generation - obyekt yaratilgandan keyin
    @post_generation
    def password(obj, create, extracted, **kwargs):
        """Password'ni hash qilish"""
        if create:
            obj.set_password(extracted or 'defaultpass123')


# =============================================================================
# 2. FACTORY BOY BILAN TESTLAR
# =============================================================================

class FactoryBoyBasicTest(APITestCase):
    """
    Factory Boy'dan foydalangan holda oddiy testlar
    """
    
    def test_create_single_book(self):
        """Bitta kitob yaratish"""
        # Factory.create() - database'ga saqlaydi
        book = BookFactory.create()
        
        # Tekshirish
        self.assertIsNotNone(book.id)
        self.assertIsNotNone(book.title)
        self.assertIsNotNone(book.author)
        self.assertIsNotNone(book.category)
        
        print(f"✅ Yaratildi: {book.title}")
        print(f"   Author: {book.author.name}")
        print(f"   Category: {book.category.name}")
    
    def test_create_multiple_books(self):
        """Bir nechta kitob yaratish"""
        # 5 ta kitob yaratish
        books = BookFactory.create_batch(5)
        
        # Tekshirish
        self.assertEqual(len(books), 5)
        self.assertEqual(Book.objects.count(), 5)
        
        for book in books:
            print(f"📚 {book.title} by {book.author.name}")
    
    def test_create_book_with_custom_data(self):
        """Custom ma'lumotlar bilan kitob yaratish"""
        book = BookFactory.create(
            title='My Custom Book',
            pages=500,
            language='Uzbek'
        )
        
        self.assertEqual(book.title, 'My Custom Book')
        self.assertEqual(book.pages, 500)
        self.assertEqual(book.language, 'Uzbek')
    
    def test_build_without_saving(self):
        """Database'ga saqlamasdan obyekt yaratish"""
        # Factory.build() - faqat obyekt, database'ga saqlamaydi
        book = BookFactory.build()
        
        self.assertIsNone(book.id)  # ID yo'q (saqlanmagan)
        self.assertIsNotNone(book.title)  # Lekin ma'lumotlar bor
        
        # Agar kerak bo'lsa, qo'lda saqlash mumkin
        book.save()
        self.assertIsNotNone(book.id)


# =============================================================================
# 3. SubFactory - BOG'LANGAN OBYEKTLAR
# =============================================================================

class ReviewFactory(DjangoModelFactory):
    """
    Review modeli uchun Factory
    SubFactory bilan user va book yaratadi
    """
    
    class Meta:
        model = Review
    
    book = SubFactory(BookFactory)
    user = SubFactory(UserFactory)
    rating = Faker('random_int', min=1, max=5)
    comment = Faker('paragraph')
    created_at = Faker('date_time_between', start_date='-30d', end_date='now')


class SubFactoryTest(APITestCase):
    """
    SubFactory bilan bog'langan obyektlarni yaratish
    """
    
    def test_create_review_creates_user_and_book(self):
        """
        Review yaratilganda avtomatik user va book ham yaratiladi
        """
        review = ReviewFactory.create()
        
        # Hammasi yaratilganini tekshirish
        self.assertIsNotNone(review.id)
        self.assertIsNotNone(review.user.id)
        self.assertIsNotNone(review.book.id)
        self.assertIsNotNone(review.book.author.id)
        self.assertIsNotNone(review.book.category.id)
        
        print(f"📝 Review by {review.user.username}")
        print(f"   Book: {review.book.title}")
        print(f"   Rating: {review.rating}/5")
    
    def test_create_review_with_existing_book(self):
        """
        Mavjud kitob bilan review yaratish
        """
        # Avval kitob yaratamiz
        book = BookFactory.create(title='Existing Book')
        
        # Review'ni shu kitob bilan yaratamiz
        review = ReviewFactory.create(book=book)
        
        self.assertEqual(review.book.title, 'Existing Book')
        self.assertEqual(review.book.id, book.id)


# =============================================================================
# 4. SEQUENCE - KETMA-KET QIYMATLAR
# =============================================================================

class SequenceExampleFactory(DjangoModelFactory):
    """
    Sequence - ketma-ket raqamlar uchun
    """
    
    class Meta:
        model = Book
    
    title = factory.Sequence(lambda n: f'Book {n}')
    isbn = factory.Sequence(lambda n: f'ISBN-{n:013d}')
    author = SubFactory(AuthorFactory)
    category = SubFactory(CategoryFactory)


class SequenceTest(APITestCase):
    """Sequence bilan testlar"""
    
    def test_create_books_with_sequence(self):
        """Sequence bilan kitoblar yaratish"""
        books = SequenceExampleFactory.create_batch(3)
        
        self.assertEqual(books[0].title, 'Book 0')
        self.assertEqual(books[1].title, 'Book 1')
        self.assertEqual(books[2].title, 'Book 2')
        
        for book in books:
            print(f"📖 {book.title} - {book.isbn}")


# =============================================================================
# 5. TRAITS - TURLI VARIANTLAR
# =============================================================================

class BookWithTraitsFactory(DjangoModelFactory):
    """
    Traits - turli xil book variantlari
    """
    
    class Meta:
        model = Book
    
    title = Faker('sentence', nb_words=3)
    author = SubFactory(AuthorFactory)
    category = SubFactory(CategoryFactory)
    isbn = Faker('isbn13')
    
    class Params:
        # Trait parametrlari
        is_bestseller = factory.Trait(
            price=Decimal('29.99'),
            pages=factory.Faker('random_int', min=400, max=800),
        )
        
        is_new_release = factory.Trait(
            published_date=factory.LazyFunction(datetime.now),
            price=Decimal('24.99'),
        )
        
        is_classic = factory.Trait(
            published_date=factory.Faker('date_between', start_date='-100y', end_date='-50y'),
            pages=factory.Faker('random_int', min=200, max=400),
        )


class TraitsTest(APITestCase):
    """Traits bilan testlar"""
    
    def test_create_bestseller_book(self):
        """Bestseller kitob yaratish"""
        book = BookWithTraitsFactory.create(is_bestseller=True)
        
        self.assertEqual(book.price, Decimal('29.99'))
        self.assertGreaterEqual(book.pages, 400)
        
        print(f"🔥 Bestseller: {book.title}")
        print(f"   Price: ${book.price}")
        print(f"   Pages: {book.pages}")
    
    def test_create_new_release(self):
        """Yangi kitob yaratish"""
        book = BookWithTraitsFactory.create(is_new_release=True)
        
        self.assertEqual(book.price, Decimal('24.99'))
        # Bugungi sana bilan
        self.assertEqual(book.published_date.date(), datetime.now().date())
        
        print(f"🆕 New Release: {book.title}")
    
    def test_create_classic_book(self):
        """Klassik kitob yaratish"""
        book = BookWithTraitsFactory.create(is_classic=True)
        
        # 50 yildan eski
        fifty_years_ago = datetime.now() - timedelta(days=365*50)
        self.assertLess(book.published_date.date(), fifty_years_ago.date())
        
        print(f"📜 Classic: {book.title}")
        print(f"   Published: {book.published_date.year}")


# =============================================================================
# 6. POST_GENERATION - YARATILGANDAN KEYIN
# =============================================================================

class AuthorWithBooksFactory(DjangoModelFactory):
    """
    Author yaratish va unga kitoblar qo'shish
    """
    
    class Meta:
        model = Author
    
    name = Faker('name')
    email = Faker('email')
    bio = Faker('text')
    
    @post_generation
    def books(self, create, extracted, **kwargs):
        """
        Author yaratilgandan keyin kitoblar qo'shish
        
        Usage:
        author = AuthorWithBooksFactory.create(books=3)  # 3 ta kitob bilan
        """
        if not create:
            return
        
        if extracted:
            # Agar son berilgan bo'lsa
            for _ in range(extracted):
                BookFactory.create(author=self)


class PostGenerationTest(APITestCase):
    """post_generation bilan testlar"""
    
    def test_create_author_with_books(self):
        """Author va uning kitoblari"""
        # 5 ta kitob bilan author yaratish
        author = AuthorWithBooksFactory.create(books=5)
        
        self.assertEqual(author.books.count(), 5)
        
        print(f"✍️  Author: {author.name}")
        print(f"   Books: {author.books.count()}")
        for book in author.books.all():
            print(f"   📚 {book.title}")


# =============================================================================
# 7. LAZY ATTRIBUTES - DINAMIK QIYMATLAR
# =============================================================================

class BookWithLazyAttributesFactory(DjangoModelFactory):
    """
    LazyAttribute - boshqa fieldlarga bog'liq qiymatlar
    """
    
    class Meta:
        model = Book
    
    title = Faker('sentence', nb_words=3)
    author = SubFactory(AuthorFactory)
    category = SubFactory(CategoryFactory)
    
    # ISBN kitob nomiga asoslangan
    isbn = LazyAttribute(
        lambda obj: f"ISBN-{hash(obj.title) % 10000000000000}"
    )
    
    # Price categoryga bog'liq
    price = LazyAttribute(
        lambda obj: Decimal('19.99') if obj.category.name == 'Fiction' 
                    else Decimal('29.99')
    )
    
    # LazyFunction - funksiya chaqirish
    published_date = factory.LazyFunction(datetime.now)


class LazyAttributesTest(APITestCase):
    """LazyAttribute bilan testlar"""
    
    def test_isbn_based_on_title(self):
        """ISBN title'ga bog'liq"""
        book1 = BookWithLazyAttributesFactory.create(title='Same Title')
        book2 = BookWithLazyAttributesFactory.create(title='Same Title')
        
        # Bir xil title - bir xil ISBN
        self.assertEqual(book1.isbn, book2.isbn)
    
    def test_price_based_on_category(self):
        """Price category'ga bog'liq"""
        fiction_cat = CategoryFactory.create(name='Fiction')
        science_cat = CategoryFactory.create(name='Science')
        
        fiction_book = BookWithLazyAttributesFactory.create(category=fiction_cat)
        science_book = BookWithLazyAttributesFactory.create(category=science_cat)
        
        self.assertEqual(fiction_book.price, Decimal('19.99'))
        self.assertEqual(science_book.price, Decimal('29.99'))


# =============================================================================
# 8. REAL-WORLD EXAMPLE - TO'LIQ MISOL
# =============================================================================

class CompleteBookstoreFactory:
    """
    To'liq bookstore uchun ma'lumotlar yaratish
    """
    
    @staticmethod
    def create_bookstore_data():
        """
        To'liq bookstore ma'lumotlari:
        - 10 ta author
        - 5 ta category
        - Har author uchun 3 ta kitob
        - Har kitob uchun 5 ta review
        """
        # Categories
        categories = CategoryFactory.create_batch(5)
        
        # Authors with books
        authors = []
        for _ in range(10):
            author = AuthorWithBooksFactory.create(books=3)
            authors.append(author)
        
        # Reviews for each book
        all_books = Book.objects.all()
        for book in all_books:
            ReviewFactory.create_batch(5, book=book)
        
        return {
            'categories': categories,
            'authors': authors,
            'books': all_books,
            'reviews': Review.objects.all()
        }


class RealWorldTest(APITestCase):
    """Real-world scenario test"""
    
    def test_complete_bookstore(self):
        """To'liq bookstore test"""
        # Ma'lumotlarni yaratish
        data = CompleteBookstoreFactory.create_bookstore_data()
        
        # Tekshirish
        self.assertEqual(Category.objects.count(), 5)
        self.assertEqual(Author.objects.count(), 10)
        self.assertEqual(Book.objects.count(), 30)  # 10 * 3
        self.assertEqual(Review.objects.count(), 150)  # 30 * 5
        
        print("\n📊 Bookstore Statistics:")
        print(f"   Categories: {Category.objects.count()}")
        print(f"   Authors: {Author.objects.count()}")
        print(f"   Books: {Book.objects.count()}")
        print(f"   Reviews: {Review.objects.count()}")


# =============================================================================
# 9. FAKER PROVIDERS - FAKE DATA TURLARI
# =============================================================================

class FakerProvidersExample(APITestCase):
    """
    Faker'ning turli providers'lari
    """
    
    def test_faker_text_providers(self):
        """Text providers"""
        print("\n📝 Text Providers:")
        print(f"Word: {Faker('word').generate()}")
        print(f"Sentence: {Faker('sentence').generate()}")
        print(f"Paragraph: {Faker('paragraph').generate()}")
        print(f"Text: {Faker('text', max_nb_chars=100).generate()}")
    
    def test_faker_person_providers(self):
        """Person providers"""
        print("\n👤 Person Providers:")
        print(f"Name: {Faker('name').generate()}")
        print(f"First Name: {Faker('first_name').generate()}")
        print(f"Last Name: {Faker('last_name').generate()}")
        print(f"Email: {Faker('email').generate()}")
        print(f"Username: {Faker('user_name').generate()}")
    
    def test_faker_number_providers(self):
        """Number providers"""
        print("\n🔢 Number Providers:")
        print(f"Random Int: {Faker('random_int', min=1, max=100).generate()}")
        print(f"Random Digit: {Faker('random_digit').generate()}")
        print(f"Pyint: {Faker('pyint').generate()}")
    
    def test_faker_date_providers(self):
        """Date providers"""
        print("\n📅 Date Providers:")
        print(f"Date: {Faker('date').generate()}")
        print(f"Date Time: {Faker('date_time').generate()}")
        print(f"Date of Birth: {Faker('date_of_birth').generate()}")
        print(f"Future Date: {Faker('future_date').generate()}")
        print(f"Past Date: {Faker('past_date').generate()}")


# =============================================================================
# XULOSA VA BEST PRACTICES
# =============================================================================

"""
FACTORY BOY - ASOSIY TUSHUNCHALAR:
===================================

1️⃣ Factory yaratish:
   class MyModelFactory(DjangoModelFactory):
       class Meta:
           model = MyModel
       
       field1 = "value"
       field2 = Faker('provider')

2️⃣ Factory'dan foydalanish:
   obj = MyModelFactory.create()        # Database'ga saqlash
   obj = MyModelFactory.build()         # Faqat obyekt
   objs = MyModelFactory.create_batch(5)  # 5 ta yaratish

3️⃣ SubFactory:
   author = SubFactory(AuthorFactory)  # Avtomatik yaratadi

4️⃣ Traits:
   class Params:
       is_special = factory.Trait(field="value")
   
   obj = MyFactory.create(is_special=True)

5️⃣ Sequence:
   field = factory.Sequence(lambda n: f'value-{n}')

6️⃣ LazyAttribute:
   field = LazyAttribute(lambda obj: f'{obj.other_field}-suffix')

7️⃣ post_generation:
   @post_generation
   def method(self, create, extracted, **kwargs):
       # Obyekt yaratilgandan keyin

8️⃣ Faker providers:
   - name, email, username
   - sentence, paragraph, text
   - date, date_time
   - random_int, random_digit
   - isbn, url, address


BEST PRACTICES:
===============
✅ Har model uchun Factory yarating
✅ Faker'dan maksimal foydalaning
✅ SubFactory bog'langan obyektlar uchun
✅ Traits turli variantlar uchun
✅ Factory'larni alohida faylda saqlang (factories.py)
✅ Minimal kerakli ma'lumot yarating


O'RNATISH:
==========
pip install factory-boy faker


ISHLATISH:
==========
python manage.py test path.to.this.file --verbosity=2
"""