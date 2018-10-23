from django.urls import path

from . import views

app_name = 'workshop'

urlpatterns = [
    path('', views.workshop_homepage, name='homepage'),
    path('dislike_pizza/<int:pk>', views.dislike_pizza, name='dislike_pizza'),
    path('like_pizza/<int:pk>', views.like_pizza, name='like_pizza'),
]