"""
getting the E[LCOE] with different alpha_penalty values
"""

import matplotlib.pyplot as plt
import sys
sys.path.append('tools')
from design import colors
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
alpha_penalty = [54750/2 * i for i in range(0, 66)]
# print([_/(20*365*24) for _ in alpha_penalty])
graph = []
for alpha in alpha_penalty:
    cm.main(alpha)
    ep.main()
    graph.append([alpha, cd.main(plot=False, choose_best=False)])

'''
plotting the difference between the best inflexible and flexible
'''
x_results, y_results = [], []
for alpha_val, values in graph:
    best_inflex, best_flex = min(values[0][1], values[1][1]), min(values[2][1], values[3][1])
    x_results.append(alpha_val/(20*365*24))
    y_results.append(best_inflex - best_flex)

# Convert y_results to a numpy array
y_results = np.array(y_results)

# Create the plot
intersect = find_intersections(x_results, y_results)

plt.plot(x_results, y_results, color='0.3', linestyle='-')
plt.grid(axis='y', zorder=3)
plt.fill_between(x_results, y_results, 0, hatch = '//', edgecolor = colors["dark_green"], facecolor=colors["green"], zorder=2, label = 'Positive Difference')
plt.fill_between(x_results, y_results, 0, where = x_results > intersect, hatch = '//', edgecolor = colors["dark_red"], facecolor=colors["red"], zorder=2, label = 'Negative Difference')
plt.rcParams.update({'mathtext.default':  'regular' })
plt.xlabel('Cost Penalty for Energy Shortage [$/kWh]')
plt.ylabel('Expected Value of Flexibility [$/kWh]')
plt.axvline(x=intersect, color=colors["dark_grey"], linestyle='--')
plt.axhline(y=0, color='0', linestyle='-')
plt.tight_layout() 
plt.ylim(y_results[-1], y_results[0])
plt.xlim(0, 10)
plt.xticks([i for i in range(0, 11)])
plt.yticks([i for i in range(int(y_results[-1]-1), int(y_results[0])+2)])
plt.legend()
plt.show()