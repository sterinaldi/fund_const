import numpy as np
import matplotlib.pyplot as plt
import optparse as op
from pathlib import Path
# This import is just for plotting purposes
from figaro.utils import plot_median_cr
from figaro.cumulative import fast_cumulative
from seaborn import color_palette, light_palette

palette =  light_palette('darksalmon', 4)[1:]


models = ['UN', 'JF', 'IG']

colors = {'UN': palette[1],
          'JF': palette[0],
          'IG': palette[2],
         }

linestyle = {'UN': 'dotted',
             'JF': 'dashdot',
             'IG': 'dashed',
            }

if __name__ == '__main__':
    
    parser = op.OptionParser()
    parser.add_option("-i", "--input", type = "string", dest = "samples_file")
    parser.add_option("-o", "--output", type = "string", dest = "out_folder")
    parser.add_option("-l", "--label", type = "string", dest = "label")
    parser.add_option("-u", "--unit", type = "string", dest = "unit")
    parser.add_option("-v", "--value", type = "float", dest = "value")
    parser.add_option("-e", "--error", type = "float", dest = "error")
    parser.add_option("-n", "--name", type = "string", dest = "name")
    (options, args) = parser.parse_args()

    data = np.genfromtxt(options.samples_file, names = True, dtype = (np.float64, np.float64, '|U16'))
    out_file = open(Path(options.out_folder, 'values.txt'), 'w')

    data['label'][np.where(data['label'] == 'HUSTT-18')] = 'HUST_T-18'
    data['label'][np.where(data['label'] == 'HUSTA-18')] = 'HUST_A-18'

    X = np.genfromtxt(Path(options.out_folder, 'prob_UN.txt'), names = True)['X']

    # Parametric inference
    medians = {mod: np.genfromtxt(Path(options.out_folder, 'prob_{0}.txt'.format(mod)), names = True)['50'] for mod in models}

    fig, ax = plt.subplots()
    rec = np.genfromtxt(Path(options.out_folder, 'plots','prob_'+options.name+'.txt'), names = True)
    ax.fill_between(rec['x'], rec['95'], rec['5'], color = 'mediumturquoise', alpha = 0.25)
    ax.fill_between(rec['x'], rec['84'], rec['16'], color = 'darkturquoise', alpha = 0.25)
    for mod in models:
        medians[mod] = medians[mod]/np.sum(medians[mod]*(X[1]-X[0]))
        ax.plot(X, medians[mod], color = colors[mod], ls = linestyle[mod], label = '$\mathrm{'+mod+'}$')
    # Median
    ax.plot(rec['x'], rec['50'], lw = 1, color = 'steelblue', label = '$\mathrm{(H)DPGMM}$')
    
    ymin, ymax = ax.get_ylim()
    hs = np.linspace(0, ymax, len(data['value'])+3)
    for hi, v, s in zip(hs[3:], data['value'][::-1], data['sigma'][::-1]):
        ax.axhline(hi, lw = 0.02, c = 'k', ls = '--')
        ax.errorbar(v, hi, xerr = s, color = 'orange', marker = 'o', ms = 4)

    # CODATA value
    ax.axhline(hs[2], lw = 0.02, c = 'k', ls = ':')
    ax.errorbar(options.value, hs[2], xerr = options.error, color = 'blue', marker = 'o', ms = 4)



    # This work
    for i, mod in enumerate(models):
        cdf = fast_cumulative(np.ascontiguousarray(medians[mod]*(X[1]-X[0])))
        pcs = [X[np.where(cdf < perc)].max() for perc in [0.05, 0.16, 0.50, 0.84, 0.95]]
        print('{0}: '.format(mod)+'{:0.8f} - {:1.8f} + {:2.8f}. Conservative: - {:3.8f} + {:4.8f}'.format(pcs[2], pcs[2]-pcs[1], pcs[3]-pcs[2], pcs[2]-pcs[0], pcs[4]-pcs[2]))
        print('{0}: '.format(mod)+'{:0.8f} - {:1.8f} + {:2.8f}. Conservative: - {:3.8f} + {:4.8f}'.format(pcs[2], pcs[2]-pcs[1], pcs[3]-pcs[2], pcs[2]-pcs[0], pcs[4]-pcs[2]), file = out_file)
        
    cdf = fast_cumulative(np.ascontiguousarray(rec['50']*(rec['x'][1]-rec['x'][0])))
    pcs = [rec['x'][np.where(cdf < perc)].max() for perc in [0.05, 0.16, 0.50, 0.84, 0.95]]
    ax.axhline(hs[0], lw = 0.02, c = 'k', ls = ':')
    ax.errorbar(pcs[2], hs[0], xerr = np.atleast_2d([pcs[2]-pcs[0], pcs[4]-pcs[2]]).T, color = 'steelblue', marker = 'o', ms = 4)
    ax.axhline(hs[1], lw = 0.02, c = 'k', ls = ':')
    ax.errorbar(pcs[2], hs[1], xerr = np.atleast_2d([pcs[2]-pcs[1], pcs[3]-pcs[2]]).T, color = 'steelblue', marker = 'o', ms = 4)
        
    print('(H)DPGMM: {:0.8f} - {:1.8f} + {:2.8f}. Conservative: - {:3.8f} + {:4.8f}'.format(pcs[2], pcs[2]-pcs[1], pcs[3]-pcs[2], pcs[2]-pcs[0], pcs[4]-pcs[2]))
    print('(H)DPGMM: {:0.8f} - {:1.8f} + {:2.8f}. Conservative: - {:3.8f} + {:4.8f}'.format(pcs[2], pcs[2]-pcs[1], pcs[3]-pcs[2], pcs[2]-pcs[0], pcs[4]-pcs[2]), file = out_file)
    
    ax.set_xlim(rec['x'].min(),rec['x'].max())
    ax.set_xlabel('$' + options.label+'\ ['+options.unit+']$')
    plt.yticks(hs[::-1], ['$\mathrm{'+l+'}$' for l in data['label']] + ['$\mathrm{CODATA\ 2018}$', '$\mathrm{(H)DPGMM}$', '$\mathrm{(H)DPGMM - Conservative}$'])
    ax.tick_params(axis='y', which='major', labelsize=6)
    ax.legend(loc = 0, frameon = False)
    ax.grid(visible = False)
    fig.savefig(Path(options.out_folder, 'post_dist.pdf'), bbox_inches = 'tight')

    out_file.close()
