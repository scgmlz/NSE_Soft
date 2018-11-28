##--IMPORT--##
'''
#############################################
The environement is initialised automatically
and then the data is loaded within the core
as defined.

Here we recommend to set the name pointing 
to the environement and minor manipulations
on the data if necessary.
#############################################
'''
parallel_env = self.env

parallel_env.current_data.metadata_class.add_metadata('Source format', value = "ToF files", logical_type = 'str')
parallel_env.current_data.metadata_class.add_metadata('Measurement type', value = "MIEZE", logical_type = 'float')
parallel_env.current_data.metadata_class.add_metadata('Wavelength error', value = 0.117 , logical_type = 'float')
parallel_env.current_data.metadata_class.add_metadata('Distance error', value = 0.0005 , logical_type = 'float')

parallel_env.current_data.metadata_class.add_metadata('R_1', value = 9. , logical_type = 'float', unit = 'm')
parallel_env.current_data.metadata_class.add_metadata('R_2', value = 5. , logical_type = 'float', unit = 'm')
parallel_env.current_data.metadata_class.add_metadata('L_1', value = 1200 , logical_type = 'float', unit = 'm')
parallel_env.current_data.metadata_class.add_metadata('L_2', value = 3500 , logical_type = 'float', unit = 'm')
parallel_env.current_data.metadata_class.add_metadata('Wavelength in', value = 6. , logical_type = 'float', unit = 'A')
parallel_env.current_data.metadata_class.add_metadata('Pixel size', value = 1.5625 , logical_type = 'float', unit = 'mum')
parallel_env.current_data.metadata_class.add_metadata('Qy', value = 0.035 , logical_type = 'float', unit = '-')
parallel_env.current_data.metadata_class.add_metadata('Selected foils', value = '[1,1,1,0,0,1,1,1]' , logical_type = 'int_array', unit = '-')

print(parallel_env.current_data)

parallel_env.mask.select_template(key = 'Pre_SkX_peak_Sixfold')
parallel_env.mask.add_command(command_str = 'mask.real[abs(mask.real) > 8] = 0')
print(parallel_env.mask)
##--IMPORT--##

##--PHASE--##
'''
#############################################
Here are stored the methods for the reduction
of the fata
#############################################
'''
parallel_env = self.env

foils_in_echo = []
for i in range(4):
    foils_in_echo.append([1,1,1,1,1,1])
foils_in_echo.append([1,1,0,1,1,1])
foils_in_echo.append([1,1,0,1,1,1])
foils_in_echo.append([0,0,0,0,1,0])
foils_in_echo.append([0,0,0,0,1,0])

#set the values to be processed as data
Select = [ 28.6, 29.0, 29.1, 29.2, 29.4, 29.6, 29.8, 30.0]

#set the reference value
Reference = [28.6,0]

#set the background
Background = 68.0

parallel_env.fit.set_parameter( name = 'Select',        value = Select       )
parallel_env.fit.set_parameter( name = 'Reference',     value = Reference    )
parallel_env.fit.set_parameter( name = 'Background',    value = Background   )
parallel_env.fit.set_parameter( name = 'foils_in_echo', value = foils_in_echo)

parallel_env.process.calculate_echo()
parallel_env.process.remove_foils()
parallel_env.process.calculate_shift()
##--PHASE--##

##--REDUCTION--##
'''
#############################################
Here are stored the methods for the reduction
of the fata
#############################################
'''
parallel_env = self.env

parallel_env.mask.select_template(key = 'SkX_peak_Sixfold')
print(parallel_env.mask)

parallel_env.process.calculate_ref_contrast()
#coorect values
parallel_env.results.set_result( 
         name = 'Reference contrast calculation', 
         position = ['Contrast_ref',0.36585973199337996], 
         value = 0.73)

parallel_env.results.set_result(
         name = 'Reference contrast calculation', 
         position = ['Contrast_ref_error',0.36585973199337996], 
         value = 0.0035)

parallel_env.process.calculate_contrast()

##--REDUCTION--##

##--POST--##
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
##--POST--##