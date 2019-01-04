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

import numpy as np
from .mask_shape import MaskShape

class CircleArc(MaskShape):

    def __init__(self):
        '''
        This class will contain all the
        informations and routines to build
        a square over a certain 2D grid.
        '''
        MaskShape.__init__(self)
        self.initialize()

    def initialize(self):
        '''
        This routine will edit the inherited 
        dictionary of parameters.
        '''
        self.parameters['type']         = 'arc'
        self.parameters['radius_range'] = (10,15)
        self.parameters['angle_range']  = (0, 350)

    def generate(self, size_x, size_y):
        '''
        This will generate the mask element 
        onto a canvas of a given dimension
        '''

        angle_range = [
            angle + self.parameters['angle'] 
            for angle in self.parameters['angle_range']]

        self.mask = self.processSector(
            self.parameters['radius_range'],
            angle_range,
            size_x,
            size_y)
