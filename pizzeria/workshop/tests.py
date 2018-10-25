from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Ingredient, Pizza


class WorkShopTests(TestCase):
    """Tests for the WorkShop app"""

    def setUp(self):
        """Creates a User for testing"""

        self.test_user = User.objects.create_user(
            email='test@test.com',
            username='test_user',
            password='test_password'
        )

        # Create some ingredients for testing
        self.ingredient = Ingredient.objects.create(name='olives')
        self.ingredient_2 = Ingredient.objects.create(name='peperoni')

        self.pizza = Pizza.objects.create(
            city='Knoxville',
            state='TN',
            likes=5,
            dislikes=1,
            crust='thin',
            name='The Knoxvillian',
            summary='The Knoxville style pizza.'
        )

        # M2M objects must be added after creation
        self.pizza.ingredients.add(self.ingredient, self.ingredient_2)

    def test_homepage_get(self):
        """Ensures that create_account shows the correct information"""

        # Check if the correct template was used
        with self.assertTemplateUsed('workshop/homepage.html'):

            # Create a response object from information given by the server
            resp = self.client.get(reverse('workshop:homepage'))

        # Check various page information
        self.assertContains(resp, 'Pizzas')
        self.assertContains(resp, 'Latest Creations')
        self.assertContains(resp, 'The finest of cuisines')

        # Ensures the Pizza object was loaded to the page
        self.assertContains(resp, 'The Knoxvillian')
        self.assertContains(resp, 'Knoxville, TN')
        self.assertContains(resp, '5')
        self.assertContains(resp, 'The Knoxville style pizza.')

    def test_dislike_pizza(self):
        """Ensures that a pizza can be disliked"""

        # Log in the test user
        self.client.login(username='test_user', password='test_password')

        resp = self.client.get(
            reverse('workshop:dislike_pizza', kwargs={'pk': 1})
        )

        # Refresh the Pizza object by getting a new copy
        # Then ensure that the dislikes was updated
        pizza = Pizza.objects.get(pk=1)
        self.assertEqual(2, pizza.dislikes)

        # The user should have been redirected
        self.assertRedirects(resp, reverse('workshop:homepage'))

    def test_like_pizza(self):
        """Ensures that a pizza can be liked"""

        self.client.login(username='test_user', password='test_password')

        resp = self.client.get(
            reverse('workshop:like_pizza', kwargs={'pk': 1})
        )

        # Refresh the Pizza object by getting a new copy
        # Then ensure that the likes was updated
        pizza = Pizza.objects.get(pk=1)
        self.assertEqual(6, pizza.likes)

        # The user should have been redirected
        self.assertRedirects(resp, reverse('workshop:homepage'))


