import numpy as np

data = np.genfromtxt('newtonsConstantWithLabels.dat', names = True)

v = data['value']
s = data['sigma']**2

G = np.average(v, weights = 1/s)
dG = np.sqrt(np.average((v-G)**2, weights = 1/s)/(len(v)-1))

print('Least-squares method: G = {:0.5f}+-{:1.5f}'.format(G, dG))
