import numpy as np
from scipy.integrate import simps
import matplotlib.pyplot as plt
from config import M_nf_40, M_total_40, C_launch, C_produce, C_payload, r_eos, C_penalty


C_nf = (M_total_40) * C_launch + (M_nf_40 * C_produce + (M_total_40) * C_payload) * (1 - r_eos)

t = np.linspace(0, 20, 100)  # Define time from 0 to 20 in 100 steps

def nuclear_capacity(M_nf, time, EOPM=40/3969, decay_rate=0.0159):
    return M_nf_40 * EOPM * (1 - decay_rate)**time

def P_demand(demand, t):
    return demand * np.ones_like(t) # A hypothetical constant demand curve

def P_supply(t):
    return nuclear_capacity(M_nf_40, time=t)

def shortfall(t):
    demand = P_demand(34.2, t)
    supply = P_supply(t)
    return np.maximum(demand - supply, 0)  # Only consider positive differences

plt.figure(figsize=(10, 6))
plt.plot(t, P_demand(34.2, t), label='P_demand (34.2 kW constant)', linestyle='--')
plt.plot(t, P_supply(t), label='P_supply (Decaying over time)')
plt.title('Demand vs. Supply Over Time')
plt.xlabel('Time (years)')
plt.ylabel('Power (kW)')
plt.legend()
plt.grid(True)
plt.show()

shortfall_values = shortfall(t)
total_costs = []


integral = simps(shortfall_values, t)

# Calculate total cost for each C_penalty
C_total = C_nf + C_penalty * integral
total_costs.append(C_total)
print(f"C_penalty: {C_penalty}, Total Cost: {C_total}")
cumulative_integral = np.array([simps(shortfall_values[:i+1], t[:i+1]) for i in range(len(t))])
C_total = C_nf + C_penalty * cumulative_integral

# Plotting C_total as a function of time
plt.figure(figsize=(10, 6))
plt.plot(t, C_total, label='Total Cost over Time')
plt.title('Total Cost as a Function of Time')
plt.xlabel('Time (years)')
plt.ylabel('Total Cost ($)')
plt.legend()
plt.grid(True)
plt.show()