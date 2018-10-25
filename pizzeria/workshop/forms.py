from django import forms

from . import models

STATES = [
    ('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'),
    ('CO', 'CO'), ('CT', 'CT'), ('DC', 'DC'), ('DE', 'DE'), ('FL', 'FL'),
    ('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'),
    ('IA', 'IA'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'),
    ('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'), ('MS', 'MS'),
    ('MO', 'MO'), ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'),
    ('NJ', 'NJ'), ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'), ('ND', 'ND'),
    ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'),
    ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'),
    ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'),
    ('WY', 'WY')
]


class IngredientForm(forms.ModelForm):
    """Form allowing a new Ingredient to be created"""

    class Meta:
        """Defines the model the form uses and what fields to use"""
        model = models.Ingredient
        fields = ['name']

    def clean_name(self):
        """Over-ride the value for name and title case it"""
        name = self.cleaned_data['name']
        return name.title()


class PizzaForm(forms.ModelForm):
    """Form allowing a new Pizza object to be created"""

    class Meta:
        """Defines the model the form uses and what fields to use"""
        model = models.Pizza
        fields = ['city', 'state', 'crust', 'ingredients', 'name', 'summary']

        # Over-ride the State field to be a state selector
        widgets = {'state': forms.Select(choices=STATES)}

