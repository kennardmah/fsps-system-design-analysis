import sys
sys.path.append('src/utils/models')
import costModel as cm
sys.path.append('src/utils/analysis')
import expectedPayoff as ep
import cumulativeDistribution as cd
            
alpha_penalty = 500000

cm.main(alpha_penalty)
ep.main()
cd.main(plot=True, choose_best=True)