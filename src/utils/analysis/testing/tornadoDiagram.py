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

# Tornado Diagram
def tornado():
    fig, ax1 = plt.subplots(figsize=(4, 5))
    bars = ax1.barh(variables[0], r_change[1], left=base_val_r, color=colors['green'], height=0.4)
    ax1.barh(variables[0], -r_change[0], left=base_val_r, color=colors['red'], height=0.4)
    bars = ax1.barh(variables[1], a_change[1], left=base_val_a, color=colors['red'], height=0.4)
    ax1.barh(variables[1], -a_change[0], left=base_val_a, color=colors['green'], height=0.4)
    for base_value in [base_val_r, base_val_a]:
        ax1.axvline(x=base_value, color='black', linestyle='-', linewidth=2)
    ax1.xaxis.set_major_locator(plt.MultipleLocator(2))
    ax1.grid(axis='x', which='both', color='gray', linestyle='--', linewidth=0.5)
    ax1.set_yticklabels(variables, rotation=90, ha='right')
    ax1.xaxis.set_label_position('bottom')
    ax1.xaxis.tick_top()
    ax1.set_xlabel('Expected Value of Flexibility', fontsize=10)
    ax1.set_title('')
    plt.show()

def case_boundaries():
    # Define the data
    variables = ['a', 'r']
    positions = [0, 1]

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(6, 8))

    bars = ax.barh(0, -1, left=0, color=colors['red'], height=0.4)
    ax.barh(0, 1, left=0, color=colors['green'], height=0.4)
    bars = ax.barh(1, -1, left=0, color=colors['red'], height=0.4)
    ax.barh(1, 1, left=0, color=colors['green'], height=0.4)
    ax.axvline(x=-1, color='gray', linestyle='--')
    ax.axvline(x=0, color='gray', linestyle='--')
    ax.axvline(x=1, color='gray', linestyle='--')
    ax.set_xticks([-1, 0, 1])
    ax.set_xticklabels(['low', 'base', 'high'], fontsize=14)
    ax.set_yticks(positions)
    ax.yaxis.set_ticks_position('none')
    ax.set_xlabel('Case Boundaries', fontsize=16)
    ax.xaxis.set_label_position('bottom')
    ax.xaxis.tick_top()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('none')

    ax.text(-1, 0, '0.00', ha='center', va='center', fontsize=20, bbox=dict(facecolor='white', edgecolor='black'))
    ax.text(0, 0, '0.05', ha='center', va='center', fontsize=20, bbox=dict(facecolor='white', edgecolor='black'))
    ax.text(1, 0, '1.00', ha='center', va='center', fontsize=20, bbox=dict(facecolor='white', edgecolor='black'))

    ax.text(-1, 1, '0', ha='center', va='center', fontsize=20, bbox=dict(facecolor='white', edgecolor='black'))
    ax.text(0, 1, '5', ha='center', va='center', fontsize=20, bbox=dict(facecolor='white', edgecolor='black'))
    ax.text(1, 1, '10', ha='center', va='center', fontsize=20, bbox=dict(facecolor='white', edgecolor='black'))
    
    plt.tight_layout()
    plt.show()

case_boundaries()