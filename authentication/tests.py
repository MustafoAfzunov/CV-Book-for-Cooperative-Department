

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.signin_url = reverse('signin')
        self.token_refresh_url = reverse('token_refresh')
        self.password_reset_url = reverse('password_reset')
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_signup_success(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_signup_duplicate_email(self):
        data = {
            'username': 'newuser',
            'email': 'test@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_signin_success(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.signin_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_signin_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(self.signin_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'error': 'Invalid credentials'})

    def test_token_refresh_success(self):
        signin_data = {'username': 'testuser', 'password': 'testpass123'}
        signin_response = self.client.post(self.signin_url, signin_data, format='json')
        refresh_token = signin_response.data['refresh']
        data = {'refresh': refresh_token}
        response = self.client.post(self.token_refresh_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_password_reset_success(self):
        data = {'email': 'test@example.com'}
        response = self.client.post(self.password_reset_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Password reset link sent.'})

    def test_password_reset_invalid_email(self):
        data = {'email': 'nonexistent@example.com'}
        response = self.client.post(self.password_reset_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_password_reset_confirm_success(self):
        user = self.user
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        data = {'new_password': 'newpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Password has been reset successfully.'})
        user.refresh_from_db()
        self.assertTrue(user.check_password('newpass123'))

    def test_password_reset_confirm_invalid_token(self):
        user = self.user
        invalid_token = 'invalidtoken'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': invalid_token})
        data = {'new_password': 'newpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'], ['Invalid or expired token.'])