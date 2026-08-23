from Parameter_Values import *

def Phi_temp(T_min, T_opt, T_max, Temp):
    num = (Temp - T_max) * ((Temp - T_min) ** 2)
    den = (T_opt - T_min) * (
        (T_opt - T_min) * (Temp - T_opt) - (T_opt - T_max) * (T_opt + T_min - 2 * Temp)
    )
    den = np.where(np.abs(den) < 1e-12, 1e-12, den)
    result = num / den
    return np.where((Temp > T_max) | (Temp < T_min), 0.0, result)

def Phi_I(P_max, alpha, I_opt, I):
    return I / (I + P_max / alpha * ((I / I_opt - 1) ** 2))

def BL(Ea, I0, X, z):
    return I0 * np.exp(-z * X * Ea)

def light_respiration(kT, kI, C, K, Temp, I, prod):
    return (kT*Temp + kI*I+ C)*prod + K

def biomass_loss_night(biomass_loss_night_temp2, biomass_loss_night_temp, biomass_loss_night_cst, Temp, dt):
    return np.exp(-(biomass_loss_night_temp2 * Temp**2 + biomass_loss_night_temp * Temp + biomass_loss_night_cst) * dt / 3600)



def calculate_biomass_production(P_max, alpha, I_opt, I, T_min, T_opt, T_max, Temp, kT, kI, C, K, depth, transparency, nb_layer):
    z = np.linspace(0, depth, num=nb_layer)
    n_hours = len(I)
    X = np.zeros(n_hours)
    prod = np.zeros(n_hours)
    respi = np.zeros(n_hours)
    
    for i in range(n_hours):
        
        
        phi_temp = Phi_temp(T_min, T_opt, T_max, Temp[i])
        if i == 0: 
            X_prev = X_initial 
        else: 
            X_prev = X[i-1]
        
        
        I_local = BL(Ea,I[i] * transparency, X_prev, z)
        phi_I = Phi_I(P_max, alpha, I_opt, I_local)
        if I[i] >0:
            gross = P_max * phi_I * phi_temp 
            resp = gross * (C + kT*Temp[i] + kI*I_local) + K
            net = np.sum(gross - resp) / len(z)
            prod[i] = np.sum(gross)/len(z)
            respi[i] =  np.sum(resp)/len(z)
            
        else:
            gross = np.zeros_like(I_local)
            resp = np.zeros_like(I_local)
            net = 0
            prod[i] = 0
            respi[i] = 0
        # net = np.maximum(np.sum(gross - resp) / len(z), 0)
        
        X[i] = X_prev * (1 + net)

    return X


