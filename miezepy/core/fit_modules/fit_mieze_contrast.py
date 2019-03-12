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

import numpy as np
import warnings

from .library_fit import contrastEquation
from .library_fit import contrastErrorEquation
from .library_fit import fitDataSinus
from .library_fit import loopLibrary
from .library_fit import reorganizeResult
from .library_fit import contrastLogicRef
from .library_fit import contrastLogicMain
from .library_fit import multiAxis

from ..module_result    import ResultStructure
from .fit_worker        import WorkerPool
from .library_iminuit    import ExpMinuit

class ContrastProcessing: 

    def calcContrastFit(self, select, data_input, target, mask, foil = None):
        '''
        This function proceeds to the contrast calculation 
        given a certain selected array to process

        Parameters
        ----------
        select : list of float
            The elements to process in the selected dataset

        data : DataStructure
            The processed and shifted data

        target : DataStructure
            The current dataset with all metadata
        
        mask : mask structure
            The mask structure 

        foil : int
            The foil to process in case not all should be 
            evaluated

        Returns
        ------- 
        temp_reorganized : dict[dict[list[float]]]
            result of amplitudes and phases
        '''
        #extract the relevant parameters
        mask_item       = mask.mask
        data_map        = target.map

        para_name       = self.para_dict['para_name']
        meas_name       = self.para_dict['meas_name']
        echo_name       = self.para_dict['echo_name']
        foil_name       = self.para_dict['foil_name']
        tcha_name       = self.para_dict['tcha_name']
        foils_in_echo   = self.para_dict['foils_in_echo']

        para_axis   = target.get_axis(para_name) 
        meas_axis   = target.get_axis(meas_name) 
        echo_axis   = target.get_axis(echo_name) 
        foil_axis   = target.get_axis(foil_name) 
        cha_axis    = target.get_axis(tcha_name)

        #loop over elements
        loop = [
            (e1, e2, e3) 
            for e1 in select 
            for e2 in target.get_axis(meas_name)
            for e3 in target.get_axis(echo_name)]

        #set up the index pointers
        index_array = []
        for para, meas, echo in loop:
            index_array.append([para,meas,echo])

        #do the lifting
        idx = 0
        worker_pool = WorkerPool(10)
        for para, meas, echo in loop:

            if  not data_map[
                para_axis.index(para), 
                meas_axis.index(meas), 
                echo_axis.index(echo), 0, 0] == -1:

                #get the idx
                meta_idx = data_map[
                    para_axis.index(para), 
                    meas_axis.index(meas), 
                    echo_axis.index(echo), 0, 0]

                #get the monitor value
                monitor = target.metadata_objects[
                    target.metadata_addresses.index(
                        target.data_objects[meta_idx].meta_address[0])]['Monitor']

                worker_pool.addWorker([
                    self.contrastProcedure,
                    idx, data_input[para][meas][echo], target, mask_item,
                    foils_in_echo[echo_axis.index(echo)],foil, 
                    monitor])

            idx += 1

        temp = worker_pool.startPool()
        temp_reorganized = reorganizeResult(temp, index_array, loop)

        return temp_reorganized

    def contrastProcedure(self, idx, data_input, target, mask_item, foils_in_echo, foil, monitor, result_dict):
        '''
        This function proceeds to the contrast calculation 
        given a certain selected array to process

        Parameters
        ----------
        idx : int
            Pointer to the address in the dictionary

        data_input : DataStructure
            The processed and shifted data

        target : DataStructure
            The current dataset with all metadata
        
        mask_item :np.ndarray
            The mask 

        foils_in_echo: int array
            1 if a foil is considered or if ignored

        foil : int
            The foil to process in case not all should be 
            evaluated

        monitor : int
            The monitor value to be used on this measurement

        result_dict : shared dict
            This is the variable used to save the result
        '''
        combined_data       = self.combineData(data_input, target, mask_item, foils_in_echo, foil)
        contrast_result     = self.fitContrastSinus(combined_data, target, monitor)
        result_dict[idx]    = contrast_result

    def combineData(self, data_input, target, mask_item, foils_in_echo, foil):
        '''
        This function proceeds to the contrast calculation 
        given a certain selected array to process

        Parameters
        ----------
        data_input : DataStructure
            The processed and shifted data

        target : DataStructure
            The current dataset with all metadata
        
        mask_item :np.ndarray
            The mask 

        foils_in_echo: int array
            1 if a foil is considered or if ignored

        foil : int
            The foil to process in case not all should be 
            evaluated

        Returns
        ------- 
        np.nd array 1D of the summed data on a mask
        '''
        #set up the parameter names
        foil_name = self.para_dict['foil_name']
        tcha_name = self.para_dict['tcha_name']

        #initialise data
        combined_data = np.zeros(target.get_axis_len(tcha_name))

        #check if we want only a specific foil
        if not foil == None:
            foil_elements = [foil]
        else:
            foil_elements = target.get_axis(foil_name)

        #reduce the foils
        for foil_idx, foil in enumerate(foil_elements):
            #logical check
            if foils_in_echo[foil_idx] == 1:
                data_array = []
                for tcha_idx in range(target.get_axis_len(tcha_name)):
                    data_array.append((np.multiply(data_input[foil_idx,tcha_idx],mask_item)).sum())
                data = np.array(data_array)
                combined_data += data
                
        return combined_data

    def fitContrastSinus(self, data_input, target, monitor):
        '''
        This function proceeds to the contrast calculation 
        given a certain selected array to process

        Parameters
        ----------
        data_input : DataStructure
            The processed and shifted data

        target : DataStructure
            The current dataset with all metadata

        monitor : int
            The monitor value to be used on this measurement
        '''
        tcha_name   = self.para_dict['tcha_name']
        echo_name   = self.para_dict['echo_name']
        results     = ResultStructure()

        #fit the data
        fitDataSinus(
            results, 
            data_input, 
            np.sqrt(data_input), 
            Q_min = 0.,
            time_chan = target.get_axis_len(tcha_name))

        result  = results.getLastResult('Fit Data Sinus')
        if result['amplitude'] == 0:
            result.log.dump_to_console()
        #process the result
        return [
            result['amplitude']/monitor,
            result['amplitude_error']/monitor,
            result['mean']/monitor,
            result['mean_error']/monitor]

    def calcContrastRef(self,target, mask, results):
        '''
        uses self.shifted to combine foils and 
        calculates contrast for chosen foils for 
        certain echos

        Parameters
        ----------
        target : DataStructure
            The current active datastructure

        mask : MaskStructure
            The current active mask structure

        results : ResultStructure
            The current active result structure
        '''
        #Initialize the output dictionary with all def.
        local_results = results.generateResult(
            name = 'Reference contrast calculation')

        #extract the relevant parameters 
        data        = results.getLastResult( 'Corrected Phase', 'Shift')
        reference   = self.test_parameter('Reference', target, mask, results)

        #fit and calculate the contrast
        print(
            'Processing the reference contrast calculation for: '
            +str(reference))

        reference   = reference[0]
        ref_result  = self.calcContrastFit([reference], data, target, mask)
        ref_result  = contrastLogicRef(ref_result[reference][0],local_results)

        #Process the result
        local_results['Reference']            = reference
        local_results['Contrast_ref']         = ref_result[0]
        local_results['Contrast_ref_error']   = ref_result[1]

        #write the dictionary entries
        local_results.addLog(
            'info', 
            'Computation of the contrast was was a success')

        #close up the result
        local_results.setComplete()

    def calcContrastMain(self,target, mask, results, select = False, foil = None):
        '''
        This is the main contrast calculation routine.

        Parameters
        ----------
        target : DataStructure
            The current active datastructure

        mask : MaskStructure
            The current active mask structure

        results : ResultStructure
            The current active result structure
        '''
        #Initialize the output dictionary with all def.
        local_results = results.generateResult( name =  'Contrast calculation')

        #extract the relevant parameters
        data        = results.getLastResult( 'Corrected Phase', 'Shift')
        BG          = self.test_parameter('Background', target, mask, results)
        para_name   = self.test_parameter('para_name', target, mask, results)

        if select == False:
            select = self.test_parameter('Select', target, mask, results)
        else:
            pass

        #process Background
        if not BG == None:
            print(
                'Processing the Background contrast calculation for: '
                +str(BG))
            BG_result = self.calcContrastFit(
                [BG], data, target, mask)
            print(BG_result)

        #contrast calculation
        contrast_results = self.calcContrastFit(
            select, data, target, mask, foil)

        #now process the data on the axis
        axis, positions = multiAxis(select, target)
        print(axis, positions)

        #initialise the contrast result
        contrast            = {}
        contrast_error      = {}

        for para in axis.keys():
            if 'BG_result' in locals():
                BG_target = BG_result[BG][0]
            else: 
                BG_target = None

            #result 
            result = contrastLogicMain(
                positions[para], 
                contrast_results[para], 
                BG_target, 
                local_results)

            #if measurement it 0 initiate the dictionary
            contrast[para]       = result[0]
            contrast_error[para] = result[1]

            #print it out
            print(
                'Processing the contrast calculation for: '
                +str(para))

        #finalize result and send it out
        local_results['Axis']                 = axis
        local_results['Contrast']             = contrast
        local_results['Contrast_error']       = contrast_error
        local_results['Background']           = BG
        local_results['Foil']                 = foil      
    
        #write the dictionary entries
        local_results.addLog('info', 'Computation of the contrast was was a success')
        local_results.setComplete()

        #tell fit handler what happened
        self.log.addLog(
            'Info', 
            'Computation of the contrast was was a success')

    def contrastFit(self,target, mask, results):
        '''
        In this function we will process the fit of 
        the data to allow fitting later on
        The package will be in dictionaries for each
        axis value1

        Parameters
        ----------
        target : DataStructure
            The current active datastructure

        mask : MaskStructure
            The current active mask structure

        results : ResultStructure
            The current active result structure
        '''
        #Initialize the output dictionary with all def.
        local_results = results.generateResult( name = 'Contrast fit')

        #get the last contrast computaiton result
        contrast            = results.getLastResult(
            'Contrast calculation', 'Contrast')
        contrast_error      = results.getLastResult(
            'Contrast calculation', 'Contrast_error')
        contrast_ref        = results.getLastResult(
            'Reference contrast calculation','Contrast_ref')
        contrast_ref_error  = results.getLastResult(
            'Reference contrast calculation','Contrast_ref_error')
        BG                  = results.getLastResult(
            'Contrast calculation', 'Background')
        axis                = results.getLastResult(
            'Contrast calculation', 'Axis')

        fitter      = ExpMinuit()
        select      = self.test_parameter('Select', target, mask, results)
        reference   = self.test_parameter('Reference', target, mask, results)
        axis_unit   = target.axes.units[0]
        x_unit      = target.axes.units[0]

        #initialize the output
        Output                  = {}
        Output['Gamma']         = {}
        Output['Gamma_error']   = {}
        Output['Curve']         = {}
        Output['Parameters']    = {}
        Output['Curve Axis']    = {}

        print(contrast)

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
            fit = fitter.fitExp(y, x, y_error)

            #prepare the result
            Output['Parameters'][key]  = {
                'x' : x,
                'x_unit' : x_unit,
                'y' : y,
                'y_raw': np.abs(data),
                'y_error' : y_error,
                'y_raw_error' : data_error}

            Output['Gamma'][key]       = fit['Gamma']
            Output['Gamma_error'][key] = fit['Gamma_error']
            Output['Curve'][key]       = fit['Curve']
            Output['Curve Axis'][key]  = fit['Curve Axis']

        #set the other information
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
        local_results.addLog('info', 'Fitting of the contrast was a success')
        local_results.setComplete()

        #tell fit handler what happened
        self.log.addLog(
            'info', 
            'Fitting of the contrast was a success')
