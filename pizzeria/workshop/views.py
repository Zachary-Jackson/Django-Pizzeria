from django.shortcuts import render

from .models import Pizza


def workshop_homepage(request):
    """
    The main homepage for the pizzeria project

    :param request: Standard Django request object
    :return: Render 'workshop:homepage.html'
    """

    all_pizzas = Pizza.objects.all()

    return render(request, 'workshop/homepage.html', {'pizzas': all_pizzas})
