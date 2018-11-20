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

import iminuit
import numpy as np
import copy

from scipy import constants as co
from scipy import optimize as op
from scipy import stats as st


from .fit_mieze_minuit  import Fit_MIEZE_Minuit

class Fit_MIEZE_Phase(Fit_MIEZE_Minuit): 

    def __init__(self):
        Fit_MIEZE_Minuit.__init__(self)


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
        wavelength  = metadata_object['wavelength']*1e-10
        freq_0      = metadata_object['freq_0']
        freq_1      = metadata_object['freq_1']
        lsd         = metadata_object['lsd']*1.e9
        wavelength_error    = target.metadata_class['Wavelength error'] 
        lsd_error           = target.metadata_class['Distance error']

        ############################################
        #process tau and the error of tau
        tau, tau_error = self.mieze_tau_calc(
            wavelength,
            freq_0,
            freq_1,
            lsd,
            wavelength_error = wavelength_error,
            lsd_error = lsd_error)

        ############################################
        #send it out to the metadata class
        metadata_object.add_metadata('tau', value = tau)
        metadata_object.add_metadata('tau_error', value = tau_error)

    def mieze_tau_calc(self, wavelength, freq_0, freq_1, lsd, wavelength_error = 0 ,lsd_error = 0):
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
        delta_freq = freq_1 - freq_0
        para = ( 2. * co.m_n ** 2 ) / (co.h ** 2) 

        tau         = para * wavelength ** 3 * delta_freq * lsd 
        tau_error   = para * ( 
            ( 
                wavelength_error 
                * wavelength * 3 
                * wavelength ** 2 
                * delta_freq * lsd )

            + ( 
                lsd_error 
                * lsd 
                *  wavelength ** 3 
                * delta_freq )
            )

        return tau, tau_error

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
        para_name = self.para_dict['para_name']
        echo_name = self.para_dict['echo_name']
        meas_name = self.para_dict['meas_name']
        foil_name = self.para_dict['foil_name']
        tcha_name = self.para_dict['tcha_name']

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
        selected_ref    = self.para_dict['Reference']
        reso_target     = target.get_slice(selected_ref)
        premask         = mask.mask

        ############################################
        #initialise variables
        phase = {}

        ############################################
        #set up the parameter names
        para_name = self.para_dict['para_name']
        echo_name = self.para_dict['echo_name']
        meas_name = self.para_dict['meas_name']
        foil_name = self.para_dict['foil_name']
        tcha_name = self.para_dict['tcha_name']

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
            print('######COUNTS#####', np.sum(counts))
            
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
            success = self.fit_data_cov(
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

                success = self.fit_data_cov(
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