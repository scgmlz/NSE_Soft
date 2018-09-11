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


class Manager:

    """
    Here lies the main NSE tool manager class. It can be
    accessed in the python terminal through: 
    "from NSE.Main import Manager as NSE"

    Note that setting GUI = True will launch the Tk/Tlc
    based interface.
     
    """

    def __init__(self, GUI = False):

        ##############################################
        #initiate the core manager  
        self.CORE_Manager = CORE_Manager(parent = self)

        ##############################################
        #initiate the GUI manager if need be
        if GUI == True:

            self.GUI_Manager  = GUI_Manager(self)


    def run(self,command, *args, **kwargs):
        
        """
        ##############################################
        In this function the user can run Core
        commands from the python terminal by inputing
        the command dictioanry key and the arguments.

        -------
        Input : command,*args, **kwargs
        ############################################## 
        """

        self.CORE_Manager.run(command, *args, **kwargs)

    def new(self,command, *args, **kwargs):
        
        """
        ##############################################
        In this function the user can run Core
        commands from the python terminal by inputing
        the command dictioanry key and the arguments.

        -------
        Input : command,*args, **kwargs
        ############################################## 
        """

        self.CORE_Manager.new(command, *args, **kwargs)

    def get(self,command, *args, **kwargs):
        
        """
        ##############################################
        In this function the user can run Core
        commands from the python terminal by inputing
        the command dictioanry key and the arguments.

        -------
        Input : command,*args, **kwargs
        ############################################## 
        """

        return self.CORE_Manager.get(command, *args, **kwargs)

    def set(self,identifier, *args, **kwargs):
        
        """
        ##############################################
        In this function the user can run Core
        commands from the python terminal by inputing
        the command dictioanry key and the arguments.

        -------
        Input : command,*args, **kwargs
        ############################################## 
        """

        self.CORE_Manager.set(identifier, *args, **kwargs)
        
        
    def help(self,command = None):
        """
        ##############################################
        In this function the user can run Core
        commands from the python terminal by inputing
        the command dictioanry key and the arguments

        -------
        Input : command 
        ##############################################
        """

        self.CORE_Manager.help(command = command)
