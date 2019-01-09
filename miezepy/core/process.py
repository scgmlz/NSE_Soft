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

def get_process_handler(select, env):
    '''
    ##############################################
    Will return the right fit manager depending 
    on the initial input
    ———————
    Input: target (Data_Structure)
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''

    if select == 'MIEZE':
        return Process_MIEZE(env)

    if select == 'SANS':
        return Process_SANS(env)

    else:
        print('Could not find the process class you are looking for. Error...')
        return None

class Process_Handler:

    def __init__(self, env):
        '''
        ##############################################
        This is the initializer of all the 
        ———————
        Input: -
        ———————
        Output: -
        ##############################################
        '''
        self.env = env

    def extract_from_metadata(self, axis, key):
        '''
        ##############################################
        This function will populate the axis with a 
        given metadata entry and then collapse the
        axis around it.  
        ———————
        Input: 
        - data_structure class (loaded already)
        - mask object
        - fit object
        ———————
        Output: -
        ##############################################
        '''
        ############################################
        #fix the axes
        idx = self.env.current_data.axes.names.index(axis)
        self.env.current_data.axes.grab_meta(idx, key, self.env.current_data)
        self.env.current_data.axes.collapse_axis(idx, self.env.current_data)

class Process_MIEZE(Process_Handler):

    def __init__(self, env):
        '''
        ##############################################
        This class is a subs process class that cont-
        ains the method related to processing the 
        MIEZE data
        ———————
        Input: 
        - environement
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #initialize the superclass
        Process_Handler.__init__(self, env)
        self.env = env
        self.initalize()

    def initalize(self):
        '''
        ##############################################
        Initialize the default python scipts so that 
        the system can be set.
        ———————
        Input: -
        ———————
        Output: -
        ##############################################
        '''
        self.default_scripts = []
        with open(os.path.dirname(os.path.realpath(__file__))+ '/process_modules/import_process.py','r') as f:
            self.default_scripts.append(f.read())
        with open(os.path.dirname(os.path.realpath(__file__))+ '/process_modules/phase_process.py','r') as f:
            self.default_scripts.append(f.read())
        with open(os.path.dirname(os.path.realpath(__file__))+ '/process_modules/reduction_process.py','r') as f:
            self.default_scripts.append(f.read())
        with open(os.path.dirname(os.path.realpath(__file__))+ '/process_modules/post_process.py','r') as f:
            self.default_scripts.append(f.read())

        self.editable_scripts = list(self.default_scripts)

    def loadScripts(self, path):
        '''
        ##############################################
        Initialize the default python scipts so that 
        the system can be set.
        ———————
        Input: 
        - path (str) file path to be loaded
        ———————
        Output: -
        ##############################################
        '''
        with open(path,'r') as f:
            text = f.read()

        strings = [
            text.split('##--IMPORT--##')[1],
            text.split('##--PHASE--##')[1],
            text.split('##--REDUCTION--##')[1],
            text.split('##--POST--##')[1]
        ]
        self.editable_scripts = list(strings)


    def saveScripts(self, path, strings):
        '''
        ##############################################
        Initialize the default python scipts so that 
        the system can be set.
        ———————
        Input: 
        - path (str) file path to be saved
        - strings([str]) scripts 
        ———————
        Output: -
        ##############################################
        '''
        string = (
            "##--IMPORT--##\n"
            + strings[0]
            + "\n##--IMPORT--##\n"
            + "##--PHASE--##\n"
            + strings[1]
            + "\n##--PHASE--##\n"
            + "##--REDUCTION--##\n"
            + strings[2]
            + "\n##--REDUCTION--##\n"
            + "##--POST--##\n"
            + strings[3]
            + "\n##--POST--##\n")

        f = open(path, 'w')
        f.write(string)
        f.close()

    def calculate_echo(self):
        '''
        ##############################################
        In this function we will process the eco time
        on the provided datastructure. 
        ———————
        Input: 
        - environment
        ———————
        Output: -
        ##############################################
        '''
        self.env.fit.set_parameter( 
            name = 'para_name', 
            value = self.env.current_data.axes.names[0])
        
        self.env.fit.set_parameter( 
            name = 'meas_name', 
            value = self.env.current_data.axes.names[1])

        self.env.fit.set_parameter( 
            name = 'echo_name', 
            value = self.env.current_data.axes.names[2])

        self.env.fit.set_parameter( 
            name = 'foil_name', 
            value = self.env.current_data.axes.names[3])

        self.env.fit.set_parameter( 
            name = 'tcha_name', 
            value = self.env.current_data.axes.names[4])

        ############################################
        #process the echo time
        for metadata_object in self.env.current_data.metadata_objects:

            self.env.fit['mieze_tau'](
                metadata_object, 
                self.env.current_data)

        self.extract_from_metadata(
            self.env.current_data.axes.names[2], 
            'tau')

    def remove_foils(self):
        '''
        ##############################################
        Removes the foils from the dataset and returns
        the deepcopy new dataset
        ———————
        Input: 
        - environment
        ———————
        Output: -
        ##############################################
        '''
        #preprocess
        self.env.set_current_data(
            key = self.env.current_data_key.split('_reduced')[0])

        new_data_key = self.env.current_data_key.split('_reduced')[0] + '_reduced'

        #remove the asked foils
        selected_foils  = self.env.current_data.metadata_class['Selected foils']
        new_target      = self.env.current_data.remove_from_axis(3,selected_foils)

        #set the new data
        self.env.data[new_data_key] = new_target
        self.env.set_current_data(new_data_key)

    def calculate_shift(self):
        '''
        ##############################################
        apply the masks and process the information
        ———————
        Input: 
        - enviroenment
        ———————
        Output: -
        ##############################################
        '''
        #generate the mask adapted to this dataset
        self.env.mask.process_mask(
            self.env.current_data)
        
        #extract the phase
        self.env.fit['extract_phase'](
            self.env.current_data, 
            self.env.mask, 
            self.env.results)

        #process the shift
        self.env.fit['calc_shift'](
            self.env.current_data, 
            self.env.mask, 
            self.env.results)

    def calculate_ref_contrast(self):
        '''
        ##############################################
        apply the masks and process the information
        ———————
        Input: 
        - MIEZE data object
        - Mask object
        - the key links to the value that will be reference
        ———————
        Output: -
        ##############################################
        '''

        #generate the mask adapted to this dataset
        self.env.mask.process_mask(
            self.env.current_data)

        #calculate the contrast
        self.env.fit['calc_ref_contrast'](
            self.env.current_data, 
            self.env.mask, 
            self.env.results)

    def calculate_contrast(self):
        '''
        ##############################################
        apply the masks and process the information
        ———————
        Input: 
        - enviroenment
        ———————
        Output: -
        ##############################################
        '''
        #generate the mask adapted to this dataset
        self.env.mask.process_mask(
            self.env.current_data)

        #calculate the contrast
        self.env.fit['calc_contrast'](
            self.env.current_data, 
            self.env.mask, 
            self.env.results)

        #fit the contrast data
        self.env.fit['fit_contrast'](
            self.env.current_data, 
            self.env.mask, 
            self.env.results)

class Process_SANS(Process_Handler):
    
    def __init__(self, env):
        '''
        ##############################################
        This class is a subs process class that cont-
        ains the method related to processing the 
        SANS data
        ———————
        Input: 
        - environnement
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #initialize the superclass
        Process_Handler.__init__(self, env)
        self.env = env

    def calculate_intensity(self):
        '''
        ##############################################
        process the intensity vs. parameter calculation
        ———————
        Input: 
        - environment
        ———————
        Output: -
        ##############################################
        '''
        #generate the mask adapted to this dataset
        self.env.mask.process_mask(
            self.env.current_data)

        #process the intensity calculations
        self.env.fit['intensity'](
            self.env.current_data, 
            self.env.mask, 
            self.env.results)
