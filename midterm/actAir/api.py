#Everything below here was written by me 


from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from django.db.models import Avg
from .models import *
from .serializers import *
from datetime import datetime

@api_view(['GET', 'POST'])

def air_quality(request):
    #POST request handling
    if request.method == 'POST':
        serializer = MeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #Check if there is measurement object at all
    try: 
        measurements = Measurement.objects.all()
    except Exception as e:
        return Response(e, status=status.HTTP_404_NOT_FOUND)
    #GET request handling
    if request.method == 'GET':
        serializer = MeasurementSerializer(measurements, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])

def location(request):

    #POST request handling
    if request.method == 'POST':
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #Check if there is location object at all
    try: 
        locations = Location.objects.all()
    except Exception as e:
        return Response(e, status=status.HTTP_404_NOT_FOUND)
    #GET request handling
    if request.method == 'GET':
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
    

@api_view(['GET'])

def latest_air_quality(request, location_id):

    #Exception handling
    try:
        #Try to find latest measurement according to DateTime column with given location id
        latest_measurement = Measurement.objects.filter(location_id=location_id).latest('DateTime')
        #If there is one serialize the measurement and display it
        serializer = MeasurementSerializer(latest_measurement)
        return Response(serializer.data)
    #If there is any other exceptions
    except Exception as e:
        msg = str(e)
        return Response(msg, status=status.HTTP_404_NOT_FOUND)

    
    

@api_view(['GET'])

def air_quality_average(request):

    #Get dates to find average
    start_date_param = request.query_params.get('start_date')
    end_date_param = request.query_params.get('end_date')

    if start_date_param and end_date_param:
        try:
            #Convert string into datetime type
            start_date = datetime.strptime(start_date_param, '%Y%m%d').date()
            end_date = datetime.strptime(end_date_param, '%Y%m%d').date()

            #Exception when user try to insert start date earlier than end date
            if start_date > end_date:
                raise Exception('Start date must be older than end date')
            
            #Exception when user try to enter start date older than recorded dataset 
            oldest_recorded_date = Measurement.objects.earliest("DateTime").DateTime
            if start_date <  oldest_recorded_date:
                raise Exception('Start date must be older than' + ' ' + oldest_recorded_date.strftime('%Y%m%d'))
            
            #Exception when user try to enter end date earlier than recorded dataset 
            earliest_recorded_date = Measurement.objects.latest("DateTime").DateTime
            if end_date >  earliest_recorded_date:
                raise Exception('Start date must be older than' + ' ' + earliest_recorded_date.strftime('%Y%m%d'))
            
            # Query measurements within the specified date range
            measurements = Measurement.objects.filter(DateTime__gte=start_date, DateTime__lte=end_date)

            # Calculate average values for CO2, NO2, O3, PM10, PM2_5
            average_values = measurements.aggregate(
                avg_CO2=Avg('CO2'),
                avg_NO2=Avg('NO2'),
                avg_O3=Avg('O3'),
                avg_PM10=Avg('PM10'),
                avg_PM2_5=Avg('PM2_5')
            )

            return Response(average_values)
        except Exception as e:
            msg = str(e) 
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])

def air_quality_history(request, location_id):

    date_param = request.query_params.get('date')

    if date_param:
        try:
            # Convert the date string from the query parameters to a datetime object
            formatted_date = datetime.strptime(date_param, '%Y%m%d').date()
            
            # Query measurements for the given date and location_id
            measurement = Measurement.objects.filter(DateTime=formatted_date, location_id=location_id)

            # Raise error if there is no measurement with given query
            if measurement:
                pass
            else:
                raise Exception("No measurement with given date and location")
            #If there is one serialize the measurement and display it
            serializer = MeasurementSerializer(measurement, many=True)
            return Response(serializer.data)
        #If there is any other exceptions
        except Exception as e:
            msg = str(e)
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

    


@api_view(['GET'])
   
def air_quality_element(request, element_name):

    #Get dates to find element values
    start_date_param = request.query_params.get('start_date')
    end_date_param = request.query_params.get('end_date')

    if start_date_param and end_date_param:
        try:
            #Convert string into datetime type
            start_date = datetime.strptime(start_date_param, '%Y%m%d').date()
            end_date = datetime.strptime(end_date_param, '%Y%m%d').date()

            #Exception when user try to insert start date earlier than end date
            if start_date > end_date:
                raise Exception('Start date must be older than end date')
            
            #Exception when user try to enter start date older than recorded dataset 
            oldest_recorded_date = Measurement.objects.earliest("DateTime").DateTime
            if start_date <  oldest_recorded_date:
                raise Exception('Start date must be older than' + ' ' + oldest_recorded_date.strftime('%Y%m%d'))
            
            #Exception when user try to enter end date earlier than recorded dataset 
            earliest_recorded_date = Measurement.objects.latest("DateTime").DateTime
            if end_date >  earliest_recorded_date:
                raise Exception('Start date must be older than' + ' ' + earliest_recorded_date.strftime('%Y%m%d'))
            
            # Query measurements within the specified date range and get given element
            measurements = Measurement.objects.filter(DateTime__gte=start_date, DateTime__lte=end_date)

            # Retrieve only the element field values
            values = list(measurements.values_list(element_name, flat=True))
            return Response({element_name: values})
        
        except Exception as e:
            msg = str(e) 
            return Response(msg, status=status.HTTP_404_NOT_FOUND)