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
environnement = self.env

environnement.current_data.metadata_class.add_metadata('Source format', value = "ToF files", logical_type = 'str')
environnement.current_data.metadata_class.add_metadata('Measurement type', value = "MIEZE", logical_type = 'float')
environnement.current_data.metadata_class.add_metadata('Wavelength error', value = 0.117 , logical_type = 'float')
environnement.current_data.metadata_class.add_metadata('Distance error', value = 0.0005 , logical_type = 'float')

environnement.current_data.metadata_class.add_metadata('R_1', value = 9. , logical_type = 'float', unit = 'm')
environnement.current_data.metadata_class.add_metadata('R_2', value = 5. , logical_type = 'float', unit = 'm')
environnement.current_data.metadata_class.add_metadata('L_1', value = 1200 , logical_type = 'float', unit = 'm')
environnement.current_data.metadata_class.add_metadata('L_2', value = 3500 , logical_type = 'float', unit = 'm')
environnement.current_data.metadata_class.add_metadata('Wavelength in', value = 6. , logical_type = 'float', unit = 'A')
environnement.current_data.metadata_class.add_metadata('Pixel size', value = 1.5625 , logical_type = 'float', unit = 'mum')
environnement.current_data.metadata_class.add_metadata('Qy', value = 0.035 , logical_type = 'float', unit = '-')
environnement.current_data.metadata_class.add_metadata('Selected foils', value = '[1,1,1,0,0,1,1,1]' , logical_type = 'int_array', unit = '-')

print(environnement.current_data)

