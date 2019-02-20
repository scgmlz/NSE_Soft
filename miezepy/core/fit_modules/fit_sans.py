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

from .fit_general import Fit_Handler

class Fit_SANS(Fit_Handler):

    def __init__(self):
        '''
        This is the initializer of the SANS fit class
        within. It will also initialize the superclass
        containing the generalized methods.
        '''
        Fit_Handler.__init__(self)

        self.ptr_dict = {}
        self.ptr_dict['intensity']      = self.intensity_vs_parameter
        self.set_defaults()
        self.set_fit_parameters()

    def set_defaults(self):
        '''
        This function will build the default 
        dictionary of function dict that will link
        the functions to the selected method
        '''

        self.fun_dict = {}
        self.fun_dict['intensity']     = self.ptr_dict['intensity']

    def set_fit_parameters(self):
        '''
        '''
        self.para_dict = {}
        self.para_dict['BG substraction']   = None

    def intensity_vs_parameter(self, target, mask, results):
        '''
        This method aims atprocessing the SANS
        intensity against the a given parameter
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

