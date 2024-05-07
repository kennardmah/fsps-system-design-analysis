import numpy as np
import capacityModel
import csv

"""
costModel.py – calculate the cost at each time step and return the total cost
"""

# Penalty Integral Calculation
def calculate_C_penalty(capacity, demand, t, alpha_penalty = 0):
    integral = max(0, demand[t]-capacity[t])
    return alpha_penalty * integral

# Development Cost
def calculate_C_capital(kW, mass_ratio = 3969/40, C_launch = 2720, C_produce = 43000, C_payload = 3500, r_eos = 0):
    M_nf = kW * mass_ratio
    M_components = 1621/40 * kW
    M_total = M_nf + M_components
    C_nf = (M_total) * C_launch + (M_nf * C_produce + (M_total) * C_payload) * (1 - r_eos)
    return C_nf

# Operational Cost at t
def calculate_C_operational(M_nf, M_components, cost_per_mass = 0):
    return (M_nf + M_components) * cost_per_mass

def add_C_capital(cost_over_time, kW, t):
    cost_over_time[t] += calculate_C_capital(kW)
    return cost_over_time

def C_total(implementation_method, mass_over_time, capacity_over_time, demand_scenarios):
    cost_over_time = [0 for _ in range(21)]
    # add implementation cost
    for t, val in enumerate(implementation_method):
        cost_over_time = add_C_capital(cost_over_time, val, t)
    # print("C_Cap",  cost_over_time)
    # add operational cost
    for t, val in enumerate(mass_over_time):
        cost_over_time[t] += calculate_C_operational(val[0], val[1])
    # print("C_op", cost_over_time)
    # add penalty cost
    results = []
    for demand in demand_scenarios:
        cost = cost_over_time.copy()
        for t in range(21):
            cost[t] += calculate_C_penalty(capacity_over_time, demand, t)
        # print("C_pen", cost)
        results.append(sum(cost))
    return results

def E_total(capacity_over_time, demand_scenarios):
    results = []
    for demand in demand_scenarios:
        energy_over_time = [0 for _ in range(21)]
        for t, val in enumerate(capacity_over_time):
            energy_over_time[t] = (min(val, demand[t]))*8760
        results.append(sum(energy_over_time))
    return results

if __name__ == '__main__':
    # read csv files from data folder
    with open('src/utils/data/implementation_methods.csv', 'r') as file:
        reader = csv.reader(file)
        implementation_methods = list(reader)
    with open('src/utils/data/capacity_over_time.csv', 'r') as file:
        reader = csv.reader(file)
        capacity_over_time = list(reader)
    with open('src/utils/data/demand_scenarios.csv', 'r') as file:
        reader = csv.reader(file)
        demand_scenarios = [list(map(float, row)) for row in reader]

    for implementation_method, capacity_over_time in zip(implementation_methods, capacity_over_time):
        if implementation_method[0] != capacity_over_time[0]:
            print("-----------------------\nERROR: Mismatched implementation methods and capacity over time\n-----------------------")
            break
        implementation_method = list(map(float, implementation_method[1:]))
        capacity_over_time = list(map(float, capacity_over_time[1:]))
        # print(implementation_method)
        # print(capacity_over_time)
        C_outcome = C_total(implementation_method, capacityModel.measure_mass(implementation_method), capacity_over_time, demand_scenarios)
        E_outcome = E_total(capacity_over_time, demand_scenarios)
        LCOE = [c/e for c, e in zip(C_outcome, E_outcome)]
        print(f"{implementation_method[0]}: {LCOE}")