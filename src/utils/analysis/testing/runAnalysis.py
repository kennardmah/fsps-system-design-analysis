import sys
sys.path.append('src/utils/models')
import costModel as cm
import demandModel as dm
sys.path.append('src/utils/analysis')
import expectedPayoff as ep
import cumulativeDistribution as cd

# intersection for E[LCOE]          
# alpha_penalty = 6.195569213940132 * 20 * 365 * 24

alpha_penalty = 1 * 20 * 365 * 24
# alpha_penalty = 500000

def main_tree():
    cm.main(alpha=175200, simulation=False)
    ep.main()
    cd.main_tree(plot=True, choose_best=True)

def main_sim():
    dm.main()
    cm.main(alpha= 6.195569213940132 * 20 * 365 * 24, simulation=True)
    cd.main_sim()

if __name__ == "__main__":
    main_sim()