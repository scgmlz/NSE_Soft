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
from ...qt_gui.display_data_raw_ui import Ui_raw_display

#private plotting library
from simpleplot.canvas.multi_canvas import MultiCanvasItem

class DisplayRawWindowLayout(Ui_raw_display):
    '''
    This class will manage the raw import 
    machinery. the UI is inherited through 
    Ui_main_window from the Qt designer anf then
    converted through pyuic5
    '''
    def __init__(self, window, window_manager):

        ##############################################
        #Local pointers
        Ui_raw_display.__init__(self)

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

        # self.ax = self.my_canvas.getSubplot(0,0)
        # self.ax.pointer.pointer_handler['Sticky'] = 3
        # self.my_canvas.canvas_nodes[0][0][0].grid_layout.setMargin(0)
        

    def link(self, import_object, mode = '3D'):
        '''
        This routine will link to the io manager class
        from the core. 
        '''
        self._mode = mode
        self.import_object = import_object
        self.initialize()
        self.connect()

    def initialize(self):
        '''
        This routine will link to the io manager class
        from the core. 
        '''
        self.echo_drop.addItems(
            [str(e) for e in self.import_object.meta_handler.values['Echo']])
        self.foil_spin.setMinimum(0)
        self.foil_spin.setMaximum(
            self.import_object.data_handler.dimension[0] - 1)
        self.time_spin.setMinimum(0)
        self.time_spin.setMaximum(
            self.import_object.data_handler.dimension[1] - 1)

        if self._mode == '3D':
            self.time_spin.show()
            self.time_check.show()
            self.ax = self.my_canvas.getSubplot(0,0)
            self.plot = self.ax.addPlot('Surface', Name = 'Surface' )
            
        elif self._mode == '4D':
            self.time_spin.hide()
            self.time_check.hide()
            self.my_canvas.canvas_nodes[0][0][0].handler['Type'] = '3D'
            self.ax = self.my_canvas.getSubplot(0,0)
            self.plot = self.ax.addPlot('Volume', Name = 'Volume' )

        self.ax.draw()
        self.draw()
        self.connect()

    def connect(self):
        '''
        This routine will link to the io manager class
        from the core. 
        '''
        self.foil_spin.valueChanged.connect(self.draw)
        self.time_spin.valueChanged.connect(self.draw)
        self.echo_drop.currentIndexChanged.connect(self.draw)
        self.foil_check.stateChanged.connect(self.draw)
        self.time_check.stateChanged.connect(self.draw)
        self.log_check.stateChanged.connect(self.draw)
        self.norm_check.stateChanged.connect(self.draw)

    def draw(self, stuff = None):
        '''
        '''
        data = self.import_object.file_handler.getElement(self.echo_drop.currentIndex())

        if self.foil_check.isChecked():
            data = np.sum(data, axis = 0)
        else:
            data = data[self.foil_spin.value()]

        if self._mode == '4D':
            data = data
        elif self.time_check.isChecked():
            data = np.sum(data, axis = 0)
        else:
            data = data[self.time_spin.value()]

        if self.log_check.isChecked():
            data = np.log10(data+1)
        
        if self.norm_check.isChecked():
            data_min = np.amin(data)
            data_max = np.amax(data)
            data = (data - data_min)/(data_max - data_min) * 10.

        if self._mode == '3D':
            self.plot.setData(
                x = np.array([ i for i in range(data.shape[0])]), 
                y = np.array([ i for i in range(data.shape[1])]), 
                z = data)
        elif self._mode == '4D':
            self.plot.setData(
                x = np.array([ i for i in range(data.shape[0])], dtype = np.float)/5, 
                y = np.array([ j for j in range(data.shape[1])], dtype = np.float)/10., 
                z = np.array([ k for k in range(data.shape[2])], dtype = np.float)/10,
                data = np.array(data, dtype=np.float64))
