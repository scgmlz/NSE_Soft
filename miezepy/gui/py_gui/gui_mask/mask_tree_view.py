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

from simpleplot.models.delegates import ParameterDelegate
from simpleplot.models.session_node import SessionNode
from .mask_model   import MaskModel

class MaskTreeView(QtWidgets.QTreeView):
    def __init__(self, parent = None):
        '''
        '''
        super().__init__(parent = parent)
        self.initialize()
        sizePolicy = QtWidgets.QSizePolicy(
        QtWidgets.QSizePolicy.Expanding, 
        QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)

    def initialize(self):
        '''
        Initialise the parameter such as the 
        delegate from the parameter class
        of simpleplot

        connect the expand and colapse routines
        to the resizing

        set up a dummy model
        '''
        self.delegate = ParameterDelegate()
        self.setItemDelegate(self.delegate)
        
        self.collapsed.connect(self.resizeTree)
        self.expanded.connect(self.resizeTree)

        self.states = {'expanded':True}
        self._rootNode  = SessionNode('Mask')
        self._model = MaskModel(self._rootNode)
        self.setModel(self._model)
        self._connect()

    def setModel(self, model):
        '''
        override the setModel of the default
        inheritance while still calling it at
        the end
        '''
        try:
            self._disconnect()
        except:
            pass
        model.referenceModel()
        super().setModel(model)
        self._connect()

    def _connect(self):
        '''
        connect all the signals to the methods
        for reprocessing tree and model changes
        '''
        self.collapsed.connect(self.notifyColapse)
        self.expanded.connect(self.notifyExpanse)

    def _disconnect(self):
        '''
        disconnect all the signals to the methods
        for reprocessing tree and model changes
        '''
        self.collapsed.disconnect(self.notifyColapse)
        self.expanded.disconnect(self.notifyExpanse)

    def resizeTree(self, index):
        '''
        keep the first and second column fit to content
        '''
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)

    def notifyExpanse(self, index):
        '''
        On expanding save the location
        '''
        index_list = self.getIndex(index)
        self.setState(True, index_list)

    def notifyColapse(self, index):
        '''
        On expanding remove the location
        '''
        index_list = self.getIndex(index)
        self.setState(False, index_list)

    def getIndex(self, index):
        '''
        Get the list of row values in respect
        to the parents of the given child. This 
        allows to build the dictionary that will 
        keep track of the expanded states
        '''
        index_list = []
        row_val = 0
        while not row_val == -1:
            row_val = index.row()
            index_list.append(row_val)
            index = index.parent()

        index_list = index_list[:-1]
        index_list = index_list[::-1]
        return index_list

    def setState(self,value, index_list):
        '''
        Set the state of the expansion in a custom
        generated dictionary.
        '''
        if value == True:
            state = self.states
            for i in index_list:
                if not i in state.keys():
                    state[i] = {}
                state = state[i]
            state['expanded'] = True
        else:
            state = self.states
            for i in index_list[:-1]:
                state = state[i]
            try:
                del state[index_list[-1]]
            except:
                pass

    def restoreState(self):
        '''
        Restore the states from the dictionary 
        to allow a more pleasent sue of the 
        treeview widget
        '''
        self._disconnect()
        self.recursiveRestore(self.states, self.model()._rootNode)
        self._connect()

    def recursiveRestore(self,state_dict, node):
        '''
        Run through the model to identify
        the indexes in the treeview to 
        restore.
        '''
        index_list = list([key for key in state_dict.keys()])
        try:
            index_list.remove('expanded')
        except:
            pass
        for index in index_list:
            if index < node.childCount():
                child = node.child(index)
                self.expand(self.model().createIndex(index, 0, child))
                child_state = state_dict[index]
                self.recursiveRestore(child_state, child)

            else:
                del state_dict[index]

    def getSelected(self):
        '''
        return the selected index of the 
        view to prepare for removal
        '''
        return self.selectedIndexes()[0]

    def saveState(self):
        self.saved_states = dict(self.states)