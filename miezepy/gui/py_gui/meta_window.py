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
import sys
import os
from scipy.ndimage import imread

from ..qt_gui.metadata_window_ui import Ui_select_meta 

class MetadataWindowLayout(Ui_select_meta):
    '''
    ##############################################
    This is the main window element that will later
    be the item managin the rest of the system. 
    Note that at a later point we will feature
    drag and drop onto this window.
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    def __init__(self, window, window_manager):

        #set up the window
        Ui_select_meta.__init__(self)
        self.window = window
        self.setupUi(window)
        self.window_manager = window_manager
        self.connect()

    def connect(self):
        '''
        ##############################################
        connect the actions to their respective buttons
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.meta_button_select.clicked.connect(self.grabFile) 
        self.meta_input_select.textChanged.connect(self.scanFile)
        self.meta_input_filter.textChanged.connect(self.setList)
        self.meta_button_accept.clicked.connect(self.accept)
        self.meta_button_cancel.clicked.connect(self.cancel)
        self.meta_button_reset.clicked.connect(self.reset)

    def link(self, meta_class):
        '''
        ##############################################
        link the class that will mnage the current 
        input output.
        ———————
        Input: 
        - meta_class is the metadata class from the io
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.meta_class = meta_class 
        self.initialize()

    def initialize(self):
        '''
        ##############################################
        This method checks if the data has been set
        in a previous instance.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if not self.meta_class.path == '':
            self.meta_input_select.setText(self.meta_class.path)
            self.scanFile()
            self.meta_class.checkPresence()
            self.setList()

    def grabFile(self):
        '''
        ##############################################
        Open a folder and set the path and then scan 
        it automatically on path change.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        file = QtWidgets.QFileDialog.getOpenFileName(
                self.window, 
                'Select directory')
                
        self.meta_input_select.setText(file[0])

    def scanFile(self):
        '''
        ##############################################
        check if thgis is a file and then send the path
        to the respective manager.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if os.path.isfile(self.meta_input_select.text()):
            self.meta_class.buildMeta(
                self.meta_input_select.text())

            self.setList()

    def setList(self):
        '''
        ##############################################
        This will generate the list view for the
        respective list.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        filter_value = self.meta_input_filter.text()

        self.model = QtGui.QStandardItemModel()
        self.index = []

        for element in self.meta_class.metadata_temp:

            if filter_value in element[1] or filter_value == '':

                item = QtGui.QStandardItem(element[1]+" ("+element[2]+")")
                item.setFlags(
                    QtCore.Qt.ItemIsUserCheckable 
                    | QtCore.Qt.ItemIsEnabled)
                check = QtCore.Qt.Checked if element[0] else QtCore.Qt.Unchecked
                item.setData(
                    QtCore.QVariant(check), 
                    QtCore.Qt.CheckStateRole)
                self.model.appendRow(item)
                self.index.append(element[1])
    
        self.meta_list_list.setModel(self.model)
        self.model.itemChanged.connect(self.onChecked)

    def onChecked(self, index):
        '''
        ##############################################
        When an item is checked the boolena value has
        to be modified in the correct element
        ———————
        Input: 
        - index is the line in which this change
        happened
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        item = self.model.item(index.row())
        if item.checkState() == QtCore.Qt.Checked:
            checked = True
        else:
            checked = False

        self.meta_class.flipBool(self.index[index.row()], checked)

    def accept(self):
        '''
        ##############################################
        When an item is checked the boolena value has
        to be modified in the correct element
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.meta_class.setMeta()
        self.window.parent.setWindowState(
            self.window.parent.windowState() & ~QtCore.Qt.WindowMinimized 
            | QtCore.Qt.WindowActive)
        self.window.parent.activateWindow()
        self.window.parent.target.widgetClasses[1].setMetaList()
        self.window.close()

    def cancel(self):
        '''
        ##############################################
        When an item is checked the boolena value has
        to be modified in the correct element
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.window.parent.setWindowState(
            self.window.parent.windowState() & ~QtCore.Qt.WindowMinimized 
            | QtCore.Qt.WindowActive)
        self.window.parent.activateWindow()
        self.window.close()

    def reset(self):
        '''
        ##############################################
        When an item is checked the boolena value has
        to be modified in the correct element
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.meta_class.reset()
        self.scanFile()
        self.window.parent.target.widgetClasses[1].setMetaList()
