import sys
sys.path.append('/Users/kennardmah/Documents/GitHub/masters-thesis-sustainable-lunar-energy/src/utils/models')

import capacityModel, demandModel, costModel
import numpy as np
import pandas as pd

EOPM = 40/3969

### robust strategy analysis
table = pd.DataFrame(columns=['Capacity', 'C_penalty', 'C_total'])
capacity = [70, 60, 50, 40]  # kW
demands = [44, 34.2, 24.4]
time = 21
penalty_values = np.linspace(2000000, 4000000, num=10)  # Range of C_penalty values, evenly spaced

for C_penalty in penalty_values:
    print(f'Analyzing for C_penalty: {C_penalty}')
    for cap in capacity:
        cap_over_time = capacityModel.nuclear_capacity_time(cap, time)
        M_nf = cap / EOPM
        M_components = cap / (40/1621)
        # Uncomment the next line to see M_nf and M_components values
        # print(M_nf, M_components)
        C_total = costModel.calculate_C_nf(M_nf, M_components, 2720, 43000, 3500, 0)
        each_outcome = []  # cost for each probability outcome
        for demand in demands:
            C_outcome = 0
            demand_over_time = demandModel.constant_demand(time, demand)
            for t in range(time):
                shortfall_costs = costModel.calculate_shortfall_costs(t, cap_over_time, demand_over_time, C_penalty, 0.1)
                C_outcome += shortfall_costs
            each_outcome.append(C_outcome)
        C_total += np.mean(each_outcome)
        table = table.append({'Capacity': cap, 'C_penalty': C_penalty, 'C_total': C_total}, ignore_index=True)
        print(f'The C_total for capacity {cap} kW is {C_total} USD')

table.to_csv('/Users/kennardmah/Documents/GitHub/masters-thesis-sustainable-lunar-energy/src/utils/analysis/robust_strategy_table.csv', index=False)