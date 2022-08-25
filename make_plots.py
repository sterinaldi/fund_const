import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
# This import is just for plotting purposes
from figaro.utils import plot_median_cr
from par_inference import out_folder


models = ['UN', 'JF', 'IG']

colors = {'UN':'r',
          'JF':'b',
          'IG':'g',
         }

data = np.genfromtxt('newtonsConstantWithLabels.dat')
G = np.genfromtxt(Path(out_folder, 'prob_G_UN.txt'), names = True)['G']

# Parametric inference
medians = {mod: np.genfromtxt(Path(out_folder, 'prob_G_{0}.txt'.format(med)), names = True)['50'] for mod in models}
G_vals_data = np.genfromtxt(Path(out_folder, 'G_vals.txt'), names = True)
G_vals = {mod:[m, s] for mod, m, s in zip(G_vals_data['model'], G_vals_data['m'], G_vals_data['s'])}

fig, ax = plt.figure()
for mod in models:
    ax.plot(G, medians[mod], color = colors[mod], label = mod)
ax.legend(loc = 0, frameon = False)
ax.set_xlabel('$G\\times10^{-11}\ [\mathrm{m}^3\mathrm{kg}^{-1}\mathrm{s}^{-2}]$')

fig.savefig(Path(out_folder, 'par_models.pdf'), bbox_inches = 'tight')
