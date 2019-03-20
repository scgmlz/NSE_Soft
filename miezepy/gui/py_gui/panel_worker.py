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
from PyQt5.QtWidgets import QInputDialog
import numpy as np

from ...core.fit_modules.library_fit import fitDataSinus

class PanelWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    intReady = QtCore.pyqtSignal(int)

    def __init__(self, parameters):
        '''
        define the parameters
        ———————
        Input: 
        - 0 data as numpy array
        - 1 para
        - 2 meas
        - 3 echo
        - 4 foil
        - 5 para
        - 6 meas
        - 7 echo
        - 8 foil
        - 9 env
        - 10 mask
        '''
        QtCore.QObject.__init__(self)
        self.parameters = parameters
        
    @QtCore.pyqtSlot()
    def run(self): 
        '''
        define the parameters
        '''
        para        = self.parameters[1]
        foil        = self.parameters[4]
        echo_idx    = self.parameters[7]
        foil_idx    = self.parameters[8]

        self.reshaped   = self.parameters[0]
        self.mask       = self.parameters[10]
        self.env        = self.parameters[9]
        self.counts     = [
            np.sum(self.mask * self.reshaped[echo_idx,foil_idx,timechannel]) 
            for timechannel in range(16)]
        fitDataSinus(self.env.results,self.counts, np.sqrt(self.counts))
        try:
            fitDataSinus(self.env.results,self.counts, np.sqrt(self.counts))

            self.fit = self.env.results.getLastResult('Fit Data Sinus')
        except:
            self.fit = None


        try:
            self.env.fit.calcContrastMain( 
                    self.env.current_data,
                    self.env.mask,
                    self.env.results,
                    select = [para],
                    foil = foil)

            self.process = self.env.results.getLastResult('Contrast calculation')
        except:
            self.process = None

        self.finished.emit()