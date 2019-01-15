'''
#############################################
Here are stored the methods for the reduction
of the fata
#############################################
'''
parallel_env = self.env



parallel_env.mask.setMask('SkX_peak_Sixfold')
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
