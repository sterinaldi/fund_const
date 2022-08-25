import numpy as np
from utils import G_inference, plot_distribution
from pathlib import Path
import cpnest

models = ['UN', 'JF', 'IG']

data = np.genfromtxt('newtonsConstantWithLabels.dat', names = True)
out_folder = Path('output')
if not out_folder.exists():
    out_folder.mkdir()

means = []
sigma = []

for mod in models:
    
    M = G_inference(data['value'], data['sigma'], mod)
    work = cpnest.CPNest(M,
                        verbose = 0,
                        nlive = 1000,
                        maxmcmc = 5000,
                        nensemble = 1,
                        )
    work.run()
    post = work.posterior_samples.ravel()
    plot_distribution(post, mod, out_folder)
    
    means.append(post['m'].mean())
    sigma.append(post['s'].mean())
    
np.savetxt(Path(out_folder, 'G_vals.txt'), np.array([models, means, sigma]).T, header = 'model m s', fmt = '%10s , %10.3f, %10.3f')
