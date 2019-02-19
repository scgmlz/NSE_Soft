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
from .core.core_handler             import Handler
from .gui.py_gui.window_handlers    import WindowHandler


class Mieze(Handler):

    '''
    ##############################################
    Here lies the main NSE tool manager class. It can be
    accessed in the python terminal through: 
    "from NSE.Main import Manager as NSE"
    ##############################################
    '''

    def __init__(self, GUI = False):

        ##############################################
        #initiate the core manager  
        Handler.__init__(self)

        ##############################################
        #initiate the GUI manager if need be
        if GUI == True:

            self.gui = WindowHandler(self)

    def run(self):
        self.gui.run()


import sys
from PyQt5.QtGui import QIcon
 
from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
QTime)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
QWidget)

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Treeview Example - pythonspot.com'
        self.width = 640
        self.height = 800
    
    def initUI(self):
        self.setWindowTitle(self.title)
        
        self.dataGroupBox = QGroupBox("Inbox")
        self.dataView_1 = QTreeView()
        self.dataView_2 = QTreeView()
        # self.dataView.setRootIsDecorated(False)
        # self.dataView.setAlternatingRowColors(True)
        
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView_1)
        dataLayout.addWidget(self.dataView_2)
        self.dataGroupBox.setLayout(dataLayout)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.dataGroupBox)
        self.setLayout(mainLayout)
        
        self.show()

if __name__ == '__main__':
    app = Mieze(GUI = True)
    app.gui.active_windows['MainWindow'].target.widgetClasses[0].addEnvironment()
    env = app.current_env
    env.io.loadFromPython(
        "Examples/file_3.py")
    app.gui.active_windows['MainWindow'].target.widgetClasses[0].refreshData()
    app.gui.active_windows['MainWindow'].target.actionDispatcher(3)
    app.gui.active_windows['MainWindow'].target.widgetClasses[3].run(0)
    app.gui.active_windows['MainWindow'].target.widgetClasses[3].run(1)
    app.gui.active_windows['MainWindow'].target.widgetClasses[3].run(2)

    app.run()
    # env_handler =  Handler()
    # env_handler.new_environment()
    # env_handler.current_env.mask.addElement([
    #             'arc',
    #             (31,35),
    #             0,
    #             (0,5), 
    #             (0,360)])

    # from .gui.py_gui.mask_visual_handler import MaskVisualHandler
    # mask_visual = MaskVisualHandler()
    # mask_visual.link(env_handler.current_env.mask)
    # app = QApplication(sys.argv)
    # test = App()
    # test.initUI()
    
    # mask_visual.connectView('hey', test.dataView_1)
    # mask_visual.connectView('hey_2', test.dataView_2)
    # test.dataView_1.resizeColumnToContents(0)
    # sys.exit(app.exec_())

