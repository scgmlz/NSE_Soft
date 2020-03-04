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

from .mask_shape import MaskShape

class Rectangle(MaskShape):

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
        self.parameters['Type']         = 'Rectangle'
        self.parameters['Dimensions']   = [10.,10.]
        self.parameters['Subdivisions'] = [1,1]
        self.parameters['Subdivision dimensions'] = [True, 1.,1.]
        self.parameters['Increment']    = True

    def setDirectly(self, **kwargs):
        '''
        The mask generator favours the direct
        input of the values onto the mask
        and will therefore send it to the mask
        element to be anaged.
        '''
        for key in kwargs.keys():
            if key in ['Type', 'Name']:
                continue
            elif key in self.parameters.keys():
                if isinstance(kwargs[key], list):
                    self.parameters[key] = kwargs[key][-1]
                else:
                    self.parameters[key] = [
                        kwargs[key][subkey][-1] for subkey in kwargs[key].keys()]
        self.parameters['Position'] = self.parameters['Position'][0:2]

    def setup(self):
        '''
        Setup the grid with the elements within
        '''
        self.polygons = []
        for i in range(self.parameters['Subdivisions'][0]):
            for j in range(self.parameters['Subdivisions'][1]):
                edge = [
                    self.parameters['Position'][0]-self.parameters['Dimensions'][0]/2.
                    +(i+0.5)*self.parameters['Dimensions'][0]
                    /self.parameters['Subdivisions'][0],
                    self.parameters['Position'][1]-self.parameters['Dimensions'][1]/2.
                    +(j+0.5)*self.parameters['Dimensions'][1]
                    /self.parameters['Subdivisions'][1]]


                temp = []
                if not self.parameters['Subdivision dimensions'][0]:
                    temp.append(self.rotatePoint(
                        self.parameters['Position'],
                        [
                            edge[0]-self.parameters['Subdivision dimensions'][1]/2.,
                            edge[1]-self.parameters['Subdivision dimensions'][2]/2.
                        ],
                        self.parameters['Angle'])
                    )
                    temp.append(self.rotatePoint(
                        self.parameters['Position'],
                        [
                            edge[0]+self.parameters['Subdivision dimensions'][1]/2.,
                            edge[1]-self.parameters['Subdivision dimensions'][2]/2.
                        ],
                        self.parameters['Angle'])
                    )
                    temp.append(self.rotatePoint(
                        self.parameters['Position'],
                        [
                            edge[0]+self.parameters['Subdivision dimensions'][1]/2.,
                            edge[1]+self.parameters['Subdivision dimensions'][2]/2.
                        ],
                        self.parameters['Angle'])
                    )
                    temp.append(self.rotatePoint(
                        self.parameters['Position'],
                        [
                            edge[0]-self.parameters['Subdivision dimensions'][1]/2.,
                            edge[1]+self.parameters['Subdivision dimensions'][2]/2.
                        ],
                        self.parameters['Angle'])
                    )
                else:
                    temp.append(self.rotatePoint(
                        self.parameters['Position'],
                        [
                            (edge[0]-self.parameters['Dimensions'][0]
                            /(2*self.parameters['Subdivisions'][0])),
                            (edge[1]-self.parameters['Dimensions'][1]
                            /(2*self.parameters['Subdivisions'][1]))
                        ],
                        self.parameters['Angle'])
                    )
                    temp.append(self.rotatePoint(
                        self.parameters['Position'],
                        [
                            (edge[0]+self.parameters['Dimensions'][0]
                            /(2*self.parameters['Subdivisions'][0])),
                            (edge[1]-self.parameters['Dimensions'][1]
                            /(2*self.parameters['Subdivisions'][1]))
                        ],
                        self.parameters['Angle'])
                    )
                    temp.append(self.rotatePoint(
                        self.parameters['Position'],
                        [
                            (edge[0]+self.parameters['Dimensions'][0]
                            /(2*self.parameters['Subdivisions'][0])),
                            (edge[1]+self.parameters['Dimensions'][1]
                            /(2*self.parameters['Subdivisions'][1]))
                        ],
                        self.parameters['Angle'])
                    )
                    temp.append(self.rotatePoint(
                        self.parameters['Position'],
                        [
                            (edge[0]-self.parameters['Dimensions'][0]
                            /(2*self.parameters['Subdivisions'][0])),
                            (edge[1]+self.parameters['Dimensions'][1]
                            /(2*self.parameters['Subdivisions'][1]))
                        ],
                        self.parameters['Angle'])
                    )

                self.polygons.append(temp)

    def generate(self, size_x, size_y):
        '''
        Generate the mask element by calling the 
        setup and then patching the masks
        '''
        self.setup()
        self.mask = np.zeros((size_x, size_y), dtype=np.int16)

        for i,polygon in enumerate(self.polygons):
            temp_map = self.processPolygon(polygon, size_x, size_y)
            if self.parameters['Increment']:
                self.mask += temp_map * (i+1)
                self.mask[self.mask > (i+1)] = (i+1)
            else:
                self.mask += temp_map
                self.mask[self.mask >1] = 1

        return self.mask
