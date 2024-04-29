import numpy as np
import matplotlib.pyplot as plt
from config import ECLSS_p1, OPERATIONS_p1

def P_ECLSS(occupants, energy_per_occupants):
    return (occupants * energy_per_occupants), (1.15* energy_per_occupants)

def P_operations(operations):
    total_energy = 0
    for i, energy in operations:
        total_energy += energy
    return total_energy, 0.1*total_energy

# Calculate mean and standard deviation for ECLSS, operations, total
mean_ECLSS_p1, std_dev_ECLSS_p1 = P_ECLSS(ECLSS_p1[0], ECLSS_p1[1])
mean_operations_p1, std_dev_operations_p1 = P_operations(OPERATIONS_p1)
mean_total_p1 = mean_ECLSS_p1 + mean_operations_p1
variance_total_p1 = (std_dev_ECLSS_p1 ** 2) + (std_dev_operations_p1 ** 2)
std_dev_total_p1 = np.sqrt(variance_total_p1)

print("Mean of Total Energy Demand for Phase 1:", mean_total_p1, "kW")
print("Standard Deviation of Total Energy Demand for Phase 1:", std_dev_total_p1, "kW")

# Plot the normal distribution for total energy demand
x_values = np.linspace(mean_total_p1 - 3*std_dev_total_p1, mean_total_p1 + 3*std_dev_total_p1, 1000)
y_values = (1 / (std_dev_total_p1 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_values - mean_total_p1) / std_dev_total_p1) ** 2)

plt.figure(figsize=(8, 4))
plt.plot(x_values, y_values, label='Normal Distribution')
plt.title('Normal Distribution of Total Energy Demand for Phase 1')
plt.xlabel('Total Energy Demand (kW)')
plt.ylabel('Probability Density')
plt.grid(True)
plt.show()