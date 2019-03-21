'''
#############################################
This is the post process script. it is free
to the user for editing. The reduction result
is grabbed from the environnement through :
result = environment.get_result(name = 'Contrast fit')

it is possible to import matplotlib or other
libraries and to perform further 
investigations. It is also possible to save 
any output to a given path. 
#############################################
'''
environment = self.env

# -> possibility to dump the log to file
# environment.fit.log.dump_to_file('result.txt')

#grab he result
result = environment.get_result(name = 'Contrast fit')

############################################
#Matplotlib plot of the result
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import scipy.constants as co
from matplotlib.colors import Colormap, LogNorm
from matplotlib.cm import get_cmap
import pandas as pd
fig = plt.figure(figsize=(16,5))
ax  = fig.add_subplot(1,2,1)
ax.set_xscale('log')
ax1 = fig.add_subplot(1,2,2)

############################################
#cycle over the echo fit results
index = 0
for T in result['Select']:
    x        = result['Parameters'][T]['x']
    y        = result['Parameters'][T]['y']
    y_error  = result['Parameters'][T]['y_error']

    ax.errorbar(
        x, 
        y+1.2-index*0.2,
        y_error, 
        fmt='o', 
        label='$T=%.2f\,K$' %T)
    x = np.linspace(0.01,3,1000)
    ax.plot(x, result['Curve'][T]+1.2-index*0.2)
    index += 1

ax1.errorbar(
    result['Select'],
    result['Gamma'],
    result['Gamma_error'],
    fmt='o', label='Franz\' quasielastic')

############################################
#evemtually save to file
#plt.savefig('result.pdf')