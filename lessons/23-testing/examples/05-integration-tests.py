"""
Lesson 23: Integration Tests - Integratsiya testlari
=====================================================

Integration Test - bu bir nechta komponentlarning birgalikda
ishlashini tekshiradigan test.

Unit Test vs Integration Test:
-------------------------------
Unit Test:
- Bitta funksiya/metod
- Izolatsiya qilingan
- Tez
- Mock'lar ishlatiladi

Integration Test:
- Bir nechta komponent
- Haqiqiy database
- Sekinroq
- Real workflow

Qachon Integration Test yoziladi?
----------------------------------
✅ User workflow'larini test qilish
✅ API endpoint'lar orasidagi bog'liqlik
✅ Database bilan ishlash
✅ Authentication flow
✅ Complete business scenario'lar
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from books.models import Book, Author, Category, Review, Order, OrderItem
from decimal import Decimal
from datetime import datetime, timedelta


# =============================================================================
# 1. ODDIY INTEGRATION TEST
# =============================================================================

class SimpleIntegrationTest(APITestCase):
    """
    Oddiy integration test - bir nechta endpoint'ni ketma-ket test qilish
    """
    
    def test_user_registration_and_book_creation_workflow(self):
        """
        User registration -> Login -> Create Book workflow
        
        Bu test 3 ta endpoint'ni ketma-ket test qiladi:
        1. User registration
        2. Login
        3. Book creation
        """
        # Step 1: User registration
        register_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'password2': 'securepass123'
        }
        register_response = self.client.post('/api/auth/register/', register_data)
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        print("✅ Step 1: User registered")
        
        # Step 2: Login
        login_data = {
            'username': 'newuser',
            'password': 'securepass123'
        }
        login_response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data.get('token')
        self.assertIsNotNone(token)
        print("✅ Step 2: User logged in")
        
        # Step 3: Create book with token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        category = Category.objects.create(name='Fiction')
        book_data = {
            'title': 'My First Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'category': category.id,
            'price': '19.99'
        }
        book_response = self.client.post('/api/books/', book_data)
        self.assertEqual(book_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(book_response.data['title'], 'My First Book')
        print("✅ Step 3: Book created")
        
        # Verify: User can see their book
        books_response = self.client.get('/api/books/')
        self.assertEqual(books_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(books_response.data), 1)
        print("✅ Verification: Book visible in list")


# =============================================================================
# 2. CRUD WORKFLOW INTEGRATION TEST
# =============================================================================

class CRUDWorkflowIntegrationTest(APITestCase):
    """
    To'liq CRUD workflow integration test
    Create -> Read -> Update -> Delete
    """
    
    def setUp(self):
        """Test uchun user va category yaratish"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Science')
    
    def test_complete_book_crud_workflow(self):
        """
        To'liq kitob CRUD workflow:
        1. Create book
        2. Read book
        3. Update book
        4. Delete book
        """
        # 1. CREATE
        book_data = {
            'title': 'Integration Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'category': self.category.id,
            'price': '29.99',
            'pages': 350
        }
        create_response = self.client.post('/api/books/', book_data)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        book_id = create_response.data['id']
        print(f"✅ CREATE: Book #{book_id} created")
        
        # 2. READ (Detail)
        read_response = self.client.get(f'/api/books/{book_id}/')
        self.assertEqual(read_response.status_code, status.HTTP_200_OK)
        self.assertEqual(read_response.data['title'], 'Integration Test Book')
        print(f"✅ READ: Book #{book_id} retrieved")
        
        # 3. READ (List)
        list_response = self.client.get('/api/books/')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)
        print("✅ READ: Book visible in list")
        
        # 4. UPDATE (PUT)
        updated_data = book_data.copy()
        updated_data['title'] = 'Updated Integration Test Book'
        updated_data['price'] = '39.99'
        update_response = self.client.put(f'/api/books/{book_id}/', updated_data)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['title'], 'Updated Integration Test Book')
        self.assertEqual(Decimal(update_response.data['price']), Decimal('39.99'))
        print(f"✅ UPDATE: Book #{book_id} updated")
        
        # 5. PARTIAL UPDATE (PATCH)
        patch_data = {'pages': 400}
        patch_response = self.client.patch(f'/api/books/{book_id}/', patch_data)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data['pages'], 400)
        print(f"✅ PATCH: Book #{book_id} partially updated")
        
        # 6. DELETE
        delete_response = self.client.delete(f'/api/books/{book_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        print(f"✅ DELETE: Book #{book_id} deleted")
        
        # 7. VERIFY DELETION
        verify_response = self.client.get(f'/api/books/{book_id}/')
        self.assertEqual(verify_response.status_code, status.HTTP_404_NOT_FOUND)
        print("✅ VERIFY: Book no longer exists")


# =============================================================================
# 3. MULTI-STEP BUSINESS SCENARIO
# =============================================================================

class BookstoreBusinessScenarioTest(APITestCase):
    """
    Real-world bookstore business scenario:
    User buys books and leaves reviews
    """
    
    def setUp(self):
        """Dastlabki ma'lumotlar"""
        # Categories
        self.fiction = Category.objects.create(name='Fiction')
        self.science = Category.objects.create(name='Science')
        
        # Books
        self.book1 = Book.objects.create(
            title='Python Programming',
            author='John Doe',
            isbn='1111111111111',
            category=self.science,
            price=Decimal('29.99'),
            stock=10
        )
        self.book2 = Book.objects.create(
            title='Django Mastery',
            author='Jane Smith',
            isbn='2222222222222',
            category=self.science,
            price=Decimal('39.99'),
            stock=5
        )
        
        # User
        self.user = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='customerpass'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_complete_purchase_and_review_workflow(self):
        """
        To'liq xarid va review workflow:
        1. Browse books
        2. Add to cart
        3. Checkout
        4. Verify order
        5. Leave review
        6. Check author's books
        """
        
        # Step 1: Browse books
        browse_response = self.client.get('/api/books/')
        self.assertEqual(browse_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(browse_response.data), 2)
        print("✅ Step 1: Browsed books")
        
        # Step 2: View book details
        book_detail = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(book_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(book_detail.data['title'], 'Python Programming')
        print("✅ Step 2: Viewed book details")
        
        # Step 3: Create order (buy books)
        order_data = {
            'items': [
                {'book': self.book1.id, 'quantity': 2},
                {'book': self.book2.id, 'quantity': 1}
            ]
        }
        order_response = self.client.post('/api/orders/', order_data)
        self.assertEqual(order_response.status_code, status.HTTP_201_CREATED)
        order_id = order_response.data['id']
        print(f"✅ Step 3: Order #{order_id} created")
        
        # Step 4: Verify order
        order_detail = self.client.get(f'/api/orders/{order_id}/')
        self.assertEqual(order_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(len(order_detail.data['items']), 2)
        
        # Calculate total
        expected_total = (self.book1.price * 2) + (self.book2.price * 1)
        self.assertEqual(
            Decimal(order_detail.data['total_price']),
            expected_total
        )
        print(f"✅ Step 4: Order verified (Total: ${expected_total})")
        
        # Step 5: Verify stock decreased
        self.book1.refresh_from_db()
        self.book2.refresh_from_db()
        self.assertEqual(self.book1.stock, 8)  # 10 - 2
        self.assertEqual(self.book2.stock, 4)  # 5 - 1
        print("✅ Step 5: Stock updated")
        
        # Step 6: Leave review for book1
        review_data = {
            'book': self.book1.id,
            'rating': 5,
            'comment': 'Excellent book! Highly recommended.'
        }
        review_response = self.client.post('/api/reviews/', review_data)
        self.assertEqual(review_response.status_code, status.HTTP_201_CREATED)
        print("✅ Step 6: Review posted")
        
        # Step 7: Verify review appears on book page
        book_with_review = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertIn('reviews', book_with_review.data)
        self.assertEqual(len(book_with_review.data['reviews']), 1)
        print("✅ Step 7: Review visible on book page")
        
        # Step 8: Check user's orders
        user_orders = self.client.get('/api/orders/my-orders/')
        self.assertEqual(user_orders.status_code, status.HTTP_200_OK)
        self.assertEqual(len(user_orders.data), 1)
        print("✅ Step 8: User orders retrieved")
        
        # Step 9: Search for books by author
        search_response = self.client.get('/api/books/?author=John')
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(search_response.data), 0)
        print("✅ Step 9: Author search works")


# =============================================================================
# 4. AUTHENTICATION FLOW INTEGRATION TEST
# =============================================================================

class AuthenticationFlowTest(APITestCase):
    """
    To'liq authentication flow test
    """
    
    def test_complete_authentication_flow(self):
        """
        Registration -> Login -> Access Protected -> Logout -> Access Fails
        """
        
        # Step 1: Register new user
        register_data = {
            'username': 'authuser',
            'email': 'auth@example.com',
            'password': 'secure123',
            'password2': 'secure123',
            'first_name': 'Auth',
            'last_name': 'User'
        }
        register_response = self.client.post('/api/auth/register/', register_data)
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        user_id = register_response.data.get('id')
        print("✅ Step 1: User registered")
        
        # Step 2: Login
        login_data = {
            'username': 'authuser',
            'password': 'secure123'
        }
        login_response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data.get('token')
        self.assertIsNotNone(token)
        print("✅ Step 2: User logged in")
        
        # Step 3: Access protected endpoint with token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        profile_response = self.client.get('/api/auth/profile/')
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data['username'], 'authuser')
        print("✅ Step 3: Accessed protected endpoint")
        
        # Step 4: Update profile
        update_data = {'first_name': 'Updated', 'last_name': 'Name'}
        update_response = self.client.patch('/api/auth/profile/', update_data)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['first_name'], 'Updated')
        print("✅ Step 4: Profile updated")
        
        # Step 5: Logout
        logout_response = self.client.post('/api/auth/logout/')
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        print("✅ Step 5: User logged out")
        
        # Step 6: Try to access protected endpoint (should fail)
        self.client.credentials()  # Remove token
        protected_response = self.client.get('/api/auth/profile/')
        self.assertEqual(protected_response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✅ Step 6: Protected endpoint blocked after logout")


# =============================================================================
# 5. PERMISSION AND AUTHORIZATION TEST
# =============================================================================

class PermissionIntegrationTest(APITestCase):
    """
    Permissions va authorization integration test
    """
    
    def setUp(self):
        """Users va data"""
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='user123'
        )
        
        self.category = Category.objects.create(name='Test')
        
        self.admin_book = Book.objects.create(
            title='Admin Book',
            author='Admin',
            isbn='1111111111111',
            category=self.category,
            created_by=self.admin
        )
        
        self.user_book = Book.objects.create(
            title='User Book',
            author='User',
            isbn='2222222222222',
            category=self.category,
            created_by=self.regular_user
        )
    
    def test_regular_user_cannot_edit_others_books(self):
        """Regular user boshqaning kitobini edit qila olmaydi"""
        self.client.force_authenticate(user=self.regular_user)
        
        # Try to edit admin's book
        response = self.client.patch(
            f'/api/books/{self.admin_book.id}/',
            {'title': 'Hacked'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("✅ Regular user blocked from editing others' books")
    
    def test_regular_user_can_edit_own_books(self):
        """Regular user o'z kitobini edit qila oladi"""
        self.client.force_authenticate(user=self.regular_user)
        
        # Edit own book
        response = self.client.patch(
            f'/api/books/{self.user_book.id}/',
            {'title': 'Updated User Book'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ Regular user can edit own books")
    
    def test_admin_can_edit_any_book(self):
        """Admin har qanday kitobni edit qila oladi"""
        self.client.force_authenticate(user=self.admin)
        
        # Edit user's book
        response = self.client.patch(
            f'/api/books/{self.user_book.id}/',
            {'title': 'Admin Updated User Book'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ Admin can edit any book")
    
    def test_unauthenticated_cannot_create_book(self):
        """Unauthenticated user kitob yarata olmaydi"""
        response = self.client.post('/api/books/', {
            'title': 'Test',
            'author': 'Test',
            'isbn': '3333333333333',
            'category': self.category.id
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✅ Unauthenticated user blocked from creating books")


# =============================================================================
# 6. DATABASE STATE VERIFICATION
# =============================================================================

class DatabaseStateIntegrationTest(APITestCase):
    """
    Database state'ni to'liq tekshirish
    """
    
    def test_cascading_deletes(self):
        """
        Cascade delete'lar to'g'ri ishlashi
        Author o'chirilsa, uning kitoblari ham o'chirilishi kerak
        """
        # Setup
        category = Category.objects.create(name='Test')
        author = Author.objects.create(
            name='Test Author',
            email='author@example.com'
        )
        
        # Create 3 books for this author
        for i in range(3):
            Book.objects.create(
                title=f'Book {i+1}',
                author=author,
                isbn=f'{i}111111111111',
                category=category
            )
        
        # Verify: 3 books exist
        self.assertEqual(Book.objects.filter(author=author).count(), 3)
        print("✅ Setup: 3 books created")
        
        # Delete author
        author_id = author.id
        author.delete()
        
        # Verify: All books deleted (cascade)
        self.assertEqual(Book.objects.filter(author_id=author_id).count(), 0)
        print("✅ Cascade delete: All author's books deleted")
    
    def test_transaction_rollback_on_error(self):
        """
        Transaction rollback test
        Error bo'lsa, hech narsa o'zgarmasligi kerak
        """
        category = Category.objects.create(name='Test')
        user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user=user)
        
        initial_count = Book.objects.count()
        
        # Try to create book with invalid data
        # (ISBN too short - validation error)
        invalid_data = {
            'title': 'Test Book',
            'author': 'Author',
            'isbn': '123',  # Invalid
            'category': category.id
        }
        
        response = self.client.post('/api/books/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify: No book created
        self.assertEqual(Book.objects.count(), initial_count)
        print("✅ Transaction rolled back on error")


# =============================================================================
# XULOSA VA BEST PRACTICES
# =============================================================================

"""
INTEGRATION TESTS - ASOSIY QOIDALAR:
====================================

1️⃣ Integration Test maqsadi:
   ✅ Real-world scenario'larni test qilish
   ✅ Komponentlar orasidagi integratsiyani tekshirish
   ✅ End-to-end workflow'larni tasdiqlash

2️⃣ Nima test qilish kerak:
   ✅ User registration va login flow
   ✅ CRUD operations
   ✅ Multi-step business scenarios
   ✅ Authentication va authorization
   ✅ Database state changes
   ✅ Permissions
   ✅ Data validation
   ✅ Error handling

3️⃣ Integration vs Unit Test:
   Unit Test:
   - Bitta funksiya
   - Mock'lar ishlatiladi
   - Tez
   - Ko'p yoziladi
   
   Integration Test:
   - Bir nechta komponent
   - Real database
   - Sekinroq
   - Kamroq yoziladi (lekin muhim)

4️⃣ Best Practices:
   ✅ AAA pattern: Arrange, Act, Assert
   ✅ Aniq step'lar bilan
   ✅ Har step'ni verify qiling
   ✅ Real user workflow'larini test qiling
   ✅ Database state'ni tekshiring
   ✅ Error case'larni ham test qiling
   ✅ Transaction rollback'ni test qiling

5️⃣ Test Data:
   ✅ setUp() da umumiy data yarating
   ✅ Har test o'z specific data'sini yaratsin
   ✅ Realistic data ishlatish
   ✅ Factory Boy yordamida

6️⃣ Assertions:
   ✅ Har step'da status code tekshiring
   ✅ Response data'ni verify qiling
   ✅ Database state'ni tekshiring
   ✅ Side effect'larni tasdiqlang

7️⃣ Debugging:
   ✅ print() statement'lar qo'shing
   ✅ Verbose mode ishlatish: --verbosity=2
   ✅ Har step'ni alohida test qiling
   ✅ Database state'ni print qiling


INTEGRATION TESTLARNI ISHGA TUSHIRISH:
======================================
python manage.py test books.tests.test_integration --verbosity=2
"""