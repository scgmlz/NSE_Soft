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

from scipy import integrate as integrate
from scipy import special as sp
from scipy import constants as co
from scipy import optimize as op
from scipy import stats as st

import iminuit
import numpy as np
import warnings

class CosineMinuit:

    def fitCosine(self, counts, time, freq, error):
        '''
        Creates the minuit fit function and runs 
        leastsquarefit.

        Parameters
        ----------
        counts : float array
            The data

        time : float array
            The x abscises so to speak

        freq : float
            The frequency distribution

        error : float array

        Returns
        -------
        fit : iminuit fit structure
        '''
        self.argument_dict = {}
        self.argument_dict['counts']       = counts
        self.argument_dict['time']         = time
        self.argument_dict['freq']         = freq
        self.argument_dict['error']        = error

        minuit_dict = {}
        minuit_dict['phase']       = 0
        minuit_dict['offset']      = np.mean(counts)
        minuit_dict['amplitude']   = np.abs(np.mean(counts) - np.amax(counts))
        minuit_dict['pedantic']    = False
        minuit_dict['print_level'] = 0

        fit     = iminuit.Minuit(self.cosine, **minuit_dict)
        fit.migrad()

        return fit 

    def cosine(self, phase, offset, amplitude):
        '''
        Creates the minuit fit function and runs 
        leastsquarefit.

        Parameters
        ----------
        phase : float
            Phase of the sinus oscillation

        offset : float
            Offset along the y absice

        amplitude : float
            Amplitude of the sinus oscillation

        Returns
        -------
        fit result : float
        '''
        with warnings.catch_warnings():
            try:
                return sum((((amplitude*np.cos(self.argument_dict['freq']*t+phase)+offset-c)**2)/e**2 if not e == 0 else np.nan for c,t,e in zip(self.argument_dict['counts'],self.argument_dict['time'],self.argument_dict['error'])))
            except:
                return np.nan

class ExpMinuit:

    def fitExp(self,contrast, SpinEchoTime, contrastError):
        '''
        Creates the minuit fit function and runs 
        leastsquarefit.

        Parameters
        ----------
        contrast : float array
            The data

        SpinEchoTime : float array
            The x abscises so to speak

        contrastError : float array

        Returns
        -------
        fit : fit result dictionary
        '''
        self.argument_dict = {}
        self.argument_dict['contrast']      = contrast
        self.argument_dict['SpinEchoTime']  = SpinEchoTime
        self.argument_dict['contrastError'] = contrastError

        minuit_dict = {}
        minuit_dict['Gamma']       = 10
        minuit_dict['pedantic']    = False
        minuit_dict['print_level'] = 0

        fit = iminuit.Minuit(self.exp,**minuit_dict)
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

    def exp(self,Gamma):
        '''
        Gamma exponential fit minimizer function

        Parameters
        ----------
        phase : float
            Phase of the sinus oscillation

        offset : float
            Offset along the y absice

        amplitude : float
            Amplitude of the sinus oscillation

        Returns
        -------
        fit result : float
        '''
        with warnings.catch_warnings():
            try:
                return sum(
                        (( np.exp(-Gamma*1.e-6*co.e*t*1.e-9/co.hbar)-c)**2. 
                        /e**2.
                        for c, t, e in zip(self.argument_dict['contrast'], self.argument_dict['SpinEchoTime'], self.argument_dict['contrastError'])))
            except:
                return np.nan
