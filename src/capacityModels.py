import numpy as np
import matplotlib.pyplot as plt

"""
Lunar Energy Implementation Optimisation - Kennard Mah 2024, Imperial College London
--- capacityModels.py ---
Calculates the energy capacity for Nuclear-based reactors
"""

# Constants
EOPM = 40/3969
decay_rate = 0.0159
time = 20

def find_mass(kW, EOPM=EOPM):
    return kW / EOPM

def nuclear_capacity(M_nf, time, EOPM=EOPM, decay_rate=decay_rate):
    return M_nf * EOPM * (1 - decay_rate)**time

# Initial capacities and corresponding masses
capacities = [60, 50, 40]
masses = [find_mass(cap) for cap in capacities]

# Colors for the plots
colors = ['0.0', '0.3', '0.6']

# Calculating capacities over time
time_range = np.arange(time)
results = {cap: [nuclear_capacity(mass, t) for t in time_range] for cap, mass in zip(capacities, masses)}

# Plotting
plt.figure(figsize=(10, 6))
for (cap, vals), color in zip(results.items(), colors):
    plt.plot(time_range, vals, label=f'Initial capacity: {cap} kW', color=color)

plt.title('Nuclear Capacity Decay Over Time')
plt.xlabel('Time (years)')
plt.ylabel('Capacity (kW)')
plt.legend()
plt.grid(True)
plt.show()
