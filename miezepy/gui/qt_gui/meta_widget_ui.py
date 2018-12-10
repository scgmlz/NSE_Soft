# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'meta_widget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_meta_widget(object):
    def setupUi(self, meta_widget):
        meta_widget.setObjectName("meta_widget")
        meta_widget.resize(260, 36)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(meta_widget.sizePolicy().hasHeightForWidth())
        meta_widget.setSizePolicy(sizePolicy)
        meta_widget.setMinimumSize(QtCore.QSize(260, 0))
        meta_widget.setMaximumSize(QtCore.QSize(260, 16777215))
        meta_widget.setBaseSize(QtCore.QSize(260, 0))
        self.horizontalLayout = QtWidgets.QHBoxLayout(meta_widget)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.meta_label_name = QtWidgets.QLabel(meta_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.meta_label_name.sizePolicy().hasHeightForWidth())
        self.meta_label_name.setSizePolicy(sizePolicy)
        self.meta_label_name.setMinimumSize(QtCore.QSize(100, 0))
        self.meta_label_name.setMaximumSize(QtCore.QSize(100, 16777215))
        self.meta_label_name.setBaseSize(QtCore.QSize(100, 0))
        self.meta_label_name.setText("TextLabel")
        self.meta_label_name.setScaledContents(True)
        self.meta_label_name.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.meta_label_name.setWordWrap(False)
        self.meta_label_name.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.meta_label_name.setObjectName("meta_label_name")
        self.horizontalLayout.addWidget(self.meta_label_name)
        self.meta_input_fact = QtWidgets.QLineEdit(meta_widget)
        self.meta_input_fact.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.meta_input_fact.sizePolicy().hasHeightForWidth())
        self.meta_input_fact.setSizePolicy(sizePolicy)
        self.meta_input_fact.setMinimumSize(QtCore.QSize(40, 0))
        self.meta_input_fact.setMaximumSize(QtCore.QSize(40, 16777215))
        self.meta_input_fact.setBaseSize(QtCore.QSize(40, 0))
        self.meta_input_fact.setAcceptDrops(False)
        self.meta_input_fact.setText("")
        self.meta_input_fact.setFrame(True)
        self.meta_input_fact.setObjectName("meta_input_fact")
        self.horizontalLayout.addWidget(self.meta_input_fact)
        self.meta_drop_equivalence = QtWidgets.QComboBox(meta_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.meta_drop_equivalence.sizePolicy().hasHeightForWidth())
        self.meta_drop_equivalence.setSizePolicy(sizePolicy)
        self.meta_drop_equivalence.setObjectName("meta_drop_equivalence")
        self.horizontalLayout.addWidget(self.meta_drop_equivalence)

        self.retranslateUi(meta_widget)
        QtCore.QMetaObject.connectSlotsByName(meta_widget)

    def retranslateUi(self, meta_widget):
        _translate = QtCore.QCoreApplication.translate
        meta_widget.setWindowTitle(_translate("meta_widget", "Form"))

