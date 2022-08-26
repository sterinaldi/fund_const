import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from tqdm import tqdm
from numba import jit
from figaro.utils import *
from pathlib import Path
from par_inference import out_folder

@jit
def s_level(m1,m2,s1,s2):
    return abs(m1-m2)/(np.sqrt(s1**2+s2**2))

data = np.genfromtxt('newtonsConstantWithLabels.dat', names = True, dtype = (np.float64,np.float64,'|U10'))

vals  = np.array([[m,s] for m, s in zip(data['value'], data['sigma'])])

sigmas = np.array([s_level(v[0][0], v[1][0], v[0][1], v[1][1]) for v in combinations(vals, 2)])

print('Fraction of pairs above 3-sigma: {:0.3f}'.format(len(sigmas[sigmas > 3])/len(sigmas)))

fig, ax = plt.subplots()
ax.hist(sigmas, bins = int(np.sqrt(len(sigmas))), histtype = 'step', color = 'cadetblue')
ax.axvline(3, ls = '--', color = 'steelblue')
ax.annotate('$3\\sigma$', xy = (3,28), xytext = (2.6,28), xycoords = 'data', color = 'steelblue', rotation = 90, fontsize = 15)
ax.set_xlabel('$\\sigma$')
fig.savefig(Path(out_folder, 'sigma_level.pdf'), bbox_inches = 'tight')
