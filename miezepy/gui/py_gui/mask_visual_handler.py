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
from functools import partial

class MaskVisualHandler(QtCore.QObject):
    mask_updated = QtCore.pyqtSignal()
    drop_updated = QtCore.pyqtSignal()

    def __init__(self):
        '''
        
        '''
        QtCore.QObject.__init__(self)
        self.model = QtGui.QStandardItemModel(0,3)
        self.views = {}
        self.drops = {}
        self.current_edit_widget = None
        self.current_item = None
        self.process_dict = {
            'rectangle': self._processRectangle,
            'arc':self._processArc,
            'triangle':self._processTriangle,
            'linear composition':self._processLinearComp,
            'radial composition':self._processRadialComp}
        self.selectables = [
            'rectangle',
            'arc',
            'triangle',
            'linear composition',
            'radial composition']

    def link(self, mask_core):
        '''
        link the model to the mask core and initiate the 
        process
        '''
        self.mask_core = mask_core
        self.setModel()

    def setModel(self):
        '''
        Populate the model after clearing it of all
        the data at hand.
        '''
        self.clearItemChildren(self.model)
        current_dict = self.mask_core.mask_dict[self.mask_core.current_mask]
        for idx,element in enumerate(current_dict):
            self._processElement(idx, element)

    def _processElement(self, idx, element):
        '''
        Process all elements of the given mask
        elements with the customized mask routine
        '''
        item = ParentMaskType(element[0]+' '+str(idx), self.selectables)
        self.process_dict[element[0]](item, element)
        self.model.appendRow(item)

    def _processArc(self, item, element = None):
        '''
        Process the creation of an arc element
        in the tree
        '''
        if element == None:
            element = ['',[64,64],0,[0,10],[0,360]]
        ChildRange(item, 'Position (x,y)', element[1], -100000, 100000)
        ChildValue(item, 'Angle', element[2], -360, 360)
        ChildRange(item, 'Radial range (min,max)', element[3], -100000, 100000)
        ChildRange(item, 'Angle range (min,max)', element[4], -100000, 100000)

    def _processTriangle(self, item, element = None):
        '''
        Process the creation of an arc element
        in the tree
        '''
        if element == None:
            element = ['',[64,64],0,10,10]
        ChildRange(item, 'Position (x,y)', element[1], -100000, 100000)
        ChildValue(item, 'Angle', element[2], -360, 360)
        ChildValue(item, 'Base', element[3], -100000, 100000)
        ChildValue(item, 'Height', element[4], -100000, 100000)

    def _processRectangle(self, item, element = None):
        '''
        Process the creation of an arc element
        in the tree
        '''
        if element == None:
            element = ['',[64,64],0,10,10]
        ChildRange(item, 'Position (x,y)', element[1], -100000, 100000)
        ChildValue(item, 'Angle', element[2], -360, 360)
        ChildValue(item, 'Width', element[3], -100000, 100000)
        ChildValue(item, 'Height', element[4], -100000, 100000)

    def _processLinearComp(self, item, element = None):
        '''
        Process the creation of an arc element
        in the tree
        '''
        if element == None:
            element = ['',[64,64],0,3,3,50,50, ['rectangle',[0,0],0,10,10, [True, True, False]]]
        ChildRange(item, 'Position (x,y)', element[1], -100000, 100000)
        ChildValue(item, 'Angle', element[2], -360, 360)
        ChildRange(item, 'Multiplicity (x,y)', [element[3],element[4]], -100000, 100000)
        ChildValue(item, 'Width', element[5], -100000, 100000)
        ChildValue(item, 'Height', element[6], -100000, 100000)
        subitem = ParentMaskType(element[7][0]+' '+str('child'), self.selectables[0:3])
        self.process_dict[element[7][0]](subitem, element[7])
        item.appendRow(subitem)
        ChildBool(item, 'Increment', element[7][-1][0])
        ChildBool(item, 'Close gap', element[7][-1][1])

    def _processRadialComp(self, item, element = None):
        '''
        Process the creation of an arc element
        in the tree
        '''
        if element == None:
            element = ['',[64,64],0,3,3,[50,100],[50,100], ['arc',[0,0],0,[10,20],[10,20], [True, True, False]]]
        ChildRange(item, 'Position (x,y)', element[1], -100000, 100000)
        ChildValue(item, 'Angle', element[2], -360, 360)
        ChildRange(item, 'Multiplicity (x,y)', [element[3],element[4]], -100000, 100000)
        ChildRange(item, 'Angle range (min,max)', element[5], -100000, 100000)
        ChildRange(item, 'Radial range (min,max)', element[6], -100000, 100000)
        subitem = ParentMaskType(element[7][0]+' '+str('child'), self.selectables[0:3])
        self.process_dict[element[7][0]](subitem, element[7])
        item.appendRow(subitem)
        ChildBool(item, 'Increment', element[7][-1][0])
        ChildBool(item, 'Close gap', element[7][-1][1])

    def clearItemChildren(self, item):
        '''
        clear all the items that are children to the 
        given master
        '''
        item.removeRows(0, item.rowCount())

    def connectView(self, name, view):
        '''
        Connect a tree to a model and to the 
        event management
        '''
        self.views[name] = view
        self.views[name].setModel(self.model)
        self.views[name].clicked.connect(partial(self._processClick, name))
        self.views[name].expanded.connect(partial(self._resizeColumn, name))

    def connectDrop(self, name, drop):
        '''
        Connect a dropdown to here to allow 
        controll over its functionalities
        '''
        self.drops[name] = drop
        self.drops[name].currentIndexChanged.connect(partial(self.setDrops, name))

    def setDrops(self, name):
        '''
        Manage the dropdowns locally
        '''
        drop = self.drops[name]
        index = drop.currentIndex()
        if index < len(self.mask_core.mask_dict.keys()):
            self.mask_core.setMask(drop.currentText())
            self.setModel()
            self.generateMask()
            self.setDropText()

    def setDropText(self):
        '''
        Manage the dropdowns locally
        '''
        index = [key for key in self.mask_core.mask_dict.keys()].index(self.mask_core.current_mask)
        for key in self.drops.keys():
            self.drops[key].blockSignals(True)
            self.drops[key].setCurrentIndex(index)
            self.drops[key].blockSignals(False)

    def setDropItems(self, item_list):
        '''
        Manage the dropdowns locally
        '''
        for key in self.drops.keys():
            self.drops[key].blockSignals(True)
            self.drops[key].clear()
            self.drops[key].addItems(item_list)
            self.drops[key].blockSignals(False)

        self.drop_updated.emit()

    def _processClick(self, name, model_index):
        '''
        Process the click of an item of the model
        on the treeview. This will then cascade through
        and allow the creation of a widget in place
        '''
        if not self.current_item == None:
            self._focusOut()
        #locally save the elements
        self.current_item = self.model.itemFromIndex(model_index)
        if not hasattr( self.current_item, 'identifier'):
            self.current_item = None
            return None

        if not self.current_item.identifier in ['spin_int', 'spin_float', 'drop', 'bool']:
            self.current_item = None
            return None

        if self.current_item.identifier == 'spin_int':
            self.current_edit_widget = SpinIntFocusTracker(parent = self.views[name])
            self.current_edit_widget.setRange(*self.current_item.ranges)
            self.current_edit_widget.setValue(self.current_item.getValue())
            self.current_edit_widget.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)  
        elif self.current_item.identifier == 'spin_float':
            self.current_edit_widget = SpinFloatFocusTracker(parent = self.views[name])
            self.current_edit_widget.setRange(*self.current_item.ranges)
            self.current_edit_widget.setValue(self.current_item.getValue())
            self.current_edit_widget.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)  
        elif self.current_item.identifier == 'drop':
            self.current_edit_widget = DropFocusTracker(parent = self.views[name])
            self.current_edit_widget.addItems(self.current_item.selectables)
            self.current_edit_widget.setCurrentText(self.current_item.value)
        elif self.current_item.identifier == 'bool':
            self.generateMask()
            self.current_item = None
            return None
        else:
            return None

        self.current_index = model_index
        self.current_view = name
        #set up the widget
        self.views[name].setIndexWidget(model_index,self.current_edit_widget)
        if len(self.current_item.identifier.split('spin')) > 1:
            self.current_edit_widget.valueChanged.connect(self._updateValues)
        elif self.current_item.identifier == 'drop':
            self.current_edit_widget.showPopup()
            self.current_edit_widget.currentIndexChanged.connect(self._updateValues)

        #connect the out of focus
        self.current_edit_widget.lostFocus.connect(self._focusOut)

    def _updateValues(self):
        '''
        update the values of the given item
        on his change. The item will handle the methods
        to be used
        '''
        self.current_item.setValue(self.current_edit_widget)
        if self.current_item.identifier == 'drop':
            self.clearItemChildren(self.current_item)
            self.process_dict[self.current_edit_widget.currentText()](self.current_item)
            self._destruction()

        self.generateMask()

    def _focusOut(self):
        '''
        Fix the focus out method to handle the leaving of the 
        current item
        '''
        self._updateValues()
        self._destruction()

    def _destruction(self):
        '''
        destroy the widget elements
        '''
        self.views[self.current_view].setIndexWidget(self.current_index,None)
        self.current_edit_widget.deleteLater()
        self.current_item = None

    def _resizeColumn(self, name):
        '''
        Resize the content of the column to match
        the size of the text
        '''
        self.views[name].resizeColumnToContents(0)

    def generateMask(self):
        '''
        generate the final dictionary to be sent out to the 
        mask manager and then be processed.
        '''
        elements = []
        for row in range(self.model.rowCount()):
            temp_element = []
            item = self.model.item(row)
            temp_element.append(' '.join(item.text().split(' ')[:-1]))
            for subrow in range(item.rowCount()):
                if item.child(subrow).identifier == 'value':
                    temp_element.append(float(item.child(subrow, 1).text()))
                elif item.child(subrow).identifier == 'range':
                    if 'Multiplicity' in item.child(subrow).text():
                        temp_element.append(float(item.child(subrow, 1).text()))
                        temp_element.append(float(item.child(subrow, 2).text()))
                    else:
                        temp_element.append([
                            float(item.child(subrow, 1).text()), 
                            float(item.child(subrow, 2).text())])
                elif item.child(subrow).identifier == 'drop':
                    sub_sub_item = item.child(subrow)
                    sub_temp_element = [' '.join(sub_sub_item.text().split(' ')[:-1])]
                    for subsubrow in range(sub_sub_item.rowCount()):
                        if sub_sub_item.child(subsubrow).identifier == 'value':
                            sub_temp_element.append(float(sub_sub_item.child(subsubrow, 1).text()))
                        elif sub_sub_item.child(subsubrow).identifier == 'range':
                            sub_temp_element.append([
                                float(sub_sub_item.child(subsubrow, 1).text()), 
                                float(sub_sub_item.child(subsubrow, 2).text())])
                    sub_temp_element.append([False, False, False])
                    temp_element.append(sub_temp_element)
                elif item.child(subrow).identifier == 'bool':
                    if item.child(subrow).text() == 'Increment':
                        temp_element[-1][-1][1] = (item.child(subrow).checkState() == QtCore.Qt.Checked)
                    elif item.child(subrow).text() == 'Close gap':
                        temp_element[-1][-1][0] = (item.child(subrow).checkState() == QtCore.Qt.Checked)
            elements.append(temp_element)
        self.mask_core.mask_dict[self.mask_core.current_mask] = list(elements)
        self.mask_updated.emit()


'''
######################################################
Basic implementation of some variable standart items
'''
class DropItem(QtGui.QStandardItem):

    def __init__(self, value, selectables):
        '''
        set default basis
        '''
        QtGui.QStandardItem.__init__(self)
        self.identifier     = 'drop'
        self.selectables    = selectables
        self.value          = value        
        self.setEditable(False)

    def setValue(self, drop):
        '''
        grab the value from the spinbox
        '''
        self.value = self.selectables[drop.currentIndex()]
        self.setText(" ".join([self.value]+[self.text().split(' ')[-1]]))

    def getValue(self):
        '''
        provide the value to the requester
        '''
        return self.value

class SpinIntItem(QtGui.QStandardItem):

    def __init__(self, value, range_min, range_max):
        '''
        set default basis
        '''
        QtGui.QStandardItem.__init__(self)
        self.identifier = 'spin_int'
        self.ranges     = [range_min, range_max]
        self.value      = value
        self.setEditable(False)
        self.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

    def setValue(self, spinbox):
        '''
        grab the value from the spinbox
        '''
        self.value = spinbox.value()
        self.setText(str(spinbox.value()))

    def getValue(self):
        '''
        provide the value to the requester
        '''
        return self.value

class SpinDoubleItem(QtGui.QStandardItem):

    def __init__(self, value, range_min, range_max):
        '''
        set default basis
        '''
        QtGui.QStandardItem.__init__(self)
        self.identifier = 'spin_float'
        self.ranges     = [range_min, range_max]
        self.value      = value    
        self.setEditable(False)
        self.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

    def setValue(self, spinbox):
        '''
        grab the value from the spinbox
        '''
        self.value = spinbox.value()
        self.setText(str(spinbox.value()))
        
    def getValue(self):
        '''
        provide the value to the requester
        '''
        return self.value

'''
######################################################
Basic implementation of some fixed standart items
'''
class ParentMaskType(DropItem):

    def __init__(self, value, selectables):

        #set default basis
        DropItem.__init__(self, ' '.join(value.split(' ')[:-1]), selectables)
        self.setText(value)

class ChildRange(QtGui.QStandardItem):

    def __init__(self, parent, name, values, range_min, range_max):

        #set default basis
        QtGui.QStandardItem.__init__(self, 0, 0)
        self.identifier = 'range'
        self.setText(name)
        self.setEditable(False)
        #set associated items
        if 'Position' in name or 'Multiplicity' in name:
            self.min_item = SpinIntItem(values[0], range_min, range_max)
            self.max_item = SpinIntItem(values[1], range_min, range_max)
            self.min_item.setText(str(values[0]))
            self.max_item.setText(str(values[1]))
        else:
            self.min_item = SpinDoubleItem(values[0], range_min, range_max)
            self.max_item = SpinDoubleItem(values[1], range_min, range_max)
            self.min_item.setText(str(values[0]))
            self.max_item.setText(str(values[1]))
        #populate
        parent.appendRow([self, self.min_item, self.max_item])

class ChildValue(QtGui.QStandardItem):

    def __init__(self, parent, name, values, range_min, range_max):

        #set default basis
        QtGui.QStandardItem.__init__(self, 0, 2)
        self.identifier = 'value'
        self.setText(name)
        self.setEditable(False)
        #set associated items
        self.val_item = SpinDoubleItem(values, range_min, range_max)
        self.val_item.setText(' '+str(values))
        #populate
        parent.appendRow([self, self.val_item])

class ChildBool(QtGui.QStandardItem):

    def __init__(self, parent, name, value):
        QtGui.QStandardItem.__init__(self, 0, 3)
        self.identifier = 'bool'
        self.setText(name)
        self.setCheckable(True)
        self.setEditable(False)
        check = QtCore.Qt.Checked if value else QtCore.Qt.Unchecked
        self.setData(QtCore.QVariant(check), QtCore.Qt.CheckStateRole)
        parent.appendRow(self)

'''
######################################################
Basic implementation of some items with focus tracking
'''
class SpinIntFocusTracker(QtWidgets.QSpinBox):
    lostFocus = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QSpinBox.__init__(self, parent=parent)

    def focusOutEvent(self, event):
        self.lostFocus.emit()
    
class SpinFloatFocusTracker(QtWidgets.QDoubleSpinBox):
    lostFocus = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QDoubleSpinBox.__init__(self, parent=parent)

    def focusOutEvent(self, event):
        self.lostFocus.emit()

class DropFocusTracker(QtWidgets.QComboBox):
    lostFocus = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QComboBox.__init__(self, parent=parent)

    def focusOutEvent(self, event):
        self.lostFocus.emit()