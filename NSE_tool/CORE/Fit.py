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
import iminuit
import numpy as np
import scipy
import warnings
import copy
import math
import timeit
 
from scipy import special as sp
from scipy import integrate as integrate
from scipy import special as sp
from scipy import constants as co
from scipy import optimize as op
from scipy import stats as st

#############################
#import child components
from .Log import Log_Handler
    
def get_fit_handler(select):
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

        return Fit_MIEZE()

    if select == 'SANS':

        return Fit_SANS()

    else:

        print('Could not find the fit class you are looking for. Error...')
        
        return None


class Fit_Handler():

    def __init__(self):
        '''
        ##############################################
        This is the initializer of the fit class
        within.
        ———————
        Input: target (Data_Structure)
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.fun_dict   = {}
        self.ptr_dict   = {}
        self.para_dict  = {}
        self.log        = Log_Handler()
        self.verbose    = False

    def __getitem__(self, key):
        '''
        ##############################################
        This getitem method will be transfered to the
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
        ———————
        Output: -
        ———————
        status: active
        ##############################################
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
        ##############################################
        This fucntion will try to select the right
        pointer for the right method
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
        if target in self.fun_dict and identifier in self.ptr_dict:

            self.fun_dict[target]= self.ptr_dict[identifier]

        else:

            print('The input keys do not match existing functions')

    def set_parameter(self, name = '', value = ''):
        '''
        ##############################################
        This function will allow the user to inject
        fit parameters...
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.para_dict[name] = value

class Fit_SANS(Fit_Handler):

    def __init__(self):
        '''
        ##############################################
        This is the initializer of the SANS fit class
        within. It will also initialize the superclass
        containing the generalized methods.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #initialize the superclass
        Fit_Handler.__init__(self)

        self.ptr_dict = {}
        self.ptr_dict['intensity']      = self.intensity_vs_parameter
        self.set_defaults()
        self.set_fit_parameters()

    def set_defaults(self):
        '''
        ##############################################
        This function will build the default 
        dictionary of function dict that will linkt 
        the functions to the selected method
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        self.fun_dict = {}
        self.fun_dict['intensity']     = self.ptr_dict['intensity']

    def set_fit_parameters(self):
        '''
        ##############################################
        This function will build the default 
        dictionary of function dict that will linkt 
        the functions to the selected method
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        ############################################
        #pack them into the dictionary
        self.para_dict = {}
        self.para_dict['BG substraction']   = None

    def intensity_vs_parameter(self, target, mask, results):
        '''
        ##############################################
        This method aims atprocessing the SANS
        intensity against the a given parameter
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        ##############################################
        #Initialize the output dictionary with all def.
        local_results = results.generate_result( name = 'Intensity')

        ##############################################
        #Initialize the output dictionary with all def.
        mask            = mask.mask
        intensity       = {}
        intensity_error = {}
        axis            = {}

        ##############################################
        #process BG metadata if necessary
        if not self.para_dict['BG substraction'] == None:

            BG_target = target.get_slice([self.para_dict['BG substraction']])

            monitor_BG = BG_target.get_metadata([0])[0]['monitor']

        ##############################################
        #loop over and process
        for idx_0 in range(len(target.axes.axes[0])):
            
            #set the key for data saving
            key  = target.axes.axes[0][idx_0]

            #process the data slice
            new_target = target.get_slice([key])
            data       = new_target.return_as_np()

            #set the axis
            axis[key]               = new_target.axes.axes[0]
            intensity[key]          = np.zeros(len(new_target.axes.axes[0]))
            intensity_error[key]    = np.zeros(len(new_target.axes.axes[0]))

            for idx_1 in range(new_target.axes.axes_len[0]):

                #grab the metadata
                monitor = new_target.get_metadata([idx_1])[0]['monitor']

                if self.para_dict['BG substraction'] == None:

                    #process the instensity
                    intensity[key][idx_1] = np.sum(data[idx_1]*mask)/monitor/np.sum(mask)

                    #process its error
                    intensity_error[key][idx_1] = np.sqrt(np.sum(data[idx_1]*mask))/monitor/np.sum(mask)

                else:
                
                    if data[0].shape[0] == data[idx_1].shape[0]:
                        
                        #process the instensity
                        intensity[key][idx_1] = np.sum(data[idx_1]*mask)/monitor/np.sum(mask) - np.sum(BG_target[0]*mask)/monitor_BG/np.sum(mask)

                        #process its error
                        intensity_error[key][idx_1] = np.sqrt(np.sum(data[idx_1]*mask)/monitor**2/np.sum(mask)**2 + np.sum(BG_target[0]*mask)/monitor_BG**2/np.sum(mask)**2)

                    else:

                        #process the instensity
                        intensity[key][idx_1] = (
                            np.sum(data[idx_1] * mask)
                            / monitor
                            /np.sum(mask) 
                            - np.sum(BG_target[0]*mask)
                            /monitor_BG
                            /np.sum(mask))
                        
                        #process its error
                        intensity_error[key][idx_1] = (np.sqrt(
                            np.sum(data[idx_1]*mask)/monitor**2/np.sum(mask)**2 
                            + np.sum(BG_target[0]*mask)/monitor_BG**2/np.sum(mask)**2))

        
        ##############################################
        #finalize result and send it out
        local_results['Intensity']       = intensity
        local_results['Intensity_error'] = intensity_error
        local_results['Axis']            = axis
    
        #write the dictionary entries
        local_results.add_log('info', 'Computation of the intensity was a success')
        local_results.set_complete()

        #tell fit handler what happened
        self.log.add_log(
            'Info', 
            'Computation of the intensity was a success')

class Fit_MIEZE(Fit_Handler):

    def __init__(self):
        '''
        ##############################################
        This is the initializer of the MIEZE fit class
        within. It will also initialize the superclass
        containing the generalized methods.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        #initialize the superclass
        Fit_Handler.__init__(self)

        self.ptr_dict = {}

        self.ptr_dict['mieze_tau']          = self.mieze_tau
        self.ptr_dict['extract_phase']      = self.extract_phase
        self.ptr_dict['fit_cov']            = self.fit_data_cov 
        self.ptr_dict['fit_goodness']       = self.fit_goodness
        self.ptr_dict['minuit_cos']         = self.minuit_fit_cosine
        self.ptr_dict['calc_shift']         = self.calc_shift
        self.ptr_dict['calc_contrast']      = self.calc_contrast
        self.ptr_dict['fit_contrast']       = self.fit_contrast
        self.ptr_dict['minuit_exp']         = self.minuit_fit_exp
        self.ptr_dict['calc_ref_contrast']  = self.calc_contrast_reference
        
        self.set_defaults()
        self.set_fit_parameters()

    def set_defaults(self):
        '''
        ##############################################
        This function will build the default 
        dictionary of function dict that will linkt 
        the functions to the selected method
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        self.fun_dict = {}

        self.fun_dict['mieze_tau']          = self.ptr_dict['mieze_tau']
        self.fun_dict['extract_phase']      = self.ptr_dict['extract_phase']
        self.fun_dict['fit_cov']            = self.ptr_dict['fit_cov']
        self.fun_dict['fit_goodness']       = self.ptr_dict['fit_goodness']
        self.fun_dict['minuit_cos']         = self.ptr_dict['minuit_cos']
        self.fun_dict['calc_shift']         = self.ptr_dict['calc_shift']
        self.fun_dict['calc_contrast']      = self.ptr_dict['calc_contrast']
        self.fun_dict['fit_contrast']       = self.ptr_dict['fit_contrast']
        self.fun_dict['calc_ref_contrast']  = self.ptr_dict['calc_ref_contrast']
        self.fun_dict['minuit_exp']         = self.ptr_dict['minuit_exp']


    def set_fit_parameters(self):
        '''
        ##############################################
        This function will build the default 
        dictionary of function dict that will linkt 
        the functions to the selected method
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        ############################################
        #pack them into the dictionary
        self.para_dict = {}

        self.para_dict['foils_in_echo'] = []
        self.para_dict['Background']    = []
        self.para_dict['Reference']     = None
        self.para_dict['Select']        = []
    
        ############################################
        #set deafult pointers
        self.para_dict['para_name'] = 'Temperature'
        self.para_dict['echo_name'] = 'Echo'
        self.para_dict['meas_name'] = 'Measurement'
        self.para_dict['foil_name'] = 'Foil'
        self.para_dict['tcha_name'] = 'Time Channel'


    def mieze_tau(self, metadata_object, target):
        '''
        ##############################################
        Processes the MIEZE time
        ———————
        Input: MIEZE metadata object
        ———————
        Output: 
        injects the Mieze time into the 
        metadata
        ##############################################
        '''
        ############################################
        #unpack the container
        wavelength  = metadata_object['wavelength'] * 1.e-10 
        freq_0      = metadata_object['freq_0']
        freq_1      = metadata_object['freq_1']
        lsd         = metadata_object['lsd'] * 1.e9 

        ############################################
        #process tau and the error of tau
        delta_freq = freq_1 - freq_0
        para = ( 2. * co.m_n ** 2 ) / (co.h ** 2) 

        tau = para * wavelength ** 3 * delta_freq * lsd 

        #systematic errors: wavelength 11.7%, distance 0.0005m, deltafreq neglectable 
        tau_error = para * ( 
            ( target.metadata_class['Wavelength error'] * wavelength * 3 * wavelength ** 2 * delta_freq * lsd )
            + ( target.metadata_class['Distance error'] * lsd *  wavelength ** 3 * delta_freq )
            )

        ############################################
        #send it out to the metadata class
        metadata_object.add_metadata('tau', value = tau)
        metadata_object.add_metadata('tau_error', value = tau_error)

    def test_parameter(self, value, target, mask, results):
        '''
        ##############################################
        Test function on the input parameters. This is
        called by the paramter vamlue which gives the
        variable to test.
        ———————
        Input: 
        - value (str)
        - MIEZE metadata object
        - mask object
        ———————
        Output: 
        - will return either false or the selected
        value.  
        ##############################################
        '''
        ############################################
        #perform the check on test
        if value == 'Select':
            
            select = self.para_dict['Select']

            
            if not isinstance(select, list):

                print('Select needs to be a list. Error...')

                return False

            else:

                if select[0] == 'all':

                    select = list(target.axes.axes[0])

                    return select
                else:
                    try:

                        [target.axes.axes[0].index(selected) for selected in select]

                    except:

                        print('The values do not match the axes. Error...')

                        return False
                    
                    return select

        ############################################
        #perform the check on test
        elif value == 'foils_in_echo':

            foils_in_echo = self.para_dict['foils_in_echo']

            #--FIX--
            #check the dimension of this list
            if not len(foils_in_echo) == target.axes.axes_len[2]:

                print('Not enought foils_in_echo initialised. Error...')
                return False

            elif not all([len(element) == target.axes.axes_len[3] for element in foils_in_echo ]):

                print('Not enought foils_in_echo initialised. Error...')
                return False

            elif foils_in_echo == []:

                print('Sine foils not set by the user. Error...')
                return False

            else:

                return foils_in_echo

        ############################################
        #perform a test on BG
        elif value == 'Background':

            BG = self.para_dict['Background']

            #check the dimension of this list
            if not BG == None and not BG in target.axes.axes[0]:

                print('The background is not in the loaded data. Error...')
                return False

            else:

                return BG


        ############################################
        #perform a test on the referece
        elif value == 'Reference':

            reference = self.para_dict['Reference']

            #check the dimension of this list
            if not reference == None and not reference in target.axes.axes[0]:

                print('This reference does not exist. Error...')
                return False

            else:

                return reference

        ############################################
        #perform a test on the referece
        elif len(value.split('name')) > 1 :

            if self.para_dict[value] in target.axes.names:

                return self.para_dict[value]

            else:

                print('The axis name does not exist in the provided data. Error...')
                return False

        else:

            print('Value to test not found. Error...')
            return False

    def calc_contrast_fit(self,select, foils_in_echo, shift, target, mask, results):
        '''
        ##############################################
        This function will process the fit of the
        given input.
        ———————
        Input: 
        - select (list)
        - MIEZE metadata object
        - mask object
        ———————
        Output: 
        - will return the result array 
        ##############################################
        '''
        premask = mask.mask
        local_results = {}

        #set up the parameter names
        para_name = self.para_dict['para_name']
        echo_name = self.para_dict['echo_name']
        meas_name = self.para_dict['meas_name']
        foil_name = self.para_dict['foil_name']
        tcha_name = self.para_dict['tcha_name']

        ############################################
        #loop over elements
        loop = [
            (e1, e2) 
            for e1 in select 
            for e2 in target.get_axis(meas_name)]

        for key, meas in loop:

            #grab the data slice
            new_target          = target.get_slice([key, meas])

            #if measurement it 0 initate the dicitoanry
            if meas == 0:

                local_results[key]    = {}

            if not new_target == False:
                    
                #print out the processing step
                print(
                    'Processing the contrast fit for: '
                    +str(key)
                    +target.get_axis_unit(para_name)
                    +' measurement '
                    +str(meas)
                    +target.get_axis_unit(meas_name))

                local_results[key][meas]    = {}

                ############################################
                for echo in new_target.get_axis(echo_name):

                    #initialise data
                    combined_data = np.zeros(new_target.get_axis_len(tcha_name))

                    #reduce the foils
                    for foil in new_target.get_axis(foil_name):

                        #grab idx for the values.
                        echo_idx_0  = target.get_axis_idx(echo_name, echo)
                        echo_idx_1  = new_target.get_axis_idx(echo_name, echo)
                        foil_idx    = new_target.get_axis_idx(foil_name, foil)

                        #logical check
                        if foils_in_echo[echo_idx_0][foil_idx] == True:
                            
                            data = np.array(
                                [(np.multiply(shift[key][meas][echo][foil_idx,tcha_idx],premask)).sum() 
                                for tcha_idx in range(new_target.get_axis_len(tcha_name))])
                            
                            combined_data += data

                    ############################################
                    #fit the data
                    self['fit_cov'](
                        results,
                        combined_data, 
                        np.sqrt(combined_data), 
                        Qmin = 0.,
                        time_chan = new_target.get_axis_len(tcha_name)
                        )

                    #process the result of the fit
                    result = results.get_last_result('Fit data covariance')

                    ############################################
                    #!!!BUG!!!!
                    monitor = int(1.e-3 * int((new_target.get_metadata([echo_idx_1,0,0])[0]['monitor'])))

                    ############################################
                    #process the result
                    local_results[key][meas][echo] = [
                        result['ampl']/monitor,
                        result['ampl_error']/monitor,
                        result['mean']/monitor,
                        result['mean_error']/monitor]

                    
        return local_results

    def calc_contrast_fit_single(self,foil, select, target, mask, results):
        '''
        ##############################################
        This function will process the fit of the
        given input.
        ———————
        Input: 
        - select (list)
        - MIEZE metadata object
        - mask object
        ———————
        Output: 
        - will return the result array 
        ##############################################
        '''
        premask = mask.mask
        local_results = {}
        shift = results.get_last_result('Shift calculation', 'Shift')

        #set up the parameter names
        para_name = self.para_dict['para_name']
        echo_name = self.para_dict['echo_name']
        meas_name = self.para_dict['meas_name']
        foil_name = self.para_dict['foil_name']
        tcha_name = self.para_dict['tcha_name']

        ############################################
        #loop over elements
        loop = [
            (e1, e2) 
            for e1 in select 
            for e2 in target.get_axis(meas_name)]

        for key, meas in loop:

            #grab the data slice
            new_target          = target.get_slice([key, meas])

            #if measurement it 0 initate the dicitoanry
            if meas == 0:

                local_results[key]    = {}

            if not new_target == False:
                    
                #print out the processing step
                print(
                    'Processing the contrast fit for: '
                    +str(key)
                    +target.get_axis_unit(para_name)
                    +' measurement '
                    +str(meas)
                    +target.get_axis_unit(meas_name))

                local_results[key][meas]    = {}

                ############################################
                for echo in new_target.get_axis(echo_name):

                    #grab idx for the values.
                    echo_idx_1  = new_target.get_axis_idx(echo_name, echo)
                    foil_idx    = new_target.get_axis_idx(foil_name, foil)
                        
                    combined_data = np.array(
                        [(np.multiply(shift[key][meas][echo][foil_idx,tcha_idx],premask)).sum() 
                        for tcha_idx in range(new_target.get_axis_len(tcha_name))])
                    
                    ############################################
                    #fit the data
                    self['fit_cov'](
                        results,
                        combined_data, 
                        np.sqrt(combined_data), 
                        Qmin = 0.,
                        time_chan = new_target.get_axis_len(tcha_name)
                        )

                    #process the result of the fit
                    result = results.get_last_result('Fit data covariance')

                    ############################################
                    #get monitor value
                    monitor = new_target.get_metadata([echo_idx_1,0,0])[0]['monitor']

                    ############################################
                    #process the result
                    local_results[key][meas][echo] = [
                        result['ampl']/monitor,
                        result['ampl_error']/monitor,
                        result['mean']/monitor,
                        result['mean_error']/monitor]
                    
        return local_results

    def calc_contrast_reference(self,target, mask, results):
        '''
        ##############################################
        uses self.shifted to combine foils and 
        calculates contrast for chosen foils for 
        certain echos
        ———————
        Input: 
        - MIEZE metadata object
        - mask object
        ———————
        Output: -
        ##############################################
        '''
        ##############################################
        #Initialize the output dictionary with all def.
        local_results = results.generate_result(name = 'Reference contrast calculation')

        ############################################
        #extract the relevant parameters
        shift           = results.get_last_result('Shift calculation', 'Shift')
        foils_in_echo   = self.test_parameter('foils_in_echo', target, mask, results)
        reference       = self.test_parameter('Reference', target, mask, results)

        #initilise the contrast result
        contrast_ref        = {}
        contrast_ref_error  = {}

        ############################################
        #process reference
        print(
            'Processing the reference contrast calculation for: '
            +str(reference)
            +target.axes.units[0])

        ref_result = self.calc_contrast_fit(
            [reference], 
            foils_in_echo, 
            shift, 
            target, 
            mask,
            results)

        ############################################
        #Process the result
        for echo in ref_result[reference][0].keys():

            #do a check of the value and throw an error if 0
            if ref_result[reference][0][echo][0] == 0:

                local_results.add_log('warning', 'The amplitude from the reference fit is 0. Please investigate...')
                local_results.add_log('error', 'Setting the value to 1')
                ref_result[reference][0][echo][0] = 1.
                ref_result[reference][0][echo][1] = 1.

            #do a check of the value and throw an error if 0
            if ref_result[reference][0][echo][2] == 0:

                local_results.add_log('error', 'The mean from the reference fit is 0. Please investigate...')
                local_results.add_log('error', 'Setting the value to 1')
                ref_result[reference][0][echo][2] = 1.
                ref_result[reference][0][echo][3] = 1.

            contrast_ref[echo]       = ref_result[reference][0][echo][0]/ref_result[reference][0][echo][2]
            contrast_ref_error[echo] = (
                np.sqrt(

                    ( ref_result[reference][0][echo][1]
                    / ref_result[reference][0][echo][0]  )**2

                    +( ref_result[reference][0][echo][3]
                    /  ref_result[reference][0][echo][2] )**2 )

                *ref_result[reference][0][echo][0]
                /ref_result[reference][0][echo][2])

        ############################################
        #Process the result
        local_results['Reference']            = reference
        local_results['Contrast_ref']         = contrast_ref
        local_results['Contrast_ref_error']   = contrast_ref_error

        #write the dictionary entries
        local_results.add_log('info', 'Computation of the contrast was was a success')
        local_results.set_complete()

    def calc_contrast(self,target, mask, results, select = False, foil = None):
        '''
        ##############################################
        uses self.shifted to combine foils and 
        calculates contrast for chosen foils for 
        certain echos
        ———————
        Input: 
        - MIEZE metadata object
        - mask object
        ———————
        Output: -
        ##############################################
        '''
        ##############################################
        #Initialize the output dictionary with all def.
        local_results = results.generate_result( name =  'Contrast calculation')

        ############################################
        #extract the relevant parameters
        shift           = results.get_last_result('Shift calculation', 'Shift')
        BG              = self.test_parameter('Background', target, mask, results)

        if select == False:
            select          = self.test_parameter('Select', target, mask, results)

        foils_in_echo   = self.test_parameter('foils_in_echo', target, mask, results)

        #set up the parameter names
        para_name = self.test_parameter('para_name', target, mask, results)
        echo_name = self.test_parameter('echo_name', target, mask, results)
        meas_name = self.test_parameter('meas_name', target, mask, results)

        if any([element == False for element in [select, foils_in_echo, BG]]):

            return False

        ############################################
        #contrast calculation
        contrast_results = self.calc_contrast_fit(
            select, 
            foils_in_echo, 
            shift, 
            target, 
            mask,
            results)

        ############################################
        #initilise the contrast result
        contrast            = {}
        contrast_error      = {}
    
        ############################################
        #process Background
        if not BG == None:

            print(
                'Processing the Background contrast calculation for: '
                +str(BG)
                +target.axes.units[0])

            BG_result = self.calc_contrast_fit(
                [BG], 
                foils_in_echo, 
                shift, 
                target, 
                mask,
                results)

        ############################################
        #prepare the axis for by adding different 
        #measurements
        axis = {}
        pos  = {}

        #set the loop
        loop = [
            (e1, e2) 
            for e1 in select 
            for e2 in target.get_axis(meas_name)]

        #current values comparators
        c_key   = None

        #loop
        for key, meas in loop:

            #grab the data slice
            new_target          = target.get_slice([key, meas])

            #check if we switched the key
            if not c_key == key and not new_target == False:

                #initialise the dictionary
                axis[key] = []
                pos[key]  = []

                #set the current keys
                c_key   = key

            #grab axis information
            if not new_target == False:

                for i in range(new_target.get_axis_len(echo_name)):

                    axis[key].append(new_target.get_axis_val(echo_name, i))
                    pos[key].append((meas, new_target.get_axis_val(echo_name, i)))


        ############################################
        #now process the data on the axis
        for key in axis.keys():

            #if measurement it 0 initate the dicitoanry
            contrast[key]       = []
            contrast_error[key] = []

            #grab the data slice
            new_target          = target.get_slice([key])

            #print it out
            print(
                'Processing the contrast calculation for: '
                +str(key)
                +target.get_axis_unit(para_name)
                )

            for meas, echo in pos[key]:

                if BG == None and not BG == key:

                    #set the contrast data
                    ctrst = abs(contrast_results[key][meas][echo][0]/contrast_results[key][meas][echo][2])
                    ctrst_err = (
                        np.sqrt(
                            
                            (contrast_results[key][meas][echo][1]
                            /contrast_results[key][meas][echo][0])**2

                            +(contrast_results[key][meas][echo][3]
                            /contrast_results[key][meas][echo][2])**2)

                        *contrast_results[key][meas][echo][0]
                        /contrast_results[key][meas][echo][2])

                elif not BG == None and not BG == key:

                    ctrst = ((
                        abs(contrast_results[key][meas][echo][0])-abs(BG_result[BG][0][echo][0]))
                        /(contrast_results[key][meas][echo][2]-BG_result[BG][0][echo][2]))

                    ctrst_err =np.sqrt(

                            (contrast_results[key][meas][echo][1]
                                /(contrast_results[key][meas][echo][2]-BG_result[BG][0][echo][2]))**2

                            + (BG_result[BG][0][echo][1]
                                /(contrast_results[key][meas][echo][2]-BG_result[BG][0][echo][2]))**2

                            + ((abs(contrast_results[key][meas][echo][0])
                                -abs(BG_result[BG][0][echo][0]))
                                /(contrast_results[key][meas][echo][2]-BG_result[BG][0][echo][2])**2
                                *contrast_results[key][meas][echo][3])**2

                            + ((abs(contrast_results[key][meas][echo][0])
                                -abs(BG_result[BG][0][echo][0]))
                                /(contrast_results[key][meas][echo][2]-BG_result[BG][0][echo][2])**2
                                *BG_result[BG][0][echo][3])**2
                    )

                contrast[key].append(float(ctrst))
                contrast_error[key].append(float(ctrst_err))

        ##############################################
        #finalize result and send it out
        local_results['Axis']                 = axis
        local_results['Contrast']             = contrast
        local_results['Contrast_error']       = contrast_error
        local_results['Background']           = BG
    
        #write the dictionary entries
        local_results.add_log('info', 'Computation of the contrast was was a success')
        local_results.set_complete()

        #tell fit handler what happened
        self.log.add_log(
            'Info', 
            'Computation of the contrast was was a success')


    def calc_contrast_single_foil(self, foil, select, target, mask, results):
        '''
        ##############################################
        uses self.shifted to combine foils and 
        calculates contrast for chosen foils for 
        certain echos
        ———————
        Input: 
        - MIEZE metadata object
        - mask object
        ———————
        Output: -
        ##############################################
        '''
        ##############################################
        #Initialize the output dictionary with all def.
        local_results = results.generate_result( name = 'Contrast calculation single')

        ############################################
        #extract the relevant parameters
        shift           = results.get_last_result('Shift calculation', 'Shift')
        foils_in_echo   = self.para_dict['foils_in_echo']
        BG              = self.para_dict['Background']
        
        #set up the parameter names
        para_name = self.para_dict['para_name']
        echo_name = self.para_dict['echo_name']
        meas_name = self.para_dict['meas_name']

        ############################################
        #contrast calculation
        contrast_results = self.calc_contrast_fit_single(
            foil, 
            select,
            target, 
            mask,
            results)

        ############################################
        #initilise the contrast result
        contrast            = {}
        contrast_error      = {}
        
        ############################################
        #process Background
        if not BG == None:

            print(
                'Processing the Background contrast calculation for: '
                +str(BG)
                +target.axes.units[0])

            BG_result = self.calc_contrast_fit(
                [BG], 
                foils_in_echo, 
                shift, 
                target, 
                mask,
                results)

        ############################################
        #prepare the axis for by adding different 
        #measurements
        axis = {}
        pos  = {}

        #set the loop
        loop = [
            (e1, e2) 
            for e1 in select 
            for e2 in target.get_axis(meas_name)]

        #current values comparators
        c_key   = None
        
        #loop
        for key, meas in loop:

            #grab the data slice
            new_target          = target.get_slice([key, meas])

            #check if we switched the key
            if not c_key == key and not new_target == False:

                #initialise the dictionary
                axis[key] = []
                pos[key]  = []

                #set the current keys
                c_key   = key

            #grab axis information
            if not new_target == False:

                for i in range(new_target.get_axis_len(echo_name)):

                    axis[key].append(new_target.get_axis_val(echo_name, i))
                    pos[key].append((meas, new_target.get_axis_val(echo_name, i)))

        ############################################
        #now process the data on the axis
        for key in axis.keys():

            #if measurement it 0 initate the dicitoanry
            contrast[key]       = []
            contrast_error[key] = []

            #grab the data slice
            new_target          = target.get_slice([key])

            #print it out
            print(
                'Processing the contrast calculation for: '
                +str(key)
                +target.get_axis_unit(para_name)
                )

            for meas, echo in pos[key]:

                if BG == None and not BG == key:

                    #set the contrast data
                    ctrst = abs(contrast_results[key][meas][echo][0]/contrast_results[key][meas][echo][2])
                    ctrst_err = (
                        np.sqrt(
                            
                            (contrast_results[key][meas][echo][1]
                            /contrast_results[key][meas][echo][0])**2

                            +(contrast_results[key][meas][echo][3]
                            /contrast_results[key][meas][echo][2])**2)

                        *contrast_results[key][meas][echo][0]
                        /contrast_results[key][meas][echo][2])

                elif not BG == None and not BG == key:

                    ctrst = ((
                        abs(contrast_results[key][meas][echo][0])-abs(BG_result[BG][0][echo][0]))
                        /(contrast_results[key][meas][echo][2]-BG_result[BG][0][echo][2]))

                    ctrst_err =np.sqrt(

                            (contrast_results[key][meas][echo][1]
                                /(contrast_results[key][meas][echo][2]-BG_result[BG][0][echo][2]))**2

                            + (BG_result[BG][0][echo][1]
                                /(contrast_results[key][meas][echo][2]-BG_result[BG][0][echo][2]))**2

                            + ((abs(contrast_results[key][meas][echo][0])
                                -abs(BG_result[BG][0][echo][0]))
                                /(contrast_results[key][meas][echo][2]-BG_result[BG][0][echo][2])**2
                                *contrast_results[key][meas][echo][3])**2

                            + ((abs(contrast_results[key][meas][echo][0])
                                -abs(BG_result[BG][0][echo][0]))
                                /(contrast_results[key][meas][echo][2]-BG_result[BG][0][echo][2])**2
                                *BG_result[BG][0][echo][3])**2
                    )

                contrast[key].append(float(ctrst))
                contrast_error[key].append(float(ctrst_err))

        ##############################################
        #finalize result and send it out
        local_results['Axis']                 = axis
        local_results['Contrast']             = contrast
        local_results['Contrast_error']       = contrast_error
        local_results['Background']           = BG
    
        #write the dictionary entries
        local_results.add_log('info', 'Computation of the contrast was was a success')
        local_results.set_complete()

        #tell fit handler what happened
        self.log.add_log(
            'Info', 
            'Computation of the contrast was was a success')

    def fit_contrast(self,target, mask, results):
        '''
        ##############################################
        In this function we will process the fit of 
        the data to allow fitting later on

        The package will be in dictionaries for each
        axis value
        ———————
        Input: 
        - MIEZE metadata object
        - mask object
        ———————
        Output: -
        ##############################################
        '''
        ##############################################
        #Initialize the output dictionary with all def.
        local_results = results.generate_result( name = 'Contrast fit')

        ############################################
        #get the last contrast computaiton result
        contrast            = results.get_last_result('Contrast calculation', 'Contrast')
        contrast_error      = results.get_last_result('Contrast calculation', 'Contrast_error')

        contrast_ref        = results.get_last_result('Reference contrast calculation','Contrast_ref')
        contrast_ref_error  = results.get_last_result('Reference contrast calculation','Contrast_ref_error')

        BG                  = results.get_last_result('Contrast calculation', 'Background')
        axis                = results.get_last_result('Contrast calculation', 'Axis')

        #set parameters
        select              = self.test_parameter('Select', target, mask, results)
        reference           = self.test_parameter('Reference', target, mask, results)
        axis_unit           = target.axes.units[0]
        x_unit              = target.axes.units[0]

        Output = {}
        Output['Gamma']         = {}
        Output['Gamma_error']   = {}
        Output['Curve']         = {}
        Output['Parameters']    = {}

        for key in contrast.keys():

            #load the data
            x           = np.asarray(axis[key])
            data        = np.asarray(contrast[key])
            data_error  = np.asarray(contrast_error[key])
            ref_data    = np.asarray([contrast_ref[echo] for echo in x])
            ref_error   = np.asarray([contrast_ref_error[echo] for echo in x])
            
            if not reference == None:

                #set the data to fit
                y       = abs(data / ref_data)
                y_error = y * np.sqrt(
                    (data_error / data) ** 2
                    + (ref_error / ref_data) ** 2)

            else:

                y = np.abs(data)
                y_error = data_error

            #fit the data
            fit = self['minuit_exp']( y, x, y_error)

            #prepare the result
            Output['Parameters'][key]  = {
                'x' : x,
                'x_unit' : x_unit,
                'y' : y,
                'y_error' : y_error}

            Output['Gamma'][key]       = fit['Gamma']
            Output['Gamma_error'][key] = fit['Gamma_error']
            Output['Curve'][key]       = fit['Curve']

        ############################################
        #set the other informations
        local_results['Gamma']        = Output['Gamma']         
        local_results['Gamma_error']  = Output['Gamma_error']  
        local_results['Curve']        = Output['Curve']   
        local_results['Parameters']   = Output['Parameters']       
        local_results['Select']       = select
        local_results['BG']           = BG
        local_results['Reference']    = reference
        local_results['Axis']         = axis
        local_results['Axis_unit']    = axis_unit

        #write the dictionary entries
        local_results.add_log('info', 'Fitting of the contrast was a success')
        local_results.set_complete()

        #tell fit handler what happened
        self.log.add_log(
            'info', 
            'Fitting of the contrast was a success')

    def calc_shift(self,target, mask, results):
        '''
        ##############################################
        Calculates the shift
        ———————
        Input: 
        - MIEZE data object
        - mask object
        ———————
        Output: -
        ##############################################
        '''

        ##############################################
        #Initialize the output dictionary with all def.
        local_results = results.generate_result( name = 'Shift calculation')

        ############################################
        #extract the relevant parameters
        premask     = mask.mask
        phase       = results.get_last_result('Phase calculation', 'Phase')

        ############################################
        #cycle over and fit
        #set up the parameter names
        para_name = self.test_parameter('para_name', target, mask, results)
        echo_name = self.test_parameter('echo_name', target, mask, results)
        meas_name = self.test_parameter('meas_name', target, mask, results)
        foil_name = self.test_parameter('foil_name', target, mask, results)
        tcha_name = self.test_parameter('tcha_name', target, mask, results)

        ############################################
        #loop over elements
        loop = [
            (e1, e2) 
            for e1 in target.get_axis(para_name) 
            for e2 in target.get_axis(meas_name)]

        #current values comparators
        temp    = {}
        c_key   = None
        c_meas  = None

        #loop
        for key, meas in loop:

            #grab the data slice
            new_target = target.get_slice([key, meas])

            #check if we switched the key
            if not c_key == key:

                #initialise the dictionary
                temp[key] = {}

                #set the current keys
                c_key   = key
                c_meas  = None

            #check if we switched the measurement
            if not c_meas == meas and not new_target == False:
                
                #initialise the dictionary
                temp[key][meas] = {}

                #set the current keys
                c_meas  = meas

            #check if the data is right
            if not new_target == False:

                #prepare
                data        = new_target.return_as_np()
                time_int    = new_target.get_axis_len(tcha_name)
                time_float  = float(time_int)

                #print the processing step
                print(
                    'Processing shift for '
                    +str(key)
                    +' '
                    +str(target.get_axis_unit(para_name)))

                for echo in new_target.get_axis(echo_name):

                    #grab the idx for the echo
                    echo_idx = new_target.get_axis_idx(echo_name, echo)

                    #set the ranges
                    loop_2 = [
                        (m1, m2)
                        for m1 in range(1,premask.max()+1)
                        for m2 in range(new_target.get_axis_len(foil_name))] 
                    
                    #initialise variables
                    shifted_element = np.zeros((
                        new_target.get_axis_len(foil_name),
                        new_target.get_axis_len(tcha_name), 
                        new_target.data_objects[0].dim[0], 
                        new_target.data_objects[0].dim[1]))
                        
                    current_mask = None

                    #cycle over the elements
                    for mask_num, foil in loop_2:

                        if not mask_num == current_mask:

                            #select only one mask
                            mask = premask == mask_num
                            mask_sum = np.sum(mask)
                            current_mask = int(mask_num)

                        #select only one mask
                        index = np.arange(

                            int(round((
                                2*np.pi-np.sum(phase[echo][foil]*mask)/mask_sum)
                                /(2*np.pi/time_float)+np.pi/2.)),

                            int(round((
                                2*np.pi-np.sum(phase[echo][foil]*mask)/mask_sum)
                                /(2*np.pi/time_float)+np.pi/2.)+time_float)
                            
                            ,1)

                        index = np.asarray(
                            [index[i]%time_int 
                            for i in range(time_int)])
                        
                        shifted_element[foil,:, :, :] += data[echo_idx, foil, index,:,:]*mask

                    temp[key][meas][echo] = copy.deepcopy(shifted_element)

        ##############################################
        #finalize result and send it out
        local_results['Shift']        = temp

        #write the dictionary entries
        local_results.add_log('info', 'Computation of the shift was a success')
        local_results.set_complete()
        

        #tell fit handler what happened
        self.log.add_log(
            'info', 
            'Computation of the shift was a success')

    def extract_phase(self, target, mask, results):
        '''
        ##############################################
        Processes the MIEZE time
        ———————
        Input: 
        - MIEZE data object
        ———————
        Output: 
        - returns the phase..
        ##############################################
        '''
        ##############################################
        #Initialize the output dictionary with all def.
        local_results = results.generate_result( name = 'Phase calculation')

        ############################################
        #extract the relevant parameters
        selected_ref    = target.metadata_class['Resolution']
        reso_target     = target.get_slice(selected_ref)
        premask         = mask.mask

        ############################################
        #initialise variables
        phase = {}

        ############################################
        #set up the parameter names
        echo_name = self.test_parameter('echo_name', target, mask, results)
        foil_name = self.test_parameter('foil_name', target, mask, results)
        tcha_name = self.test_parameter('tcha_name', target, mask, results)

        ############################################
        #initialize
        for echo in reso_target.get_axis(echo_name):
            
            #initialise the dictionary
            phase[echo] = np.zeros((
                reso_target.get_axis_len(foil_name),
                reso_target.data_objects[0].dim[0],
                reso_target.data_objects[0].dim[1]
                ))

        ############################################
        #loop over elements
        loop = [
            (e1, e2, e3)
            for e1 in range(1,premask.max()+1)
            for e2 in reso_target.get_axis(echo_name)
            for e3 in reso_target.get_axis(foil_name)
        ]

        for mask_num, echo, foil in loop:
            
            #select only one mask
            mask = premask == mask_num
            #grab the idx for the echo
            echo_idx = reso_target.get_axis_idx(echo_name, echo)
            foil_idx = reso_target.get_axis_idx(foil_name, foil)

            #prepare the data
            counts = [
                (np.multiply(reso_target[echo_idx, foil_idx, timechannel],mask)).sum()
                for timechannel in range(reso_target.get_axis_len(tcha_name))
                ]
            
            #process the errors
            count_error = np.sqrt([float(count) for count in counts])

            #Generate the fit description
            position = [
                selected_ref[0],
                echo,
                foil
            ]

            fit_des = 'At a position'

            #fit the data
            success = self['fit_cov'](
                results,
                data        = counts, 
                data_error  = count_error, 
                Qmin        = 0.,
                time_chan   = reso_target.get_axis_len(tcha_name),
                position    = position,
                fit_des     = fit_des)

            if not success and results.get_last_result('Fit data covariance').log.return_last_log('error') == 'cov_failed':

                print ('covariance failed in echo %d on foil %d' %(echo, foil))

                counts = counts[1:]
                count_error = np.sqrt([float(count) for count in counts])

                success = self['fit_cov'](
                    results,
                    data        = counts, 
                    data_error  = count_error, 
                    Qmin        = 0.,
                    time_chan   = reso_target.get_axis_len(tcha_name),
                    position    = position,
                    fit_des     = fit_des)

                if not success and results.get_last_result('Fit data covariance').log.return_last_log('error') == 'cov_failed':

                    print ('covariance failed AGAIN (15 instead of 16 points were fitted) in echo %d on foil %d' %(echo, foil))
                    phase[echo][foil_idx, :, :] +=  -1*mask

                else:

                    phase[echo][foil_idx, :, :] += ((
                        results.get_last_result('Fit data covariance')['phase'] 
                        + (np.pi if results.get_last_result('Fit data covariance')['ampl'] < 0 else 0
                        )) % (2. * np.pi))*mask

            else:

                phase[echo][foil_idx, :, :] += ((
                    results.get_last_result('Fit data covariance')['phase'] 
                    + (np.pi if results.get_last_result('Fit data covariance')['ampl'] < 0 else 0
                    ))% (2. * np.pi))*mask

        ############################################
        #send out the result to the handler
        local_results['Phase']        = phase
        local_results['Reference']    = selected_ref

        #write the dictionary entries
        local_results.add_log('info', 'Fit of the phase was a success')
        local_results.set_complete()

        #tell fit handler what happened
        self.log.add_log(
            'Info', 
            'Fit of the phase was a success')

    def fit_data_cov(self,results, data, data_error, Qmin = 0, time_chan = 16,  position = [], fit_des = '', ):
        '''
        ##############################################
        Fits sine curves into n_point echoes.
        ———————
        Input: 
        - data is a list of data arrays (~128x128)
        - data_error is an array of errors associated
        - Qmin is the goodness of fit minimal value
        ———————
        Output: 
        - will store the fit result into the associated
        class as a dictionary:
            'ampl'
            'phase'
            'mean'
            'error'
            'pol'
            'fit_error'
            'chi_2'
            'pol_error'
            'mean_error'
            'ampl_error'
        ———————
        status: active
        ##############################################
        '''
        ##############################################
        #Initialize the output dictionary with all def.
        local_results = results.generate_result( name = 'Fit data covariance')

        #the description
        local_results.add_log('info', fit_des)

        ##############################################
        #Set basis variables
        len_data    = len(data)
        time        = np.arange(len_data, dtype=float)
        freq        = (2.*np.pi)/time_chan
     
        ##############################################
        #there is no data so no fit...
        if np.sum(data) == 0.:
            
            #write the dictionary entries
            local_results.add_log('warning', 'Fit failed: No counts present.')
            local_results.set_complete()

            #tell fit handler what happened
            self.log.add_log(
                'error', 
                'Fit failed: No counts present.')

            return False

        ##############################################
        # Fit the data
        fit = self.minuit_fit_cosine(data, time, freq, data_error)

        ##############################################
        # minuit failed
        if fit == None:

            #write the dictionary entries
            local_results.add_log('error', 'minuit failed')
            local_results.set_complete()

            #tell fit handler what happened
            self.log.add_log(
                'error', 
                'Fit failed: Minuit failed to compute.')

            return False

        ##############################################
        # covariance innacutrate
        if not fit.matrix_accurate():
            
            #write the dictionary entries
            local_results.add_log('error', 'cov_failed')
            local_results.set_complete()

            #tell fit handler what happened
            self.log.add_log(
                'error', 
                'Fit failed: Covariance not valid.')

            return False

        ##############################################
        # evaluate goodness
        params  = fit.values
        chi2    = fit.fval

        # Calculate the fit goodness
        Q = self.fit_goodness(chi2, len(data))

        # fit not trusted
        if not Q >= Qmin:

            #write the dictionary entries
            local_results.add_log('info', 'Qmin_bigger_Q')
            local_results.set_complete()

            #tell fit handler what happened
            self.log.add_log(
                'error', 
                'Fit not trusted: Q = {:.2f} < {:.2f} = Qmin).'.
                format(Q, Qmin))

            return False

        ##############################################
        # Everything in order proceed
        cov     = fit.np_matrix()
        Cov     = np.array(cov).reshape([3,3])
        ampl    = params['ampl']
        amplerr = np.sqrt(Cov[2][2])
        offset  = params['offset']

        offset_error   = np.sqrt(Cov[1][1])
        phase_error    = np.sqrt(Cov[0][0])
       
        #Error of Polarisation using covariance matrix
        #order of Covariance matrix Cov: Cov[0][0]: phase, Cov[1][1]: offset, Cov[2][2]: amplitude
        errCov = np.sqrt(Cov[2][2]/(offset)**2
                        + Cov[1][1]*(ampl/((offset)**2))**2)

        #Error of Sine-Fits using covariance matrix
        err_1 = (
            Cov[0][0] * (
                params['ampl'] 
                * np.sin(freq*np.arange(len_data)+params['phase'])
                )**2
            )

        err_2 = (
            Cov[1][1] * (
                params['ampl']*np.sin(freq*np.arange(len_data)
                + params['phase'])+1
                )**2 
            )

        err_3 = (
            Cov[2][2] * (
                np.sin(freq*np.arange(len_data)+params['phase'])
                )**2
            )
                
        fit_error_Cov = (np.sqrt(err_1 + err_2 + err_3))

        ##############################################
        # populate result dictionary
        local_results['ampl']         = ampl
        local_results['ampl_error']   = amplerr
        local_results['phase']        = params['phase']
        local_results['phase_error']  = phase_error
        local_results['mean']         = params['offset']
        local_results['mean_error']   = offset_error
        local_results['pol']          = abs(ampl/(params['offset']))
        local_results['pol_error']    = {'Cov': errCov}
        local_results['sine_error']   = {'Cov': fit_error_Cov}
        local_results['chi_2']        = chi2/10.**5

        #write the dictionary entries
        local_results.add_log('info', 'success')
        local_results.set_complete()

        #tell fit handler what happened
        self.log.add_log(
            'info', 
            'Fit success')

        return True

    def fit_goodness(self,chi2, N_dof):
        '''
        ##############################################
        Calculates the goodness of a leastsquare fit 
        according to 'Everything you want to know 
        about Data Analysis and Fitting'.
        ———————
        Input: 
        - chi
        - N_dof
        ———————
        Output: 
        - Q
        ———————
        status: active
        ##############################################
        '''
        Gamma = sp.gamma(N_dof/2.)
        func = lambda y: y**(N_dof/2. - 1.) * math.exp(-y)
        integral,error = scipy.integrate.quad(func, chi2/2., np.inf)
        Q = 1.0 / Gamma * integral

        return Q

    def minuit_fit_cosine(self,counts, time, freq, count_error):
        '''
        ##############################################
        Creates the minuit fit function and runs 
        leastsquarefit.
        ———————
        Input: 
        - counts (array of)
        - time (echo time ?)
        - freq (float)
        - count_error (array of float)
        ———————
        Output: 
        - Q
        ———————
        status: active
        ##############################################
        '''
        ##############################################
        #pack the variables and set the starts
        self.minuit_parameters = [counts, time,count_error, freq]

        phase0 = np.max(counts)-np.min(counts)
        offset0 = 0
        ampl0 = np.mean(counts)

        ##############################################
        #create fit object and fit
        fit = iminuit.Minuit(self.fit_cosine,
                            phase   = phase0,
                            offset  = offset0,
                            ampl    = ampl0,
                            pedantic=False,
                            print_level=0)
        fit.migrad()

        return fit 

    def minuit_fit_exp(self,contrast, SEtime, contrasterr):
        '''
        ##############################################
        Creates the minuit fit function and runs 
        leastsquarefit.
        ———————
        Input: 
        - counts (array of)
        - time (echo time ?)
        - count_error (array of float)
        ———————
        Output: 
        - Q
        ———————
        status: active
        ##############################################
        '''
        ##############################################
        #pack the variables and set the starts
        self.minuit_parameters = [contrast,SEtime,contrasterr]

        Gamma0 = 10.

        ##############################################
        #create fit object and fit
        fit = iminuit.Minuit(
            self.fit_exp,

            Gamma = Gamma0,

            pedantic=False,
            print_level=0)

        fit.migrad()

        ##############################################
        #process output
        params  = fit.values
        chi2    = fit.fval
        cov     = fit.np_matrix()
        Cov     = np.array(cov).reshape([1,1])
        Gamma   = fit.values['Gamma']
        Gammaerr = np.sqrt(Cov[0][0])

        x = np.linspace(0.01,3,1000)

        return {'Gamma': Gamma,
                'Gamma_error': Gammaerr,
                #'Curve': minuitfunction(Gamma)
                'Curve':np.exp(-Gamma*1e-6*co.e*x*1e-9/co.hbar)
            }


    def fit_exp(self,Gamma):
        '''
        ##############################################
        Gamma exponential fit minimizer function
        ———————
        Input: 
        - counts (array of)
        - time (echo time ?)
        - count_error (array of float)
        ———————
        Output: 
        - Q
        ———————
        status: active
        ##############################################
        '''
        ##############################################
        #unpack the variables
        contrast    = self.minuit_parameters[0]
        SEtime      = self.minuit_parameters[1]
        contrasterr = self.minuit_parameters[2]

        ##############################################
        #proceed to fit
        np.seterr(all='warn')
        with warnings.catch_warnings():
            try:
 
                return sum(

                        ((math.exp((-Gamma*1e-6*t*1e-9)/(6.582*1e-16))-c) ** 2 / e ** 2 
                        for c,t,e in zip(contrast,SEtime,contrasterr))
                    
                )
                    
                
            except:
                return np.nan

    def fit_cosine(self,phase,offset,ampl):
        '''
        ##############################################
        Creates the minuit fit function and runs 
        leastsquarefit.
        ———————
        Input: 
        - counts (array of)
        - time (echo time ?)
        - freq (float)
        - count_error (array of float)
        ———————
        Output: 
        - Q
        ———————
        status: active
        ##############################################
        '''

        ##############################################
        #unpack the variables
        counts      = self.minuit_parameters[0]
        time        = self.minuit_parameters[1]
        count_error = self.minuit_parameters[2]
        freq        = self.minuit_parameters[3]

        ##############################################
        #proceed to fit
        np.seterr(all='warn')
        with warnings.catch_warnings():
            try:
                return sum((((ampl*np.cos(freq*t+phase)+offset-c)**2)/e**2 for c,t,e in zip(counts,time,count_error)))
            except:
                return np.nan