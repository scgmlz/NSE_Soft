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
from ..py_gui.plot_widget           import PlotItem

class ResultHandlerUI:
 
    def __init__(self, parent):
        self.parent = parent
        self.data_sets_x    = {}
        self.data_sets_y    = {}
        self.data_sets_e    = {}
        self.plot_list      = []
        self.result_dict    = {}

    def _fillAllResults(self,env_handler, process_tree_error, process_tree_x, process_tree_y, process_list_plot,process_list_results):
        '''
        After the run fill the result structure
        '''
        #grab the visual elements
        self.process_tree_error     = process_tree_error
        self.process_tree_x         = process_tree_x
        self.process_tree_y         = process_tree_y
        self.process_list_plot      = process_list_plot
        self.process_list_results   = process_list_results

        self.env_model = QtGui.QStandardItemModel()
        self.process_list_results.setModel(self.env_model)
        self.env_model.itemChanged.connect(self._processPartResults)

        self.plot_model = QtGui.QStandardItemModel()
        self.process_list_plot.setModel(self.plot_model)
        self.process_list_plot.clicked.connect(self._grabPlotItem)
        
        #manage environment specific things
        self.env_handler  = env_handler

    def refreshDict(self):
        '''
        Refresh the dictionary of environments to 
        take into account. 
        '''
        names = [env.name for env in self.env_handler.env_array]

        #fix from env to dict
        for name in names: 
            if not name in self.result_dict.keys():
                self.result_dict[name] = [False, True]
        
        #fix from dict to env
        keys = [key for key in self.result_dict.keys()]
        for name in keys:
            if name not in names:
                del self.result_dict[name]
                
        self._refreshDictView()

    def _refreshDictView(self):
        '''
        Refresh the view associated to the dictionary
        through the elements.
        '''
        to_remove = []

        for idx in range(self.env_model.rowCount()):
            if not self.env_model.item(idx).text() in self.result_dict.keys():
                to_remove.append(idx)

        for idx in to_remove[::-1]:
            self.env_model.removeRow(idx)
        
        for key in self.result_dict.keys():
            if not self.result_dict[key][0]:
                item = QtGui.QStandardItem(key)
                item.setFlags(
                    QtCore.Qt.ItemIsUserCheckable 
                    | QtCore.Qt.ItemIsEnabled)
                check = QtCore.Qt.Checked if self.result_dict[key][1] else QtCore.Qt.Unchecked
                item.setData(
                    QtCore.QVariant(check), 
                    QtCore.Qt.CheckStateRole)
                self.env_model.appendRow(item)
                self.result_dict[key][0] = True

    def _processPartResults(self):
        '''
        Check which environments have been selected and then 
        set the result structure to load
        '''
        self.data_set = {}
        for env in self.env_handler.env_array:
            try:
                self.data_set[env.name] = env.get_result(name = 'Contrast fit').result_dict
            except:
                pass
                
        for tree in [self.process_tree_error, self.process_tree_x, self.process_tree_y]:
            try:
                tree.clear()
                self._fillResult(tree.invisibleRootItem(),self.data_set)
            except:
                pass

    def _fillResult(self, item, value):
        '''
        After the run fill the result structure
        '''
        item.setExpanded(False)

        if type(value) is dict:
            for key, val in sorted(value.items()):
                child = QtWidgets.QTreeWidgetItem()
                child.setText(0, str(key))
                item.addChild(child)
                if isinstance(val,dict):
                    flags = child.flags()
                    flags &= ~QtCore.Qt.ItemIsSelectable
                    child.setFlags(flags)
                self._fillResult(child, val)

    def _grabCascadeState(self, item):
        '''
        This will go through all children 
        of a given item and them check all
        of them for children. If no children 
        are present it will check for the 
        isSelected state.
        Then return False if not all are selected
        and return True if all are selected.
        '''
        boolean_list = []
        for i in range(item.childCount()):
            subitem = item.child(i)
            if subitem.childCount() > 0:
                boolean_list.append(self._grabCascadeState(subitem))
            else:
                boolean_list.append(subitem.isSelected())

        if not all(boolean_list):
            state = False
        elif all(boolean_list):
            state = True

        return state

    def _getAllEndChildren(self, item):
        '''
        get the plot items of the tree items and
        try to make sense of it
        '''
        children = []
        for i in range(item.childCount()):
            subitem = item.child(i)
            if subitem.childCount() > 0:
                elements = self._getAllEndChildren(subitem)
                for element in elements:
                    children.append(element)
            else:
                children.append(subitem)

        return children

    def _setAllEndChildren(self, children, state):
        '''
        get the plot items of the tree items and
        try to make sense of it
        '''
        for child in children:
            child.setSelected(not state)

    def _getPlotItems(self, item):
        '''
        get the plot items of the tree items and
        try to make sense of it
        '''
        if not isinstance(item, str):
            if item.childCount() > 0:
                state       = self._grabCascadeState(item)
                children    = self._getAllEndChildren(item)
                self._setAllEndChildren(children, state)
            
        x_selected = self.process_tree_x.selectedItems()
        y_selected = self.process_tree_y.selectedItems()
        e_selected = self.process_tree_error.selectedItems()

        x_keywords = []
        for item in x_selected:
            x_keywords.append(self._buildDictTree(item))
        y_keywords = []
        for item in y_selected:
            y_keywords.append(self._buildDictTree(item))
        e_keywords = []
        for item in e_selected:
            e_keywords.append(self._buildDictTree(item))

        self._buildPlotData(x_keywords, y_keywords,e_keywords)
        self._populatePlots()

    def _buildDictTree(self, item):
        '''
        get the plot items of the tree items and
        try to make sense of it
        '''
        keywords = []
        while item is not None:
            keywords.append(str(item.text(0)))
            item = item.parent() 
        return keywords[::-1]

    def _buildPlotData(self, x_keywords, y_keywords, e_keywords):
        '''
        Build the data array that will then try to be
        plotted accordingly
        '''
        self.data_sets_x    = {}
        self.data_sets_y    = {}
        self.data_sets_e    = {}

        for element in x_keywords:
            self.data_sets_x['>'.join(element)] = self._getDictVal([element])
        for element in y_keywords:
            self.data_sets_y['>'.join(element)] = self._getDictVal([element])
        for element in e_keywords:
            self.data_sets_e['>'.join(element)] = self._getDictVal([element])

    def _getDictVal(self, elements):
        '''
        Build the data array that will then try to be
        plotted accordingly
        '''
        values = []
        for element in elements:
            val = self.data_set
            for key in element:
                try:
                    val = val[key]
                except:
                    val = val[float(key)]
            values.append(val)

        return values

    def quickGammaSet(self):
        '''
        Plot Gamma elements
        '''
        self.removeAllPlotElement()
        names = ['Select', 'Gamma', 'Gamma_error']
        trees = [
            self.process_tree_x,
            self.process_tree_y,
            self.process_tree_error]

        for idx, tree in enumerate(trees):
            root = tree.invisibleRootItem()
            for i in range(root.childCount()):
                env_item = root.child(i)
                for l in range(env_item.childCount()):
                    subitem = env_item.child(l)
                    if subitem.text(0) in names:
                        subitem.setSelected(True)

        for j,root_key in enumerate([root_key for root_key in self.data_set.keys()]):
            self._getPlotItems('')
            self.addPlotElement()
            self.plot_list[0].setManually(
                x_val = '>'.join([root_key,names[0]]), 
                y_val = '>'.join([root_key,names[1]]),
                e_val = '>'.join([root_key,names[2]]))
        self._populatePlots()

    def quickEchoSet(self):
        '''
        Plot Gamma elements
        '''
        self.removeAllPlotElement()
        names = [ 'Parameters', 'Curve', 'Curve Axis']
        trees = [
            self.process_tree_x,
            self.process_tree_y,
            self.process_tree_error]

        for idx, tree in enumerate(trees):
            root = tree.invisibleRootItem()
            for i in range(root.childCount()):
                env_item = root.child(i)
                for l in range(env_item.childCount()):
                    subitem = env_item.child(l)
                    if subitem.text(0) in names:
                        state       = False
                        children    = self._getAllEndChildren(subitem)
                        self._setAllEndChildren(children, state)

        self._getPlotItems('')
        color_list = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

        index = 0
        for j,root_key in enumerate([root_key for root_key in self.data_set.keys()]):
            for i,key in enumerate([key for key in self.data_set[root_key]['Parameters'].keys()]):

                #add the data plot
                self.addPlotElement()
                self.plot_list[index].setManually(
                    x_val = '>'.join([root_key, 'Parameters', str(key), 'x']), 
                    y_val = '>'.join([root_key, 'Parameters', str(key), 'y']), 
                    e_val = '>'.join([root_key, 'Parameters', str(key), 'y_error']))
                self.plot_list[index].scatter        = True
                self.plot_list[index].scatter_type   = 0
                self.plot_list[index].scatter_size   = 10
                self.plot_list[index].line           = False
                self.plot_list[index].line_thickness = 2
                self.plot_list[index].setColor(color_list[index%9])

                index += 1

                #add the fit curve
                self.addPlotElement()
                self.plot_list[index].setManually(
                    x_val = '>'.join([root_key, 'Curve Axis', str(key)]), 
                    y_val = '>'.join([root_key, 'Curve', str(key)]), 
                    e_val = 'None')
                self.plot_list[index].scatter        = False
                self.plot_list[index].scatter_type   = 0
                self.plot_list[index].scatter_size   = 5
                self.plot_list[index].line           = True
                self.plot_list[index].line_thickness = 2
                self.plot_list[index].setColor(color_list[index%9])

                index += 1

        self._populatePlots()

        index = 0
        for j,root_key in enumerate([root_key for root_key in self.data_set.keys()]):
            for i,key in enumerate([key for key in self.data_set[root_key]['Parameters'].keys()]):
                self.plot_list[index+1].setLink(value ='>'.join([root_key, 'Parameters', str(key), 'y']))
                index += 2

    def getDataFromKey(self, formatted_key):
        '''
        Cycles through the key and returns the data
        '''
        key_list = formatted_key.split('>')
        data = self.data_set
        for key in key_list:
            try:
                data = data[key]
            except:
                data = data[float(key)]

        return data

    def removeAllPlotElement(self):        
        '''
        Remove all element by deleting the
        the list entry. Then 
        repopulate the list.
        '''
        self.plot_list = []
        self.plot_model.clear()
        
    def removePlotElement(self):        
        '''
        Remove an element by grabing its position in the 
        list and then deleting the list entry. Then 
        repopulate the list.
        '''
        if len(self.process_list_plot.selectedIndexes())>0:
            del self.plot_list[self.process_list_plot.selectedIndexes()[0].row()]

    def addPlotElement(self):        
        '''
        A plot element will be a construct containing 
        all the data and logic to create the plots
        '''
        stdItem = QtGui.QStandardItem('None')
        stdItem.setFlags(
            QtCore.Qt.ItemIsUserCheckable 
            | QtCore.Qt.ItemIsEnabled)
        check = QtCore.Qt.Checked 
        stdItem.setData(
            QtCore.QVariant(check), 
            QtCore.Qt.CheckStateRole)
        self.plot_model.appendRow(stdItem)
        self.plot_list.append(PlotItem(stdItem, self))
        self._populatePlots()

    def _grabPlotItem(self, index):
        
        if hasattr(self, 'current_item'):
            try:
                self.current_item.disconnectParent()
            except:
                pass

        self.current_item   = self.plot_list[index.row()]
        self.current_item.connectParent(self.parent)

    def _repopulateLinks(self):        
        '''
        Repopulate all the internal elements of the link 
        classes on name change
        '''
        for item in self.plot_list:
            item._updateLink()

    def _populatePlots(self):        
        '''
        Send out the information to the plots and
        then rebuild them
        '''
        if len(self.plot_list) > 0:
            for plot_element in self.plot_list:
                plot_element.x_keys = [key for key in self.data_sets_x.keys()]
                plot_element.y_keys = [key for key in self.data_sets_y.keys()]
                plot_element.e_keys = [key for key in self.data_sets_e.keys()]
            self._repopulateLinks()
            
            if len(self.process_list_plot.selectedIndexes()) > 0:
                self._grabPlotItem(self.process_list_plot.selectedIndexes()[0].row())



    def _processPlot(self):
        '''
        Plot the data from the plot elements
        '''
        plot_parameters = {}
        for element in self.plot_list:
            element_dict  = element._getPlotDict()
            if element_dict['actif']:
                plot_parameters[element.stdItem.text()] = element._getPlotDict()

        return plot_parameters
