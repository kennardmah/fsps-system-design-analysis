### this file needs to evaluate the continuous cost of C_penalty * shortfall at each time step
import numpy as np


# Discounted Value Function
def discounted_value(costs, t, r_discount=0.15):
    return np.sum(costs * (1 - r_discount)**t)

# Penalty Integral Calculation
def calculate_shortfall_costs(t, capacity, demand, C_penalty, r_discount):
    integral = max(0, demand[t]-capacity[t])
    return discounted_value(C_penalty * integral, t, r_discount)

# Development Cost
def calculate_C_nf(M_nf, M_components, C_launch, C_produce, C_payload, r_eos = 0):
    M_total = M_nf + M_components
    C_nf = (M_total) * C_launch + (M_nf * C_produce + (M_total) * C_payload) * (1 - r_eos)
    return C_nf
