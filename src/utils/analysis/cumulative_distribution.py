import csv
import matplotlib.pyplot as plt
import numpy as np

filename = "src/utils/data/processed/decision_tree_optimal_path.csv"
with open(filename, 'r') as file:
    reader = csv.reader(file)
    expected_payoffs = list(reader)

# define probabilities
second_prob = [0.7, 0.2, 0.1, 0.1, 0.8, 0.1, 0.1, 0.2, 0.7]
first_prob = [1/3, 1/3, 1/3]
for i in range(9):
    second_prob[i] *= first_prob[i%3]
    # Initialize an empty list to store all the data
    all_data = []
    legend = []

for outcomes in expected_payoffs:
    legend.append(outcomes[0])
    outcomes = list(map(float, outcomes[1:]))
    data = []
    for lcoe, prob in zip(outcomes, second_prob):
        data.extend([lcoe] * int(prob * 100))
    all_data.append(data)

color = [[163, 206, 220], [93, 120, 105], [70, 70, 100],  [118, 118, 118]]
color = [(r/255, g/255, b/255) for r, g, b in color]
mean = []
for i, data in enumerate(all_data):
    # plt.axvline(np.mean(data), linestyle='dotted', color=color[i])
    plt.hist(data, cumulative=True, bins=10, edgecolor='none', alpha=0.5, color=color[i])
    mean.append(np.mean(data))
plt.xlabel('LCOE')
plt.ylabel('Frequency')
plt.title('Histogram Distribution of LCOE')
plt.legend(legend)
for m, c in zip(mean, color):
    plt.axvline(m, linestyle='dashed', color=c)
plt.show()