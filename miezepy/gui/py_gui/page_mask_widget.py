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
import time

#private dependencies
from ..qt_gui.main_mask_editor_ui      import Ui_mask_editor
# from ...gui.py_gui.loaded_data_widget   import LoadedDataWidget
# from ...gui.py_gui.meta_widget          import MetaWidget 
from ...gui.py_gui.dialog               import dialog 
# from ...gui.py_gui.drag_drop_file       import DropListView 

#private plotting library
from simpleplot.multi_canvas import Multi_Canvas

class PageMaskWidget(Ui_mask_editor):
    
    def __init__(self, stack, parent):
    
        Ui_mask_editor.__init__(self)
        self.parent         = parent
        self.stack          = stack
        self.local_widget   = QtWidgets.QWidget() 
        self.setupUi(self.local_widget)
        self.setup()
        self.connect()
        self.initialize()

        #to be removed
        

    def initialize(self):
        '''
        Reset all the inputs and all the fields
        present in the current view.
        '''
        self.mask_elements  = []
        self.mask_core      = None

        self.mask_list_loaded.reset()
        self.mask_list_loaded.clear()

    def setup(self):
        '''
        This is the initial setup method that will 
        build the layout and introduce the graphics
        area
        '''
        self.my_canvas    = Multi_Canvas(
            self.mask_widget_visual,
            grid        = [[True]],
            x_ratios    = [1],
            y_ratios    = [1],
            background  = "w",
            highlightthickness = 0)

        self.ax = self.my_canvas.get_subplot(0,0)
        self.ax.pointer['Sticky'] = 3
        self.my_canvas.canvas_objects[0][0][0].grid_layout.setMargin(0)

    def link(self, mask_core):
        '''
        This routine will link to the io manager class
        from the core. 
        '''
        self.initialize()
        self.mask_core = mask_core
        self.mask_core.addMask('circular at 50 50')
        self.populateAll()

    def connect(self):
        '''
        Connec the interactive elements to their
        respective methods.
        '''
        self.mask_button_add.clicked.connect(self.addElement)

    def setCurrentElement(self, row = None):
        '''
        On clicking an element the system will set the
        classes linked to the current element 
        '''

    def addElement(self):
        '''
        Add an element into the list which is loaded 
        from a custom widget.
        '''
        self.mask_core.addElement([
            'arc',
            (31,35), 
            (0,5), 
            (0,360)])
        self.refreshList()

    def refreshList(self):
        '''
        refresh and rebuild the view
        '''
        # self.initialize()

        for element in self.mask_core.mask_dict[self.mask_core.current_mask]:
            print(element)

    def clear(self):
        '''
        Clear the current element list
        '''
        self.mask_list_loaded.clear()
        self.elements = []

    def populateAll(self):
        '''
        This routine will call the generator for the 
        currently active object.
        '''
