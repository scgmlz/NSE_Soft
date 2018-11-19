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
from ...gui.qt_gui.data_import_ui       import Ui_import_window
from ...gui.py_gui.loaded_data_widget   import LoadedDataWidget
from ...gui.py_gui.meta_widget          import MetaWidget 

#private plotting library
from simpleplot.multi_canvas import Multi_Canvas


class ImportWindowLayout(Ui_import_window):
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
        Ui_import_window.__init__(self)

        self.window_manager = window_manager
        self.window         = window
        self.setup()
        self.connect()

        self.elements       = []
        self.meta_elements  = []

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

        self.data_list_loaded.setStyleSheet(
            "QListWidget::item { border: 2px solid black ;background-color: palette(Midlight) }"
            "QListWidget::item:selected { background-color: palette(Mid)  }")

        self.mycanvas    = Multi_Canvas(
            self.data_widget_graph,
            grid        = [[True]],
            x_ratios    = [1],
            y_ratios    = [1],
            background  = "w",
            highlightthickness = 0)

        self.ax = self.mycanvas.get_subplot(0,0)
        self.ax.pointer['Sticky'] = 3

        self.mycanvas.canvas_objects[0][0][0].grid_layout.setMargin(0)

    def link(self, io_core):
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
        self.io_core = io_core

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
        self.data_button_meta_add.clicked.connect(self.openMetadataWindow)
        self.data_button_meta_remove.clicked.connect(self.removeMeta)
        self.data_button_meta_all.clicked.connect(self.propagateMeta)
        self.data_button_files_add.clicked.connect(self.getFiles)
        self.data_button_files_reset.clicked.connect(self.resetFiles)
        self.data_list_files.clicked.connect(self.setPrev)
        self.data_list_loaded.currentItemChanged.connect(self.setCurrentElement)
        self.data_button_populate.clicked.connect(self.populate)
        #self.data_button_generate.clicked.connect(self.generate)
        self.actionSave.triggered.connect(self.save)
        self.actionLoad.triggered.connect(self.load)
        self.actionAdd_Element.triggered.connect(self.addElement)
        self.actionRemove_Element.triggered.connect(self.removeElement)

        #the dimension fields
        self.data_input_foils.textChanged.connect(self.dimChanged)
        self.data_input_time_channel.textChanged.connect(self.dimChanged)
        self.data_input_pix_x.textChanged.connect(self.dimChanged)
        self.data_input_pix_y.textChanged.connect(self.dimChanged)
        
    def openMetadataWindow(self):
        '''
        ##############################################
        This routine will launch the metadat window.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.window_manager.newWindow('MetaWindow')
        self.window_manager.active_windows['MetaWindow'].target.link(self.meta_handler)

    def removeMeta(self):
        '''
        ##############################################
        This routine will remove an element of the
        selected meta.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        index = self.data_list_meta.currentRow()
        self.meta_handler.removeElement(index)
        self.setMetaList()

    def propagateMeta(self):
        '''
        ##############################################
        This routine will simply propagate the
        current meta information to all other meta 
        windows.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        for element in self.io_core.import_objects:
            element.meta_handler = copy.deepcopy(self.meta_handler)

    def setCurrentElement(self, row = None):
        '''
        ##############################################
        On clicking an element the system will set the
        classes linked to the current element 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if isinstance(row, int):
            index = row
        else:
            index = self.data_list_loaded.currentRow()

        self.import_object      = self.io_core.import_objects[index]
        self.file_handler       = self.io_core.import_objects[index].file_handler
        self.meta_handler       = self.io_core.import_objects[index].meta_handler
        self.data_handler       = self.io_core.import_objects[index].data_handler
        self.current_element    = self.elements[index][1]

        self.setFileList()
        self.setMetaList()
        self.setDimInputs()

    def addElement(self):
        '''
        ##############################################
        Add an element into the list which is loaded 
        from a custome widget
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.io_core.addObject()

        self.elements.append([
            QtWidgets.QListWidgetItem(self.data_list_loaded),
            LoadedDataWidget(self.io_core.import_objects[-1].data_handler) 
            ])

        self.elements[-1][0].setSizeHint(self.elements[-1][1].widget.size())

        self.data_list_loaded.setItemWidget(
            self.elements[-1][0],
            self.elements[-1][1].widget)

        self.setCurrentElement(len(self.io_core.import_objects)-1)

    def removeElement(self):
        '''
        ##############################################
        Remove an element from the curren dataset
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        row = self.data_list_loaded.currentRow()
        item = self.data_list_loaded.takeItem(self.data_list_loaded.currentRow())
        item = None
        del self.io_core.import_objects[row]

    def clear(self):
        '''
        ##############################################
        Add an element into the list which is loaded 
        from a custome widget
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.data_list_loaded.clear()
        self.elements = []

    def setMetaList(self):
        '''
        ##############################################
        grabs the information from the initial meta 
        container in the core and then produces the 
        adequat list.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.clearMeta()

        for i in range(len(self.meta_handler.selected_meta)):
            self.addMetaElement()
            self.meta_elements[-1][1].setParentList(
                self.meta_handler.selected_meta[i])
            self.meta_elements[-1][1].edited.connect(self.meta_handler.editValue)
            
    def addMetaElement(self):
        '''
        ##############################################
        Add an element into the list which is loaded 
        from a custome widget
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.meta_elements.append([
            QtWidgets.QListWidgetItem(self.data_list_meta),
            MetaWidget()
            ])

        self.meta_elements[-1][0].setSizeHint(self.meta_elements[-1][1].widget.size())

        self.data_list_meta.setItemWidget(
            self.meta_elements[-1][0],
            self.meta_elements[-1][1].widget)

    def clearMeta(self):
        '''
        ##############################################
        Add an element into the list which is loaded 
        from a custome widget
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.data_list_meta.clear()
        self.meta_elements = []

    def getFiles(self):
        '''
        ##############################################
        Add an element into the list which is loaded 
        from a custome widget
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        filter      = "All (*);; TOF (*.tof);;PAD (*.pad)"
        file_name   = QtWidgets.QFileDialog()
        file_name.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        names       = file_name.getOpenFileNames(
            self.window,
            'Select files ...',
            '',
            filter)

        self.file_handler.addFiles(names[0])
        self.setFileList()

    def setFileList(self):
        '''
        ##############################################
        This will be the loading of files to the 
        io file handler class
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.file_model = QtGui.QStandardItemModel()

        for element in self.file_handler.nice_path_files:

            item = QtGui.QStandardItem(element)
            self.file_model.appendRow(item)
    
        self.data_list_files.setModel(self.file_model)
        
    def resetFiles(self):
        '''
        ##############################################
        This will reset the file view and the 
        associated core io routine.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.file_handler.initialize()
        self.setFileList()

    def setPrev(self, index):
        '''
        ##############################################
        This will generate the preview of the dataset
        selected in the current file view
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if not len(self.file_handler.total_path_files) == 0:
            self.file_handler.genPrev(index.row())
            self.displayPrev()

    def displayPrev(self):
        '''
        ##############################################
        This routine will display the preview of the
        selected dataset processed by setPrev 
        beforehand.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        try:
            self.ax.clear()
        except:
            pass

        self.ax.add_plot(
            'Bin', 
            [ i for i in range(self.file_handler.current_preview.shape[0])], 
            [ i for i in range(self.file_handler.current_preview.shape[1])], 
            self.file_handler.current_preview, Name = 'bin' )

        self.ax.redraw()

    def populate(self):
        '''
        ##############################################
        This routine will call the genrator for the 
        currently active object.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.import_object.processObject()
        self.current_element.setMeta(
            self.meta_handler.values,
            self.file_handler.nice_path_files)
        self.current_element.initialize()

    def save(self):
        '''
        ##############################################
        This will launch the save file of the io
        class
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        filters = "mieze_save.py"

        file_path = QtWidgets.QFileDialog.getSaveFileName(
                self.window, 
                'Select file',
                filters)[0]

        self.focusWindow()
        self.io_core.saveToPython(file_path)
        
    def load(self):
        '''
        ##############################################
        This will launch the save file of the io
        class
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        filters = "*.py"

        file_path = QtWidgets.QFileDialog.getOpenFileName(
                self.window, 
                'Select file',
                filters)[0]
        self.focusWindow()
        self.clear()
        self.io_core.load(file_path, self)
        
    def dimChanged(self):
        '''
        ##############################################
        This will launch the save file of the io
        class
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        dim = [
            int(self.data_input_foils.text()),
            int(self.data_input_time_channel.text()),
            int(self.data_input_pix_x.text()),
            int(self.data_input_pix_y.text())]

        self.data_handler.dimension = list(dim)
        
    def setDimInputs(self):
        '''
        ##############################################
        This routine will simply propagate the
        current meta information to all other meta 
        windows.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.data_input_foils.setText(str(self.data_handler.dimension[0]))
        self.data_input_time_channel.setText(str(self.data_handler.dimension[1]))
        self.data_input_pix_x.setText(str(self.data_handler.dimension[2]))
        self.data_input_pix_y.setText(str(self.data_handler.dimension[3]))

    def focusWindow(self):
        '''
        ##############################################
        This routine will simply propagate the
        current meta information to all other meta 
        windows.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.window.raise_()
        self.window.activateWindow()
        