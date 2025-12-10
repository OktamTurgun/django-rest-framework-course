"""
Books Models Tests - REAL PROJECT
==================================

Book, Author, Genre modellarini test qilish
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from books.models import Book, Author, Genre
from decimal import Decimal
from datetime import date


class GenreModelTest(TestCase):
    """Genre model testlari"""
    
    def test_genre_creation(self):
        """Genre yaratish"""
        genre = Genre.objects.create(
            name='Fiction',
            description='Fiction books'
        )
        
        self.assertEqual(genre.name, 'Fiction')
        self.assertEqual(genre.description, 'Fiction books')
        self.assertIsNotNone(genre.id)
    
    def test_genre_str_method(self):
        """Genre __str__ metodi"""
        genre = Genre.objects.create(name='Science')
        self.assertEqual(str(genre), 'Science')
    
    def test_genre_name_unique(self):
        """Genre name unique bo'lishi"""
        Genre.objects.create(name='Fiction')
        
        # Duplicate genre yaratish
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Genre.objects.create(name='Fiction')


class AuthorModelTest(TestCase):
    """Author model testlari"""
    
    def test_author_creation(self):
        """Author yaratish"""
        author = Author.objects.create(
            name='John Doe',
            email='john@example.com',
            bio='Famous author',
            birth_date=date(1980, 1, 1)
        )
        
        self.assertEqual(author.name, 'John Doe')
        self.assertEqual(author.email, 'john@example.com')
        self.assertIsNotNone(author.id)
    
    def test_author_str_method(self):
        """Author __str__ metodi"""
        author = Author.objects.create(
            name='Jane Smith',
            email='jane@example.com',
            bio='Author bio',
            birth_date=date(1990, 5, 15)
        )
        self.assertEqual(str(author), 'Jane Smith')
    
    def test_author_email_unique(self):
        """Email unique bo'lishi"""
        Author.objects.create(
            name='Author 1',
            email='same@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        
        # Duplicate email
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Author.objects.create(
                name='Author 2',
                email='same@example.com',
                bio='Bio 2',
                birth_date=date(1985, 1, 1)
            )
    
    def test_author_books_relationship(self):
        """Author va Book orasidagi aloqa"""
        author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        
        genre = Genre.objects.create(name='Fiction')
        user = User.objects.create_user(username='testuser', password='pass123')
        
        # Author uchun 3 ta kitob yaratish
        for i in range(3):
            Book.objects.create(
                title=f'Book {i+1}',
                author=author,
                isbn_number=f'{i}1234567890{i}{i}',
                price=Decimal('10.00'),
                pages=100,
                publisher='Publisher',
                owner=user
            )
        
        # Author'ning kitoblari soni
        self.assertEqual(author.books.count(), 3)


class BookModelTest(TestCase):
    """Book model testlari"""
    
    def setUp(self):
        """Har test uchun kerakli ma'lumotlar"""
        self.genre = Genre.objects.create(name='Fiction')
        self.author = Author.objects.create(
            name='Test Author',
            email='author@example.com',
            bio='Author bio',
            birth_date=date(1980, 1, 1)
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
    
    def test_book_creation(self):
        """Kitob yaratish"""
        book = Book.objects.create(
            title='Test Book',
            subtitle='Test Subtitle',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('19.99'),
            pages=200,
            language='English',
            published_date=date(2024, 1, 1),
            publisher='Test Publisher',
            owner=self.user
        )
        
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.author, self.author)
        self.assertEqual(book.price, Decimal('19.99'))
        self.assertIsNotNone(book.id)
    
    def test_book_str_method(self):
        """Book __str__ metodi"""
        book = Book.objects.create(
            title='My Book',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('10.00'),
            pages=100,
            publisher='Publisher',
            owner=self.user
        )
        
        # "My Book by Test Author" formatda
        self.assertIn('My Book', str(book))
        self.assertIn('Test Author', str(book))
    
    def test_book_isbn_unique(self):
        """ISBN unique bo'lishi"""
        Book.objects.create(
            title='Book 1',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('10.00'),
            pages=100,
            publisher='Publisher',
            owner=self.user
        )
        
        # Duplicate ISBN
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title='Book 2',
                author=self.author,
                isbn_number='9781234567897',
                price=Decimal('10.00'),
                pages=100,
                publisher='Publisher',
                owner=self.user
            )
    
    def test_book_price_positive(self):
        """Narx musbat bo'lishi kerak"""
        book = Book(
            title='Test',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('-10.00'),  # Manfiy narx
            pages=100,
            publisher='Publisher',
            owner=self.user
        )
        
        with self.assertRaises(ValidationError):
            book.full_clean()
    
    def test_book_pages_positive(self):
        """Pages musbat bo'lishi"""
        book = Book(
            title='Test',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('10.00'),
            pages=-50,  # Manfiy sahifalar
            publisher='Publisher',
            owner=self.user
        )
        
        with self.assertRaises(ValidationError):
            book.full_clean()
    
    def test_book_default_values(self):
        """Default qiymatlar"""
        book = Book.objects.create(
            title='Test Book',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('10.00'),
            pages=100,
            publisher='Publisher',
            owner=self.user
        )
        
        # Default qiymatlar
        self.assertEqual(book.language, 'English')
        self.assertFalse(book.published)
        self.assertEqual(book.available_copies, 5)
        self.assertIsNotNone(book.created_at)
        self.assertIsNotNone(book.updated_at)
    
    def test_book_genres_relationship(self):
        """Book va Genre orasidagi ManyToMany aloqa"""
        book = Book.objects.create(
            title='Test',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('10.00'),
            pages=100,
            publisher='Publisher',
            owner=self.user
        )
        
        # Yangi noyob genre nomlari
        genre1 = Genre.objects.create(name='SciFi')
        genre2 = Genre.objects.create(name='Adventure')
        
        book.genres.add(genre1, genre2)
        
        # Tekshirish
        self.assertEqual(book.genres.count(), 2)
        self.assertIn(genre1, book.genres.all())
        self.assertIn(genre2, book.genres.all())
    
    def test_book_author_relationship(self):
        """Book va Author orasidagi ForeignKey aloqa"""
        book = Book.objects.create(
            title='Test',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('10.00'),
            pages=100,
            publisher='Publisher',
            owner=self.user
        )
        
        self.assertEqual(book.author.name, 'Test Author')
        self.assertIn(book, self.author.books.all())
    
    def test_book_owner_relationship(self):
        """Book'ni kim yaratgani"""
        book = Book.objects.create(
            title='Test',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('10.00'),
            pages=100,
            publisher='Publisher',
            owner=self.user
        )
        
        self.assertEqual(book.owner, self.user)
        self.assertEqual(book.owner.username, 'testuser')
    
    def test_book_timestamps(self):
        """created_at va updated_at"""
        book = Book.objects.create(
            title='Test',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('10.00'),
            pages=100,
            publisher='Publisher',
            owner=self.user
        )
        
        created_at = book.created_at
        
        # Update qilish
        book.title = 'Updated Title'
        book.save()
        book.refresh_from_db()
        
        # created_at o'zgarmaydi
        self.assertEqual(book.created_at, created_at)
        # updated_at o'zgaradi
        self.assertGreater(book.updated_at, created_at)


class BookAvailableCopiesTest(TestCase):
    """Book available_copies bilan bog'liq testlar"""
    
    def setUp(self):
        self.genre = Genre.objects.create(name='Fiction')
        self.author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        self.user = User.objects.create_user(username='test', password='pass')
    
    def test_default_available_copies(self):
        """Default available_copies = 5"""
        book = Book.objects.create(
            title='Test',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('10.00'),
            pages=100,
            publisher='Publisher',
            owner=self.user
        )
        
        self.assertEqual(book.available_copies, 5)
    
    def test_decrease_available_copies(self):
        """Available copies'ni kamaytirish"""
        book = Book.objects.create(
            title='Test',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('10.00'),
            pages=100,
            publisher='Publisher',
            owner=self.user,
            available_copies=10
        )
        
        # Kamaytirish
        book.available_copies -= 2
        book.save()
        book.refresh_from_db()
        
        self.assertEqual(book.available_copies, 8)
    
    def test_available_copies_cannot_be_negative(self):
        """Available copies manfiy bo'lmasligi"""
        book = Book(
            title='Test',
            author=self.author,
            isbn_number='9781234567897',
            price=Decimal('10.00'),
            pages=100,
            publisher='Publisher',
            owner=self.user,
            available_copies=-5
        )
        
        with self.assertRaises(ValidationError):
            book.full_clean()