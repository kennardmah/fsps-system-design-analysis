import sys
sys.path.append('src/utils/models')
import costModel as cm
sys.path.append('src/utils/analysis')
import expectedPayoff as ep
import cumulativeDistribution as cd

# intersection for E[LCOE]          
# alpha_penalty = 6.195569213940132 * 20 * 365 * 24

alpha_penalty = 1 * 20 * 365 * 24
# alpha_penalty = 500000

cm.main(alpha_penalty)
ep.main()
cd.main(plot=True, choose_best=True)

print(alpha_penalty/(20*365*24))