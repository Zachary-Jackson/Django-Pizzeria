from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

# Create your views here.


def create_account(request):
    """
    Allows a site user to create a new account using the UserCreationForm

    :param request: Standard Django request object
    :return if GET request: render 'accounts/create_account.html'
    :return if successful POST: return redirect 'accounts:create_account'
    """
    # If the HTTP method is POST we check the form for validity
    if request.method == 'POST':
        form = UserCreationForm(data = request.POST)

        # If the form is valid, save the form and preform a redirect
        if form.is_valid():
            form.save()
            return redirect('accounts:login')

    form = UserCreationForm
    return render(request, 'accounts/create_account.html', {'form': form})


def login_user(request):
    """
    Allows a user to login to the site with valid credentials

    :param request: Standard Django request object
    :return if GET request: render 'accounts:login'
    :return if successful POST request: return redirect 'homepage'
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('homepage')

    form = AuthenticationForm
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_user(request):
    """
    Allows a logged in user to logout

    :param request: Standard Django Request object
    :return: return render redirect 'homepage'
    """
    # Log the user out and redirect them to the homepage
    logout(request)
    return redirect('homepage')
