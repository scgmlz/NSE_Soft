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
from ..module_log import Log_Handler

class Fit_Handler():
    
    def __init__(self):
        '''
        This is the initializer of the fit class
        within.
        Input: target (Data_Structure)
        '''
        self.fun_dict   = {}
        self.ptr_dict   = {}
        self.para_dict  = {}
        self.log        = Log_Handler()
        self.verbose    = False

    def __getitem__(self, key):
        '''
        This getitem method will be transferred to the
        children and is here to manage different calls
        key = 'error', 'warning', 'info' will return
        the element of the log. 
        key = 'result' will return the last result
        key = 'print_result' will print it
        key = 'results' or 'logs' will return the 
        actual classes
        any other key will try to grab the dictionary
        ———————
        Input: target (Data_Structure)
        '''
        if key == 'error':
            return self.log.return_last_log('error')
        elif key == 'info':
            return self.log.return_last_log('info')
        elif key == 'warning':
            return self.log.return_last_log('warning')
        else:
            return self.fun_dict[key]


    def set_method(self, target, identifier):
        '''
        This function will try to select the right
        pointer for the right method
        ———————
        Input: 
        - target (str) the target method keyword
        - identifier (str) the method to select
        '''
        if target in self.fun_dict and identifier in self.ptr_dict:
            self.fun_dict[target]= self.ptr_dict[identifier]
        else:
            print('The input keys do not match existing functions')

    def set_parameter(self, name = '', value = ''):
        '''
        This function will allow the user to inject
        fit parameters...
        '''
        self.para_dict[name] = value

    def test_parameter(self, value, target, mask, results):
        '''
        Test function placeholder
        '''
        return value