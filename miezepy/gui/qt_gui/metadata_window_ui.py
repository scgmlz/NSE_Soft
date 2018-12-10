# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'metadata_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_select_meta(object):
    def setupUi(self, select_meta):
        select_meta.setObjectName("select_meta")
        select_meta.resize(519, 451)
        select_meta.setStyleSheet("#main_widget{\n"
"background-color: rgb(64, 66, 68);}")
        self.main_widget = QtWidgets.QWidget(select_meta)
        self.main_widget.setObjectName("main_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.meta_label_select = QtWidgets.QLabel(self.main_widget)
        self.meta_label_select.setStyleSheet("#meta_label_select{color: rgb(179, 179, 179);}")
        self.meta_label_select.setObjectName("meta_label_select")
        self.horizontalLayout.addWidget(self.meta_label_select)
        self.meta_input_select = QtWidgets.QLineEdit(self.main_widget)
        self.meta_input_select.setObjectName("meta_input_select")
        self.horizontalLayout.addWidget(self.meta_input_select)
        self.meta_button_select = QtWidgets.QToolButton(self.main_widget)
        self.meta_button_select.setObjectName("meta_button_select")
        self.horizontalLayout.addWidget(self.meta_button_select)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.meta_input_filter = QtWidgets.QLineEdit(self.main_widget)
        self.meta_input_filter.setObjectName("meta_input_filter")
        self.horizontalLayout_3.addWidget(self.meta_input_filter)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.meta_list_list = QtWidgets.QListView(self.main_widget)
        self.meta_list_list.setObjectName("meta_list_list")
        self.verticalLayout.addWidget(self.meta_list_list)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.meta_button_reset = QtWidgets.QPushButton(self.main_widget)
        self.meta_button_reset.setObjectName("meta_button_reset")
        self.horizontalLayout_2.addWidget(self.meta_button_reset)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.meta_button_cancel = QtWidgets.QPushButton(self.main_widget)
        self.meta_button_cancel.setObjectName("meta_button_cancel")
        self.horizontalLayout_2.addWidget(self.meta_button_cancel)
        self.meta_button_accept = QtWidgets.QPushButton(self.main_widget)
        self.meta_button_accept.setDefault(True)
        self.meta_button_accept.setFlat(False)
        self.meta_button_accept.setObjectName("meta_button_accept")
        self.horizontalLayout_2.addWidget(self.meta_button_accept)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        select_meta.setCentralWidget(self.main_widget)
        self.menubar = QtWidgets.QMenuBar(select_meta)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 519, 22))
        self.menubar.setObjectName("menubar")
        select_meta.setMenuBar(self.menubar)

        self.retranslateUi(select_meta)
        QtCore.QMetaObject.connectSlotsByName(select_meta)

    def retranslateUi(self, select_meta):
        _translate = QtCore.QCoreApplication.translate
        select_meta.setWindowTitle(_translate("select_meta", "Select Metadata ..."))
        self.meta_label_select.setText(_translate("select_meta", "Path: "))
        self.meta_button_select.setText(_translate("select_meta", "..."))
        self.meta_button_reset.setText(_translate("select_meta", "Reset"))
        self.meta_button_cancel.setText(_translate("select_meta", "Cancel"))
        self.meta_button_accept.setText(_translate("select_meta", "Accept"))

