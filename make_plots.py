import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
# This import is just for plotting purposes
from figaro.utils import plot_median_cr
from figaro.cumulative import fast_cumulative
from par_inference import out_folder
from seaborn import color_palette

palette =  color_palette('Paired', 3)

codata_val = 6.67430
codata_err = 0.00015

models = ['UN', 'JF', 'IG']

colors = {'UN':palette[1],
          'JF':palette[0],
          'IG':palette[2],
         }

linestyle = {'UN': '-',
             'JF': '--',
             'IG': '-.',
            }

data = np.genfromtxt('newtonsConstantWithLabels.dat', names = True, dtype = (np.float64, np.float64, '|U10'))

data['label'][np.where(data['label'] == 'HUSTT-18')] = 'HUST_T-18'
data['label'][np.where(data['label'] == 'HUSTA-18')] = 'HUST_A-18'

G = np.genfromtxt(Path(out_folder, 'prob_G_UN.txt'), names = True)['G']

# Parametric inference
medians = {mod: np.genfromtxt(Path(out_folder, 'prob_G_{0}.txt'.format(mod)), names = True)['50'] for mod in models}

fig, ax = plt.subplots()
for mod in models:
    medians[mod] = medians[mod]/np.sum(medians[mod]*(G[1]-G[0]))
    ax.plot(G, medians[mod], color = colors[mod], ls = linestyle[mod], label = '$\mathrm{'+mod+'}$')
    
ymin, ymax = ax.get_ylim()
hs = np.linspace(0, ymax, len(data['value'])+7)
for hi, v, s in zip(hs[7:], data['value'][::-1], data['sigma'][::-1]):
    ax.axhline(hi, lw = 0.03, c = 'k', ls = ':')
    ax.errorbar(v, hi, xerr = s, color = 'orange', marker = 'o', ms = 4)

# CODATA value
ax.axhline(hs[6], lw = 0.03, c = 'k', ls = ':')
ax.errorbar(codata_val, hs[6], xerr = codata_err, color = 'blue', marker = 'o', ms = 4)

# This work
for i, mod in enumerate(models):
    cdf = fast_cumulative(np.ascontiguousarray(medians[mod]*(G[1]-G[0])))
    pcs = [G[np.where(cdf < perc)].max() for perc in [0.05, 0.16, 0.50, 0.84, 0.95]]
    ax.axhline(hs[2*i], lw = 0.03, c = 'k', ls = ':')
    ax.errorbar(pcs[2], hs[2*i], xerr = np.atleast_2d([pcs[2]-pcs[0], pcs[4]-pcs[2]]).T, color = colors[mod], marker = 'o', ms = 4)
    ax.axhline(hs[2*i+1], lw = 0.03, c = 'k', ls = ':')
    ax.errorbar(pcs[2], hs[2*i+1], xerr = np.atleast_2d([pcs[2]-pcs[1], pcs[3]-pcs[2]]).T, color = colors[mod], marker = 'o', ms = 4)
    print('{0}: {1} - {2} + {3}. Conservative: - {4} + {5}'.format(mod, pcs[2], pcs[2]-pcs[1], pcs[3]-pcs[2], pcs[2]-pcs[0], pcs[4]-pcs[2]))

plt.yticks(hs[::-1], ['$\mathrm{'+l+'}$' for l in data['label']] + ['$\mathrm{CODATA}$', '$\mathrm{IG}$', '$\mathrm{IG - Conservative}$','$\mathrm{JF}$', '$\mathrm{JF - Conservative}$','$\mathrm{UN}$', '$\mathrm{UN - Conservative}$'])
ax.grid(visible = False)
ax.set_xlim(G.min(),G.max())
ax.legend(loc = 0, frameon = False)
ax.set_xlabel('$G\ [\\times10^{-11}\ \mathrm{m}^3\mathrm{kg}^{-1}\mathrm{s}^{-2}]$')

ax.tick_params(axis='y', which='major', labelsize=6)
fig.savefig(Path(out_folder, 'par_models.pdf'), bbox_inches = 'tight')

# Nonparametric inference
rec = np.genfromtxt(Path(out_folder, 'plots','prob_newtonG.txt'), names = True)

fig, ax = plt.subplots()
ax.fill_between(rec['x'], rec['95'], rec['5'], color = 'mediumturquoise', alpha = 0.5)
ax.fill_between(rec['x'], rec['84'], rec['16'], color = 'darkturquoise', alpha = 0.5)
# Median
ax.plot(rec['x'], rec['50'], lw = 1, color = 'steelblue')

ymin, ymax = ax.get_ylim()

hs = np.linspace(0, ymax, len(data['value'])+3)
for hi, v, s in zip(hs[3:], data['value'][::-1], data['sigma'][::-1]):
    ax.axhline(hi, lw = 0.03, c = 'k', ls = ':')
    ax.errorbar(v, hi, xerr = s, color = 'orange', marker = 'o', ms = 4)

# CODATA value
ax.axhline(hs[2], lw = 0.03, c = 'k', ls = ':')
ax.errorbar(codata_val, hs[2], xerr = codata_err, color = 'blue', marker = 'o', ms = 4)

# This work
cdf = fast_cumulative(np.ascontiguousarray(rec['50']*(G[1]-G[0])))
pcs = [rec['x'][np.where(cdf < perc)].max() for perc in [0.05, 0.16, 0.50, 0.84, 0.95]]
ax.axhline(hs[0], lw = 0.03, c = 'k', ls = ':')
ax.errorbar(pcs[2], hs[0], xerr = np.atleast_2d([pcs[2]-pcs[0], pcs[4]-pcs[2]]).T, color = 'steelblue', marker = 'o', ms = 4)
ax.axhline(hs[1], lw = 0.03, c = 'k', ls = ':')
ax.errorbar(pcs[2], hs[1], xerr = np.atleast_2d([pcs[2]-pcs[1], pcs[3]-pcs[2]]).T, color = 'steelblue', marker = 'o', ms = 4)
    
print('(H)DPGMM: {1} - {2} + {3}. Conservative: - {4} + {5}'.format(mod, pcs[2], pcs[2]-pcs[1], pcs[3]-pcs[2], pcs[2]-pcs[0], pcs[4]-pcs[2]))
plt.yticks(hs[::-1], ['$\mathrm{'+l+'}$' for l in data['label']] + ['$\mathrm{CODATA}$', '$\mathrm{(H)DPGMM}$', '$\mathrm{(H)DPGMM - Conservative}$'])
ax.grid(visible = False)
ax.set_xlim(G.min(),G.max())
ax.set_xlabel('$G\ [\\times10^{-11}\ \mathrm{m}^3\mathrm{kg}^{-1}\mathrm{s}^{-2}]$')

ax.tick_params(axis='y', which='major', labelsize=6)
fig.savefig(Path(out_folder, 'hdpgmm.pdf'), bbox_inches = 'tight')
