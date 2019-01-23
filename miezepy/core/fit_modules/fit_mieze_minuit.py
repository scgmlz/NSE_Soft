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

from scipy import special as sp
from scipy import integrate as integrate
from scipy import special as sp
from scipy import constants as co
from scipy import optimize as op
from scipy import stats as st


import iminuit
import numpy as np
import scipy
import warnings
import math

from .fit_general import Fit_Handler

class Fit_MIEZE_Minuit(Fit_Handler): 

    def __init__(self):
        Fit_Handler.__init__(self)

    def fit_goodness(self,chi2, N_dof):
        ''' 
        Calculates the goodness of a leastsquare fit 
        according to 'Everything you want to know 
        about Data Analysis and Fitting'.
        Input: 
        - chi
        - N_dof
        Output: 
        - Q
        '''
        Gamma           = sp.gamma(N_dof/2.)
        func            = lambda y: y**(N_dof/2. - 1.) * math.exp(-y)
        integral,error  = scipy.integrate.quad(func, chi2/2., np.inf)
        Q               = 1.0 / Gamma * integral

        return Q

    def minuit_fit_cosine(self,counts, time, freq, count_error):
        '''
        Creates the minuit fit function and runs 
        leastsquarefit.
        - counts (array of)
        - time (echo time ?)
        - freq (float)
        - count_error (array of float)
        '''
        self.minuit_parameters = [counts, time,count_error, freq]

        phase0  = 0
        offset0 = np.mean(counts)
        ampl0   = np.abs(np.mean(counts) - np.amin(counts))

        fit     = iminuit.Minuit(self.fit_cosine,
                            phase   = phase0,
                            offset  = offset0,
                            ampl    = ampl0,
                            pedantic=False,
                            print_level=0)
        fit.migrad()

        return fit 

    def fit_cosine(self,phase,offset,ampl):
        '''
        Creates the minuit fit function and runs 
        leastsquarefit.
        '''
        counts      = self.minuit_parameters[0]
        time        = self.minuit_parameters[1]
        count_error = self.minuit_parameters[2]
        freq        = self.minuit_parameters[3]

        with warnings.catch_warnings():
            try:
                return sum((((ampl*np.cos(freq*t+phase)+offset-c)**2)/e**2 for c,t,e in zip(counts,time,count_error)))
            except:
                return np.nan

    def minuit_fit_exp(self,contrast, SEtime, contrasterr):
        '''
        Creates the minuit fit function and runs 
        leastsquarefit.
        '''
        self.minuit_parameters = [contrast,SEtime,contrasterr]
        Gamma0 = 10.

        fit = iminuit.Minuit(
            self.fit_exp,
            Gamma = Gamma0,
            pedantic=False,
            print_level=0)

        fit.migrad()

        params  = fit.values
        chi2    = fit.fval
        cov     = fit.np_matrix()
        Cov     = np.array(cov).reshape([1,1])
        Gamma   = fit.values['Gamma']
        Gammaerr = np.sqrt(Cov[0][0])

        x = np.linspace(0.01,3,1000)

        return {'Gamma': Gamma,
                'Gamma_error': Gammaerr,
                'Curve':np.exp(-Gamma*1e-6*co.e*x*1e-9/co.hbar),
                'Curve Axis':x}

    def fit_exp(self,Gamma):
        '''
        Gamma exponential fit minimizer function
        '''
        contrast    = self.minuit_parameters[0]
        SEtime      = self.minuit_parameters[1]
        contrasterr = self.minuit_parameters[2]
        with warnings.catch_warnings():
            try:
                return sum(
                        (( np.exp(-Gamma*1.e-6*co.e*t*1.e-9/co.hbar)-c)**2. 
                        /e**2.
                        for c, t, e in zip(contrast, SEtime, contrasterr)))
            except:
                return np.nan


    def fit_data_cov(
        self,
        results, 
        data, 
        data_error, 
        Qmin = 0, 
        time_chan = 16,  
        position = [], 
        fit_des = ''):

        '''
        Fits sine curves into n_point echoes.
        Input: 
        - data is a list of data arrays (~128x128)
        - data_error is an array of errors associated
        - Qmin is the goodness of fit minimal value
        Output: 
        - will store the fit result into the associated
        class as a dictionary:
            'ampl'
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
        ##############################################
        #Initialize the output dictionary with all def.
        local_results = results.generate_result( name = 'Fit data covariance')

        #the description
        local_results.add_log('info', fit_des)

        ##############################################
        #Set basis variables
        len_data    = len( data )
        time        = np.arange( len_data, dtype=float )
        freq        = ( 2. * np.pi ) / time_chan
     
        ##############################################
        #there is no data so no fit...
        if np.sum(data) == 0.:
            local_results.add_log('warning', 'Fit failed: No counts present.')
            local_results.set_complete()
            self.log.add_log(
                'error', 
                'Fit failed: No counts present.')
            return False

        ##############################################
        # Fit the data
        fit = self.minuit_fit_cosine(data, time, freq, data_error)

        ##############################################
        # minuit failed
        if fit == None:
            local_results.add_log('error', 'minuit failed')
            local_results.set_complete()
            self.log.add_log(
                'error', 
                'Fit failed: Minuit failed to compute.')
            return False

        ##############################################
        # covariance inaccurate
        if not fit.matrix_accurate():
            local_results.add_log('error', 'cov_failed')
            local_results.set_complete()
            self.log.add_log(
                'error', 
                'Fit failed: Covariance not valid.')
            return False

        ##############################################
        # evaluate goodness
        params  = fit.values
        chi2    = fit.fval
        Q       = self.fit_goodness(chi2, len(data))

        if not Q >= Qmin:
            local_results.add_log('info', 'Qmin_bigger_Q')
            local_results.set_complete()
            self.log.add_log(
                'error', 
                'Fit not trusted: Q = {:.2f} < {:.2f} = Qmin).'.
                format(Q, Qmin))
            return False

        ##############################################
        # Everything in order proceed
        Cov             = np.array(fit.np_matrix()).reshape([3,3])
        ampl            = params['ampl']
        amplerr         = np.sqrt(Cov[2][2])
        offset          = params['offset']
        offset_error    = np.sqrt(Cov[1][1])
        phase_error     = np.sqrt(Cov[0][0])
        errCov          = np.sqrt(Cov[2][2]/(offset)**2+Cov[1][1]*(ampl/((offset)**2))**2)
        fit_error_Cov   = np.sqrt(
            Cov[0][0] * ( params['ampl'] 
                * np.sin(freq * np.arange(len_data) + params['phase']) ) ** 2 
            + Cov[1][1] * ( params['ampl']
                * np.sin(freq * np.arange(len_data) + params['phase']) + 1 ) ** 2 
            + Cov[2][2] * ( 1
                * np.sin(freq * np.arange(len_data) + params['phase']) ) ** 2 )

        ##############################################
        # populate result dictionary
        local_results['ampl']         = ampl
        local_results['ampl_error']   = amplerr
        local_results['phase']        = params['phase']
        local_results['phase_error']  = phase_error
        local_results['mean']         = params['offset']
        local_results['mean_error']   = offset_error
        local_results['pol']          = abs(ampl/(params['offset']))
        local_results['pol_error']    = {'Cov': errCov}
        local_results['sine_error']   = {'Cov': fit_error_Cov}
        local_results['chi_2']        = chi2/10.**5

        #write the dictionary entries
        local_results.add_log('info', 'success')
        local_results.set_complete()

        #tell fit handler what happened
        self.log.add_log(
            'info', 
            'Fit success')

        return True
