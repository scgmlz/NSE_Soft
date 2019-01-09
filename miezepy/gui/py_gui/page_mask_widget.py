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
from PyQt5.QtWidgets import QInputDialog

#private dependencies
from ..qt_gui.main_mask_editor_ui   import Ui_mask_editor
from ...gui.py_gui.dialog           import dialog 
from ...gui.py_gui.mask_widget      import MaskWidget 

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

    def initialize(self):
        '''
        Reset all the inputs and all the fields
        present in the current view.
        '''
        self.mask_elements  = []
        self.mask_widgets   = []
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
        self.updateSelector()
        self.populateAll()

    def connect(self):
        '''
        Connect the interactive elements to their
        respective methods.
        '''
        self.mask_button_add.clicked.connect(self.addElement)
        self.mask_button_remove.clicked.connect(self.removeElement)

    def updateSelector(self, default = None):
        '''
        The selector in the top of the window allows to 
        switch between lists and therefore needs to 
        be updated with the content
        '''
        try:
            self.comboBox.currentIndexChanged.disconnect(self.updateSelection)
        except:
            pass
        keys = [key for key in self.mask_core.mask_dict.keys()]
        self.comboBox.clear()
        self.comboBox.addItems(keys + ['new ...'])
        if not default == None:
            self.comboBox.setCurrentIndex(keys.index(default))
        self.comboBox.currentIndexChanged.connect(self.updateSelection)

    def updateSelection(self, idx):
        '''
        Tell the mask class that we switched element.
        '''
        keys = [key for key in self.mask_core.mask_dict.keys()]

        if idx < len(keys):
            key = keys[idx]
            self.mask_core.setMask(key)
            self.populateAll()

        else:
            text, ok = QInputDialog.getText(self.local_widget, 'New mask name', 'Enter the new mask:')
            if ok:
                self.mask_core.addMask(text)
                keys = [key for key in self.mask_core.mask_dict.keys()]
                self.updateSelector(default = text)
                self.populateAll()

    def addElement(self):
        '''
        Add an element into the list which is loaded 
        from a custom widget.
        '''
        self.mask_core.addElement([
            'arc',
            (31,35),
            50, 
            (0,5), 
            (0,360)])
        self.refreshList()
        self.resetAndSend()

    def removeElement(self):
        '''
        Add an element into the list which is loaded 
        from a custom widget.
        '''
        idx = self.mask_list_loaded.currentRow()
        del self.mask_core.mask_dict[self.mask_core.current_mask][idx]

        self.refreshList()
        self.resetAndSend()

    def refreshList(self):
        '''
        refresh and rebuild the view
        '''
        self.mask_elements  = []
        self.mask_widgets   = []

        self.mask_list_loaded.reset()
        self.mask_list_loaded.clear()

        for element in self.mask_core.mask_dict[self.mask_core.current_mask]:
            self.mask_widgets.append(
                QtWidgets.QListWidgetItem(self.mask_list_loaded))
            self.mask_elements.append(MaskWidget(
                element,
                self.mask_widgets[-1]))

        for element, widget in zip(self.mask_elements, self.mask_widgets):
            self.mask_list_loaded.addItem(widget)
            self.mask_list_loaded.setItemWidget(
                widget,
                element.widget)

            element.mask_edited.connect(self.parseAndSend)
            element.mask_reset.connect(self.resetAndSend)

    def clear(self):
        '''
        Clear the current element list
        '''
        self.mask_list_loaded.clear()
        self.elements = []

    def populateAll(self):
        '''
        '''
        self.clear()
        self.mask_core.sendToGenerator()
        self.mask_core.generateMask(
            int(self.mask_input_x.text()), 
            int(self.mask_input_y.text()))
        self.updateGraph()
        self.refreshList()

    def parseAndSend(self):
        '''
        This routine will simply grab the parameters of each of the 
        mask widgets and parse it to the linked mask class
        '''
        parsed_array = []

        for element in self.mask_elements:
            parsed_array.append(element.parameters)

        self.mask_core.mask_dict[self.mask_core.current_mask] = parsed_array
        self.mask_core.sendToGenerator(recreate = False)
        self.mask_core.generateMask(
            int(self.mask_input_x.text()), 
            int(self.mask_input_y.text()))
        self.updateGraph()

    def resetAndSend(self):
        '''
        This routine will simply grab the parameters of each of the 
        mask widgets and parse it to the linked mask class
        '''
        self.mask_core.mask_dict[self.mask_core.current_mask] = []
        for element in self.mask_elements:
            self.mask_core.addElement(element.parameters)
            print(element.parameters)
        self.mask_core.sendToGenerator(recreate = True)
        self.mask_core.generateMask(
            int(self.mask_input_x.text()), 
            int(self.mask_input_y.text()))
        self.updateGraph()

    def updateGraph(self):
        '''
        '''
        data = self.mask_core.mask_gen.mask

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
        
    def saveSingle(self):
        '''
        
        '''
        filters     = "mask_save.txt"
        file_path   = QtWidgets.QFileDialog.getSaveFileName(
                self.parent.window, 
                'Select file',
                filters)[0]

        if not file_path == '':
            self.mask_core.saveSingleMask(file_path)

    def saveMultiple(self):
        '''
        
        '''
        filters     = "masks_save.txt"
        file_path   = QtWidgets.QFileDialog.getSaveFileName(
                self.parent.window, 
                'Select file',
                filters)[0]

        if not file_path == '':
            self.mask_core.saveAllMasks(file_path)

    def loadSingle(self):
        '''
        
        '''
        filters = "*.txt"

        file_path = QtWidgets.QFileDialog.getOpenFileName(
                self.parent.window, 
                'Select file',
                filters)[0]

        if not file_path == '':
            self.mask_core.loadSingleMask(file_path)
            self.updateSelector(self.mask_core.current_mask)
            self.populateAll()

    def loadMultiple(self):
        '''
        
        '''
        filters = "*.txt"

        file_path = QtWidgets.QFileDialog.getOpenFileName(
                self.parent.window, 
                'Select file',
                filters)[0]

        if not file_path == '':
            self.mask_core.loadAllMasks(file_path)
            self.updateSelector(self.mask_core.current_mask)
            self.populateAll()

