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

class Process_Manager:

    def __init__(self):
        '''
        ##############################################
        This is the initializer of all the 
        ———————
        Input: -
        ———————
        Output: -
        ##############################################
        '''

        pass

    def ALL_extract_from_metadata(self, target, mask, fit, axis, key):
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
        idx = target.axes.names.index(axis)
        target.axes.grab_meta(idx, key)
        target.axes.collapse_axis(idx)

    def MIEZE_calculate_echo(self, target, mask, fit, results):
        '''
        ##############################################
        In this function we will process the eco time
        on the provided datastructure. 
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
        #process the echo time
        for metadata_object in target.metadata_objects:

            fit['mieze_tau'](metadata_object, target)

        self.ALL_extract_from_metadata(
            target, 
            mask, 
            fit, 
            'Echo', 
            'tau')

    def MIEZE_remove_foils(self, target, mask, fit, results):
        '''
        ##############################################
        Removes the foils from the dataset and returns
        the deepcopy new dataset
        ———————
        Input: 
        - MIEZE data object
        - Mask object
        - the key links to the value that will be reference
        ———————
        Output: -
        ##############################################
        '''
        #remove the asked foils
        selected_foils  = target.metadata_class['Selected foils']
        new_target      = target.remove_from_axis(3,selected_foils)

        return new_target

    def MIEZE_calculate_shift(self, target, mask, fit, results):
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
        mask.process_mask(target)
        
        #extract the phase
        fit['extract_phase'](target, mask, results)

        #process the shift
        fit['calc_shift'](target, mask, results)

    def MIEZE_calculate_ref_contrast(self, target, mask, fit, results):
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
        mask.process_mask(target)

        #calculate the contrast
        fit['calc_ref_contrast'](target, mask, results)


    def MIEZE_calculate_contrast(self, target, mask, fit, results):
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
        mask.process_mask(target)

        #calculate the contrast
        fit['calc_contrast'](target, mask, results)

        #fit the contrast data
        fit['fit_contrast'](target, mask, results)

    def SANS_intensity(self, target, mask, fit, results):
        '''
        ##############################################
        process the intensity vs. parameter calculation
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
        mask.process_mask(target)

        #process the intensity calculations
        fit['intensity'](target, mask, results)
