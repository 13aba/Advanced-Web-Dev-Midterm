#Every code below here are my own

# RUN THIS CODE TO POPULATE THE DATABASE

import sys
import os 

import django
from django.db import IntegrityError


#import helper function
from helper import clean_dataframe


# Getting path to midterm folder path using dirname since midterm is three folder from this script
app_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#Path to csv file
csv_path = os.path.join(app_path, "Air_Quality_Monitoring_Data.csv")

sys.path.append(app_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "midterm.settings")
django.setup()

#import django models
from actAir.models import *


#Create cleaned dataframe using helper function
clean_df = clean_dataframe(csv_path)

#Delete all previous data in the models
Measurement.objects.all().delete()
Location.objects.all().delete()

#location dataframe 
loc_df = clean_df.drop_duplicates(subset = "location")

# Convert DataFrame rows into list of Location model instances
for index, row in loc_df.iterrows():
    #exception handling
    try:
        # Creating and saving instances individually for each location
        instance = Location(
            id=row['location'],  # Assigning the ID from the DataFrame
            location_name=row['Name'], 
            gps=row['GPS']
        )
        instance.save()
    except Exception as e:
        print(f"An error occurred for ID {row['location']}: {e}")
        # Handle potential exceptions

# Convert DataFrame rows into list of measurement model instances
instances_to_create = [
    Measurement(
        CO2=row['CO'],
        O3=row['O3_1hr'],
        NO2=row['NO2'],
        PM10=row['PM10 1 hr'],
        PM2_5=row['PM2.5 1 hr'],
        DateTime=row['Date'],
        location=Location.objects.get(id=row['location'])
    )
    for _, row in clean_df.iterrows()
]

try:
    # Bulk create the instances
    Measurement.objects.bulk_create(instances_to_create)
except IntegrityError as e:
    # Handle IntegrityError (or any other specific exceptions if needed)
    print(f"IntegrityError occurred: {e}")
except Exception as e:
    # Handle other potential exceptions
    print(f"An error occurred: {e}")





