### what do I need

# case boundaries legend

# E[V_flex] = LCOE[inflex] - LCOE[flex]

import numpy as np
import matplotlib.pyplot as plt
import discountRate
import alphaPenalty
import sys
sys.path.append('tools')
from design import colors

alpha_penalty = [54750 * i for i in range(0, 33)]
discount_rate = [0.01 * i for i in range(0, 101)]
base_r = 0.05
base_a = 5

r, expected_val_r = discountRate.main(simulation=False, plot=False, discount_rates=discount_rate)
a, expected_val_a = alphaPenalty.main(simulation=False, plot=False, alpha_penalty=alpha_penalty)

for i, j in zip(r, expected_val_r):
    if i == base_r:
        base_val_r = j

for i, j in zip(a, expected_val_a):
    if i == base_a:
        base_val_a = j

min_r, max_r = min(expected_val_r), max(expected_val_r)
min_a, max_a = min(expected_val_a), max(expected_val_a)

r_change = [base_val_r - min_r, max_r - base_val_r]
a_change = [base_val_a - min_a, max_a - base_val_a]

# Prepare data for plotting
variables = ['Discount Rate (r)', 'Alpha Penalty (a)']
changes = [r_change, a_change]

# Plotting the tornado diagram
fig, ax = plt.subplots(figsize=(10, 6))

# Plot each bar for the changes in both directions
bars = ax.barh(variables, [r_change[1], a_change[1]], left=[base_val_r, base_val_a], color=colors['green'])
ax.barh(variables, [-r_change[0], -a_change[0]], left=[base_val_r, base_val_a], color=colors['red'])

ax.set_xlabel('Expected Value of Flexibility')
plt.legend(loc='upper right')
plt.grid(axis='x')
plt.show()