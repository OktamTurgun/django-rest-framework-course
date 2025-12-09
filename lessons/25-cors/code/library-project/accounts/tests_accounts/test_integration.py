"""
Accounts Integration Tests
===========================

To'liq authentication flow testlari
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse


class AuthenticationFlowTest(APITestCase):
    """To'liq authentication flow"""

    def test_complete_auth_flow(self):
        """
        To'liq flow:
        1. Register
        2. Login
        3. Access protected endpoint
        4. Update profile
        5. Change password
        6. Logout
        7. Verify access blocked after logout
        """

        # Step 1: Register
        register_url = reverse('accounts:register')
        register_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        register_response = self.client.post(register_url, register_data)
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        print("✅ Step 1: User registered")

        # Step 2: Login
        login_url = reverse('login')
        login_data = {
            'username': 'newuser',
            'password': 'SecurePass123!'
        }
        login_response = self.client.post(login_url, login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data.get('token')
        self.assertIsNotNone(token)
        print("✅ Step 2: User logged in")

        # Step 3: Access protected endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        profile_url = reverse('accounts:user_info')
        profile_response = self.client.get(profile_url)
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data['username'], 'newuser')
        print("✅ Step 3: Accessed protected endpoint")

        # Step 4: Update profile
        update_data = {'first_name': 'Updated', 'bio': 'My bio'}
        update_response = self.client.patch(profile_url, update_data)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['first_name'], 'Updated')
        print("✅ Step 4: Profile updated")

        # Step 5: Change password
        change_pass_url = reverse('change-password')
        change_pass_data = {
            'old_password': 'SecurePass123!',
            'new_password': 'NewSecure456!',
            'new_password2': 'NewSecure456!'
        }
        change_pass_response = self.client.post(change_pass_url, change_pass_data)
        self.assertEqual(change_pass_response.status_code, status.HTTP_200_OK)
        print("✅ Step 5: Password changed")

        # Step 6: Logout
        logout_url = reverse('logout')
        logout_response = self.client.post(logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        print("✅ Step 6: User logged out")

        # Step 7: Verify access blocked after logout
        self.client.credentials()  # Remove token
        verify_response = self.client.get(profile_url)
        self.assertEqual(verify_response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✅ Step 7: Protected endpoint blocked after logout")


class TokenAuthenticationTest(APITestCase):
    """Token authentication integration test"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='SecurePass123!'
        )

    def test_login_and_use_token(self):
        """Login -> Token olish -> Token bilan protected endpoint"""
        login_url = reverse('login')
        data = {'username': 'testuser', 'password': 'SecurePass123!'}
        login_response = self.client.post(login_url, data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data.get('token')
        self.assertIsNotNone(token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        profile_url = reverse('accounts:user_info')
        profile_response = self.client.get(profile_url)
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        print("✅ Token used for authentication")

    def test_invalid_token_rejected(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token')
        profile_url = reverse('profile')
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✅ Invalid token rejected")

    def test_no_token_rejected(self):
        profile_url = reverse('accounts:user_info')
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("✅ No token rejected")


class PasswordManagementTest(APITestCase):
    """Password boshqaruv integration test"""

    def test_password_change_and_login_flow(self):
        user = User.objects.create_user(
            username='testuser',
            password='OldPass123!'
        )
        self.client.force_authenticate(user=user)

        # Change password
        change_url = reverse('accounts:change_password')
        change_data = {
            'old_password': 'OldPass123!',
            'new_password': 'NewPass456!',
            'new_password2': 'NewPass456!'
        }
        response = self.client.post(change_url, change_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("✅ Password changed")

        self.client.force_authenticate(user=None)

        # Old password should fail
        login_url = reverse('login')
        old_login = self.client.post(login_url, {'username': 'testuser', 'password': 'OldPass123!'})
        self.assertEqual(old_login.status_code, status.HTTP_400_BAD_REQUEST)
        print("✅ Old password rejected")

        # New password should succeed
        new_login = self.client.post(login_url, {'username': 'testuser', 'password': 'NewPass456!'})
        self.assertEqual(new_login.status_code, status.HTTP_200_OK)
        self.assertIn('token', new_login.data)
        print("✅ New password accepted")
