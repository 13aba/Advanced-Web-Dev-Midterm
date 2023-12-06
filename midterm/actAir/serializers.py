#Everything below is written by me

from rest_framework import serializers
from .models import *

#Location serializer
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

#Measurement serializer
class MeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measurement
        fields = '__all__'



