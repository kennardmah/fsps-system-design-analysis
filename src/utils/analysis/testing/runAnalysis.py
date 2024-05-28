import sys
sys.path.append('src/utils/models')
import costModel as cm
import demandModel as dm
sys.path.append('src/utils/analysis')
import expectedPayoff as ep
import cumulativeDistribution as cd

# intersection for E[LCOE]          
alpha_penalty = 5 * 20 * 365 * 24

def main_tree(alpha=5*20*365*24, simulation=False, plot=True, choose_best=True):
    cm.main(alpha=alpha, simulation=simulation)
    ep.main()
    cd.main_tree(plot=plot, choose_best=choose_best)

def main_sim(alpha=6.195569213940132 * 20 * 365 * 24,simulation=True,plot=True):
    dm.main()
    cm.main(alpha=alpha, simulation=simulation)
    cd.main_sim(plot=plot)

if __name__ == "__main__":
    main_tree(alpha=5*20*365*24, simulation=False, plot=True, choose_best=False)
    # main_sim(alpha=alpha_penalty)