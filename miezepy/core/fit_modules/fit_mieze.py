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

import copy
#############################
# import general components
import numpy as np
import warnings

from .fit_general import Fit_Handler
from .fit_mieze_contrast import ContrastProcessing
from .fit_mieze_phase import PhaseProcessing


class Fit_MIEZE(Fit_Handler, PhaseProcessing, ContrastProcessing):

    def __init__(self):
        '''
        This is the initializer of the MIEZE fit class
        within. It will also initialize the superclass
        containing the generalized methods.
        '''
        Fit_Handler.__init__(self)
        PhaseProcessing.__init__(self)
        ContrastProcessing.__init__(self)
        self.set_fit_parameters()

    def set_fit_parameters(self):
        '''
        Set the default parameters in the fitting
        routine.
        '''
        ############################################
        # pack them into the dictionary
        self.para_dict = {}

        self.para_dict['foils_in_echo'] = []
        self.para_dict['time_channels'] = []
        self.para_dict['Background'] = None
        self.para_dict['Reference'] = None
        self.para_dict['Select'] = []
        self.para_dict['foil_correct'] = []
        self.para_dict['processors'] = 1
        self.para_dict['exposure'] = False
        self.para_dict['sum_foils'] = True

        ############################################
        # set deafult pointers
        self.para_dict['para_name'] = 'Parameter'
        self.para_dict['echo_name'] = 'Echo Time'
        self.para_dict['meas_name'] = 'Measurement'
        self.para_dict['foil_name'] = 'Foil'
        self.para_dict['tcha_name'] = 'Time Channel'

    def test_parameter(self, value, target, mask, results):
        '''
        Test function on the input parameters. This is
        called by the parameter value which gives the
        variable to test.
        Input: 
        - value (str)
        - MIEZE metadata object
        - mask object
        Output: 
        - will return either false or the selected
        value. 
        '''
        ############################################
        # perform the check on test
        if value == 'Select':
            select = self.para_dict['Select']

            if not isinstance(select, list):
                raise Exception('Select needs to be a list. Error...')

            else:
                if select[0] == 'all':
                    select = list(target.get_axis(self.para_dict['para_name']))
                    return select
                else:
                    try:
                        [target.get_axis(self.para_dict['para_name']).index(selected) for selected in select]
                    except:
                        raise Exception('The values do not match the axes. Error...')

                    return select

        ############################################
        # perform the check on test
        elif value == 'foils_in_echo':
            foils_in_echo = self.para_dict['foils_in_echo']

            # check the dimension of this list
            if not len(foils_in_echo) == target.get_axis_len(self.para_dict['echo_name']):
                raise Exception('Not enough foils_in_echo initialized. Error...')

            elif not all(
                    [len(element) == target.get_axis_len(self.para_dict['foil_name']) for element in foils_in_echo]):
                raise Exception('Not enough foils_in_echo initialized. Error...')

            elif foils_in_echo == []:
                raise Exception('Sine foils not set by the user. Error...')

            else:

                return foils_in_echo

        ############################################
        # perform a test on BG
        elif value == 'Background':

            BG = self.para_dict['Background']

            # check the dimension of this list
            if not BG == None and not BG in target.get_axis(self.para_dict['para_name']):
                raise Exception('The background is not in the loaded data. Error...')

            else:
                return BG

        ############################################
        # perform a test on the reference
        elif value == 'Reference':
            reference = self.para_dict['Reference']

            if not reference == None and not reference[0] in target.get_axis(self.para_dict['para_name']):
                raise Exception('This reference does not exist. Error...')

            else:
                return reference

        ############################################
        # perform a test on the reference
        elif len(value.split('name')) > 1:
            if self.para_dict[value] in target.axes.names:
                return self.para_dict[value]
            else:
                raise Exception('The axis name does not exist in the provided data. Error...')

        else:
            raise Exception('Value to test not found. Error...')
