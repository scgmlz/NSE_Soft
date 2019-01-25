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

import operator
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import sys
import os

from ...gui.qt_gui.loaded_data_ui import Ui_dataset_widget

class LoadedDataWidget(Ui_dataset_widget,QtCore.QObject):
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

    def __init__(self, data_handler):

        ##############################################
        #Local pointers
        QtCore.QObject.__init__(self)
        Ui_dataset_widget.__init__(self)
        self.widget = QtWidgets.QWidget()
        self.setupUi(self.widget)
        self.meta_table.resizeColumnsToContents()
        self.data_handler = data_handler
        self.initialize()
        self.connect()

    def initialize(self):
        '''
        ##############################################
        set all the fields after initialising the gui

        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        try:
            self.disconnect()
        except:
            pass

        self.para_input.setText(self.data_handler.parameter)
        self.meas_input.setValue(int(self.data_handler.meas))
        self.ref_radio.setChecked(self.data_handler.reference)
        self.back_radio.setChecked(self.data_handler.background)

        self.connect()


    def setMeta(self,val_dict, file_list):
        '''
        ##############################################
        Process an array of values to set the 
        parameters in the design
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        new_val_dict = dict(val_dict)
        try:
            del new_val_dict['Parameter']
        except:
            pass
        try:
            del new_val_dict['Measurement']
        except:
            pass
        

        self.clearTable()
        self.setTable(new_val_dict, file_list)


    def clearTable(self):
        '''
        ##############################################
        Clears the tble content and makes it ready 
        for new entries
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        pass

    def setTable(self,val_dict, file_list):
        '''
        ##############################################
        Put the elements into the table widget
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.clearTable()
        data_list = [[val_dict[key][i] for key in val_dict.keys()] for i in range(len(file_list))]
        self.header = [key for key in val_dict.keys()]
        self.model = MyTableModel(
            None,
            data_list, 
            self.header, 
            file_list)

        self.meta_table.setModel(self.model)

    def connect(self):
        '''
        ##############################################
        connect
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.para_input.textChanged.connect(self.getValues)
        self.meas_input.valueChanged.connect(self.getValues)
        self.ref_radio.toggled.connect(self.getValues)
        self.back_radio.toggled.connect(self.getValues)

    def disconnect(self):
        '''
        ##############################################
        connect
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.para_input.textChanged.disconnect()
        self.meas_input.valueChanged.disconnect()
        self.ref_radio.toggled.disconnect()
        self.back_radio.toggled.disconnect()

    def getValues(self, index = None):
        '''
        ##############################################
        initialize the widget and set the stage
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        self.data_handler.parameter = self.para_input.text()
        self.data_handler.meas      = str(self.meas_input.value())
        self.data_handler.reference = self.ref_radio.isChecked()
        self.data_handler.background= self.back_radio.isChecked()


#https://stackoverflow.com/questions/19411101/pyside-qtableview-example
class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mylist, col_header,row_header, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.col_header = col_header
        self.row_header = row_header

    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        if len(self.mylist) > 0:
            return len(self.mylist[0])
        else:
            return 0
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.col_header[col]
        elif orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return self.row_header[col]
        else:
            return None
    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))


                
        
