import pandas as pd
from Import_Weather_Data import *

# Title
st.title("Microalgae Transparency Model, v0.01")

# Enter the location, city
your_loc = st.text_input("Which city do you want the microalgae culture located? ")

# Test the weather data function
data = import_weather_data_function(your_loc, "2024-07-01", "2024-07-02")

#data is the data for the graph, test
graph_data = pd.DataFrame({"x": range(0,48), "y": data[0]})

# Graph display
st.line_chart(graph_data)
