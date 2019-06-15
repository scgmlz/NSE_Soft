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

from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np

from ....core.fit_modules.library_fit import fitDataSinus

class PanelWorker(QtCore.QObject):
    '''
    This is the panel worker that will be used to 
    perform on the fly computation of the contrast
    for a single parameter, measurement, echo, and
    foil.

    Signals
    ----------
    finished : pyqt signal
        Triggered when the worker successfully completed his job
    '''
    finished = QtCore.pyqtSignal()

    def __init__(self, method):
        '''
        Parameters
        ----------
        method : python class method
            The contrast calculation method
        '''
        QtCore.QObject.__init__(self)
        self.method     = method
        self._finished  = False
        
    def setParameters(self,data, para, foil, mask, results, time_channels):
        '''
        Parameters
        ----------
        data : numpy array
            The reduced data

        para : str or float
            The parameter value

        meas : int
            The measurement idx

        echo : float
            The echo time value

        foil : int 
            The foil value
        
        mask : numpy array
            The mask
        '''
        self.data = data
        self.para = para
        self.foil = foil
        self.mask = mask
        self.results = results
        self.time_channels = time_channels

    @QtCore.pyqtSlot()
    def run(self): 
        '''
        define the parameters
        '''
        self.counts = [
            np.sum(self.mask * self.data[timechannel]) 
            for timechannel in range(16)]
        fitDataSinus(self.results,self.counts, np.sqrt(self.counts), time_select=self.time_channels)
        try:
            fitDataSinus(self.results,self.counts, np.sqrt(self.counts), time_select=self.time_channels)
            self.fit = self.results.getLastResult('Fit Data Sinus')
        except:
            self.fit = None
            

        try:
            self.method(self.para,self.foil)
            self.process = self.results.getLastResult('Contrast calculation')
        except:
            self.process = None
        self._finished = True
        self.finished.emit()
