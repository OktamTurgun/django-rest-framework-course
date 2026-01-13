"""
Accounts Serializers Tests
===========================

Registration, Login serializer testlari
"""

from django.test import TestCase
from django.contrib.auth.models import User
from accounts.serializers import (
    UserSerializer,
    UserRegistrationSerializer,
)


class UserSerializerTest(TestCase):
    """UserSerializer testlari"""
    
    def test_user_serializer_fields(self):
        """Serializer'dagi fieldlarni tekshirish"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        
        serializer = UserSerializer(user)
        data = serializer.data
        
        self.assertIn('id', data)
        self.assertIn('username', data)
        self.assertIn('email', data)
        self.assertIn('first_name', data)
        self.assertIn('last_name', data)
        
        # Password bo'lmasligi kerak
        self.assertNotIn('password', data)


class UserRegistrationSerializerTest(TestCase):
    """UserRegistrationSerializer testlari"""
    
    def test_register_serializer_valid_data(self):
        """Valid ma'lumotlar bilan registration"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'new@example.com')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')
        
        # Password hash qilingan
        self.assertTrue(user.check_password('SecurePass123!'))
    
    def test_register_password_mismatch(self):
        """Password va password2 mos kelmasligi"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
            'password2': 'different123'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
    
    def test_register_username_required(self):
        """Username majburiy"""
        data = {
            'email': 'new@example.com',
            'password': 'pass123',
            'password2': 'pass123'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
    
    def test_register_email_required(self):
        """Email majburiy"""
        data = {
            'username': 'newuser',
            'password': 'pass123',
            'password2': 'pass123'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
    
    def test_register_username_unique(self):
        """Username unique bo'lishi kerak"""
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='pass123'
        )
        
        data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password': 'pass123',
            'password2': 'pass123'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
    
    def test_register_email_unique(self):
        """Email unique bo'lishi kerak"""
        User.objects.create_user(
            username='user1',
            email='same@example.com',
            password='pass123'
        )
        
        data = {
            'username': 'user2',
            'email': 'same@example.com',
            'password': 'pass123',
            'password2': 'pass123'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
    
    def test_register_weak_password(self):
        """Zaif password (validate_password orqali)"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': '123',
            'password2': '123'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
