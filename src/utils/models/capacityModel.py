import matplotlib.pyplot as plt

def nuclear_capacity(kW, time, r_decay=0.0159):
    return kW * (1 - r_decay)**time

# this must be updated to enable adding capacity for flexibility
def nuclear_capacity_time(kW, time, r_decay=0.0159):
    capacity_over_time = []
    for t in range(time):
        capacity_over_time.append(nuclear_capacity(kW, t, r_decay))
    # plot_energy_capacity(capacity_over_time)
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

nuclear_capacity_time(40, 21)

