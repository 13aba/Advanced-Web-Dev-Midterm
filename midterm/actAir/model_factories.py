#Everything below here are written by me 

import factory
from django.test import TestCase
from django.conf import settings
from django.core.files import File
import datetime
from .models import *


class LocationFactory(factory.django.DjangoModelFactory):
    location_name = 'London'
    gps = '51.5072, 0.1276'

    class Meta:
        model = Location


class MeasurementFactory(factory.django.DjangoModelFactory):
    CO2 = '0.05'
    NO2 = '0.02'
    O3 = '0.03'
    PM10 = '0.09'
    PM2_5 = '5'
    DateTime = factory.Faker('date_object')
    location = factory.SubFactory(LocationFactory)

    class Meta: 
        model = Measurement