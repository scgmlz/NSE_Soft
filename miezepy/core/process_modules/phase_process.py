#  -*- coding: utf-8 -*-
'''
#############################################
Here we set the overall fit parameters as well
as proceeding through the phase corrections. 
#############################################
'''
environnement = self.env

environnement.mask.setMask('Pre_SkX_peak_Sixfold')
environnement.mask.addCommand(command_str = 'mask.real[abs(mask.real) > 8] = 0')
print(environnement.mask)

environnement.process.calculate_echo()
environnement.process.remove_foils()
environnement.process.calculate_shift()