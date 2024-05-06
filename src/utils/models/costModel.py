### this file needs to evaluate the continuous cost of C_penalty * shortfall at each time step
import numpy as np

# Penalty Integral Calculation
def calculate_C_penalty(t, capacity, demand, alpha_penalty):
    integral = max(0, demand[t]-capacity[t])
    return alpha_penalty * integral

# Development Cost
def calculate_C_capital(M_nf, M_components, C_launch, C_produce, C_payload, r_eos = 0):
    M_total = M_nf + M_components
    C_nf = (M_total) * C_launch + (M_nf * C_produce + (M_total) * C_payload) * (1 - r_eos)
    return C_nf

def calculate_C_
