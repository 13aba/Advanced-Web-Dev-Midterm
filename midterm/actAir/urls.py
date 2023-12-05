#Everything below here was written by me 

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index')
]