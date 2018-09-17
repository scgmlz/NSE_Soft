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

from .CORE_Masks    import Masks 
from .CORE_Data     import Data_Structure 
from .CORE_Fit      import get_fit_handler
from .CORE_Result   import Result_Handler
from .CORE_Process  import get_process_handler
from .CORE_io       import IO_Manager

class Environment:
    '''
    ##############################################
    An environment contains the different struc-
    tures necessary to contain and process the 
    data. 

    At start the following elements will be 
    initialised:
    - A datastructure array with a structure
    - A fit handler
    - A mask
    - A result handler

    ———————
    Input: 
    - title (str) name of the env
    - select (str) 'MIEZE', 'SANS'
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    def __init__(self, title = 'No_Name', select = 'MIEZE'):

        #set up
        self.name   = title
        self.select = select
        self.data   = {}

        #initialize
        self.new_data()
        self.new_fit(select)
        self.new_mask()
        self.new_results()
        
        self.process = get_process_handler(select, self)
        self.io      = IO_Manager(self)
        
    def new_data(self, title = 'No_Name'):
        '''
        ##############################################
        This function will initiate a new data class
        and then set the current pointer to it.
        ———————
        Input: 
        - title or key (str)
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #this will simply create the dataclass
        self.data[title] = Data_Structure()

        #set it to the current data structure
        self.set_current_data(key = title)

    def set_current_data(self, key = None):
        '''
        ##############################################
        This function sets the current data
        with the right key
        ———————
        Input: 
        - key (str)
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if not key == None:

            if key in self.data.keys():
                self.current_data_key = key
                self.current_data = self.data[key]
            else:
                print("\nERROR: The key '"+str(key)+"' you have provided is not present in the dictionary...\n")

    def new_fit(self, select = 'MIEZE'):
        '''
        ##############################################
        This function will initiate a new fit handler
        and then set the current fit to it.
        ———————
        Input: 
        - title or key (str)
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        #this will simply create the dataclass
        self.fit = get_fit_handler(select)

    def new_results(self):
        '''
        ##############################################
        This function will initiate a new 
        result structure that will be used int he 
        current environment.
        ———————
        Input: 
        - title or key (str)
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        #this will simply create the dataclass
        self.results = Result_Handler()

    def new_mask(self):
        '''
        ##############################################
        This function will initiate a new mask.
        ———————
        Input: 
        - title or key (str)
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        #this will simply create the dataclass
        self.mask = Masks()

    def new_mask_command(self, command_str = ''):
        '''
        ##############################################
        This function sets the current data
        with the right key
        ———————
        Input: 
        - key (str)
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.mask.add_command(command_str)

    def get_result(self, name = '', key = None, last = True):
        '''
        ##############################################
        Fetch the result class from the current result
        class. The result object can then be used
        locally. We do not advise to change evetual
        results the result of this method. 

        For this a specific branch of the set method
        has been engineered. 
        ———————
        Input: 
        - key (str)
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if last:

            try:

                return self.results.get_last_result(name, key)

            except ValueError:

                print("\nERROR: The name '"+str(name)+"' or key '"+str(key)+"'you have provided is not present in the dictionary. Error...\n")
