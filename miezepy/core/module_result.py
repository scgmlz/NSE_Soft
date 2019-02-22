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
import time
import datetime
import pprint

from .module_log import Log_Handler

class ResultStructure:
    '''
    The result handler will manage the the input 
    output of a mathematical process. This can be 
    a fit fir example. Each result will then be
    saved in a Result_object class. 
    '''

    def __init__(self, mode = 'List'):
        '''
        This is the initializer of the fit results 
        handler class
        '''
        self.mode       = mode
        if self.mode == 'List':
            self.results  =  []
        elif self.mode == 'Dict':
            self.results  =  {}
        self.log        = Log_Handler()

    def reset(self):
        '''
        Reset the result handler class by deleting 
        all results. 
        '''
        self.results.clear()

    def generate_result(self, name):
        '''
        This class will create a new result object and
        then return it onto the owner. 
        '''
        if self.mode == 'Dict':
            self.results[name] = Result_Object(name)
            return self.results[name]
        else:
            self.results.append(Result_Object(name))
            return self.results[-1]

    def get_last_result(self, name = '', key = None):
        '''
        This will go through the results in reverse 
        and return the whole result dictionary in full
        or the value if key has been set and declared
        Input: 
        - target (str) the target method keyword
        - identifier (str) the method to select
        '''
        #log it
        self.log.add_log(
            'info', 
            'The user is asking for result name: '
            + str(name)
            + ' and key: '
            + str(key))

        ##############################################
        #dictionary mode
        if self.mode == 'Dict':
            if key == None:
                #log it
                self.log.add_log(
                    'info', 
                    'Successfully returning result with name: '
                    + str(name))
                return self.results[name]
            elif not key == None and key not in self.results[name].result_dict:
                #log it
                self.log.add_log(
                    'error', 
                    'Could not find the result with name: '
                    + str(name)
                    + ' and key: '
                    + str(key))
            else:
                return self.results[name][key]

        ##############################################
        #list mode
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
                    elif not key == None and key not in self.results[i].result_dict:
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
        This will set a value for a given result. This
        can be used to manually inject a value. 
        '''
        ##############################################
        #dictionary mode
        if self.mode == 'Dict':
            eval_string = "self.results['" + str(name) + "']"

        ##############################################
        #List mode
        else:
            eval_string = "self.results[i]"

        ##############################################
        #Common part
        for element in position:
            if isinstance(element, str):
                eval_string += "['"+str(element)+"']"
            elif isinstance(element, int):
                eval_string += "['"+int(element)+"']"
            else:
                eval_string += "["+str(element)+"]"
        eval_string += " = value"

        ##############################################
        #dictionary mode
        if self.mode == 'Dict':
            exec(eval_string)

        ##############################################
        #List mode
        else:
            for i in range(len(self.results) - 1, -1, -1):
                if self.results[i]['name'] == name:
                    exec(eval_string)
                    return 0

class Result_Object:
    '''
    A result object gets initialised at the
    beginning of a mathematical operation and 
    then populated with information. As the process
    is completed the result is closed closed. 
    '''

    def __init__(self, name):
        '''
        Initialise a Result_object. Note that the
        caller refers to the method that called the
        creation of the present Result. 
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
        self.add_metadata('name',   name)

    def __str__(self):
        '''
        The print class method. Will return the current
        class as a string to be displayed in a print
        call. 
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
        The getitem will get the element associated to
        the key. 
        ''' 
        try:
            return self.result_dict[key]
        except:
            pointers = [
                self.metadata_dict, 
                self.parameter_dict, 
                self.input_dict, 
                self.result_dict]

            for dictionary in pointers:
                if key in dictionary:
                    return dictionary[key]
                    
            self.log.add_log(
                'error', 
                'Could not find the key: '+str(key)+', returning 0')

            return 0

    def __setitem__(self, key, value):
        '''
        The setitem method will automatically 
        reference to the result dictionary.  
        ''' 
        #call the method
        self.add_result( key, value)
        
    def set_complete(self):
        '''
        The result has been provided and the class is
        now being locked to forbid overwriting of the
        data. 
        ''' 
        self.add_metadata('End',  datetime.datetime.now())
        self.add_metadata('Duration',  self['Start'] - self['End'])
        
        if not 'name' in self.metadata_dict.keys():
            self.log.add_log('error', 'Each result object needs a name... Fix please.')

        self.complete = True

    def add_metadata(self, name, value):
        '''
        Add a metadata to the metadata dictionary. 
        ''' 
        self.metadata_dict[name] = value

        self.log.add_log(
            'info', 
            "Added the entry'"
            + name
            + "' to the metadata")

    def add_parameter(self, name, value):
        '''
        Add a parameter to the parameter dictionary.
        ''' 
        self.parameter_dict[name] = value

        self.log.add_log(
            'info', 
            "Added the entry'"
            + name
            + "' to the parameters")

    def add_input(self, name, value):
        '''
        Add a parameter to the parameter dictionary. 
        ''' 
        self.input_dict[name] = value

        self.log.add_log(
            'info', 
            "Added the entry'"
            + name
            + "' to the inputs")

    def add_result(self, name, value):
        '''
        Add a result to the result dictionary. 
        ''' 
        self.result_dict[name] = value

        self.log.add_log(
            'info', 
            "Added the entry'"
            + name
            + "' to the results")

    def add_log(self, name, value):
        '''

        ''' 
        self.log.add_log(name, value)

