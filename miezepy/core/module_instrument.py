
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

class InstrumentStructure:
    '''
    This module will contain the instruments
    characteristics.
    '''

    def __init__(self):
        '''

        '''
        self.detector   = DetectorStructure()
        self.success    = True

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
        self.num_foils          = 0
        self.size_foil          = [0, 0]
        self.num_foil_pixels    = [0, 0]
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
            self._loadFoils(
                self.foil_file_list[idx])
        
    def _loadFoils(self, foil_info):
        '''
        This is the routine that will load the foils as such 
        into a numpy array
        '''
        self.foil_array = np.load(foil_info[-1])

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
            if os.path.isfile(file_path):
                num     = file_name.split('_')[1].split('.npy')[0]
                date    = num[0:2] + '.' + num[2:4] + '.' +num[4:] 
                text    = 'Reseda at ' + date
                formated_file_list.append([int(num), date, text, file_path])

        self.foil_file_list = sorted(
            formated_file_list,
            key = lambda formated_file_list: formated_file_list[0])

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
        self.size_foil          = [20,20]
        self.num_foil_pixels    = [128, 128]
        self.num_time_channels  = 16

        self._initFoilList()
