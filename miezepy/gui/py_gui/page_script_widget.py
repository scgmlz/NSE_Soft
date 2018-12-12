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
import traceback
from functools import partial
import sys, token, tokenize

#private dependencies
from ..qt_gui.main_script_ui        import Ui_script_widget
from ...gui.py_gui.python_syntax        import PythonHighlighter
from ...gui.py_gui.panel_handler        import PanelHandler
from ...gui.py_gui.dialog               import dialog 


class PageScriptWidget(Ui_script_widget):
    
    def __init__(self, stack, parent):
        
        Ui_script_widget.__init__(self)
        self.parent         = parent
        self.stack          = stack
        self.local_widget   = QtWidgets.QWidget() 
        
        self._setup()
        self._connect()
        self.fadeActivity()

        self.elements       = []
        self.meta_elements  = []
        self.env            = None

    def _setup(self):
        '''
        This is the initial setup method that will 
        build the layout and introduce the graphics
        area.
        '''
        self.setupUi(self.local_widget)

        self.text_widgets = [
            self.script_text_import,
            self.script_text_phase,
            self.script_text_reduction,
            self.script_text_post]

        self.button_widgets = [
            self.script_button_import_run,
            self.script_button_phase_run,
            self.script_button_phase_view,
            self.script_button_reduction_run,
            self.script_button_post_run]

        self.syntaxHighliter_0 = PythonHighlighter(
            self.text_widgets[0].document())
        self.syntaxHighliter_1 = PythonHighlighter(
            self.text_widgets[1].document())
        self.syntaxHighliter_2 = PythonHighlighter(
            self.text_widgets[2].document())
        self.syntaxHighliter_3 = PythonHighlighter(
            self.text_widgets[3].document())

        self.tool = PanelHandler(
            self.panel_widget,
            self.para_group,
            self.mask_group)

    def link(self, env):
        '''
        Link the GUI to the environment that will be  read and
        taken care of.
        '''

        self.env = env
        self._refresh()

    def _connect(self):
        '''
        Connect all Qt slots to their respective methods.
        '''
        self.button_widgets[0].clicked.connect(partial(self.run,0))
        self.button_widgets[1].clicked.connect(partial(self.run,1))
        self.button_widgets[2].clicked.connect(partial(self.run,5))
        self.button_widgets[3].clicked.connect(partial(self.run,2))
        self.button_widgets[4].clicked.connect(partial(self.run,3))

        self.text_widgets[0].textChanged.connect(partial(self._updateEditable, 0))
        self.text_widgets[1].textChanged.connect(partial(self._updateEditable, 1))
        self.text_widgets[2].textChanged.connect(partial(self._updateEditable, 2))
        self.text_widgets[3].textChanged.connect(partial(self._updateEditable, 3))

    def _refresh(self):
        '''
        Refresh the text present in the code editors
        with the source present in the core env.process 
        class. 
        '''        
        self.text_widgets[0].setText(self.env.process.editable_scripts[0])
        self.text_widgets[1].setText(self.env.process.editable_scripts[1])
        self.text_widgets[2].setText(self.env.process.editable_scripts[2])
        self.text_widgets[3].setText(self.env.process.editable_scripts[3])

    def _updateEditable(self, index):
        if not self.env == None:
            try:
                self.env.process.editable_scripts[index] = self.text_widgets[index].toPlainText()
            except Exception as e:
                dialog(
                    icon = 'error', 
                    title= 'Could not update script',
                    message = 'The core encountered an error',
                    add_message = str(e),
                    det_message = traceback.format_exc())


    def run(self, index):
        '''
        This is the run method that will determine the measure
        to undertake. 
        '''
        if not self.env == None:
            if index < 5:
                self._runPythonCode(self.text_widgets[index].toPlainText())
            elif index == 5:
                self._runPanel() 

    def runAll(self):
        '''
        Run all the scripts.
        '''
        for i in range(5):
            self.run(i)

    def _runPythonCode(self, code):
        '''
        Parse and run python code. 
        '''

        code_array = self._parseCode(code)
        meta_array = self._parseMeta(code_array)
        self.script_label_running.setText('Script running')
        self.scrip_label_action.setText('Command:')
        self.setActivity(0, len(meta_array))
        success = True

        for i in range(len(code_array)):
            self.setProgress(meta_array[i].strip('\n'), i)

            try:
                exec(code_array[i])

            except Exception as e:
                error = e
                dialog(
                    icon = 'error', 
                    title= 'Script error',
                    message = 'Your script has encountered an error.',
                    add_message = str(e),
                    det_message = traceback.format_exc())
                success = False
                break
        if success:
            self.setProgress('Script ended with success', len(meta_array))
            self.fadeActivity()
        else:
            self.script_label_running.setText('Aborted')
            self.scrip_label_action.setText('Error: ')
            self.setProgress(str(error), i)

        

    def _parseCode(self, code):
        '''
        This function will break down the code into smaller 
        parts to allow interpretation of the failed sequence
        as well as a meaningfull understanding of the progress.
        '''

        temp_code_array = []
        indentation     = False
        comment_bool    = False
        code_lines      = code.split('\n') 

        for line in code_lines:
            if line == '' or line[0] == '#':
                pass
            elif line[0] == "'" or line[0] == '"':
                comment_bool = not comment_bool

            elif line[0].isspace() and not line == '' and not comment_bool:
                if not indentation:
                    indentation = not indentation
                    temp = temp_code_array[-1]
                    temp.append(line)
                else:
                    temp.append(line)
            elif not comment_bool:
                if indentation:
                    indentation = not indentation
                temp_code_array.append([line])

        code_array = []
        for element in temp_code_array:
            if len(element) > 1:
                code_string = ''
                for sub_element in element:
                    code_string += sub_element + '\n'
                code_array.append(code_string)
            else:
                code_array.append(element[0])

        return code_array

    def _parseMeta(self, code_array):
        '''
        This function will try to identify the individual 
        function parts to provide nice insight on what is 
        being processed at the moment.
        '''

        meta_array = []
        for element in code_array:
            if len(element.split('for ')) > 1:
                meta_array.append(
                    "'for' loop over "+str(element.split(' in ')[1].split(':')[0]))
            elif '(' in element and ')' in element:
                meta_array.append(
                    "'function' "+element.split('(')[0]+' with the parameters ('+''.join(element.split('(')[1].split(')')[0])[0:30]+')')
            else:
                 meta_array.append(element[0:40])

        return meta_array

    def _runPanel(self):
        '''
        This function will initiate the panel from the current 
        phase processed data.
        '''
        self.tool.load_initial(self.env)

    def saveScripts(self):
        '''
        This method as the name indicates is in charge of
        prompting the user for a savefile name and location 
        through a QFileDialog and then saves the file as
        a script.
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
        This method will load the string from file through 
        a QFileDialog. Specify a file formated in the right
        way or saved through miezepy.
        '''
        filters = "*.py"

        file_path = QtWidgets.QFileDialog.getOpenFileName(
                self.window, 
                'Select file',
                filters)[0]

        self.env.process.loadScripts(
            file_path)
        self.refresh()



    def setActivity(self, min_val, max_val):
        '''

        '''
        #make it visible in case it was hidden
        self.script_label_running.show()
        self.script_bar_running.show()
        self.scrip_label_action.show()
        self.script_label_action_2.show()

        #in case it was faded
        self._unfade(self.script_label_running)
        self._unfade(self.script_bar_running)
        self._unfade(self.scrip_label_action)
        self._unfade(self.script_label_action_2)

        self.script_bar_running.setMinimum(min_val)
        self.script_bar_running.setMaximum(max_val)

    def hideActivity(self):
        '''

        '''
        self.script_label_running.hide()
        self.script_bar_running.hide()
        self.scrip_label_action.hide()
        self.script_label_action_2.hide()

    def fadeActivity(self):
        '''

        '''
        self._fade(self.script_label_running)
        self._fade(self.script_bar_running)
        self._fade(self.scrip_label_action)
        self._fade(self.script_label_action_2)

    def _unfade(self, widget):
        '''


        '''
        effect = QtWidgets.QGraphicsOpacityEffect()
        effect.setOpacity(1)
        widget.setGraphicsEffect(effect)

    def _fade(self, widget):
        '''

        '''
        widget.effect = QtWidgets.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(widget.effect)

        widget.animation = QtCore.QPropertyAnimation(widget.effect, b"opacity")
        widget.animation.setDuration(1000)
        widget.animation.setStartValue(1)
        widget.animation.setEndValue(0)
        widget.animation.start()

    def setProgress(self, label, val):
        '''

        '''
        self.script_bar_running.setValue(val)
        self.script_label_action_2.setText(label)
        self.parent.window_manager.app.processEvents()