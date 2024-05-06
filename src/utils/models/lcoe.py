'''
lcoe.py (levelised cost of electricity)
'''

def levelised_cost_of_electricity(c_total, p_demand, p_supply, t, r_discount):
    '''
    Calculate the levelised cost of electricity (LCOE) for a given total cost, total energy and number of years.
    '''
    num = c_total[t]/((1+r_discount)**t) # Discounted total cost
    den = min(p_demand[t], p_supply[t]) # Minimum of demand and supply
    return num/den