### this file needs to evaluate the continuous cost of C_penalty * shortfall at each time step
import numpy as np


# Discounted Value Function
def discounted_value(costs, t, r_discount=0.01):
    return np.sum(costs * (1 - r_discount)**t)

# Penalty Integral Calculation
def calculate_shortfall_costs(t, shortfall_values, C_penalty, r_discount):
    integral = np.trapz(shortfall_values, t)
    return discounted_value(C_penalty * integral, t, r_discount)
