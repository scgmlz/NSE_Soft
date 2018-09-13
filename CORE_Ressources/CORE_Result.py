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

import time
import datetime
import pprint

from .CORE_Log import Log_Handler

class Result_Handler:
    '''
    ##############################################
    The result handler will manage the the input 
    output of a mathematical process. This can be 
    a fit fir example. Each result will then be
    saved in a Result_object class. 
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''

    def __init__(self):
        '''
        ##############################################
        This is the initializer of the fit results 
        handler class
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.results = []
        self.log     = Log_Handler()

    def generate_result(self):
        '''
        ##############################################
        This class will create a new result object and
        then return it onto the owner. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #add the element
        self.results.append(Result_Object())

        return self.results[-1]

    def get_last_result(self, name = '', key = None):
        '''
        ##############################################
        This will go through the results in reverse 
        and return the whole result dicitonary in full
        or the value if key has been set and declared
        ———————
        Input: 
        - target (str) the target method keyword
        - identifier (str) the method to select
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        #log it
        self.log.add_log(
            'info', 
            'The user is asking for result name: '
            + str(name)
            + ' and key: '
            + str(key))

        if name == '':

            return self.results[-1]

        else:

            for i in range(len(self.results) - 1, -1, -1):

                if self.results[i]['name'] == name:

                    if key == None:
                        
                        #log it
                        self.log.add_log(
                            'info', 
                            'Successfully returning result with name: '
                            + str(name))

                        return self.results[i]

                    elif not key == None and key not in self.results[i].result_dict.keys():

                        #log it
                        self.log.add_log(
                            'error', 
                            'Could not find the result with name: '
                            + str(name)
                            + ' and key: '
                            + str(key))

                    else:

                        return self.results[i][key]

            #log it
            self.log.add_log(
                'error', 
                'Could not find result with name: '
                + str(name))

            return None

    def set_result(self, name = '' , position = ['None'], value = None):
        '''
        ##############################################
        This will set a value for a given result. This
        can be used to manually inject a value. 
        ———————
        Input: 
        - target (str) the target method keyword
        - identifier (str) the method to select
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        #build the string
        eval_string = "self.results[i]"

        for element in position:

            if isinstance(element, str):

                eval_string += "['"+str(element)+"']"

            else:

                eval_string += "["+str(element)+"]"

        eval_string += " = value"

        for i in range(len(self.results) - 1, -1, -1):

            if self.results[i]['name'] == name:

                exec(eval_string)

                return 0

class Result_Object:
    '''
    ##############################################
    A result object gets intialised at the
    beginning of a mathematical operation and 
    then populated with information. As the process
    is completed the result is closed closed. 
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''

    def __init__(self):
        '''
        ##############################################
        Initialise a Result_object. Note that the
        caller refers to the method that called the
        creation of the present Result. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #set the complete
        self.complete   = False
        self.log        = Log_Handler()

        #initialise the dictionaries
        self.metadata_dict   = {}
        self.result_dict     = {}
        self.input_dict      = {}
        self.parameter_dict  = {}

        #set first metadata
        self.add_metadata('Date',   str(time.ctime()))
        self.add_metadata('Start',  datetime.datetime.now())

    def __str__(self):
        '''
        ##############################################
        The print class method. Will retun the current
        class as a string to be displayed in a print
        call. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        ''' 
        output ="\n##########################################################\n"
        output += "################## RESULT STRUCTURE ######################\n"
        output += "##########################################################\n"
        output += "- METADATA:\n"
        output += pprint.pformat(self.metadata_dict)
        output += "\n----------------------------------------------------------\n"
        output += "- INPUT:\n"
        output += pprint.pformat(self.input_dict)
        output += "\n----------------------------------------------------------\n"
        output += "- PARAMETERS:\n"
        output += pprint.pformat(self.parameter_dict)
        output += "\n----------------------------------------------------------\n"
        output += "- RESULTS:\n"
        output += pprint.pformat(self.result_dict)
        output += "\n##########################################################\n"
        return output

    def __getitem__(self, key):
        '''
        ##############################################
        The getitem will get the element associated to
        the key. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        ''' 

        #create the pointer
        pointers = [
            self.metadata_dict, 
            self.parameter_dict, 
            self.input_dict, 
            self.result_dict]

        #run through it
        for dicitonary in pointers:

            if key in dicitonary.keys():
                
                #log the request
                self.log.add_log(
                    'info', 
                    'Found the key: '+str(key))

                #return value
                return dicitonary[key]

        #if we reach here we could not find the element
        self.log.add_log(
            'error', 
            'Could not find the key: '+str(key)+', returning 0')

        return 0

    def __setitem__(self, key, value):
        '''
        ##############################################
        The setitem method will automatically 
        referenct to the result dictionary.  
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        ''' 
        #call the method
        self.add_result( key, value)
        

    def set_complete(self):
        '''
        ##############################################
        The result has been provided and the class is
        now being locked to forbid overwriting of the
        data. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        ''' 
        #process time
        self.add_metadata('End',  datetime.datetime.now())
        self.add_metadata('Duration',  self['Start'] - self['End'])
        
        #check if there is a name
        if not 'name' in self.metadata_dict.keys():

            #log it
            self.log.add_log('error', 'Each result object needs a name... Fix please.')

        #set value
        self.complete = True

    def add_metadata(self, name, value):
        '''
        ##############################################
        Add a metadata to the metadata dictionary. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        ''' 
        #set the value
        self.metadata_dict[name] = value

        #log it
        self.log.add_log('info', 'Added '+name+' to the metadata')

    def add_parameter(self, name, value):
        '''
        ##############################################
        Add a parameter to the parameter dictionary. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        ''' 
        #set the value
        self.parameter_dict[name] = value

        #log it
        self.log.add_log('info', 'Added '+name+' to the parameters')

    def add_input(self, name, value):
        '''
        ##############################################
        Add a parameter to the parameter dictionary. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        ''' 
        #set the value
        self.input_dict[name] = value

        #log it
        self.log.add_log('info', 'Added '+name+' to the inputs')

    def add_result(self, name, value):
        '''
        ##############################################
        Add a result to the result dictionary. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        ''' 
        #set the value
        self.result_dict[name] = value

        #log it
        self.log.add_log('info', 'Added '+name+' to the results')

    def add_log(self, name, value):
        '''
        ##############################################
        Add a result to the result dictionary. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        ''' 
        #log it
        self.log.add_log(name, value)

