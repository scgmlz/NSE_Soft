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
# from .plot_widget               import PlotItem
from .drag_drop_model           import DragModel, DropModel
from simpleplot.model.node      import SessionNode
from .plot_node                 import PlotNode

class ResultHandlerUI:
 
    def __init__(self, parent, result_tree_view, plot_tree_view):
        self.parent             = parent
        self.result_tree_view   = result_tree_view
        self.plot_tree_view     = plot_tree_view

        self._root_result_node  = SessionNode('Root')
        self.result_model       = DragModel(
            self._root_result_node,col_count=1)
        self.result_tree_view.setModel(self.result_model)

        self._plot_node     = SessionNode('Root')
        self._echo_root     = SessionNode('Echos',    parent = self._plot_node)
        self._fit_root      = SessionNode('Fits',     parent = self._plot_node)
        self._gamma_root    = SessionNode('Gammas',   parent = self._plot_node)
        self._other_root    = SessionNode('Others',   parent = self._plot_node)
        self.plot_model = DropModel(
            self._plot_node,col_count=1)
        self.plot_tree_view.setModel(self.plot_model)

        self._echo_plot_items   = []
        self._gamma_plot_items  = []
        self._other_plot_items  = []

        self.current_item = None

    def link(self, env_handler):
        '''
        link the enc handler
        '''
        self.env_handler = env_handler

    def refreshDict(self):
        '''
        Refresh the dictionary of environments to 
        take into account. 
        '''
        names = [env.name for env in self.env_handler.env_array]
        for name in names: 
            child = self._root_result_node.childFromName(name)
            if child is None:
                temp_element = SessionNode(name, parent = self._root_result_node)
                temp_echo    = SessionNode('Echo result', parent = temp_element)
                temp_fit     = SessionNode('Fit result', parent = temp_element)
                temp_gamma   = SessionNode('Gamma result', parent = temp_element)
            else:
                temp_echo    = child.childFromName('Echo result')
                temp_fit     = child.childFromName('Fit result')
                temp_gamma   = child.childFromName('Gamma result')

            target  = self.env_handler.getEnv(name)
            result  = target.results.getLastResult(name = 'Contrast fit')

            if not result is None:
                temp_gamma.setData(1, [
                    result.result_dict['Select'],
                    result.result_dict['Gamma'],
                    result.result_dict['Gamma_error']])

                para_target = result.result_dict['Parameters']
                for key in para_target.keys():
                    child = temp_echo.childFromName(str(key))
                    if child is None:
                        child = SessionNode(str(key), parent = temp_echo)
                    child.setData(1, [
                        para_target[key]['x'],
                        para_target[key]['y'],
                        para_target[key]['y_error'],
                        para_target[key]['y_raw'],
                        para_target[key]['y_raw_error'] ])

                curve_target    = result.result_dict['Curve']
                axis_target     = result.result_dict['Curve Axis']
                for key in para_target.keys():
                    child = temp_fit.childFromName(str(key))
                    if child is None:
                        child = SessionNode(str(key), parent = temp_fit)
                    child.setData(1, [
                        axis_target[key],
                        curve_target[key]])

        self.result_model.referenceModel()

        for child in self._root_result_node._children:
            if not child._name in names:
                row = child.index().row()
                self.result_model.removeRows(row, 1, self._root_result_node)

        self.result_model.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def processDrop(self, link):
        '''
        After the drag and drop the addresses need
        to be analysed to find the items to link
        into our view
        '''
        link = str(link, 'utf-8')
        items = []
        for address in link.split('|'):
            path = address.split('>')
            item = self._root_result_node
            for step in path[1:]:
                item = item.childFromName(step)
            items.append(item)

        echo_items  = []
        gamma_items = []
        fit_items   = []
        for item in items:
            if item.parent()._name == 'Root':
                echo_pointer    = item.childFromName('Echo result')
                for child in echo_pointer._children:
                    echo_items.append(child)
                gamma_items.append(item.childFromName('Gamma result'))
            elif item._name == 'Echo result':
                for child in item._children:
                    echo_items.append(child)
            elif item._name == 'Fit result':
                for child in item._children:
                    fit_items.append(child)
            elif item._name == 'Gamma result':
                gamma_items.append(item)
            elif item.parent()._name == 'Echo result':
                echo_items.append(item)
            elif item.parent()._name == 'Fit result':
                fit_items.append(item)

        names = [item._name for item in self._echo_root._children]
        for echo_item in echo_items:
            name = echo_item.parent().parent()._name + '>data>' +echo_item._name
            if not name in names:
                PlotNode(name,self._echo_root,echo_item)

        names = [item._name for item in self._fit_root._children]
        for fit_item in fit_items:
            name = fit_item.parent().parent()._name + '>fit>' +fit_item._name
            if not name in names:
                PlotNode(name,self._fit_root,fit_item)

        names = [item._name for item in self._gamma_root._children]
        for gamma_item in gamma_items:
            name = gamma_item.parent().parent()._name + '>' +gamma_item._name
            if not name in names:
                QtGui.QStandardItem(name,self._gamma_root,gamma_item)

    def setPlotItem(self, index):
        if not self.current_item is None:
            self.current_item.disconnectFromWidget()
        self.current_item  = self.plot_model.itemAt(index)
        if not self.current_item is self._gamma_root and not self.current_item is self._echo_root:
            self.current_item.connectToWidget(self.parent)

    def removePlotElements(self):
        '''
        Remove all plot elements
        '''
        indices = self.plot_tree_view.selectedIndexes()
        for index in indices:
            self.plot_model.removeRows(index.row(), 1, self.plot_model.itemAt(index).parent())

    def removeAllIntElement(self):
        '''
        Remove all plot elements
        '''
        self.plot_model.removeRows(0, len(self._fit_root._children), self._fit_root)
        self.plot_model.removeRows(0, len(self._gamma_root._children), self._gamma_root)
        self.plot_model.removeRows(0, len(self._echo_root._children), self._echo_root)

    def removeAllExtElement(self):
        '''
        Remove all plot elements
        '''
        self.plot_model.removeRows(0, len(self._other_root._children), self._other_root)

    def _processPlot(self):
        '''
        Plot the data from the plot elements
        '''
        plot_parameters = {}
        for child in self._echo_root._children:
            plot_parameters[child._name] = child._getPlotDict()
        for child in self._gamma_root._children:
            plot_parameters[child._name] = child._getPlotDict()
        for child in self._fit_root._children:
            plot_parameters[child._name] = child._getPlotDict()
        return plot_parameters
