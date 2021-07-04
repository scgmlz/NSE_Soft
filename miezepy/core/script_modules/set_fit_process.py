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

#Set the selected (edit in GUI)
Selected = [ 278.0, 288.0, 300.0, 313.0, 328.0]

#Set the time channels to use(edit in GUI)
TimeChannels = []

#Set the background (edit in GUI)
Background = None

#Set the reference (edit in GUI)
Reference = ['Reso',0]

#Instrument (edit in GUI)
instrument = 'Reseda'

#Detector(edit in GUI)
detector = 14032019

#Use the high exposure setting (edit in GUI)
exposure = False

#Use the foil summation methodology
sum_foils = True

environnement.fit.set_parameter( name = 'Select',        value = Selected     )
environnement.fit.set_parameter( name = 'Reference',     value = Reference    )
environnement.fit.set_parameter( name = 'Background',    value = Background   )
environnement.fit.set_parameter( name = 'foils_in_echo', value = foils_in_echo)
environnement.fit.set_parameter( name = 'processors',    value = 1)
environnement.fit.set_parameter( name = 'exposure',      value = exposure)
environnement.fit.set_parameter( name = 'time_channels', value = TimeChannels)
environnement.fit.set_parameter( name = 'sum_foils',     value = sum_foils)
environnement.instrument.setDetector(instrument, detector)
