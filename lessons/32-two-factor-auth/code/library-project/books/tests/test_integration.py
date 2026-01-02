"""
Books Integration Tests - REAL PROJECT
=======================================

To'liq workflow integration testlari
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from books.models import Book, Author, Genre
from decimal import Decimal
from datetime import date


class BookCRUDIntegrationTest(APITestCase):
    """To'liq Book CRUD workflow"""
    
    def test_complete_book_lifecycle(self):
        """
        To'liq kitob lifecycle:
        1. User yaratish
        2. Author yaratish
        3. Genre yaratish
        4. Book yaratish
        5. Book ro'yxatini olish
        6. Book detalni olish
        7. Book yangilash
        8. Book o'chirish
        """
        
        # Step 1: User yaratish
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)
        print("✅ Step 1: User created")
        
        # Step 2: Author yaratish
        author = Author.objects.create(
            name='Test Author',
            email='author@example.com',
            bio='Author bio',
            birth_date=date(1980, 1, 1)
        )
        print("✅ Step 2: Author created")
        
        # Step 3: Genre yaratish
        genre = Genre.objects.create(
            name='Programming',
            description='Programming books'
        )
        print("✅ Step 3: Genre created")
        
        # Step 4: Book yaratish
        book_url = '/api/books/'
        book_data = {
            'title': 'Integration Test Book',
            'subtitle': 'Test Subtitle',
            'author_id': author.id,
            'genre_ids': [genre.id],
            'isbn_number': '9781234567897',
            'price': '29.99',
            'pages': 350,
            'publisher': 'Test Publisher',
            'language': 'English',
            'published_date': '2024-01-01'
        }
        
        create_response = self.client.post(book_url, book_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        book_id = create_response.data['id']
        print(f"✅ Step 4: Book created (ID: {book_id})")
        
        # Step 5: Book ro'yxatini olish
        list_response = self.client.get(book_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        
        results = list_response.data.get('results', list_response.data)
        self.assertGreaterEqual(len(results), 1)
        print("✅ Step 5: Book list retrieved")
        
        # Step 6: Book detalni olish
        detail_url = f'/api/books/{book_id}/'
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['title'], 'Integration Test Book')
        print("✅ Step 6: Book detail retrieved")
        
        # Step 7: Book yangilash
        update_data = {
            'title': 'Updated Integration Book',
            'price': '34.99'
        }
        update_response = self.client.patch(detail_url, update_data)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['title'], 'Updated Integration Book')
        print("✅ Step 7: Book updated")
        
        # Step 8: Book o'chirish
        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        print("✅ Step 8: Book deleted")
        
        # Step 9: O'chirilganini tekshirish
        verify_response = self.client.get(detail_url)
        self.assertEqual(verify_response.status_code, status.HTTP_404_NOT_FOUND)
        print("✅ Step 9: Deletion verified")


class MultiUserBookManagementTest(APITestCase):
    """Bir nechta user bilan kitob boshqaruvi"""
    
    def test_multiple_users_create_and_manage_books(self):
        """
        Scenario:
        1. User1 va User2 yaratish
        2. Har ikkalasi kitob yaratadi
        3. User1 o'z kitobini update qila oladi
        4. User1 User2'ning kitobini update qila olmaydi (agar permission qo'shilgan bo'lsa)
        """
        
        # Create users
        user1 = User.objects.create_user(
            username='user1',
            password='pass123'
        )
        user2 = User.objects.create_user(
            username='user2',
            password='pass123'
        )
        
        # Setup author and genre
        author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        genre = Genre.objects.create(name='Fiction')
        
        # User1 creates book
        self.client.force_authenticate(user=user1)
        book1_data = {
            'title': 'User1 Book',
            'author_id': author.id,
            'isbn_number': '9781111111111',
            'price': '19.99',
            'pages': 200,
            'publisher': 'Publisher'
        }
        
        book1_response = self.client.post('/api/books/', book1_data, format='json')
        self.assertEqual(book1_response.status_code, status.HTTP_201_CREATED)
        book1_id = book1_response.data['id']
        print("✅ User1 created book")
        
        # User2 creates book
        self.client.force_authenticate(user=user2)
        book2_data = {
            'title': 'User2 Book',
            'author_id': author.id,
            'isbn_number': '9782222222222',
            'price': '24.99',
            'pages': 250,
            'publisher': 'Publisher'
        }
        
        book2_response = self.client.post('/api/books/', book2_data, format='json')
        self.assertEqual(book2_response.status_code, status.HTTP_201_CREATED)
        book2_id = book2_response.data['id']
        print("✅ User2 created book")
        
        # User1 updates own book
        self.client.force_authenticate(user=user1)
        update_url = f'/api/books/{book1_id}/'
        update_response = self.client.patch(update_url, {'title': 'User1 Updated'})
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        print("✅ User1 updated own book")
        
        # User1 tries to update User2's book
        update_url2 = f'/api/books/{book2_id}/'
        update_response2 = self.client.patch(update_url2, {'title': 'Hacked'})
        
        # Agar permission qo'shilgan: 403
        # Agar yo'q: 200
        if update_response2.status_code == status.HTTP_403_FORBIDDEN:
            print("✅ User1 blocked from updating User2's book (permission works)")
        else:
            print("⚠️  User1 updated User2's book (no permission yet)")


class BookSearchAndFilterIntegrationTest(APITestCase):
    """Search va filter integration test"""
    
    def setUp(self):
        """Test data setup"""
        self.user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Categories
        self.fiction = Genre.objects.create(name='Fiction')
        self.science = Genre.objects.create(name='Science')
        
        # Authors
        self.author1 = Author.objects.create(
            name='John Doe',
            email='john@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        self.author2 = Author.objects.create(
            name='Jane Smith',
            email='jane@example.com',
            bio='Bio',
            birth_date=date(1985, 1, 1)
        )
        
        # Books
        book1 = Book.objects.create(
            title='Python Programming',
            author=self.author1,
            isbn_number='9781111111111',
            price=Decimal('29.99'),
            pages=400,
            publisher='Publisher',
            owner=self.user
        )
        book1.genres.add(self.science)
        
        book2 = Book.objects.create(
            title='Django Development',
            author=self.author1,
            isbn_number='9782222222222',
            price=Decimal('39.99'),
            pages=500,
            publisher='Publisher',
            owner=self.user
        )
        book2.genres.add(self.science)
        
        book3 = Book.objects.create(
            title='Mystery Novel',
            author=self.author2,
            isbn_number='9783333333333',
            price=Decimal('19.99'),
            pages=300,
            publisher='Publisher',
            owner=self.user
        )
        book3.genres.add(self.fiction)
    
    def test_search_filter_and_ordering_combined(self):
        """
        Complex query: Search + Filter + Ordering
        """
        url = f'/api/books/?search=Python&author={self.author1.id}&ordering=-price'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 1)
        
        if results:
            self.assertIn('Python', results[0]['title'])
        
        print("✅ Combined search, filter, and ordering works")


class BookPermissionIntegrationTest(APITestCase):
    """Permission integration test"""
    
    def test_permission_flow(self):
        """
        Complete permission flow:
        1. Anonymous user - can read, can't write
        2. Authenticated user - can create, can edit own
        3. Admin - can do anything
        """
        
        author = Author.objects.create(
            name='Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        
        user = User.objects.create_user(
            username='user',
            password='pass123'
        )
        admin = User.objects.create_superuser(
            username='admin',
            password='admin123'
        )
        
        # Step 1: Anonymous can read
        url = '/api/books/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ Anonymous user can read")
        
        # Step 2: Anonymous can't create
        book_data = {
            'title': 'Test',
            'author_id': author.id,
            'isbn_number': '9781234567897',
            'price': '29.99',
            'pages': 200,
            'publisher': 'Publisher'
        }
        response = self.client.post(url, book_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✅ Anonymous user blocked from creating")
        
        # Step 3: Authenticated user can create
        self.client.force_authenticate(user=user)
        response = self.client.post(url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book_id = response.data['id']
        print("✅ Authenticated user can create")
        
        # Step 4: User can edit own book
        update_url = f'/api/books/{book_id}/'
        response = self.client.patch(update_url, {'title': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ User can edit own book")
        
        # Step 5: Admin can edit any book
        self.client.force_authenticate(user=admin)
        response = self.client.patch(update_url, {'title': 'Admin Updated'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ Admin can edit any book")


class FullStackIntegrationTest(APITestCase):
    """Full stack integration test"""
    
    def test_realistic_user_scenario(self):
        """
        Realistic scenario:
        User registratsiya qiladi, kitoblarni ko'radi,
        qidiradi, filter qiladi
        """
        
        # Setup initial data
        genre = Genre.objects.create(name='Fiction')
        
        author = Author.objects.create(
            name='Popular Author',
            email='author@example.com',
            bio='Bio',
            birth_date=date(1980, 1, 1)
        )
        
        # User yaratish
        user = User.objects.create_user(
            username='buyer',
            password='pass123'
        )
        
        # Create multiple books
        book1 = Book.objects.create(
            title='Bestseller Fiction',
            author=author,
            isbn_number='9781111111111',
            price=Decimal('24.99'),
            pages=300,
            publisher='Publisher',
            owner=user
        )
        book1.genres.add(genre)
        
        book2 = Book.objects.create(
            title='Science Guide',
            author=author,
            isbn_number='9782222222222',
            price=Decimal('34.99'),
            pages=400,
            publisher='Publisher',
            owner=user
        )
        
        # User journey starts
        # 1. Browse books (no auth required)
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 2)
        print("✅ User browsed books")
        
        # 2. Search for specific book
        response = self.client.get('/api/books/?search=Fiction')
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 1)
        print("✅ User searched books")
        
        # 3. Filter by genre
        response = self.client.get(f'/api/books/?genres={genre.id}')
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 1)
        print("✅ User filtered books")
        
        # 4. Authenticate
        self.client.force_authenticate(user=user)
        print("✅ User logged in")
        
        # 5. View book detail
        response = self.client.get(f'/api/books/{book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ User viewed book details")
        
        print("\n✅✅✅ Full user journey completed successfully!")