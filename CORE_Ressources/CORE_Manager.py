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

#############################
#import general components
import sys  
import numpy as np
import logging

#############################
#import child components
from .CORE_io       import IO_Manager
from .CORE_Environment    import Environment 

class CORE_Manager:

    def __init__(self, parent = None):

        ##############################################
        #initiate the core manager  
        self.parent = parent
        self.generate_children()

    def generate_children(self):
        '''
        ##############################################
        Thsi will genrate the dictionary for the 
        loaded data and link the other core classes
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.env_dict  = {}

    def new_environment(self, title = 'No_Name', select = 'MIEZE'):
        '''
        ##############################################
        This function will automise the environment
        creation for the user.
        ———————
        Input: 
        - title or key (str)
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #link to an environement
        self.env_dict[title] = Environment(title = title, select = select)

        #set environement
        self.set_current_env(title)

        self.current_env = self.env_dict[title]

        return self.env_dict[title]

    def set_current_env(self, key = None):
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

            if key in self.env_dict.keys():

                self.current_env_key    = key

                self.current_env = self.env_dict[key]

                return self.env_dict[key]

            else:
                print("\nERROR: The key '"+str(key)+"' you have provided is not present in the dictionary...\n")

