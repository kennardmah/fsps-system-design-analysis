import csv
import matplotlib.pyplot as plt
import numpy as np

def main():
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
            data.append([lcoe, prob])
        data.sort(key=lambda x: x[0])
        all_data.append(data)
    color = [(r/255, g/255, b/255) for r, g, b in [[163, 206, 220], [93, 120, 105], [70, 70, 100],  [118, 118, 118]]]
    mean = [["inflexible_50"], ["inflexible_60"], ["flexible_40"], ["flexible_30"]]
    for i, data in enumerate(all_data):
        values = [x[0] for x in data]
        probabilities = [x[1] for x in data]
        mean[i].append(np.dot(values, probabilities))
        cumulative_probabilities = []
        cumulative_sum = 0
        for prob in probabilities:
            cumulative_sum += prob
            cumulative_probabilities.append(cumulative_sum)
        plt.step(values, cumulative_probabilities, color = color[i], where='post', label='CDF')
    plt.xlabel('LCOE (Levelised Cost of Electricity)')
    plt.ylabel('Cumulative Probability')
    plt.legend(legend)
    for m, c in zip(mean, color):
        plt.axvline(m[1], linestyle='dashed', color=c)
    plt.show()
    return mean

if __name__ == "__main__":
    main()