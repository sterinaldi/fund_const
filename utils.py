import numpy as np
import matplotlib.pyplot as plt
import cpnest.model
from scipy.stats import norm
from scipy.special import gammaln
from pathlib import Path
import corner

G_min = 6.668
G_max = 6.678
sigma_max = 0.01
a_max = 100
b_max = 100

out_folder = Path('output')
if not out_folder.exists():
    out_folder.mkdir()

# UN
def uniform(x):
    return 0.

# JF
def jeffreys(x):
    return -np.log(x['s'])

# IG
def inverse_gamma(x):
    return x['a']*np.log(x['b']) - gammaln(x['a']) - (x['a']+1)*np.log(x['s']) - x['b']/x['s']

def log_norm_1d(x, m, s):
    return -(x-m)**2/(2*s) - 0.5*np.log(2*np.pi*s)

dict_names = {'UN':['m','s'],
              'JF':['m','s'],
              'IG':['m','s','a','b']
             }

dict_bounds = {'UN':[[G_min, G_max], [0,sigma_max**2]],
               'JF':[[G_min, G_max], [0,sigma_max**2]],
               'IG':[[G_min, G_max], [0,sigma_max**2], [0,a_max], [0,b_max]],
              }

dict_priors = {'UN': uniform,
               'JF': jeffreys,
               'IG': inverse_gamma
              }

class G_inference(cpnest.model.Model):
    
    def __init__(self, values, errors, model):
        
        super(G_inference, self).__init__()
        
        self.values = values
        self.errors = errors**2
        self.names  = dict_names[model]
        self.bounds = dict_bounds[model]
        self.prior  = dict_priors[model]
    
    def log_prior(self, x):
        logP = super(G_inference, self).log_prior(x)
        if np.isfinite(logP):
            logP = self.prior(x)
        return logP
    
    def log_likelihood(self, x):
        return np.sum(log_norm_1d(x['m'], self.values, x['s']+self.errors))


def plot_distribution(post, model):

    G = np.linspace(G_min, G_max, 1000)
    samps = np.column_stack([post['m'], np.sqrt(post['s'])])
    
    pdf = []
    for i,si in enumerate(samps):
        f = norm(si[0], si[1]).pdf(G)
        pdf.append(f)
    low_90, low_68, med, high_68, high_90 = np.percentile(pdf, [5,16,50,84,95], axis=0)
        
    c = corner.corner(samps,
           labels= [r'${0}$'.format(lab) for lab in dict_names[model]],
           quantiles=[0.05, 0.16, 0.5, 0.84, 0.95],
           show_titles=True, title_fmt='.7f', title_kwargs={"fontsize": 16}, label_kwargs={"fontsize": 16},
           use_math_text=True)
    c.savefig(Path(out_folder'joint_posterior_{0}.pdf'.format(model)), bbox_inches='tight')
    
    fig, ax = plt.subplots()
    ax.fill_between(G, high_90, low_90, color = 'mediumturquoise', alpha = 0.5)
    ax.fill_between(G, high_68, low_68, color = 'darkturquoise', alpha = 0.5)
    # Median
    ax.plot(G, med, lw = 0.7, color = 'steelblue')
    
    ax.set_xlabel('$G\\times10^{-11}\ [\mathrm{m}^3\mathrm{kg}^{-1}\mathrm{s}^{-2}]$')
    ax.set_ylabel('$p(G)$')
    
    fig.savefig(Path(out_folder, 'p_{0}.pdf'.format(model)), bbox_inches = 'tight')
    np.savetxt(Path(out_folder, 'prob_G_{0}.txt'.format(model)), np.array([G, med, low_90, low_68, high_68, high_90]).T, header = 'G 50 5 16 84 95')