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
from simpleplot.model.node import SessionNode
import numpy as np

class PlotNode(SessionNode):
    def __init__(self, name, parent=None, link = None):
        super().__init__(name, parent=parent)
        self.link = link
        self._initialize()

        # self.setCheckable(True)
        # self.setCheckState(QtCore.Qt.Checked)

    def _initialize(self):
        '''
        set up all the plot related data
        '''
        self._active         = True
        self._expanded       = False
        self._link           = 'None'
        self._offset         = 0
        self._raw            = False
        self._color          = QtGui.QColor('b')

        self._scatter        = True
        self._scatter_type   = 0
        self._scatter_types  = ['o','s','t','d']
        self._scatter_size   = 5

        self._line           = True
        self._line_thickness = 2

    def connectToWidget(self, widget):
        self.widget = widget
        self._populateComboBoxes()
        self._populateFields()
        self._populateCheckBoxes()
        self._setColorStyleSheet()
        self._updateTable()
        self._updateLink()
        self._connectWidgets()

    def disconnectFromWidget(self):
        self._disconnectWidgets()
        self.widget = None

    def _populateComboBoxes(self):
        self.widget.link_input.clear()

    def _populateFields(self):
        self.widget.line_thickness_spin.setValue(int(self._line_thickness))
        self.widget.scatter_size_spin.setValue(int(self._scatter_size))
        self.widget.offset_spin.setValue(float(self._offset))

    def _populateCheckBoxes(self):
        self.widget.line_check.setChecked(self._line)
        self.widget.scatter_check.setChecked(self._scatter)

    def _connectWidgets(self):
        self.widget.link_input.currentIndexChanged.connect(self._getLink)
        self.widget.scatter_type_combo.currentIndexChanged.connect(self._grabInfo)
        self.widget.line_thickness_spin.valueChanged.connect(self._grabInfo)
        self.widget.scatter_size_spin.valueChanged.connect(self._grabInfo)
        self.widget.scatter_check.stateChanged.connect(self._grabInfo)
        self.widget.line_check.stateChanged.connect(self._grabInfo)
        self.widget.color_button.clicked.connect(self._colorSelect)
        self.widget.offset_spin.valueChanged.connect(self._grabInfo)

    def _disconnectWidgets(self):
        self.widget.link_input.currentIndexChanged.disconnect(self._getLink)
        self.widget.scatter_type_combo.currentIndexChanged.disconnect(self._grabInfo)
        self.widget.line_thickness_spin.valueChanged.disconnect(self._grabInfo)
        self.widget.scatter_size_spin.valueChanged.disconnect(self._grabInfo)
        self.widget.scatter_check.stateChanged.disconnect(self._grabInfo)
        self.widget.line_check.stateChanged.disconnect(self._grabInfo)
        self.widget.color_button.clicked.disconnect(self._colorSelect)
        self.widget.offset_spin.valueChanged.disconnect(self._grabInfo)

    def _grabInfo(self, parent):
        self._scatter_type   = self.widget.scatter_type_combo.currentIndex()
        self._line_thickness = self.widget.line_thickness_spin.value() 
        self._scatter_size   = self.widget.scatter_size_spin.value()
        self._scatter        = self.widget.scatter_check.isChecked()
        self._line           = self.widget.line_check.isChecked()        
        self._offset         = self.widget.offset_spin.value()
       
    def _updateTable(self):
        '''
        Put the elements into the table widget
        '''
        self.header = ['x','y','error','y raw', 'y raw error']
        self.data_list = [np.asarray(e) for e in self.link._value]
        self.data_list = np.array(self.data_list).transpose().tolist()

        self.model = DataTableModel(
            self.widget.local_widget,
            self.data_list, 
            self.header,
            [e for e in range(len(self.data_list))])
        self.widget.process_table_data.setModel(self.model)

    def _updateLink(self):

        pass
        # names   = []
        # for i in range(self.stdItem.model().rowCount()):
        #     names.append(self.stdItem.model().item(i).text())
        # self.link_keys = ['None'] + names

    def setLink(self, value = None):

        pass
        # if not value in self.link_keys:
        #     value = 'None'
        # self.link = value

    def _getLink(self):

        pass
        # self.link   = self.link_keys[self.parent.link_input.currentIndex()]


    def _colorSelect(self):
        self.color_dialog = QtGui.QColorDialog(parent = self.widget.local_widget)
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
        self._color = QtGui.QColor(color)
        self._setColorStyleSheet()

    def _setColorStyleSheet(self):
        self.widget.color_button.setStyleSheet(
            '''
            #color_button{
            background-color: rgb('''+str(self._color.getRgb()[0])+","+str(self._color.getRgb()[1])+","+str(self._color.getRgb()[2])+''');
            border-style: inset;
            border-width: 2px}

            #color_button:pressed{
            border-style: outset;
            border-width: 2px}
            '''
        )

    def _getPlotDict(self):
        plot_dict = {}

        data_list = [np.asarray(e) for e in self.link._value]
        plot_dict['x'] = data_list[0]

        if len(data_list) == 5:
            if self._raw:
                plot_dict['y'] = data_list[3]
                plot_dict['e'] = data_list[4]
            else:
                plot_dict['y'] = data_list[1]
                plot_dict['e'] = data_list[2]
        elif len(data_list) == 3:
            plot_dict['y'] = data_list[1]
            plot_dict['e'] = data_list[2]
        elif len(data_list) == 2:
            plot_dict['y'] = data_list[1]

        style = []
        if self._line:
            style.append('-')
        if self._scatter:
            style.append(self._scatter_types[self._scatter_type])
            style.append(self._scatter_size)

        plot_dict['style']      = style
        plot_dict['thickness']  = self._line_thickness
        plot_dict['offset']     = self._offset

        if self._link == 'None':
            plot_dict['link']   = None
        else:
            plot_dict['link']   = self._link

        plot_dict['color']      = QtGui.QColor(self._color)
        plot_dict['active']     = self._active

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
    # def sort(self, col, order):
    #     """sort table by given column number col"""
    #     self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
    #     # self.data_list = sorted(self.data_list,
    #     #     key=operator.itemgetter(col))
    #     if order == QtCore.Qt.DescendingOrder:
    #         self.data_list.reverse()
    #     self.emit(QtCore.SIGNAL("layoutChanged()"))