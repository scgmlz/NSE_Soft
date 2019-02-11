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
import numpy as np

#private dependencies
from ..qt_gui.main_result_ui        import Ui_result_widget
from ..py_gui.dialog                import dialog 
from ..py_gui.result_list_handler   import ResultHandlerUI

#private plotting library
from simpleplot.multi_canvas        import Multi_Canvas

class PageResultWidget(Ui_result_widget):
    
    def __init__(self, stack, parent):
        
        Ui_result_widget.__init__(self)
        self.parent         = parent
        self.stack          = stack
        self.local_widget   = QtWidgets.QWidget() 
        self.env_handler    = None
        self._setup()
        self._connect()
        
    def _setup(self):
        '''
        This is the initial setup method that will 
        build the layout and introduce the graphics
        area.
        '''
        self.setupUi(self.local_widget)
        self.my_canvas          = Multi_Canvas(
            self.process_widget_plot,
            grid        = [[True]],
            x_ratios    = [1],
            y_ratios    = [1],
            background  = "w",
            highlightthickness = 0)
        self.ax                 = self.my_canvas.get_subplot(0,0)
        self.ax.pointer['Label_Precision'] = ('.4','.4','.4','.4')
        self.result_handler_ui  = ResultHandlerUI(self)

    def _connect(self):
        '''
        Connect all Qt slots to their respective methods.
        '''
        self.process_tree_x.itemClicked.connect(self.result_handler_ui._getPlotItems)
        self.process_tree_y.itemClicked.connect(self.result_handler_ui._getPlotItems)
        self.process_button_refresh.clicked.connect(self.result_handler_ui.refreshDict)
        self.process_button_set.clicked.connect(self.result_handler_ui._processPartResults)
        self.process_tree_error.itemClicked.connect(self.result_handler_ui._getPlotItems)
        self.process_button_plot_add.clicked.connect(self.result_handler_ui.addPlotElement)
        self.process_button_plot_remove.clicked.connect(self.result_handler_ui.removePlotElement)
        self.process_button_plot_reset.clicked.connect(self.result_handler_ui.removeAllPlotElement)
        self.process_button_plot_plot.clicked.connect(self._updatePlot)
        self.process_button_plot_hide_data.clicked.connect(self._hidePlotData)
        self.process_button_plot_hide_plot_items.clicked.connect(self._hidePlotItems)
        self.process_button_echo_fit.clicked.connect(self._plotEcho)
        self.process_button_gamma.clicked.connect(self._plotGamma)

    def link(self, env_handler = None):
        '''
        Link the GUI to the environment that will be  read and
        taken care of.
        '''
        if not env_handler == None:
            self.env_handler = env_handler

        self.result_handler_ui._fillAllResults(
            self.env_handler,
            self.process_tree_error,
            self.process_tree_x,
            self.process_tree_y,
            self.process_list_plot,
            self.process_list_results)

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

    def _hidePlotData(self):
        '''
        Hide the plot_manager to allow more space for the
        plot view in the frame.
        '''
        self.data_group.setVisible(
            not self.data_group.isVisible())

        if self.data_group.isVisible():
            self.process_button_plot_hide_plot_items.setText('Hide Items')
        else:
            self.process_button_plot_hide_plot_items.setText('Show Items')

    def _hidePlotItems(self):
        '''
        Hide the plot_manager to allow more space for the
        plot view in the frame.
        '''
        self.plot_items_group.setVisible(
            not self.plot_items_group.isVisible())

        if self.plot_items_group.isVisible():
            self.process_button_plot_hide_data.setText('Hide Data')
        else:
            self.process_button_plot_hide_data.setText('Show Data')

    def _updatePlot(self):
        '''

        '''
        try:
            self.ax.clear()
        except:
            pass

        #get the instructions
        instructions = self.result_handler_ui._processPlot()

        #set up the offsets
        idx = 0
        for key in instructions.keys():
            if self.process_check_offset.isChecked() and instructions[key]['link'] == None:
                instructions[key]['offset'] += self.process_spin_offset_total.value() + idx * self.process_spin_offset.value()
                idx+=1

        for key in instructions.keys():
            if not instructions[key]['link'] == None:
                instructions[key]['offset'] = instructions[instructions[key]['link']]['offset']

        #plot all
        for key in instructions.keys():
            if len(instructions[key]['style']) == 0:
                pass
            elif not 'y key' in instructions[key].keys():
                pass
            elif not 'x key' in instructions[key].keys() and not 'e key' in instructions[key].keys():
                self._plotSingleY(instructions[key])
            elif 'x key' in instructions[key].keys() and not 'e key' in instructions[key].keys():
                self._plotDoubleY(instructions[key])
            elif 'x key' in instructions[key].keys() and 'e key' in instructions[key].keys():
                self._plotTripleY(instructions[key])

        self.ax.redraw()

    def _plotSingleY(self, instruction):
        '''
        Plot a curve where only the y axes is defined.
        '''
        y = np.asarray(self.result_handler_ui.getDataFromKey(instruction['y key']))
        x = np.asarray([i for i in range(len(y))])

        self.ax.add_plot(
            'Scatter', 
            x, 
            y+instruction['offset'], 
            Style       = instruction['style'], 
            Thickness   = instruction['thickness'],
            Color       = instruction['color'],
            Log         = [
                self.process_check_log_x.isChecked(),self.process_check_log_y.isChecked()])

    def _plotDoubleY(self, instruction):
        '''
        Plot a curve where only the y and x axes are defined.
        '''
        y = np.asarray(self.result_handler_ui.getDataFromKey(instruction['y key']))
        x = np.asarray(self.result_handler_ui.getDataFromKey(instruction['x key']))
        sort_idx = x.argsort()

        self.ax.add_plot(
            'Scatter', 
            x[sort_idx], 
            y[sort_idx]+instruction['offset'],
            Style       = instruction['style'], 
            Thickness   = instruction['thickness'],
            Color       = instruction['color'],
            Log         = [
                self.process_check_log_x.isChecked(),self.process_check_log_y.isChecked()])

    def _plotTripleY(self, instruction):
        '''
        Plot a curve where all axes are defined.
        '''
        y = np.asarray(self.result_handler_ui.getDataFromKey(instruction['y key']))
        x = np.asarray(self.result_handler_ui.getDataFromKey(instruction['x key']))
        e = np.asarray(self.result_handler_ui.getDataFromKey(instruction['e key']))
        sort_idx = x.argsort()

        self.ax.add_plot(
            'Scatter', 
            x[sort_idx], 
            y[sort_idx]+instruction['offset'],
            Error       = {
                'bottom':e[sort_idx],
                'top':e[sort_idx]},
            Style       = instruction['style'], 
            Thickness   = instruction['thickness'],
            Color       = instruction['color'],
            Log         = [
                self.process_check_log_x.isChecked(),self.process_check_log_y.isChecked()])

    def _plotGamma(self):
        '''
        Plot gamma in a way that all is done
        automatically
        '''
        self.result_handler_ui.quickGammaSet()
        self._updatePlot()

    def _plotEcho(self):
        '''
        Plot gamma in a way that all is done
        automatically
        '''
        self.result_handler_ui.quickEchoSet()
        self._updatePlot()
