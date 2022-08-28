import numpy as np
from utils import G_inference, plot_distribution
from pathlib import Path
import os

out_folder = Path('output')
if not out_folder.exists():
    out_folder.mkdir()

models = ['UN', 'JF', 'IG']
n_live_points = 1000

if __name__ == '__main__':
    import cpnest
    data = np.genfromtxt('newtonsConstantWithLabels.dat', names = True)

    means = []
    sigma = []

    for mod in models:
        print('Model {0}'.format(mod))
        M = G_inference(data['value'], data['sigma'], mod)
        work = cpnest.CPNest(M,
                            verbose = 0,
                            nlive = n_live_points,
                            maxmcmc = 5000,
                            nensemble = 1,
                            )
        work.run()
        post = work.posterior_samples.ravel()
        plot_distribution(post, mod, out_folder)
        
        means.append(post['m'].mean())
        sigma.append(post['s'].mean())
    # Remove files from CPNest
    [os.remove(f) for f in ['chain_{0}_0.txt'.format(n_live_points), 'chain_{0}_0.txt_evidence_0.txt'.format(n_live_points),'cpnest.log','header.txt']]
