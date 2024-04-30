from scipy.optimize import minimize
import numpy as np
from power_capacity import nuclear_capacity, pv_capacity
from energy_demand_p1 import generate_demand_scenarios

def objective_function(x, num_periods, maintenance_cost_nuclear, maintenance_cost_pv, cost_pv_additional):
    """
    Calculates the total cost including initial implementation, maintenance, and additional installations.

    :param x: Array of decision variables [initial_nuclear_capacity, initial_pv_capacity] + [additional_pv_capacity for each period]
    :param num_periods: Number of time periods in the simulation
    :param maintenance_cost_nuclear: Maintenance cost per MW per period for nuclear
    :param maintenance_cost_pv: Maintenance cost per MW per period for PV
    :param cost_pv_additional: Cost per MW for additional PV installations
    :return: Total cost (scalar)
    """
    initial_nuclear_capacity = x[0]
    initial_pv_capacity = x[1]
    additional_pv_capacity = x[2:]  # Additional capacities in subsequent periods
    
    # Initial implementation cost
    total_cost = 1000 * initial_nuclear_capacity + 1200 * initial_pv_capacity  # Example cost values per MW
    
    # Maintenance and additional installation costs
    for period in range(num_periods):
        total_cost += (maintenance_cost_nuclear * initial_nuclear_capacity +
                       maintenance_cost_pv * (initial_pv_capacity + sum(additional_pv_capacity[:period + 1])))
        if period < len(additional_pv_capacity):
            total_cost += cost_pv_additional * additional_pv_capacity[period]
    
    return total_cost


def demand_constraint(x, demands, num_periods):
    """
    Chance constraint ensuring that capacity meets demand in at least 95% of scenarios for each period.

    :param x: Decision variables [initial_nuclear_capacity, initial_pv_capacity] + [additional_pv_capacity for each period]
    :param demands: Matrix of demand scenarios (rows are periods, columns are scenarios)
    :param num_periods: Number of time periods
    :return: Array of constraint values (should be non-negative to satisfy the constraints)
    """
    constraints = []
    initial_nuclear_capacity = x[0]
    initial_pv_capacity = x[1]
    additional_pv_capacity = x[2:]

    for period in range(num_periods):
        total_capacity = initial_nuclear_capacity + initial_pv_capacity + sum(additional_pv_capacity[:period + 1])
        period_demands = demands[period, :]
        probability_of_meeting_demand = np.mean(total_capacity >= period_demands)
        constraint_value = 0.95 - probability_of_meeting_demand
        constraints.append(constraint_value)
        # print(f"Period {period}: Capacity = {total_capacity}, Mean Demand = {np.mean(period_demands)}, Probability = {probability_of_meeting_demand}, Constraint = {constraint_value}")

    return np.array(constraints)


# Define parameters
num_periods = 10  # Number of periods
maintenance_cost_nuclear = 5  # Example maintenance costs
maintenance_cost_pv = 4
cost_pv_additional = 1300

# Define initial conditions and demand scenarios
initial_guess = [50, 50] + [10] * num_periods  # Initial capacities and additional capacities for each period
demands = np.random.normal(100, 20, (num_periods, 1000))  # Simulated demand scenarios

# Setup optimization
cons = {'type': 'ineq', 'fun': lambda x: demand_constraint(x, demands, num_periods)}
result = minimize(objective_function, initial_guess, args=(num_periods, maintenance_cost_nuclear, maintenance_cost_pv, cost_pv_additional), constraints=cons, method='SLSQP')

print("Optimal Capacities:", result.x)
