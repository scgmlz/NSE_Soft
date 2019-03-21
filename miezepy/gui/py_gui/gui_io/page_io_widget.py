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
import os

from ...qt_gui.main_io_widget_ui    import Ui_io_widget
from .tree_class                    import *

class PageIOWidget(Ui_io_widget):
    
    def __init__(self, stack, parent):
        Ui_io_widget.__init__(self)
        self.parent         = parent
        self.stack          = stack
        self.local_widget   = QtWidgets.QWidget() 
        self.extra_folders  = []
        self.setupUi(self.local_widget)
        self.connect()

    def connect(self):
        '''
        connect the actions to their respective buttons
        '''
        self.io_button_load_path.clicked.connect(self.getLoadPath)
        self.io_button_save_path.clicked.connect(self.getSavePath)
        self.io_button_save.clicked.connect(self.save)
        self.io_button_load.clicked.connect(self.load)

        self.io_check_save_data.stateChanged.connect(self.triggerNodeSave)
        self.io_check_save_mask.stateChanged.connect(self.triggerNodeSave)
        self.io_check_save_scripts.stateChanged.connect(self.triggerNodeSave)

        self.io_check_load_data.stateChanged.connect(self.triggerNodeLoad)
        self.io_check_load_mask.stateChanged.connect(self.triggerNodeLoad)
        self.io_check_load_scripts.stateChanged.connect(self.triggerNodeLoad)

        self.io_button_add.clicked.connect(self.addFolderElement)
        self.io_button_remove.clicked.connect(self.removeFolderElement)

    def getLoadPath(self, quick = False):
        '''
        connect the actions to their respective buttons
        '''
        file_path = QtWidgets.QFileDialog.getExistingDirectory(
                self.parent.window, 
                'Select folder')

        self.io_input_load_path.setText(os.path.abspath(file_path))
        self.triggerNodeLoad()

        if quick:
            self.load()

    def triggerNodeLoad(self):
        '''
        This function will be triggered as the load
        field is changed or one of the checkboxes
        is changed.
        '''
        self.parseNodesLoad(
            self.io_input_load_path.text(),
            self.io_check_load_data.isChecked(),
            self.io_check_load_mask.isChecked(),
            self.io_check_load_scripts.isChecked()
        )

    def parseNodesLoad(self, root, data_bool, masks_bool, scripts_bool):
        '''
        This will tell the core manger to prepare for
        an import and then build the corresponding 
        tree.
        '''
        prep_list = self.handler.prepSessionLoad(
            root, data_bool, masks_bool, 
            scripts_bool, list(self.extra_folders))
        
        root_node       = Node("Root")
        env_nodes       = []
        data_nodes      = []
        mask_nodes      = []
        script_nodes    = []

        for i,element in enumerate(prep_list[0]):
            name = element.split(os.path.sep)[-2]

            env_nodes.append([
                name, 
                EnvNode(name, root_node)])

            if not prep_list[1][i]  == None:
                data_nodes.append([
                    name+'_data',
                    DataNode(name+'_data', env_nodes[i][1])
                ])

            if not prep_list[1][i] == None:
                data_nodes.append([
                    name+'_mask',
                    DataNode(name+'_mask', env_nodes[i][1])
                ])

            if not prep_list[1][i]  == None:
                data_nodes.append([
                    name+'_script',
                    DataNode(name+'_script', env_nodes[i][1])
                ])

        model = FileTreeModel(root_node)
        self.io_tree_load.setModel(model)

    def getSavePath(self, quick = False):
        '''
        '''
        file_path = QtWidgets.QFileDialog.getExistingDirectory(
                self.parent.window, 
                'Select folder')

        self.io_input_save_path.setText(os.path.abspath(file_path))
        self.triggerNodeSave()

        if quick:
            self.save()

    def triggerNodeSave(self):
        '''
        This function will be triggered as the save
        field is changed or one of the checkboxes
        is changed.
        '''
        self.parseNodesSave(
            self.io_input_save_path.text().split(os.path.sep)[-1],
            self.io_check_save_data.isChecked(),
            self.io_check_save_mask.isChecked(),
            self.io_check_save_scripts.isChecked()
        )

    def parseNodesSave(self, root, data_bool, masks_bool, scripts_bool):
        '''
        This will parse the visual nodes of the tree to 
        see what is going to be saved and in later
        releases select the data to be saved.
        '''
        main_handler = self.parent.handler

        root_node       = Node("Root")
        env_nodes       = []
        data_nodes      = []
        mask_nodes      = []
        script_nodes    = []

        names = [env.name for env in  main_handler.env_array]
        for name in names:
            env_nodes.append(
                [name, EnvNode(name, root_node)])

        if data_bool:
            for element in env_nodes:
                data_nodes.append(
                    [element[0]+"_data", DataNode(element[0]+"_data", element[1])])

        if scripts_bool:
            for element in env_nodes:
                    script_nodes.append(
                    [element[0]+"_script", ScriptNode(element[0]+"_script", element[1])])
        if masks_bool:
            for element in env_nodes:
                        script_nodes.append(
                    [element[0]+"_mask", MaskNode(element[0]+"_mask", element[1])])

        model = FileTreeModel(root_node)
        self.io_tree_save.setModel(model)

    def link(self, handler):
        '''
        link the class that will manage the current 
        input output.
        Input: 
        - meta_class is the metadata class from the io
        '''
        self.handler = handler 
        self.setFolderList()

    def initialize(self):
        '''
        '''
        pass

    def save(self):
        '''
        connect the actions to their respective buttons
        '''
        self.handler.saveSession(
            self.io_input_save_path.text(),
            self.io_check_save_data.isChecked(),
            self.io_check_save_mask.isChecked(),
            self.io_check_save_scripts.isChecked())

    def load(self):
        '''
        connect the actions to their respective buttons
        '''
        self.parent.setActivity(
            'Loading session',
            0,
            len(self.handler.prep_load_list[0]))
        outputs = self.handler.sessionLoad(
            self.io_check_load_add.isChecked(),
            main_window = self.parent)

        for output in outputs[0]:
            self.parent.widgetClasses[1].testLoadOutput(output[0], output[1])

        self.parent.fadeActivity()
        self.parent.link(self.handler)
        
    def setFolderList(self):
        '''
        This will be the loading of files to the 
        io file handler class.
        '''
        self.folder_model = QtGui.QStandardItemModel()

        for element in self.extra_folders:
            item = QtGui.QStandardItem(element)
            self.folder_model.appendRow(item)
    
        self.io_list_folders.setModel(self.folder_model)

    def addFolderElement(self):
        '''
        This will allow to add an extra folder element to the 
        handler and then call the rebuild of the array
        '''
        path = QtWidgets.QFileDialog.getExistingDirectory(
                self.parent.window, 
                'Select folder')

        if not path == '':
            self.extra_folders.append(os.path.abspath(path))
        
        self.setFolderList()
        self.triggerNodeLoad()
        
    def removeFolderElement(self):
        '''
        This will allow to remove an extra folder element to the 
        handler and then call the rebuild of the array
        '''
        del self.extra_folders[self.io_list_folders.currentIndex().row()]
        self.setFolderList()
        self.triggerNodeLoad()