import numpy as np
import optparse as op
from scipy.stats import norm
from pathlib import Path

np.random.seed(1)
n_draws = 1000

if __name__ == '__main__':

    parser = op.OptionParser()
    parser.add_option("-i", "--input", type = "string", dest = "samples_file")
    parser.add_option("-o", "--output", type = "string", dest = "out_folder")
    (options, args) = parser.parse_args()
    
    filename = Path(options.samples_file)
    exp_folder = Path(options.out_folder, 'experiments').resolve()
    if not exp_folder.exists():
        exp_folder.mkdir()

    data  = np.genfromtxt(filename, names = True, dtype = (float, float, 'U16'))

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
    
    print('Min sample: {0}\nMax sample: {1}'.format(np.min(mins), np.max(maxs)))
