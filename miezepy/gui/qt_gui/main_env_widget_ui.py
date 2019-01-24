# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_env_widget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_env_widget(object):
    def setupUi(self, env_widget):
        env_widget.setObjectName("env_widget")
        env_widget.resize(559, 317)
        env_widget.setStyleSheet("#env_widget{background-color: rgb(179, 179, 179);}")
        self.verticalLayout = QtWidgets.QVBoxLayout(env_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.env_button_add = QtWidgets.QPushButton(env_widget)
        self.env_button_add.setObjectName("env_button_add")
        self.horizontalLayout.addWidget(self.env_button_add)
        self.env_button_remove = QtWidgets.QPushButton(env_widget)
        self.env_button_remove.setObjectName("env_button_remove")
        self.horizontalLayout.addWidget(self.env_button_remove)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.main_widget_env = QtWidgets.QListWidget(env_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_widget_env.sizePolicy().hasHeightForWidth())
        self.main_widget_env.setSizePolicy(sizePolicy)
        self.main_widget_env.setStyleSheet("main_widget_env::item{\n"
"border: 2px solid black ;\n"
"background-color: rgb(217, 217, 217);\n"
"}\n"
"\n"
"main_widget_env::item:selected{\n"
"border: 2px solid black ;\n"
"background-color: rgb(120, 120, 120);\n"
"}")
        self.main_widget_env.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.main_widget_env.setObjectName("main_widget_env")
        self.verticalLayout.addWidget(self.main_widget_env)

        self.retranslateUi(env_widget)
        QtCore.QMetaObject.connectSlotsByName(env_widget)

    def retranslateUi(self, env_widget):
        _translate = QtCore.QCoreApplication.translate
        env_widget.setWindowTitle(_translate("env_widget", "Form"))
        self.env_button_add.setText(_translate("env_widget", "+"))
        self.env_button_remove.setText(_translate("env_widget", "-"))

