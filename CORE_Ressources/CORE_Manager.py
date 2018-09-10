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
from .CORE_io        import IO_Manager
from .CORE_Process   import Process_Manager 
from .CORE_Process   import Masks 
from .CORE_Data      import Data_Structure 
from .CORE_Fit       import get_fit_handler
from .CORE_Result    import Result_Handler

class CORE_Manager:

    def __init__(self, parent = None):

        ##############################################
        #initiate the core manager  
        self.parent = parent
        self.generate_children()

        ##############################################
        #initilise own variables
        self.generate_fun_dict()

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

        self.data_dict = {}
        self.mask_dict = {}
        self.fit_dict  = {}
        self.res_dict  = {}
        self.env_dict  = {}

        self.io = IO_Manager()
        self.process = Process_Manager()

    def generate_fun_dict(self):
        '''
        ##############################################
        This function will generate the dictionary
        linking the functions to the respecive target
        function.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.fun_dict = {}

        self.fun_dict['print'] = [
            self.Print,
            "Basic print function with one argument."
            ]

        self.fun_dict['new data'] = [
            self.new_data,
            "Initiates a new data structure."
            ]

        self.fun_dict['new mask'] = [
            self.new_mask,
            "Initiates a new mask structure."
            ]

        self.fun_dict['new fit'] = [
            self.new_fit,
            "Initiates a new fit structure."
            ]

        self.fun_dict['new result'] = [
            self.new_result,
            "Initiates a new fit structure."
            ]

        self.fun_dict['new environement'] = [
            self.new_environement,
            "Creates a new environement."
            ]

        self.fun_dict['load data'] = [
            self.load_data,
            "Loads the data from a file path."
            ]

        self.fun_dict['set data'] = [
            self.set_current_data,
            "Set the current dataset through its dicitonary key."
            ]

        self.fun_dict['set mask'] = [
            self.set_current_mask,
            "Set the current mask through its dicitonary key."
            ]

        self.fun_dict['set result'] = [
            self.set_current_result,
            "Set the current mask through its dicitonary key."
            ]

        self.fun_dict['set mask template'] = [
            self.set_current_mask_template,
            "Selects one of the mask templates."
            ]

        self.fun_dict['calculate shift'] = [
            self.calculate_shift,
            "Applies the current mask on the selected data."
            ]

        self.fun_dict['calculate data contrast'] = [
            self.calculate_contrast,
            "Perform data contrast calculations."
            ]

        self.fun_dict['calculate reference contrast'] = [
            self.calculate_ref_contrast,
            "Perform reference contrast calculations."
            ]

        self.fun_dict['calculate echo'] = [
            self.calculate_echo,
            "Calculate the echo time on the current dataset."
            ]

        self.fun_dict['calculate intensity'] = [
            self.calculate_intensity,
            "Calculate the intensity of SANS data."
            ]

        self.fun_dict['result'] = [
            self.get_result,
            "returns the result of a fit."
            ]

        self.fun_dict['remove foils'] = [
            self.remove_foils,
            "Removes the foils predefined in the metadata."
            ]

        self.fun_dict['process axis'] = [
            self.process_axis,
            "Set an absciss value from the metadata."
            ]


    def run(self,command, *args, **kwargs):
        '''
        ##############################################
        In this function the user can run Core
        commands from the python terminal by inputing
        the command dictioanry key and the arguments

        ———————
        Input: 
        - command to be evaluated (str)
        - *args list of positional arguments
        - **kwargs list of optional arguments
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if not command in list(self.fun_dict.keys()):

            logging.warn(" The given command "+str(command)+" is not recognized...")
            logging.warn(" Run help for a list of commands.")

        else:

            self.fun_dict[command][0](*args,**kwargs)

    def get(self,command, *args, **kwargs):
        '''
        ##############################################
        In this function the user can run Core
        commands from the python terminal by inputing
        the command dictioanry key and the arguments

        ———————
        Input: 
        - command to be evaluated (str)
        - *args list of positional arguments
        - **kwargs list of optional arguments
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if not command in list(self.fun_dict.keys()):

            logging.warn("The given command "+str(command)+" is not recognized...")
            logging.warn("Run help for a list of commands.")

        else:

            return self.fun_dict[command][0](*args,**kwargs)


    def set(self,identifier, name = '', location = '', value = None):
        '''
        ##############################################
        In this function the user can run Core
        commands from the python terminal by inputing
        the command dictioanry key and the arguments

        ———————
        Input: 
        - command to be evaluated (str)
        - *args list of positional arguments
        - **kwargs list of optional arguments
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if identifier == 'result value':
            
            self.res_dict[self.current_res_key].set_result(name, location,value)
            

        elif identifier == 'fit parameter':

            self.fit_dict[self.current_fit_key].set_parameter(name, value)



    def help(self, command = None):
        '''
        ##############################################
        In this function the user can run Core
        commands from the python terminal by inputing
        the command dictioanry key and the arguments
    
        ———————
        Input: 
        - command to be evaluated (str)
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if command == None:

            for key, element in self.fun_dict.items():

                print(key, element[1])

    def Print(self, text = '', element = ''):
        '''
        ##############################################
        Test function
        ———————
        Input: 
        - text to print (str)
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        if not text == '':

            print("This is the input text: ", text)
        
        if not element == '':

            if element == 'data':

                print(self.data_dict[self.current_data_key])

            elif element == 'mask':

                print(self.mask_dict[self.current_mask_key])

        sys.stdout.flush()

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
        self.data_dict[title] = Data_Structure()

        #set it to the current data structure
        self.set_current_data(key = title)

    def new_fit(self, title = 'No_Name', select = 'MIEZE'):
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
        self.fit_dict[title] = get_fit_handler(select)

        #set it to the current data structure
        self.set_current_fit(key = title)

    def new_result(self, title = 'No_Name'):
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
        self.res_dict[title] = Result_Handler()

        #set it to the current data structure
        self.set_current_result(key = title)

    def new_mask(self, title = 'No_Name'):
        '''
        ##############################################
        This function will initiate a new mask and 
        then set the current mask to it.
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
        self.mask_dict[title] = Masks()

        #set it to the current data structure
        self.set_current_mask(key = title)


    def new_environement(self, title = 'No_Name', select = 'MIEZE'):
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
        #Create the actual elements
        self.new_data(  title = title)
        self.new_fit(   title = title, select = select)
        self.new_mask(  title = title)
        self.new_result(title = title)

        #link to an environement
        self.env_dict[title] = [
            self.current_data_key, 
            self.current_fit_key, 
            self.current_mask_key, 
            self.current_res_key]

        #set environement
        self.set_current_env(title)


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

            if key in self.data_dict.keys():
                self.current_data_key = key
            else:
                print("\nERROR: The key '"+str(key)+"' you have provided is not present in the dictionary...\n")

    def set_current_fit(self, key = None):
        '''
        ##############################################
        This function sets the current fit
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

            if key in self.fit_dict.keys():
                self.current_fit_key = key

            else:
                print("\nERROR: The key '"+str(key)+"' you have provided is not present in the dictionary...\n")

    
    def set_current_result(self, key = None):
        '''
        ##############################################
        This function sets the current fit
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

            if key in self.res_dict.keys():
                self.current_res_key = key

            else:
                print("\nERROR: The key '"+str(key)+"' you have provided is not present in the dictionary...\n")


    def set_current_mask(self, key = None):
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

            if key in self.mask_dict.keys():
                self.current_mask_key = key
            else:
                print("\nERROR: The key '"+str(key)+"' you have provided is not present in the dictionary...\n")

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
                self.current_data_key   = self.env_dict[key][0]
                self.current_fit_key    = self.env_dict[key][1]
                self.current_mask_key   = self.env_dict[key][2]

            else:
                print("\nERROR: The key '"+str(key)+"' you have provided is not present in the dictionary...\n")


    def remove_foils(self):
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
        #generate the reduced key
        current_data_key = self.current_data_key.split('_reduced')[0] + '_reduced'

        #this will simply create the dataclass
        self.data_dict[current_data_key] = self.process.MIEZE_remove_foils(
            self.data_dict[self.current_data_key],
            self.mask_dict[self.current_mask_key],
            self.fit_dict[self.current_fit_key],
            self.res_dict[self.current_res_key]
        )

        #set it to the current data structure
        self.set_current_data(key = current_data_key)
 
    def load_data(self, path = '', data_type = ''):
        '''
        ##############################################
        this function will load a dataset from an 
        advanced data preparation routine
        ———————
        Input: 
        - path to a loader file (str)
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        ##############################################
        #loading Mieze data in tof format
        if data_type == 'MIEZE_TOF' or data_type == '':
            try:
                    
                #let the io manager grab the paths
                self.io.load_MIEZE_TOF(
                    load_path   = path, 
                    target      = self.data_dict[self.current_data_key]
                    )

            except ValueError:

                print("\nERROR: Unable to load the data...\n")

        ##############################################
        #loading Mieze data
        if data_type == 'SANS_PAD':

            try:
                    
                #let the io manager grab the paths
                self.io.load_SANS_PAD(
                    load_path   = path, 
                    target      = self.data_dict[self.current_data_key]
                    )

            except ValueError:

                print("\nERROR: Unable to load the data...\n")

    def set_current_mask_template(self, key = None):
        '''
        ##############################################
        This function will run through the 
        ———————
        Input: 
        - key (str)
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.mask_dict[self.current_mask_key].select_template(key = key)
                

    def calculate_shift(self):
        '''
        ##############################################
        this function process the current echo times
        for the different measurements. Note that 
        this operation will be performed solely on 
        the data metadata and then appended in the 
        same
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.process.MIEZE_calculate_shift(
            self.data_dict[self.current_data_key],
            self.mask_dict[self.current_mask_key],
            self.fit_dict[self.current_fit_key],
            self.res_dict[self.current_res_key])

    def calculate_contrast(self):
        '''
        ##############################################
        this function process the current echo times
        for the different measurements. Note that 
        this operation will be performed solely on 
        the data metadata and then appended in the 
        same
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        self.process.MIEZE_calculate_contrast(
            self.data_dict[self.current_data_key],
            self.mask_dict[self.current_mask_key],
            self.fit_dict[self.current_fit_key],
            self.res_dict[self.current_res_key])

    def calculate_ref_contrast(self):
        '''
        ##############################################
        this function process the current echo times
        for the different measurements. Note that 
        this operation will be performed solely on 
        the data metadata and then appended in the 
        same
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        self.process.MIEZE_calculate_ref_contrast(
            self.data_dict[self.current_data_key],
            self.mask_dict[self.current_mask_key],
            self.fit_dict[self.current_fit_key],
            self.res_dict[self.current_res_key])

    def calculate_echo(self):
        '''
        ##############################################
        this function process the current echo times
        for the different measurements. Note that 
        this operation will be performed solely on 
        the data metadata and then appended in the 
        same
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.process.MIEZE_calculate_echo(
            self.data_dict[self.current_data_key],
            self.mask_dict[self.current_mask_key],
            self.fit_dict[self.current_fit_key],
            self.res_dict[self.current_res_key])

    def calculate_intensity(self):
        '''
        ##############################################
        This funciton processes the intensity of SANS
        data against the predefined axis.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.process.SANS_intensity(
            self.data_dict[self.current_data_key],
            self.mask_dict[self.current_mask_key],
            self.fit_dict[self.current_fit_key],
            self.res_dict[self.current_res_key])

    def get_result(self, name = '', key = None, last = True):
        '''
        ##############################################
        Sets a parameter in the fit dicitonary
        ———————
        Input: 
        - key (str)
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        target = self.res_dict[self.current_res_key]

        if last:

            try:

                return target.get_last_result(name, key)

            except ValueError:

                print("\nERROR: The name '"+str(name)+"' or key '"+str(key)+"'you have provided is not present in the dictionary. Error...\n")

    def process_axis(self, axis = '', key = None):
        '''
        ##############################################
        Sets a parameter in the fit dicitonary
        ———————
        Input: 
        - key (str)
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        try:

            self.process.ALL_extract_from_metadata(
                self.data_dict[self.current_data_key],
                self.mask_dict[self.current_mask_key],
                self.fit_dict[self.current_fit_key],
                axis, key)

        except ValueError:

            print("\nERROR: The name '"+str(axis)+"' or key '"+str(key)+"'you have provided is not present in the dictionary. Error...\n")