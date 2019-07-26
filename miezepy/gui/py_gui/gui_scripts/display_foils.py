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


#public dependencies
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import os
import copy
import numpy as np

#private dependencies
from ...qt_gui.display_foils_ui import Ui_foil_display

#private plotting library
from simpleplot.canvas.multi_canvas import MultiCanvasItem

class DisplayFoilWindowLayout(Ui_foil_display):
    '''
    This class will manage the raw import 
    machinery. the UI is inherited through 
    Ui_main_window from the Qt designer anf then
    converted through pyuic5
    '''
    def __init__(self, window, window_manager):

        Ui_foil_display.__init__(self)
        self.window_manager = window_manager
        self.window         = window
        self.setup()
        
    def setup(self):
        '''
        This is the initial setup method that will 
        build the layout and introduce the graphics
        area
        '''
        self.setupUi(self.window)

        self.my_canvas    = MultiCanvasItem(
            self.graph_widget,
            grid        = [[True]],
            x_ratios    = [1],
            y_ratios    = [1],
            background  = "w",
            highlightthickness = 0)

        ax = self.my_canvas.getSubplot(0,0)
        ax.pointer.pointer_handler['Sticky'] = 2

    def link(self, instrument):
        '''
        This routine will link to the io manager class
        from the core. 
        '''
        self._instrument = instrument
        self.foil_detector_label.setText(
            self._instrument.detector.identifier + ' ('
            +self._instrument.detector.current_date +')')
        self.initialize()
        self.connect()

    def initialize(self):
        '''
        This routine will link to the io manager class
        from the core. 
        '''

        self.foil_spin.setMinimum(0)
        self.foil_spin.setMaximum(self._instrument.detector.foil_array.shape[0]-1)

        self.ax     = self.my_canvas.getSubplot(0,0)
        self.plot   = self.ax.addPlot('Surface', Name = 'Surface' )
        histogram   = self.plot.childFromName('Surface').childFromName('Shader').getHistogramItem()
        self.ax.addItem('right', histogram)
        self.ax.draw()
        self.draw()
        self.connect()

    def connect(self):
        '''
        This routine will link to the io manager class
        from the core. 
        '''
        self.foil_spin.valueChanged.connect(self.draw)
        self.foil_factor_spin.valueChanged.connect(self.draw)

    def draw(self):
        '''
        '''
        data = self._instrument.detector.foil_array[self.foil_spin.value()]*self.foil_factor_spin.value()

        self.plot.setData(
            x = np.array([ i for i in range(data.shape[0])]), 
            y = np.array([ i for i in range(data.shape[1])]), 
            z = data)
