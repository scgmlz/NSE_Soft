# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_env_widget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_main_env_widget(object):
    def setupUi(self, main_env_widget):
        main_env_widget.setObjectName("main_env_widget")
        main_env_widget.resize(559, 373)
        main_env_widget.setStyleSheet("#main_env_widget{background-color: rgb(179, 179, 179);}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(main_env_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.env_button_add = QtWidgets.QPushButton(main_env_widget)
        self.env_button_add.setObjectName("env_button_add")
        self.horizontalLayout.addWidget(self.env_button_add)
        self.env_button_remove = QtWidgets.QPushButton(main_env_widget)
        self.env_button_remove.setObjectName("env_button_remove")
        self.horizontalLayout.addWidget(self.env_button_remove)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.main_widget_env = QtWidgets.QListWidget(main_env_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_widget_env.sizePolicy().hasHeightForWidth())
        self.main_widget_env.setSizePolicy(sizePolicy)
        self.main_widget_env.setStyleSheet("")
        self.main_widget_env.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.main_widget_env.setObjectName("main_widget_env")
        self.verticalLayout.addWidget(self.main_widget_env)

        self.retranslateUi(main_env_widget)
        QtCore.QMetaObject.connectSlotsByName(main_env_widget)

    def retranslateUi(self, main_env_widget):
        _translate = QtCore.QCoreApplication.translate
        main_env_widget.setWindowTitle(_translate("main_env_widget", "Form"))
        self.env_button_add.setText(_translate("main_env_widget", "+"))
        self.env_button_remove.setText(_translate("main_env_widget", "-"))

