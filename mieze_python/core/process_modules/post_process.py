'''
#############################################
Here the methods after the fit are being
shown.
#############################################
'''
parallel_env = self.env
parallel_env.fit.log.dump_to_file('result.txt')
parallel_result = parallel_env.get_result(name = 'Contrast fit')

############################################
#do the results
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import scipy.constants as co
from matplotlib.colors import Colormap, LogNorm
from matplotlib.cm import get_cmap
import pandas as pd
fig = plt.figure(figsize=(16,5))
ax = fig.add_subplot(1,2,1)

Ts = []
Gammas = []
Gammaerrs = []

index = 0

for T in parallel_result['Select']:
    x           = parallel_result['Parameters'][T]['x']
    y           = parallel_result['Parameters'][T]['y']
    y_error  = parallel_result['Parameters'][T]['y_error']

    ax.errorbar(
        x, 
        y+1.2-index*0.2,
        y_error, 
        fmt='o', 
        label='$T=%.2f\,K$' %T)
    x = np.linspace(0.01,3,1000)
    ax.plot(x, parallel_result['Curve'][T]+1.2-index*0.2)
    index += 1

ax.set_xscale('log')
ax.set_xlim(0.01,3)
ax.legend(bbox_to_anchor=(-0.1,0.9))
ax.text(2e-2, 0, r'$B \perp n$, $B=160\,mT$', fontsize=14)

y = []
y_error = []
for T in parallel_result['Select']:
    y.append(parallel_result['Gamma'][T])
    y_error.append(parallel_result['Gamma_error'][T])
    
ax1 = fig.add_subplot(1,2,2)
ax1.errorbar(
    parallel_result['Select'],
    y,
    y_error,
    fmt='o', label='Franz\' quasielastic')

ax1.set_ylabel(r'$\Gamma\ (\mu eV)$')
ax1.set_xlabel(r'$T\ (K)$')
ax1.set_xlim(27,31)
ax1.legend()

plt.savefig('B_parallel_n.pdf')