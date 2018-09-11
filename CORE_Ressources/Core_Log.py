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

import copy
import datetime

class Log_Handler:

    def __init__(self):
        '''
        ##############################################
        This is the initializer of the fit log and
        errors  handler class
    
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.info       = []
        self.warning    = []
        self.error      = []

    def return_last_log(self, selected):
        '''
        ##############################################
        Will return the last log entry for the 
        selected type.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if selected == 'error':

            return copy.deepcopy(self.error[-1]) if len(self.error) > 0 else None

        elif selected == 'warning':

            return copy.deepcopy(self.warning[-1]) if len(self.warning) > 0 else None

        elif selected == 'info':

            return copy.deepcopy(self.info[-1]) if len(self.info) > 0 else None

    def add_log(self, selected, message):
        '''
        ##############################################
        Will return the last log entry for the 
        selected type.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if selected == 'error':

            self.error.append([
                datetime.datetime.now(),
                message])

        elif selected == 'warning':

            self.warning.append([
                datetime.datetime.now(),
                message])

        elif selected == 'info':

            self.info.append([
                datetime.datetime.now(),
                message])

    def dump_log(self, path, level = 0):

        '''
        ##############################################
        This function will dump the log to file with 
        the adequat level. Note that level 0 inidicates
        that everything should be writen while level
        1,2,3 refere to 'error', 'error' + 'warnings'
        'error'+'warnings'+'information'
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        log_array = self.return_last_log(level = level)


    def return_single_array(self, level = 0):
        '''
        ##############################################
        This function will dump the log to an array with 
        the adequat level. Note that level 0 inidicates
        that everything should be writen while level
        1,2,3 refere to 'error', 'error' + 'warnings'
        'error'+'warnings'+'information'
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        array = []

        for log_list in [self.info, self.warning, self.error]:


        return array
        