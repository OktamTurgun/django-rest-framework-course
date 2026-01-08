"""
Accounts Views Tests
====================

Registration, Login, Logout, Profile, Password Change view testlari
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.serializers import UserSerializer


class RegistrationViewTest(APITestCase):
    """Registration view testlari"""

    def test_register_user_success(self):
        """Muvaffaqiyatli registration"""
        url = reverse('accounts:register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'New',
            'last_name': 'User'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'newuser')
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_password_mismatch(self):
        """Password va password2 mos kelmasligi"""
        url = reverse('accounts:register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'Password123!',
            'password2': 'Different123!'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_missing_fields(self):
        """Majburiy fieldlar yo'q"""
        url = reverse('accounts:register')
        data = {'username': 'newuser'}  # email va password yo'q

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)

    def test_register_duplicate_username(self):
        """Mavjud username bilan"""
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='pass123'
        )
        url = reverse('accounts:register')
        data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_register_duplicate_email(self):
        """Mavjud email bilan"""
        User.objects.create_user(
            username='user1',
            email='same@example.com',
            password='pass123'
        )
        url = reverse('accounts:register')
        data = {
            'username': 'user2',
            'email': 'same@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class LoginViewTest(APITestCase):
    """Login view testlari"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123!'
        )

    def test_login_success(self):
        """Muvaffaqiyatli login"""
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'SecurePass123!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_credentials(self):
        """Noto'g'ri credentials"""
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'WrongPass123!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_fields(self):
        """Majburiy fieldlar yo'q"""
        url = reverse('login')
        response = self.client.post(url, {'password': 'SecurePass123!'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(url, {'username': 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutViewTest(APITestCase):
    """Logout view testlari"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='SecurePass123!'
        )
        self.client.force_authenticate(user=self.user)

    def test_logout_success(self):
        """Muvaffaqiyatli logout"""
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_unauthenticated(self):
        """Unauthenticated logout"""
        self.client.force_authenticate(user=None)
        url = reverse('logout')
        response = self.client.post(url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_200_OK])


class ProfileViewTest(APITestCase):
    """Profile view testlari"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123!'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        url = reverse('accounts:user_info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_update_profile(self):
        url = reverse('accounts:user_info')
        data = {'first_name': 'Updated', 'last_name': 'Name', 'email': 'updated@example.com'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_get_profile_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('accounts:user_info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PasswordChangeViewTest(APITestCase):
    """Password change view testlari"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='OldPass123!'
        )
        self.client.force_authenticate(user=self.user)

    def test_change_password_success(self):
        url = reverse('accounts:change_password')
        data = {'old_password': 'OldPass123!', 'new_password': 'NewPass123!', 'new_password2': 'NewPass123!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass123!'))

    def test_change_password_wrong_old_password(self):
        url = reverse('accounts:change_password')
        data = {'old_password': 'WrongPass123!', 'new_password': 'NewPass123!', 'new_password2': 'NewPass123!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_mismatch(self):
        url = reverse('accounts:change_password')
        data = {'old_password': 'OldPass123!', 'new_password': 'NewPass123!', 'new_password2': 'Mismatch123!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
