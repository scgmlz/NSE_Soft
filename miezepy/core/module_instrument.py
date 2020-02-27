
#  -*- coding: utf-8 -*-
# *****************************************************************************
# Copyright (c) 2017 by the NSE analysis contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Alexander Schober <alex.schober@mac.com>
#
# *****************************************************************************

import os
import numpy as np
import sys
import inspect

class InstrumentStructure:
    '''
    This module will contain the instruments
    characteristics.
    '''
    def __init__(self):
        '''

        '''
        self._getDetectors()
        self.detector = MIEZEReseda()
        self.success    = True

    def _getDetectors(self):
        '''
        Investigate the present detector classes to 
        initialize the detector list for the GUI
        '''
        self.detector_names = []
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj) and 'MIEZE' in name:
                self.detector_names.append(name.split('MIEZE')[1])

    def setDetector(self, name, date = None):
        '''
        Here you can set the detector to use and finnally 
        set its properties through self.detector
        Note that if no date is provided the last 
        one will be used

        Parameters
        ----------
        idx : int
            foil to be used from the foil array
        '''
        if name in self.detector_names:
            exec('self.detector = MIEZE'+name+'()')
            if date == None:
                self.detector.setFoilFile(None)
            else:
                self.detector.setFoilFile(date)

class DetectorStructure:
    '''
    This module will contain the detector
    characteristics. This will be the ability 
    to load the appropriate config file and the 
    foil distortions
    '''

    def __init__(self):
        '''

        '''
        self.identifier         = 'Default'
        self.current_date       = 'None'
        self.num_foils          = 0
        self.size_foil          = [0, 0]
        self.num_foil_pixels    = [0, 0]
        self.foil_center        = [0, 0]
        self.num_time_channels  = 0

    def setFoilFile(self, date):
        '''
        In this function we will process the fit of 
        the data to allow fitting later on
        The package will be in dictionaries for each
        axis value1

        Parameters
        ----------
        date : int or string
            foil to be used from the foil array
        '''
        if date == None:
            self._loadFoils(self.foil_file_list[-1])
        else:
            idx = [e[0] for e in self.foil_file_list].index(date)
            self._loadFoils(self.foil_file_list[idx])
        
    def _loadFoils(self, foil_info):
        '''
        This is the routine that will load the foils as such 
        into a numpy array
        '''
        self.current_date = foil_info[1]
        self.foil_array = np.load(foil_info[-1])
        self.foil_array = np.transpose(self.foil_array,(0,2,1))

    def _initFoilList(self):
        '''
        Use the name to run through the foil directory 
        to get all elements.
        '''
        path        = os.path.dirname(os.path.realpath(__file__))
        folder      = os.path.join(path, 'instrument_modules', self.identifier, '')
        file_list   = os.listdir(folder)
        
        formated_file_list = []
        for file_name in file_list:
            file_path = os.path.join(folder, file_name)
            if os.path.isfile(file_path) and not '__init__' in file_path:
                num     = file_name.split('_')[1].split('.npy')[0]
                date    = num[0:2] + '.' + num[2:4] + '.' +num[4:] 
                text    = 'Reseda at ' + date
                formated_file_list.append([int(num), date, text, file_path])

        self.foil_file_list = sorted(
            formated_file_list,
            key = lambda formated_file_list: formated_file_list[0])

    def processPhaseShift(self, echos, velocities, d_sam_det, freq):
        '''
        This function is the detector routine to 
        correct the phase shift of the foil through
        the height profile loaded

        Parameters
        ----------
        echos : list float
            The list of echo times

        velocities : dict float
            The list of velocities for each echo

        d_sam_det : dict float
            The dictionary of distances sample detector

        freq : dict float
            The dictionary of frequency difference
        '''
        m_pixel_x   = self.size_foil[0]/self.num_foil_pixels[0]
        m_pixel_y   = self.size_foil[1]/self.num_foil_pixels[1]

        phase = np.zeros([
            len(echos), 
            self.num_foils,
            self.num_time_channels,
            self.num_foil_pixels[0] ,
            self.num_foil_pixels[1] ])

        loop_pixel = [
            (e1,e2) 
            for e1 in range(self.num_foil_pixels[0])
            for e2 in range(self.num_foil_pixels[1]) ]

        for echo_idx,echo in enumerate(echos):
            for foil_idx in range(self.num_foils):
                for x,y in loop_pixel:
                    phase[echo_idx, foil_idx, :,x,y] = (
                        2*np.pi-2*np.pi*(
                            d_sam_det[echo] - np.sqrt(d_sam_det[echo]**2 - ((x-self.foil_center[0])*m_pixel_x)**2- ((y-self.foil_center[1])*m_pixel_y)**2)
                            + self.foil_array[foil_idx,x,y])
                        /(velocities[echo]/(2*freq[echo])))

        index_map = np.zeros(phase.shape)
        for echo_idx,echo in enumerate(echos):
            for foil_idx in range(self.num_foils):
                index_map[echo_idx,foil_idx] = np.round(
                    ((2*np.pi-phase[echo_idx,foil_idx])/(2*np.pi/16.)+np.pi/2.)%16)

        return index_map


class MIEZEReseda(DetectorStructure):
    '''
    This module will contain the detector
    characteristics. This will be the ability 
    to load the appropriate config file and the 
    foil distortions
    '''

    def __init__(self):
        '''

        '''
        self.identifier         = 'Reseda'
        self.num_foils          = 8
        self.size_foil          = [0.20,0.20]
        self.num_foil_pixels    = [128, 128]
        self.foil_center        = [64, 64]
        self.num_time_channels  = 16

        self._initFoilList()
