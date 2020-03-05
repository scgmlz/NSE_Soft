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

from simpleplot.models.session_node          import SessionNode
from simpleplot.models.parameter_class       import ParameterHandler
from simpleplot.models.delegates             import ParameterDelegate
from simpleplot.models.widget_constructors   import comboBoxConstructor

from .mask_tree_view    import MaskTreeView
from .mask_model        import MaskModel
from .mask_node         import MaskNode

import sys

class MaskInterface(QtCore.QObject):
    mask_updated = QtCore.pyqtSignal()
    drop_updated = QtCore.pyqtSignal()
    about_to_add = QtCore.pyqtSignal()
    about_to_remove = QtCore.pyqtSignal()
    finished_modifications = QtCore.pyqtSignal()

    def __init__(self):
        '''
        '''
        QtCore.QObject.__init__(self)
        self._rootNode      = SessionNode('Mask')
        self._mask_model    = MaskModel(self._rootNode)
        self._item_model    = QtGui.QStandardItemModel()
        self.combo_ptrs_signal  = []
        self.combo_ptrs_silent  = []
        self._mask_core      = None
        self._connect()

    def link(self, mask_core):
        self._mask_core = mask_core
        self._refreshItemModel()
        self._refreshMaskModel(self._mask_core.current_mask)
        
    def _refreshItemModel(self):
        '''
        Refresh the models used by the 
        comboboxes.
        '''
        for combo in self.combo_ptrs_signal:
            combo.blockSignals(True)

        for combo in self.combo_ptrs_silent:
            combo.blockSignals(True)

        self._item_model.clear()
        
        string_items = [
            key for key in 
            self._mask_core.mask_dict.keys()]

        for i,string in enumerate(string_items):
            self._item_model.insertRow(
                i, QtGui.QStandardItem(string))

        for combo in self.combo_ptrs_signal:
            combo.blockSignals(False)

        for combo in self.combo_ptrs_silent:
            combo.blockSignals(False)

    def _comboboxSet(self, idx):
        '''
        filter actions on combobox press
        '''
        if idx >= 0 and idx <= self._item_model.rowCount()-1:
            self._refreshMaskModel([
            key for key in 
            self._mask_core.mask_dict.keys()][idx])
        else: 
            self._refreshMaskModel([
            key for key in 
            self._mask_core.mask_dict.keys()][0])

    def insertNewMask(self, key):
        '''
        Upon completion the combobox
        will return the text as a key to 
        create a new mask
        '''
        if not key == '':
            name = self._mask_core.addMask(key)
            self._refreshItemModel()
            self._refreshMaskModel(key)
            idx = [key for key in self._mask_core.mask_dict.keys()].index(name)
            self._comboboxSet(idx)

    def _refreshMaskModel(self, key):
        '''
        Refresh the models used by the 
        comboboxes.
        '''
        self.about_to_add.emit()
        self._setAllCombos(key)
        self._mask_core.setMask(key)
        
        if not self._rootNode.childCount() == 0:
            self._mask_model.removeRows(
                0, self._rootNode.childCount(),
                self._rootNode)

        if key is None:
            self.finished_modifications.emit()
            self._generateMaskDict()

        mask_list = self._mask_core.mask_dict[key]
        for mask_item in mask_list:
            model_item = MaskNode()
            self._mask_model.insertRows(0,1,[model_item], self._rootNode)
            self._mask_model.referenceModel()
            model_item._value = mask_item['Type']
            model_item.typeChanged()
            model_item.setParameters(mask_item)

        self.finished_modifications.emit()
        self._generateMaskDict()

    def _connect(self):
        '''
        Connect the routines
        '''
        self._mask_model.dataChanged.connect(self._checkBeforeProcess)

    def _disconnect(self):
        '''
        Disconnect the routines
        '''
        try:
            self._mask_model.dataChanged.disconnect(self._checkBeforeProcess)
        except:
            pass

    def _connectCombos(self):
        '''
        connect all the signals to the methods
        for reprocessing tree and model changes
        '''
        for combo in self.combo_ptrs_signal:
            try:
                combo.currentIndexChanged.connect(self._comboboxSet)
            except:
                pass

    def _setAllCombos(self, key):
        '''
        Set all the combos to the same value to avoid confusing
        later on
        '''
        for combo in self.combo_ptrs_signal:
            try:
                combo.blockSignals(True)
                combo.setCurrentText(key)
                combo.blockSignals(False)
            except:
                pass

    def _disconnectCombos(self):
        '''
        connect all the signals to the methods
        for reprocessing tree and model changes
        '''
        for combo in self.combo_ptrs_signal:
            try:
                combo.currentIndexChanged.disconnect(self._comboboxSet)
            except:
                pass

    def _connectCombosEdit(self):
        '''
        connect all the signals to the methods
        for reprocessing tree and model changes
        '''
        for combo in self.combo_ptrs_signal:
            try:
                combo.editing_finished.connect(self._comboEditManager)
                combo.editing_aborted.connect(self._comboAbortManager)
                combo.currentIndexChanged.connect(self._comboAbortManager)
            except:
                pass

    def _disconnectCombosEdit(self):
        '''
        disconnect all the signals to the methods
        for reprocessing tree and model changes
        '''
        for combo in self.combo_ptrs_signal:
            try:
                combo.editing_finished.disconnect(self._comboEditManager)
                combo.editing_aborted.disconnect(self._comboAbortManager)
                combo.currentIndexChanged.disconnect(self._comboAbortManager)
            except:
                pass

    def addItem(self):
        '''
        Add a major node item representing the
        mask elements
        '''
        self.about_to_add.emit()

        model_item = MaskNode()
        self._mask_model.insertRows(0,1,[model_item], self._rootNode)
        self._mask_model.referenceModel()
        model_item.typeChanged()

        self._generateMaskDict()
        self.finished_modifications.emit()

        return model_item

    def removeItem(self, row):
        '''
        Add a major node item representing the
        mask element
        '''
        self.about_to_remove.emit()

        self._mask_model.removeRows(row, 1, self._rootNode)
        self._generateMaskDict()

        self.finished_modifications.emit()
        
    def removeCurrentMask(self):
        '''
        Add a major node item representing the
        mask elements
        '''
        self._mask_core.removeMask(self._mask_core.current_mask)
        self._refreshItemModel()
        self._comboboxSet(0)

    def getTreeView(self):
        '''
        return a predefined and connected
        custom treeview
        '''
        tree_view = MaskTreeView()
        tree_view.setModel(self._mask_model)

        self.about_to_add.connect(tree_view.saveState)
        self.about_to_remove.connect(tree_view.saveState)
        self.finished_modifications.connect(tree_view.restoreState)

        return tree_view

    def getComboBox(self, connect = True):
        '''
        return a predefined and connected
        custom treeview
        '''
        combobox = MaskComboBox()
        combobox.setModel(self._item_model)

        if not self._mask_core == None and connect:
            combobox.setCurrentText(self._mask_core.current_mask)

        if connect:
            combobox.currentIndexChanged.connect(self._comboboxSet)
            self.combo_ptrs_signal.append(combobox)
        else:
            self.combo_ptrs_silent.append(combobox)

        return combobox

    def _checkBeforeProcess(self, index):
        if not self._mask_model.data(index, role = QtCore.Qt.DisplayRole) == None:
            self._generateMaskDict()

    def _generateMaskDict(self):
        '''
        grab all data form the dictionaries and 
        then send it to the mas class 
        '''
        if self._mask_model._update:
            masks_dictionaries = []
            for child in self._rootNode._children:
                masks_dictionaries.append(child.synthesize())
            self._mask_core.mask_dict[self._mask_core.current_mask] = masks_dictionaries
            self.mask_updated.emit()

class MaskComboBox(QtWidgets.QComboBox):
    '''
    This is our own combobox method
    '''
    editing_finished = QtCore.pyqtSignal(str)
    editing_aborted = QtCore.pyqtSignal()

    def __init__(self,parent = None):
        super().__init__(parent = parent)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Enter or QKeyEvent.key() == QtCore.Qt.Key_Return:
            self.editing_finished.emit(self.currentText())
        elif QKeyEvent.key() == QtCore.Qt.Key_Escape:
            self.editing_aborted.emit()
        elif QKeyEvent.key() == QtCore.Qt.Key_Up:
            self.editing_aborted.emit()
        elif QKeyEvent.key() == QtCore.Qt.Key_Down:
            self.editing_aborted.emit()
        elif QKeyEvent.key() == QtCore.Qt.Key_Left:
            self.editing_aborted.emit()
        elif QKeyEvent.key() == QtCore.Qt.Key_Right:
            self.editing_aborted.emit()
        else:
            super().keyPressEvent(QKeyEvent)

if __name__ == '__main__':
    from ....core.module_mask import MaskStructure
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mask = MaskStructure()
    interface = MaskInterface()
    interface.link(mask)
    interface.addItem()
    interface.addItem()
    interface.addItem()
    tree_1 = interface.getTreeView()
    tree_2 = interface.getTreeView()
    combo_1 = interface.getComboBox()
    combo_2 = interface.getComboBox()

    tree_1.show()
    tree_2.show()
    combo_1.show()
    combo_2.show()

    sys.exit(app.exec())