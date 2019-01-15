#  -*- coding: utf-8 -*-
'''
#############################################
Here are stored the methods for the reduction
of the data
#############################################
'''
parallel_env = self.env

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

parallel_env.fit.set_parameter( name = 'Select',        value = Selected     )
parallel_env.fit.set_parameter( name = 'Reference',     value = Reference    )
parallel_env.fit.set_parameter( name = 'Background',    value = Background   )
parallel_env.fit.set_parameter( name = 'foils_in_echo', value = foils_in_echo)

parallel_env.process.calculate_echo()
parallel_env.process.remove_foils()
parallel_env.process.calculate_shift()