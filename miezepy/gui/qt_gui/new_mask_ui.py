# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_mask.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_new_msk(object):
    def setupUi(self, new_msk):
        new_msk.setObjectName("new_msk")
        new_msk.resize(322, 96)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(new_msk.sizePolicy().hasHeightForWidth())
        new_msk.setSizePolicy(sizePolicy)
        new_msk.setMinimumSize(QtCore.QSize(322, 96))
        new_msk.setMaximumSize(QtCore.QSize(322, 96))
        self.centralwidget = QtWidgets.QWidget(new_msk)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.new_mask_name = QtWidgets.QLineEdit(self.centralwidget)
        self.new_mask_name.setObjectName("new_mask_name")
        self.horizontalLayout_2.addWidget(self.new_mask_name)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.ok_button = QtWidgets.QPushButton(self.centralwidget)
        self.ok_button.setObjectName("ok_button")
        self.horizontalLayout.addWidget(self.ok_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        new_msk.setCentralWidget(self.centralwidget)

        self.retranslateUi(new_msk)
        QtCore.QMetaObject.connectSlotsByName(new_msk)

    def retranslateUi(self, new_msk):
        _translate = QtCore.QCoreApplication.translate
        new_msk.setWindowTitle(_translate("new_msk", "Select a mask name"))
        self.label.setText(_translate("new_msk", "Mask name"))
        self.cancel_button.setText(_translate("new_msk", "Cancel"))
        self.ok_button.setText(_translate("new_msk", "Ok"))

