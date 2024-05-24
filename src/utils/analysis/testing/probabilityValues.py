"""
probabilityValues.py - sensitivity analysis
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('tools')
from design import colors
sys.path.append('src/utils/models')
import costModel as cm
sys.path.append('src/utils/analysis')
import expectedPayoff as ep
import cumulativeDistribution as cd

def main():
    probabilities = generate_prob_1()
    total = []
    res = []
    probabilities.sort(key=lambda x: x[0])
    index = 0
    cm.main(alpha=5*20*365*24)
    for prob in probabilities:
        if index != prob[0]*100:
            index = prob[0]*100
            total.append(res)
            res = []
        ep.main(prob)
        res.append([[prob[1], prob[2]], label_results((cd.main_tree([prob,calculate_prob_2(prob)], plot=False, choose_best=False)))])
        res.sort(key=lambda x: x[1])
    for res in total:
        print(res)
        plot_results(res)

def generate_prob_1():
    probabilities = []
    for x1 in range(0, 11):
        for x2 in range(0, 101):
            for x3 in range(0, 101):
                if x1 + x2 + x3 <= 100:
                    probabilities.append([x1*0.1, x2*0.01, x3*0.01])
            # x1_value = x1
            # x2_value = x2
            # x3_value = 10 - x1_value - x2_value
            # if x1_value + x2_value + x3_value == 10 and x3_value >= 0:
            #     probabilities.append([round(x1_value*0.1, 1), round(x2_value*0.1, 1), round(x3_value*0.1, 1)])
    return probabilities

def calculate_prob_2(prob): # bayes' theorem
    EVSI = np.array([
        [0.7, 0.2, 0.1],
        [0.2, 0.6, 0.2],
        [0.1, 0.2, 0.7]
    ])
    # marginal probabilities for B_j
    P_B = np.dot(EVSI, np.array(prob))
    # apply Bayes' theorem to update probabilities
    P_A_given_B = np.zeros((3, 3))
    for j in range(3):
        for i in range(3):
            P_A_given_B[i, j] = (EVSI[i, j] * prob[i]) / P_B[j]
    res = []
    for j in range(3):
        for i in range(3):
            res.append(P_A_given_B[i, j])
    return res

def label_results(mean): # mean = [['desc', val]]
    max_desc = max(mean, key=lambda x: x[1])[0]
    if max_desc == 'inflexible_50':
        return colors["blue"]
    if max_desc == 'inflexible_60':
        return colors["dark_blue"]
    if max_desc == 'flexible_40':
        return colors["purple"]
    if max_desc == 'flexible_30':
        return colors["dark_purple"]
    
def plot_results(res): # res = [[[x, y], 'desc']...]
    x = [item[0][0] for item in res]
    y = [item[0][1] for item in res]
    desc = [item[1] for item in res]
    
    plt.scatter(x, y, c=desc)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.xlabel('probability_mid')
    plt.ylabel('probability_low')
    plt.show()

if __name__ == "__main__":
    print(calculate_prob_2)
    main()