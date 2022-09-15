import numpy as np
import optparse as op
from fund_const.utils import parametric_inference, plot_distribution
from pathlib import Path
import os

if __name__ == '__main__':

    import cpnest
    parser = op.OptionParser()
    parser.add_option("-i", "--input", type = "string", dest = "samples_file")
    parser.add_option("-o", "--output", type = "string", dest = "out_folder")
    parser.add_option("-b", "--bounds", type = "string", dest = "bounds")
    parser.add_option("-l", "--label", type = "string", dest = "label")
    parser.add_option("-u", "--unit", type = "string", dest = "unit")
    
    (options, args) = parser.parse_args()
    
    options.bounds = np.atleast_1d(eval(options.bounds))
    
    data = np.genfromtxt(options.samples_file, names = True)
    models = ['UN', 'JF', 'IG']
    means = []
    sigma = []
    for mod in models:
        print('Model {0}'.format(mod))
        M = parametric_inference(data['value'], data['sigma'], mod, options.bounds)
        work = cpnest.CPNest(M,
                            verbose = 0,
                            nlive = 1000,
                            maxmcmc = 5000,
                            nensemble = 1,
                            )
        work.run()
        post = work.posterior_samples.ravel()
        plot_distribution(post, mod, Path(options.out_folder).resolve(), options.label, options.unit, options.bounds)
    # Remove files from CPNest
    [os.remove(f) for f in ['chain_{0}_0.txt'.format(n_live_points), 'chain_{0}_0.txt_evidence_0.txt'.format(n_live_points),'cpnest.log','header.txt']]
