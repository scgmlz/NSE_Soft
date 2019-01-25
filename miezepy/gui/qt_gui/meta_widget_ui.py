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
        meta_widget.resize(260, 57)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(meta_widget.sizePolicy().hasHeightForWidth())
        meta_widget.setSizePolicy(sizePolicy)
        meta_widget.setMinimumSize(QtCore.QSize(260, 0))
        meta_widget.setMaximumSize(QtCore.QSize(1000, 500))
        meta_widget.setSizeIncrement(QtCore.QSize(0, 0))
        meta_widget.setBaseSize(QtCore.QSize(260, 0))
        meta_widget.setStyleSheet("#meta_widget{\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-color: rgb(0, 0, 0);}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(meta_widget)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.meta_label_name = QtWidgets.QLabel(meta_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.meta_label_name.sizePolicy().hasHeightForWidth())
        self.meta_label_name.setSizePolicy(sizePolicy)
        self.meta_label_name.setMinimumSize(QtCore.QSize(100, 0))
        self.meta_label_name.setMaximumSize(QtCore.QSize(100, 16777215))
        self.meta_label_name.setBaseSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.meta_label_name.setFont(font)
        self.meta_label_name.setText("TextLabel")
        self.meta_label_name.setScaledContents(True)
        self.meta_label_name.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.meta_label_name.setWordWrap(False)
        self.meta_label_name.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.meta_label_name.setObjectName("meta_label_name")
        self.horizontalLayout.addWidget(self.meta_label_name)
        self.meta_input_fact = QtWidgets.QLineEdit(meta_widget)
        self.meta_input_fact.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.meta_input_fact.sizePolicy().hasHeightForWidth())
        self.meta_input_fact.setSizePolicy(sizePolicy)
        self.meta_input_fact.setMinimumSize(QtCore.QSize(40, 0))
        self.meta_input_fact.setMaximumSize(QtCore.QSize(40, 40))
        self.meta_input_fact.setBaseSize(QtCore.QSize(40, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.meta_input_fact.setFont(font)
        self.meta_input_fact.setAcceptDrops(False)
        self.meta_input_fact.setText("")
        self.meta_input_fact.setFrame(True)
        self.meta_input_fact.setObjectName("meta_input_fact")
        self.horizontalLayout.addWidget(self.meta_input_fact)
        self.meta_drop_equivalence = QtWidgets.QComboBox(meta_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.meta_drop_equivalence.sizePolicy().hasHeightForWidth())
        self.meta_drop_equivalence.setSizePolicy(sizePolicy)
        self.meta_drop_equivalence.setMinimumSize(QtCore.QSize(0, 0))
        self.meta_drop_equivalence.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.meta_drop_equivalence.setFont(font)
        self.meta_drop_equivalence.setCurrentText("")
        self.meta_drop_equivalence.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.meta_drop_equivalence.setFrame(True)
        self.meta_drop_equivalence.setObjectName("meta_drop_equivalence")
        self.horizontalLayout.addWidget(self.meta_drop_equivalence)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.meta_label_manual = QtWidgets.QLabel(meta_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.meta_label_manual.sizePolicy().hasHeightForWidth())
        self.meta_label_manual.setSizePolicy(sizePolicy)
        self.meta_label_manual.setMinimumSize(QtCore.QSize(50, 0))
        self.meta_label_manual.setMaximumSize(QtCore.QSize(50, 16777215))
        self.meta_label_manual.setBaseSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.meta_label_manual.setFont(font)
        self.meta_label_manual.setText("Manual")
        self.meta_label_manual.setScaledContents(True)
        self.meta_label_manual.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.meta_label_manual.setWordWrap(False)
        self.meta_label_manual.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.meta_label_manual.setObjectName("meta_label_manual")
        self.horizontalLayout_2.addWidget(self.meta_label_manual)
        self.meta_input_manual = QtWidgets.QLineEdit(meta_widget)
        self.meta_input_manual.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.meta_input_manual.sizePolicy().hasHeightForWidth())
        self.meta_input_manual.setSizePolicy(sizePolicy)
        self.meta_input_manual.setMinimumSize(QtCore.QSize(0, 0))
        self.meta_input_manual.setMaximumSize(QtCore.QSize(500, 500))
        self.meta_input_manual.setBaseSize(QtCore.QSize(40, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.meta_input_manual.setFont(font)
        self.meta_input_manual.setAcceptDrops(False)
        self.meta_input_manual.setText("")
        self.meta_input_manual.setFrame(True)
        self.meta_input_manual.setObjectName("meta_input_manual")
        self.horizontalLayout_2.addWidget(self.meta_input_manual)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(meta_widget)
        QtCore.QMetaObject.connectSlotsByName(meta_widget)

    def retranslateUi(self, meta_widget):
        _translate = QtCore.QCoreApplication.translate
        meta_widget.setWindowTitle(_translate("meta_widget", "Form"))

