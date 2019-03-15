'''
#############################################
In this script we will effectively reduce the
data. Essential to this is the selection of
the mask that will be used to reduce.

environment.process.calculate_ref_contrast()
-> will evaluate the contrast of the 
reference.

environment.process.calculate_contrast()
-> will evaluate the contrast of selected 
measurements.

It is possible to edit missfit results as 
seen with the set_result command
#############################################
'''
environment = self.env

environment.mask.setMask('SkX_peak_Sixfold')
print(environment.mask)

# environment.results.set_result( 
#          name = 'Reference contrast calculation', 
#          position = ['Contrast_ref',0.36585973199337996], 
#          value = 0.73)

# environment.results.set_result(
#          name = 'Reference contrast calculation', 
#          position = ['Contrast_ref_error',0.36585973199337996], 
#          value = 0.0035)


environment.process.calcContrastRef()
environment.process.calcContrastMain()
