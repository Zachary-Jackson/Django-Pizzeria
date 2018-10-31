from django.db import models
from django.urls import reverse


class Crust(models.Model):
    """Model representing a Pizza's Crust"""

    type = models.CharField(max_length=30, unique=True)

    def __str__(self):
        """
        Defines how a Crust object is displayed

        :return: The Crust's type attribute
        """
        return self.type


class Ingredient(models.Model):
    """Ingredients for some sort of food"""

    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        """
        Defines how an Ingredient object is displayed

        :return: The Ingredient's name attribute
        """
        return self.name


class Pizza(models.Model):
    """An object representing a pizza"""

    # Location information
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)

    # Media status
    likes = models.IntegerField(blank=True, default=0)
    dislikes = models.IntegerField(blank=True, default=0)

    # Pizza properties
    crust = models.ForeignKey('Crust', on_delete='cascade')
    ingredients = models.ManyToManyField('Ingredient')
    name = models.CharField(max_length=40, unique=True)

    # Miscellaneous
    summary = models.CharField(max_length=200)
    time_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        """Determines where a Pizza object's 'homepage' is"""
        return reverse('workshop:view_pizza', args=(self.id,))

    def __str__(self):
        """
        Defines how a Pizza object is displayed

        :return: The Pizza's name attribute
        """
        return self.name
