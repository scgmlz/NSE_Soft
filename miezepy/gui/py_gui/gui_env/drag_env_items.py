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

from PyQt5 import QtWidgets,QtGui, QtCore

class DraggableButton(QtWidgets.QPushButton):
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_start_position = event.pos()

        if self.objectName() == 'env_button_load':
            icon = QtGui.QIcon(":/Ressources/data.ico")
            identifier = 'data'
        elif self.objectName() == 'env_button_mask':
            icon = QtGui.QIcon(":/Ressources/mask.ico")
            identifier = 'mask'
        elif self.objectName() == 'env_button_scripts':
            icon = QtGui.QIcon(":/Ressources/script.ico")
            identifier = 'scripts'
        elif self.objectName() == 'env_button_results':
            icon = QtGui.QIcon(":/Ressources/plot_result.ico")
            identifier = 'results'

        self.pixmap = icon.pixmap(QtCore.QSize(30,30))
        self.mimedata = QtCore.QMimeData()
        self.mimedata.setText(
            self.parent().findChild(
                QtWidgets.QLineEdit, 'env_input_name').text()
            +'|'
            +identifier)

        self.drag = QtGui.QDrag(self)
        self.drag.setMimeData(self.mimedata)
        self.drag.setDragCursor(self.pixmap, QtCore.Qt.DropAction.MoveAction)
        self.drag.setDragCursor(self.pixmap, QtCore.Qt.DropAction.CopyAction)

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

    def mouseMoveEvent(self, event):
        if not (event.buttons() & QtCore.Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QtWidgets.QApplication.startDragDistance():
            return

        self.drag.setHotSpot(event.pos())
        self.drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)

class DropLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        QtWidgets.QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

class DropWidget(QtWidgets.QWidget):
    dropAccepted = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            self.setStyleSheet('#env_frame{background-color: darkGreen;}')
        else:
            self.setStyleSheet('#env_frame{background-color: red;}')

    def dropEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
            drag_operation = (
                event.mimeData().text() 
                + '|'
                + self.findChild(
                QtWidgets.QLineEdit, 'env_input_name').text())
            self.dropAccepted.emit(drag_operation)
        self.setStyleSheet('#env_frame{background-color: transparent;}')

    def dragLeaveEvent(self, event):
        self.setStyleSheet('#env_frame{background-color: transparent;}')

