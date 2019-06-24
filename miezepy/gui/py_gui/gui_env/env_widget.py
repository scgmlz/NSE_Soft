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

from ...qt_gui.env_widget_ui import Ui_env_widget
from .drag_env_items import DraggableButton, DropLabel, DropWidget

class EnvWidget(Ui_env_widget,QtCore.QObject):
    '''
    This class will manage the raw import 
    machinery. the UI is inherited through 
    Ui_main_window from the Qt designer anf then
    converted through pyuic5
    '''
    edited          = QtCore.pyqtSignal(list)
    load_clicked    = QtCore.pyqtSignal(str)
    mask_clicked    = QtCore.pyqtSignal(str)
    script_clicked  = QtCore.pyqtSignal(str)
    results_clicked = QtCore.pyqtSignal(str)
    dropAccepted    = QtCore.pyqtSignal(str)

    def __init__(self, env, parent = None):
        QtCore.QObject.__init__(self)
        Ui_env_widget.__init__(self)

        self.parent = parent
        self.item   = QtWidgets.QListWidgetItem(parent)
        self.widget = DropWidget()

        self.setupUi(self.widget)
        self.setUpMore()

        self.env    = env
        self.initialize()

        self.parent.setItemWidget(self.item, self.widget)
        self.item.setSizeHint(self.widget.size())

    def setUpMore(self):
        '''
        Manage the local buttons
        '''
        self.env_button_load = DraggableButton(self.env_frame)
        self.env_button_load.setText('Data')        
        self.env_button_load.setObjectName("env_button_load")
        self.verticalLayout.addWidget(self.env_button_load)
        self.env_button_mask = DraggableButton(self.env_frame)
        self.env_button_mask.setText('Masks')        
        self.env_button_mask.setObjectName("env_button_mask")
        self.verticalLayout.addWidget(self.env_button_mask)
        self.env_button_scripts = DraggableButton(self.env_frame)
        self.env_button_scripts.setText('Process')
        self.env_button_scripts.setObjectName("env_button_scripts")
        self.verticalLayout.addWidget(self.env_button_scripts)
        self.env_button_results = DraggableButton(self.env_frame)
        self.env_button_results.setText('Results')
        self.env_button_results.setObjectName("env_button_results")
        self.verticalLayout.addWidget(self.env_button_results)

    def initialize(self):
        '''
        initialize the widget and set the stage
        '''
        self.env_input_name.setText(self.env.name)
        self.refreshData()
        self.connect()

    def connect(self):
        '''
        connect
        '''
        self.env_input_name.textChanged.connect(self.nameEdit)
        self.env_button_load.clicked.connect(self.loadClicked)
        self.env_button_mask.clicked.connect(self.maskClicked)
        self.env_button_scripts.clicked.connect(self.scriptClicked)

        self.env_input_name.installEventFilter(self)
        self.env_button_load.installEventFilter(self)
        self.env_button_mask.installEventFilter(self)
        self.env_button_scripts.installEventFilter(self)
        self.env_text_data_print.installEventFilter(self)
        
        self.widget.dropAccepted.connect(self.dropAccepted.emit)

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
        self.env_text_data_print.setText(self.env.current_data.__str__())

    def nameEdit(self):
        '''
        connect
        '''
        self.env.name = self.env_input_name.text()

    def eventFilter(self, in_object, event):
        '''
        The event filter to manage clicks on all 
        '''
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.item.setSelected(True)
        return in_object.eventFilter(in_object, event)

