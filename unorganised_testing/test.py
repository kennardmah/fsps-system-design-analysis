import numpy as np
import calculation
from config import EOPM, C_launch, C_produce, C_payload, C_penalty, r_eos, capacities
import matplotlib.pyplot as plt

# Define the chance arrays
chance_1 = [(44.0, 1/3), (34.2, 1/3), (24.4, 1/3)]
chance_2_high = [(44.0, 0.7), (34.2, 0.2), (24.4, 0.1)]
chance_2_med = [(44.0, 0.2), (34.2, 0.6), (24.4, 0.2)]
chance_2_low = [(44.0, 0.1), (34.2, 0.2), (24.4, 0.7)]

# Define the capacities list
capacities = [40, 50, 60, 70]

# Define the time array
t = np.linspace(0, 10, 100)

# Recursive Decision Tree Analysis Function
def analyze_tree(decisions, chances, expected_costs, cost_over_time, path=[]):
    if not decisions:
        return

    capacity = decisions[0]
    next_decisions = decisions[1:]
    M_nf = capacity / EOPM
    M_components = capacity / (40/1621)
    initial_cost = calculation.calculate_costs(M_nf, M_components, C_launch, C_produce, C_payload, r_eos)

    # Create a cost array initialized to initial cost
    cost_array = np.full_like(t, initial_cost)

    for demand, probability in chances:
        shortfall_values = calculation.calculate_shortfall(M_nf, demand, t)
        C_total = calculation.calculate_shortfall_costs(t, shortfall_values, C_penalty)
        cost_array += C_total * probability  # Incorporate shortfall cost over time adjusted by probability

    expected_costs[capacity] = cost_array[-1]  # Store the final cost at the end of the period
    cost_over_time[capacity] = cost_array  # Store time-series data
    path.append(capacity)

    # Determine next chance scenario based on the current capacity
    next_chances = chance_2_high if capacity == 44 else chance_2_med if capacity == 34.2 else chance_2_low if capacity == 24.4 else chance_2_low
    if next_decisions:
        analyze_tree(next_decisions, next_chances, expected_costs, cost_over_time, path.copy())
    else:
        # Record the path once it is fully explored
        print(f"Path: {path} -> Final Cost at t=10: ${cost_array[-1]:.2f}")

# Initialize dictionaries
expected_costs = {}
cost_over_time = {}

# Start the analysis
analyze_tree(capacities, chance_1, expected_costs, cost_over_time)

# Visualization
plt.figure()
for capacity, costs in cost_over_time.items():
    plt.plot(t, costs, label=f"Capacity {capacity}")
plt.xlabel("Time")
plt.ylabel("Cost")
plt.legend()
plt.title("Cost Over Time by Capacity")
plt.show()
