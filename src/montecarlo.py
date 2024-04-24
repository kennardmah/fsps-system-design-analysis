import numpy as np
import matplotlib.pyplot as plt

# Number of simulations
n_simulations = 10000

def P_ECLSS(occupants, energy_per_occupants):
    return (occupants * energy_per_occupants), 0.1*(occupants * energy_per_occupants)

def P_operations(operations):
    total_energy = 0
    for op, energy in operations:
        total_energy += energy
    return total_energy, 0.1*total_energy

# Phase 1 parameters
ECLSS_p1 = [6, 4.2]
mean_ECLSS_p1, std_dev_ECLSS_p1 = P_ECLSS(ECLSS_p1[0], ECLSS_p1[1])  # kW

OPERATIONS_p1 = [('ISRU Operations', 7), ('Rover Operations', 1), ('Some other stuff', 1)]
mean_operations_p1, std_dev_operations_p1 = P_operations(OPERATIONS_p1)

# Phase 2 parameters
ECLSS_p2 = [12, 4.2]
mean_ECLSS_p2, std_dev_ECLSS_p2 = P_ECLSS(ECLSS_p2[0], ECLSS_p2[1])  # kW

OPERATIONS_p2 = [('ISRU Operations', 14), ('Rover Operations', 2), ('Some other stuff', 2)]
mean_operations_p2, std_dev_operations_p2 = P_operations(OPERATIONS_p2)

# Simulate Phase 1
ECLSS_p1 = np.random.normal(mean_ECLSS_p1, std_dev_ECLSS_p1, n_simulations)
operations_p1 = np.random.normal(mean_operations_p1, std_dev_operations_p1, n_simulations)
total_demand_p1 = ECLSS_p1 + operations_p1

# Simulate Phase 2
ECLSS_p2 = np.random.normal(mean_ECLSS_p2, std_dev_ECLSS_p2, n_simulations)
operations_p2 = np.random.normal(mean_operations_p2, std_dev_operations_p2, n_simulations)
total_demand_p2 = ECLSS_p2 + operations_p2

# Plot results
plt.figure(figsize=(14, 6))
plt.hist(total_demand_p1, bins=50, alpha=0.5, label='Phase 1 Demand')
plt.hist(total_demand_p2, bins=50, alpha=0.5, label='Phase 2 Demand')
plt.title('Monte Carlo Simulation of Energy Demand on the Moon')
plt.xlabel('Total Energy Demand (kW)')
plt.ylabel('Frequency')
plt.legend()
plt.show()
