"""
discountRate.py

Getting the E[LCOE] with different discount_rate values (Section 5.2)

This file contains functions to:
    1) main: Runs the model with varying discount rates, performs simulations or tree-based evaluations, and plots the results to analyze the expected value of flexibility.
    2) find_intersections: Identifies the x-value where the y-value crosses zero, indicating a change in sign using linear interpolation.
    3) comparative_analysis: Compares the results of the simulations or tree evaluations, identifying the best flexible and inflexible options and calculating their differences.
    4) plot_graph: Plots the results of the comparative analysis, highlighting regions where flexibility provides positive or negative differences in expected values.
"""


import matplotlib.pyplot as plt
import sys
sys.path.append('tools')
from design import colors
sys.path.append('src/utils/models')
import costModel as cm
import demandModel as dm
sys.path.append('src/utils/analysis')
import expectedPayoff as ep
import cumulativeDistribution as cd
import numpy as np

def main(simulation=False, plot=False, discount_rates=[0.05]):
    graph = []
    if simulation:
        dm.main(plot=plot)
    for d in discount_rates:
        cm.main(discount = d, simulation = simulation)
        ep.main()
        graph.append([d, cd.main_tree(plot=plot, choose_best=False)[0]])
    x_results, y_results = comparative_analysis(graph)
    intersect = find_intersections(x_results, y_results)
    plot_graph(x_results, y_results, intersect)
    return x_results, y_results # discount rate, expected value of flex.

def find_intersections(x_values, y_values):
    for i in range(1, len(y_values)):
        y1, y2 = y_values[i-1], y_values[i]
        if y1 * y2 <= 0:  # where it changes sign
            x1, x2 = x_values[i-1], x_values[i]
            # Linear interpolation formula to find the x-value where y = 0
            return(x1 - y1 * (x2 - x1) / (y2 - y1))
            
def comparative_analysis(graph):
    x_results, y_results = [], []
    for d, values in graph:
        if len(values) == 4:
            best_inflex, best_flex = min(values[0][1], values[1][1]), min(values[2][1], values[3][1])
        elif len(values) == 2:
            best_inflex, best_flex = values[1][1], values[0][1]
        x_results.append(d)
        y_results.append(best_inflex - best_flex)
    y_results = np.array(y_results)
    return x_results, y_results

def plot_graph(x_results, y_results, intersect):
    plt.plot(x_results, y_results, color='0.3', linestyle='-')
    plt.grid(axis='y', zorder=3)
    plt.fill_between(x_results, y_results, 0, hatch = '//', edgecolor = colors["dark_green"], facecolor=colors["green"], zorder=2, label = 'Positive Difference')
    if intersect: 
        plt.fill_between(x_results, y_results, 0, where = x_results > intersect, hatch = '//', edgecolor = colors["dark_red"], facecolor=colors["red"], zorder=2, label = 'Negative Difference')
        plt.axvline(x=intersect, color=colors["dark_grey"], linestyle='--')
    plt.xlabel('Discount Rate (r_discount)')
    plt.ylabel('Expected Value of Flexibility [$/kWh]')
    plt.axhline(y=0, color='0', linestyle='-')
    plt.tight_layout() 
    plt.ylim(0, 22)
    plt.xlim(0, 0.5)
    plt.xticks([i*0.1 for i in range(0, 11)])
    # plt.yticks([i for i in range(int(y_results[-1]-1), int(y_results[0])+2)])
    plt.legend()
    plt.savefig(f'src/utils/analysis/testing/figures/discount_rate_sensitivity_analysis.png')
    plt.show()

if __name__ == "__main__":
    discount_rate = [0.01 * i for i in range(0, 101)]
    # print(discount_rate)
    simulation = False
    plot = False
    main(simulation, plot, discount_rate)