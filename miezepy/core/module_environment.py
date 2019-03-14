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
#   Alexander Schober <alexander.schober@mac.com>
#
# *****************************************************************************

#############################
#import child components
from .module_mask       import MaskStructure 
from .module_data       import DataStructure 
from .module_fit        import getFitStructure
from .module_result     import ResultStructure
from .module_process    import getProcessStructure
from .module_io         import IOStructure
from .module_instrument import InstrumentStructure

class Environment:
    '''
    This will define the heart of each single measurement. It will 
    incorporate the data structure, mask system, the reduction 
    computation and the result structure.
    '''

    def __init__(self, env_handler, title, select = 'MIEZE'):
        '''
        Initialise the Environment class

        Parameters
        ----------
        env_handler : CoreHandler
            A link back to the parent in case an access is needed

        title: str
            the name of the current environnement
        '''
        #set up
        self.env_handler    = env_handler
        self.name           = title
        self.select         = select
        self.initialise()

    def initialise(self):
        '''
        set all the local items
        '''
        self.data           = []

        self._initDataStructure()
        self._initFitStructure()
        self._initProcessStructure()
        self._initMaskStructure()
        self._initResultStructure()
        self._initIOHandler()
        self._initInstrumentStructure()
    
    def _initDataStructure(self):
        '''
        This function will initiate a new data class
        and then set the current pointer to it.
        '''
        self.data.append(DataStructure())
        self.setCurrentData()

    def _initFitStructure(self):
        '''
        This function will initiate a new fit handler
        and then set the current fit to it.
        '''
        self.fit = getFitStructure(self.select)

    def _initProcessStructure(self):
        '''
        This function will initiate a new data class
        and then set the current pointer to it.
        '''
        self.process = getProcessStructure(self)

    def _initMaskStructure(self):
        '''
        This function will initiate a new mask class to the 
        environnement. 
        '''
        self.mask = MaskStructure()

    def _initResultStructure(self):
        '''
        This function will initiate a new 
        result structure that will be used int he 
        current environment.
        '''
        self.results = ResultStructure(mode = 'Dict')

    def _initIOHandler(self):
        '''
        initialise the io handler that will manage the 
        data and content flow back and forth between the
        miezepy software and the operating system.
        '''
        self.io      = IOStructure(self)

    def _initInstrumentStructure(self):
        '''
        This function will initiate a new 
        result structure that will be used int he 
        current environment.
        '''
        self.instrument = InstrumentStructure()

    def saveToPy(self, path):
        '''
        This function will initiate a new data class
        and then set the current pointer to it.

        Parameters
        ----------
        path : str
            Path to which the environment file has to be saved
        '''
        script = ""
        indent = 1

        script += "def setEnv(handler):\n"
        script += indent * "    " +"env = handler.new_environment('"+str(self.name)+"')\n"
        script += indent * "    " +"return env\n"

        f = open(path, 'w')
        f.write(script)
        f.close()

    def setCurrentData(self, idx = None):
        '''
        This function sets the current data
        with the right key

        Parameters
        ----------
        idx (optional) : int
            Set the currently active dataset to idx
        '''
        if not idx == None:
            self.current_data = self.data[idx]
        else:
            self.current_data = self.data[-1]
