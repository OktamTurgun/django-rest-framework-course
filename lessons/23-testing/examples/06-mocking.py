"""
Lesson 23: Mocking - Mock obyektlar va unittest.mock
====================================================

Mocking - bu test paytida haqiqiy obyektlarning o'rniga
"soxta" (fake) obyektlardan foydalanish.

Nima uchun Mocking kerak?
--------------------------
✅ Tashqi servislarni test qilish (Email, SMS, Payment)
✅ Sekin operatsiyalarni tezlashtirish (Database, File I/O)
✅ Test environment'ni izolatsiya qilish
✅ Har xil holatlarni simulatsiya qilish (error, timeout)
✅ External API'larga bog'liq bo'lmaslik

Qachon Mock ishlatiladi?
-------------------------
✅ Email yuborish
✅ SMS yuborish
✅ Payment processing
✅ External API calls (Weather, Maps, etc.)
✅ File operations
✅ Time-dependent code
✅ Random values
"""

from unittest.mock import Mock, MagicMock, patch, call
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.core.mail import send_mail
from books.models import Book, Category, Author
from decimal import Decimal
import requests
from datetime import datetime


# =============================================================================
# 1. MOCK BASICS - Asosiy tushunchalar
# =============================================================================

class MockBasicsTest(TestCase):
    """
    Mock obyekt bilan ishlash asoslari
    """
    
    def test_simple_mock(self):
        """Oddiy Mock obyekt"""
        # Mock obyekt yaratish
        mock_obj = Mock()
        
        # Mock'ga qiymat berish
        mock_obj.method.return_value = 42
        
        # Mock'ni chaqirish
        result = mock_obj.method()
        
        # Tekshirish
        self.assertEqual(result, 42)
        mock_obj.method.assert_called_once()
        print("✅ Simple mock works")
    
    def test_mock_with_attributes(self):
        """Attribute'lar bilan Mock"""
        mock_user = Mock()
        mock_user.username = 'testuser'
        mock_user.email = 'test@example.com'
        mock_user.is_active = True
        
        # Tekshirish
        self.assertEqual(mock_user.username, 'testuser')
        self.assertEqual(mock_user.email, 'test@example.com')
        self.assertTrue(mock_user.is_active)
        print("✅ Mock with attributes works")
    
    def test_mock_method_calls(self):
        """Mock method'larini chaqirishni kuzatish"""
        mock_service = Mock()
        
        # Method'ni chaqirish
        mock_service.process_payment(100, 'USD')
        mock_service.send_confirmation('user@example.com')
        
        # Chaqirilganini tekshirish
        mock_service.process_payment.assert_called_once_with(100, 'USD')
        mock_service.send_confirmation.assert_called_once_with('user@example.com')
        
        # Umumiy chaqiriqlar soni
        self.assertEqual(mock_service.process_payment.call_count, 1)
        print("✅ Mock method calls tracked")


# =============================================================================
# 2. PATCH DECORATOR - @patch
# =============================================================================

class EmailService:
    """Email yuborish servisi (mock qilish uchun)"""
    
    @staticmethod
    def send_welcome_email(user_email, username):
        """Welcome email yuborish"""
        subject = f'Welcome {username}!'
        message = f'Thank you for registering, {username}!'
        send_mail(subject, message, 'noreply@example.com', [user_email])
        return True
    
    @staticmethod
    def send_order_confirmation(user_email, order_id, total):
        """Order confirmation email"""
        subject = f'Order #{order_id} Confirmed'
        message = f'Your order total: ${total}'
        send_mail(subject, message, 'orders@example.com', [user_email])
        return True


class PatchDecoratorTest(TestCase):
    """
    @patch decorator bilan mock qilish
    """
    
    @patch('django.core.mail.send_mail')
    def test_send_welcome_email_mocked(self, mock_send_mail):
        """
        Email yuborishni mock qilish
        
        @patch - bu haqiqiy send_mail funksiyasini
        mock bilan almashtiradi
        """
        # Mock'ning return value'sini belgilash
        mock_send_mail.return_value = 1  # Email yuborildi
        
        # Email yuborish
        result = EmailService.send_welcome_email('user@example.com', 'John')
        
        # Tekshirish
        self.assertTrue(result)
        
        # send_mail chaqirilganini tekshirish
        mock_send_mail.assert_called_once()
        
        # Argumentlarni tekshirish
        args, kwargs = mock_send_mail.call_args
        self.assertEqual(args[0], 'Welcome John!')  # subject
        self.assertEqual(args[3], ['user@example.com'])  # recipient
        
        print("✅ Email sending mocked successfully")
    
    @patch('django.core.mail.send_mail')
    def test_multiple_emails(self, mock_send_mail):
        """Bir nechta email yuborish"""
        mock_send_mail.return_value = 1
        
        # 2 ta email yuborish
        EmailService.send_welcome_email('user1@example.com', 'User1')
        EmailService.send_order_confirmation('user2@example.com', '123', 99.99)
        
        # 2 marta chaqirilganini tekshirish
        self.assertEqual(mock_send_mail.call_count, 2)
        
        # Har bir chaqiriqni tekshirish
        calls = [
            call('Welcome User1!', 'Thank you for registering, User1!', 
                 'noreply@example.com', ['user1@example.com']),
            call('Order #123 Confirmed', 'Your order total: $99.99',
                 'orders@example.com', ['user2@example.com'])
        ]
        mock_send_mail.assert_has_calls(calls)
        print("✅ Multiple emails mocked")


# =============================================================================
# 3. MOCKING EXTERNAL API CALLS
# =============================================================================

class WeatherService:
    """Tashqi API - Weather service"""
    
    @staticmethod
    def get_weather(city):
        """Shahar ob-havosini olish"""
        response = requests.get(
            f'https://api.weather.com/v1/current',
            params={'city': city}
        )
        return response.json()
    
    @staticmethod
    def get_temperature(city):
        """Haroratni olish"""
        weather_data = WeatherService.get_weather(city)
        return weather_data.get('temperature')


class ExternalAPITest(TestCase):
    """
    External API'larni mock qilish
    """
    
    @patch('requests.get')
    def test_get_weather_success(self, mock_get):
        """
        Weather API muvaffaqiyatli javob
        """
        # Mock response yaratish
        mock_response = Mock()
        mock_response.json.return_value = {
            'temperature': 25,
            'condition': 'Sunny',
            'humidity': 60
        }
        mock_get.return_value = mock_response
        
        # Weather ma'lumotlarini olish
        weather = WeatherService.get_weather('Tashkent')
        
        # Tekshirish
        self.assertEqual(weather['temperature'], 25)
        self.assertEqual(weather['condition'], 'Sunny')
        
        # API chaqirilganini tekshirish
        mock_get.assert_called_once()
        print("✅ External API mocked (success)")
    
    @patch('requests.get')
    def test_get_weather_api_error(self, mock_get):
        """
        Weather API xato qaytaradi
        """
        # Mock'ni exception throw qilish uchun sozlash
        mock_get.side_effect = requests.RequestException('API unavailable')
        
        # Xatoni tekshirish
        with self.assertRaises(requests.RequestException):
            WeatherService.get_weather('Tashkent')
        
        print("✅ External API error mocked")
    
    @patch.object(WeatherService, 'get_weather')
    def test_get_temperature_mocked(self, mock_get_weather):
        """
        Specific method'ni mock qilish (patch.object)
        """
        # get_weather method'ini mock qilish
        mock_get_weather.return_value = {
            'temperature': 30,
            'condition': 'Hot'
        }
        
        # Haroratni olish
        temp = WeatherService.get_temperature('Tashkent')
        
        # Tekshirish
        self.assertEqual(temp, 30)
        mock_get_weather.assert_called_once_with('Tashkent')
        print("✅ Specific method mocked with patch.object")


# =============================================================================
# 4. MOCKING DATABASE QUERIES
# =============================================================================

class BookService:
    """Book service - database bilan ishlash"""
    
    @staticmethod
    def get_expensive_books(min_price=50):
        """Qimmat kitoblarni olish"""
        return Book.objects.filter(price__gte=min_price).count()
    
    @staticmethod
    def get_book_details(book_id):
        """Kitob ma'lumotlarini olish"""
        try:
            book = Book.objects.get(id=book_id)
            return {
                'id': book.id,
                'title': book.title,
                'price': book.price
            }
        except Book.DoesNotExist:
            return None


class DatabaseMockingTest(TestCase):
    """
    Database query'larni mock qilish
    """
    
    @patch.object(Book.objects, 'filter')
    def test_get_expensive_books_mocked(self, mock_filter):
        """
        Database query'ni mock qilish
        """
        # Mock queryset
        mock_queryset = Mock()
        mock_queryset.count.return_value = 5
        mock_filter.return_value = mock_queryset
        
        # Method'ni chaqirish
        count = BookService.get_expensive_books(min_price=100)
        
        # Tekshirish
        self.assertEqual(count, 5)
        mock_filter.assert_called_once_with(price__gte=100)
        print("✅ Database query mocked")


# =============================================================================
# 5. MOCKING datetime.now() - VAQTNI MOCK QILISH
# =============================================================================

class TimeService:
    """Vaqt bilan ishlash"""
    
    @staticmethod
    def get_current_year():
        """Joriy yilni olish"""
        return datetime.now().year
    
    @staticmethod
    def is_weekend():
        """Hafta oxirimi?"""
        weekday = datetime.now().weekday()
        return weekday >= 5  # 5=Saturday, 6=Sunday


class TimeMockingTest(TestCase):
    """
    datetime.now() ni mock qilish
    """
    
    @patch('books.services.datetime')
    def test_get_current_year_mocked(self, mock_datetime):
        """
        datetime.now() ni mock qilish
        """
        # Mock datetime
        mock_datetime.now.return_value = datetime(2030, 6, 15)
        
        # Yilni olish
        year = TimeService.get_current_year()
        
        # Tekshirish
        self.assertEqual(year, 2030)
        print("✅ datetime.now() mocked")
    
    @patch('books.services.datetime')
    def test_is_weekend_saturday(self, mock_datetime):
        """Shanba kunini mock qilish"""
        # Saturday = weekday 5
        mock_datetime.now.return_value = datetime(2024, 1, 6)  # Saturday
        
        result = TimeService.is_weekend()
        self.assertTrue(result)
        print("✅ Weekend (Saturday) mocked")
    
    @patch('books.services.datetime')
    def test_is_weekend_monday(self, mock_datetime):
        """Dushanba kunini mock qilish"""
        # Monday = weekday 0
        mock_datetime.now.return_value = datetime(2024, 1, 1)  # Monday
        
        result = TimeService.is_weekend()
        self.assertFalse(result)
        print("✅ Weekday (Monday) mocked")


# =============================================================================
# 6. MOCK side_effect - TURLI NATIJALAR
# =============================================================================

class PaymentService:
    """Payment processing service"""
    
    @staticmethod
    def process_payment(amount, card_number):
        """To'lovni qayta ishlash"""
        # External payment gateway
        # (Bu yerda haqiqiy payment API chaqiriladi)
        pass


class SideEffectTest(TestCase):
    """
    side_effect bilan turli natijalarni simulatsiya qilish
    """
    
    def test_side_effect_with_list(self):
        """
        side_effect - har chaqiriqda boshqa natija
        """
        mock_payment = Mock()
        
        # Har chaqiriqda boshqa qiymat
        mock_payment.process.side_effect = [True, False, True]
        
        # 1-chaqiriq: True
        self.assertTrue(mock_payment.process())
        
        # 2-chaqiriq: False
        self.assertFalse(mock_payment.process())
        
        # 3-chaqiriq: True
        self.assertTrue(mock_payment.process())
        
        print("✅ side_effect with list works")
    
    def test_side_effect_with_exception(self):
        """
        side_effect - exception throw qilish
        """
        mock_payment = Mock()
        
        # Exception throw qilish
        mock_payment.process.side_effect = ValueError('Insufficient funds')
        
        # Exception'ni tekshirish
        with self.assertRaises(ValueError) as cm:
            mock_payment.process(100)
        
        self.assertIn('Insufficient funds', str(cm.exception))
        print("✅ side_effect with exception works")
    
    def test_side_effect_with_function(self):
        """
        side_effect - custom funksiya
        """
        def custom_side_effect(amount):
            if amount > 1000:
                raise ValueError('Amount too large')
            return True
        
        mock_payment = Mock()
        mock_payment.process.side_effect = custom_side_effect
        
        # Kichik miqdor - muvaffaqiyatli
        self.assertTrue(mock_payment.process(500))
        
        # Katta miqdor - xato
        with self.assertRaises(ValueError):
            mock_payment.process(2000)
        
        print("✅ side_effect with function works")


# =============================================================================
# 7. REAL-WORLD EXAMPLE - TO'LIQ MISOL
# =============================================================================

class OrderService:
    """Order yaratish servisi"""
    
    @staticmethod
    def create_order(user, items):
        """
        Order yaratish:
        1. Payment processing
        2. Email yuborish
        3. SMS yuborish
        4. Inventory update
        """
        from services.payment_gateway import PaymentGateway
        from services.email_service import EmailService
        from services.sms_service import SMSService
        from services.inventory_service import InventoryService
        
        # Calculate total
        total = sum(item['price'] * item['quantity'] for item in items)
        
        # Process payment
        payment_result = PaymentGateway.charge(user.id, total)
        if not payment_result['success']:
            raise ValueError('Payment failed')
        
        # Send confirmation email
        EmailService.send_order_confirmation(
            user.email,
            payment_result['order_id'],
            total
        )
        
        # Send SMS
        SMSService.send_order_sms(user.phone, payment_result['order_id'])
        
        # Update inventory
        for item in items:
            InventoryService.decrease_stock(item['product_id'], item['quantity'])
        
        return payment_result['order_id']


class OrderServiceIntegrationTest(TestCase):
    """
    OrderService - barcha tashqi servislarni mock qilish
    """
    
    @patch('inventory_service.InventoryService.decrease_stock')
    @patch('sms_service.SMSService.send_order_sms')
    @patch('email_service.EmailService.send_order_confirmation')
    @patch('payment_gateway.PaymentGateway.charge')
    def test_create_order_success(
        self,
        mock_charge,
        mock_email,
        mock_sms,
        mock_inventory
    ):
        """
        Muvaffaqiyatli order yaratish
        Barcha tashqi servislar mock qilingan
        """
        # Setup user
        user = User(
            id=1,
            username='testuser',
            email='user@example.com',
            phone='+998901234567'
        )
        
        # Setup items
        items = [
            {'product_id': 1, 'price': 10, 'quantity': 2},
            {'product_id': 2, 'price': 15, 'quantity': 1}
        ]
        
        # Mock payment gateway
        mock_charge.return_value = {
            'success': True,
            'order_id': 'ORD-12345'
        }
        
        # Create order
        order_id = OrderService.create_order(user, items)
        
        # Verify: Order ID returned
        self.assertEqual(order_id, 'ORD-12345')
        
        # Verify: Payment processed
        mock_charge.assert_called_once_with(1, 35)  # user_id=1, total=35
        
        # Verify: Email sent
        mock_email.assert_called_once_with(
            'user@example.com',
            'ORD-12345',
            35
        )
        
        # Verify: SMS sent
        mock_sms.assert_called_once_with('+998901234567', 'ORD-12345')
        
        # Verify: Inventory updated (2 items)
        self.assertEqual(mock_inventory.call_count, 2)
        
        print("✅ Complete order flow mocked successfully")


# =============================================================================
# 8. MOCK BEST PRACTICES
# =============================================================================

"""
MOCKING BEST PRACTICES:
=======================

1️⃣ Nimani mock qilish kerak:
   ✅ External API calls
   ✅ Email/SMS services
   ✅ Payment gateways
   ✅ File I/O operations
   ✅ datetime.now(), random()
   ✅ Slow database queries
   ✅ Third-party libraries

2️⃣ Nimani mock qilmaslik kerak:
   ❌ O'zingizning business logic
   ❌ Simple funksiyalar
   ❌ Data models
   ❌ Constants

3️⃣ Mock strukturasi:
   @patch('module.path.to.function')
   def test_method(self, mock_function):
       # Setup mock
       mock_function.return_value = 'result'
       
       # Call code
       result = my_function()
       
       # Verify
       mock_function.assert_called_once()

4️⃣ return_value vs side_effect:
   return_value: Har doim bir xil natija
   side_effect: Har xil natijalar, exception'lar

5️⃣ Assertion metodlari:
   ✅ assert_called()
   ✅ assert_called_once()
   ✅ assert_called_with(args)
   ✅ assert_called_once_with(args)
   ✅ assert_not_called()
   ✅ assert_has_calls([call1, call2])

6️⃣ Patch strategies:
   @patch('module.function') - Function'ni patch qilish
   @patch.object(Class, 'method') - Method'ni patch qilish
   @patch.multiple() - Bir nechta narsani patch qilish

7️⃣ Context manager bilan:
   with patch('module.function') as mock_func:
       mock_func.return_value = 'value'
       # Test code

8️⃣ Mock vs MagicMock:
   Mock: Oddiy mock
   MagicMock: Magic methods bilan (__str__, __len__, etc.)


UMUMIY XATOLAR:
===============

❌ Mock'ni noto'g'ri yo'lda patch qilish
✅ To'g'ri import path ishlatish

❌ Mock'ni verify qilmaslik
✅ Har doim assert_called_* ishlatish

❌ Ortiqcha mock qilish
✅ Faqat kerakli narsalarni mock qiling

❌ Real code bilan mock aralashtirib yuborish
✅ Aniq ajrating


ISHLATISH:
==========
python manage.py test path.to.this.file --verbosity=2
"""