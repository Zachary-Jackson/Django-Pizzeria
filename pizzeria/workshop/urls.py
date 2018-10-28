from django.urls import path

from . import views

app_name = 'workshop'

urlpatterns = [
    path('', views.workshop_homepage, name='homepage'),
    path(
        'sorted_by/<str:sorted_by>',
        views.workshop_homepage_sorted,
        name='homepage_sorted'
    ),
    path(
        'create_ingredient/',
        views.create_ingredient,
        name='create_ingredient'
    ),
    path(
        'create_pizza/',
        views.create_pizza,
        name='create_pizza'
    ),
    path('delete/<int:pk>', views.delete_pizza, name='delete_pizza'),
    path('dislike_pizza/<int:pk>', views.dislike_pizza, name='dislike_pizza'),
    path('like_pizza/<int:pk>', views.like_pizza, name='like_pizza'),
    path('view/<int:pk>', views.view_pizza, name='view_pizza'),
]
