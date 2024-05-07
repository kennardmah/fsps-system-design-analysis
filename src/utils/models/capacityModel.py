import pandas as pd

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
    return capacity_over_time

def add_capacity(capacity_over_time, add_kW, add_time = 11, time = 21):
    for t in range(time - add_time):
        capacity_over_time[add_time + t] += nuclear_capacity(add_kW, t)
    return capacity_over_time

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
    for robust_capacity in [50, 60, 70]:
        robust = nuclear_capacity_time(robust_capacity)
        table_data.append(robust)

    for flexible_capacity in [30, 40]:
        for add in [0, 10, 20]:
            flexible = add_capacity(nuclear_capacity_time(flexible_capacity), add)
            table_data.append(flexible)

    table_rows = ['50', '60', '70', '30_0', '30_10', '30_20', '40_0', '40_10', '40_20']
    table_columns = list(range(21))
    table = pd.DataFrame(table_data, index=table_rows, columns=table_columns)
    table.transpose().to_csv('/Users/kennardmah/Documents/GitHub/masters-thesis-sustainable-lunar-energy/src/utils/data/capacity_over_time.csv')
    # table.transpose().plot()
    # plt.xlabel('Time (years)')
    # plt.ylabel('Capacity (kW)')
    # plt.title('Capacity Over Time')
    # plt.show()
    print(table)

