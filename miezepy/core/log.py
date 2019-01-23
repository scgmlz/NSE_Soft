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
import copy
import datetime

class Log_Handler:

    def __init__(self):
        '''
        This is the initializer of the log and
        errors  handler class.

        The print_level parameter is the setting in which
        the log handler will print log inputs to the 
        console as it is fed.
        '''
        self.info           = []
        self.warning        = []
        self.error          = []
        self.print_level    = ['error','warning']
        self.children       = [] 
        self.parent         = None 

    def return_last_log(self, selected):
        '''
        Will return the last log entry for the 
        selected type.
        '''
        if selected == 'error':
            return copy.deepcopy(self.error[-1]) if len(self.error) > 0 else None

        elif selected == 'warning':
            return copy.deepcopy(self.warning[-1]) if len(self.warning) > 0 else None

        elif selected == 'info':
            return copy.deepcopy(self.info[-1]) if len(self.info) > 0 else None

    def add_log(self, selected, message):
        '''
        Add an event to the log.
        '''

        ##############################################
        #are we fed by an error
        if selected == 'error':
            #add error
            self.error.append([
                datetime.datetime.now(),
                message,
                'ERROR'])
            #print error
            if  'error' in self.print_level:
                line = self.error[-1]
                print(str(line[0])+' '+line[2]+' '+line[1])

        ##############################################
        #are we fed by a warning
        elif selected == 'warning':
            #add error
            self.warning.append([
                datetime.datetime.now(),
                message,
                'WARNING'])
            #print error
            if  'warning' in self.print_level:
                line = self.warning[-1]
                print(str(line[0])+' '+line[2]+' '+line[1])

        ##############################################
        #are we fed by an information
        elif selected == 'info':
            #add error
            self.info.append([
                datetime.datetime.now(),
                message,
                'INFORMATION'])
            #print error
            if  'info' in self.print_level:
                line = self.info[-1]
                print(str(line[0])+' '+line[2]+' '+line[1])

    def dump_to_file(self, path, level = 0):
        '''
        This function will dump the log to file with 
        the adequat level. Note that level 0 indicates
        that everything should be writen while level
        1,2,3 refere to 'error', 'error' + 'warnings'
        'error'+'warnings'+'information'
        '''
        log_array = self.return_single_array(level = level)
        file = open(path, 'w')
        for line in log_array:
            file.write(str(line[0])+' '+line[2]+' '+line[1]+'\n')

    def dump_to_console(self,level = 0):
        '''
        This function will dump the log to file with 
        the adequat level. Note that level 0 inidicates
        that everything should be writen while level
        1,2,3 refere to 'error', 'error' + 'warnings'
        'error'+'warnings'+'information'
        '''
        log_array = self.return_single_array(level = level)
        for line in log_array:
            print(str(line[0])+' '+line[2]+' '+line[1])

    def return_single_array(self, level = 0):
        '''
        This function will dump the log to an array with 
        the adequat level. Note that level 0 inidicates
        that everything should be writen while level
        1,2,3 refere to 'error', 'error' + 'warnings'
        'error'+'warnings'+'information'
        '''
        #initialize
        log_array = []

        #create the list of lsits
        if level == 0:
            log_lists = [self.info, self.warning, self.error]
        elif level == 1:
            log_lists = [self.error]
        elif level == 2:
            log_lists = [self.error, self.warning]
        elif level == 3:
            log_lists = [self.info, self.warning, self.error]
    
        #now populate all the warnings
        for log_list in log_lists:
            log_array += list(log_list)

        #now sort it 
        log_array.sort()
        return log_array
        