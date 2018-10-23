from django.db import models


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
    likes = models.IntegerField()
    dislikes = models.IntegerField()

    # Pizza properties
    crust = models.CharField(max_length=20)
    ingredients = models.ManyToManyField('Ingredient')
    name = models.CharField(max_length=40)

    # Miscellaneous
    summary = models.CharField(max_length=200)
    time_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Defines how a Pizza object is displayed

        :return: The Pizza's name attribute
        """
        return self.name
