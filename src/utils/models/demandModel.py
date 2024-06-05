"""
demandModel.py

This file estimates demand and returns N simulations based on a 'random walk' that the capacityModel will simulate with.

This file contains functions to:
    1) main: Generate demand simulations, save them to a CSV file, and optionally plot the demand simulations and final value distribution.
    2) constant_demand: Generate a constant demand over time.
    3) demand_calculator: Calculate the total demand based on the ELCSS headcount, power per person, and operations.
    4) generate_demand_walk: Generate a single demand walk using a random walk with specified mean and standard deviation.
    5) generate_demand_simulations: Generate multiple demand simulations using the random walk method.
    6) plot_demand_simulations: Plot the generated demand simulations over time.
    7) plot_final_value_distribution: Plot the distribution of final values of the demand simulations.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import sys
sys.path.append('tools')
from design import colors


def main(plot=True):
    mean, std_dev, num_simulations = 34.2, np.sqrt(4.8/21), 1000
    # store the same demand simulations for each to have a fair comparison
    demand_simulations = generate_demand_simulations(mean, std_dev, num_simulations)
    demand_table = pd.DataFrame(demand_simulations)
    demand_table.to_csv("src/utils/data/raw/demand_simulations.csv")
    if plot:
        plot_demand_simulations(demand_simulations)
        plot_final_value_distribution(demand_simulations)

### PRELIMINARY ANALYSIS BELOW
def constant_demand(t, demand):
    return demand * np.ones(t)

### USEFUL FUNCTIONS BELOW
def demand_calculator(elcss_headcount, elcss_power_per_person, operations):
    p_elcss = elcss_headcount * elcss_power_per_person
    p_operations = sum([operation[1] for operation in operations])
    return (p_elcss + p_operations)

def generate_demand_walk(mean, std_dev, num_steps = 21):
    steps = np.random.normal(0, std_dev*2, num_steps//2+1)
    uniform_steps = np.random.normal(0, std_dev, num_steps//2)
    steps = np.concatenate([steps, uniform_steps])
    demand_walk = mean + np.cumsum(steps)
    return demand_walk

def generate_demand_simulations(mean, std_dev, num_simulations):
    demand_simulations = []
    for _ in range(num_simulations):
        demand_walk = generate_demand_walk(mean, std_dev)
        demand_simulations.append(demand_walk)
    return demand_simulations

def plot_demand_simulations(demand_simulations, colors=colors):
    start_c, end_c = mcolors.hex2color(colors["blue"]), mcolors.hex2color(colors["dark_purple"])
    color = [
    (
        start_c[0] + (end_c[0] - start_c[0]) * i / (len(demand_simulations) - 1),
        start_c[1] + (end_c[1] - start_c[1]) * i / (len(demand_simulations) - 1),
        start_c[2] + (end_c[2] - start_c[2]) * i / (len(demand_simulations) - 1)
    )
    for i in range(len(demand_simulations))
    ]
    for i, demand_walk in enumerate(demand_simulations):
        plt.plot(demand_walk, color=color[i], linewidth=0.3)
    plt.xlabel('Time (t) [years]')
    plt.ylabel('Energy Demand (kW)')
    # plt.title('Demand Forecast (using Random Walk)')
    plt.xticks(range(len(demand_walk)))
    plt.xlim(0,20)
    plt.ylim(20.4, 48) 
    plt.tight_layout()
    plt.show()

# plot the final value distribution to reflect researched energy demand
def plot_final_value_distribution(demand_simulations, colors=colors):
    final_values = [demand_walk[-1] for demand_walk in demand_simulations]
    plt.grid(axis='x', linewidth=0.5, zorder = 3)
    plt.hist(final_values, bins=20, color=colors["dark_purple"], zorder = 2)
    plt.axvline(np.mean(final_values), color=colors["blue"], linestyle='--', linewidth=1, label='Mean')
    plt.axvline(np.mean(final_values) + np.std(final_values), color=colors["purple"], linestyle='--', linewidth=1, label='Mean ± σ')
    plt.axvline(np.mean(final_values) - np.std(final_values), color=colors["purple"], linestyle='--', linewidth=1)
    plt.xlabel('Final Value')
    plt.ylabel('Frequency')
    # plt.title('Distribution of Final Energy Demand')
    plt.xticks(np.arange(20, 50, 2))
    plt.tight_layout()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()