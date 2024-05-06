'''
lcoe.py (levelised cost of electricity)
'''
import numpy as np

def levelised_cost_of_electricity(c_total, p_demand, p_supply, t, r_discount):
    '''
    Calculate the levelised cost of electricity (LCOE) for a given total cost, total energy and number of years.
    '''
    num = c_total[t]/((1+r_discount)**t) # Discounted total cost
    den = (min(p_demand[t], p_supply[t])/((1+r_discount)**t)) # Minimum of demand and supply
    return num, den

def lcoe_at_time(c_total, p_demand, p_supply, r_discount):
    '''
    Calculate the levelised cost of electricity (LCOE) for a given total cost, total energy and number of years.
    '''
    num, den = 0, 0
    for t in range(21):
        n, d = levelised_cost_of_electricity(c_total, p_demand, p_supply, t, r_discount)
        num += n
        den += d
    print(f"The LCOE is: {num/den}")
    return num/den

# testing
if __name__ == '__main__':
    c_total = [100 for x in range(21)]
    p_demand = [40 for x in range(21)]
    p_supply = [50 for x in range(21)]
    r_discount = 0.05
    print(lcoe_at_time(c_total, p_demand, p_supply, r_discount))