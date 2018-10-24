from django import forms

from . import models


class IngredientForm(forms.ModelForm):
    """Form allowing a new Ingredient to be created"""

    class Meta:
        """Defines the model the form uses and what fields to use"""
        model = models.Ingredient
        fields = ['name']
