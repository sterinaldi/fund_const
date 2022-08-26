import numpy as np
from scipy.stats import norm
from pathlib import Path

np.random.seed(1)

n_draws = 1000

filename = Path('newtonsConstantWithLabels.dat')
exp_folder = Path('experiments').resolve()
if not exp_folder.exists():
    exp_folder.mkdir()

data  = np.genfromtxt(filename, names = True, dtype = (float, float, 'U10'))

means = data['value']
std   = data['sigma']
names = data['label']

mins = []
maxs = []

for m, s, n in zip(means, std, names):
    samps = norm(loc = m, scale = s).rvs(n_draws)
    mins.append(samps.min())
    maxs.append(samps.max())
    np.savetxt(Path(exp_folder, n+'.txt'), samps)
