from django.shortcuts import render


def project_homepage(request):
    """
    The main homepage for the pizzeria project

    :param request: Standard Django request object
    :return: Render 'homepage.html'
    """

    return render(request, 'homepage.html',)
