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
import os
from functools import partial

#inspired from https://stackoverflow.com/questions/29888959/pyqt4-drag-and-drop-files-in-qlistview

class DropListView(QtWidgets.QListView): 
    drop_success = QtCore.pyqtSignal(list)
    '''
    Thi method is a custom modification of the 
    QListView widget that supports drag and 
    drop.
    '''        
    def __init__(self, parent, drop_type):
        super(DropListView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setFrameShape(QtWidgets.QFrame.Box)

        if drop_type == 'tof_file_drop':
            self.dropEvent = partial(tofFileDrop, self)
            self.check     = tofFileCheck

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            if self.check(event):
                event.acceptProposedAction()
            else:
                super(DropListView, self).dragEnterEvent(event)
        else:
            super(DropListView, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(DropListView, self).dragMoveEvent(event)

def tofFileDrop(generator_class, event):
    '''
    This is the drop method and will support the
    drop of the files into the list. 
    '''
    if event.mimeData().hasUrls():
        if tofFileCheck(event):
            event.acceptProposedAction()
            generator_class.drop_success.emit([url.path() for url in event.mimeData().urls()])

def tofFileCheck(event):
    '''
    check if the file are tof
    '''
    urls        = [url for url in event.mimeData().urls()]
    bool_tof    = [False for e in urls]

    for i, url in enumerate(urls):
        if url.path().split('.')[-1] == "tof":
            bool_tof[i] = True

    if all(bool_tof):
        return True
    else:
        return False