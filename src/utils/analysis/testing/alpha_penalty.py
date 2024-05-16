"""
getting the E[LCOE] with different alpha_penalty values
"""

import matplotlib.pyplot as plt
import sys
sys.path.append('src/utils/models')
import costModel as cm
sys.path.append('src/utils/analysis')
import expectedPayoff as ep
import cumulativeDistribution as cd

alpha_penalty = [500000]
alpha_penalty = [5000 * i for i in range(0, 400)]
graph = []
for alpha in alpha_penalty:
    cm.main(alpha)
    ep.main()
    graph.append([alpha, cd.main(plot=False)])

'''
plotting methods
'''
# results = {}
# for alpha_val, values in graph:
#     for typ, result in values:
#         if typ not in results:
#             results[typ] = []
#         results[typ].append((alpha_val, result))
# fig, ax = plt.subplots()
# i = 0
# color = [(r/255, g/255, b/255) for r, g, b in [[163, 206, 220], [93, 120, 105], [70, 70, 100],  [118, 118, 118]]]
# for typ, points in results.items():
#     alpha_vals, res = zip(*points)
#     ax.plot(res, alpha_vals, label=typ, color=color[i])
#     # for x, y in zip(res, alpha_vals):
#         # ax.text(x, y, f'{x:.2f}', ha='center', va='bottom')
#     i += 1
# ax.set_xlabel('E[LCOE]')
# ax.set_ylabel('$ per kW missed')
# ax.legend()
# plt.show()

x_results, y_results = [], []
vert_line = 0
for alpha_val, values in graph:
    best_inflex, best_flex = min(values[0][1], values[1][1]), min(values[2][1], values[3][1])
    x_results.append(alpha_val/(20*365*24))
    y_results.append(best_inflex - best_flex)
    if best_inflex - best_flex > 0: vert_line = alpha_val/(20*365*24)

# Create the plot
plt.plot(x_results, y_results, color = '0.3', linestyle='-')
plt.xlabel('Penalty for Energy Shortage ($/kWh)')
plt.ylabel('E[LCOE] Benefit of Flexibility over Inflexibility ($/kWh)')
plt.axvline(x=vert_line, color='0.5', linestyle='--')
plt.show()