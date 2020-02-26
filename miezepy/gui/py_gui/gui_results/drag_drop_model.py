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
from simpleplot.models.plot_model   import PlotModel
from simpleplot.models.session_node import SessionNode

class DragModel(PlotModel):
    '''
    This is an adaptation for the drag and drop model
    that we designed for SImpleplot
    '''
    def __init__(self, root, parent=None, col_count=2):
        super().__init__(root, parent=parent, col_count=col_count)

    def supportedDropActions(self): 
        return QtCore.Qt.CopyAction

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled

    def mimeTypes(self):
        return ['text']

    def mimeData(self, indices):
        addresses = []
        for index in indices:
            item    = self.itemAt(index)
            strings = [item._name]

            root_reached = False
            while not root_reached:
                item = item.parent()
                if item is None:
                    root_reached = True
                else:
                    strings.append(item._name)

            addresses.append('>'.join(strings[::-1]))

        link = '|'.join(addresses)
        mimedata = QtCore.QMimeData()
        mimedata.setData('text', bytes(link,'utf-8'))
        return mimedata
        
class DropModel(PlotModel):
    '''
    This is an adaptation for the drag and drop model
    that we designed for SImpleplot
    '''
    def __init__(self, root, parent=None, col_count=2):
        super().__init__(root, parent=parent, col_count=col_count)

    def supportedDropActions(self): 
        return QtCore.Qt.CopyAction

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled

    def mimeTypes(self):
        return ['text']

    def dropMimeData(self, data, action, row, column, parent):
        print('dropMimeData %s %s %s %s' % (data.data('text'), action, row, parent) )
