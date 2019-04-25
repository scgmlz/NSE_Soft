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
from scipy import integrate as integrate
from scipy import special as sp
from scipy import constants as co
import math

from .library_iminuit import CosineMinuit
from ..module_result import ResultStructure

def fitGoodness(chi2, N_dof):
    ''' 
    Calculates the goodness of a leastsquare fit 
    according to 'Everything you want to know 
    about Data Analysis and Fitting'.

    Parameters
    ----------
    chi
    N_dof

    Returns
    -------
    Q
    '''
    Gamma           = sp.gamma(N_dof/2.)
    func            = lambda y: y**(N_dof/2. - 1.) * math.exp(-y)
    integral,error  = integrate.quad(func, chi2/2., np.inf)
    Q               = 1.0 / Gamma * integral

    return Q

def fitDataSinus(results, data, data_error, Q_min = 0, time_chan = 16, time_select = []):
    '''
    This routine will fit the data sinus elements

    Parameters
    ----------
    - data is a list of data arrays (~128x128)
    - data_error is an array of errors associated
    - Q_min is the goodness of fit minimal value

    Returns
    ------- 
    return : boolean
        This value is true if the result is set:
        'amplitude'
        'phase'
        'mean'
        'error'
        'pol'
        'fit_error'
        'chi_2'
        'pol_error'
        'mean_error'
        'ampl_error'
    '''
    #Initialize the output dictionary with all def.
    local_results = results.generateResult( name = 'Fit Data Sinus')

    #there is no Data so no fit...
    if np.sum(data) == 0.:
        local_results.addLog('warning', 'Fit failed: No counts present.')
        local_results.setComplete()
        return False

    # Fit the data
    freq = (2.*np.pi ) / time_chan
    fit_structure = CosineMinuit()

    if not len(time_select) == 0:
        fit = fit_structure.fitCosine(
            np.array(data)[np.array(time_select)], 
            np.arange(len(data), dtype=float)[np.array(time_select)], 
            freq, 
            np.array(data_error)[np.array(time_select)])
    else:
        fit = fit_structure.fitCosine(
            data,np.arange(len(data), dtype=float), 
            freq, data_error)        

    # minuit failed
    if fit == None:
        local_results.addLog('error', 'minuit failed')
        local_results.setComplete()
        return False

    # covariance inaccurate
    if not fit.matrix_accurate():
        local_results.addLog('error', 'cov_failed')
        local_results.setComplete()
        return False

    # evaluate goodness
    params  = fit.values
    chi2    = fit.fval
    Q       = fitGoodness(chi2, len(data))

    if not Q >= Q_min:
        local_results.addLog('info', 'Q_min_bigger_Q')
        local_results.setComplete()
        return False

    # Everything in order proceed
    len_data        = len(data)
    Cov             = np.array(fit.np_matrix()).reshape([3,3])
    amplitude       = params['amplitude']
    amplitude_error = np.sqrt(Cov[2][2])
    offset          = params['offset']
    offset_error    = np.sqrt(Cov[1][1])
    phase_error     = np.sqrt(Cov[0][0])
    errCov          = np.sqrt(Cov[2][2]/(offset)**2+Cov[1][1]*(amplitude/((offset)**2))**2)
    fit_error_Cov   = np.sqrt(
        Cov[0][0] * ( params['amplitude'] 
            * np.sin(freq * np.arange(len_data) + params['phase']) ) ** 2 
        + Cov[1][1] * ( params['amplitude']
            * np.sin(freq * np.arange(len_data) + params['phase']) + 1 ) ** 2 
        + Cov[2][2] * ( 1
            * np.sin(freq * np.arange(len_data) + params['phase']) ) ** 2 )

    # populate result dictionary
    local_results['amplitude']      = amplitude
    local_results['amplitude_error']= amplitude_error

    local_results['phase']          = params['phase']
    local_results['phase_error']    = phase_error

    local_results['mean']           = params['offset']
    local_results['mean_error']     = offset_error

    local_results['pol']          = abs(amplitude/(params['offset']))
    local_results['pol_error']    = {'Cov': errCov}

    local_results['sine_error']   = {'Cov': fit_error_Cov}
    local_results['chi_2']        = chi2/10.**5

    #write the dictionary entries
    local_results.addLog('info', 'success')
    local_results.setComplete()

    return True

def phaseExposure(idx, data_input, index_map, loop, foil_axis, cha_axis, result_dict) :
    '''
    This function will manage the run over the echo 
    times for the set echo time. Note that the 
    result_dict is a shared dictionary instance by 
    the python process manager.

    Parameters
    ----------
    data_input : np.ndarray
        This is the actual data

    index_map : np.ndarray
        This indexes to be shifted
        
    loop : int arrays
        This is the loop to be performed over the 
        mask and the foils. It is processed before
        to avoid to much arguments

    foil_axis : int array
        The axis fo the foils

    cha_axis : int array
        The axis fo the time channels

    result_dict : shared dict
        This is the variable used to save the result

    '''
    # perform the shift:
    temp_reorganized = np.zeros(data_input.shape)

    for foil, cha in loop:
        #set indexes
        foil_idx    = foil_axis.index(foil)
        cha_idx    = cha_axis.index(cha)

        #select only those pixels and timechannels, where the shifting index matches the timechannel.
        temp = np.where(
            index_map[foil_idx] == cha_idx, 
            data_input[foil_idx,:,:,:], 0) 

        # shift these pixels by the required amount of timechannels
        temp_2 = np.roll(temp[:,:, :],-cha_idx, 0) 

        # fill the "shifted" array with the correctly shifted timechannels and pixels
        temp_reorganized[foil_idx] += temp_2 

    result_dict[idx] = temp_reorganized

def phaseMaskFunction(
    idx, foil, result_dimension, loop, 
    foil_axis,reference_meas, chan_num, premask, 
    time_select,result_dict ):
    '''
    This function will manage the run over the echo 
    times for the set echo time. Note that the 
    result_dict is a shared dictionary instance by 
    the python process manager.

    Parameters
    ----------
    result_dimension : int array
        This is the dimensionality of the array that
        will be computed and sent as output

    echo : float 
        This is the echo time

    loop : int arrays
        This is the loop to be performed over the 
        mask and the foils. It is processed before
        to avoid to much arguments

    foil_axis : int array
        The axis fo the foils

    reference_meas : np.ndarray
        This is the actual data

    chan_num : int
        Number of time channels

    premask : ndarray
        The mask

    result_dict : shared dict
        This is the variable used to save the result

    '''
    results = ResultStructure()
    foil_idx    = foil_axis.index(foil)
    output  = np.zeros(result_dimension)
    for mask_num in loop:
        proc_mask   = premask == mask_num
        output[:, :] += phaseFit(
            proc_mask, foil_idx, 
            chan_num, reference_meas, 
            results, time_select = time_select)

    result_dict[idx] = output

def phaseFit(proc_mask, foil_idx, chan_num, reference_meas, results, time_select = []):
    '''
    Processing the phase

    Parameters
    ----------
    foil_idx : int
        The index of the chosen foil

    reference_meas : np.ndarray
        This is the actual data

    chan_num : int
        Number of time channels

    proc_mask : ndarray
        The mask

    results : ResultStructure
        Where the results are saved

    '''
    counts = [
        (np.multiply(reference_meas[foil_idx, timechannel],proc_mask)).sum()
        for timechannel in range(chan_num)]
    count_error = np.sqrt([float(count) for count in counts])
    success     = fitDataSinus(
        results,
        data        = counts, 
        data_error  = count_error, 
        Q_min       = 0.,
        time_chan   = chan_num,
        time_select = time_select)

    message = results.getLastResult('Fit Data Sinus').log.returnLastLog('error')
    if not success and message == 'cov_failed':
        counts      = counts[1:]
        count_error = np.sqrt([float(count) for count in counts])
        success     = fitDataSinus(
            results,
            data        = counts, 
            data_error  = count_error, 
            Q_min        = 0.,
            time_chan   = chan_num,
            time_select = time_select)

        message = results.getLastResult('Fit Data Sinus').log.returnLastLog('error')
        if not success and message == 'cov_failed':
            return  -1*proc_mask

    return((
        results.getLastResult('Fit Data Sinus')['phase'] 
        + (np.pi if results.getLastResult('Fit Data Sinus')['amplitude'] < 0 else 0 ))% (2. * np.pi))*proc_mask

def correctPhaseParaMeas(index_array, idx,  data_meas, cha_num, echo_axis, foil_axis, premask, loop, phase, output_dict):
    '''
    This function will manage the run over the echo 
    times for the set echo time. Note that the 
    result_dict is a shared dictionary instance by 
    the python process manager.

    Parameters
    ----------
    data_meas : int array
        This is the dimensionality of the array that
        will be computed and sent as output

    echo : float 
        This is the echo time

    loop : int arrays
        This is the loop to be performed over the 
        mask and the foils. It is processed before
        to avoid to much arguments

    foil_axis : int array
        The axis fo the foils

    reference_meas : np.ndarray
        This is the actual data

    chan_num : int
        Number of time channels

    premask : ndarray
        The mask

    echo_axis : int array
        The axis fo the echos

    foil_axis : int array
        The axis fo the foils

    phase : dictionary of ndarrays
        This is the result from the phase shift correction
        extraction for each echo

    result_dict : shared dict
        This is the variable used to save the result

    '''
    cha_num_int    = cha_num
    cha_num_float  = float(cha_num)
    output = {}

    #print the processing step
    print(
        'Processing shift for ' + str(index_array[0]) 
        +' measurement ' + str(index_array[1])
        +' echo ' + str(index_array[2]))

    #initialise variables
    shifted_element = np.zeros((data_meas.shape))    
    current_mask = None

    #cycle over the elements
    for mask_num, foil in loop:
        if not mask_num == current_mask:
            #select only one mask
            proc_mask       = premask == mask_num
            mask_sum        = np.sum(proc_mask)
            current_mask    = int(mask_num)
        
        #select only one mask
        index = np.arange(
            int((
                2*np.pi-np.sum(phase[foil]*proc_mask)/mask_sum)
                /(2*np.pi/cha_num_float)+np.pi/2.),
            int((
                2*np.pi-np.sum(phase[foil]*proc_mask)/mask_sum)
                /(2*np.pi/cha_num_float)+np.pi/2.+cha_num_float)
            ,1)
        index = np.asarray(
            [index[i]%cha_num_int 
            for i in range(cha_num_int)])
        shifted_element[foil,:, :, :] += data_meas[foil, index,:,:]*proc_mask

    #process the result
    output_dict[idx] = shifted_element

def miezeTauProcessing(metadata_object, target):
    '''
    Processes the MIEZE time from a dataset
    This will later go through the instrument 
    definition. 

    Parameters
    ----------
    metadata_object : metadata object
        This is where the instrument states are stored

    target : DataStructure
        This is the structure storing the dat

    Returns
    ------- 
    the resulting tau value with all the parameters used to 
    generate it
    '''
    #unpack the container
    wavelength          = metadata_object['Wavelength']
    freq_0              = metadata_object['Freq. first']
    freq_1              = metadata_object['Freq. second']
    lsd                 = metadata_object['lsd']
    wavelength_error    = target.metadata_class['Wavelength error']
    lsd_error           = target.metadata_class['Distance error']

    #process tau and the error of tau
    tau, tau_error = miezeTauCalculation(
        wavelength,
        freq_0,
        freq_1,
        lsd,
        wavelength_error = wavelength_error,
        lsd_error = lsd_error)

    #send it out to the metadata class
    metadata_object.addMetadata('tau', value = tau)
    metadata_object.addMetadata('tau_error', value = tau_error)

    return [
        tau, 
        {
            'tau_error': tau_error, 
            'wavelength': wavelength, 
            'wavelength_error': wavelength_error,
            'freq_0': freq_0, 
            'freq_1': freq_1, 
            'lsd' :lsd,
            'lsd_error': lsd_error}]

def miezeTauCalculation(wavelength, freq_0, freq_1, lsd, wavelength_error = 0 ,lsd_error = 0):
    '''
    Processes the MIEZE time

    Parameters
    ----------
    wavelength : float
        The wavelength of the incident neutron beam

    freq_0 : float
        The frequency of the first coil

    freq_1 : float
        The frequency of the second coil

    lsd : float
        The distance between the sample and the detector

    Returns
    ------- 
    the resulting tau  and the error
    '''
    delta_freq  = freq_1 - freq_0
    para        = ( 2. * co.m_n ** 2 ) / (co.h ** 2) 
    tau         = para * wavelength ** 3 * delta_freq * lsd 
    tau_error   = para * ( 
        ( wavelength_error * wavelength * 3 * wavelength ** 2 * delta_freq * lsd )
        + ( lsd_error * lsd * wavelength ** 3 * delta_freq ))

    return tau, tau_error

def contrastEquation(target, BG_target):
    '''
    Contrast equation separating the case of 
    background or not in a smart way

    Parameters
    ----------
    target : float array
        This is the contrast result for the normal value
    BG_target : float array
        This is the contrast for the background
    '''
    if target[2]-BG_target[2] == 0:
        return 0
    else:
        return ((abs(target[0])-abs(BG_target[0]))/(target[2]-BG_target[2]))

def contrastErrorEquation(target, BG_target):
    '''
    Contrast error equation separating the case of 
    background or not in a smart way

    Parameters
    ----------
    target : float array
        This is the contrast result for the normal value
    BG_target : float array
        This is the contrast for the background
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

def loopLibrary(fit, target, name):
    '''
    This routine allows to ease the code within the
    critical functions by returning the requested loop

    Parameters
    ----------
    fit : fit instance 
        The fit instance that is asking for the loop

    target : datastructure
        This is the contrast result for the normal value

    name : string
        The name of the loop requested

    Returns
    ----------
    loop : array of values
    '''

    para_name   = fit.para_dict['para_name']
    meas_name   = fit.para_dict['meas_name']
    echo_name   = fit.para_dict['echo_name']
    foil_name   = fit.para_dict['foil_name']
    tcha_name   = fit.para_dict['tcha_name']

    para_axis   = target.get_axis(para_name) 
    meas_axis   = target.get_axis(meas_name) 
    echo_axis   = target.get_axis(echo_name) 
    foil_axis   = target.get_axis(foil_name) 
    cha_axis    = target.get_axis(tcha_name)

    if name == 'loop_main':
        loop = [
            (e1, e2, e3) 
            for e1 in para_axis
            for e2 in meas_axis
            for e3 in echo_axis]

    elif name == 'loop_para':
        loop  = [
            (e0,e1) 
            for e0 in echo_axis 
            for e1 in foil_axis]

    elif name == 'loop_pixel':
        loop  = [
            (x,y) 
            for x in range(128) 
            for y in range(128)]

    elif name == 'loop_final':
        loop  = [
            (e1,e2)
            for e1 in foil_axis
            for e2 in cha_axis]

    return loop

def reorganizeResult(temp, index_array, loop):
    '''
    This routine allows to ease the code within the
    critical functions by returning the requested loop

    Parameters
    ----------
    temp : data
        The data organized in a linear dictionary

    index_array : array of values
        These will be used to construct the keys of the output

    loop : array of values
        The definition of the loop

    Returns
    ----------
    temp_reorganized : dictionary of values
    '''
    temp_reorganized = {}
    idx = 0
    for idx in range(len(loop)):
        if idx in temp.keys():
            para = index_array[idx][0]
            meas = index_array[idx][1]
            echo = index_array[idx][2]

            if not para in temp_reorganized.keys():
                temp_reorganized[para] = {}
            
            if not meas in temp_reorganized[para].keys():
                temp_reorganized[para][meas] = {}

            temp_reorganized[para][meas][echo] = temp[idx]
        idx +=1

    return temp_reorganized


def contrastLogicRef(target, local_results):
    '''
    This function was built to ease readability
    and to provide the contrast calculation
    routine.

    Parameters
    ----------
    target : DataStructure
        The current dataset with all metadata
    
    local_results : ResultStructure 

    Returns
    ------- 
    contrast : list of float
        The Contrast and its error
    '''
    #initialise the contrast result
    contrast_ref        = {}
    contrast_ref_error  = {}

    #Process the result
    for echo in target.keys():

        #do a check of the value and throw an error if 0
        if target[echo][0] == 0 or target[echo][2] == 0:
            if target[echo][0] == 0:
                local_results.addLog(
                    'warning', 
                    'The amplitude from the reference fit is 0. Please investigate...')
                local_results.addLog(
                    'error', 
                    'Setting the value to 1')
            elif target[echo][2] == 0:
                local_results.addLog(
                    'error', 
                    'The mean from the reference fit is 0. Please investigate...')
                local_results.addLog(
                    'error', 
                    'Setting the value to 1')

            target[echo][0] = 1.
            target[echo][1] = 1.

        #set output
        contrast_ref[echo] = contrastEquation(
            target[echo],    
            [0,0,0,0])

        contrast_ref_error[echo] = contrastErrorEquation(
            target[echo], 
            [0,0,0,0])

    return [contrast_ref, contrast_ref_error]

def contrastLogicMain(positions, contrast_results, BG_result, local_results):
    '''
    This function was built to ease readability
    and to provide the contrast calculation
    routine.

    Parameters
    ----------
    target : DataStructure
        The current dataset with all metadata

    BG_result : array of float
        The result of the background processing
    
    local_results : ResultStructure 

    Returns
    ------- 
    contrast : list of float
        The Contrast and its error
    '''
    ############################################
    #initialise the contrast result
    contrast        = []
    contrast_error  = []

    for meas, echo in positions:
        
        target = contrast_results[meas][echo]

        if not BG_result == None:
            BG_target = BG_result[echo]
        else:
            BG_target = [0,0,0,0]

        contrast.append(
            float(contrastEquation(target, BG_target)))
        contrast_error.append(
            float(contrastErrorEquation(target, BG_target)))

    return [contrast, contrast_error]

def multiAxis(select, target):
    '''
    This function performs axis modifications 
    to allow the compression of measurements
    for different parameters

    Parameters
    ----------
    select : list of parameters
        The selected elements

    target : DataStructure
        The current active datastructure 

    Returns
    ------- 
    axis and position of the elements
    '''
    #grab meta
    para_name = target.axes.names[0]
    meas_name = target.axes.names[1]
    echo_name = target.axes.names[2]

    para_axis = target.get_axis(para_name)
    meas_axis = target.get_axis(meas_name)
    echo_axis = target.get_axis(echo_name)

    data_map  = target.map
    axis      = {}
    positions = {}

    #set the loop
    loop = [
        (e1, e2, e3) 
        for e1 in select 
        for e2 in meas_axis
        for e3 in echo_axis]

    #loop
    for para, meas, echo in loop:
        if not data_map[
            para_axis.index(para),
            meas_axis.index(meas),
            echo_axis.index(echo),0,0] == -1:

            if not para in axis.keys():
                axis[para]      = []
                positions[para] = []

            axis[para].append(echo)
            positions[para].append((meas, echo))

    return axis, positions