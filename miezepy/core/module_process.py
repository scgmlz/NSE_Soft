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
from .fit_modules.library_fit import miezeTauProcessing

def getProcessStructure(env):
    '''
    Will return the right fit manager depending 
    on the initial input
    Input: target (Data_Structure)
    '''
    if env.select == 'MIEZE':
        return Process_MIEZE(env)
    if env.select == 'SANS':
        return Process_SANS(env)
    else:
        print('Could not find the process class you are looking for. Error...')
        return None

class Process_Handler:

    def __init__(self, env):
        '''
        This is the initializer of all the 
        '''
        self.env = env

    def extract_from_metadata(self, axis, key):
        '''
        This function will populate the axis with a 
        given metadata entry and then collapse the
        axis around it.  
        ———————
        Input: 
        - data_structure class (loaded already)
        - mask object
        - fit object
        '''
        idx = self.env.current_data.axes.names.index(axis)
        self.env.current_data.axes.grab_meta(idx, key, self.env.current_data)
        self.env.current_data.axes.collapse_axis(idx, self.env.current_data)

class Process_MIEZE(Process_Handler):

    def __init__(self, env):
        '''
        This class is a subs process class that 
        contains the method related to processing the 
        MIEZE data
        '''
        Process_Handler.__init__(self, env)
        self.env = env
        self.initialize()

    def initialize(self):
        '''
        Initialize the default python scipts so that 
        the system can be set.
        '''
        self.default_scripts = []
        with open(
            os.path.dirname(os.path.realpath(__file__))
            + '/process_modules/import_process.py','r') as f:
            self.default_scripts.append(f.read())
        with open(
            os.path.dirname(os.path.realpath(__file__))
            + '/process_modules/set_fit_process.py','r') as f:
            self.default_scripts.append(f.read())
        with open(
            os.path.dirname(os.path.realpath(__file__))
            + '/process_modules/phase_process.py','r') as f:
            self.default_scripts.append(f.read())
        with open(
            os.path.dirname(os.path.realpath(__file__))
            + '/process_modules/reduction_process.py','r') as f:
            self.default_scripts.append(f.read())
        with open(os.path.dirname(
            os.path.realpath(__file__))
            + '/process_modules/post_process.py','r') as f:
            self.default_scripts.append(f.read())

        self.editable_scripts = list(self.default_scripts)

    def loadScripts(self, path):
        '''
        Initialize the default python scipts so that 
        the system can be set.
        '''
        with open(path,'r') as f:
            text = f.read()

        if 'metadata_class.add_metadata' in text:
            text = self.reformatScript(text)

        check = text.split('##--FIT-PARA--##')
        if len(check) > 1:
            file_type = 'new'
        else:
            file_type = 'old'

        if file_type == 'old':
            strings = [
                text.split('##--IMPORT--##')[1],
                text.split('##--PHASE--##')[1].split(
                    'value = foils_in_echo)')[0]+'value = foils_in_echo)',
                'environnement = self.env\n'+text.split('##--PHASE--##')[1].split(
                    'value = foils_in_echo)')[1],
                text.split('##--REDUCTION--##')[1],
                text.split('##--POST--##')[1] ]
        elif file_type == 'new':
            strings = [
                text.split('##--IMPORT--##')[1],
                text.split('##--FIT-PARA--##')[1],
                text.split('##--PHASE--##')[1],
                text.split('##--REDUCTION--##')[1],
                text.split('##--POST--##')[1]]

        self.editable_scripts = list(strings)

    def reformatScript(self, text):
        '''
        This function will reformat the text input to meet the
        new specifications of our software. Most function calls
        have been updated.

        Parameters
        ----------
        text : string
            The formated text to be formater

        Returns
        ------- 
        text : string
            The formated text to returned to the text importer
        '''
        text = text.replace('add_metadata', 'addMetadata')
        text = text.replace('get_result', 'results.getLastResult')
        text = text.replace('calculate_echo', 'calculateEcho')
        text = text.replace('calculate_shift', 'calcShift')
        text = text.replace('calculate_ref_contrast', 'calcContrastRef')
        text = text.replace('calculate_contrast', 'calcContrastMain')
        text = text.replace('environnement.process.remove_foils()\n', '')

        return text

    def saveScripts(self, path, strings):
        '''
        Initialize the default python scipts so that 
        the system can be set.
        ———————
        Input: 
        - path (str) file path to be saved
        - strings([str]) scripts 
        '''
        string = (
            "##--IMPORT--##\n"
            + strings[0]
            + "\n##--IMPORT--##\n"
            "##--FIT-PARA--##\n"
            + strings[1]
            + "\n##--FIT-PARA--##\n"
            + "##--PHASE--##\n"
            + strings[2]
            + "\n##--PHASE--##\n"
            + "##--REDUCTION--##\n"
            + strings[3]
            + "\n##--REDUCTION--##\n"
            + "##--POST--##\n"
            + strings[4]
            + "\n##--POST--##\n")

        f = open(path, 'w')
        f.write(string)
        f.close()

    def calculateEcho(self):
        '''
        This function will calculate the echo times of 
        the dataset depending on the input of the 
        matdata from both the data_objects and the 
        dataclass itself
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
        local_results = self.env.results.generateResult( name = 'Echo Sources')
        echo_dict = {}

        for metadata_object in self.env.current_data.metadata_objects:
            result = miezeTauProcessing(metadata_object, self.env.current_data)
            echo_dict[result[0]] = result[1]

        local_results['Echo Dict'] = echo_dict
        local_results.addLog('info', 'Computation of the shift was a success')
        local_results.setComplete()
        self.extract_from_metadata(self.env.current_data.axes.names[2],'tau')
        self.prepareBuffer()

    def prepareBuffer(self):
        '''
        Tell the datclass to process the buffer of 
        the dataset
        '''
        self.env.current_data.bufferAsNumpy()

    def calcShift(self):
        '''
        Calculate and process the phase shift of the 
        dataset if required.
        '''
        #generate the mask adapted to this dataset
        self.env.mask.generateMask(
            self.env.current_data.data_objects[0].dim[0],
            self.env.current_data.data_objects[0].dim[1])
        
        #extract the phase
        self.env.fit.extractPhaseMask(
            self.env.current_data, 
            self.env.mask, 
            self.env.results)

        #process the shift
        self.env.fit.correctPhase(
            self.env.current_data, 
            self.env.mask, 
            self.env.results)

    def calcContrastRef(self):
        '''
        Calculate the contrast of the reference measurement.
        '''
        #generate the mask adapted to this dataset
        self.env.mask.generateMask(
            self.env.current_data.data_objects[0].dim[0],
            self.env.current_data.data_objects[0].dim[1])

        #calculate the contrast
        self.env.fit.calcContrastRef(
            self.env.current_data, 
            self.env.mask, 
            self.env.results)

    def calcContrastMain(self):
        '''
        Calculate and process the contrast of all measurement.
        '''
        #generate the mask adapted to this dataset
        self.env.mask.generateMask(
            self.env.current_data.data_objects[0].dim[0],
            self.env.current_data.data_objects[0].dim[1])

        #calculate the contrast
        self.env.fit.calcContrastMain(
            self.env.current_data, 
            self.env.mask, 
            self.env.results)

        #fit the contrast data
        self.env.fit.contrastFit(
            self.env.current_data, 
            self.env.mask, 
            self.env.results)

class Process_SANS(Process_Handler):
    
    def __init__(self, env):
        '''
        This class is a subs process class that 
        contains the method related to processing the 
        SANS data
        '''
        #initialize the superclass
        Process_Handler.__init__(self, env)
        self.env = env

    def calculate_intensity(self):
        '''
        process the intensity vs. parameter calculation
        '''
        #generate the mask adapted to this dataset
        self.env.mask.generateMask(
            self.env.current_data.data_objects[0].dim[0],
            self.env.current_data.data_objects[0].dim[1])

        #process the intensity calculations
        self.env.fit['intensity'](
            self.env.current_data, 
            self.env.mask, 
            self.env.results)
