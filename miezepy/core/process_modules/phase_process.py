#  -*- coding: utf-8 -*-
'''
#############################################
Here we set the overall fit parameters as well
as proceeding through the phase corrections. 
#############################################
'''
environnement = self.env

foils_in_echo = []
foils_in_echo.append([1, 1, 1, 1, 1, 1])
foils_in_echo.append([1, 1, 1, 1, 1, 1])
foils_in_echo.append([1, 1, 1, 1, 1, 1])
foils_in_echo.append([1, 1, 1, 1, 1, 1])
foils_in_echo.append([1, 1, 0, 1, 1, 1])
foils_in_echo.append([1, 1, 0, 1, 1, 1])
foils_in_echo.append([0, 0, 0, 0, 1, 0])
foils_in_echo.append([0, 0, 0, 0, 1, 0])

#set the values to be processed as data
Selected = [ 28.6, 29.0, 29.1, 29.2, 29.4, 29.6, 29.8, 30.0]

#set the reference value
Reference = [28.6,0]

#set the background
Background = 68.0

environnement.fit.set_parameter( name = 'Select',        value = Selected     )
environnement.fit.set_parameter( name = 'Reference',     value = Reference    )
environnement.fit.set_parameter( name = 'Background',    value = Background   )
environnement.fit.set_parameter( name = 'foils_in_echo', value = foils_in_echo)

environnement.process.calculate_echo()
environnement.process.remove_foils()
environnement.process.calculate_shift()