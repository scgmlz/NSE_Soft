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

#hey dude
#############################
#import main components
from .CORE_Ressources.CORE_Manager import CORE_Manager
from .GUI_Ressources.GUI_Manager import GUI_Manager


class Manager (CORE_Manager, GUI_Manager):

    '''
    ##############################################
    Here lies the main NSE tool manager class. It can be
    accessed in the python terminal through: 
    "from NSE.Main import Manager as NSE"

    Note that setting GUI = True will launch the Tk/Tlc
    based interface.
     
    ##############################################
    '''

    def __init__(self, GUI = False):

        ##############################################
        #initiate the core manager  
        CORE_Manager.__init__(self)

        ##############################################
        #initiate the GUI manager if need be
        if GUI == True:

            GUI_Manager.__init__(self)
