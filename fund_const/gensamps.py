import numpy as np
import optparse as op
from scipy.stats import norm
from pathlib import Path
from figaro.utils import make_gaussian_mixture

np.random.seed(1)
n_draws = 1000

if __name__ == '__main__':

    parser = op.OptionParser()
    parser.add_option("-i", "--input", type = "string", dest = "samples_file")
    parser.add_option("-o", "--output", type = "string", dest = "out_folder")
    parser.add_option("-b", "--bounds", type = "string", dest = "bounds")
    (options, args) = parser.parse_args()
    
    filename     = Path(options.samples_file)
    exp_folder   = Path(options.out_folder, 'experiments').resolve()
    if not exp_folder.exists():
        exp_folder.mkdir()
    
    options.bounds = np.atleast_1d(eval(options.bounds))
    data  = np.genfromtxt(filename, names = True, dtype = (float, float, 'U16'))

    means = data['value']
    std   = data['sigma']
    names = data['label']
    
    draws = make_gaussian_mixture(np.atleast_2d(means).T, np.atleast_2d(std**2).T, probit = False, bounds = options.bounds, save = True, save_samples = True, out_folder = options.out_folder)
    
    mins = []
    maxs = []

    for m, s, n in zip(means, std, names):
        samps = norm(loc = m, scale = s).rvs(n_draws)
        mins.append(samps.min())
        maxs.append(samps.max())
        np.savetxt(Path(exp_folder, n+'.txt'), samps)
    
    print('Min sample: {0}\nMax sample: {1}'.format(np.min(mins), np.max(maxs)))
