import pandas as pd
import streamlit as st
from Import_Weather_Data import *
from Culture_Temperature import *
from Biomass_Production import *
from Parameter_Values import *
year = 2025
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
# Define the start and end dates for the entire year
start_date = f"{year}-01-01"
end_date = f"{year}-12-31"

# Use the mock function to import the weather data for the entire year
weather_data = import_weather_data_function(your_loc, start_date, end_date)

# Define the number of months and hours
num_months = 12
num_hours = 24  # 24 hours in a day

# Initialize NumPy arrays to store the hourly averages
temperature_avg = np.zeros((num_months, num_hours))
humidity_avg = np.zeros((num_months, num_hours))
dew_point_avg = np.zeros((num_months, num_hours))
wind_speed_avg = np.zeros((num_months, num_hours))
diffuse_rad_avg = np.zeros((num_months, num_hours))
direct_rad_avg = np.zeros((num_months, num_hours))
PAR_avg = np.zeros((num_months, num_hours))


# Calculation of the hourly aevrage for each month
# Loop over each month
for month in range(1, num_months + 1):
    # Get the number of days in the month
    num_days_in_month = calendar.monthrange(year, month)[1]

    # Calculate the start and end indices for the current month
    start_index = sum(calendar.monthrange(year, m)[1] for m in range(1, month)) * 24
    end_index = start_index + num_days_in_month * 24

    # Extract the data for the current month
    monthly_data = [d[start_index:end_index] for d in weather_data]

    # Calculate the hourly averages and store them in the NumPy arrays
    temperature_avg[month - 1, :] = calculate_hourly_averages(monthly_data[0])
    humidity_avg[month - 1, :] = calculate_hourly_averages(monthly_data[1])
    dew_point_avg[month - 1, :] = calculate_hourly_averages(monthly_data[2])
    wind_speed_avg[month - 1, :] = calculate_hourly_averages(monthly_data[3])
    diffuse_rad_avg[month - 1, :] = calculate_hourly_averages(monthly_data[4])
    direct_rad_avg[month - 1, :] = calculate_hourly_averages(monthly_data[5])
    PAR_avg[month - 1, :] = calculate_hourly_averages(2.15 * (monthly_data[4] + monthly_data[5]))


#data is the data for the graph, test
graph_data = pd.DataFrame({"Average Hourly temperature for January": temperature_avg[0,:]})
table_data = pd.DataFrame({"Optimal Transparency for January": [1], "Optimal Transparency for April": [7], "Optimal Transparency for July": [10], "Optimal Transparency for October": [15]})


# Graph display
st.line_chart(graph_data)

# Table display
st.write(table_data)

