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

from .library_fit import phaseMaskFunction, correctPhaseParaMeas
from .fit_worker import WorkerPool

class PhaseProcessing(): 

    def __init__(self):
        self.para_dict = {}

    def correctPhase(self,target, mask, results):
        '''
        Calculates the shift
        Input: 
        - MIEZE data object
        - mask object
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

        loop = [
            (e1, e2, e3) 
            for e1 in target.get_axis(para_name) 
            for e2 in target.get_axis(meas_name)
            for e3 in target.get_axis(echo_name)]

        loop_2 = [
            (m1, m2)
            for m1 in range(1,premask.max()+1)
            for m2 in range(target.get_axis_len(foil_name))] 

        worker_pool = WorkerPool(10)
        index_array = []
        for key, meas, echo in loop:
            index_array.append([key,meas, echo])

        #loop
        idx = 0
        for key, meas, echo in loop:
            #grab the data slice
            if data_map[ para_axis.index(index_array[idx][0]), 
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

        temp_reorganized = {}
        idx = 0
        for key, meas, echo in loop:
            if idx in temp.keys():
                para = index_array[idx][0]
                meas = index_array[idx][1]
                echo = index_array[idx][2]

                if not para in temp_reorganized.keys():
                    temp_reorganized[para] = {}
                
                if not meas in temp_reorganized[para].keys():
                    temp_reorganized[para][meas] = {}

                temp_reorganized[para][meas][echo] = temp[idx]
                
            idx += 1

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
                
    def extractPhaseMask(self, target, mask, results):
        '''
        This part will try to correct the phase anomalies through the 
        fit of each mask region an then fit it the sinus form. After
        which a map will be generated to which the entire dataset will
        be corrected.
        '''
        #Initialize the output dictionary with all def.
        local_results   = results.generateResult( name = 'Phase calculation')
        selected_ref    = self.para_dict['Reference']
        reference_meas  = target.bufferedData.__getitem__(tuple(selected_ref))
        premask         = mask.mask
        echo_name       = self.para_dict['echo_name']
        foil_name       = self.para_dict['foil_name']
        tcha_name       = self.para_dict['tcha_name']

        #set result dimensions
        result_dimension = (
            target.get_axis_len(foil_name),
            target.data_objects[0].dim[0],
            target.data_objects[0].dim[1])      
        loop = [
            (e1, e3)
            for e1 in range(1,premask.max()+1)
            for e3 in target.get_axis(foil_name)]

        echo_axis = target.get_axis(echo_name)
        foil_axis = target.get_axis(foil_name)
        chan_num  = target.get_axis_len(tcha_name)

        #initialise the output
        phase_shift = {}
        worker_pool = WorkerPool(10)
        for echo in target.get_axis(echo_name):
            worker_pool.addWorker([
                phaseMaskFunction,
                result_dimension,echo, loop,
                foil_axis,reference_meas[echo_axis.index(echo)], 
                chan_num, premask])

        phase_shift = worker_pool.startPool()

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
