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
import numpy as np

def find_intersections(x_values, y_values):
    for i in range(1, len(y_values)):
        y1, y2 = y_values[i-1], y_values[i]
        if y1 * y2 <= 0:  # where it changes sign
            x1, x2 = x_values[i-1], x_values[i]
            # Linear interpolation formula to find the x-value where y = 0
            return(x1 - y1 * (x2 - x1) / (y2 - y1))
            
# alpha_penalty = [1 * 20 * 365 * 24]
alpha_penalty = [54750 * i for i in range(0, 33)]
print(alpha_penalty)
graph = []
for alpha in alpha_penalty:
    cm.main(alpha)
    ep.main()
    graph.append([alpha, cd.main(plot=True)])

'''
plotting the difference between the best inflexible and flexible
'''
results = {}
for alpha_val, values in graph:
    for typ, result in values:
        if typ not in results:
            results[typ] = []
        results[typ].append((alpha_val, result))
fig, ax = plt.subplots()
i = 0
color = [(r/255, g/255, b/255) for r, g, b in [[163, 206, 220], [93, 120, 105], [70, 70, 100],  [118, 118, 118]]]
for typ, points in results.items():
    alpha_vals, res = zip(*points)
    ax.plot(res, alpha_vals, label=typ, color=color[i])
    i += 1
ax.set_xlabel('E[LCOE]')
ax.set_ylabel('$ per kW missed')
ax.legend()
plt.show()

x_results, y_results = [], []
vert_line = 0
for alpha_val, values in graph:
    best_inflex, best_flex = min(values[0][1], values[1][1]), min(values[2][1], values[3][1])
    x_results.append(alpha_val/(20*365*24))
    y_results.append(best_inflex - best_flex)
    if best_inflex - best_flex > 0: vert_line = alpha_val/(20*365*24)

# Convert y_results to a numpy array
y_results = np.array(y_results)

# Create the plot
plt.plot(x_results, y_results, color='0.3', linestyle='-')
plt.fill_between(x_results, y_results, 0, hatch = '/', edgecolor = '0.5', facecolor='0.8')
plt.xlabel('Penalty for Energy Shortage ($/kWh)')
plt.ylabel('Benefit of Flexibility over Inflexibility ( ΔE[LCOE] )')
plt.axvline(x=(find_intersections(x_results, y_results)), color='0.5', linestyle='--')
plt.axhline(y=0, color='0.3', linestyle='-')
plt.grid(True)
plt.tight_layout() 
plt.ylim(y_results[-1], y_results[0])
plt.xlim(0, 10)
plt.xticks([i for i in range(0, 11)])
plt.yticks([i for i in range(int(y_results[-1]-1), int(y_results[0])+2)])
plt.show()