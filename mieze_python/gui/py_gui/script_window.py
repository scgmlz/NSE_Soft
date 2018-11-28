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

#private dependencies
from ...gui.qt_gui.script_window_ui import Ui_script_window
from ...gui.py_gui.python_syntax import PythonHighlighter


class ScriptWindowLayout(Ui_script_window):
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
    def __init__(self, window, window_manager):

        ##############################################
        #Local pointers
        Ui_script_window.__init__(self)

        self.window_manager = window_manager
        self.window         = window
        self.setup()
        self.connect()

        self.elements       = []
        self.meta_elements  = []

    def setup(self):
        '''
        ##############################################
        This is the initial setup method that will 
        build the layout and introduce the graphics
        area
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.setupUi(self.window)
        self.syntaxHighliter_0 = PythonHighlighter(
            self.script_text_import.document())
        self.syntaxHighliter_1 = PythonHighlighter(
            self.script_text_phase.document())
        self.syntaxHighliter_2 = PythonHighlighter(
            self.script_text_reduction.document())
        self.syntaxHighliter_3 = PythonHighlighter(
            self.script_text_post.document())

    def link(self, env):
        '''
        ##############################################

        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.env = env
        self.refresh()

    def refresh(self):
        '''
        ##############################################

        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''        
        self.script_text_import.setText(self.env.process.editable_scripts[0])
        self.script_text_phase.setText(self.env.process.editable_scripts[1])
        self.script_text_reduction.setText(self.env.process.editable_scripts[2])
        self.script_text_post.setText(self.env.process.editable_scripts[3])

    def connect(self):
        '''
        ##############################################

        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.script_button_import_run.clicked.connect(self.runImport)
        self.script_button_phase_run.clicked.connect(self.runPhase)
        self.script_button_reduction_run.clicked.connect(self.runReduction)
        self.script_button_post_run.clicked.connect(self.runPost)
        self.actionLoad_scripts.triggered.connect(self.loadScripts)
        self.actionSave_scripts.triggered.connect(self.saveScripts)

    def runImport(self):
        print(type(self.script_text_import.toPlainText()))
        exec(compile(self.script_text_import.toPlainText(), '<string>', 'exec'))

    def runPhase(self):
        exec(compile(self.script_text_phase.toPlainText(), '<string>', 'exec'))

    def runReduction(self):
        exec(compile(self.script_text_reduction.toPlainText(), '<string>', 'exec'))

    def runPost(self):
        exec(compile(self.script_text_post.toPlainText(), '<string>', 'exec'))

    def saveScripts(self):
        '''
        ##############################################

        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        filters = "mieze_script_save.py"

        file_path = QtWidgets.QFileDialog.getSaveFileName(
                self.window, 
                'Select file',
                filters)[0]

        self.env.process.saveScripts(
            file_path,
            [
                self.script_text_import.toPlainText(),
                self.script_text_phase.toPlainText(),
                self.script_text_reduction.toPlainText(),
                self.script_text_post.toPlainText()
            ])


    def loadScripts(self):
        '''
        ##############################################

        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        filters = "*.py"

        file_path = QtWidgets.QFileDialog.getOpenFileName(
                self.window, 
                'Select file',
                filters)[0]

        self.env.process.loadScripts(
            file_path)
        self.refresh()