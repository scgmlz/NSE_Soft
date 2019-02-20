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

class PlotItem():
     
    def __init__(self, stdItem, result_handler):
        self._initialValues()
        self.stdItem = stdItem
        self.result_handler = result_handler

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

    def _prepare(self):
        if not 'None' in self.x_keys:
            self.x_keys = ['None'] + self.x_keys
        if not 'None' in self.y_keys:
            self.y_keys = ['None'] + self.y_keys
        if not 'None' in self.e_keys:
            self.e_keys = ['None'] + self.e_keys
        if not 'None' in self.link_keys:
            self.link_keys = ['None'] + self.link_keys

    def connectParent(self, parent):
        self.parent = parent
        self._prepare()
        self._populateComboBoxes()
        self._populateFields()
        self._populateCheckBoxes()
        self._setColorStyleSheet()
        self._updateTable()
        self._updateLink()
        self._connectWidgets()

    def disconnectParent(self):
        self._disconnectWidgets()
        self.parent = None

    def _populateComboBoxes(self):
        self.parent.x_input.clear()
        self.parent.x_input.addItems(self.x_keys)
        if not self.x_val in self.x_keys:
            self.x_val = 'None'
        self.parent.x_input.setCurrentIndex(self.x_keys.index(self.x_val))

        self.parent.y_input.clear()
        self.parent.y_input.addItems(self.y_keys)
        if not self.y_val in self.y_keys:
            self.y_val = 'None'
        self.parent.y_input.setCurrentIndex(self.y_keys.index(self.y_val))

        self.parent.error_input.clear()
        self.parent.error_input.addItems(self.e_keys)
        if not self.e_val in self.e_keys:
            self.e_val = 'None'
        self.parent.error_input.setCurrentIndex(self.e_keys.index(self.e_val))
        self.parent.scatter_type_combo.setCurrentIndex(int(int(self.scatter_type) % 4))

        self.parent.link_input.clear()
        self.parent.link_input.addItems(self.link_keys)
        if not self.link in self.link_keys:
            self.link = 'None'
        self.parent.link_input.setCurrentIndex(self.link_keys.index(self.link))

    def _populateFields(self):
        self.parent.line_thickness_spin.setValue(int(self.line_thickness))
        self.parent.scatter_size_spin.setValue(int(self.scatter_size))
        self.parent.offset_spin.setValue(float(self.offset))

    def _populateCheckBoxes(self):
        self.parent.active_check.setChecked(self.active)
        self.parent.line_check.setChecked(self.line)
        self.parent.scatter_check.setChecked(self.scatter)

    def setManually(self, x_val = 'None', y_val = 'None', e_val = 'None', offset = 0.):
        if not x_val in self.x_keys:
            x_val = 'None'
        else:
            self.x_val = x_val
        if not y_val in self.y_keys:
            y_val = 'None'
        else:
            self.y_val = y_val
        if not e_val in self.e_keys:
            e_val = 'None'
        else:
            self.e_val = e_val
        self.offset = offset
        self.stdItem.setText(self.y_val)

    def _connectWidgets(self):
        self.parent.x_input.currentIndexChanged.connect(self._grabInfo)
        self.parent.y_input.currentIndexChanged.connect(self._grabInfo)
        self.parent.link_input.currentIndexChanged.connect(self._getLink)
        self.parent.error_input.currentIndexChanged.connect(self._grabInfo)
        self.parent.scatter_type_combo.currentIndexChanged.connect(self._grabInfo)
        self.parent.line_thickness_spin.valueChanged.connect(self._grabInfo)
        self.parent.scatter_size_spin.valueChanged.connect(self._grabInfo)
        self.parent.scatter_check.stateChanged.connect(self._grabInfo)
        self.parent.line_check.stateChanged.connect(self._grabInfo)
        self.parent.color_button.clicked.connect(self._colorSelect)
        self.parent.active_check.stateChanged.connect(self._grabInfo)
        self.parent.offset_spin.valueChanged.connect(self._grabInfo)

    def _disconnectWidgets(self):
        self.parent.x_input.currentIndexChanged.disconnect(self._grabInfo)
        self.parent.y_input.currentIndexChanged.disconnect(self._grabInfo)
        self.parent.link_input.currentIndexChanged.disconnect(self._getLink)
        self.parent.error_input.currentIndexChanged.disconnect(self._grabInfo)
        self.parent.scatter_type_combo.currentIndexChanged.disconnect(self._grabInfo)
        self.parent.line_thickness_spin.valueChanged.disconnect(self._grabInfo)
        self.parent.scatter_size_spin.valueChanged.disconnect(self._grabInfo)
        self.parent.scatter_check.stateChanged.disconnect(self._grabInfo)
        self.parent.line_check.stateChanged.disconnect(self._grabInfo)
        self.parent.color_button.clicked.disconnect(self._colorSelect)
        self.parent.active_check.stateChanged.disconnect(self._grabInfo)
        self.parent.offset_spin.valueChanged.disconnect(self._grabInfo)

    def _grabInfo(self, parent):
        self.x_val  = self.x_keys[self.parent.x_input.currentIndex()]
        self.y_val  = self.y_keys[self.parent.y_input.currentIndex()]
        self.e_val  = self.e_keys[self.parent.error_input.currentIndex()]

        self.scatter_type   = self.parent.scatter_type_combo.currentIndex()
        self.line_thickness = self.parent.line_thickness_spin.value() 
        self.scatter_size   = self.parent.scatter_size_spin.value()
        self.scatter        = self.parent.scatter_check.isChecked()
        self.line           = self.parent.line_check.isChecked()
        self.active         = self.parent.active_check.isChecked()         
        self.offset         = self.parent.offset_spin.value()
       
        self.stdItem.setText(self.y_val)
        self._updateTable()

    def _updateTable(self):
        '''
        Put the elements into the table widget
        '''
        self.header = []
        self.data_list = []

        if not self.x_val == 'None':
            self.header.append('x')
            self.data_list.append(np.asarray(self.result_handler.getDataFromKey(self.x_val)).tolist())
        if not self.y_val == 'None':
            self.header.append('y')
            self.data_list.append(np.asarray(self.result_handler.getDataFromKey(self.y_val)).tolist())
        if not self.e_val == 'None':
            self.header.append('error')
            self.data_list.append(np.asarray(self.result_handler.getDataFromKey(self.e_val)).tolist())

        self.data_list = np.array(self.data_list).transpose().tolist()
        
        if not len(self.data_list) == 0:
            self.model = DataTableModel(
                self.parent.local_widget,
                self.data_list, 
                self.header,
                [e for e in range(len(self.data_list))])

            self.parent.process_table_data.setModel(self.model)

    def _updateLink(self):
        names   = []
        for i in range(self.stdItem.model().rowCount()):
            names.append(self.stdItem.model().item(i).text())
        self.link_keys = ['None'] + names

    def setLink(self, value = None):
        if not value in self.link_keys:
            value = 'None'
        self.link = value

    def _getLink(self):
        self.link   = self.link_keys[self.parent.link_input.currentIndex()]


    def _colorSelect(self):
        self.color_dialog = QtGui.QColorDialog(parent = self.parent.local_widget)
        self.color_dialog.colorSelected.connect(self.setColorWindows)
        self.color_dialog.show()

    def setColor(self, hex = None):
        if not hex == None:
            col = tuple(int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2 ,4))
            self.color = QtGui.QColor(
                col[0],
                col[1],
                col[2])

    def setColorWindows(self, color):
        self.color = QtGui.QColor(color)
        self._setColorStyleSheet()

    def _setColorStyleSheet(self):
        self.parent.color_button.setStyleSheet(
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
        plot_dict['offset']     = self.offset

        if self.link == 'None':
            plot_dict['link']   = None
        else:
            plot_dict['link']   = self.link

        plot_dict['color']      = QtGui.QColor(self.color)
        plot_dict['actif']      = self.active

        return plot_dict


class DataTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, data_list, col_header,row_header, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.data_list = data_list
        self.col_header = col_header
        self.row_header = row_header

    def rowCount(self, parent):
        return len(self.data_list)

    def columnCount(self, parent):
        if len(self.data_list) > 0:
            return len(self.data_list[0])
        else:
            return 0
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.data_list[index.row()][index.column()]
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.col_header[col]
        elif orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return self.row_header[col]
        else:
            return None
    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.data_list = sorted(self.data_list,
            key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self.data_list.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))