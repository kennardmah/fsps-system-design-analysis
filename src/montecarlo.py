import numpy as np
import pandas as pd

def generate_demand_scenarios(annual_growth, initial_demand, std_dev, num_years, num_scenarios):
    """
    Generate energy demand scenarios using Monte Carlo simulation.

    :param annual_growth: Annual growth rate of demand (percentage)
    :param initial_demand: Initial energy demand at the starting period
    :param std_dev: Standard deviation of demand growth
    :param num_years: Number of years for which to forecast demand
    :param num_scenarios: Number of scenarios to simulate
    :return: DataFrame of demand scenarios
    """
    years = np.arange(num_years)
    scenarios = np.zeros((num_years, num_scenarios))
    
    for i in range(num_scenarios):
        growth_rates = np.random.normal(annual_growth, std_dev, num_years)
        scenarios[:, i] = initial_demand * np.cumprod(1 + growth_rates)
    
    return pd.DataFrame(scenarios, index=years, columns=[f'Scenario_{i+1}' for i in range(num_scenarios)])

# Example usage
if __name__ == "__main__":
    demand_scenarios = generate_demand_scenarios(0.02, 100, 0.01, 10, 1000)
    print(demand_scenarios.head())