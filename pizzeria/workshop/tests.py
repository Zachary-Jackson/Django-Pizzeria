from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Crust, Ingredient, Pizza


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
        self.ingredient = Ingredient.objects.create(name='Pineapple')
        self.ingredient_2 = Ingredient.objects.create(name='Sausage')
        self.crust = Crust.objects.create(type='Extra Thin')

        self.pizza = Pizza.objects.create(
            city='Knoxville',
            state='TN',
            likes=5,
            dislikes=1,
            crust=self.crust,
            name='The Knoxvillian',
            summary='The Knoxville style pizza.',
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

    def test_create_ingredient_get(self):
        """Checks that create_ingredient looks correctly"""

        self.client.login(username='test_user', password='test_password')

        with self.assertTemplateUsed('workshop/create_ingredient.html'):
            resp = self.client.get(reverse('workshop:create_ingredient'))

        # Checks that the page and form looks good
        self.assertContains(resp, 'New Ingredient')
        self.assertContains(resp, 'Name')
        self.assertContains(resp, 'Create')

    def test_create_ingredient_post(self):
        """Ensures that the user can create an Ingredient"""

        self.client.login(username='test_user', password='test_password')

        # Create data to POST to the server
        post_data = {
            'name': 'Jelly Bean',
        }
        self.client.post(
            reverse('workshop:create_ingredient'),
            data=post_data
        )

        # Check the last Ingredient object to see if it matches the POSTed data
        ingredient = Ingredient.objects.last()
        self.assertEqual('Jelly Bean', ingredient.name)

    def test_create_pizza_get(self):
        """Checks that create_pizza looks correctly"""

        self.client.login(username='test_user', password='test_password')

        with self.assertTemplateUsed('workshop/create_pizza.html'):
            resp = self.client.get(reverse('workshop:create_pizza'))

        # Checks that the page looks good
        self.assertContains(resp, 'Create Pizza')
        self.assertContains(resp, 'or Ingredient')
        self.assertContains(resp, 'Create')

    def test_create_pizza_post(self):
        """Ensures that the user can create a Pizza"""

        self.client.login(username='test_user', password='test_password')

        # Create data to POST to the server
        post_data = {
            'name': 'Pineapple and pepperoni',
            'city': 'Olive',
            'state': 'NY',
            'crust': 1,  # ForeignKeys Get added by ID numbers
            'ingredients': [1, 2],  # Many to Many fields get added by ID
            'summary': 'Is this a real town?'
        }
        resp = self.client.post(
            reverse('workshop:create_pizza'),
            data=post_data
        )

        # Check the last Ingredient object to see if it matches the POSTed data
        pizza = Pizza.objects.last()
        self.assertEqual('Pineapple and pepperoni', pizza.name)

        # The user should have been redirected
        self.assertRedirects(resp, reverse('workshop:homepage'))

    def test_delete_pizza(self):
        """Checks if a user can delete a pizza"""

        self.client.login(username='test_user', password='test_password')

        resp = self.client.get(
            reverse('workshop:delete_pizza', kwargs={'pk': 1})
        )

        # Ensure that no Pizzas are in the database
        self.assertEqual(0, len(Pizza.objects.all()))

        # The user should have been redirect to the homepage
        self.assertRedirects(resp, reverse('workshop:homepage'))

    def test_view_pizza_get(self):
        """Checks how the page looks for a user"""

        resp = self.client.get(
            reverse('workshop:view_pizza', kwargs={'pk': 1})
        )

        # All of the Pizza information should have been loaded to the page
        self.assertContains(resp, 'Knoxville, TN')
        self.assertContains(resp, 'Summary: The Knoxville style pizza.')
        self.assertContains(resp, 'Crust: Extra Thin')
        self.assertContains(resp, 'Ingredients: Pineapple, Sausage')
        self.assertContains(resp, 'Likes: 5')
        self.assertContains(resp, 'Dislikes: 1')
