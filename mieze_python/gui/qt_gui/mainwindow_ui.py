# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MIEZETool(object):
    def setupUi(self, MIEZETool):
        MIEZETool.setObjectName("MIEZETool")
        MIEZETool.resize(1239, 843)
        self.centralwidget = QtWidgets.QWidget(MIEZETool)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.main_widget_env = QtWidgets.QListWidget(self.centralwidget)
        self.main_widget_env.setObjectName("main_widget_env")
        self.horizontalLayout.addWidget(self.main_widget_env)
        MIEZETool.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MIEZETool)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1239, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuCurrent_Environment = QtWidgets.QMenu(self.menuFile)
        self.menuCurrent_Environment.setObjectName("menuCurrent_Environment")
        MIEZETool.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MIEZETool)
        self.statusbar.setObjectName("statusbar")
        MIEZETool.setStatusBar(self.statusbar)
        self.actionAdd_Environement = QtWidgets.QAction(MIEZETool)
        self.actionAdd_Environement.setObjectName("actionAdd_Environement")
        self.actionAdd_Data = QtWidgets.QAction(MIEZETool)
        self.actionAdd_Data.setObjectName("actionAdd_Data")
        self.actionLoad_Data = QtWidgets.QAction(MIEZETool)
        self.actionLoad_Data.setObjectName("actionLoad_Data")
        self.actionCompute = QtWidgets.QAction(MIEZETool)
        self.actionCompute.setObjectName("actionCompute")
        self.actionResult = QtWidgets.QAction(MIEZETool)
        self.actionResult.setObjectName("actionResult")
        self.menuCurrent_Environment.addAction(self.actionAdd_Data)
        self.menuCurrent_Environment.addAction(self.actionLoad_Data)
        self.menuCurrent_Environment.addAction(self.actionCompute)
        self.menuCurrent_Environment.addSeparator()
        self.menuCurrent_Environment.addAction(self.actionResult)
        self.menuFile.addAction(self.actionAdd_Environement)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuCurrent_Environment.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MIEZETool)
        QtCore.QMetaObject.connectSlotsByName(MIEZETool)

    def retranslateUi(self, MIEZETool):
        _translate = QtCore.QCoreApplication.translate
        MIEZETool.setWindowTitle(_translate("MIEZETool", "MIEZE Tool"))
        self.menuFile.setTitle(_translate("MIEZETool", "File"))
        self.menuCurrent_Environment.setTitle(_translate("MIEZETool", "Current Environment"))
        self.actionAdd_Environement.setText(_translate("MIEZETool", "Add Environement"))
        self.actionAdd_Data.setText(_translate("MIEZETool", "Add Data"))
        self.actionLoad_Data.setText(_translate("MIEZETool", "Load Data"))
        self.actionCompute.setText(_translate("MIEZETool", "Compute"))
        self.actionResult.setText(_translate("MIEZETool", "Result ..."))

