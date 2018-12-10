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
from functools import partial

from ..qt_gui.main_env_widget_ui    import Ui_env_widget
from ..py_gui.env_widget            import EnvWidget

class PageEnvWidget(Ui_env_widget):
    
    def __init__(self, stack, parent):
        Ui_env_widget.__init__(self)
        self.parent         = parent
        self.stack          = stack
        self.local_widget   = QtWidgets.QWidget() 
        self.setupUi(self.local_widget)
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
        self.main_widget_env.currentRowChanged.connect(self.setCurrentElement)

    def link(self, handler):
        '''
        ##############################################
        link the class that will manage the current 
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
        self.refreshList()

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
        self.main_widget_env.clear()
        self.envs_widgets = []
        self.envs = []
        
    def refreshList(self):
        '''
        ##############################################
        refresh and rebuild the view
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.initialize()

        for key in self.handler.env_dict.keys():

            self.envs.append(EnvWidget(self.handler.env_dict[key]))
            self.envs_widgets.append(QtWidgets.QListWidgetItem(self.main_widget_env))


        for env, env_widget in zip(self.envs, self.envs_widgets):

            env_widget.setSizeHint(env.widget.size())
            self.main_widget_env.addItem(env_widget)
            self.main_widget_env.setItemWidget(
                env_widget,
                env.widget)

            env.load_clicked.connect(partial(self.openLoad, env.env))
            env.script_clicked.connect(partial(self.openScript, env.env))

        if len(self.envs) > 0:
            self.setCurrentElement(len(self.envs)-1)

    def addEnvironment(self):
        '''
        ##############################################
        Add an environment to the system
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        env = self.handler.new_environment()

        self.refreshList()

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

        self.main_widget_env.itemWidget(self.main_widget_env.item(index)).setFocus()

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
            env.refreshData()

    def openLoad(self, env):
        '''
        ##############################################
        open the load window through the current 
        button system
        ———————
        Input: 
        - env_name (str) is the name of the environment
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.parent.widgetClasses[1].link(env.io)
        self.parent.widgetClasses[1].populateAll()
        self.parent.refreshChecked(index = 1)

    def openScript(self, env):
        '''
        ##############################################
        open the load window through the current 
        button system
        ———————
        Input: 
        - env_name (str) is the name of the environment
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.parent.widgetClasses[2].link(env)
        self.parent.refreshChecked(index = 2)
