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

from PyQt5 import QtWidgets,QtCore,QtGui

class FoilDelegate(QtWidgets.QStyledItemDelegate):

    def paint(self, painter, option, index):
        item = index.model().item(index.row(), index.column()) 
        if item.isCheckable() or item.isTristate():
            checked = item.checkState()
            check_box_style_option = QtWidgets.QStyleOptionButton()
            
    
            if checked == QtCore.Qt.Checked:
                check_box_style_option.state |= QtWidgets.QStyle.State_On
            elif checked == QtCore.Qt.PartiallyChecked:
                check_box_style_option.state |= QtWidgets.QStyle.State_NoChange
            elif checked == QtCore.Qt.Unchecked:
                check_box_style_option.state |= QtWidgets.QStyle.State_Off
    
            check_box_style_option.rect = self.getCheckBoxRect(option)
            check_box_style_option.state |= QtWidgets.QStyle.State_Enabled
            QtWidgets.QApplication.style().drawControl(
                QtWidgets.QStyle.CE_CheckBox, check_box_style_option, painter)

        else:
            super().paint(painter, option, index)

    def getCheckBoxRect(self, option):
        check_box_style_option = QtWidgets.QStyleOptionButton()
        check_box_rect = QtWidgets.QApplication.style().subElementRect(
            QtWidgets.QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QtCore.QPoint (
            option.rect.x(), 
            option.rect.y() + option.rect.height() / 2 
            - check_box_rect.height() / 2)

        return QtCore.QRect(check_box_point, check_box_rect.size())

    def sizeHint(self, option, index):
        item = index.model().item(index.row(), index.column()) 
        if item.isCheckable() or item.isTristate():
            rect = self.getCheckBoxRect(option)
            size = QtCore.QSize(rect.width(), rect.height())
        else:
            size = super(FoilDelegate, self).sizeHint(option, index)
        return size