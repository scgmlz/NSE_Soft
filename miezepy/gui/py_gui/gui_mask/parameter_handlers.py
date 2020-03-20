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

from simpleplot.ploting.graph_items.pie_item import PieItem
from simpleplot.ploting.graph_items.rectangle_item import RectangleItem
from simpleplot.ploting.graph_items.triangle_item import TriangleItem
from simpleplot.ploting.graph_items.ellipse_item import EllipseItem

class RectangleHandler(RectangleItem):
    def __init__(self):
        super().__init__('Rectangle')
    
    def refresh(self):
        '''
        Overwrite the refresh
        '''
        pass

    def resetSubdivision(self):
        '''
        Overwrite the refresh
        '''
        pass

    def draw(self):
        '''
        Overwrite the refresh
        '''
        pass

    def drawGL(self):
        '''
        Overwrite the refresh
        '''
        pass

class TriangleHandler(TriangleItem):
    def __init__(self):
        super().__init__('Triangle')

    def refresh(self):
        '''
        Overwrite the refresh
        '''
        pass

    def resetSubdivision(self):
        '''
        Overwrite the refresh
        '''
        pass

    def draw(self):
        '''
        Overwrite the refresh
        '''
        pass

    def drawGL(self):
        '''
        Overwrite the refresh
        '''
        pass

class PieHandler(PieItem):
    def __init__(self):
        super().__init__('Pie')

    def refresh(self):
        '''
        Overwrite the refresh
        '''
        pass

    def resetSubdivision(self):
        '''
        Overwrite the refresh
        '''
        pass

    def draw(self):
        '''
        Overwrite the refresh
        '''
        pass

    def drawGL(self):
        '''
        Overwrite the refresh
        '''
        pass

class EllipseHandler(EllipseItem):
    def __init__(self):
        super().__init__('Ellipse')

    def refresh(self):
        '''
        Overwrite the refresh
        '''
        pass

    def resetSubdivision(self):
        '''
        Overwrite the refresh
        '''
        pass

    def draw(self):
        '''
        Overwrite the refresh
        '''
        pass

    def drawGL(self):
        '''
        Overwrite the refresh
        '''
        pass
