# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'script_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_script_window(object):
    def setupUi(self, script_window):
        script_window.setObjectName("script_window")
        script_window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(script_window)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.script_group_elements = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.script_group_elements.sizePolicy().hasHeightForWidth())
        self.script_group_elements.setSizePolicy(sizePolicy)
        self.script_group_elements.setObjectName("script_group_elements")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.script_group_elements)
        self.verticalLayout.setObjectName("verticalLayout")
        self.script_label_methods = QtWidgets.QLabel(self.script_group_elements)
        self.script_label_methods.setObjectName("script_label_methods")
        self.verticalLayout.addWidget(self.script_label_methods)
        self.script_tree_methods = QtWidgets.QTreeWidget(self.script_group_elements)
        self.script_tree_methods.setObjectName("script_tree_methods")
        self.script_tree_methods.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.script_tree_methods)
        self.script_label_results = QtWidgets.QLabel(self.script_group_elements)
        self.script_label_results.setObjectName("script_label_results")
        self.verticalLayout.addWidget(self.script_label_results)
        self.script_tree_results = QtWidgets.QTreeWidget(self.script_group_elements)
        self.script_tree_results.setObjectName("script_tree_results")
        self.script_tree_results.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.script_tree_results)
        self.horizontalLayout.addWidget(self.script_group_elements)
        self.script_tab_main = QtWidgets.QTabWidget(self.centralwidget)
        self.script_tab_main.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.script_tab_main.setObjectName("script_tab_main")
        self.script_tab_import = QtWidgets.QWidget()
        self.script_tab_import.setObjectName("script_tab_import")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.script_tab_import)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.script_text_import = QtWidgets.QTextBrowser(self.script_tab_import)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.script_text_import.sizePolicy().hasHeightForWidth())
        self.script_text_import.setSizePolicy(sizePolicy)
        self.script_text_import.setObjectName("script_text_import")
        self.verticalLayout_2.addWidget(self.script_text_import)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.script_button_import_reset = QtWidgets.QPushButton(self.script_tab_import)
        self.script_button_import_reset.setObjectName("script_button_import_reset")
        self.horizontalLayout_2.addWidget(self.script_button_import_reset)
        self.script_button_import_run = QtWidgets.QPushButton(self.script_tab_import)
        self.script_button_import_run.setDefault(True)
        self.script_button_import_run.setObjectName("script_button_import_run")
        self.horizontalLayout_2.addWidget(self.script_button_import_run)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.script_tab_main.addTab(self.script_tab_import, "")
        self.script_tab_phase = QtWidgets.QWidget()
        self.script_tab_phase.setObjectName("script_tab_phase")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.script_tab_phase)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.script_text_phase = QtWidgets.QTextBrowser(self.script_tab_phase)
        self.script_text_phase.setObjectName("script_text_phase")
        self.verticalLayout_3.addWidget(self.script_text_phase)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.script_button_phase_reset = QtWidgets.QPushButton(self.script_tab_phase)
        self.script_button_phase_reset.setObjectName("script_button_phase_reset")
        self.horizontalLayout_5.addWidget(self.script_button_phase_reset)
        self.script_button_phase_run = QtWidgets.QPushButton(self.script_tab_phase)
        self.script_button_phase_run.setDefault(True)
        self.script_button_phase_run.setObjectName("script_button_phase_run")
        self.horizontalLayout_5.addWidget(self.script_button_phase_run)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.script_tab_main.addTab(self.script_tab_phase, "")
        self.script_tab_reduction = QtWidgets.QWidget()
        self.script_tab_reduction.setObjectName("script_tab_reduction")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.script_tab_reduction)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.script_text_reduction = QtWidgets.QTextBrowser(self.script_tab_reduction)
        self.script_text_reduction.setObjectName("script_text_reduction")
        self.verticalLayout_4.addWidget(self.script_text_reduction)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.script_button_reduction_reset = QtWidgets.QPushButton(self.script_tab_reduction)
        self.script_button_reduction_reset.setObjectName("script_button_reduction_reset")
        self.horizontalLayout_6.addWidget(self.script_button_reduction_reset)
        self.script_button_reduction_run = QtWidgets.QPushButton(self.script_tab_reduction)
        self.script_button_reduction_run.setDefault(True)
        self.script_button_reduction_run.setObjectName("script_button_reduction_run")
        self.horizontalLayout_6.addWidget(self.script_button_reduction_run)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.script_tab_main.addTab(self.script_tab_reduction, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.script_text_post = QtWidgets.QTextBrowser(self.tab)
        self.script_text_post.setObjectName("script_text_post")
        self.verticalLayout_8.addWidget(self.script_text_post)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.script_button_post_reset = QtWidgets.QPushButton(self.tab)
        self.script_button_post_reset.setObjectName("script_button_post_reset")
        self.horizontalLayout_7.addWidget(self.script_button_post_reset)
        self.script_button_post_run = QtWidgets.QPushButton(self.tab)
        self.script_button_post_run.setDefault(True)
        self.script_button_post_run.setObjectName("script_button_post_run")
        self.horizontalLayout_7.addWidget(self.script_button_post_run)
        self.verticalLayout_8.addLayout(self.horizontalLayout_7)
        self.script_tab_main.addTab(self.tab, "")
        self.horizontalLayout.addWidget(self.script_tab_main)
        script_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(script_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        script_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(script_window)
        self.statusbar.setObjectName("statusbar")
        script_window.setStatusBar(self.statusbar)

        self.retranslateUi(script_window)
        self.script_tab_main.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(script_window)

    def retranslateUi(self, script_window):
        _translate = QtCore.QCoreApplication.translate
        script_window.setWindowTitle(_translate("script_window", "MainWindow"))
        self.script_group_elements.setTitle(_translate("script_window", "Elements"))
        self.script_label_methods.setText(_translate("script_window", "Methods:"))
        self.script_label_results.setText(_translate("script_window", "Results:"))
        self.script_button_import_reset.setText(_translate("script_window", "Reset"))
        self.script_button_import_run.setText(_translate("script_window", "Run"))
        self.script_tab_main.setTabText(self.script_tab_main.indexOf(self.script_tab_import), _translate("script_window", "Data import"))
        self.script_button_phase_reset.setText(_translate("script_window", "Reset"))
        self.script_button_phase_run.setText(_translate("script_window", "Run"))
        self.script_tab_main.setTabText(self.script_tab_main.indexOf(self.script_tab_phase), _translate("script_window", "Phase correction"))
        self.script_button_reduction_reset.setText(_translate("script_window", "Reset"))
        self.script_button_reduction_run.setText(_translate("script_window", "Run"))
        self.script_tab_main.setTabText(self.script_tab_main.indexOf(self.script_tab_reduction), _translate("script_window", "Reduction"))
        self.script_button_post_reset.setText(_translate("script_window", "Reset"))
        self.script_button_post_run.setText(_translate("script_window", "Run"))
        self.script_tab_main.setTabText(self.script_tab_main.indexOf(self.tab), _translate("script_window", "Post process"))

