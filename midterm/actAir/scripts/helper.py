# DO NOT RUN THIS SCRIPT THIS IS JUST A HELPER FUNCTION FOR POPULATE.PY, RUNNING POPULATE.PY WILL AUTOMATICALLY CALL THIS

#Everything below here is my code

#Helper function to seperate data cleaning and database populating funtions

# Import panda to clean and organize the CSV dataset
import pandas as pd

# Transform the dataset from csv to panda dataframes



def clean_dataframe(csv_path):

    df = pd.read_csv(csv_path)
    # Remove rows with null value
    cleaned_df = df.dropna()

    #Original dataframe has 22 columns with some repeated information like datetime, date, and time and some reduntant columns
    # like AQI ones which are some measurements from another source. To stay in the given limit of 10000 we remove this columns

    selected_columns = ['Name', 'GPS', 'DateTime', 'NO2', 'O3_1hr', 'CO', 'PM10 1 hr', 'PM2.5 1 hr']
    cleaned_df = cleaned_df.loc[:, selected_columns ]

    # Convert datetime to only date as we are not interested in hourly air quality report
    cleaned_df['DateTime'] = pd.to_datetime(cleaned_df['DateTime'], format='%d/%m/%Y %I:%M:%S %p')
    cleaned_df['Date'] = cleaned_df['DateTime'].dt.date

    #Group by each date, gps, and name
    cleaned_df = cleaned_df.groupby(['Date', 'GPS', 'Name']).agg({
        'NO2': 'mean', 
        'O3_1hr': 'mean',  
        'CO': 'mean',  
        'PM10 1 hr': 'mean',  
        'PM2.5 1 hr': 'mean',  
    }).reset_index()

    # Using pd.factorize() to convert string values to unique integers
    locations = cleaned_df['Name']
    cleaned_df['location'] = pd.factorize(locations)[0] + 1 
     
    return cleaned_df