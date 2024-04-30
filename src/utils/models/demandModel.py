import numpy as np
import matplotlib.pyplot as plt

### this file will estimate demand and return N simulations based on 'random walk' that the capacityModel will simulate with

'''
VARIABLE
- p_elcss : electrical power demand of the ELCSS
    - elcss_headcount : number of people in the habitat (data structure: float)
    - elcss_power_per_person : power demand per person (data structure: float)
- p_operations : electrical power demand of the operations (data structure: list of tuples)
'''
    
def demand_calculator(elcss_headcount, elcss_power_per_person, operations):
    p_elcss = elcss_headcount * elcss_power_per_person
    p_operations = sum([operation[1] for operation in operations])
    return (p_elcss + p_operations)

def generate_demand_walk(mean, std_dev, num_steps = 21):
    steps = np.random.normal(0, std_dev, num_steps)
    demand_walk = mean + np.cumsum(steps)
    return demand_walk

def generate_demand_simulations(mean, std_dev, num_simulations):
    demand_simulations = []
    for _ in range(num_simulations):
        demand_walk = generate_demand_walk(mean, std_dev)
        demand_simulations.append(demand_walk)
    return demand_simulations

def plot_demand_simulations(demand_simulations):
    for i, demand_walk in enumerate(demand_simulations):
        color = f'{i*1/len(demand_simulations)}'
        plt.plot(demand_walk, color=color, linewidth=0.3)
    plt.xlabel('Time')
    plt.ylabel('Energy Demand (kW)')
    plt.title('Simulations of Demand Random Walk')
    plt.xticks(range(len(demand_walk)))
    plt.ylim(23.4, 45)  # Set y-axis limits
    plt.show()

# plot the final value distribution to reflect researched energy demand
def plot_final_value_distribution(demand_simulations):
    final_values = [demand_walk[-1] for demand_walk in demand_simulations]
    plt.hist(final_values, bins=20, color='gray')
    plt.axvline(np.mean(final_values), color='red', linestyle='dashed', linewidth=1, label='Mean')
    plt.axvline(np.mean(final_values) + np.std(final_values), color='blue', linestyle='dashed', linewidth=1, label='Mean + Std Dev')
    plt.axvline(np.mean(final_values) - np.std(final_values), color='blue', linestyle='dashed', linewidth=1, label='Mean - Std Dev')
    plt.xlabel('Final Value')
    plt.ylabel('Frequency')
    plt.title('Distribution of Final Energy Demand')
    plt.legend()  # Add legend to the plot
    plt.show()

# std_dev of each steps should be std_dev/sqrt(num_steps) to keep the same std_dev for the final value
# update code to call these values instead of hardcoding them
mean, std_dev, num_simulations = 34.2, np.sqrt(4.8/21), 500

# store the same demand simulations for each to have a fair comparison
demand_simulations = generate_demand_simulations(mean, std_dev, num_simulations)
plot_demand_simulations(demand_simulations)
plot_final_value_distribution(demand_simulations)