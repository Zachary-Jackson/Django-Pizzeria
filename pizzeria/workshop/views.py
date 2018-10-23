from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Pizza


def workshop_homepage(request):
    """
    The main homepage for the pizzeria project

    :param request: Standard Django request object
    :return: Render 'workshop:homepage.html'
    """

    all_pizzas = Pizza.objects.all()

    # Sort all_pizzas by the newest time created and grab the first two
    latest_pizzas = all_pizzas.order_by('-time_created')[:2]

    return render(
        request,
        'workshop/homepage.html',

        # Send the all_pizza and latest_pizza queryset to the template
        {'pizzas': all_pizzas, 'latest_pizzas': latest_pizzas}
    )


@login_required
def dislike_pizza(request, pk: int):
    """
    Increments by one, the dislikes associated with a pizza

    :param request: Standard Django Request Object
    :param pk: The PK value of a Pizza Object
    :return: redirect to 'workshop:homepage'
    """

    pizza = Pizza.objects.get(pk=pk)

    # Add one to the Pizza's dislikes and save it
    pizza.dislikes += 1
    pizza.save()

    return redirect('workshop:homepage')


@login_required
def like_pizza(request, pk: int):
    """
    Increments by one, the likes associated with a pizza

    :param request: Standard Django Request Object
    :param pk: The PK value of a Pizza Object
    :return: redirect to 'workshop:homepage'
    """

    pizza = Pizza.objects.get(pk=pk)

    # Add one to the Pizza's likes and save it
    pizza.likes += 1
    pizza.save()

    return redirect('workshop:homepage')

