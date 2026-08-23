import numpy as np

#Parameter values for the biomass production

Ea, depth, X_initial = 170.4, 0.1, 0.1
nb_layer = 100
T_min, T_opt, T_max = 0, 29.6, 45.3
P_max, alpha, I_opt = 0.1003, 0.00043819, 278.7
kT, kI, K, C = 0.0074977, 0.0000768, 0.00010051, -0.09666

biomass_loss_night_temp2 = 4.679e-05 / (24)
biomass_loss_night_temp = -2.623e-03 /(24) 
biomass_loss_night_cst = 3.912e-05 /(24) 

#Parameter values for the culture temperature model

#Culture absorptivity
culture_absorptivity = 0.7#-



#specific heat capacity of the culture
C_p = 4.184 #J·kg−1·°C−1
#density of the culture
rho = 1000.0 #kg·m−3

#sigma is the Stefan-Boltzmann constant in W·m−2·K−4
sigma = 5.6697e-08 #W·m−2·K−4
#e_w is the water emissivity -
e_w = 0.9 #1

#evaporation exchange coefficient in m·s−1·Pa−1
#A_evap and B_evap are evaporation experimental coefficients that must be calibrated
A_evap = 1.2e-11
B_evap=4.67e-12

#convection transfer coefficient obtained experimentally
A_conv =4.78
B_conv =6.83


#T under which the culture is heated when the heating is ON
T_limit = 30.0#°C
Temperature_Control = False

