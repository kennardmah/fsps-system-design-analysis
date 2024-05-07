import pandas as pd
import csv

'''
capacityModel.py
- the purpose of this model is to return a list for how much energy is produced every year
- the model will be based on a decay rate of 1.59% per year (r_decay) that can be adjusted
- the model will also have a function to add capacity at a certain time (t = 10)
- import capacityModel and use function capacity_model for all in one function.
'''

import matplotlib.pyplot as plt

def nuclear_capacity(kW, time, r_decay=0.0159):
    return kW * (1 - r_decay)**time

def nuclear_capacity_time(kW, time = 21, r_decay=0.0159):
    capacity_over_time = []
    for t in range(time):
        capacity_over_time.append(nuclear_capacity(kW, t, r_decay))
    return capacity_over_time # [50, 49, 48 ...]

def add_capacity(capacity_over_time, add_kW, add_time = 11, time = 21):
    for t in range(time - add_time):
        capacity_over_time[add_time + t] += nuclear_capacity(add_kW, t)
    return capacity_over_time # [50, 49, 48 ...]

def measure_mass(implementation_method, mass_nf = 3969/40, mass_components = 1621/40):
    mass_over_time = [1 for _ in range(21)]
    first_kW = implementation_method[0]
    second_kW = implementation_method[10] + implementation_method[0]
    for t in range(21):
        if t < 10:
            mass_over_time[t] = (first_kW * mass_nf, first_kW * mass_components)
        else:
            mass_over_time[t] = (second_kW * mass_nf, second_kW * mass_components)
    return mass_over_time # [(mass_nf, mass_components) for _ in range(21]]

def plot_energy_capacity(capacity_over_time):
    plt.figure(figsize=(10, 6))
    x = list(range(len(capacity_over_time)))
    plt.plot(x, capacity_over_time, label='Power Supply Capacity')
    plt.title('Nuclear Capacity Over Time')
    plt.xlabel('Time (years)')
    plt.ylabel('Capacity (kW)')
    plt.xticks(x)  # Show each time step on the x-axis
    plt.legend()
    plt.show()

def capacity_model(initial_kW, expansion_kW):
    return add_capacity(nuclear_capacity_time(initial_kW), expansion_kW)

# testing
if __name__ == '__main__':
    table_data = []
    for robust_capacity in [50, 60]:
        robust = nuclear_capacity_time(robust_capacity)
        table_data.append([f"inflexible_{robust_capacity}"] + robust)

    for flexible_capacity in [30, 40]:
        for add in [0, 10, 20]:
            flexible = add_capacity(nuclear_capacity_time(flexible_capacity), add)
            table_data.append([f"flexible_{flexible_capacity}_{add}"] + flexible)

    # table_rows = ['inflexible_50', 'inflexible_60', 'flexible_30_0', 'flexible_30_10', 'flexible_30_20', 'flexible_40_0', 'flexible_40_10', 'flexible_40_20']
    # table_columns = list(range(21))

    filename = "src/utils/data/capacity_over_time.csv"

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(table_data)