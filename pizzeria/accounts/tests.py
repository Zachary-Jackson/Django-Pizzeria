from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountsTests(TestCase):
    """Tests for the accounts app"""

    def setUp(self):
        """Creates a User for testing"""

        self.test_user = User.objects.create_user(
            email='test@test.com',
            username='test_user',
            password='test_password'
        )

    def test_create_account_get(self):
        """Ensures that create_account shows the correct information"""

        # Check if the correct template was used
        with self.assertTemplateUsed('accounts/create_account.html'):

            # Create a response object from information given by the server
            resp = self.client.get(reverse('accounts:create_account'))

        # Check various page information
        self.assertContains(resp, 'Create your account!')
        self.assertContains(resp, 'or Login')
        self.assertContains(resp, 'Create')

    def test_create_account_post(self):
        """Checks that a user can be created"""

        # Create data to POST to the server
        post_data = {
            'username': 'new_user',
            'password1': 'test_password',
            'password2': 'test_password',
        }
        resp = self.client.post(
            reverse(
                'accounts:create_account',
            ), data=post_data
        )

        # Ensure that we have 2 users, one from setUp and one from the POST
        self.assertEqual(len(User.objects.all()), 2)

        # We should have been redirected to the account login
        self.assertRedirects(resp, reverse('accounts:login'))

    def test_create_account_post_invalid(self):
        """Checks if an invalid user was created"""

        # Create data to POST to the server
        post_data = {
            'username': 'new_user',
            'password1': 'password1',
            'password2': 'password2',
        }

        # The user should not have been redirect and should be using the
        # same GET template
        with self.assertTemplateUsed('accounts/create_account.html'):
            self.client.post(
                reverse('accounts:create_account'),
                data=post_data
            )

        # Ensure that we have not created a user
        self.assertEqual(len(User.objects.all()), 1)

    def test_login_user_get(self):
        """Ensures that login_user shows the correct information"""

        with self.assertTemplateUsed('accounts/login.html'):
            resp = self.client.get(reverse('accounts:login'))

        # Check various page information
        self.assertContains(resp, 'Login')
        self.assertContains(resp, 'or create an account')
        self.assertContains(resp, 'Username')

    def test_login_user_post(self):
        """Ensures that a user can be logged in"""

        # Create data to POST to the server
        post_data = {
            'username': 'test_user',
            'password': 'test_password',
        }
        resp = self.client.post(
            reverse('accounts:login'),
            data=post_data
        )

        # We should have been redirected to the site's homepage
        self.assertRedirects(resp, reverse('homepage'))

    def test_login_user_post_invalid(self):
        """Ensures that a user can be logged in"""

        # Create data to POST to the server
        post_data = {
            'username': 'test_user',
            'password': 'bad_password',
        }
        resp = self.client.post(
            reverse('accounts:login'),
            data=post_data
        )

        # Ensures that the user sees the proper error
        self.assertContains(
            resp, 'Please enter a correct username and password.'
        )

    def test_logout_user(self):
        """Ensures that a user can log out"""

        # Log in the test user
        self.client.login(username='test_user', password='test_password')

        resp = self.client.get(reverse('accounts:logout'))

        # Check that we can not find a logged in user
        with self.assertRaises(TypeError):
            # If the user context is not found it will raise a TypeError
            resp.context['user']

        # We should have been redirected to the site's homepage
        self.assertRedirects(resp, reverse('homepage'))
