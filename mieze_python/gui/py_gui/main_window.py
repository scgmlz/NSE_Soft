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

from ..qt_gui.mainwindow_ui import Ui_MIEZETool 
from ..py_gui.env_widget    import EnvWidget


class MainWindowLayout(Ui_MIEZETool):
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
        Ui_MIEZETool.__init__(self)
        self.window = window
        self.window_manager = window_manager
        self.setupUi(window)
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
        self.actionAdd_Environement.triggered.connect(self.addEnvironment)

    def link(self, handler):
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
        self.handler = handler 
        self.initialize()

    def initialize(self):
        '''
        ##############################################
        This method checks if the data has been set
        in a previsou instance
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.envs = []

    def addEnvironment(self):
        '''
        ##############################################
        Add an evironement to the system
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        env = self.handler.new_environment()

        self.envs.append([
            QtWidgets.QListWidgetItem(self.main_widget_env),
            EnvWidget(env)
            ])

        self.envs[-1][0].setSizeHint(self.envs[-1][1].widget.size())
        self.main_widget_env.setItemWidget(
            self.envs[-1][0],
            self.envs[-1][1].widget)

        self.envs[-1][1].load_clicked.connect(self.openLoad)
        self.envs[-1][1].script_clicked.connect(self.openScript)

        self.setCurrentElement(len(self.envs)-1)

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
            index = self.main_widget_env.currentRow()

    def refreshData(self):
        '''
        ##############################################
        refresh the current data text display
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        for env in self.envs:
            env[1].refreshData()

    def openLoad(self, env_name):
        '''
        ##############################################
        open the load window through the current 
        biutton system
        ———————
        Input: 
        - env_name (str) is the name of the envionment
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.window_manager.newWindow('Import')
        self.window_manager.active_windows['Import'].target.link(
            self.handler.env_dict[env_name].io)
        self.window_manager.active_windows['Import'].target.populateAll()

    def openScript(self, env_name):
        '''
        ##############################################
        open the load window through the current 
        biutton system
        ———————
        Input: 
        - env_name (str) is the name of the envionment
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.window_manager.newWindow('Scripts')
        self.window_manager.active_windows['Scripts'].target.link(
            self.handler.env_dict[env_name])
