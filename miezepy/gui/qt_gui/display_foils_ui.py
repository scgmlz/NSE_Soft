# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'display_foils.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_foil_display(object):
    def setupUi(self, foil_display):
        foil_display.setObjectName("foil_display")
        foil_display.resize(805, 600)
        foil_display.setStyleSheet("#main_widget{\n"
"background-color: rgb(64, 66, 68);}")
        self.main_widget = QtWidgets.QWidget(foil_display)
        self.main_widget.setObjectName("main_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.foil_detector_label = QtWidgets.QLabel(self.main_widget)
        self.foil_detector_label.setStyleSheet("#foil_label{color: rgb(179, 179, 179);}")
        self.foil_detector_label.setObjectName("foil_detector_label")
        self.horizontalLayout.addWidget(self.foil_detector_label)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.foil_label = QtWidgets.QLabel(self.main_widget)
        self.foil_label.setStyleSheet("#foil_label{color: rgb(179, 179, 179);}")
        self.foil_label.setObjectName("foil_label")
        self.horizontalLayout.addWidget(self.foil_label)
        self.foil_spin = QtWidgets.QSpinBox(self.main_widget)
        self.foil_spin.setObjectName("foil_spin")
        self.horizontalLayout.addWidget(self.foil_spin)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.foil_factor_label = QtWidgets.QLabel(self.main_widget)
        self.foil_factor_label.setStyleSheet("#foil_label{color: rgb(179, 179, 179);}")
        self.foil_factor_label.setObjectName("foil_factor_label")
        self.horizontalLayout.addWidget(self.foil_factor_label)
        self.foil_factor_spin = QtWidgets.QDoubleSpinBox(self.main_widget)
        self.foil_factor_spin.setDecimals(5)
        self.foil_factor_spin.setMinimum(-1000000000000000.0)
        self.foil_factor_spin.setMaximum(1e+16)
        self.foil_factor_spin.setSingleStep(100.0)
        self.foil_factor_spin.setProperty("value", 3000.0)
        self.foil_factor_spin.setObjectName("foil_factor_spin")
        self.horizontalLayout.addWidget(self.foil_factor_spin)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.graph_widget = QtWidgets.QWidget(self.main_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graph_widget.sizePolicy().hasHeightForWidth())
        self.graph_widget.setSizePolicy(sizePolicy)
        self.graph_widget.setStyleSheet("#graph_widget{background-color: rgb(179, 179, 179);}")
        self.graph_widget.setObjectName("graph_widget")
        self.verticalLayout.addWidget(self.graph_widget)
        foil_display.setCentralWidget(self.main_widget)
        self.menubar = QtWidgets.QMenuBar(foil_display)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 805, 27))
        self.menubar.setObjectName("menubar")
        foil_display.setMenuBar(self.menubar)

        self.retranslateUi(foil_display)
        QtCore.QMetaObject.connectSlotsByName(foil_display)

    def retranslateUi(self, foil_display):
        _translate = QtCore.QCoreApplication.translate
        foil_display.setWindowTitle(_translate("foil_display", "MainWindow"))
        self.foil_detector_label.setText(_translate("foil_display", "Detector:"))
        self.foil_label.setText(_translate("foil_display", "Foil"))
        self.foil_factor_label.setText(_translate("foil_display", "Factor"))

