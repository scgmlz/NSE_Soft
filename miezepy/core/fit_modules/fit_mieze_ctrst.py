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
#   Alexander Schober <alexander.schober@mac.com>
#
# *****************************************************************************

import numpy as np
import warnings
warnings.filterwarnings("ignore")

from .fit_mieze_minuit  import Fit_MIEZE_Minuit

class Fit_MIEZE_Ctrst(Fit_MIEZE_Minuit): 

    def __init__(self):
        
        Fit_MIEZE_Minuit.__init__(self)

    def calcCtrstFit(self, select, foils_in_echo, shift, target, mask, results, foil = None):

        '''
        This function will process the fit of the
        given input.
        Input: 
        - select (list)
        - MIEZE metadata object
        - mask object
        '''
        premask         = mask.mask
        local_results   = {}

        #set up the parameter names
        para_name = self.para_dict['para_name']
        echo_name = self.para_dict['echo_name']
        meas_name = self.para_dict['meas_name']

        ############################################
        #loop over elements
        loop = [
            (e1, e2) 
            for e1 in select 
            for e2 in target.get_axis(meas_name)]

        for key, meas in loop:
            #grab the data slice
            new_target = target.get_slice([key, meas])

            #if measurement it 0 initiate the dictionary
            if meas == 0:
                local_results[key]    = {}

            if not new_target == False:
                #print out the processing step
                print(
                    'Processing the contrast fit for: '
                    +str(key)
                    +' measurement '
                    +str(meas))

                local_results[key][meas]    = {}

                for echo in new_target.get_axis(echo_name):
                    combined_data = self.combineData(
                        key, meas, echo, 
                        shift, target, new_target, 
                        premask, foil, foils_in_echo )
                    print([key][meas][echo])
                    local_results[key][meas][echo] = self.fitSinus(
                        results, combined_data, new_target, echo)

        return local_results

    def fitSinus(self, results, combined_data, new_target, echo):
        '''
        ##############################################
        
        ———————
        Input: 
        - MIEZE metadata object
        - mask object
        ———————
        Output: -
        ##############################################
        '''

        tcha_name = self.para_dict['tcha_name']
        echo_name = self.para_dict['echo_name']

        ############################################
        #fit the data
        
        self.fit_data_cov(
            results,
            combined_data, 
            np.sqrt(combined_data), 
            Qmin = 0.,
            time_chan = new_target.get_axis_len(tcha_name))

        result      = results.get_last_result('Fit data covariance')
        echo_idx_1  = new_target.get_axis_idx(echo_name, echo)
        monitor     = new_target.get_metadata([echo_idx_1,0,0])[0]['Monitor']
        print([
            result['ampl']/monitor,
            result['ampl_error']/monitor,
            result['mean']/monitor,
            result['mean_error']/monitor])
        ############################################
        #process the result
        return [
            result['ampl']/monitor,
            result['ampl_error']/monitor,
            result['mean']/monitor,
            result['mean_error']/monitor]

    def combineData(self,key, meas, echo, shift, target, new_target, premask, foil, foils_in_echo):
        '''
        '''
        #set up the parameter names
        echo_name = self.para_dict['echo_name']
        foil_name = self.para_dict['foil_name']
        tcha_name = self.para_dict['tcha_name']

        #initialise data
        combined_data = np.zeros(new_target.get_axis_len(tcha_name))

        #check if we want only a specific foil
        if not foil == None:
            foil_elements = [foil]
        else:
            foil_elements = new_target.get_axis(foil_name)

        #reduce the foils
        for foil in foil_elements:
            #grab idx for the values.
            echo_idx_0  = target.get_axis_idx(echo_name, echo)
            foil_idx    = new_target.get_axis_idx(foil_name, foil)

            #logical check
            if foils_in_echo[echo_idx_0][foil_idx] == 1:
                data_array = []
                for tcha_idx in range(new_target.get_axis_len(tcha_name)):
                    data_array.append((np.multiply(shift[key][meas][echo][foil_idx,tcha_idx],premask)).sum())
                data = np.array(data_array)
                combined_data += data
                
        return combined_data

    def calcCtrstRef(self,target, mask, results):
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
        local_results = results.generate_result(
            name = 'Reference contrast calculation')

        ############################################
        #extract the relevant parameters 
        shift           = results.get_last_result(
            'Shift calculation', 'Shift')
        foils_in_echo   = self.test_parameter(
            'foils_in_echo', target, mask, results)
        reference       = self.test_parameter(
            'Reference', target, mask, results)

        ############################################
        #fit and calculate the contrast
        print(
            'Processing the reference contrast calculation for: '
            +str(reference))

        reference   = reference[0] 
        ref_result  = self.calcCtrstFit(
            [reference], 
            foils_in_echo, 
            shift, 
            target, 
            mask,
            results)
            
        contrast_result = self.ctrstLogicRef(
            ref_result[reference][0],
            local_results)
        ############################################
        #Process the result
        local_results['Reference']            = reference
        local_results['Contrast_ref']         = contrast_result[0]
        local_results['Contrast_ref_error']   = contrast_result[1]

        #write the dictionary entries
        local_results.add_log(
            'info', 
            'Computation of the contrast was was a success')

        #close up the result
        local_results.set_complete()

    def ctrstLogicRef(self, target, local_results):
        '''
        ##############################################
        This function was built to ease readability
        and to provide the contrast calculation
        routine.
        ———————
        Input: 
        - target (fit results) from calcCtrstFit
        ———————
        Output: -
        ##############################################
        '''
        ############################################
        #initilise the contrast result
        contrast_ref        = {}
        contrast_ref_error  = {}

        ############################################
        #Process the result
        for echo in target.keys():

            #do a check of the value and throw an error if 0
            if target[echo][0] == 0 or target[echo][2] == 0:
                if target[echo][0] == 0:
                    local_results.add_log(
                        'warning', 
                        'The amplitude from the reference fit is 0. Please investigate...')
                    local_results.add_log(
                        'error', 
                        'Setting the value to 1')
                elif target[echo][2] == 0:
                    local_results.add_log(
                        'error', 
                        'The mean from the reference fit is 0. Please investigate...')
                    local_results.add_log(
                        'error', 
                        'Setting the value to 1')

                target[echo][0] = 1.
                target[echo][1] = 1.

            ############################################
            #set output
            contrast_ref[echo] = self.ctrstEq(
                target[echo],    
                [0,0,0,0])

            contrast_ref_error[echo] = self.ctrstErrEq(
                target[echo], 
                [0,0,0,0])

        return [contrast_ref, contrast_ref_error]

    def calcCtrstMain(self,target, mask, results, select = False, foil = None):
        '''
        ##############################################
        This is the main contrast calculation routine.
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
        foils_in_echo   = self.test_parameter('foils_in_echo', target, mask, results)
        para_name       = self.test_parameter('para_name', target, mask, results)

        if select == False:
            select = self.test_parameter('Select', target, mask, results)
        else:
            pass

        if any([element == False for element in [select, foils_in_echo, BG]]):

            return False

        ############################################
        #contrast calculation
        contrast_results = self.calcCtrstFit(
            select, foils_in_echo, shift, 
            target, mask, results, foil)

        ############################################
        #process Background
        if not BG == None:

            print(
                'Processing the Background contrast calculation for: '
                +str(BG))

            BG_result = self.calcCtrstFit(
                [BG],foils_in_echo, shift, 
                target, mask,results)

        ############################################
        #now process the data on the axis
        axis, positions = self.multiAxis(select, target)

        ############################################
        #initilise the contrast result
        contrast            = {}
        contrast_error      = {}

        for key in axis.keys():
            
            if 'BG_result' in locals():
                BG_target = BG_result[BG][0]

            else: 
                BG_target = None

            #result 
            result = self.ctrstLogicMain(
                positions[key], 
                contrast_results[key], 
                BG_target, 
                local_results)

            #if measurement it 0 initate the dicitoanry
            contrast[key]       = result[0]
            contrast_error[key] = result[1]

            #print it out
            print(
                'Processing the contrast calculation for: '
                +str(key))

        ##############################################
        #finalize result and send it out
        local_results['Axis']                 = axis
        local_results['Contrast']             = contrast
        local_results['Contrast_error']       = contrast_error
        local_results['Background']           = BG
        local_results['Foil']                 = foil      

    
        #write the dictionary entries
        local_results.add_log('info', 'Computation of the contrast was was a success')
        local_results.set_complete()

        #tell fit handler what happened
        self.log.add_log(
            'Info', 
            'Computation of the contrast was was a success')

    def ctrstLogicMain(self, positions, contrast_results, BG_result, local_results):
        '''
        ##############################################
        This function was built to ease readability
        and to provide the contrast calculation
        routine.
        ———————
        Input: 
        - target (fit results) from calcCtrstFit
        ———————
        Output: -
        ##############################################
        '''
        ############################################
        #initilise the contrast result
        contrast        = []
        contrast_error  = []

        for meas, echo in positions:
            #contrast target
            target = contrast_results[meas][echo]

            if not BG_result == None:
                BG_target = BG_result[echo]
            else:
                BG_target = [0,0,0,0]

            ctrst       = self.ctrstEq(target, BG_target)
            ctrst_err   = self.ctrstErrEq(target, BG_target)

            contrast.append(float(ctrst))
            contrast_error.append(float(ctrst_err))

        return [contrast, contrast_error]

    def multiAxis(self,select, target):
        '''
        ##############################################
        In this routine we try to construct the axis
        of points. This is important when you bind
        together different measurements. 
        ———————
        Input: 
        - MIEZE metadata object
        - mask object
        ———————
        Output: -
        ##############################################
        '''
        #grab meta
        echo_name = self.para_dict['echo_name']
        meas_name = self.para_dict['meas_name']
        axis      = {}
        positions = {}

        #set the loop
        loop = [(e1, e2) for e1 in select for e2 in target.get_axis(meas_name)]

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
                positions[key]  = []
                #set the current keys
                c_key   = key

            #grab axis information
            if not new_target == False:
                for i in range(new_target.get_axis_len(echo_name)):
                    axis[key].append(new_target.get_axis_val(echo_name, i))
                    positions[key].append((meas, new_target.get_axis_val(echo_name, i)))

        return axis, positions

    def ctrstEq(self,target, BG_target):
        '''
        ##############################################
        Contrast equation separating the case of 
        background or not in a smart way
        ———————
        Input: 
        - MIEZE metadata object
        - mask object
        ———————
        Output: -
        ##############################################
        '''
        if target[2]-BG_target[2] == 0:
            return 0
        else:
            return ((abs(target[0])-abs(BG_target[0]))/(target[2]-BG_target[2]))

    def ctrstErrEq(self,target, BG_target):
        '''
        ##############################################
        Contrast error equation separating the case of 
        background or not in a smart way
        ———————
        Input: 
        - MIEZE metadata object
        - mask object
        ———————
        Output: -
        ##############################################
        '''
        if target[2]-BG_target[2] == 0:
            return 0
        else:
            return np.sqrt(
            (target[1] / (target[2] - BG_target[2])) ** 2
            + (BG_target[1] / (target[2]-BG_target[2])) ** 2
            + ( (abs(target[0]) - abs(BG_target[0]))
                /(target[2]-BG_target[2]) ** 2 * target[3]) ** 2
            + ( (abs(target[0])-abs(BG_target[0])) 
                /(target[2]-BG_target[2]) ** 2 * BG_target[3]) ** 2)


    def ctrstFit(self,target, mask, results):
        '''
        ##############################################
        In this function we will process the fit of 
        the data to allow fitting later on

        The package will be in dictionaries for each
        axis value1
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
        contrast            = results.get_last_result(
            'Contrast calculation', 'Contrast')
        contrast_error      = results.get_last_result(
            'Contrast calculation', 'Contrast_error')
        contrast_ref        = results.get_last_result(
            'Reference contrast calculation','Contrast_ref')
        contrast_ref_error  = results.get_last_result(
            'Reference contrast calculation','Contrast_ref_error')
        BG                  = results.get_last_result(
            'Contrast calculation', 'Background')
        axis                = results.get_last_result(
            'Contrast calculation', 'Axis')

        select              = self.test_parameter('Select', target, mask, results)
        reference           = self.test_parameter('Reference', target, mask, results)
        axis_unit           = target.axes.units[0]
        x_unit              = target.axes.units[0]

        ############################################
        #initialize the ouptup
        Output                  = {}
        Output['Gamma']         = {}
        Output['Gamma_error']   = {}
        Output['Curve']         = {}
        Output['Parameters']    = {}
        Output['Curve Axis']    = {}

        ############################################
        #process thecomputation
        for key in contrast.keys():

            #load the data
            x           = np.asarray(axis[key])
            data        = np.asarray(contrast[key])
            data_error  = np.asarray(contrast_error[key])
            ref_data    = np.asarray([contrast_ref[echo] for echo in x])
            ref_error   = np.asarray([contrast_ref_error[echo] for echo in x])
            
            if not reference == None:
                y       = np.abs(data / ref_data)
                y_error = y * np.sqrt(
                    (data_error / data) ** 2
                    + (ref_error / ref_data) ** 2)

            else:
                y = np.abs(data)
                y_error = data_error

            #fit the data
            fit = self.minuit_fit_exp(y, x, y_error)

            #prepare the result
            Output['Parameters'][key]  = {
                'x' : x,
                'x_unit' : x_unit,
                'y' : y,
                'y_error' : y_error}

            Output['Gamma'][key]       = fit['Gamma']
            Output['Gamma_error'][key] = fit['Gamma_error']
            Output['Curve'][key]       = fit['Curve']
            Output['Curve Axis'][key]  = fit['Curve Axis']

        ############################################
        #set the other informations
        local_results['Gamma']        = [Output['Gamma'][T] for T in select]
        local_results['Gamma_error']  = [Output['Gamma_error'][T] for T in select]
        local_results['Curve']        = Output['Curve']   
        local_results['Curve Axis']   = Output['Curve Axis']   
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