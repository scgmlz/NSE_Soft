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


import sys
import io
import numpy as np

from .CORE_Modules.CORE_Import_MIEZE_TOF import Import_MIEZE_TOF
from .CORE_Modules.CORE_Import_SANS_PAD import Import_SANS_PAD

class IO_Manager:

    def __init__(self):

        self.verbose = True

    def load_MIEZE_TOF(self,load_path, target):
        '''
        ##############################################
        This function will manage the load of tof
        files through different smaller import
        components
        ##############################################
        '''
        load = Import_MIEZE_TOF(load_path,target)

    def load_MIEZE_HD5(self,load_path, target):
        '''
        ##############################################
        This function will manage the load of tof
        files through different smaller import
        components
        ##############################################
        '''

        pass


    def load_SANS_PAD(self,load_path, target):
        '''
        ##############################################
        This function will import the data from the 
        PAD format. 
        ##############################################
        '''

        load = Import_SANS_PAD(load_path,target)

         