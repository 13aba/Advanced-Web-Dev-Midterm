from django.test import TestCase

# Create your tests here.

#Everything below written by me

import json
from datetime import date
from django.urls import reverse
from django.urls import reverse_lazy
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

class AirQualityTest(APITestCase):

    def setUp(self):
        #Create fake datas in the model
        self.start_date = date(2022, 5, 26)
        self.end_date = date(2022, 5, 27)
        CO2_measurements = [1, 2]
        measurement1 = MeasurementFactory.create(pk=1, CO2=CO2_measurements[0], DateTime=self.start_date)
        measurement2 = MeasurementFactory.create(pk=2, CO2=CO2_measurements[1], DateTime=self.end_date)

    def tearDown(self):
        #Delete all fake models when test end
        Measurement.objects.all().delete()
        Location.objects.all().delete()
        MeasurementFactory.reset_sequence(0)
        LocationFactory.reset_sequence(0)

    #Testing air-quality API
    def test_AirQualityReturnsSuccess(self):
        url = reverse('air-quality')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    #Testing location API
    def test_LocationReturnsSuccess(self):
        url = reverse('location')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    #Testing air-quality/location/<int:location_id> API
    def test_LatestReturnsSuccess(self):
        url = reverse('latest-air-quality', kwargs={'location_id':1})
        response = self.client.get(url)
        #Parse the response content into dictionary so we can check if content is correct
        parsed = json.loads(response.content)
        self.assertEqual(parsed['id'], 1)

    #Testing air-quality/history/<int:location_id> API
    def test_HistoryReturnsSuccess(self):
        url = reverse('air-quality-history', kwargs={'location_id':1})
        date_param = '20220526'
        response = self.client.get(f'{url}?date={date_param}')
        #Parse the response content into dictionary so we can check if content is correct
        parsed = json.loads(response.content)
        #First object must be our measurement1 object which has id 1
        self.assertEqual(parsed[0]['id'], 1)

    def test_HistoryReturnsError(self):
        url = reverse('air-quality-history', kwargs={'location_id':1})
        #Date parameter thats not in our database
        date_param = '20250826'
        response = self.client.get(f'{url}?date={date_param}')
        #Check if API is returning 404 not found error
        self.assertEqual(response.status_code, 404)

    def test_AverageReturnsSuccess(self):
        url = reverse('air-quality-average')
        #Date parameter thats not in our database
        start_date = '20220526'
        end_date = '20220527'
        response = self.client.get(f'{url}?start_date={start_date}&end_date={end_date}')
        #Parse the response content into dictionary so we can check if content is correct
        parsed = json.loads(response.content)
        #Average CO2 must be equal to 1.5 as we entered 1 and 2 as CO2 when creating fake measurements
        self.assertEqual(parsed['avg_CO2'], 1.5)

    def test_ElementReturnsSuccess(self):
        #Get url with element id as CO2
        url = reverse('air-quality-element', kwargs={'element_name': "CO2"})
        #Date parameter thats not in our database
        start_date = '20220526'
        end_date = '20220527'
        response = self.client.get(f'{url}?start_date={start_date}&end_date={end_date}')
        #Parse the response content into dictionary so we can check if content is correct
        parsed = json.loads(response.content)
        #Get the CO2 measurements from the parsed content
        CO2_API = parsed["CO2"]
        #Check if API returned array is same as ours
        self.assertEqual(CO2_API[0], 1)
        self.assertEqual(CO2_API[1], 2)
    
    
    
    


    
