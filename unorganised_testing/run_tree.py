import numpy as np
import calculation
from config import EOPM, C_launch, C_produce, C_payload, C_penalty, r_eos, capacities, r_discount

# variables
fixed_decisions = capacities

# chance nodes
chance_1 = [(44, 1/3), (34.2, 1/3), (24.4, 1/3)]
chance_2_high = [(44, 0.7), (34.2, 0.2), (24.4, 0.1)]
chance_2_med = [(44, 0.2), (34.2, 0.6), (24.4, 0.2)]
chance_2_low = [(44, 0.1), (34.2, 0.2), (24.4, 0.7)]

t = np.linspace(0, 10, 100)  # Time from 0 to 20 in 100 steps

# Dictionary to hold expected costs for each fixed decision
expected_costs = {}
each_chance_1 = {}

# Recursive Tree
def analyze_tree(decisions, chances):
    if not decisions:
        return  # Terminate recursion when no decisions are left to process
    
    # Process the first decision in the list
    capacity = decisions[0]
    remaining_decisions = decisions[1:]  # Remaining decisions for further recursive calls

    M_nf = capacity / EOPM
    M_components = capacity / (40/1621)
    total_expected_cost = C_nf = calculation.calculate_costs(M_nf, M_components, C_launch, C_produce, C_payload, r_eos)
    each_chance_1[capacity] = []

    for demand, probability in chances:
        shortfall_values = calculation.calculate_shortfall(M_nf, demand, t)
        C_total = calculation.calculate_shortfall_costs(t, shortfall_values, C_penalty, r_discount)
        total_expected_cost += C_total * probability
        each_chance_1[capacity].append((demand, total_expected_cost))

    expected_costs[capacity] = total_expected_cost

    # Select appropriate next chances based on the current capacity
    next_chances = chance_2_high if capacity == 44 else chance_2_med if capacity == 34.2 else chance_2_low

    # Recur for each remaining decision in the current chance scenario
    if remaining_decisions:
        analyze_tree(remaining_decisions, chances)  # Continue with the same chance for remaining decisions
        analyze_tree([capacity], next_chances)  # Explore further depths for the current capacity with next chance

analyze_tree(fixed_decisions, chance_1)

# Print the results
print(each_chance_1)
for deployment, cost in expected_costs.items():
    print(f"Initial deployment {deployment}: Expected Cost = ${cost:.2f}")
