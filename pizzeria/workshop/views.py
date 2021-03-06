from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import IngredientForm, PizzaForm
from .models import Pizza

""" Views """


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

    pizza = get_object_or_404(Pizza, pk=pk)

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
    pizza = get_object_or_404(Pizza, pk=pk)

    # Add one to the Pizza's dislikes and save it
    pizza.dislikes += 1
    pizza.save()

    # Create success message
    create_and_apply_liked_disliked_message(request, pizza.name, False)

    return redirect('workshop:homepage')


@login_required
def like_pizza(request, pk: int):
    """
    Increments by one, the likes associated with a pizza

    :param request: Standard Django Request Object
    :param pk: The PK value of a Pizza Object
    :return: redirect to 'workshop:homepage'
    """
    pizza = get_object_or_404(Pizza, pk=pk)

    # Add one to the Pizza's likes and save it
    pizza.likes += 1
    pizza.save()

    # Create success message
    create_and_apply_liked_disliked_message(request, pizza.name, True)

    return redirect('workshop:homepage')


class UpdatePizza(LoginRequiredMixin, UpdateView):
    """Allows a user to update a Pizza object"""
    model = Pizza
    form_class = PizzaForm
    template_name = 'workshop/update_pizza.html'


def view_pizza(request, pk: int):
    """
    Allows a user to view a particular pizza

    :param request: Standard Django Request object
    :param pk: Primary key for Pizza object
    :return: render 'workshop/view_pizza.html'
    """
    pizza = get_object_or_404(Pizza, pk=pk)

    return render(request, 'workshop/view_pizza.html', {'pizza': pizza})


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
    :return if valid: Render 'workshop:homepage.html'
    """
    # Ensure that the sorted by string is correct or raise 404
    validate_sorted_by_string_or_404(sorted_by)

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


"""Functions"""


def create_and_apply_liked_disliked_message(request, name: str, liked: bool):
    """
    Creates a django message and applies it

    :param request: Standard Django request object
    :param name: The name of the liked/disliked object
    :param liked: Whether or not the object was liked or disliked
    """

    if liked:
        message = f'You have liked the Pizza: {name}.'
    else:
        message = f'{name}: has been disliked.'

    messages.success(request, message)


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


def validate_sorted_by_string_or_404(sorted_by: str):
    """
    Ensures that searching_by is a valid option

    :param sorted_by: A string saying how something is searched
    :return if valid: boolean stating True
    :return if False: HTTP 404
    """
    valid_options = ['state', '-likes', '-dislikes']

    if sorted_by in valid_options:
        return True
    raise Http404('The search requested can not be found.')
