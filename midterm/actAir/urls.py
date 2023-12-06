#Everything below here was written by me 

from django.urls import path

from . import api
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('air-quality', api.air_quality, name='air-quality'),
    path('location', api.location, name='location'),
    path('air-quality/location/<int:location_id>', api.latest_air_quality, name='latest-air-quality'),
    path('air-quality/history/<int:location_id>', api.air_quality_history, name='air-quality-history'),
    path('air-quality/average/average', api.air_quality_average, name='air-quality-average'),
    path('air-quality/element/<str:element_name>', api.air_quality_element, name='air-quality-element'),
]