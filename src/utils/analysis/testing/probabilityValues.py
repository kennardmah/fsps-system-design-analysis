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

probabilities = []
increment = 0.1
tolerance = 1e-9  # small tolerance for floating point precision
print(colors)

for x1 in range(0, 11):
    for x2 in range(0, 11):
        x1_value = x1 * increment
        x2_value = x2 * increment
        x3_value = 1 - x1_value - x2_value
        if 0 - tolerance <= x3_value <= 1 + tolerance and abs(x3_value % increment) < tolerance:
            probabilities.append([round(x1_value, 1), round(x2_value, 1), round(x3_value, 1)])

for prob in probabilities:
    cm.main()
    ep.main(prob)
    cd.main()
print(probabilities)