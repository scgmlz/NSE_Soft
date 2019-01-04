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

#############################
#import general components
import numpy as np
import copy

from .mask_shape    import MaskShape
from .triangle      import Triangle
from .square        import Square
from .circle_arc    import CircleArc

class LinearComposition(MaskShape):

    def __init__(self):
        '''
        This is the grid mode of the element. 
        Note that this composition can only 
        be set to close gaps if the subelement
        is of rectangular shape.
        '''
        MaskShape.__init__(self)
        self.initialize()

    def initialize(self):
        '''
        This routine will edit the inherited 
        dictionary of parameters.
        '''
        self.parameters['type']         = 'linear composition'
        self.parameters['child type']   = 'square'
        self.parameters['horizontal']   = 1
        self.parameters['vertical']     = 1
        self.parameters['width']        = 50
        self.parameters['height']       = 50
        self.parameters['close gap']    = True
        self.parameters['increment']    = True
        
        self.children = []

        self.setChildType(self.parameters['child type'])

    def setChildType(self, child_type):
        '''
        If a child is selected we need to maintin a 
        certain coherence. This is why we then load
        a template into here to manage the parameters
        for all.
        '''
        if child_type == 'square':
            self.template = Square()
            self.parameters['child type']   = 'square'
        elif child_type == 'triangle':
            self.template = Triangle()
            self.parameters['child type']   = 'triangle'
        elif child_type == 'arc':
            self.template = CircleArc()
            self.parameters['child type']   = 'arc'

    def setup(self):
        '''
        Setup the grid with the elements within
        '''
        x = np.linspace(
            self.parameters['position'][0] - self.parameters['width'] / 2,
            self.parameters['position'][0] + self.parameters['width'] / 2,
            num = self.parameters['horizontal'])

        y = np.linspace(
            self.parameters['position'][1] - self.parameters['height'] / 2,
            self.parameters['position'][1] + self.parameters['height'] / 2,
            num = self.parameters['vertical'])

        xx, yy = np.meshgrid(x,y)
        edges = []

        for i in range(xx.shape[0]):
            for j in range(xx.shape[1]):
                edges.append([xx[i,j], yy[i,j]])

        for i in range(len(edges)):
            edges[i] = self.rotatePoint(
                self.parameters['position'],
                edges[i],
                self.parameters['angle'])

        self.children = []

        for edge in edges:
            element = copy.deepcopy(self.template)

            if self.parameters['child type'] == 'square':
                if self.parameters['close gap']: 
                    element.parameters['width']  = (x[1] - x[0])
                    element.parameters['height'] = (y[1] - y[0])

            element.move(absolute = edge)
            element.rotate(absolute = self.parameters['angle'])

            self.children.append(element)

    def generate(self, size_x, size_y):
        '''
        Generate the mask element by calling the 
        setup and then patching the masks
        '''
        self.setup()
        self.mask = np.zeros((size_x, size_y), dtype=np.int16)

        for i, child in enumerate(self.children):
            child.generate(size_x, size_y)
            if self.parameters['increment']:
                self.mask += child.mask * (i+1)
            else:
                self.mask += child.mask



if __name__ == '__main__':

    import matplotlib.pyplot as plt

    comp = LinearComposition()
    comp.parameters['horizontal']   = 6
    comp.parameters['vertical']     = 6
    comp.parameters['width']        = 100
    comp.parameters['height']       = 100
    comp.parameters['angle']        = 30
    comp.parameters['increment']    = False
    comp.setChildType('arc')
    comp.template.parameters['angle_range']     = (0, 180)
    comp.template.parameters['radius_range']    = (3, 8)
    comp.move(absolute = [50,50])
    comp.generate(128,128)

    plt.pcolormesh(comp.mask)
    plt.show()
