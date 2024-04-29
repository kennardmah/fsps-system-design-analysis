import numpy as np
import calculation
from config import EOPM, C_launch, C_produce, C_payload, C_penalty, r_eos, capacities

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

# Fixed Tree
def run_tree(decisions, chances):
    for capacity in decisions:

        M_nf = capacity / EOPM
        M_components = capacity / (40/1621)
        total_expected_cost = C_nf = calculation.calculate_costs(M_nf, M_components, C_launch, C_produce, C_payload, r_eos)
        each_chance_1[capacity] = []

        for demand, probability in chances:
            shortfall_values = calculation.calculate_shortfall(M_nf, demand, t)
            C_total = calculation.calculate_shortfall_costs(t, shortfall_values, C_penalty)
            total_expected_cost += C_total * probability
            each_chance_1[capacity].append(total_expected_cost)
        
        # store data
        expected_costs[capacity] = total_expected_cost

run_tree(fixed_decisions, chance_1)
# Print the results
print(each_chance_1)
for deployment, cost in expected_costs.items():
    print(f"Initial deployment {deployment}: Expected Cost = ${cost:.2f}")
