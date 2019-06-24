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

def dialog(
    parent      = None,
    icon        = None, 
    message     = None, 
    add_message = None, 
    det_message = None, 
    title       = None):

    '''
    '''
    parent.msg = QtWidgets.QMessageBox(parent = parent)
    if icon == 'error':
        parent.msg.setIcon(QtWidgets.QMessageBox.Critical)
    elif icon == 'info':
        parent.msg.setIcon(QtWidgets.QMessageBox.Information)
    elif icon == 'warning':
        parent.msg.setIcon(QtWidgets.QMessageBox.Warning)
    else:
        icon = 'warning'
        parent.msg.setIcon(QtWidgets.QMessageBox.Warning)
    
    if not message == None:
        parent.msg.setText(message)
    if not add_message == None:
        parent.msg.setInformativeText(add_message)
    if not det_message == None:
        parent.msg.setDetailedText(det_message)
    if not title == None:
        parent.msg.setText(title)
    else:
        parent.msg.setWindowTitle(icon)
    if not message == None:
        parent.msg.setText(message)
    
    parent.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    parent.msg.exec_()