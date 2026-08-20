#Function that recovers the hourly weather data (air temperature, relative humidity,  dew point, wind speed, diffuse and direct sunlight) 
#for a location (a city, your_loc) between one day (start_date) to the other (end_date)


import openmeteo_requests
import pandas as pd
import numpy as np


import requests_cache
from retry_requests import retry

from geopy.geocoders import Nominatim

def import_location_data(your_loc):
    # Instantiate a new Nominatim client
    app = Nominatim(user_agent="tutorial")

    if app.geocode(your_loc) is None:
        return None, None
    else:
        location = app.geocode(your_loc).raw
    
        latitude = location.get('lat')
        longitude = location.get('lon')
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)
    return latitude, longitude

def import_weather_data_function(latitude, longitude, start_date, end_date):
    

        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
        	"latitude": latitude,
        	"longitude": longitude,
        	"start_date": start_date,
        	"end_date": end_date,
        	"hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "wind_speed_10m", "diffuse_radiation", "direct_radiation"],
        	"timezone": "auto"
        }
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
        hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
        hourly_wind_speed_10m = hourly.Variables(3).ValuesAsNumpy()
        hourly_diffuse_radiation = hourly.Variables(4).ValuesAsNumpy() #W/m2
        hourly_direct_radiation = hourly.Variables(5).ValuesAsNumpy() #W/m2
    
    
        hourly_data = {"date": pd.date_range(
        	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        	freq = pd.Timedelta(seconds = hourly.Interval()),
        	inclusive = "left"
        )}
        
        
        return hourly_temperature_2m, hourly_relative_humidity_2m, hourly_dew_point_2m, hourly_wind_speed_10m, hourly_diffuse_radiation , hourly_direct_radiation
