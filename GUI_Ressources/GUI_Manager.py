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
#   Alexander Lenz <alexander.schober@mac.com>
#
# *****************************************************************************


class GUI_Manager:

    def __init__(self, Parent):

        ##############################################
        #initiate the core manager  
        self.Parent = Parent

    def run(self,command):
        '''
        ##############################################
        In this function the user can run Core
        commands from the python terminal by inputing
        the command dictioanry key and the arguments

        -------
        Input : command, 
        ##############################################
        '''
        pass