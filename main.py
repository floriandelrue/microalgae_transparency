import pandas as pd
import streamlit as st
from Import_Weather_Data import *
from Culture_Temperature import *
from Biomass_production import *
from Parameter_Values import *

# Function to calculate the hourly average
def calculate_hourly_averages(data):
  if data is None:
    return np.zeros(24)
  hourly_averages = np.zeros(24)
  for i in range(24):
    hourly_averages[i] = np.mean(data[i::24])
  return hourly_averages
# Title
st.title("Microalgae Transparency Model, v0.01")

# Enter the location, city
your_loc = st.text_input("Which city do you want the microalgae culture located? ")

# Import the weather data
jan_data_extended = import_weather_data_function(your_loc, "2023-12-15", "2025-01-31") 
apr_data_extended = import_weather_data_function(your_loc, "2025-03-15", "2025-04-30") 
jul_data_extended = import_weather_data_function(your_loc, "2025-06-15", "2025-07-31") 
oct_data_extended = import_weather_data_function(your_loc, "2025-09-15", "2025-10-31") 

jan_data = import_weather_data_function(your_loc, "2025-01-01", "2025-01-31") 
apr_data = import_weather_data_function(your_loc, "2025-04-01", "2025-04-30") 
jul_data = import_weather_data_function(your_loc, "2025-07-01", "2025-07-31") 
oct_data = import_weather_data_function(your_loc, "2025-10-01", "2025-10-31") 

# Calculation of the hourly aevrage for each month
jan_temperature_avg = calculate_hourly_averages(jan_data[0])
jan_humidity_avg = calculate_hourly_averages(jan_data[1])
jan_dew_point_avg = calculate_hourly_averages(jan_data[2])
jan_wind_speed_avg = calculate_hourly_averages(jan_data[3])
jan_diffuse_rad_avg = calculate_hourly_averages(jan_data[4])
jan_direct_rad_avg = calculate_hourly_averages(jan_data[5])
jan_PAR_avg = calculate_hourly_averages(2.15*(jan_data[4] + jan_data[5]))

apr_temperature_avg = calculate_hourly_averages(apr_data[0])
apr_humidity_avg = calculate_hourly_averages(apr_data[1])
apr_dew_point_avg = calculate_hourly_averages(apr_data[2])
apr_wind_speed_avg = calculate_hourly_averages(apr_data[3])
apr_diffuse_rad_avg = calculate_hourly_averages(apr_data[4])
apr_direct_rad_avg = calculate_hourly_averages(apr_data[5])
apr_PAR_avg = calculate_hourly_averages(2.15*(apr_data[4] + apr_data[5]))

jul_temperature_avg = calculate_hourly_averages(jul_data[0])
jul_humidity_avg = calculate_hourly_averages(jul_data[1])
jul_dew_point_avg = calculate_hourly_averages(jul_data[2])
jul_wind_speed_avg = calculate_hourly_averages(jul_data[3])
jul_diffuse_rad_avg = calculate_hourly_averages(jul_data[4])
jul_direct_rad_avg = calculate_hourly_averages(jul_data[5])
jul_PAR_avg = calculate_hourly_averages(2.15*(jul_data[4] + jul_data[5]))

oct_temperature_avg = calculate_hourly_averages(oct_data[0])
oct_humidity_avg = calculate_hourly_averages(oct_data[1])
oct_dew_point_avg = calculate_hourly_averages(oct_data[2])
oct_wind_speed_avg = calculate_hourly_averages(oct_data[3])
oct_diffuse_rad_avg = calculate_hourly_averages(oct_data[4])
oct_direct_rad_avg = calculate_hourly_averages(oct_data[5])
oct_PAR_avg = calculate_hourly_averages(2.15*(oct_data[4] + oct_data[5]))

#data is the data for the graph, test
graph_data = pd.DataFrame({"Average Hourly temperature for January": jan_temperature_avg})
table_data = pd.DataFrame({"Optimal Transparency for January": [1], "Optimal Transparency for April": [7], "Optimal Transparency for July": [10], "Optimal Transparency for October": [15]})


# Graph display
st.line_chart(graph_data)

# Table display
st.write(table_data)

