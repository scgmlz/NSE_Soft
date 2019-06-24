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
import numpy as np

#private dependencies
from ...qt_gui.main_result_ui   import Ui_result_widget
from ..gui_common.dialog        import dialog 
from .result_list_handler       import ResultHandlerUI
from .drag_drop_trees           import ResultTree, PlotTree

#private plotting library
from simpleplot.canvas.multi_canvas import MultiCanvasItem

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
        self.process_tree = ResultTree(self.data_group)
        self.verticalLayout_4.addWidget(self.process_tree)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.process_refresh_button = QtWidgets.QPushButton('Refresh', self.data_group)
        self.process_refresh_button.setObjectName("process_refresh_button")
        self.horizontalLayout.addWidget(self.process_refresh_button)
        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.process_list_plot = PlotTree(self.plot_items_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.process_list_plot.sizePolicy().hasHeightForWidth())
        self.verticalLayout_2.addWidget(self.process_list_plot)

        self.my_canvas = MultiCanvasItem(
            self.process_widget_plot,
            grid        = [[True]],
            x_ratios    = [1],
            y_ratios    = [1],
            background  = "w",
            highlightthickness = 0)
        self.ax = self.my_canvas.getSubplot(0,0)
        self.my_canvas.canvas_nodes[0][0][0].grid_layout.setMargin(0)

        self.result_handler_ui  = ResultHandlerUI(
            self, 
            self.process_tree,
            self.process_list_plot)

    def _connect(self):
        '''
        Connect all Qt slots to their respective methods.
        '''
        self.result_handler_ui.result_model.dataChanged.connect(
            self._resize_tree)
        self.process_refresh_button.clicked.connect(
            self.result_handler_ui.refreshDict)
        self.process_list_plot.dropAccepted.connect(
            self.result_handler_ui.processDrop)
        self.process_list_plot.clicked.connect(
            self.result_handler_ui.setPlotItem)

        self.remove_plot.clicked.connect(
            self.result_handler_ui.removePlotElements)
        self.reset_intern.clicked.connect(
            self.result_handler_ui.removeAllIntElement)
        self.reset_external.clicked.connect(
            self.result_handler_ui.removeAllExtElement)

        self.process_button_plot_plot.clicked.connect(
            self._updatePlot)
        self.set_rainbow.clicked.connect(
            self.result_handler_ui.setRainbow)
            
        self.process_check_log_x.clicked.connect(
            self.manageLog)
        self.process_check_log_y.clicked.connect(
            self.manageLog)
        self.my_canvas._model.dataChanged.connect(
            self.setLog)

    def _resize_tree(self):
        '''
        process with the log
        '''
        self.process_tree.resizeColumnToContents(0)

    def manageLog(self):
        '''
        process with the log
        '''
        self.my_canvas._model.dataChanged.disconnect(self.setLog)
        self.ax.axes.general_handler['Log'] = [
            self.process_check_log_x.isChecked(),
            self.process_check_log_y.isChecked()]
        self.my_canvas._model.dataChanged.connect(self.setLog)
        
    def setLog(self):
        '''
        process with the log
        '''
        self.process_check_log_x.setChecked(
            self.ax.axes.general_handler['Log'][0])
        self.process_check_log_y.setChecked(
            self.ax.axes.general_handler['Log'][1])

    def link(self, env_handler = None):
        '''
        Link the GUI to the environment that will be  read and
        taken care of.
        '''
        if not env_handler == None:
            self.env_handler = env_handler
        
        self.result_handler_ui.link(env_handler)

    def _updatePlot(self):
        '''

        '''
        self.ax.clear()

        #get the instructions
        instructions = self.result_handler_ui._processPlot()

        #set up the offsets
        idx = 0
        for key in instructions.keys():
            if self.process_check_offset.isChecked() and instructions[key]['link'] == None:
                instructions[key]['offset'] += self.process_spin_offset_total.value() + idx * self.process_spin_offset.value()
                idx+=1

        for key in instructions.keys():
            if not instructions[key]['link'] == None and instructions[key]['link'] in instructions.keys():
                instructions[key]['offset'] = instructions[instructions[key]['link']]['offset']

        #plot all
        for key in instructions.keys():
            if len(instructions[key]['style']) == 0:
                pass
            elif not 'y' in instructions[key].keys():
                pass
            elif not 'x' in instructions[key].keys() and not 'e' in instructions[key].keys():
                self._plotSingleY(instructions[key], key)
            elif 'x' in instructions[key].keys() and not 'e' in instructions[key].keys():
                self._plotDoubleY(instructions[key], key)
            elif 'x' in instructions[key].keys() and 'e' in instructions[key].keys():
                self._plotTripleY(instructions[key], key)

        self.ax.draw()

    def _plotSingleY(self, instruction, key):
        '''
        Plot a curve where only the y axes is defined.
        '''
        y = instruction['y']
        x = np.array([i for i in range(len(y))])

        self.ax.addPlot(
            'Scatter', 
            Name        = key,
            x           = x, 
            y           = y+instruction['offset'],
            Style       = instruction['style'], 
            Thickness   = instruction['thickness'],
            Color       = instruction['color'])

    def _plotDoubleY(self, instruction, key):
        '''
        Plot a curve where only the y and x axes are defined.
        '''
        y = instruction['y']
        x = instruction['x']
        sort_idx = x.argsort()

        self.ax.addPlot(
            'Scatter', 
            Name        = key,
            x           = x[sort_idx], 
            y           = y[sort_idx]+instruction['offset'],
            Style       = instruction['style'], 
            Thickness   = instruction['thickness'],
            Color       = instruction['color'])

    def _plotTripleY(self, instruction, key):
        '''
        Plot a curve where all axes are defined.
        '''
        y = instruction['y']
        x = instruction['x']
        e = instruction['e']
        sort_idx = x.argsort()
        error = {
                'height':None,
                'width' : None,
                'bottom':e[sort_idx],
                'top'   :e[sort_idx]}

        self.ax.addPlot(
            'Scatter', 
            Name        = key,
            x           = x[sort_idx], 
            y           = y[sort_idx]+instruction['offset'],
            error       = error,
            Style       = instruction['style'], 
            Thickness   = instruction['thickness'],
            Color       = instruction['color'])

