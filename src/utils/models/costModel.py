import numpy as np

"""
costModel.py – calculate the cost at each time step and return the total cost
"""

# Penalty Integral Calculation
def calculate_C_penalty(capacity, demand, t, alpha_penalty = 5000000):
    integral = max(0, demand[t]-capacity[t])
    return alpha_penalty * integral

# Development Cost
def calculate_C_capital(kW, mass_ratio = 3969/40, C_launch = 2720, C_produce = 43000, C_payload = 3500, r_eos = 0):
    M_nf = kW * mass_ratio
    M_components = 1621/40 * kW
    M_total = M_nf + M_components
    C_nf = (M_total) * C_launch + (M_nf * C_produce + (M_total) * C_payload) * (1 - r_eos)
    return C_nf

# Operational Cost at t
def calculate_C_operational(M_nf, M_components, cost_per_mass = 0):
    return (M_nf + M_components) * cost_per_mass

# Total Cost at t
def calculate_C_total(kW, t):
    C_capital = calculate_C_capital(kW_added)
    C_operational = calculate_C_operational(3969/40 * kW, 1621/40 * kW)
    C_penalty = calculate_C_penalty(kW_produced, t)
    return C_capital + C_operational + C_penalty

def add_C_capital(cost_overtime, kW, t):
    cost_overtime[t] += calculate_C_capital(kW)
    return cost_overtime
