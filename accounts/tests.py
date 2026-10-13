from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


class SignupViewTests(TestCase):
    def test_signup_page_loads(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create an account')

    def test_signup_creates_user_and_redirects(self):
        payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'role': 'seeker',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }

        response = self.client.post(reverse('accounts:signup'), payload)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('jobs:job_list'))
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())
