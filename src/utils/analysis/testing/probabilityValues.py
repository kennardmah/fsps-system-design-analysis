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

def main():
    probabilities = generate_prob_1()
    for prob in probabilities:
        cm.main()
        ep.main(prob)
        cd.main()

def generate_prob_1(increment=0.1):
    probabilities = []
    tolerance = 1e-9  # small tolerance for floating point precision
    for x1 in range(0, 11):
        for x2 in range(0, 11):
            x1_value = x1 * increment
            x2_value = x2 * increment
            x3_value = 1 - x1_value - x2_value
            if 0 - tolerance <= x3_value <= 1 + tolerance and abs(x3_value % increment) < tolerance:
                probabilities.append([round(x1_value, 1), round(x2_value, 1), round(x3_value, 1)])
    return probabilities

def calculate_prob_2(prob): #prob = [0.1, 0.2, 0.7]
    

if __name__ == "__main__":
    main()