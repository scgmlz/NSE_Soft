#  -*- coding: utf-8 -*-
'''
#############################################
Here we set the overall fit parameters as well
as proceeding through the phase corrections. 
#############################################
'''
environnement = self.env

environnement.mask.setMask('Pre_SkX_peak_Sixfold')
print(environnement.mask)

environnement.process.calculateEcho()
environnement.process.calcShift()