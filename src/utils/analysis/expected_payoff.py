"""
Read the "decision_tree_outcome.csv" file and calculate the expected payoff for each implementation method.
"""

import csv

filename = "src/utils/data/decision_tree_outcome.csv"
with open(filename, 'r') as file:
    reader = csv.reader(file)
    expected_payoffs = list(reader)

"""
Combine flexible implementation methods with the same initial capacity.
"""

flexible_30 = []
flexible_40 = []
first_prob = [1/3, 1/3, 1/3]
high_prob = [0.7, 0.2, 0.1]
med_prob = [0.1, 0.8, 0.1]
low_prob = [0.1, 0.2, 0.7]

for i in range(len(expected_payoffs)):
    if "flexible_30_" in expected_payoffs[i][0]:
        flexible_30.append(expected_payoffs[i])
    elif "flexible_40_" in expected_payoffs[i][0]:
        flexible_40.append(expected_payoffs[i])

print(flexible_30)
print(flexible_40)
    