from django.contrib import admin

from .models import Ingredient, Pizza

admin.site.register(Ingredient)
admin.site.register(Pizza)
