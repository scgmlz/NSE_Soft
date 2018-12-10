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
from ..qt_gui.main_data_import_ui       import Ui_data_import
from ...gui.py_gui.loaded_data_widget   import LoadedDataWidget
from ...gui.py_gui.meta_widget          import MetaWidget 
from ...gui.py_gui.dialog               import dialog 
from ...gui.py_gui.drag_drop_file       import DropListView 

#private plotting library
from simpleplot.multi_canvas import Multi_Canvas

class PageDataWidget(Ui_data_import):
    
    def __init__(self, stack, parent):
    
        Ui_data_import.__init__(self)
        self.parent         = parent
        self.stack          = stack
        self.local_widget   = QtWidgets.QWidget() 
        self.setupUi(self.local_widget)
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

        ##############################################
        #add the file drop
        self.data_list_files = DropListView(self.data_group_dialog, 'tof_file_drop')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_list_files.sizePolicy().hasHeightForWidth())
        self.data_list_files.setSizePolicy(sizePolicy)
        self.data_list_files.setMinimumSize(QtCore.QSize(0, 30))
        self.data_list_files.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.data_list_files.setObjectName("data_list_files")
        self.add_custome_file.addWidget(self.data_list_files)

        ##############################################
        #add the file drop
        self.data_list_loaded.setStyleSheet(
            "QListWidget::item { border: 2px solid black ;background-color: palette(Midlight) }"
            "QListWidget::item:selected { background-color: palette(Mid)  }")

        ##############################################
        #add the 
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
        #connect buttons
        self.data_button_meta_add.clicked.connect(self.openMetadataWindow)
        self.data_button_meta_remove.clicked.connect(self.removeMeta)
        self.data_button_meta_all.clicked.connect(self.propagateMeta)
        self.data_button_files_add.clicked.connect(self.getFiles)
        self.data_button_files_reset.clicked.connect(self.resetFiles)
        self.data_button_populate.clicked.connect(self.populate)
        self.data_button_files_remove.clicked.connect(self.removeFile)

        #connect lists
        self.data_list_files.clicked.connect(self.setPrev)
        self.data_list_files.drop_success.connect(self.addFiles)
        self.data_list_loaded.currentItemChanged.connect(self.setCurrentElement)

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
        if len(self.elements) == 0:
            dialog(
                icon = 'error', 
                title= 'No data element set',
                message = 'No data element initialised. Add one first...',
                add_message='You can add a dataset by going to File>add element.')

        else:
            self.parent.window_manager.newWindow('MetaWindow')
            self.parent.window_manager.active_windows['MetaWindow'].target.link(self.meta_handler)

    def openVisualWindow(self):
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
        self.parent.window_manager.newWindow('RawVisual')
        self.parent.window_manager.active_windows['RawVisual'].target.link(self.import_object)

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
        from a custom widget
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
        self.elements[-1][1].vis_button.clicked.connect(self.openVisualWindow)

        self.data_list_loaded.setItemWidget(
            self.elements[-1][0],
            self.elements[-1][1].widget)

        self.setCurrentElement(len(self.io_core.import_objects)-1)

    def addElementSilent(self,i):
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

        self.elements.append([
            QtWidgets.QListWidgetItem(self.data_list_loaded),
            LoadedDataWidget(self.io_core.import_objects[i].data_handler) 
            ])

        self.elements[-1][0].setSizeHint(self.elements[-1][1].widget.size())
        self.elements[-1][1].vis_button.clicked.connect(self.openVisualWindow)

        self.data_list_loaded.setItemWidget(
            self.elements[-1][0],
            self.elements[-1][1].widget)

        self.setCurrentElement(i)

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
        from a custom widget
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
        if len(self.elements) == 0:
            dialog(
            icon = 'error', 
            title= 'No data element set',
            message = 'No data element initialised. Add one first...',
            add_message='You can add a dataset by going to File>add element.')

        else:
            filter      = "All (*);; TOF (*.tof);;PAD (*.pad)"
            file_name   = QtWidgets.QFileDialog()
            file_name.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            names       = file_name.getOpenFileNames(
                self.parent.window,
                'Select files ...',
                '',
                filter)
            self.addFiles(names[0])


    def addFiles(self, filenames):
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
        self.file_handler.addFiles(filenames)
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

    def removeFile(self):
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
        self.file_handler.removeFile(self.data_list_files.currentIndex().row())
        self.setFileList()
        
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

    def populateAll(self):
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
        self.parent.setActivity(
            "Populating data", 
            0, 
            len(self.io_core.import_objects))
        
        for i in range(len(self.io_core.import_objects)):
            self.parent.setProgress("Adding element "+str(i+1), i+1)
            self.addElementSilent(i)
            self.parent.setProgress("Populating element "+str(i+1), i+1)
            self.populate()
            
        self.parent.fadeActivity()

    def generateDataset(self):
        '''
        ##############################################
        This routine will call the generator for the 
        currently active object.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.io_core.generate()
        self.parent.widgetClasses[0].refreshData()

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
                self.parent.window, 
                'Select file',
                filters)[0]
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
                self.parent.window, 
                'Select file',
                filters)[0]
        self.clear()
        self.io_core.loadFromPython(file_path, self)
        
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
