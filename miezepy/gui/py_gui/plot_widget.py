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

from ..qt_gui.plot_widget_ui import Ui_PlotWidget
class PlotItem(Ui_PlotWidget):
     
    def __init__(self):
        Ui_PlotWidget.__init__(self)
        self._initialValues()

    def _initialValues(self):
        self.x_keys         = ['None']
        self.y_keys         = ['None']
        self.e_keys         = ['None']
        self.link_keys      = ['None']
        self.x_val          = 'None'
        self.y_val          = 'None'
        self.e_val          = 'None'

        self.active         = True
        self.expanded       = False
        self.link           = 'None'
        self.offset         = 0
        self.color          = QtGui.QColor('b')

        self.scatter        = True
        self.scatter_type   = 0
        self.scatter_types  = ['o','s','t','d']
        self.scatter_size   = 5

        self.line           = True
        self.line_thickness = 2

    def createWidgets(self, parent, child):
        self.parent = parent
        self.child  = child

        self._prepare()
        self._createWidgets()
        self._populateWidgets()
        self._connectWidgets()

    def _prepare(self):
        if not 'None' in self.x_keys:
            self.x_keys = ['None'] + self.x_keys
        if not 'None' in self.y_keys:
            self.y_keys = ['None'] + self.y_keys
        if not 'None' in self.e_keys:
            self.e_keys = ['None'] + self.e_keys
        if not 'None' in self.link_keys:
            self.link_keys = ['None'] + self.link_keys

    def _createWidgets(self):
        self.widget = QtWidgets.QWidget()
        self.setupUi(self.widget)
        
    def _populateWidgets(self):
        self.child.setText(0, self.y_val)
        self._populateComboBoxes()
        self._populateFields()
        self._populateCheckBoxes()

    def _populateComboBoxes(self):
        self.x_input.clear()
        self.x_input.addItems(self.x_keys)
        if not self.x_val in self.x_keys:
            self.x_val = 'None'
        self.x_input.setCurrentIndex(self.x_keys.index(self.x_val))

        self.y_input.clear()
        self.y_input.addItems(self.y_keys)
        if not self.y_val in self.y_keys:
            self.y_val = 'None'
        self.y_input.setCurrentIndex(self.y_keys.index(self.y_val))

        self.error_input.clear()
        self.error_input.addItems(self.e_keys)
        if not self.e_val in self.e_keys:
            self.e_val = 'None'
        self.error_input.setCurrentIndex(self.e_keys.index(self.e_val))

        self.scatter_type_combo.setCurrentIndex(int(int(self.scatter_type) % 4))

    def _populateFields(self):
        self.line_thickness_spin.setValue(int(self.line_thickness))
        self.scatter_size_spin.setValue(int(self.scatter_size))
        self.offset_spin.setValue(float(self.offset))

    def _populateCheckBoxes(self):
        self.active_check.setChecked(self.active)
        self.line_check.setChecked(self.line)
        self.scatter_check.setChecked(self.scatter)

    def setManually(self, x_val = 'None', y_val = 'None', e_val = 'None', offset = 0.):
        if not x_val in self.x_keys:
            x_val = 'None'
        self.x_input.setCurrentIndex(self.x_keys.index(x_val))

        if not y_val in self.y_keys:
            y_val = 'None'
        self.y_input.setCurrentIndex(self.y_keys.index(y_val))

        if not e_val in self.e_keys:
            e_val = 'None'
        self.error_input.setCurrentIndex(self.e_keys.index(e_val))

        self.offset = offset
        self.offset_spin.setValue(self.offset)

    def _connectWidgets(self):
        self.x_input.currentIndexChanged.connect(self._grabInfo)
        self.y_input.currentIndexChanged.connect(self._grabInfo)
        self.link_input.currentIndexChanged.connect(self._getLink)
        self.error_input.currentIndexChanged.connect(self._grabInfo)
        self.scatter_type_combo.currentIndexChanged.connect(self._grabInfo)
        self.line_thickness_spin.valueChanged.connect(self._grabInfo)
        self.scatter_size_spin.valueChanged.connect(self._grabInfo)
        self.scatter_check.stateChanged.connect(self._grabInfo)
        self.line_check.stateChanged.connect(self._grabInfo)
        self.color_button.clicked.connect(self._colorSelect)

    def _disconnectWidgets(self):
        self.x_input.currentIndexChanged.disconnect(self._grabInfo)
        self.y_input.currentIndexChanged.disconnect(self._grabInfo)
        self.link_input.currentIndexChanged.disconnect(self._getLink)
        self.error_input.currentIndexChanged.disconnect(self._grabInfo)
        self.scatter_type_combo.currentIndexChanged.disconnect(self._grabInfo)
        self.line_thickness_spin.valueChanged.disconnect(self._grabInfo)
        self.scatter_size_spin.valueChanged.disconnect(self._grabInfo)
        self.scatter_check.stateChanged.disconnect(self._grabInfo)
        self.line_check.stateChanged.disconnect(self._grabInfo)
        self.color_button.clicked.disconnect(self._colorSelect)

    def _grabInfo(self):
        self.x_val  = self.x_keys[self.x_input.currentIndex()]
        self.y_val  = self.y_keys[self.y_input.currentIndex()]
        self.e_val  = self.e_keys[self.error_input.currentIndex()]

        self.scatter_type   = self.scatter_type_combo.currentIndex()
        self.line_thickness = self.line_thickness_spin.value() 
        self.scatter_size   = self.scatter_size_spin.value()
        self.scatter        = self.scatter_check.isChecked()
        self.line           = self.line_check.isChecked()

        self.child.setText(0, self.y_val)

    def _updateLink(self, override = False):
        try:
            self._disconnectWidgets()
        except:
            pass

        names   = []
        for i in range(self.parent.topLevelItemCount()):
            names.append(self.parent.topLevelItem(i).text(0))
        self.link_keys = ['None'] + names

        self.link_input.clear()
        self.link_input.addItems(self.link_keys)

        self._connectWidgets()

    def setLink(self, value = None):
        if not value in self.link_keys:
            value = 'None'
        self.link_input.setCurrentIndex(self.link_keys.index(value))

    def _getLink(self):
        self.link   = self.link_keys[self.link_input.currentIndex()]

    def _colorSelect(self):
        self.color = QtGui.QColorDialog.getColor()
        self._setColorStyleSheet()

    def setColor(self, hex):
        col = tuple(int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2 ,4))
        self.color = QtGui.QColor(
            col[0],
            col[1],
            col[2])
        self._setColorStyleSheet()

    def _setColorStyleSheet(self):
        self.color_button.setStyleSheet(
            '''
            #color_button{
            background-color: rgb('''+str(self.color.getRgb()[0])+","+str(self.color.getRgb()[1])+","+str(self.color.getRgb()[2])+''');
            border-style: inset;
            border-width: 2px}

            #color_button:pressed{
            border-style: outset;
            border-width: 2px}
            '''
        )

    def _getPlotDict(self):
        plot_dict = {}

        if not self.x_val == 'None':
            plot_dict['x key'] = self.x_val
        if not self.y_val == 'None':
            plot_dict['y key'] = self.y_val
        if not self.e_val == 'None':
            plot_dict['e key'] = self.e_val

        style = []
        if self.line:
            style.append('-')
        if self.scatter:
            style.append(self.scatter_types[self.scatter_type])
            style.append(self.scatter_size)

        plot_dict['style']      = style
        plot_dict['thickness']  = self.line_thickness
        plot_dict['offset']     = self.offset_spin.value()

        if self.link == 'None':
            plot_dict['link']   = None
        else:
            plot_dict['link']   = self.link

        plot_dict['color']      = QtGui.QColor(self.color)
        plot_dict['actif']      = self.active_check.isChecked()

        return plot_dict
