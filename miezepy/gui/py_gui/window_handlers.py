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
from PyQt5 import QtGui, QtCore, QtWidgets

from .main_window           import MainWindowLayout
from .gui_data.meta_window           import MetadataWindowLayout
from .gui_data.display_raw_window    import DisplayRawWindowLayout

from ...gui.qt_gui import images_rcc

class WindowHandler:
    '''
    Initializer of the class, It will immediately call
    the first Managing instance to initialize a first
    window level. This will always be alive as it 
    contains the holder frame.
    
    The manager will also create root of the bat. 
    Tkinter build tge windows with dependance and
    root needs to be initialise from the start. 
    '''

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

    def initialize(self, link):
        '''
        This routine performs the initialization in case that the 
        gui is loaded.
        '''
        self.window_dictionary = {}
        self.window_dictionary['MainWindow']    = [MainWindowLayout, None]
        self.window_dictionary['MetaWindow']    = [MetadataWindowLayout, 'MainWindow']
        self.window_dictionary['RawVisual']     = [DisplayRawWindowLayout, 'MainWindow']

        self.active_windows = {}

        self.main_window = MainWindow(self)
        self.main_window.show()
        self.active_windows['MainWindow'] = self.main_window
        self.active_windows['MainWindow'].target.link(link)
        self.main_window.show()

    def newWindow(self, name):
        '''
        Create a new window
        '''
        if name in self.window_dictionary.keys():
            saved = False

            if name in self.active_windows.keys():
                settings = QtCore.QSettings()
                settings.setValue(
                    'geometry',
                    self.active_windows[name].saveGeometry())
                settings.setValue(
                    'windowState',
                    self.active_windows[name].saveState())
                self.active_windows[name].close()
                saved = True
                
            self.active_windows[name] = (
                ChildWindow(
                    self.active_windows[self.window_dictionary[name][1]],
                    self.window_dictionary[name][0],
                    self))
            if saved:
                self.active_windows[name].restoreGeometry(
                    settings.value("geometry"))
                self.active_windows[name].restoreState(settings.value(
                    "windowState"))

            self.active_windows[name].show()
        
    def run(self):
        '''
        Run the application
        '''
        sys.exit(self.app.exec_())

class MainWindow(QtWidgets.QMainWindow):
    '''
    This class is the main window that will be 
    used as a window base. All other windows will
    be children.
    '''
    def __init__(self, window_manager, parent = None):
        super(MainWindow, self).__init__(parent)
        self.target = MainWindowLayout(self, window_manager)
        self.setWindowIcon(QtGui.QIcon(':/Ressources/miezepy_logo.svg'))

    def closeEvent(self, event):
        # do stuff
        event.accept() # let the window close
        sys.exit()

class ChildWindow(QtWidgets.QMainWindow):
    '''
    This class will launch and generate the child
    windows. Note that this is simply a wrapper
    that will then call the target class defining
    the arrangement. 
    '''
    def __init__(self, parent, target, window_manager):

        #set the inheritance 
        super(ChildWindow, self).__init__(parent = parent)
        self.setWindowIcon(QtGui.QIcon(':/Ressources/miezepy_logo.svg'))

        #set the gui
        self.parent = parent
        self.target = target(self, window_manager)

