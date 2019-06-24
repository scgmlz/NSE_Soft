# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'env_widget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_env_widget(object):
    def setupUi(self, env_widget):
        env_widget.setObjectName("env_widget")
        env_widget.resize(520, 232)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(env_widget.sizePolicy().hasHeightForWidth())
        env_widget.setSizePolicy(sizePolicy)
        env_widget.setMinimumSize(QtCore.QSize(0, 0))
        env_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        env_widget.setBaseSize(QtCore.QSize(0, 250))
        env_widget.setAutoFillBackground(False)
        env_widget.setStyleSheet("")
        self.horizontalLayout = QtWidgets.QHBoxLayout(env_widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.env_frame = QtWidgets.QFrame(env_widget)
        self.env_frame.setObjectName("env_frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.env_frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.env_label_name = QtWidgets.QLabel(self.env_frame)
        self.env_label_name.setObjectName("env_label_name")
        self.verticalLayout_3.addWidget(self.env_label_name)
        self.env_input_name = QtWidgets.QLineEdit(self.env_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.env_input_name.sizePolicy().hasHeightForWidth())
        self.env_input_name.setSizePolicy(sizePolicy)
        self.env_input_name.setAcceptDrops(False)
        self.env_input_name.setObjectName("env_input_name")
        self.verticalLayout_3.addWidget(self.env_input_name)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.env_text_data_print = QtWidgets.QTextBrowser(self.env_frame)
        self.env_text_data_print.setObjectName("env_text_data_print")
        self.horizontalLayout_2.addWidget(self.env_text_data_print)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout.addWidget(self.env_frame)

        self.retranslateUi(env_widget)
        QtCore.QMetaObject.connectSlotsByName(env_widget)

    def retranslateUi(self, env_widget):
        _translate = QtCore.QCoreApplication.translate
        env_widget.setWindowTitle(_translate("env_widget", "Form"))
        self.env_label_name.setText(_translate("env_widget", "Name:"))

