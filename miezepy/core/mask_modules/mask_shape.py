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
from PIL import Image, ImageDraw


class MaskShape:

    def __init__(self):
        '''
        This will be the miezepy shape default class
        and will then be inherited by the different
        other classes. It avoids repeating definitions.
        '''
        self.parameters = {}

        self.parameters['index']    = 0
        self.parameters['color']    = (0,0,0)
        self.parameters['exclude']  = False
        self.parameters['processed']= False
        self.parameters['increment']= True
        self.parameters['methods']  = []

        self.parameters['angle']    = 0
        self.parameters['position'] = [0, 0]

    def move(self, relative = [None,None], absolute = [None,None]):
        '''
        Set the move method general to all objects 
        in the inherited class allows flexibility
        '''
        if any([not element == None for element in absolute]):
            self.parameters['position'] = list(absolute)
            self.parameters['processed'] = False

        elif any([not element == None for element in relative]):
            self.parameters['position'][0] += relative[0]
            self.parameters['position'][1] += relative[1]
            self.parameters['processed'] = False
        
    def rotate(self, relative = None, absolute = None):
        '''
        Set the move method general to all objects 
        in the inherited class allows flexibility
        '''
        if not absolute == None:
            self.parameters['angle'] = absolute
            self.parameters['processed'] = False

        elif not relative == None:
            self.parameters['angle'] += relative
            self.parameters['processed'] = False
               
    def processPolygon(self, edges, size_x, size_y):
        '''
        This method is universal and will check if 
        a point is situated within a polygon 
        defined by the the edges.
        '''

        temp_image = Image.new('1', (size_x, size_y))
        temp_draw = ImageDraw.Draw(temp_image)
        
        temp_draw.polygon(tuple([tuple(edge) for edge in edges]), fill = 1)

        return np.array(temp_image).astype(np.int16)

    def processSector(self, radius_range, angle_range, size_x, size_y):
        '''
        This part will process a circular region of the 
        current numpy array range. This part was taken
        of the original python MIEZE package of TUM.
        '''
        # -> Check whether sector is in image
        y, x        = np.ogrid[:size_x,:size_y]
        cx,cy       = self.parameters['position']
        t_min,t_max = np.deg2rad(angle_range)

        if t_max < t_min:
            t_max += 2 * np.pi

        #convert cartesian --> polar coordinates
        r2 = ( x - cx ) * ( x - cx ) + ( y - cy ) * ( y - cy )
        theta = np.arctan2(y-cy,x-cx) - t_min

        #wrap angles between 0 and 2*pi
        theta %= (2*np.pi)

        #circular mask
        circmask    = r2 <  radius_range[1] * radius_range[1]
        circmask2   = r2 >= radius_range[0] * radius_range[0]

        # angular mask
        anglemask = theta <= (t_max-t_min)
        mask =  (circmask * circmask2 * anglemask).astype(np.int16)

        return mask

    def rotatePoint(self, origin, point, angle):
        """
        Rotate a point counterclockwise by a given 
        angle around a given origin.
        The angle should be given in radians.
        """
        ox, oy = origin
        px, py = point

        angle = np.deg2rad(angle)

        qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
        qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)

        return [qx, qy]