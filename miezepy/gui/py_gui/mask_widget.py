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

from ...gui.qt_gui.mask_widget_ui import Ui_mask_widget

class MaskWidget(Ui_mask_widget,QtCore.QObject):
    '''
    This class will manage the raw import 
    machinery. the UI is inherited through 
    Ui_main_window from the Qt designer anf then
    converted through pyuic5
    '''
    mask_reset  = QtCore.pyqtSignal()
    mask_edited = QtCore.pyqtSignal()

    def __init__(self, parameters, item_widget):
        QtCore.QObject.__init__(self)
        Ui_mask_widget.__init__(self)
        self.widget = QtWidgets.QWidget()
        self.item_widget = item_widget
        self.setupUi(self.widget)
        self.parameters = parameters
        self.types = [
            'arc',
            'square',
            'triangle',
            'linear_comp',
            'radial_comp']

        self.child_types = self.types[0:3]

        self.mask_combo_type.addItems(self.types)
        self.mask_combo_type_child.addItems(self.child_types)

        self.equivalence = {
            'arc': self.buildArc,
            'square': self.buildSquare,
            'triangle': self.buildTriangle,
            'linear_comp': self.buildLinearComposition,
            'radial_comp': self.buildRadialComposition }

        self.mask_spin_position_0.setMinimum(-1000)
        self.mask_spin_position_0.setMaximum( 1000)
        self.mask_spin_position_1.setMinimum(-1000)
        self.mask_spin_position_1.setMaximum( 1000)
        self.mask_spin_angle.setMinimum(-1000)
        self.mask_spin_angle.setMaximum( 1000)
        self.mask_spin_angle_child.setMinimum(-1000)
        self.mask_spin_angle_child.setMaximum( 1000)

        self.initialize()
        self.connect_invariant()
        

    def initialize(self):
        '''
        initialize the widget and set the stage
        '''
        self.widgets        = []
        self.widgets_child  = []

        self.removeWidgets()
        self.equivalence[self.parameters[0]]()
        self.placeWidgets()

        self.removeWidgets(child = True)
        self.equivalence['arc'](child = True)
        self.placeWidgets(child = True)

        self.setValues()
        self.connect()

        self.checkChildToggle()

    def connect_invariant(self):
        '''
        connect the signals to their output
        '''
        self.mask_combo_type.currentIndexChanged.connect(self.changeType)
        self.mask_combo_type_child.currentIndexChanged.connect(self.changeChildType)

        self.mask_spin_position_0.valueChanged.connect(self.triggerGrab)
        self.mask_spin_position_1.valueChanged.connect(self.triggerGrab)
        self.mask_spin_angle.valueChanged.connect(self.triggerGrab)
        self.mask_spin_angle_child.valueChanged.connect(self.triggerGrab)
        self.mask_spin_angle_child.valueChanged.connect(self.triggerGrab)

    def connect(self):
        '''
        connect the signals to their output
        '''
        for i,row in enumerate(self.widgets):
            for j,element in enumerate(row):
                if isinstance(element, QtWidgets.QSpinBox):
                    element.valueChanged.connect(self.triggerGrab)
                elif isinstance(element, QtWidgets.QCheckBox):
                    element.stateChanged.connect(self.triggerGrab)

        for i,row in enumerate(self.widgets_child):
            for j,element in enumerate(row):
                if isinstance(element, QtWidgets.QSpinBox):
                    element.valueChanged.connect(self.triggerGrab)
                elif isinstance(element, QtWidgets.QCheckBox):
                    element.stateChanged.connect(self.triggerGrab)

    def changeType(self, idx):
        '''
        Change the type of the shape
        '''
        self.removeWidgets()
        self.equivalence[self.types[idx]]()
        self.placeWidgets()
        self.grabValues()
        self.connect()
        self.mask_reset.emit()

    def changeChildType(self, idx):
        '''
        Change the type of the shape
        '''
        self.removeWidgets(child = True)
        self.equivalence[self.child_types[idx]](child = True)
        self.placeWidgets(child = True)
        self.grabValues()
        self.connect()
        self.mask_reset.emit()

    def triggerGrab(self):
        '''
        Trigger the value grab abd notify the system
        '''
        self.grabValues()
        self.mask_edited.emit()

    def grabValues(self):
        '''
        Grab the values and build the 
        parameter array
        '''
        self.parameters = [self.types[self.mask_combo_type.currentIndex()]]
        self.parameters.append([
            self.mask_spin_position_0.value(),
            self.mask_spin_position_1.value()])
        self.parameters.append(self.mask_spin_angle.value())

        for widget_row in self.widgets:
            values = []
            for widget in widget_row:
                if isinstance(widget, QtWidgets.QLabel):
                    pass
                elif isinstance(widget, QtWidgets.QSpinBox):
                    values.append(widget.value())
            if len(values) == 1:
                self.parameters.append(values[0])
            else:
                self.parameters.append(values)

        if 'comp' in self.types[self.mask_combo_type.currentIndex()]:
            child_parameters = [
                self.child_types[self.mask_combo_type_child.currentIndex()],
                [0,0],
                self.mask_spin_angle_child.value()]
            for widget_row in self.widgets_child:
                values = []
                for widget in widget_row:
                    if isinstance(widget, QtWidgets.QLabel):
                        pass
                    elif isinstance(widget, QtWidgets.QSpinBox):
                        values.append(widget.value())
                    elif isinstance(widget, QtWidgets.QCheckBox):
                        values.append(widget.isChecked())
                if len(values) == 1:
                    child_parameters.append(values[0])
                else:
                    child_parameters.append(values)
            self.parameters.append(child_parameters)

    def setValues(self, child = False):
        '''
        Set the value sin the widget.
        '''
        self.mask_combo_type.setCurrentIndex(self.types.index(self.parameters[0]))
        self.mask_spin_position_0.setValue(self.parameters[1][0])
        self.mask_spin_position_1.setValue(self.parameters[1][1])
        self.mask_spin_angle.setValue(self.parameters[2])

        if child:
            target = self.widgets_child
        else:
            target = self.widgets

        for i, widget_row in enumerate(target):

            if isinstance(widget_row[2], QtWidgets.QLabel):
                if isinstance(widget_row[1], QtWidgets.QSpinBox):
                    widget_row[1].setValue(self.parameters[i + 3])
            else:
                for j,widget in enumerate(widget_row):
                    if isinstance(widget, QtWidgets.QLabel):
                        pass
                    elif isinstance(widget, QtWidgets.QSpinBox):
                        widget.setValue(self.parameters[i + 3][j - 1])

    def placeWidgets(self, child = False):
        '''
        Place the widgets on the layout,
        '''
        if child:
            target = self.widgets_child
            layout = self.mask_layout_para_grid_child
        else:
            target = self.widgets
            layout = self.mask_layout_para_grid
        for i,row in enumerate(target):
            for j,element in enumerate(row):
                layout.addWidget(element, i, j)
                if isinstance(element, QtWidgets.QLabel):
                    element.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                elif isinstance(element, QtWidgets.QSpinBox):
                    element.setMinimum(-1000)
                    element.setMaximum( 1000)

                element.setFont(QtGui.QFont(".SF NS Text", 10))
                element.resize(50,21)
        self.checkChildToggle()

    def checkChildToggle(self):
        '''
        Shall we expand the widget
        '''
        if 'comp' in self.types[self.mask_combo_type.currentIndex()]:
            self.mask_box_child.setVisible(True)
            self.widget.resize(400,250)

        else:
            self.mask_box_child.setVisible(False)
            self.widget.resize(400,150)

        self.item_widget.setSizeHint(self.widget.size())

    def removeWidgets(self, child = False):
        '''
        Remove the widgets from the layout so 
        that new ones can eb created.
        '''
        if child:
            for i in reversed(range(self.mask_layout_para_grid_child.count())): 
                self.mask_layout_para_grid_child.itemAt(i).widget().deleteLater()
            self.widgets_child = []

        else:
            for i in reversed(range(self.mask_layout_para_grid.count())): 
                self.mask_layout_para_grid.itemAt(i).widget().deleteLater()
            self.widgets = []

    def buildArc(self, child = False):
        '''
        Build the items according to their 
        types.
        '''
        if child:
            target = self.widgets_child
        else:
            target = self.widgets

        target.append([
            QtWidgets.QLabel('Radial range:', parent=self.widget), 
            QtWidgets.QSpinBox(parent=self.widget),
            QtWidgets.QSpinBox(parent=self.widget)])

        target.append([
            QtWidgets.QLabel('Angular range:', parent=self.widget), 
            QtWidgets.QSpinBox(parent=self.widget),
            QtWidgets.QSpinBox(parent=self.widget)])

        if child:
            target.append([
                QtWidgets.QCheckBox('Close gap', parent = self.widget),
                QtWidgets.QCheckBox('Increment', parent = self.widget),
                QtWidgets.QCheckBox('Exclude', parent = self.widget)])

    def buildSquare(self, child = False):
        '''
        Build the items according to their 
        types.
        '''
        if child:
            target = self.widgets_child
        else:
            target = self.widgets

        target.append([
            QtWidgets.QLabel('Width:', parent=self.widget), 
            QtWidgets.QSpinBox(parent=self.widget),
            QtWidgets.QLabel('', parent=self.widget)])

        target.append([
            QtWidgets.QLabel('Height:', parent=self.widget), 
            QtWidgets.QSpinBox(parent=self.widget),
            QtWidgets.QLabel('', parent=self.widget)])

        if child:
            target.append([
                QtWidgets.QCheckBox('Close gap', parent = self.widget),
                QtWidgets.QCheckBox('Increment', parent = self.widget),
                QtWidgets.QCheckBox('Exclude', parent = self.widget)])


    def buildTriangle(self, child = False):
        '''
        Build the items according to their 
        types.
        '''
        if child:
            target = self.widgets_child
        else:
            target = self.widgets

        target.append([
            QtWidgets.QLabel('Base:', parent=self.widget), 
            QtWidgets.QSpinBox(parent=self.widget),
            QtWidgets.QLabel('', parent=self.widget)])

        target.append([
            QtWidgets.QLabel('Height:', parent=self.widget), 
            QtWidgets.QSpinBox(parent=self.widget),
            QtWidgets.QLabel('', parent=self.widget)])

        if child:
            target.append([
                QtWidgets.QCheckBox('Close gap', parent = self.widget),
                QtWidgets.QCheckBox('Increment', parent = self.widget),
                QtWidgets.QCheckBox('Exclude', parent = self.widget)])

    def buildLinearComposition(self, child = False):
        '''
        Build the items according to their 
        types.
        '''
        target = self.widgets

        target.append([
            QtWidgets.QLabel('Horizontal multiplicity:', parent=self.widget), 
            QtWidgets.QSpinBox(parent=self.widget),
            QtWidgets.QLabel('', parent=self.widget)])

        target.append([
            QtWidgets.QLabel('Vertical multiplicity:', parent=self.widget), 
            QtWidgets.QSpinBox(parent=self.widget),
            QtWidgets.QLabel('', parent=self.widget)])

        target.append([
            QtWidgets.QLabel('Width:', parent=self.widget), 
            QtWidgets.QSpinBox(parent=self.widget),
            QtWidgets.QLabel('', parent=self.widget)])

        target.append([
            QtWidgets.QLabel('Height:', parent=self.widget), 
            QtWidgets.QSpinBox(parent=self.widget),
            QtWidgets.QLabel('', parent=self.widget)])


    def buildRadialComposition(self):
        '''
        Build the items according to their 
        types.
        '''
        target = self.widgets

        target.append([
            QtWidgets.QLabel('Radial multiplicity:', parent=self.widget), 
            QtWidgets.QSpinBox(parent=self.widget),
            QtWidgets.QLabel('', parent=self.widget)])

        target.append([
            QtWidgets.QLabel('Angular multiplicity:', parent=self.widget), 
            QtWidgets.QSpinBox(parent=self.widget),
            QtWidgets.QLabel('', parent=self.widget)])

        target.append([
            QtWidgets.QLabel('Radius range:', parent=self.widget), 
            QtWidgets.QSpinBox(parent=self.widget),
            QtWidgets.QSpinBox(parent=self.widget)])

        target.append([
            QtWidgets.QLabel('Angular range:', parent=self.widget), 
            QtWidgets.QSpinBox(parent=self.widget),
            QtWidgets.QSpinBox(parent=self.widget)])
