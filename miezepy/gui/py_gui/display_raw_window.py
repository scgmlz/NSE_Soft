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

#private dependencies
from ...gui.qt_gui.display_data_raw_ui import Ui_raw_display

#private plotting library
from simpleplot.multi_canvas import Multi_Canvas


class DisplayRawWindowLayout(Ui_raw_display):
    '''
    ##############################################
    This class will manage the raw import 
    machinery. the UI is inherited through 
    Ui_main_window from the Qt designer anf then
    converted through pyuic5
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    def __init__(self, window, window_manager):

        ##############################################
        #Local pointers
        Ui_raw_display.__init__(self)

        self.window_manager = window_manager
        self.window         = window
        self.setup()
        self.connect()

    def setup(self):
        '''
        ##############################################
        This is the initial setup method that will 
        build the layout and introduce the graphics
        area
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.setupUi(self.window)

        self.mycanvas    = Multi_Canvas(
            self.graph_widget,
            grid        = [[True]],
            x_ratios    = [1],
            y_ratios    = [1],
            background  = "w",
            highlightthickness = 0)

        self.ax = self.mycanvas.get_subplot(0,0)
        self.ax.pointer['Sticky'] = 3

        self.mycanvas.canvas_objects[0][0][0].grid_layout.setMargin(0)

    def link(self, import_object):
        '''
        ##############################################
        This routine will link to the io manager class
        from the core. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.import_object = import_object
        self.initialize()

    def initialize(self):
        '''
        ##############################################
        This routine will link to the io manager class
        from the core. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.echo_drop.addItems(
            [str(e) for e in self.import_object.meta_handler.values['Echo']])
        self.foil_spin.setMinimum(0)
        self.foil_spin.setMaximum(
            self.import_object.data_handler.dimension[0] - 1)
        self.time_spin.setMinimum(0)
        self.time_spin.setMaximum(
            self.import_object.data_handler.dimension[1] - 1)
        
        self.connect()

    def connect(self):
        '''
        ##############################################
        This routine will link to the io manager class
        from the core. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.foil_spin.valueChanged.connect(self.draw)
        self.time_spin.valueChanged.connect(self.draw)
        self.echo_drop.currentIndexChanged.connect(self.draw)

    def draw(self, stuff = None):
        '''
        ##############################################
        
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        data = self.import_object.file_handler.getElement([
            self.echo_drop.currentIndex(),
            self.foil_spin.value(),
            self.time_spin.value()])

        try:
            self.ax.clear()
        except:
            pass

        self.ax.add_plot(
            'Bin', 
            [ i for i in range(data.shape[0])], 
            [ i for i in range(data.shape[1])], 
            data, Name = 'bin' )

        self.ax.redraw()