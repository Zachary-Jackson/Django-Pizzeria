from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import IngredientForm, PizzaForm
from .models import Pizza


def create_searching_by_message(searching_by: str):
    """
    Creates a message informing the user how something is being searched

    :param searching_by: A string saying how something is searched
    :return:
        A title cased string in the format of 'Searching: {searching_by}' minus
        any `-` characters
    """
    # remove any `-` characters and title case
    formatted_string = searching_by.replace('-', '').title()

    return f'Searching: {formatted_string}'


""" Views """


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


def workshop_homepage_sorted(request, sorted_by: str):
    """
    Allows the main homepage to be sorted by various conditions

    :param request: Standard Django request object
    :param sorted_by: A string describing how the user wants to sort the Pizzas
    :return: Render 'workshop:homepage.html'
    """
    all_pizzas_query = Pizza.objects.all()

    # Sort all_pizzas_query based upon the sort_by parameter
    all_pizzas = all_pizzas_query.order_by(sorted_by)

    latest_pizzas = all_pizzas_query.order_by('-time_created')[:2]
    searching_by_message = create_searching_by_message(sorted_by)

    return render(
        request,
        'workshop/homepage.html',

        # Send the all_pizza and latest_pizza queryset to the template
        {
            'pizzas': all_pizzas,
            'latest_pizzas': latest_pizzas,
            'searching_by_message': searching_by_message
        }
    )


@login_required
def create_ingredient(request):
    """
    Allows a user to submit a form to create an Ingredient object

    :param request: Standard Django Request Object
    :return if GET request: render 'workshop:create_ingredient'
    :return if successful POST: same as GET, but create an Ingredient
    """
    form = IngredientForm()

    if request.POST:

        # Get the form information from the POST request
        form = IngredientForm(data=request.POST)

        if form.is_valid():
            form.save()

            # Create a message telling the user their Ingredient was created
            ingredient_name = form.cleaned_data['name']
            messages.success(
                request,
                f'A new ingredient {ingredient_name} was created!'
            )

            # By reinstating the form here, we can clear the form from a prior
            # submission. This makes it easy to create many Ingredients.
            form = IngredientForm()

    return render(request, 'workshop/create_ingredient.html', {'form': form})


@login_required
def create_pizza(request):
    """
    Allows a user to submit a form to create a Pizza object

    :param request: Standard Django Request Object
    :return if GET request: render 'workshop:create_pizza'
    :return if successful POST:
        Create a Pizza object and redirect to 'workshop:homepage'
    """
    form = PizzaForm()

    if request.POST:
        form = PizzaForm(data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('workshop:homepage')

    return render(request, 'workshop/create_pizza.html', {'form': form})


@login_required
def delete_pizza(request, pk: int):
    """
    Deletes a pizza and returns the user to the homepage

    :param request: Standard Django request object
    :param pk: Primary key for a Pizza object
    :return: Delete Pizza and redirect to 'workshop:homepage'
    """
    pizza = Pizza.objects.get(pk=pk)

    # Create delete message
    pizza_name = pizza.name
    messages.success(
        request,
        f'{pizza_name} was deleted.'
    )

    pizza.delete()

    return redirect('workshop:homepage')


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


def view_pizza(request, pk: int):
    """
    Allows a user to view a particular pizza

    :param request: Standard Django Request object
    :param pk: Primary key for Pizza object
    :return: render 'workshop/view_pizza.html'
    """
    pizza = Pizza.objects.get(pk=pk)

    return render(request, 'workshop/view_pizza.html', {'pizza': pizza})
