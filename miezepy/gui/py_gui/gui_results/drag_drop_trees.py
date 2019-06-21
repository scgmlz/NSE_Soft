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

class ResultTree(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setProperty("showDropIndicator", True)
        self.setDragEnabled(True)

        self.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.setObjectName("process_tree")
        self.header().setVisible(False)
        self.header().setDefaultSectionSize(28)
        self.header().setHighlightSections(False)
        self.header().setSortIndicatorShown(False)
        self.header().setStretchLastSection(True)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_start_position = event.pos()
        self.mimeData = self.model().mimeData(self.selectedIndexes())
        self.drag = QtGui.QDrag(self)
        self.drag.setMimeData(self.mimeData)
        

    def mouseMoveEvent(self, event):
        if not (event.buttons() & QtCore.Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QtWidgets.QApplication.startDragDistance():
            return 

        self.drag.setHotSpot(event.pos())
        self.drag.exec_(QtCore.Qt.CopyAction)
    
    def mouseReleaseEvent(self, event):
        if (event.pos() - self.drag_start_position).manhattanLength() < QtWidgets.QApplication.startDragDistance():
            super().mousePressEvent(QtGui.QMouseEvent(
                QtCore.QEvent.MouseButtonPress,
                event.pos(),
                QtCore.Qt.LeftButton,
                QtCore.Qt.LeftButton,
                QtCore.Qt.NoModifier))
            super().mouseReleaseEvent(event)
        else:
            return


class PlotTree(QtWidgets.QTreeView):
    dropAccepted = QtCore.pyqtSignal(QtCore.QByteArray)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setProperty("showDropIndicator", True)

        self.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.setObjectName("plot_tree")
        self.header().setVisible(False)
        self.header().setDefaultSectionSize(28)
        self.header().setHighlightSections(False)
        self.header().setSortIndicatorShown(False)
        self.header().setStretchLastSection(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text'):
            event.accept()
            self.setStyleSheet('#plot_tree{background-color: darkGreen;}')
        else:
            self.setStyleSheet('#plot_tree{background-color: red;}')

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('text'):
            event.accept()
            self.setStyleSheet('#plot_tree{background-color: darkGreen;}')
        else:
            self.setStyleSheet('#plot_tree{background-color: red;}')

    def dropEvent(self, event):
        if event.mimeData().hasFormat('text'):
            event.acceptProposedAction()
            self.dropAccepted.emit(event.mimeData().data('text'))
        self.setStyleSheet('#plot_tree{}')

    def dragLeaveEvent(self, event):
        self.setStyleSheet('#plot_tree{}')
