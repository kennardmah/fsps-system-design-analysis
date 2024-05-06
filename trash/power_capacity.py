import numpy as np
import matplotlib.pyplot as plt
from config import EOPM, r_decay, time, capacities

"""
Lunar Energy Implementation Optimisation - Kennard Mah 2024, Imperial College London
--- capacityModels.py ---
Calculates the energy capacity for Nuclear-based reactors and plots it over time
"""

def find_mass(kW, EOPM=EOPM):
    return kW / EOPM

def nuclear_capacity(M_nf, time = 20, EOPM=40/3969, r_decay=0.0159):
    return M_nf * EOPM * (1 - r_decay)**time

# calculate parameters
masses = [find_mass(cap) for cap in capacities]

# calculate nuclear capacity over time
time_range = np.arange(time)
results = {cap: [nuclear_capacity(mass, t) for t in time_range] for cap, mass in zip(capacities, masses)}

# Plotting
plt.figure(figsize=(10, 6))
colors = ['0.0', '0.3', '0.6']
for (cap, vals), color in zip(results.items(), colors):
    plt.plot(time_range, vals, label=f'Initial capacity: {cap} kW', color=color)
plt.title('Nuclear Capacity Decay Over Time')
plt.xlabel('Time (years)')
plt.ylabel('Capacity (kW)')
plt.legend()
plt.grid(True)
plt.show()
