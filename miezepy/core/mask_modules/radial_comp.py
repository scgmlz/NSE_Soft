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
from .linear_comp   import LinearComposition


class RadialComposition(LinearComposition):
    
    def __init__(self):
        '''
        This is the grid mode of the element. 
        Note that this composition can only 
        be set to close gaps if the subelement
        is of rectangular shape.
        '''
        LinearComposition.__init__(self)
        self.initialize()

    def initialize(self):
        '''
        This routine will edit the inherited 
        dictionary of parameters.
        '''
        self.parameters['Name']                 = 'Radial composition'
        self.parameters['child']                = {'Name':'Arc'}
        self.parameters['Multiplicity']         = [1,1]
        self.parameters['Angular range']        = [0, 360]
        self.parameters['Radial range']         = [30, 60]
        self.parameters['Close Gap']            = True
        self.parameters['Increment']            = True
        
        self.children = []
        self.setChildType('Arc')

    def setDirectly(self, **kwargs):
        '''
        The mask generator favours the direct
        input of the values onto the mask
        and will therefore send it to the mask
        element to be anaged.
        '''
        self.parameters = kwargs
        self.setChildType(self.parameters['child']['Name'], self.parameters['child'])

    def setup(self):
        '''
        Setup the grid with the elements within
        '''
        t = np.deg2rad(np.linspace(
            self.parameters['Angular range'][0],
            self.parameters['Angular range'][1],
            num = self.parameters['Multiplicity'][0]))

        r = np.linspace(
            self.parameters['Radial range'][0],
            self.parameters['Radial range'][1],
            num = self.parameters['Multiplicity'][1]) 

        rr, tt = np.meshgrid(r, t)
        
        edges = []
        angles = []

        for i in range(tt.shape[0]):
            for j in range(tt.shape[1]):
                edges.append([
                    rr[i,j] * np.cos(tt[i,j]) + self.parameters['Position'][0], 
                    rr[i,j] * np.sin(tt[i,j]) + self.parameters['Position'][1]])

                angles.append(tt[i,j])

        for i in range(len(edges)):
            edges[i] = self.rotatePoint(
                self.parameters['Position'],
                edges[i],
                self.parameters['Angle'])

        self.children = []

        for i, edge in enumerate(edges):
            element = copy.deepcopy(self.template)
            if self.parameters['child']['Name'] == 'Arc' and self.parameters['Close Gap']:
                element.move(absolute = self.parameters['Position'])
                element.parameters['Angular range'] = [
                    np.rad2deg(angles[i] - np.abs(t[1]-t[0])/2),
                    np.rad2deg(angles[i] + np.abs(t[1]-t[0])/2)]
                element.parameters['Radial range'] = [
                    np.linalg.norm(
                        np.array(edge) 
                        - np.array(self.parameters['Position'])) 
                    - np.abs(r[1]-r[0])/2,
                    np.linalg.norm(
                        np.array(edge) 
                        - np.array(self.parameters['Position'])) 
                    + np.abs(r[1]-r[0])/2]
                element.rotate(absolute = self.parameters['Angle'])
            else:
                element.move(absolute = edge)
                element.rotate(absolute = self.parameters['Angle'])
                element.rotate(relative = np.rad2deg(angles[i]))
            self.children.append(element)
