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

from ...qt_gui.main_env_widget_ui   import Ui_main_env_widget
from .env_widget                    import EnvWidget

class PageEnvWidget(Ui_main_env_widget):
    
    def __init__(self, stack, parent):
        Ui_main_env_widget.__init__(self)
        self.parent         = parent
        self.stack          = stack
        self.local_widget   = QtWidgets.QWidget() 
        self.setup()
        self.connect()

    def setup(self):
        '''
        This is the initial setup method that will 
        build the layout and introduce the graphics
        area
        '''
        self.setupUi(self.local_widget)
        self.main_widget_env.setStyleSheet(
            "QListWidget::item { border: 2px solid black ;background-color: palette(Midlight) }"
            "QListWidget::item:selected { background-color: palette(Mid)  }")

    def connect(self):
        '''
        connect the actions to their respective buttons
        '''
        self.main_widget_env.currentRowChanged.connect(self.setCurrentElement)
        self.env_button_add.clicked.connect(self.addEnvironment)
        self.env_button_remove.clicked.connect(self.deleteEnvironment)

    def link(self, handler):
        '''
        link the class that will manage the current 
        input output.
        '''
        self.handler = handler 
        self.initialize()
        self.refreshList()

    def initialize(self):
        '''
        This method checks if the data has been set
        in a previous instance.
        '''
        self.main_widget_env.clear()
        self.envs_widgets = []
        self.envs = []
        
    def refreshList(self):
        '''
        refresh and rebuild the view
        '''
        self.initialize()

        for element in self.handler.env_array:
            self.envs.append(
                EnvWidget(element, self.main_widget_env))
            self.envs[-1].load_clicked.connect(
                partial(self.openLoad, self.envs[-1].env))
            self.envs[-1].mask_clicked.connect(
                partial(self.openMask, self.envs[-1].env))
            self.envs[-1].script_clicked.connect(
                partial(self.openScript, self.envs[-1].env))
            self.envs[-1].dropAccepted.connect(self.processDrop)

        if len(self.envs) > 0:
            self.setCurrentElement(len(self.envs)-1)

    def addEnvironment(self):
        '''
        Add an environment to the system
        '''
        self.handler.addEnv()
        self.refreshList()

    def deleteEnvironment(self):
        '''
        delete an environment of the system
        '''
        index = self.main_widget_env.currentRow()
        if not index == -1:
            names = [env.name for env in self.handler.env_array]

            for element in self.handler.env_array:
                if element.name == self.envs[index].env.name:
                    index_to_delete = names.index(element.name)
                    break

            self.main_widget_env.takeItem(index)
            del self.envs[index]
            del self.handler.env_array[index_to_delete]
            del self.handler.current_env

            self.setCurrentElement(index - 1)

    def setCurrentElement(self, row = None):
        '''
        On clicking an element the system will set the
        classes linked to the current element 
        '''
        if isinstance(row, int):
            index = row
        else:
            index = self.main_widget_env.currentRow()

        if index == len(self.envs):
            index -=1
        elif index == -1 and not len(self.envs) == 0:
            index =0
        elif len(self.envs) == 0:
            self.parent.window.setWindowTitle('MIEZEPY')
            return

        self.handler.setCurrentEnv(idx = index)
        self.parent.window.setWindowTitle('MIEZEPY ('+str(self.handler.current_env.name)+')')
        self.envs[index].widget.setFocus()
        self.parent.mask_interface.link(self.handler.current_env.mask)

    def refreshData(self):
        '''
        refresh the current data text display
        '''
        for env in self.envs:
            env.refreshData()

    def openLoad(self, env):
        '''
        open the load window through the current 
        button system
        '''
        self.main_widget_env.setCurrentRow(self.handler.getIdx(env.name))
        self.parent.actionDispatcher(1)

    def openMask(self, env):
        '''
        open the load window through the current 
        button system
        '''
        self.main_widget_env.setCurrentRow(self.handler.getIdx(env.name))
        self.parent.actionDispatcher(2)

    def openScript(self, env):
        '''
        open the load window through the current 
        button system
        '''
        self.main_widget_env.setCurrentRow(self.handler.getIdx(env.name))
        self.parent.actionDispatcher(3)

    def processDrop(self, drop_intructions):
        '''
        This method is here to allow transfer of items
        from one environnement to another

        Parameters
        ----------
        from_env : Environnement
            The source environnement
        to_env : Environnement
            The source environnement
            
        '''
        self.handler.processOperation(*drop_intructions.split('|'))
        self.main_widget_env.setCurrentRow(self.handler.getIdx(
                self.handler.getEnv(drop_intructions.split('|')[-1]).name))
        
