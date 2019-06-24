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

from simpleplot.model.parameter_class   import ParameterHandler

class DefaultHandler(ParameterHandler):
    def __init__(self):
        super().__init__('Parameters')
        self.addParameter(
            'Position', [10.,10.], 
            names = ['x','y'],
            min     = -1000.,
            max     = 1000.,
            method = self._process)
        self.addParameter(
            'Angle', 0.,
            min     = -360.,
            max     = 360.,
            method  = self._process)

    def _process(self):
        pass

    def flags(self, index):
        if index.column() is 1: 
            return QtCore.Qt.ItemIsEnabled  | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled 
            
class RectangleHandler(DefaultHandler):
    def __init__(self):
        super().__init__()
        self.addParameter(
            'Dimensions', [10.,10.], 
            names = ['Width','Height'],
            method = self._process)

class TriangleHandler(DefaultHandler):
    def __init__(self):
        super().__init__()
        self.addParameter(
            'Dimensions', [10.,10.], 
            names = ['Width','Height'],
            method = self._process)

class ArcHandler(DefaultHandler):
    def __init__(self):
        super().__init__()
        self.addParameter(
            'Radial range', [0.,10.], 
            names = ['Lower','Upper'],
            method = self._process)
        self.addParameter(
            'Angular range', [0.,180.], 
            names = ['Lower','Upper'],
            method = self._process)

class RadialHandler(DefaultHandler):
    def __init__(self):
        super().__init__()
        self.addParameter(
            'Radial range', [0.,10.], 
            names = ['Lower','Upper'],
            method = self._process)
        self.addParameter(
            'Angular range', [0.,180.], 
            min     = -360.,
            max     = 360.,
            names = ['Lower','Upper'],
            method = self._process)
        self.addParameter(
            'Multiplicity', [2,2], 
            names = ['Radial','Angular'],
            method = self._process)
        self.addParameter(
            'Increment', True, 
            names = ['Lower','Upper'],
            method = self._process)
        self.addParameter(
            'Close Gap', True, 
            names = ['Width','Height'],
            method = self._process)

class LinearHandler(DefaultHandler):
    def __init__(self):
        super().__init__()
        self.addParameter(
            'Multiplicity', [2,2], 
            names = ['Lower','Upper'],
            method = self._process)
        self.addParameter(
            'Dimensions', [10.,10.], 
            names = ['Width','Height'],
            method = self._process)
        self.addParameter(
            'Increment', True, 
            names = ['Lower','Upper'],
            method = self._process)
        self.addParameter(
            'Close Gap', True, 
            names = ['Width','Height'],
            method = self._process)
        
