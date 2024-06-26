"""
expectedPayoff.py

Read the "decision_tree_outcome.csv" file and calculate the expected payoff for each implementation method.

This file contains functions to:
    1) main: Reads the decision tree outcomes from a CSV file, processes flexible implementation methods, and calculates the expected LCOE for each method.
    2) combine_flexible_methods: Combines flexible implementation methods with the same initial capacity.
    3) analyse_flexible_40: Analyzes and calculates the expected LCOE for flexible_40 methods.
    4) analyse_flexible_30: Analyzes and calculates the expected LCOE for flexible_30 methods.
    5) save_expected_LCOE: Saves the calculated expected LCOE values to a CSV file.
"""

import csv
from collections import defaultdict

def main(first_prob = [1/3, 1/3, 1/3]):
    filename = "src/utils/data/processed/decision_tree_outcome.csv"
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        expected_payoffs = list(reader)

    """
    Combine flexible implementation methods with the same initial capacity.
    """
    flexible_30 = []
    flexible_40 = []
    expected_LCOE = []

    for i in range(len(expected_payoffs)):
        if "flexible_30_" in expected_payoffs[i][0]:
            flexible_30.append(expected_payoffs[i])
        elif "flexible_40_" in expected_payoffs[i][0]:
            flexible_40.append(expected_payoffs[i])
        else:
            expected_LCOE.append(expected_payoffs[i])

    '''
    analyse flexible_40 first
    '''
    new_flexible_40 = defaultdict(list)

    new_flexible_40['high'] += (flexible_40[2][1:4])
    new_flexible_40['high'] += (flexible_40[1][1:4])
    new_flexible_40['high'] += (flexible_40[0][1:4])
    new_flexible_40['med']  += (flexible_40[2][4:7])
    new_flexible_40['med']  += (flexible_40[1][4:7])
    new_flexible_40['med']  += (flexible_40[0][4:7])
    new_flexible_40['low']  += (flexible_40[0][7:])
    new_flexible_40['low']  += (flexible_40[1][7:])
    new_flexible_40['low']  += (flexible_40[2][7:])
    # print for treeage
    # print("flexible_40")
    # print(new_flexible_40)
    # print()

    # converting to expected lcoe * probability 2 (e.g., $41.55/kWh * 0.7)
    temp_1 = []
    for type in ['high', 'med', 'low']:
        temp_2 = []
        expected_payoffs = list(map(float, new_flexible_40[type]))
        prob_payoffs = [expected_payoffs[i]*first_prob[i%3] for i in range(9)]
        min_i, min_val = 0, float('inf')
        for i in range(3):
            temp_2.append([i, sum(prob_payoffs[i*3:i*3+3]), expected_payoffs[i*3:i*3+3]])
            if temp_2[i][1] < min_val:
                min_val = temp_2[i][1]
                min_i = i
        temp_1 += temp_2[min_i][2]
    expected_LCOE.append(["flexible_40"] + temp_1)

    '''
    analyse flexible_30 next
    '''
    new_flexible_30 = defaultdict(list)

    new_flexible_30['high'] += (flexible_30[2][1:4])
    new_flexible_30['high'] += (flexible_30[1][1:4])
    new_flexible_30['high'] += (flexible_30[0][1:4])
    new_flexible_30['med']  += (flexible_30[2][4:7])
    new_flexible_30['med']  += (flexible_30[1][4:7])
    new_flexible_30['med']  += (flexible_30[0][4:7])
    new_flexible_30['low']  += (flexible_30[0][7:])
    new_flexible_30['low']  += (flexible_30[1][7:])
    new_flexible_30['low']  += (flexible_30[2][7:])
    # print for treeage 
    # print("flexible_30")
    # print(new_flexible_30)
    # print()

    # converting to expected lcoe * probability 1
    temp_1 = []
    for type in ['high', 'med', 'low']:
        temp_2 = []
        expected_payoffs = list(map(float, new_flexible_30[type]))
        prob_payoffs = [expected_payoffs[i]*first_prob[i%3] for i in range(9)]
        min_i, min_val = 0, float('inf')
        for i in range(3):
            temp_2.append([i, sum(prob_payoffs[i*3:i*3+3]), expected_payoffs[i*3:i*3+3]])
            if temp_2[i][1] < min_val:
                min_val = temp_2[i][1]
                min_i = i
        temp_1 += temp_2[min_i][2]
    expected_LCOE.append(["flexible_30"] + temp_1)

    # Save expected LCOE as a CSV file
    output_filename = "src/utils/data/processed/decision_tree_optimal_path.csv"
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(expected_LCOE)

if __name__ == "__main__":
    main()