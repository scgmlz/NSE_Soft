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

from ...gui.qt_gui.meta_widget_ui import Ui_meta_widget

class MetaWidget(Ui_meta_widget,QtCore.QObject):
    '''
    This class will manage the raw import 
    machinery. the UI is inherited through 
    Ui_main_window from the Qt designer anf then
    converted through pyuic5
    '''
    #set up the edit signal
    edited = QtCore.pyqtSignal(list)

    def __init__(self):
        QtCore.QObject.__init__(self)
        Ui_meta_widget.__init__(self)
        self.widget = QtWidgets.QWidget()
        self.setupUi(self.widget)
        self.initialize()

    def initialize(self):
        '''
        initialize the widget and set the stage
        '''
        self.equivalence = [
            'None',
            'Parameter',
            'Measurement',
            'Freq. first',
            'Freq. second',
            'Wavelength',
            'lsd',
            'Monitor',
            'Echo']

        self.meta_drop_equivalence.addItems(self.equivalence)
        self.meta_input_fact.setText('1')
        self.meta_label_name.setText('No Name')

    def connect(self):
        '''
        connect
        '''
        self.meta_input_fact.textChanged.connect(self.getValues)
        self.meta_drop_equivalence.currentIndexChanged.connect(self.getValues)
        self.meta_input_manual.textChanged.connect(self.getValues)

    def setParentList(self, parent_list):
        '''
        initialize the widget and set the stage
        '''
        self.parent_list = parent_list

        self.meta_label_name.setText(self.parent_list[0])
        self.meta_input_fact.setText(self.parent_list[3])
        self.meta_drop_equivalence.setCurrentIndex(
            self.equivalence.index(self.parent_list[2]))
        try:
            self.meta_input_manual.setText(self.parent_list[4])
        except:
            pass

        self.connect()

    def getValues(self, index = None):
        '''
        initialize the widget and set the stage
        '''
        self.parent_list = [
            self.parent_list[0],
            self.parent_list[1],
            self.equivalence[self.meta_drop_equivalence.currentIndex()],
            self.meta_input_fact.text(),
            self.meta_input_manual.text()
        ]

        self.edited.emit(self.parent_list)

        
