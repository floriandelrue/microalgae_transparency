import pandas as pd
import streamlit as st
import calendar
from Import_Weather_Data import *
from Culture_Temperature import *
from Biomass_Production import *
from Parameter_Values import *
import matplotlib.pyplot as plt

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


#Sidebar for model parameters values




# Function to update parameters
def update_params(
    new_Ea, new_depth, new_X_initial, new_T_min, new_T_opt, new_T_max, new_P_max,
    new_alpha, new_I_opt, new_kT, new_kI, new_K, new_C, new_biomass_loss_night_temp2,
    new_biomass_loss_night_temp, new_biomass_loss_night_cst, new_culture_absorptivity,
    new_culture_depth, new_culture_dz, new_nb_layer, new_C_p, new_rho, new_sigma,
    new_e_w, new_A_evap, new_B_evap, new_A_conv, new_B_conv
):
    global Ea, depth, X_initial, T_min, T_opt, T_max, P_max, alpha, I_opt, kT, kI, K, C, \
        biomass_loss_night_temp2, biomass_loss_night_temp, biomass_loss_night_cst, \
        culture_absorptivity, culture_depth, culture_dz, nb_layer, C_p, rho, sigma, \
        e_w, A_evap, B_evap, A_conv, B_conv
    Ea = new_Ea
    depth = new_depth
    X_initial = new_X_initial
    T_min = new_T_min
    T_opt = new_T_opt
    T_max = new_T_max
    P_max = new_P_max
    alpha = new_alpha
    I_opt = new_I_opt
    kT = new_kT
    kI = new_kI
    K = new_K
    C = new_C
    biomass_loss_night_temp2 = new_biomass_loss_night_temp2
    biomass_loss_night_temp = new_biomass_loss_night_temp
    biomass_loss_night_cst = new_biomass_loss_night_cst
    culture_absorptivity = new_culture_absorptivity
    culture_depth = new_culture_depth
    culture_dz = new_culture_dz
    nb_layer = new_nb_layer
    C_p = new_C_p
    rho = new_rho
    sigma = new_sigma
    e_w = new_e_w
    A_evap = new_A_evap
    B_evap = new_B_evap
    A_conv = new_A_conv
    B_conv = new_B_conv
    global z
    z = np.linspace(0, depth, num=100)
    z = z.reshape(-1, 1)

# Function to reset parameters to default values
def reset_params():
    global Ea, depth, X_initial, T_min, T_opt, T_max, P_max, alpha, I_opt, kT, kI, K, C, \
        biomass_loss_night_temp2, biomass_loss_night_temp, biomass_loss_night_cst, \
        culture_absorptivity, culture_depth, culture_dz, nb_layer, C_p, rho, sigma, \
        e_w, A_evap, B_evap, A_conv, B_conv
    from Parameter_Values import (
        Ea, depth, X_initial, T_min, T_opt, T_max, P_max, alpha, I_opt, kT, kI, K, C,
        biomass_loss_night_temp2, biomass_loss_night_temp, biomass_loss_night_cst, z,
        culture_absorptivity, culture_depth, culture_dz, nb_layer, C_p, rho, sigma,
        e_w, A_evap, B_evap, A_conv, B_conv
    )
    global z
    z = np.linspace(0, depth, num=100)
    z = z.reshape(-1, 1)

# Initialize session state
if 'Ea' not in st.session_state:
    st.session_state.Ea = Ea
if 'depth' not in st.session_state:
    st.session_state.depth = depth
if 'X_initial' not in st.session_state:
    st.session_state.X_initial = X_initial
if 'T_min' not in st.session_state:
    st.session_state.T_min = T_min
if 'T_opt' not in st.session_state:
    st.session_state.T_opt = T_opt
if 'T_max' not in st.session_state:
    st.session_state.T_max = T_max
if 'P_max' not in st.session_state:
    st.session_state.P_max = P_max
if 'alpha' not in st.session_state:
    st.session_state.alpha = alpha
if 'I_opt' not in st.session_state:
    st.session_state.I_opt = I_opt
if 'kT' not in st.session_state:
    st.session_state.kT = kT
if 'kI' not in st.session_state:
    st.session_state.kI = kI
if 'K' not in st.session_state:
    st.session_state.K = K
if 'C' not in st.session_state:
    st.session_state.C = C
if 'biomass_loss_night_temp2' not in st.session_state:
    st.session_state.biomass_loss_night_temp2 = biomass_loss_night_temp2
if 'biomass_loss_night_temp' not in st.session_state:
    st.session_state.biomass_loss_night_temp = biomass_loss_night_temp
if 'biomass_loss_night_cst' not in st.session_state:
    st.session_state.biomass_loss_night_cst = biomass_loss_night_cst
if 'culture_absorptivity' not in st.session_state:
    st.session_state.culture_absorptivity = culture_absorptivity
if 'culture_depth' not in st.session_state:
    st.session_state.culture_depth = culture_depth
if 'culture_dz' not in st.session_state:
    st.session_state.culture_dz = culture_dz
if 'nb_layer' not in st.session_state:
    st.session_state.nb_layer = nb_layer
if 'C_p' not in st.session_state:
    st.session_state.C_p = C_p
if 'rho' not in st.session_state:
    st.session_state.rho = rho
if 'sigma' not in st.session_state:
    st.session_state.sigma = sigma
if 'e_w' not in st.session_state:
    st.session_state.e_w = e_w
if 'A_evap' not in st.session_state:
    st.session_state.A_evap = A_evap
if 'B_evap' not in st.session_state:
    st.session_state.B_evap = B_evap
if 'A_conv' not in st.session_state:
    st.session_state.A_conv = A_conv
if 'B_conv' not in st.session_state:
    st.session_state.B_conv = B_conv

# Sidebar for changing parameters
with st.sidebar.form("parameter_form"):
    st.header("For Informed Users")
    st.header("Model Parameters")
    st.text("In this sidebar, you can modify the model parameters value, or leave the default one")
    # Input fields for parameters
    st.header("Initialization")
    new_depth = st.number_input("Culture depth in m", value=st.session_state.depth)
    new_culture_depth = st.number_input("Culture Depth for the Temperature model, in m", value=st.session_state.culture_depth)
    new_culture_dz = st.number_input("Culture Dz for the Temperature model, in m", value=st.session_state.culture_dz)
    new_nb_layer = st.number_input("Number of Layers for the Temperature model", value=st.session_state.nb_layer)
    new_X_initial = st.number_input("Initial Biomass Concentration at the beginning of each day, in kg/m3", value=st.session_state.X_initial)
    st.header("Beer-Lambert light absorption model")
    st.latex(r'''I_{z} = I_{0}\cdot \text{exp}\left( -E_{a}\cdot X\cdot z \right)''')
    
    st.latex(r''' \small E_{a}''')
    col1, col2 = st.columns([5,1])
    with col1:
      st.latex(r''' \scriptsize I_{z} \text{: The local light intensity at depth z, in } \mu mol/m^{2}/s''')
      st.latex(r''' \scriptsize I_{0} \text{: The incident light intensity, in } \mu mol/m^{2}/s''')
      st.latex(r''' \scriptsize E_{a} \text{: The light absorption coefficient of the culture, in } m^{2}/kg''')
      st.latex(r''' \scriptsize X \text{: The biomass concentration of the culture, in } kg/m^{3}''')
      st.latex(r''' \scriptsize z \text{: The depth in the reactor}''')
      
    with col2:
      st.text("")
      st.text("")
      new_Ea = st.number_input("", value=st.session_state.Ea)
      st.text("")
      st.text("")
    st.header("Biomass production model")
    st.text("The biomass production model decorrelates")
    st.text("the effect of temperature an light:")
    st.latex(r'P(T,I)= P_{max} \cdot f(T) \cdot g(I) \cdot X')
    st.latex(r''' \scriptsize P(T,I) \text{: The biomass productivity for a temperature T and a light intensity I, in } kg/m^{3}/h''')
    st.latex(r''' \scriptsize P_{max} \text{: The maximum specific biomass productivity, in } /h''')
    st.latex(r''' \scriptsize f(T) \text{: The function that represents the temperature effect on biomass productivity}''')
    st.latex(r''' \scriptsize g(I) \text{: The function that represents the light intensity effect on biomass productivity}''')
    st.latex(r''' \scriptsize X \text{: The biomass concentration, in } kg/m^{3}''')
    col1, col2 = st.columns([1,1])
    with col1:
      st.latex(r'\small P_{max}')
    with col2:
      new_P_max = st.number_input("", value=st.session_state.P_max)
    st.header("Model for temperature effect on biomass productivity")
    st.text("Cardinal Temperature Model with Inflection (CTMI)")
    st.text("Developped by Rosso et al., 1993")
    st.link_button("https://doi.org/10.1006/jtbi.1993.1099",  "https://doi.org/10.1006/jtbi.1993.1099")
    st.text("First applied to microalgae by Bernard and Rémond, 2012")
    st.link_button("https://doi.org/10.1016/j.biortech.2012.07.022", "https://doi.org/10.1016/j.biortech.2012.07.022")
    st.latex(r'''\begin{equation}
\left\{
\begin{aligned}
f(T) &= 0 \text{ for } T < T_{min} \\
f(T) &= \frac{\left( T-T_{max} \right)\left( T-T_{min} \right)^2}{\left(T_{opt}-T_{min}\right)\left[ \left(T_{opt}-T_{min}\right)\left( T-T_{opt}\right)-\left( T_{opt}-T_{max} \right)\left( T_{opt}+T_{min}-2T \right) \right]} \\
f(T) &= 0 \text{ for } T > T_{max}
\end{aligned}
\right.
\end{equation}''')

    st.latex(r''' \scriptsize T \text{: The temperature of the culture, in °C } ''')
    st.latex(r''' \scriptsize T_{min} \text{: The minimal temperature for growth, in °C } ''')
    st.latex(r''' \scriptsize T_{opt} \text{: The optimal temperature for growth, in °C } ''')
    st.latex(r''' \scriptsize T_{max} \text{: The maximal temperature for growth, in °C } ''')
    #Table for inputs
    col1, col2 = st.columns([1, 3])
    with col1:
      st.latex(r'\small T_{min}')
      st.latex(r'\small T_{opt}')
      st.latex(r'\small T_{max}')
    with col2:
      new_T_min = st.number_input('', value=st.session_state.T_min)
      new_T_opt = st.number_input("", value=st.session_state.T_opt)
      new_T_max = st.number_input("", value=st.session_state.T_max)
    
    st.header("Model for light intensity effect on biomass productivity (PI curve)")
    st.text("Developped by Eilers and Peeters, 1988")
    st.link_button("https://doi.org/10.1016/0304-3800(88)90057-9",  "https://doi.org/10.1016/0304-3800(88)90057-9")
    st.text("Modified by Beranrd and Rémond, 2012 (see above for reference)")
    st.text("For better parameter identification")
    st.latex(r'''g(I) = \frac{I}{I+\frac{P_{max}}{\alpha}\left( \frac{I}{I_{opt}}-1 \right)^{2}}''')
    st.latex(r''' \scriptsize {\alpha} \text{: The initial slope of biomass productivity towards light intensity, in} \frac{kg/m^{3}/h}{\mu mol/m^{2}/s} ''')
    st.latex(r''' \scriptsize I_{opt} \text{: The optimal light intensity for growth, in } \mu mol/m^{2}/s ''')
    col1,col2 = st.columns([1,2])
    with col1:
      st.latex(r'\small {\alpha}')
      st.latex(r'\small I_{opt}')
    with col2:
      new_alpha = st.number_input("", value=st.session_state.alpha)
      new_I_opt = st.number_input("", value=st.session_state.I_opt)
    st.header("Model for biomass respiration on light")
    st.text("Adapted from Laws and Chalup, 1990")
    st.link_button("https://doi.org/10.4319/lo.1990.35.3.0597",  "https://doi.org/10.4319/lo.1990.35.3.0597")
    st.latex(r'''R(T,I)=\left(R_{P} + R_{P,T}\cdot T+R_{P,I}\cdot I  \right)\cdot P_{max}+R_{0}''')
    st.latex(r''' \scriptsize R(T,I) \text{: Biomass respiration for a temperature T and a light intensity I, in } kg/m^{3}/h ''')
    st.latex(r''' \scriptsize R_{P} \text{: Respiration Sensitivity to Productivity}  ''')
    st.latex(r''' \scriptsize R_{P,T} \text{: Respiration Sensitivity to Productivity-Temperature Interaction, in } /°C ''')
    st.latex(r''' \scriptsize R_{P,I} \text{: Respiration Sensitivity to Productivity-Light Intensity Interaction, in } \left( \mu mol/m^{2}/s \right)^{-1} ''')
    st.latex(r''' \scriptsize R_{0} \text{: Maintenance respiration, in } kg/m^{3}/h ''')
  
    col1,col2 = st.columns([1,4])
    with col1:
      st.latex(r''' \small R_{P} ''')
      st.latex(r''' \small R_{P,T}''')
      st.latex(r''' \small R_{P,I}''')
      st.latex(r''' \small R_{0}''')
    with col2:
      new_C = st.number_input("", value=st.session_state.C)
      new_kT = st.number_input("", value=st.session_state.kT)
      new_kI = st.number_input("", value=st.session_state.kI)
      new_K = st.number_input("", value=st.session_state.K)
      
    #new_biomass_loss_night_temp2 = st.number_input("Biomass Loss Night Temp2", value=st.session_state.biomass_loss_night_temp2)
    #new_biomass_loss_night_temp = st.number_input("Biomass Loss Night Temp", value=st.session_state.biomass_loss_night_temp)
    #new_biomass_loss_night_cst = st.number_input("Biomass Loss Night Cst", value=st.session_state.biomass_loss_night_cst)
    st.header("Model for estimating the temperature of the microalgae culture")
    st.text("Developped by Rodríguez-Miranda et al., 2020")
    st.link_button("https://doi.org/10.1002/bit.27617",  "https://doi.org/10.1002/bit.27617")
    new_culture_absorptivity = st.number_input("Culture Absorptivity", value=st.session_state.culture_absorptivity)

    new_C_p = st.number_input("C_p", value=st.session_state.C_p)
    new_rho = st.number_input("Rho", value=st.session_state.rho)
    new_sigma = st.number_input("Sigma", value=st.session_state.sigma)
    new_e_w = st.number_input("E_w", value=st.session_state.e_w)
    new_A_evap = st.number_input("A_evap", value=st.session_state.A_evap)
    new_B_evap = st.number_input("B_evap", value=st.session_state.B_evap)
    new_A_conv = st.number_input("A_conv", value=st.session_state.A_conv)
    new_B_conv = st.number_input("B_conv", value=st.session_state.B_conv)

    # Submit button
    submitted = st.form_submit_button("Update Parameters")

    if submitted:
        update_params(new_Ea, new_depth, new_X_initial, new_T_min, new_T_opt, new_T_max, new_P_max,
            new_alpha, new_I_opt, new_kT, new_kI, new_K, new_C, new_biomass_loss_night_temp2,
            new_biomass_loss_night_temp, new_biomass_loss_night_cst, new_culture_absorptivity,
            new_culture_depth, new_culture_dz, new_nb_layer, new_C_p, new_rho, new_sigma,
            new_e_w, new_A_evap, new_B_evap, new_A_conv, new_B_conv)
        st.session_state.Ea = Ea
        st.session_state.depth = depth
        st.session_state.X_initial = X_initial
        st.session_state.T_min = T_min
        st.session_state.T_opt = T_opt
        st.session_state.T_max = T_max
        st.session_state.P_max = P_max
        st.session_state.alpha = alpha
        st.session_state.I_opt = I_opt
        st.session_state.kT = kT
        st.session_state.kI = kI
        st.session_state.K = K
        st.session_state.C = C
        st.session_state.biomass_loss_night_temp2 = biomass_loss_night_temp2
        st.session_state.biomass_loss_night_temp = biomass_loss_night_temp
        st.session_state.biomass_loss_night_cst = biomass_loss_night_cst
        st.session_state.culture_absorptivity = culture_absorptivity
        st.session_state.culture_depth = culture_depth
        st.session_state.culture_dz = culture_dz
        st.session_state.nb_layer = nb_layer
        st.session_state.C_p = C_p
        st.session_state.rho = rho
        st.session_state.sigma = sigma
        st.session_state.e_w = e_w
        st.session_state.A_evap = A_evap
        st.session_state.B_evap = B_evap
        st.session_state.A_conv = A_conv
        st.session_state.B_conv = B_conv
        st.success("Parameters updated!")

# Reset button
if st.button("Reset to Parameters Values to Default"):
    reset_params()
    st.session_state.Ea = Ea
    st.session_state.depth = depth
    st.session_state.X_initial = X_initial
    st.session_state.T_min = T_min
    st.session_state.T_opt = T_opt
    st.session_state.T_max = T_max
    st.session_state.P_max = P_max
    st.session_state.alpha = alpha
    st.session_state.I_opt = I_opt
    st.session_state.kT = kT
    st.session_state.kI = kI
    st.session_state.K = K
    st.session_state.C = C
    st.session_state.biomass_loss_night_temp2 = biomass_loss_night_temp2
    st.session_state.biomass_loss_night_temp = biomass_loss_night_temp
    st.session_state.biomass_loss_night_cst = biomass_loss_night_cst
    st.session_state.culture_absorptivity = culture_absorptivity
    st.session_state.culture_depth = culture_depth
    st.session_state.culture_dz = culture_dz
    st.session_state.nb_layer = nb_layer
    st.session_state.C_p = C_p
    st.session_state.rho = rho
    st.session_state.sigma = sigma
    st.session_state.e_w = e_w
    st.session_state.A_evap = A_evap
    st.session_state.B_evap = B_evap
    st.session_state.A_conv = A_conv
    st.session_state.B_conv = B_conv
    st.success("Parameters reset to default!")


st.write("Current Parameters:", {
    "Ea": st.session_state.Ea, "depth": st.session_state.depth, "X_initial": st.session_state.X_initial,
    "T_min": st.session_state.T_min, "T_opt": st.session_state.T_opt, "T_max": st.session_state.T_max,
    "P_max": st.session_state.P_max, "alpha": st.session_state.alpha, "I_opt": st.session_state.I_opt,
    "kT": st.session_state.kT, "kI": st.session_state.kI, "K": st.session_state.K, "C": st.session_state.C,
    "biomass_loss_night_temp2": st.session_state.biomass_loss_night_temp2,
    "biomass_loss_night_temp": st.session_state.biomass_loss_night_temp,
    "biomass_loss_night_cst": st.session_state.biomass_loss_night_cst,
    "culture_absorptivity": st.session_state.culture_absorptivity,
    "culture_depth": st.session_state.culture_depth, "culture_dz": st.session_state.culture_dz,
    "nb_layer": st.session_state.nb_layer, "C_p": st.session_state.C_p, "rho": st.session_state.rho,
    "sigma": st.session_state.sigma, "e_w": st.session_state.e_w, "A_evap": st.session_state.A_evap,
    "B_evap": st.session_state.B_evap, "A_conv": st.session_state.A_conv, "B_conv": st.session_state.B_conv
})



# Enter the location, city
your_loc = st.text_input("Which city do you want the microalgae culture located? ")

options = ["All months", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
month_select = st.selectbox(
    "For which month do you want to optimize the transparency of the semi-transparent PV panel?",
    options,
    index=None,
    placeholder="Select all months or a specific month...",
)

st.write("You selected:", options.index(month_select))


if options.index(month_select) == 0:
  # Import the weather data
  # Define the start and end dates for the entire year
  start_date = f"{year}-01-01"
  end_date = f"{year}-12-31"

  # Import the weather data for the entire year
  latitude, longitude = import_location_data(your_loc)
  weather_data = import_weather_data_function(latitude, longitude, start_date, end_date)

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


  # Calculation of the hourly average for each month
  #Initiate the Matplotlib figure
  fig, ax = plt.subplots()
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
    #Plot the hourly average for the month
  
  
    ax.plot(range(24), temperature_avg[month - 1, :], label= "Average Fourly Temperatures for " + str(calendar.month_name[month]))

  # Graph display
  ax.set_ylabel("Average Hourly Temperature (°C)")
  ax.set_xlabel("Hour of the day")
  ax.set_title(f"Average Hourly Temperatures for all months of {year}")
  ax.legend()
  st.pyplot(fig)

else:
  month = options.index(month_select)
  # Import the weather data for the selected month and year
  num_days_in_month = calendar.monthrange(year, month)[1]
  # Define the start and end dates for the selected month
  start_date = f"{year}-{str(month).zfill(2)}-01"
  end_date = f"{year}-{str(month).zfill(2)}-{num_days_in_month}"

  # Import the weather data for the entire year
  latitude, longitude = import_location_data(your_loc)
  weather_data = import_weather_data_function(latitude, longitude, start_date, end_date)



  # Initialize NumPy arrays to store the hourly averages
  temperature_avg = np.zeros(24)
  humidity_avg = np.zeros(24)
  dew_point_avg = np.zeros(24)
  wind_speed_avg = np.zeros(24)
  diffuse_rad_avg = np.zeros(24)
  direct_rad_avg = np.zeros(24)
  PAR_avg = np.zeros(24)


  # Calculation of the hourly average for the selected month
  start_index = 1
  end_index = num_days_in_month * 24



  # Calculate the hourly averages and store them in the NumPy arrays
  temperature_avg = calculate_hourly_averages(weather_data[0])
  humidity_avg = calculate_hourly_averages(weather_data[1])
  dew_point_avg = calculate_hourly_averages(weather_data[2])
  wind_speed_avg = calculate_hourly_averages(weather_data[3])
  diffuse_rad_avg = calculate_hourly_averages(weather_data[4])
  direct_rad_avg = calculate_hourly_averages(weather_data[5])
  PAR_avg = calculate_hourly_averages(2.15 * (weather_data[4] + weather_data[5]))

  #Matplotlib figure
  fig, ax = plt.subplots()
  ax.plot(range(24), temperature_avg)
  ax.set_ylabel("Average Hourly Temperature (°C)")
  ax.set_xlabel("Hour of the day")
  ax.set_title(f"Average Hourly Temperatures for {month_select} of {year}")
  # Graph display
  st.pyplot(fig)




# Table display
table_data = pd.DataFrame({"Optimal Transparency for January": [1], "Optimal Transparency for April": [7], "Optimal Transparency for July": [10], "Optimal Transparency for October": [15]})
st.write(table_data)

