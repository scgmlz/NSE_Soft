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

def fitDataSinus(results, data, data_error, Q_min = 0, time_chan = 16):
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
    fit = fit_structure.fitCosine(
        data, 
        np.arange( len(data), dtype=float ), 
        freq, 
        data_error)

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

    local_results['phase']          = params['phase']%np.pi
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

def phaseMaskFunction(result_dimension,echo, loop, foil_axis,reference_meas, chan_num, premask, result_dict):
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
    output  = np.zeros(result_dimension)
    for mask_num, foil in loop:
        proc_mask   = premask == mask_num
        foil_idx    = foil_axis.index(foil)
        output[foil_idx, :, :] += phaseFit(
            proc_mask, foil_idx, chan_num, reference_meas, results)
    result_dict[echo] = output

def phaseFit(proc_mask, foil_idx, chan_num, reference_meas, results):
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
        time_chan   = chan_num)

    message = results.getLastResult('Fit Data Sinus').log.returnLastLog('error')
    if not success and message == 'cov_failed':
        counts      = counts[1:]
        count_error = np.sqrt([float(count) for count in counts])
        success     = fitDataSinus(
            results,
            data        = counts, 
            data_error  = count_error, 
            Q_min        = 0.,
            time_chan   = chan_num)

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
