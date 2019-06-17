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
import numpy as np

#private dependencies
from ...qt_gui.main_data_import_ui  import Ui_data_import
from .loaded_data_widget            import LoadedDataWidget
from .meta_widget                   import MetaWidget 
from ..gui_common.dialog            import dialog 
from .drag_drop_file                import DropListView 

#private plotting library
from simpleplot.canvas.multi_canvas import MultiCanvasItem

class PageDataWidget(Ui_data_import):
    
    def __init__(self, stack, parent):
    
        Ui_data_import.__init__(self)
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
        self.elements       = []
        self.meta_elements  = []
        self.io_core        = None
        self.data_list_files.reset()
        self.data_list_loaded.clear()
        self.data_list_meta.clear()

    def setup(self):
        '''
        This is the initial setup method that will 
        build the layout and introduce the graphics
        area
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
        self.data_list_meta.setStyleSheet(
            "QListWidget::item { border: 2px solid black ;background-color: palette(Midlight) }"
            "QListWidget::item:selected { background-color: palette(Mid)  }")
        ##############################################
        #add the 
        self.my_canvas    = MultiCanvasItem(
            self.data_widget_graph,
            grid        = [[True]],
            x_ratios    = [1],
            y_ratios    = [1],
            background  = "w",
            highlightthickness = 0)

        self.ax = self.my_canvas.getSubplot(0,0)
        self._prev_plot = self.ax.addPlot('Surface',Name = 'Surface')

        self.ax.axes.general_handler['Active'] = [False]*4
        self.ax.pointer.pointer_handler['Sticky'] = 3
        self.my_canvas.canvas_nodes[0][0][0].grid_layout.setMargin(0)
        self.ax.draw()

    def link(self, io_core):
        '''
        This routine will link to the io manager class
        from the core. 
        '''
        self.initialize()
        self.io_core = io_core
        self.populateAll()

    def connect(self):
        '''
        This routine will link to the io manager class
        from the core. 
        '''
        #connect buttons
        self.data_button_meta_add.clicked.connect(self.openMetadataWindow)
        self.data_button_meta_remove.clicked.connect(self.removeMeta)
        self.data_button_meta_all.clicked.connect(self.propagateMeta)
        self.data_button_files_add.clicked.connect(self.getFiles)
        self.data_button_files_reset.clicked.connect(self.resetFiles)
        self.data_button_populate.clicked.connect(self.populate)
        self.data_button_validate.clicked.connect(self.generateDataset)
        self.data_button_files_remove.clicked.connect(self.removeFile)
        self.data_button_prev.clicked.connect(self.hide_preview)
        self.data_button_add_object.clicked.connect(self.addElement)
        self.data_button_remove_object.clicked.connect(self.removeElement)

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
        This routine will launch the metadat window.
        '''
        if len(self.elements) == 0:
            dialog(
                parent = self.local_widget,
                icon = 'error', 
                title= 'No data element set',
                message = 'No data element initialized. Add one first...',
                add_message='You can add a dataset by going to File>add element.')

        else:
            self.parent.window_manager.newWindow('MetaWindow')
            self.parent.window_manager.active_windows['MetaWindow'].target.link(self.meta_handler)

    def hide_preview(self):
        '''
        This routine will launch the metadat window.
        '''
        self.data_widget_graph.setVisible(not self.data_widget_graph.isVisible())

        if self.data_widget_graph.isVisible():
            self.data_button_prev.setText('Hide')
        else:
            self.data_button_prev.setText('Show')

    def openVisualWindow(self):
        '''
        This routine will launch the metadat window.
        '''
        self.parent.window_manager.newWindow('RawVisual')
        self.parent.window_manager.active_windows['RawVisual'].target.link(self.import_object)

    def removeMeta(self):
        '''
        This routine will remove an element of the
        selected meta.
        '''
        index = self.data_list_meta.currentRow()
        self.meta_handler.removeElement(index)
        self.setMetaList()

    def propagateMeta(self):
        '''
        This routine will simply propagate the
        current meta information to all other meta 
        windows.
        '''
        for element in self.io_core.import_objects:
            element.meta_handler = copy.deepcopy(self.meta_handler)

    def setCurrentElement(self, row = None):
        '''
        On clicking an element the system will set the
        classes linked to the current element 
        '''
        if isinstance(row, int):
            index = row
        else:
            index = self.data_list_loaded.currentRow()

        if not self.io_core == None:
            self.import_object      = self.io_core.import_objects[index]
            self.file_handler       = self.io_core.import_objects[index].file_handler
            self.meta_handler       = self.io_core.import_objects[index].meta_handler
            self.data_handler       = self.io_core.import_objects[index].data_handler
            self.current_element    = self.elements[index][1]

            self.setFileList()
            self.setMetaList()
            self.setDimInputs()

            self.elements[index][1].widget.setFocus()

    def addElement(self):
        '''
        Add an element into the list which is loaded 
        from a custom widget.
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
        Add an element into the list which is loaded 
        from a custom widget.
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
        Remove an element from the current dataset
        '''
        row = self.data_list_loaded.currentRow()
        item = self.data_list_loaded.takeItem(self.data_list_loaded.currentRow())
        item = None
        del self.io_core.import_objects[row]

    def clear(self):
        '''
        Clear the current element list
        '''
        self.data_list_loaded.clear()
        self.elements = []

    def setMetaList(self):
        '''
        grabs the information from the initial meta 
        container in the core and then produces the 
        adequate list.
        '''
        self.clearMeta()

        for i in range(len(self.meta_handler.selected_meta)):
            self.addMetaElement()
            self.meta_elements[-1][1].setParentList(
                self.meta_handler.selected_meta[i])
            self.meta_elements[-1][1].edited.connect(self.meta_handler.editValue)
            
    def addMetaElement(self):
        '''

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

        '''
        self.data_list_meta.clear()
        self.meta_elements = []

    def getFiles(self):
        '''

        '''
        if len(self.elements) == 0:
            dialog(
                parent = self.local_widget,
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
        Adding files to the data either through the 
        filedialog or the drag and drop.
        '''
        self.file_handler.addFiles(filenames)
        self.setFileList()

    def setFileList(self):
        '''
        This will be the loading of files to the 
        io file handler class.
        '''
        self.file_model = QtGui.QStandardItemModel()

        for element in self.file_handler.nice_path_files:

            item = QtGui.QStandardItem(element)
            self.file_model.appendRow(item)
    
        self.data_list_files.setModel(self.file_model)

    def removeFile(self):
        '''
        This will reset the file view and the 
        associated core io routine.
        '''
        self.file_handler.removeFile(self.data_list_files.currentIndex().row())
        self.setFileList()
        
    def resetFiles(self):
        '''
        This will reset the file view and the 
        associated core io routine.
        '''
        self.file_handler.initialize()
        self.setFileList()

    def setPrev(self, index):
        '''
        This will generate the preview of the dataset
        selected in the current file view.
        '''
        if not len(self.file_handler.total_path_files) == 0:
            self.file_handler.genPrev(index.row())
            self.displayPrev()

    def displayPrev(self):
        '''
        This routine will display the preview of the
        selected dataset processed by setPrev.
        '''
        self._prev_plot.setData(
            x = np.array([ i for i in range(self.file_handler.current_preview.shape[0])]), 
            y = np.array([ i for i in range(self.file_handler.current_preview.shape[1])]), 
            z = self.file_handler.current_preview )

    def populate(self, warning = True):
        '''
        This routine will call the generator for the 
        currently active object.
        '''
        self.import_object.processObject()
        self.current_element.setMeta(
            self.meta_handler.values,
            self.file_handler.nice_path_files)
        self.current_element.initialize()

        try:
            self.import_object.meta_handler.values['Echo']
        except:
            if warning:
                dialog(
                    parent = self.local_widget,
                    icon = 'error', 
                    title= 'Echo time not processed',
                    message = 'The echo time has not been processed. This is probably due to a lack of deinitions. See details...',
                    add_message='The calculation of the echo time require the presence of the Wavelength, the first and second frequency attributed the the first and second RF coils and finally the lsd distance in between them extracted from the metadata. One or multiple of them are missing. Please rectify.')

    def populateAll(self):
        '''
        This routine will call the generator for the 
        currently active object.
        '''
        self.parent.setActivity(
            "Populating data", 
            0, 
            len(self.io_core.import_objects))
        
        for i in range(len(self.io_core.import_objects)):
            self.parent.setProgress("Adding element "+str(i+1), i+1)
            self.addElementSilent(i)
            self.parent.setProgress("Populating element "+str(i+1), i+1)
            self.populate(warning = False)
            
        self.parent.fadeActivity()

    def generateDataset(self):
        '''
        This routine will call the generator for the 
        currently active object.
        '''
        self.io_core.generate()
        self.parent.widgetClasses[0].refreshData()
        self.parent.widgetClasses[3].link(self.parent.handler.current_env)

    def save(self):
        '''
        This will launch the save file of the io
        class
        '''
        filters = "mieze_save.py"

        file_path = QtWidgets.QFileDialog.getSaveFileName(
                self.parent.window, 
                'Select file',
                filters)[0]
        self.io_core.saveToPython(file_path)
        
    def load(self):
        '''
        This will launch the save file of the io
        class
        '''
        filters = "*.py"

        file_path = QtWidgets.QFileDialog.getOpenFileName(
                self.parent.window, 
                'Select file',
                filters)[0]

        if not file_path == '':
            self.clear()

            output = self.io_core.loadFromPython(file_path, self)

            self.testLoadOutput(output, file_path)

    def testLoadOutput(self, output, file_path):
        '''
        Test the output with the user and  notify him if
        anything went wrong
        '''
        try:
            passed = all([all([subelement[0] for subelement in element]) for element in output])

            if not passed:

                meta_string = []
                folder_string = []

                for element in output:
                    if not element[0][0]:
                        meta_string.append('Invalid meta file location: ' + element[0][1])
                    if not element[1][0]:
                        folder_string.append('Invalid file folder location: ' + element[1][1])
                dialog(
                    parent = self.local_widget,
                    icon = 'warning', 
                    title= 'Could not load all files',
                    message = 'Some files and folders seem to either have moved or not exist. Please rebase them manually in the import file located at:\n'+file_path,
                    det_message = '\n\n'.join(meta_string+folder_string))
        except:
            pass
        
    def dimChanged(self):
        '''
        This will launch the save file of the io
        class
        '''
        dim = [
            int(self.data_input_foils.text()),
            int(self.data_input_time_channel.text()),
            int(self.data_input_pix_x.text()),
            int(self.data_input_pix_y.text())]

        self.data_handler.dimension = list(dim)
        
    def setDimInputs(self):
        '''
        This routine will simply propagate the
        current meta information to all other meta 
        windows.
        '''
        self.data_input_foils.setText(str(self.data_handler.dimension[0]))
        self.data_input_time_channel.setText(str(self.data_handler.dimension[1]))
        self.data_input_pix_x.setText(str(self.data_handler.dimension[2]))
        self.data_input_pix_y.setText(str(self.data_handler.dimension[3]))
