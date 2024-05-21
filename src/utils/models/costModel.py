import capacityModel
import csv
# import argparse


"""
costModel.py – calculate the cost at each time step and return the total cost
"""

def main(alpha=175200, simulation=False):
    
    with open('src/utils/data/raw/implementation_methods.csv', 'r') as file:
        reader = csv.reader(file)
        implementation_methods = list(reader)
    with open('src/utils/data/raw/capacity_over_time.csv', 'r') as file:
        reader = csv.reader(file)
        capacity_over_time = list(reader)
    if simulation == True:
        with open('src/utils/data/raw/demand_simulations.csv', 'r') as file:
            reader = csv.reader(file)
            demand_scenarios = [list(map(float, row[1:])) for row in reader]
            demand_scenarios = demand_scenarios[1:]
    else: 
        with open('src/utils/data/raw/demand_scenarios.csv', 'r') as file:
            reader = csv.reader(file)
            demand_scenarios = [list(map(float, row)) for row in reader]
    res = []
    for implementation_method, capacity_over_time in zip(implementation_methods, capacity_over_time):
        if implementation_method[0] != capacity_over_time[0]:
            print("-----------------------\nERROR: Mismatched implementation methods and capacity over time\n-----------------------")
            break
        desc = implementation_method[0]
        implementation_method = list(map(float, implementation_method[1:]))
        capacity_over_time = list(map(float, capacity_over_time[1:]))
        C_outcome = C_total(implementation_method, capacityModel.measure_mass(implementation_method), capacity_over_time, demand_scenarios, alpha)
        E_outcome = E_total(capacity_over_time, demand_scenarios)
        LCOE = [c/e for c, e in zip(C_outcome, E_outcome)]
        res.append([desc] + LCOE)
    if simulation == True:
        filename = "src/utils/data/raw/decision_tree_outcome_sim.csv"
    else: filename = "src/utils/data/processed/decision_tree_outcome.csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(res)

# Discounted Value Calculation
def discounted_value(cost, t, r_discount = 0.05):
    return cost/((1+r_discount)**t)

# Development Cost at time t
def calculate_C_capital(kW, mass_ratio = 3969/40, C_launch = 2720, C_produce = 43000, C_payload = 3500, r_eos = 0):
    M_nf = kW * mass_ratio
    M_components = 1621/40 * kW
    M_total = M_nf + M_components
    C_nf = (M_total) * C_launch + (M_nf * C_produce + (M_total) * C_payload) * (1 - r_eos)
    return C_nf

# Add Capital Cost at time t
def add_C_capital(cost_over_time, kW, t):
    cost_over_time[t] += calculate_C_capital(kW)
    return cost_over_time

# Operational Cost per year
def calculate_C_operational(M_nf, M_components, cost_per_mass = 2720):
    return (M_components) * cost_per_mass

# Penalty Calculation at time t
def calculate_C_penalty(capacity, demand, t, alpha_penalty = 0):
    integral = max(0, demand[t]-capacity[t])
    return alpha_penalty * integral

# Combined Cost Calculation
def C_total(implementation_method, mass_over_time, capacity_over_time, demand_scenarios, alpha = 0):
    cost_over_time = [0 for _ in range(21)]
    # add implementation cost
    for t, val in enumerate(implementation_method):
        cost_over_time = add_C_capital(cost_over_time, val, t)
    # add operational cost
    for t, val in enumerate(mass_over_time):
        cost_over_time[t] += calculate_C_operational(val[0], val[1])
    # add penalty cost
    res = []
    for demand in demand_scenarios:
        cost = cost_over_time.copy()
        for t in range(21):
            cost[t] += calculate_C_penalty(capacity_over_time, demand, t, alpha)
            # convert to discounted rate
            cost[t] = discounted_value(cost[t], t)
        res.append(sum(cost))
    return res

def E_total(capacity_over_time, demand_scenarios):
    res = []
    for demand in demand_scenarios:
        energy_over_time = [0 for _ in range(21)]
        for t, val in enumerate(capacity_over_time):
            energy_over_time[t] = discounted_value((min(val, demand[t]))*8760, t)
        res.append(sum(energy_over_time))
    return res

if __name__ == '__main__':
    main(simulation=True)
