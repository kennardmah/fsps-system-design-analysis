"""
Read the "decision_tree_outcome.csv" file and calculate the expected payoff for each implementation method.
"""

import csv
from collections import defaultdict
import numpy as np

def main():
    filename = "src/utils/data/processed/decision_tree_outcome.csv"
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        expected_payoffs = list(reader)

    """
    Combine flexible implementation methods with the same initial capacity.
    """

    flexible_30 = []
    flexible_40 = []
    first_prob = [1/3, 1/3, 1/3]
    expected_LCOE = []

    for i in range(len(expected_payoffs)):
        if "flexible_30_" in expected_payoffs[i][0]:
            flexible_30.append(expected_payoffs[i])
        elif "flexible_40_" in expected_payoffs[i][0]:
            flexible_40.append(expected_payoffs[i])
        else:
            expected_LCOE.append(expected_payoffs[i])

    # flexible_40 = [['flexible_40_0', '32.618132694441094', '32.618132694441094',
    #                 '36.04421844620991', '34.06612460153879', '34.06612460153879',
    #                 '37.82065185295815', '40.382395663922665', '40.382395663922665',
    #                 '45.76832454667622'], 
    #                 ['flexible_40_10', '36.09653052903419', '39.15732942000517', '45.055273057762385',
    #                  '37.50797357472049', '40.82381255046264', '47.27581481619769',
    #                  '43.501201427119376', '48.02524880757883', '57.21040568334527'],
    #                 ['flexible_40_20', '41.5497419079228', '46.9887953040062', '54.06632766931486',
    #                  '43.105693260167996', '48.98857506055517', '56.730977779437225',
    #                  '49.65772762080088', '57.6302985690946', '68.65248682001433']]

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