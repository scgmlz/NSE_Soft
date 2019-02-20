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

from ...gui.qt_gui.env_widget_ui import Ui_env_widget

class EnvWidget(Ui_env_widget,QtCore.QObject):
    '''
    This class will manage the raw import 
    machinery. the UI is inherited through 
    Ui_main_window from the Qt designer anf then
    converted through pyuic5
    '''
    #set up the edit signal
    edited          = QtCore.pyqtSignal(list)
    load_clicked    = QtCore.pyqtSignal(str)
    mask_clicked    = QtCore.pyqtSignal(str)
    script_clicked  = QtCore.pyqtSignal(str)
    results_clicked = QtCore.pyqtSignal(str)

    def __init__(self, env):

        QtCore.QObject.__init__(self)
        Ui_env_widget.__init__(self)
        self.widget = QtWidgets.QWidget()
        self.setupUi(self.widget)
        self.env = env
        self.initialize()
        self.connect()

    def initialize(self):
        '''
        initialize the widget and set the stage
        '''
        self.env_input_name.setText(self.env.name)
        self.refreshData()

    def connect(self):
        '''
        connect
        '''
        self.env_input_name.textChanged.connect(self.nameEdit)
        self.env_button_load.clicked.connect(self.loadClicked)
        self.env_button_mask.clicked.connect(self.maskClicked)
        self.env_button_scripts.clicked.connect(self.scriptClicked)

    def loadClicked(self):
        '''
        connect
        '''
        self.load_clicked.emit(self.env.name)

    def maskClicked(self):
        '''
        connect
        '''
        self.mask_clicked.emit(self.env.name)

    def scriptClicked(self):
        '''
        connect
        '''
        self.script_clicked.emit(self.env.name)

    def refreshData(self):
        '''
        connect
        '''
        self.env_text_data_print.setText(self.env.data[self.env.initial_data_name].__str__())

    def nameEdit(self):
        '''
        connect
        '''
        self.env.name = self.env_input_name.text()