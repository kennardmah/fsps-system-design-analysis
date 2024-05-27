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

def main_test():
    probabilities = generate_prob_1()
    print(probabilities)
    res = []
    probabilities.sort(key=lambda x: x[0])
    cm.main(alpha=876000)
    for prob in probabilities:
        ep.main(prob)
        res.append([[prob[0], prob[1], prob[2]], label_results((cd.main_tree([prob,calculate_prob_2(prob)], plot=False, choose_best=False)))])
        res.sort(key=lambda x: x[1])
    plot_results_3d(res)

def main():
    probabilities = generate_prob_1()
    total = []
    res = []
    probabilities.sort(key=lambda x: x[0])
    index = 0
    cm.main(alpha=6*20*365*24)
    for prob in probabilities:
        if index != prob[0]*100:
            index = prob[0]*100
            total.append(res)
            res = []
        ep.main(prob)
        res.append([[prob[1], prob[2]], label_results((cd.main_tree([prob,calculate_prob_2(prob)], plot=False, choose_best=False)))])
        res.sort(key=lambda x: x[1])
    for res in total:
        # print(res)
        plot_results(res)

def generate_prob_1():
    probabilities = []
    # for x1 in range(0, 11):
    #     for x2 in range(0, 101):
    #         x3 = 100 - x1*10 - x2
    #         if x1*10 + x2 + x3 == 100 and x3 >= 0:
    #             probabilities.append([x1*0.1, x2*0.01, x3*0.01])
    for x1 in range(0, 101):
        for x2 in range(0, 101):
            x3 = 100 - x1 - x2
            if x1 + x2 + x3 == 100 and x3 >= 0:
                probabilities.append([x1*0.01, x2*0.01, x3*0.01])
    print(probabilities)
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
    min_desc = min(mean, key=lambda x: x[1])[0]
    if min_desc == 'inflexible_50':
        return colors["purple"]
    if min_desc == 'inflexible_60':
        return colors["dark_purple"]
    if min_desc == 'flexible_40':
        return colors["blue"]
    if min_desc == 'flexible_30':
        return colors["dark_blue"]
    
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

def plot_results_3d(res): # res = [[[x, y, z], 'desc']...]
    x = [item[0][0] for item in res]
    y = [item[0][1] for item in res]
    z = [item[0][2] for item in res]
    desc = [item[1] for item in res]
    legend = {
        colors["blue"]: "flexible_40",
        colors["dark_blue"]: "flexible_30",
        colors["purple"]: "inflexible_50"
    }
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c=desc)
    ax.set_xlabel('probability_high')
    ax.set_ylabel('probability_mid')
    ax.set_zlabel('probability_low')
    plt.legend(legend.keys(), legend.values(), loc='upper right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # print(calculate_prob_2([0, 0, 0.1]))
    main_test()
    # main()