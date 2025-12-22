"""
Accounts Models Tests
=====================

User va Profile modellarini test qilish
"""

from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile


class UserModelTest(TestCase):
    """User model testlari"""
    
    def test_user_creation(self):
        """User yaratish"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_superuser_creation(self):
        """Superuser yaratish"""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
    
    def test_user_str_method(self):
        """User __str__ metodi"""
        user = User.objects.create_user(
            username='john',
            email='john@example.com',
            password='pass123'
        )
        
        self.assertEqual(str(user), 'john')


class ProfileModelTest(TestCase):
    """Profile model testlari"""
    
    def test_profile_auto_creation(self):
        """
        User yaratilganda avtomatik Profile yaratilishi
        (agar signal ishlatilgan bo'lsa)
        """
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Profile avtomatik yaratilganini tekshirish
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsNotNone(user.profile)
    
    def test_profile_str_method(self):
        """Profile __str__ metodi"""
        user = User.objects.create_user(
            username='john',
            password='pass123'
        )
        
        profile_str = str(user.profile)
        self.assertIn('john', profile_str)
    
    def test_profile_bio_optional(self):
        """Bio field optional"""
        user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
        
        profile = user.profile
        self.assertEqual(profile.bio, '')  # yoki None
    
    def test_profile_update(self):
        """Profile ma'lumotlarini yangilash"""
        user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
        
        profile = user.profile
        profile.bio = 'Test bio'
        profile.location = 'Tashkent'
        profile.birth_date = '1990-01-01'
        profile.save()
        
        profile.refresh_from_db()
        self.assertEqual(profile.bio, 'Test bio')
        self.assertEqual(profile.location, 'Tashkent')


class UserPasswordTest(TestCase):
    """Password bilan bog'liq testlar"""
    
    def test_password_hashing(self):
        """Password hash qilinishi"""
        user = User.objects.create_user(
            username='testuser',
            password='plaintext123'
        )
        
        # Password hash qilingan bo'lishi kerak
        self.assertNotEqual(user.password, 'plaintext123')
        
        # check_password ishlatib tekshirish
        self.assertTrue(user.check_password('plaintext123'))
        self.assertFalse(user.check_password('wrongpassword'))
    
    def test_password_change(self):
        """Passwordni o'zgartirish"""
        user = User.objects.create_user(
            username='testuser',
            password='oldpass123'
        )
        
        # Eski password ishlashi
        self.assertTrue(user.check_password('oldpass123'))
        
        # Yangi password o'rnatish
        user.set_password('newpass123')
        user.save()
        
        # Yangi password ishlashi
        self.assertTrue(user.check_password('newpass123'))
        self.assertFalse(user.check_password('oldpass123'))