import numpy as np
import optparse as op

if __name__ == '__main__':

    parser = op.OptionParser()
    parser.add_option("-i", "--input", type = "string", dest = "samples_file")
    (options, args) = parser.parse_args()
    data = np.genfromtxt(options.samples_file, names = True)

    v = data['value']
    s = data['sigma']**2

    X = np.average(v, weights = 1/s)
    dX = np.sqrt(np.average((v-X)**2, weights = 1/s)/(len(v)-1))

    print('Least-squares method: {:1.5f}+-{:2.5f}'.format(X, dX))
