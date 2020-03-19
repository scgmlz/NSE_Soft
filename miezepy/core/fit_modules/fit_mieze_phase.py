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

import iminuit
import numpy as np
import copy
import os

#functions for processing the phase through pregroup masks
from .library_fit import phaseMaskFunction
from .library_fit import correctPhaseParaMeas
from .library_fit import loopLibrary
from .library_fit import phaseExposure
from .library_fit import reorganizeResult

#functions to be used for processing the phase through foil corrections
from .fit_worker import WorkerPool

class PhaseProcessing():
    para_dict = {}
    log       = None

    def __init__(self):
        self.para_dict = {}

    def noCorrection(self, target, results):
        '''
        The phase correction can be turned off to 
        allow for quick analysis of the data. This
        will simply fill the associated datafield.

        Parameters
        ----------
        target : DataStructure
            The current active datastructure

        results : ResultStructure
            The current active result structure
        '''
        #Initialize the output dictionary with all def.
        local_results = results.generateResult( name = 'Uncorrected Phase')
        data_meas   = target.bufferedData
        data_map    = target.map
        para_name   = self.para_dict['para_name']
        echo_name   = self.para_dict['echo_name']
        meas_name   = self.para_dict['meas_name']

        para_axis   = target.get_axis(para_name) 
        meas_axis   = target.get_axis(meas_name) 
        echo_axis   = target.get_axis(echo_name)

        loop = loopLibrary(self, target, 'loop_main')
        index_array = []
        for key, meas, echo in loop:
            index_array.append([key,meas, echo])

        #loop
        idx = 0
        temp = {}
        for key, meas, echo in loop:
            #grab the data slice
            if not data_map[para_axis.index(index_array[idx][0]), 
                        meas_axis.index(index_array[idx][1]), 
                        echo_axis.index(index_array[idx][2]), 0, 0] == -1:

                temp[idx] = data_meas[
                        para_axis.index(index_array[idx][0]), 
                        meas_axis.index(index_array[idx][1]), 
                        echo_axis.index(index_array[idx][2])]

            idx += 1

        temp_reorganized = reorganizeResult(temp, index_array, loop)

        ##############################################
        #finalize result and send it out
        local_results['Shift'] = temp_reorganized

        #write the dictionary entries
        local_results.addLog('info', 'Computation of the shift was a success')
        local_results.setComplete()
        
        #tell fit handler what happened
        self.log.addLog(
            'info', 
            'Computation of the shift was a success')

    def correctPhase(self,target, mask, results):
        '''
        This function is the main callable
        to process with the change of the phase. 
        note that this method uses the pregroup
        mask method.

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
        local_results = results.generateResult( name = 'Corrected Phase')

        #extract the relevant parameters
        premask     = mask.mask
        phase       = results.getLastResult('Phase calculation', 'Phase')
        data_meas   = target.bufferedData
        data_map    = target.map
        para_name   = self.para_dict['para_name']
        echo_name   = self.para_dict['echo_name']
        meas_name   = self.para_dict['meas_name']
        foil_name   = self.para_dict['foil_name']
        tcha_name   = self.para_dict['tcha_name']
        cha_num     = target.get_axis_len(tcha_name)

        para_axis   = target.get_axis(para_name) 
        meas_axis   = target.get_axis(meas_name) 
        echo_axis   = target.get_axis(echo_name) 
        foil_axis   = target.get_axis(foil_name) 

        loop = loopLibrary(self, target, 'loop_main')

        loop_2 = [
            (m1, m2)
            for m1 in range(1,premask.max()+1)
            for m2 in range(target.get_axis_len(foil_name))] 

        worker_pool = WorkerPool(self.para_dict['processors'])
        index_array = []
        for key, meas, echo in loop:
            index_array.append([key,meas, echo])

        #loop
        idx = 0
        for key, meas, echo in loop:
            #grab the data slice
            if data_map[para_axis.index(index_array[idx][0]), 
                        meas_axis.index(index_array[idx][1]), 
                        echo_axis.index(index_array[idx][2]), 0, 0] == -1:
                pass
            else:
                worker_pool.addWorker([
                    correctPhaseParaMeas,
                    index_array[idx], idx,
                    data_meas[
                        para_axis.index(index_array[idx][0]), 
                        meas_axis.index(index_array[idx][1]), 
                        echo_axis.index(index_array[idx][2])],
                    cha_num, echo_axis, foil_axis,
                    premask, loop_2, phase[echo]])
            idx += 1

        temp = worker_pool.startPool()
        temp_reorganized = reorganizeResult(temp, index_array, loop)

        ##############################################
        #finalize result and send it out
        local_results['Shift'] = temp_reorganized

        #write the dictionary entries
        local_results.addLog('info', 'Computation of the shift was a success')
        local_results.setComplete()
        
        #tell fit handler what happened
        self.log.addLog(
            'info', 
            'Computation of the shift was a success')
                
    def extractPhaseMask(self, target, mask, results):
        '''
        This part will try to correct the phase anomalies through the 
        fit of each mask region an then fit it the sinus form. After
        which a map will be generated to which the entire dataset will
        be corrected.

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
        local_results   = results.generateResult( name = 'Phase calculation')
        selected_ref    = self.para_dict['Reference']

        para_name       = self.para_dict['para_name']
        meas_name       = self.para_dict['meas_name']
        echo_name       = self.para_dict['echo_name']
        foil_name       = self.para_dict['foil_name']
        tcha_name       = self.para_dict['tcha_name']

        echo_axis = target.get_axis(echo_name)
        foil_axis = target.get_axis(foil_name)
        chan_num  = target.get_axis_len(tcha_name)
        
        ref_index       = [
            target.get_axis_idx(para_name, selected_ref[0]),
            target.get_axis_idx(meas_name, selected_ref[1])]
        reference_meas  = target.bufferedData.__getitem__(tuple(ref_index))
        premask         = mask.mask

        #set result dimensions
        result_dimension = (
            target.data_objects[0].dim[0],
            target.data_objects[0].dim[1])   

        loop = [e1 for e1 in range(1,premask.max()+1)]

        loop_2 = [
            (e1, e2)
            for e1 in target.get_axis(echo_name)
            for e2 in target.get_axis(foil_name)]

        phase_shift = {}
        for echo in target.get_axis(echo_name):
            phase_shift[echo] = np.zeros((
                target.get_axis_len(foil_name),
                target.data_objects[0].dim[0],
                target.data_objects[0].dim[1]))

        worker_pool = WorkerPool(self.para_dict['processors'])
        index_array = []
        for echo, foil in loop_2:
            index_array.append([echo, foil])

        #initialise the output
        idx = 0
        for echo, foil in loop_2:
            worker_pool.addWorker([
                phaseMaskFunction, idx, foil,
                result_dimension, loop,
                foil_axis,reference_meas[echo_axis.index(echo)],
                chan_num, premask, self.para_dict['time_channels']])
            idx += 1
        temp = worker_pool.startPool()
        for idx in range(len(index_array)):
            phase_shift[index_array[idx][0]][index_array[idx][1],:,:] = temp[idx][:,:]

        ############################################
        #send out the result to the handler
        local_results['Phase']        = phase_shift
        local_results['Reference']    = selected_ref

        #write the dictionary entries
        local_results.addLog('info', 'Fit of the phase was a success')
        local_results.setComplete()

        #tell fit handler what happened
        self.log.addLog(
            'Info', 
            'Fit of the phase was a success')

    def correctPhaseExposure(self, target, mask, instrument, results):
        '''
        This function is the main callable
        to process with the change of the phase. 
        note that this method uses the pregroup
        mask method.

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
        local_results = results.generateResult( name = 'Corrected Phase')

        #extract the relevant parameters
        echo_source     = results.getLastResult('Echo Sources', 'Echo Dict')
        data_meas       = target.bufferedData
        data_map        = target.map

        para_name   = self.para_dict['para_name']
        meas_name   = self.para_dict['meas_name']
        echo_name   = self.para_dict['echo_name']
        foil_name   = self.para_dict['foil_name']
        tcha_name   = self.para_dict['tcha_name']

        para_axis   = target.get_axis(para_name) 
        meas_axis   = target.get_axis(meas_name) 
        echo_axis   = target.get_axis(echo_name) 
        foil_axis   = target.get_axis(foil_name) 
        cha_axis    = target.get_axis(tcha_name)

        loop_main   = loopLibrary(self, target, 'loop_main')
        loop_para   = loopLibrary(self, target, 'loop_para')
        loop_pixel  = loopLibrary(self, target, 'loop_pixel')
        loop_final  = loopLibrary(self, target, 'loop_final')

        #other constants
        m_n             = 1.674927471e-27 # kg
        h_J             = 6.626070040e-34 # J*s

        #neutron velocities
        velocities  = {}
        d_sam_det   = {}
        freq        = {}
        for key in echo_source.keys():
            velocities[key] = h_J/(m_n*echo_source[key]['wavelength'])
            d_sam_det[key]  = echo_source[key]['lsd']*1e-9
            freq[key]       = echo_source[key]['freq_1'] - echo_source[key]['freq_0']

        index_map = instrument.detector.processPhaseShift(
            echo_axis,velocities,
            d_sam_det,freq)

        worker_pool = WorkerPool(self.para_dict['processors'])
        index_array = []
        for key, meas, echo in loop_main:
            index_array.append([key,meas, echo])

        #loop
        idx = 0
        for key, meas, echo in loop_main:
            #grab the data slice
            if data_map[para_axis.index(index_array[idx][0]), 
                        meas_axis.index(index_array[idx][1]), 
                        echo_axis.index(index_array[idx][2]), 0, 0] == -1:
                pass
            else:
                worker_pool.addWorker([
                    phaseExposure, idx,
                    data_meas[
                        para_axis.index(index_array[idx][0]), 
                        meas_axis.index(index_array[idx][1]), 
                        echo_axis.index(index_array[idx][2])],
                    index_map[echo_axis.index(index_array[idx][2])],
                    loop_final, foil_axis, cha_axis])
            idx += 1

        temp = worker_pool.startPool()
        temp_reorganized = reorganizeResult(temp, index_array, loop_main)

        ##############################################
        #finalize result and send it out
        local_results['Shift']        = temp_reorganized

        #write the dictionary entries
        local_results.addLog('info', 'Computation of the shift was a success')
        local_results.setComplete()
        
        #tell fit handler what happened
        self.log.addLog(
            'info', 
            'Computation of the shift was a success')
