import pandas as pd
import streamlit as st
from Import_Weather_Data import *

# Title
st.title("Microalgae Transparency Model, v0.01")

# Enter the location, city
your_loc = st.text_input("Which city do you want the microalgae culture located? ")

# Test the weather data function
data = import_weather_data_function(your_loc, "2024-07-01", "2024-07-02")

#data is the data for the graph, test
graph_data = pd.DataFrame({"Hourly temperature": data[0]})
table_data = pd.DataFrame({"Optimal Transparency for January": [1], "Optimal Transparency for April": [7], "Optimal Transparency for July": [10], "Optimal Transparency for October": [15]})
# Graph display
st.line_chart(graph_data)

# Table display
st.write(table_data)
