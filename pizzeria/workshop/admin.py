from django.contrib import admin

from .models import Crust, Ingredient, Pizza

admin.site.register(Crust)
admin.site.register(Ingredient)
admin.site.register(Pizza)
