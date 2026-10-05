#Function that estimates the temperature of a culture, based on the paper:
#Rodríguez-Miranda E, Acién FG, Guzmán JL, Berenguel M, Visioli A. 
#A new model to analyze the temperature effect on the microalgae performance at large scale raceway reactors. 
#Biotechnology and Bioengineering. 2021; 118: 877–889. 
#https://doi.org/10.1002/bit.27617

import numpy as np

def Culture_Temperature_function(dt, nb_hours, raceway_area, depth, hourly_global_radiation, hourly_relative_humidity_2m, hourly_temperature_2m, \
                                 hourly_dew_point_2m, hourly_wind_speed_10m, T_soil, culture_absorptivity, nb_layer, C_p, rho, sigma, \
                                        e_w, A_evap, B_evap, A_conv, B_conv, x_liner, K_liner, x_soil, K_soil):
    
        
        #Q_accumulated is the accumulated heat flow
    def Q_accumulated(d,raceway_area, C_p, rho, dT_culture):
        return d*raceway_area*C_p*rho*dT_culture
    
    #Q_irradiance is the heat flow due to the solar irradiance
    def Q_irradiance(I_global, a, raceway_area):
        return I_global*a*raceway_area
    
    #Q_radiation is the Radiation heat losses
    def Q_radiation(sigma, raceway_area, e_w, T_culture, T_sky):
        return sigma*raceway_area*e_w*(T_sky**4-(T_culture+273.15)**4)
    
    #T_dew is the dew point temperature in °C
    #time_solar is the number of hours after midnight
    #T_sky is the temperature of the sky in K
    #T_amb is the ambient temperature in °C
    def T_sky(T_amb,T_dew,time_solar):
        return (273.15+T_amb)*(0.711+0.0056*T_dew+0.000073*(T_dew)**2 + 0.013*np.cos(np.radians(15*time_solar)))**0.25
    #Latent heat of evaporation
    def latent_heat_evaporation(T_culture):
        return (2494-2.2*T_culture)*1000

    #evaporation exchange coefficient in m·s−1·Pa−1
    def h_evap(A_evap, B_evap, wind_speed):
        return A_evap+B_evap*wind_speed

    #vapour pressure at ambient temperature in kPa
    def vapour_pressure_ambient(T_amb):
        return 610.78*np.exp(17.27*T_amb/(T_amb+237.3))

    #evaporation rate
    #RH relative humidity in %
    def evaporation_rate(RH, vapour_pressure, h_evap):
        return (RH*vapour_pressure/100-vapour_pressure)*h_evap

    #Evaporation heat flow
    def Q_evaporation(raceway_area, evaporation_rate_value, rho, latent_heat_vapor):
        return raceway_area*evaporation_rate_value*rho*latent_heat_vapor


    #Convection heat flow

    def Q_convection(h_conv, raceway_area, T_amb, T_culture):
        return h_conv*raceway_area*(T_amb-T_culture)

    #convection transfer coefficient obtained experimentally
    def h_conv(A_conv, B_conv, wind_speed):
        return A_conv+B_conv*wind_speed
    #Heat flow by conduction
                                          
    def Q_conduction(x_liner, K_liner, x_soil, K_soil, raceway_area, T_soil, T_culture):
        R_total = x_liner/K_liner + x_soil/K_soil #total resistance of the heat transfer for the soil and the liner
        return raceway_area * (T_soil - T_culture) / R_total
    #Function that estimates the variation of temperature dT_culture
    def dT_culture_func(T_culture,I_avg, RH, a, raceway_area, d, C_p, rho,T_amb, T_dew, time_solar, A_conv, B_conv, x_liner, K_liner, x_soil, K_soil, wind_speed, T_soil):
        Q_irradiance_value=Q_irradiance(I_avg, a, raceway_area)
        
        T_sky_value = T_sky(T_amb, T_dew, time_solar)
        Q_radiation_value = Q_radiation(sigma, raceway_area, e_w, T_culture, T_sky_value)
        
        latent_heat_evaporation_value = latent_heat_evaporation(T_culture)
        vapour_pressure_value = vapour_pressure_ambient(T_amb)
        h_evap_value = h_evap(A_evap, B_evap, wind_speed)
        evaporation_rate_value = evaporation_rate(RH, vapour_pressure_value, h_evap_value)
        Q_evaporation_value = Q_evaporation(raceway_area, evaporation_rate_value, rho, latent_heat_evaporation_value)
        
        h_conv_value = h_conv(A_conv, B_conv, wind_speed)
        Q_convection_value = Q_convection(h_conv_value,raceway_area, T_amb, T_culture)
        Q_conduction_value = Q_conduction(x_liner, K_liner, x_soil, K_soil, raceway_area, T_soil, T_culture)
        dT_culture = (Q_irradiance_value + Q_radiation_value + Q_evaporation_value + Q_convection_value+Q_conduction_value)/(d*raceway_area*C_p*rho)
        return dT_culture
    
    # --- Initialization ---
    n_sub = 10                           # sub-steps per hour (dt_sub = 360 s)
    dt_sub = 3600.0 / n_sub
    nb_h = int(nb_hours)

    T_hourly = np.zeros(nb_h + 1)
    T_hourly[0] = hourly_temperature_2m[0]
    T = T_hourly[0]

    h_cond = 1.0 / (x_liner / K_liner + x_soil / K_soil)   # W/m²/K
    C_area = depth * C_p * rho                              # J/m²/K

    for hh in range(nb_h):
        h_c = h_conv(A_conv, B_conv, hourly_wind_speed_10m[hh])
        for k in range(n_sub):
            time_solar = (hh + k / n_sub) % 24
            f = dT_culture_func(T, hourly_global_radiation[hh], hourly_relative_humidity_2m[hh],
                                culture_absorptivity, raceway_area, depth, C_p, rho,
                                hourly_temperature_2m[hh], hourly_dew_point_2m[hh], time_solar,
                                A_conv, B_conv, x_liner, K_liner, x_soil, K_soil,
                                hourly_wind_speed_10m[hh], T_soil[hh])           # K/s
            # linearised loss coefficient (radiation + convection + conduction)
            h_lin = 4 * sigma * e_w * (T + 273.15) ** 3 + h_c + h_cond
            # linearly implicit (Rosenbrock-Euler) update
            T = T + dt_sub * f / (1.0 + dt_sub * h_lin / C_area)
        T_hourly[hh + 1] = T

    return T_hourly
