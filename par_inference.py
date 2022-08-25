import numpy as np
from utils import G_inference, plot_distribution
import cpnest

data = np.genfromtxt('newtonsConstantWithLabels.dat', names = True)

for mod in ['UN', 'JF', 'IG']:
    
    M = G_inference(data['value'], data['sigma'], mod)
    work = cpnest.CPNest(M,
                        verbose = 0,
                        nlive = 1000,
                        maxmcmc = 5000,
                        nensemble = 1,
                        )
    work.run()
    post = work.posterior_samples.ravel()
    plot_distribution(post, mod)
    
    
