"""
runAnalysis.py

Main script to run the analysis and generate CDF (Section 5.1)

This file contains functions to:
    1) main_tree: Runs the model using a decision tree approach with varying alpha_penalty values, generates CDF plots, and allows for choosing the best options based on expected payoffs.
    2) main_sim: Runs the simulation model with varying alpha_penalty values, processes demand and cost models, and generates CDF plots.
    3) main: Executes the main_tree and main_sim functions with default or specified parameters, integrating demand and cost models, and producing cumulative distribution results.
"""

import sys
sys.path.append('src/utils/models')
import costModel as cm
import demandModel as dm
sys.path.append('src/utils/analysis')
import expectedPayoff as ep
import cumulativeDistribution as cd

# intersection for E[LCOE]          
alpha_penalty = 5 * 20 * 365 * 24

def main_tree(alpha=5*20*365*24, simulation=False, plot=True, choose_best=True, discount=0.05):
    cm.main(alpha=alpha, simulation=simulation, discount=discount)
    ep.main()
    cd.main_tree(plot=plot, choose_best=choose_best)

def main_sim(alpha=5 * 20 * 365 * 24,simulation=True,plot=True):
    dm.main()
    cm.main(alpha=alpha, simulation=simulation)
    cd.main_sim(plot=plot)

if __name__ == "__main__":
    main_tree(alpha=5*20*365*24, simulation=False, plot=True, choose_best=False, discount=0.05)
    main_sim(alpha=alpha_penalty)