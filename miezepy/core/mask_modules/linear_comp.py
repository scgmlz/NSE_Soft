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
from .rectangle     import Rectangle
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
        self.parameters['Name']         = 'Linear composition'
        self.parameters['child']        = {'Name' : 'Rectangle'}
        self.parameters['Multiplicity'] = [1,1]
        self.parameters['Dimensions']   = [10.,10.]
        self.parameters['Close Gap']    = True
        self.parameters['Increment']    = True
        
        self.children = []
        self.setChildType('Rectangle')

    def setDirectly(self, **kwargs):
        '''
        The mask generator favours the direct
        input of the values onto the mask
        and will therefore send it to the mask
        element to be anaged.
        '''
        self.parameters = kwargs
        self.setChildType(self.parameters['child']['Name'], self.parameters['child'])

    def setChildType(self, child_type, parameters = None):
        '''
        If a child is selected we need to maintin a 
        certain coherence. This is why we then load
        a template into here to manage the parameters
        for all.
        '''
        if child_type == 'Rectangle':
            self.template = Rectangle()
        elif child_type == 'Triangle':
            self.template = Triangle()
        elif child_type == 'Arc':
            self.template = CircleArc()

        if parameters == None:
            self.parameters['child']   = self.template.parameters
        else:
            self.template.setDirectly(**parameters)

    def setup(self):
        '''
        Setup the grid with the elements within
        '''
        x = np.linspace(
            self.parameters['Position'][0] - self.parameters['Dimensions'][0] / 2,
            self.parameters['Position'][0] + self.parameters['Dimensions'][0] / 2,
            num = self.parameters['Multiplicity'][0])

        y = np.linspace(
            self.parameters['Position'][1] - self.parameters['Dimensions'][1] / 2,
            self.parameters['Position'][1] + self.parameters['Dimensions'][1] / 2,
            num = self.parameters['Multiplicity'][1])

        xx, yy = np.meshgrid(x,y)
        edges = []

        for i in range(xx.shape[0]):
            for j in range(xx.shape[1]):
                edges.append([xx[i,j], yy[i,j]])

        for i in range(len(edges)):
            edges[i] = self.rotatePoint(
                self.parameters['Position'],
                edges[i],
                self.parameters['Angle'])


        self.children = []
        for edge in edges:
            element = copy.deepcopy(self.template)
            if self.parameters['child']['Name'] == 'Rectangle' and self.parameters['Close Gap']:
                element.parameters['Dimensions'][0]  = self.parameters['Dimensions'][0] / (self.parameters['Multiplicity'][0] - 1)
                element.parameters['Dimensions'][1] = self.parameters['Dimensions'][1] / (self.parameters['Multiplicity'][1] - 1)
            element.move(absolute = edge)
            if not self.parameters['child']['Name'] == 'Rectangle' or not self.parameters['Close Gap']:
                element.rotate(absolute = self.parameters['Angle'])
                element.rotate(relative = (self.template.parameters['Angle']))
            else:
                element.rotate(absolute = self.parameters['Angle'])
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
            if self.parameters['Increment']:
                self.mask += child.mask * (i+1)
                self.mask[self.mask > (i+1)] = (i+1)
            else:
                self.mask += child.mask
                self.mask[self.mask >1] = 1

        return self.mask
