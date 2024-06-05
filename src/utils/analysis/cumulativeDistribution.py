import csv
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import copy
import sys

sys.path.append('tools')
from design import colors

def main_tree(probabilities = [[1/3, 1/3, 1/3], [0.7, 0.2, 0.1, 0.2, 0.6, 0.2, 0.1, 0.2, 0.7]], plot = False, choose_best = False):

    # read in decision_tree_optimal_path.csv
    filename = "src/utils/data/processed/decision_tree_optimal_path.csv"
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        expected_payoffs = list(reader)
    # define probabilities
    first_prob, second_prob = probabilities[0], copy.deepcopy(probabilities[1])

    # initialize values and list for storing data
    for i in range(9):
        second_prob[i] *= first_prob[i%3]
        all_data = []
        legend = []

    # backward induction
    for outcomes in expected_payoffs:
        legend.append(outcomes[0])
        # print(outcomes[0])
        outcomes = list(map(float, outcomes[1:]))
        data = []
        for lcoe, prob in zip(outcomes, second_prob):
            data.append([lcoe, prob])
        # print(data)
        data.sort(key=lambda x: x[0])
        all_data.append(data)
    
    # color/labels for plotting
    color = [colors["blue"], colors["dark_blue"], colors["purple"], "orange"]
    mean = [["inflexible_50"], ["inflexible_60"], ["flexible_40"], ["flexible_30"]]
    best_flex, best_inflex = ['type', float('inf')], ['type', float('inf')]

    """
    this part is for filtering to only show the best inflexible and flexible
    """
    if choose_best:
        mean = [["inflex"], ["flexible"]]
        for i, data in enumerate(all_data):
            e_lcoe = np.dot([x[0] for x in data], [x[1] for x in data])
            if i < 2:
                if e_lcoe < best_inflex[1]:
                    best_inflex = [i, e_lcoe]
            else:
                if e_lcoe < best_flex[1]:
                    best_flex = [i, e_lcoe]
        all_data = [data for i, data in enumerate(all_data) if i in [best_inflex[0], best_flex[0]]]
        color = [colors["purple"], colors["blue"]]
        dark_color = [colors["dark_purple"], colors["dark_blue"]]
        legend = [legend[i] for i in [best_inflex[0], best_flex[0]]]
        legend = ['Inflexible', 'Flexible']
    left = float('inf')
    right = float('-inf')
    for i, data in enumerate(all_data):
        values = [x[0] for x in data]
        left = min(left, values[0] - 0.5)
        right = max(right, values[-1] + 1)
        probabilities = [x[1] for x in data]
        mean[i].append(np.dot(values, probabilities))
        cumulative_probabilities = []
        cumulative_prob = 0
        for prob in probabilities:
            cumulative_prob += prob
            cumulative_probabilities.append(cumulative_prob)
        if plot:
            if choose_best:
                plt.axvline(values[0], linestyle='dashed', color=dark_color[i], linewidth=1)
                plt.axvline(values[-1], linestyle='dashed', color=dark_color[i], linewidth=1)
                plt.annotate(f'E[LCOE]', xy=(mean[i][1] + 0.3, 0.1*(i+1)), xycoords='data', ha='left', fontsize=10, weight = 'bold', color=color[i])
                plt.annotate(f'= {mean[i][1]:.2f}', xy=(mean[i][1] + 0.3, 0.05 +0.1*i), xycoords='data', ha='left', fontsize=10, weight = 'semibold', color=color[i])
                plt.annotate(f'min[LCOE]', xy=(values[0] + 0.3, 0.85 - 0.1*i), xycoords='data', ha='left', fontsize=8, weight = 'bold', color=color[i])
                plt.annotate(f'= {values[0]:.2f}', xy=(values[0] + 0.3, 0.8-0.1*i), xycoords='data', ha='left', fontsize=8, weight = 'semibold', color=color[i])
                plt.annotate(f'max[LCOE]', xy=(values[-1] + 0.3, 0.85 - 0.1*i), xycoords='data', ha='left', fontsize=8, weight = 'bold', color=color[i])
                plt.annotate(f'= {values[-1]:.2f}', xy=(values[-1] + 0.3, 0.8 - 0.1*i), xycoords='data', ha='left', fontsize=8, weight = 'semibold', color=color[i])
            plt.step([0] + values, [0] + cumulative_probabilities, color = color[i], linestyle = "-", where='post')
    if plot:
        plt.xlabel('LCOE (Levelised Cost of Electricity) [$/kWh]')
        plt.ylabel('Cumulative Probability')
        plt.ylim(0, 1)
        plt.xlim(left=left)
        plt.xticks(list(plt.xticks()[0]), rotation=45)
        custom_lines = [Line2D([0], [0], color=c, lw=4) for c in color]
        plt.legend(custom_lines, legend, loc = 'lower right')
        plt.tight_layout()
        plt.grid(axis='y', linewidth=0.5)
        if choose_best:
            color = dark_color
        for m, c in zip(mean, color):
            plt.axvline(m[1], linestyle='dashed', color=c)
        plt.savefig(f'src/utils/analysis/testing/figures/cdf_lcoe_{choose_best}_{right-0.5}.png')
        plt.show()
    return mean

def main_sim(plot = True):
    process_simulation_outcomes()
    filename = "src/utils/data/processed/decision_tree_outcome_sim.csv"
    legend, values = [], []
    mean = []
    color = [colors["blue"], colors["dark_purple"], colors["dark_blue"], colors["purple"]]
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        expected_payoffs = list(reader)
    for row in expected_payoffs:
        values.append(list(map(float, row[1:])))
        legend.append(row[0])
        mean.append([row[0], np.mean(values[-1])])
        if plot:
            plt.annotate(f'E[LCOE]', xy=(mean[-1][1] + 0.3, 0.1), xycoords='data', ha='left', fontsize=9, weight = 'bold', color=color[legend.index(row[0])])
            plt.annotate(f'= {mean[-1][1]:.2f}', xy=(mean[-1][1] + 0.3, 0.05), xycoords='data', ha='left', fontsize=9, weight = 'semibold', color=color[legend.index(row[0])])
    for i, row_values in enumerate(values):
        sorted_values = sorted(row_values)
        if plot:
            plt.axvline(sorted_values[0], linestyle='dashed', color=color[i])
            plt.axvline(sorted_values[-1], linestyle='dashed', color=color[i])
            plt.annotate(f'min[LCOE]', xy=(sorted_values[0] + 0.3, 0.85 - 0.1*i), xycoords='data', ha='left', fontsize=8, weight = 'bold', color=color[i])
            plt.annotate(f'= {sorted_values[0]:.2f}', xy=(sorted_values[0] + 0.3, 0.8-0.1*i), xycoords='data', ha='left', fontsize=8, weight = 'semibold', color=color[i])
            plt.annotate(f'max[LCOE]', xy=(sorted_values[-1] + 0.3, 0.85 - 0.1*i), xycoords='data', ha='left', fontsize=8, weight = 'bold', color=color[i])
            plt.annotate(f'= {sorted_values[-1]:.2f}', xy=(sorted_values[-1] + 0.3, 0.8 - 0.1*i), xycoords='data', ha='left', fontsize=8, weight = 'semibold', color=color[i])
            cumulative_probabilities = np.arange(1, len(sorted_values) + 1) / len(sorted_values)
            plt.plot(sorted_values, cumulative_probabilities, color=color[i])
    if plot:
        custom_lines = [Line2D([0], [0], color=c, lw=4) for c in color]
        plt.legend(custom_lines, legend, loc = 'lower right')
        plt.xlabel('LCOE (Levelised Cost of Electricity) [$/kWh]')
        plt.ylabel('Cumulative Probability')
        plt.grid(axis='y', linewidth=0.5)
        plt.ylim(0, 1)
        plt.xlim(left = min(sorted(row_values)[0] for row_values in values) - 0.5, right = max(sorted(row_values)[-1] for row_values in values) + 5.3)
        for i in range(len(mean)):
            plt.axvline(mean[i][1], linestyle='dashed', color=color[i])
        plt.tight_layout()
        plt.savefig(f'src/utils/analysis/testing/figures/cdf_lcoe_sim_{round(mean[0][1])}{round(mean[1][1])}.png')
        plt.show()
    return mean

def process_simulation_outcomes():
    filename = "src/utils/data/raw/decision_tree_outcome_sim.csv"
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        e_lcoe = [[row[0]] + list(map(float, row[1:])) for row in reader]
    flexible, inflex = ["flexible"], ["inflex"]
    for i in range(1, len(e_lcoe[0])):
        min_flex_30, min_flex_40 = min([row[i] for row in e_lcoe[2:5]]), min([row[i] for row in e_lcoe[5:7]])
        flexible.append(min(min_flex_30, min_flex_40))
        inflex.append(min([row[i] for row in e_lcoe[0:2]]))
    e_lcoe = [flexible, inflex]
    filename = "src/utils/data/processed/decision_tree_outcome_sim.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(e_lcoe)
        

# testing
if __name__ == "__main__":
    # main_tree(plot=True, choose_best = False)
    print(main_tree(plot=True, choose_best = True))
    main_sim()
