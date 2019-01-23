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

import copy

import numpy as np

from .linear_comp   import LinearComposition
from .radial_comp   import RadialComposition
from .square        import Square
from .triangle      import Triangle
from .circle_arc    import CircleArc

class MaskGenerator:
    
    def __init__(self):
        '''
        This class is an instance to translate the
        information of the Mask class into
        information that can be used by the mask 
        modules. 
        '''
        self.resetElementClasses()
        self.dummies = [
            Square(),
            Triangle(),
            CircleArc(),
            LinearComposition(),
            RadialComposition()]

    def resetElementClasses(self):
        '''
        This method will grab the mask dialogue 
        and then translate it to the proper mask
        class system.
        '''
        self.element_classes = []

    def grabMask(self, mask_dialogue, recreate = True):
        '''
        This method will grab the mask dialogue 
        and then translate it to the proper mask
        class system.
        '''
        self.current_dialogue = mask_dialogue

        if recreate:
            self.resetElementClasses()
            for element in self.current_dialogue:
                self.populateElement(element)

        for i, element in enumerate(self.current_dialogue):
            self.setParameters(i, element)

    def populateElement(self, mask_parameters):
        '''
        This method will tell the machinery to
        grab the right class and initialise
        it depending on its type.
        '''
        for element in self.dummies:
            if element.parameters['type'] == mask_parameters[0]:
                self.element_classes.append(copy.deepcopy(element))
                break

    def setParameters(self, idx, mask_parameters):
        '''
        This method will tell the machinery to
        grab the right class and initialise
        it depending on its type.
        '''
        self.element_classes[idx].setDirectly(mask_parameters)

    def generateMask(self, size_x, size_y):
        '''
        This method will tell the machinery to
        grab the right class and initialise
        it depending on its type.
        '''
        self.mask = np.zeros((size_x, size_y)).astype(np.int16)
        for element in self.element_classes:
            temp_mask = np.array(element.generate(size_x, size_y))
            temp_mask[temp_mask>0] += np.amax(self.mask) 
            self.mask +=  temp_mask

        for i in range(np.amax(self.mask)):
            if np.sum(self.mask[self.mask == i]) == 0:
                self.mask[self.mask < i] += 1
        
        self.mask == np.amin(self.mask)



