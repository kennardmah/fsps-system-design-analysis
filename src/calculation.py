import numpy as np
from scipy.integrate import simps
import matplotlib.pyplot as plt

# Constants and global variables
M_nf = 3929
M_components = 1621
M_total = M_nf + M_components
C_launch = 2720
C_produce = 43000
C_payload = 3500
r = 0.1
C_penalty = 500000

def calculate_costs(M_nf, M_components, C_launch, C_produce, C_payload, r):
    M_total = M_nf + M_components
    C_nf = (M_total) * C_launch + (M_nf * C_produce + (M_total) * C_payload) * (1 - r)
    return C_nf

def nuclear_capacity(M_nf, time, EOPM=40/3969, decay_rate=0.0159):
    return M_nf * EOPM * (1 - decay_rate)**time

def constant_demand(t, demand):
    return demand * np.ones_like(t)

def calculate_shortfall(M_nf, demand, t):
    supply = nuclear_capacity(M_nf, t)
    return np.maximum(demand - supply, 0)  # Only consider positive differences

def calculate_shortfall_costs(t, shortfall_values, C_penalty):
    integral = simps(shortfall_values, t)
    return C_penalty * integral

def plot_power(t, demand):
    plt.figure(figsize=(10, 6))
    plt.plot(t, constant_demand(t, demand), label='P_demand (34.2 kW constant)', linestyle='--')
    plt.plot(t, nuclear_capacity(M_nf, t), label='P_supply (Decaying over time)')
    plt.title('Demand vs. Supply Over Time')
    plt.xlabel('Time (years)')
    plt.ylabel('Power (kW)')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_costs(t, C_total):
    plt.figure(figsize=(10, 6))
    plt.plot(t, C_total, label='Total Cost over Time')
    plt.title('Total Cost as a Function of Time')
    plt.xlabel('Time (years)')
    plt.ylabel('Total Cost ($)')
    plt.legend()
    plt.grid(True)
    plt.show()