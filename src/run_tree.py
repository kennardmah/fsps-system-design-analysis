import numpy as np
import calculation

# variables
fixed_decisions = [60, 50, 40]

chance_1 = [(44, 1/3), (34.2, 1/3), (24.4, 1/3)]
t = np.linspace(0, 10, 100)  # Time from 0 to 20 in 100 steps

# parameters
EOPM = 40/3969
C_launch = 2720
C_produce = 43000
C_payload = 3500
r = 0.1
C_penalty = 5000000

# Dictionary to hold expected costs for each fixed decision
expected_costs = {}
each_chance_1 = {}

for initial_deployment in fixed_decisions:

    M_nf = initial_deployment / EOPM
    M_components = initial_deployment / (40/1621)
    total_expected_cost = C_nf = calculation.calculate_costs(M_nf, M_components, C_launch, C_produce, C_payload, r)
    each_chance_1[initial_deployment] = []

    for demand, probability in chance_1:
        shortfall_values = calculation.calculate_shortfall(M_nf, demand, t)
        C_total = calculation.calculate_shortfall_costs(t, shortfall_values, C_penalty)
        total_expected_cost += C_total * probability
        each_chance_1[initial_deployment].append(total_expected_cost)
    
    # store data
    expected_costs[initial_deployment] = total_expected_cost

# Print the results
print(each_chance_1)
for deployment, cost in expected_costs.items():
    print(f"Initial deployment {deployment}: Expected Cost = ${cost:.2f}")
