### what do I need

# case boundaries legend

# E[V_flex] = LCOE[inflex] - LCOE[flex]

import numpy as np
import matplotlib.pyplot as plt
import discountRate
import alphaPenalty

alpha_penalty = [54750 * i for i in range(0, 33)]
discount_rate = [0.01 * i for i in range(0, 101)]
base_r = 0.05
base_a = 876000

r, expected_val_r = discountRate.main(simulation=False, plot=False, discount_rates=discount_rate)
a, expected_val_a = alphaPenalty.main(simulation=False, plot=False, alpha_pealty=alpha_penalty)


# Calculate EVF for the entire range of r and a
evf_r = np.array([calculate_evf(r, 0) for r in r_values])
evf_a = np.array([calculate_evf(0, a) for a in a_values])

# Calculate the changes for tornado diagram
r_change = evf_r.max() - evf_r.min()
a_change = evf_a.max() - evf_a.min()

# Prepare data for plotting
variables = ['Discount Rate (r)', 'Alpha Penalty (a)']
changes = [r_change, a_change]
base_value = calculate_evf(0, 0)

# Plotting the tornado diagram
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(variables, changes, left=base_value - np.array(changes)/2, color=['blue', 'orange'])

# Add the base value text in the middle of the bars
for bar in bars:
    width = bar.get_width()
    ax.text(bar.get_x() + width / 2, bar.get_y() + bar.get_height() / 2,
            f'{base_value:.2f}', ha='center', va='center', color='black', fontsize=12)

ax.set_xlabel('Expected Value of Flexibility Change')
ax.set_title('Tornado Diagram for Sensitivity Analysis')
plt.grid(True)
plt.show()
