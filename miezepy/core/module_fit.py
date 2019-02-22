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
import iminuit
import numpy as np
import scipy
import warnings
import copy
import math
import timeit
 

#############################
#import child components
from .fit_modules.fit_mieze import Fit_MIEZE
from .fit_modules.fit_sans import Fit_SANS
    
def getFitStructure(select):
    '''
    Will return the right fit manager depending 
    on the initial input
    Input: target (Data_Structure)
    '''
    if select == 'MIEZE':
        return Fit_MIEZE()
    if select == 'SANS':
        return Fit_SANS()
    else:
        print('Could not find the fit class you are looking for. Error...')
        return None



