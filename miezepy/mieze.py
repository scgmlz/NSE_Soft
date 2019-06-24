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
#import main components
from .core.core_handler             import CoreHandler
from .gui.py_gui.window_handlers    import WindowHandler
import os

class Mieze(CoreHandler):
    '''
    Here lies the main NSE tool manager class. It can be
    accessed in the python terminal through: 
    "from NSE.Main import Manager as NSE"
    '''

    def __init__(self, GUI = False):
        '''
        initialise app components
        '''
        self.success = False
        self.checkRessources()
        
        #initiate the core manager  
        CoreHandler.__init__(self)

        #initiate the GUI manager if need be
        if GUI == True:
            self.gui = WindowHandler()
            self.gui.initialize(self)

        self.success = True

    def checkRessources(self):
        '''
        The ressources are not part of the git package
        and may not be present on first launch. This littel
        function will try to lacate the files and then take
        the appropriate measures.
        '''
        base = str(os.path.realpath(__file__)).split(os.path.sep)[0:-1]

        #resources directory
        ressource_directory_path = os.path.realpath(os.path.sep.join(
            base + ['ressources', '']))
        if not os.path.isdir(ressource_directory_path):
            os.mkdir(ressource_directory_path)

        #the default post processing save path
        default_post_path = os.path.realpath(os.path.sep.join(
            base + ['ressources', 'default_post_path.txt']))
        if not os.path.isfile(default_post_path):
            f = open(default_post_path,'w')
            f.write('')
            f.close()

    def run(self, test = False):
        '''
        Execute the application upon initialization
        '''
        self.gui.run()

if __name__ == '__main__':

    app = Mieze(GUI = True)
    # app.gui.active_windows['MainWindow'].target.widgetClasses[0].addEnvironment()
    # env = app.current_env
    # env.io.loadFromPython(
    #     "Examples/file_3.py")
    # app.gui.active_windows['MainWindow'].target.widgetClasses[0].refreshData()
    # app.gui.active_windows['MainWindow'].target.actionDispatcher(3)
    # app.gui.active_windows['MainWindow'].target.widgetClasses[3].run(0)
    # app.gui.active_windows['MainWindow'].target.widgetClasses[3].run(1)
    # app.gui.active_windows['MainWindow'].target.widgetClasses[3].run(2)

    app.run()
