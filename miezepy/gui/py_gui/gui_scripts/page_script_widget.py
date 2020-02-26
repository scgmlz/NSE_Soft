#  -*- coding: utf-8 -*-
# *****************************************************************************
# Copyright (c) 2017 by the NSE analysis contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Alexander Schober <alex.schober@mac.com>
#
# *****************************************************************************

#public dependencies
from PyQt5 import QtWidgets, QtGui, QtCore
import traceback
from functools import partial
import numpy as np
import os

#private dependencies
from ...qt_gui.main_script_ui       import Ui_script_widget
from ..gui_common.python_syntax     import PythonHighlighter
from ..gui_mask.page_mask_widget    import PanelPageMaskWidget
from ..gui_common.dialog            import dialog 
from ..gui_common.code_editor       import CodeEditor

from .foil_delegate import FoilDelegate

class PageScriptWidget(Ui_script_widget):
    
    def __init__(self, stack, parent, mask_interface):
        
        Ui_script_widget.__init__(self)
        self.parent         = parent
        self.stack          = stack
        self.local_widget   = QtWidgets.QWidget() 
        self.env            = None
        self.mask_interface = mask_interface

        self._setup()
        self._connect()
        self.fadeActivity()

        self.elements       = []
        self.meta_elements  = []
        
    def _setup(self):
        '''
        This is the initial setup method that will 
        build the layout and introduce the graphics
        area.
        '''
        self.setupUi(self.local_widget)
        self._setEditors()

        self.process_box_mask_fit = self.mask_interface.getComboBox()
        self.fit_select_layout.addWidget(self.process_box_mask_fit)

        self.process_box_masks = self.mask_interface.getComboBox(connect = False)
        self.phase_mask_layout.addWidget(self.process_box_masks)

        self.text_widgets = [
            self.script_text_import,
            self.script_text_set_fit,
            self.script_text_phase,
            self.script_text_reduction,
            self.script_text_post]

        self.button_widgets = [
            self.script_button_import_run,
            self.script_button_set_fit_run,
            self.script_button_phase_run,
            self.script_button_reduction_run,
            self.script_button_post_run,

            self.process_button_run_data,
            self.process_button_run_phase,
            self.process_button_run_fit,
            self.process_button_run_post,            
            
            None,
            None,
            None,
            None,
            
            self.script_button_import_gui,
            self.script_button_phase_gui,
            self.script_button_reduction_gui]

        self.tool = PanelPageMaskWidget(self, self.parent, self.mask_interface)
        self.tool.local_widget.setStyleSheet(
            "#mask_editor{background:transparent;}")
        self.panel_layout.addWidget(self.tool.local_widget)

        with open(os.path.realpath(os.path.sep.join(str(os.path.realpath(__file__)).split(os.path.sep)[0:-4] + ['ressources', 'default_post_path.txt'])),'r') as f:
            self.path = f.readline()
            self.script_line_def_save.setText(self.path)

    def _setEditors(self):
        '''
        locally create the editors to allow custom ones. These parts
        have been engineered through the pyqt framework and then 
        exported through the pyuic5 routine. Note that here we are
        simply selecting parts of it and changing the intput text editor
        '''

        self.script_tabs = QtWidgets.QTabWidget(self.script_tab)
        self.script_tabs.setStyleSheet("")
        self.script_tabs.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.script_tabs.setObjectName("script_tabs")
        self.verticalLayout_8.addWidget(self.script_tabs)

        # for script_text_import
        self.script_tab_import = QtWidgets.QWidget()
        self.script_tab_import.setObjectName("script_tab_import")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.script_tab_import)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.script_text_import = CodeEditor(self.script_tab_import)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.script_text_import.sizePolicy().hasHeightForWidth())
        self.script_text_import.setSizePolicy(sizePolicy)
        self.script_text_import.setObjectName("script_text_import")
        self.verticalLayout_2.addWidget(self.script_text_import)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.import_gui_reset = QtWidgets.QPushButton(
            'Reset', self.script_tab_import)
        self.import_gui_reset.setObjectName("import_gui_reset")
        self.horizontalLayout_2.addWidget(self.import_gui_reset)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.script_button_import_gui = QtWidgets.QPushButton('GUI', self.script_tab_import)
        self.script_button_import_gui.setObjectName("script_button_import_gui")
        self.horizontalLayout_2.addWidget(self.script_button_import_gui)
        self.script_button_import_run = QtWidgets.QPushButton('Run', self.script_tab_import)
        self.script_button_import_run.setDefault(True)
        self.script_button_import_run.setObjectName("script_button_import_run")
        self.horizontalLayout_2.addWidget(self.script_button_import_run)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.script_tabs.addTab(self.script_tab_import, "Import")

        # for script_text_set_fit
        self.script_tab_set_fit = QtWidgets.QWidget()
        self.script_tab_set_fit.setObjectName("script_tab_set_fit")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.script_tab_set_fit)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.script_text_set_fit = CodeEditor(self.script_tab_set_fit)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.script_text_set_fit.sizePolicy().hasHeightForWidth())
        self.script_text_set_fit.setSizePolicy(sizePolicy)
        self.script_text_set_fit.setObjectName("script_text_set_fit")
        self.verticalLayout_20.addWidget(self.script_text_set_fit)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.set_fit_gui_reset = QtWidgets.QPushButton(
            'Reset', self.script_tab_set_fit)
        self.set_fit_gui_reset.setObjectName("set_fit_gui_reset")
        self.horizontalLayout_3.addWidget(self.set_fit_gui_reset)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.script_button_set_fit_gui = QtWidgets.QPushButton('GUI', self.script_tab_set_fit)
        self.script_button_set_fit_gui.setObjectName("script_button_set_fit_gui")
        self.horizontalLayout_3.addWidget(self.script_button_set_fit_gui)
        self.script_button_set_fit_run = QtWidgets.QPushButton('Run', self.script_tab_set_fit)
        self.script_button_set_fit_run.setDefault(True)
        self.script_button_set_fit_run.setObjectName("script_button_set_fit_run")
        self.horizontalLayout_3.addWidget(self.script_button_set_fit_run)
        self.verticalLayout_20.addLayout(self.horizontalLayout_3)
        self.script_tabs.addTab(self.script_tab_set_fit, "Fit parameters")

        # for script_text_phase
        self.script_tab_phase = QtWidgets.QWidget()
        self.script_tab_phase.setObjectName("script_tab_phase")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.script_tab_phase)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.script_text_phase = CodeEditor(self.script_tab_phase)
        self.script_text_phase.setObjectName("script_text_phase")
        self.verticalLayout_3.addWidget(self.script_text_phase)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.phase_gui_reset = QtWidgets.QPushButton(
            'Reset', self.script_tab_phase)
        self.phase_gui_reset.setObjectName("phase_gui_reset")
        self.horizontalLayout_5.addWidget(self.phase_gui_reset)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem8)
        self.script_button_phase_gui = QtWidgets.QPushButton('GUI', self.script_tab_phase)
        self.script_button_phase_gui.setObjectName("script_button_phase_gui")
        self.horizontalLayout_5.addWidget(self.script_button_phase_gui)
        self.script_button_phase_run = QtWidgets.QPushButton('Run',self.script_tab_phase)
        self.script_button_phase_run.setDefault(True)
        self.script_button_phase_run.setObjectName("script_button_phase_run")
        self.horizontalLayout_5.addWidget(self.script_button_phase_run)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.script_tabs.addTab(self.script_tab_phase, "Phase correction")

        # for script_text_reduction
        self.script_tab_reduction = QtWidgets.QWidget()
        self.script_tab_reduction.setObjectName("script_tab_reduction")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.script_tab_reduction)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.script_text_reduction = CodeEditor(self.script_tab_reduction)
        self.script_text_reduction.setObjectName("script_text_reduction")
        self.verticalLayout_4.addWidget(self.script_text_reduction)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.reduction_gui_reset = QtWidgets.QPushButton(
            'Reset', self.script_tab_reduction)
        self.reduction_gui_reset.setObjectName("reduction_gui_reset")
        self.horizontalLayout_6.addWidget(self.reduction_gui_reset)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem9)
        self.script_button_reduction_gui = QtWidgets.QPushButton('GUI', self.script_tab_reduction)
        self.script_button_reduction_gui.setObjectName("script_button_reduction_gui")
        self.horizontalLayout_6.addWidget(self.script_button_reduction_gui)
        self.script_button_reduction_run = QtWidgets.QPushButton('Run', self.script_tab_reduction)
        self.script_button_reduction_run.setDefault(True)
        self.script_button_reduction_run.setObjectName("script_button_reduction_run")
        self.horizontalLayout_6.addWidget(self.script_button_reduction_run)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.script_tabs.addTab(self.script_tab_reduction, "Reduction")

        # for script_text_post
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.script_text_post = CodeEditor(self.tab)
        self.script_text_post.setObjectName("script_text_post")
        self.verticalLayout_8.addWidget(self.script_text_post)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.script_line_def_save = QtWidgets.QLineEdit(self.tab)
        self.script_line_def_save.setObjectName("script_line_def_save")
        self.horizontalLayout_7.addWidget(self.script_line_def_save)
        self.script_save_def_save = QtWidgets.QPushButton('...',self.tab)
        self.script_save_def_save.setObjectName("script_save_def_save")
        self.horizontalLayout_7.addWidget(self.script_save_def_save)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem10)
        self.script_button_post_run = QtWidgets.QPushButton('Run',self.tab)
        self.script_button_post_run.setDefault(True)
        self.script_button_post_run.setObjectName("script_button_post_run")
        self.horizontalLayout_7.addWidget(self.script_button_post_run)
        self.verticalLayout_8.addLayout(self.horizontalLayout_7)
        self.script_tabs.addTab(self.tab, "Post-reduction")

    def _connect(self):
        '''
        Connect all Qt slots to their respective methods.
        '''
        self.button_widgets[0].clicked.connect(partial(self.run,0))
        self.button_widgets[2].clicked.connect(partial(self.run,0))
        self.button_widgets[2].clicked.connect(partial(self.run,1))
        self.button_widgets[3].clicked.connect(partial(self.run,2))
        self.button_widgets[4].clicked.connect(partial(self.run,3))

        self.button_widgets[5].clicked.connect(partial(self.run,0))
        self.button_widgets[6].clicked.connect(partial(self.run,1))
        self.button_widgets[7].clicked.connect(partial(self.run,2))
        self.button_widgets[8].clicked.connect(partial(self.run,3))

        self.button_widgets[13].clicked.connect(
            partial(self.link, None))
        self.button_widgets[14].clicked.connect(
            partial(self.link, None))
        self.button_widgets[15].clicked.connect(
            partial(self.link, None))

        self.text_widgets[0].textChanged.connect(
            partial(self._updateEditable, 0))
        self.text_widgets[1].textChanged.connect(
            partial(self._updateEditable, 1))
        self.text_widgets[2].textChanged.connect(
            partial(self._updateEditable, 2))
        self.text_widgets[3].textChanged.connect(
            partial(self._updateEditable, 3))
        self.text_widgets[4].textChanged.connect(
            partial(self._updateEditable, 4))
        
        self.script_save_def_save.clicked.connect(
            self._setNewDefaultSavePath)

        self.import_gui_reset.clicked.connect(
            partial(self._resetScript, 0))
        self.set_fit_gui_reset.clicked.connect(
            partial(self._resetScript, 1))
        self.phase_gui_reset.clicked.connect(
            partial(self._resetScript, 2))
        self.reduction_gui_reset.clicked.connect(
            partial(self._resetScript, 3))

        self.process_button_foils.clicked.connect(self._openFoilView)

    def _resetScript(self, idx):
        '''
        Reset a script given by his index 
        value as integer.

        Parameters
        ----------
        idx : int
            The index of the script to reset
        '''
        self.env.scripts.resetScript(idx)
        self._synthesize()

    def _openFoilView(self):
        '''
        This routine will launch the metadat window.
        '''
        self.env.instrument.setDetector(
            self.process_box_detector.currentText(), 
            self.process_box_detector.currentText())

        self.parent.window_manager.newWindow('FoilVisual')
        self.parent.window_manager.active_windows['FoilVisual'].target.link(self.env.instrument)

    def _setNewDefaultSavePath(self):
        '''
        When the button is clicked a new file
        dialogue will be open to set the new 
        file.
        '''
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(
            self.parent.window, 
            'Select folder')

        with open(os.path.sep.join(str(os.path.realpath(__file__)).split(os.path.sep)[0:-3] + ['ressources', 'default_post_path.txt']),'w') as f:
            f.writelines([dir_path])
            self.path = dir_path
            self.script_line_def_save.setText(dir_path)

    def link(self, env = None):
        '''
        Link the GUI to the environment that will be  read and
        taken care of.
        '''
        self.synthesize_scripts = False
        if not env == None:
            self.env = env
        self.tool.link(self.env.mask, self.env)
        self._refresh()
        self._linkVisualComponents()
        self.synthesize_scripts = True
        self.tabWidget.setCurrentIndex(0)
        self.script_tabs.setCurrentIndex(0)
        self.run(0)

    def unlink(self):
        '''
        To remove the item
        '''
        self.env = None

    def _linkVisualComponents(self):
        '''
        Once the link is done the system can inject the attributes
        into the selectors. This is manages through this dispatcher.
        '''
        self.synthesize_scripts     = False
        self._reset()

        self.container = self.env.scripts.readFromScripts()
        self._linkVisualInstrument()
        self._linkVisualDetector()
        self._linkVisualFit()
        
        self._setVisualFit()
        self._setVisualPhase()
        self._setVisualExposure()
        self._setVisualInstrument()
        self._setVisualDetector()

        self.foil_header_active     = True
        self.foil_elements_active   = True
        self.synthesize_scripts     = True
        
        self._connectVisualFit()
        self._connectVisualPhase()
        self._connectVisualInstrument()

        self._synthesize()

    def _reset(self):
        '''
        '''
        pass


    #######################################################################
    #######################################################################

    def _setVisualPhase(self):
        '''
        Set the widget values depending on the input of the 
        environnement
        '''
        if not self.container['phase_mask'] == None:
            try:
                self.process_box_masks.setCurrentIndex(
                    [key for key in self.env.mask.mask_dict.keys()].index(self.container['phase_mask']))
            except:
                pass

    def _connectVisualPhase(self):
        '''
        Connect all the elements after the value has been
        set in the set routine.
        '''
        self.process_box_masks.currentIndexChanged.connect(self._synthesizePhase)

    def _disconnectVisualPhase(self):
        '''
        Disconnect all the elements after the value has been
        set in the set routine.
        '''
        self.process_box_masks.currentIndexChanged.disconnect(self._synthesizePhase)

    #######################################################################
    #######################################################################
    def _linkVisualInstrument(self):
        '''
        Link the Instrument selection component
        '''
        self.process_box_instrument.clear()
        self.process_box_instrument.addItems(self.env.instrument.detector_names)

    def _linkVisualDetector(self, update = False):
        '''
        Link the detector selection component
        '''
        array = [ text[2] for text in self.env.instrument.detector.foil_file_list] + ['None']
        self.process_box_detector.clear()
        self.process_box_detector.addItems(array)
        if update:
            self._setVisualDetector()

    def _setVisualExposure(self):
        '''
        Link the exposure selection component
        '''
        if self.container['exposure']:
            self.process_radio_exposure.setChecked(True)
            self.process_radio_mask.setChecked(False)
        else:
            self.process_radio_exposure.setChecked(False)
            self.process_radio_mask.setChecked(True)

    def _setVisualInstrument(self):
        '''
        Set the widget values depending on the input of the 
        environnement
        '''
        try:
            self.process_box_instrument.setCurrentIndex(
                self.env.instrument.detector_names.index(self.container['instrument']))
        except:
            pass

    def _setVisualDetector(self):
        '''
        Set the widget values depending on the input of the 
        environnement
        '''
        array = [text[0] for text in self.env.instrument.detector.foil_file_list] + ['None']
        try:
            self.process_box_detector.setCurrentIndex(
                array.index(self.container['detector']))
        except:
            pass

    def _connectVisualInstrument(self):
        '''
        Connect all the elements after the value has been
        set in the set routine.
        '''
        self.process_box_instrument.currentIndexChanged.connect(self._processInstrument)
        self.process_box_detector.currentIndexChanged.connect(self._processInstrument)
        self.process_radio_exposure.toggled.connect(self._processInstrument)

    def _disconnectVisualInstrument(self):
        '''
        Disconnect all the elements after the value has been
        set in the set routine.
        '''
        self.process_box_instrument.currentIndexChanged.disconnect(self._processInstrument)
        self.process_box_detector.currentIndexChanged.disconnect(self._processInstrument)
        self.process_radio_exposure.toggled.disconnect(self._processInstrument)

    def _processInstrument(self):
        '''
        The instrument is more complex and needs to be managed 
        through an intermediate routine here
        '''
        self._disconnectVisualInstrument()

        new     = self.process_box_instrument.currentText()
        array   = [text[0] for text in self.env.instrument.detector.foil_file_list] + ['None']
        element = array[self.process_box_detector.currentIndex()]

        self.env.instrument.setDetector(
            new, None if element == 'None' else int(element))

        self._linkVisualDetector()
        self._setVisualInstrument()
        self._setVisualDetector()
        self._synthesizeFit()
        self._connectVisualInstrument()

    #######################################################################
    #######################################################################

    def _linkVisualFit(self):
        '''
        Link the fit parameters component
        '''
        self._buildEchoFoils()
        self._buildSelectedItems()
        self._buildTimeChannelItems()
        self._linkVisualBackground()
        self._linkVisualReference()

    def _linkVisualBackground(self):
        '''
        Link the fit parameters component
        '''
        array = [ str(val) for val in self.env.current_data.get_axis('Parameter') ]+['None']
        self.process_box_back_fit.clear()
        self.process_box_back_fit.addItems(array)

    def _linkVisualReference(self):
        '''
        Link the fit parameters component
        '''
        array = [ str(val) for val in self.env.current_data.get_axis('Parameter') ]
        self.process_box_refs_fit.clear()
        self.process_box_refs_fit.addItems(array)

    def _setVisualFit(self):   
        '''
        Set the widget values depending on the input of the 
        environnement
        '''
        self._setVisualFitDrops()
        self._setVisualFitSelected()
        self._setVisualFitFoilsInEcho()

    def _setVisualFitDrops(self):   
        '''
        Set the widget values depending on the input of the 
        environnement
        '''
        #Reduction mask
        if not self.container['reduction_mask'] == None:
            try:
                self.process_box_mask_fit.setCurrentIndex(
                    [ key for key in self.env.mask.mask_dict.keys() ].index(self.container['reduction_mask']))
            except:
                pass

        #Background field
        array = [ str(val) for val in self.env.current_data.get_axis('Parameter') ]+['None']
        if self.container['Background'] == None:
            self.process_box_back_fit.setCurrentIndex(array.index('None'))
        else:
            try:
                self.process_box_back_fit.setCurrentIndex(
                    array.index(str(self.container['Background'])))
            except:
                pass

        #Reference field
        array = [ str(val) for val in self.env.current_data.get_axis('Parameter') ]
        if self.container['Reference'] == None:
            try:
                self.process_box_refs_fit.setCurrentIndex(
                    array.index(self.env.current_data.metadata_class['Reference']))
            except:
                pass
        else:
            try:
                self.process_box_refs_fit.setCurrentIndex(
                    array.index(str(list(self.container['Reference'])[0])))
            except:
                pass
        
    def _setVisualFitSelected(self):   
        '''
        Set the widget values depending on the input of the 
        environnement
        '''
        if not self.container['Selected'] == None:
            for item in self.selected_items:
                checked = QtCore.Qt.Checked if str(item.text()) in [str(element) for element in self.container['Selected']] else QtCore.Qt.Unchecked
                item.setCheckState(checked)

    def _setVisualTimeChannel(self):   
        '''
        Set the widget values depending on the input of the 
        environnement
        '''
        if not self.container['time_channels'] == None:
            for i, item in enumerate(self.selected_items):
                checked = QtCore.Qt.Checked if i in self.container['time_channels'] else QtCore.Qt.Unchecked
                item.setCheckState(checked)

    def _setVisualFitFoilsInEcho(self):   
        '''
        Set the widget values depending on the input of the 
        environnement
        '''
        for i, foil_select in enumerate(self.container['foils_in_echo']):
            for j, element in enumerate(foil_select):
                try:
                    self._foil_model.item(i+1,j).setCheckState(QtCore.Qt.Checked if element == 1 else QtCore.Qt.Unchecked)
                except:
                    pass

        for i in range(self.env.current_data.get_axis_len('Foil')):
            self._foil_model.item(0, i).setCheckState(self._allInCol(i))

    def _connectVisualFit(self):   
        '''
        Connect all the elements after the value has been
        set in the set routine.
        '''
        self.process_box_back_fit.currentIndexChanged.connect(self._synthesizeFit)
        self.process_box_refs_fit.currentIndexChanged.connect(self._synthesizeFit)
        self.mask_interface.mask_updated.connect(self._synthesizeReduction)

    def _disconnectVisualFit(self):   
        '''
        Disconnect all the elements after the value has been
        set in the set routine.
        '''
        self.process_box_back_fit.currentIndexChanged.disconnect(self._synthesizeFit)
        self.process_box_refs_fit.currentIndexChanged.disconnect(self._synthesizeFit)
        self.mask_interface.mask_updated.disconnect(self._synthesizeReduction)

    #######################################################################
    #######################################################################
            
    def _buildSelectedItems(self):
        '''
        Build the list that will contain the standart 
        items of the measurements selected.
        '''
        self.selected_model = QtGui.QStandardItemModel()
        self.selected_model.itemChanged.connect(self._synthesize)
        self.selected_items = []

        for i in range(self.env.current_data.get_axis_len('Parameter')):
            self._addSelectedItem(
                str(self.env.current_data.get_axis('Parameter')[i]))

        self.process_list_selected.setModel(self.selected_model)

    def _addSelectedItem(self,name, check = True):
        '''
        Add an echo type widget to the widget view
        '''
        self.selected_items.append(QtGui.QStandardItem(name))
        checked = QtCore.Qt.Checked if check else QtCore.Qt.Unchecked
        self.selected_items[-1].setCheckState(checked)
        self.selected_items[-1].setCheckable(True)
        self.selected_model.appendRow(self.selected_items[-1])

    def _buildTimeChannelItems(self):
        '''
        Build the list that will contain the standart 
        items of the measurements selected.
        '''
        self.time_channel_model = QtGui.QStandardItemModel()
        self.time_channel_model.itemChanged.connect(self._synthesize)
        self.time_channel_items = []
        
        for i in range(self.env.current_data.get_axis_len('Time Channel')):
            self._addTimeChannelItem(str(i))

        self.time_channel_selected.setModel(self.time_channel_model)

    def _addTimeChannelItem(self,name, check = True):
        '''
        Add an echo type widget to the widget view
        '''
        self.time_channel_items.append(QtGui.QStandardItem(name))
        checked = QtCore.Qt.Checked if check else QtCore.Qt.Unchecked
        self.time_channel_items[-1].setCheckState(checked)
        self.time_channel_items[-1].setCheckable(True)
        self.time_channel_model.appendRow(self.time_channel_items[-1])

    def _buildEchoFoils(self):
        '''
        Build the tiny widgets for the widget list containing
        all the foils that will or will not be active at
        different echo times.
        '''
        num_foils = self.env.current_data.get_axis_len('Foil')
        self._foil_model = QtGui.QStandardItemModel()
        self._foil_delegate = FoilDelegate()

        try:
            self.names = ['{:0.5e}'.format(x) for x in self.env.current_data.get_axis('Echo Time').sort()]
        except:
            self.names = ['{:0.5e}'.format(x) for x in self.env.current_data.get_axis('Echo Time')]

        for j in range(num_foils):
            item = QtGui.QStandardItem()
            item.setCheckable(True)
            item.setEditable(False)
            self._foil_model.setItem(0,j,item)

        for i in range(len(self.names)):
            for j in range(num_foils):
                item = QtGui.QStandardItem()
                item.setCheckable(True)
                item.setEditable(False)
                self._foil_model.setItem(i+1,j,item)

        self.process_list_echo_times.setModel(self._foil_model)
        self.process_list_echo_times.setItemDelegate(self._foil_delegate)
        self._foil_model.setVerticalHeaderLabels(['All']+self.names)
        self._foil_model.setHorizontalHeaderLabels([ 
            str(val) for val in self.env.current_data.get_axis('Foil') ])
        for j in range(num_foils):
            self.process_list_echo_times.resizeColumnsToContents()
        
        self.process_list_echo_times.clicked.connect(self._updateFoil)

    def _updateFoil(self, index):
        '''
        The first row in are tristate checkboxes who need to
        be set depending on the state of the column
        '''
        item = self._foil_model.item(index.row(), index.column())

        if index.row() == 0:
            self._setFoilCol(index.column(), item.checkState())
        else:
            self._foil_model.item(0, index.column()).setCheckState(self._allInCol(index.column()))

        self._synthesizeFit()

    def _allInCol(self, col):
        '''
        check if the elements in a colum are either
        all selected or all unselected
        '''
        selected = []
        for i in range(len(self.names)):
            selected.append(self._foil_model.item(i+1, col).checkState() == QtCore.Qt.Checked)

        if all(selected):
            return QtCore.Qt.Checked
        elif not any(selected):
            return QtCore.Qt.Unchecked
        else:
            return QtCore.Qt.PartiallyChecked


    def _setFoilCol(self, col, state):
        '''
        set the state of the element in a column
        '''
        for i in range(len(self.names)):
            self._foil_model.item(i+1, col).setCheckState(state)


    #######################################################################
    #######################################################################

    def _synthesize(self):
        '''
        run synthesis scripts
        '''
        if not self.synthesize_scripts:
            return None

        self._synthesizeFit()
        self._synthesizePhase()
        self._synthesizeReduction()

    def _synthesizeFit(self):
        '''
        This function will build the container for the
        script structure to rewrite the script. This
        was separated into reading the GUI here and 
        writing the script in the script structure.
        '''
        container = {}

        #get the foils
        foils_in_echo = []
        echo_len = self.env.current_data.get_axis_len('Echo Time')
        foil_len = self.env.current_data.get_axis_len('Foil')
        for i in range(echo_len):
            items = []
            for j in range(foil_len): 
                if self._foil_model.item(i+1,j).checkState() == QtCore.Qt.Checked:
                    items.append(1)
                else:
                    items.append(0)
            foils_in_echo.append(items)    
        container['foils_in_echo'] = foils_in_echo

        #get selected
        selected = []
        for i, item in enumerate(self.selected_items):
            if item.checkState() == QtCore.Qt.Checked:
                selected.append(self.env.current_data.get_axis('Parameter')[i])
        try:
            container['selected'] = sorted(selected)
        except:
            container['selected'] = selected

        #get the background
        array = [ str(val) for val in self.env.current_data.get_axis('Parameter') ]
        if self.process_box_back_fit.currentIndex() == len(array):
            container['Background'] = "None"
        else:
            try:
                container['Background'] = str(float(array[self.process_box_back_fit.currentIndex()]))
            except:
               container['Background'] = "'"+str(array[self.process_box_back_fit.currentIndex()])+"'"

        #get the reference
        array = [ str(val) for val in self.env.current_data.get_axis('Parameter') ]
        try:
            container['Reference'] = "["+str(float(array[self.process_box_refs_fit.currentIndex()]))+",0]"
        except:
            container['Reference'] = "['"+str(array[self.process_box_refs_fit.currentIndex()])+"',0]"

        #get the Instrument
        container['Instrument'] = str(self.process_box_instrument.currentText())

        #get the detector
        array = [ text[0] for text in self.env.instrument.detector.foil_file_list] + ['None']
        container['Detector'] = str(array[self.process_box_detector.currentIndex()])

        #get the exposure
        container['exposure'] = str(self.process_radio_exposure.isChecked())

        time_channels = []
        for i, item in enumerate(self.time_channel_items):
            if item.checkState() == QtCore.Qt.Checked:
                time_channels.append(int(i))
        container['time_channels'] = sorted(time_channels)

        self.env.scripts.synthesizeFitScript(container)
        self._refresh()

    def _synthesizePhase(self):
        '''
        prepare the python script part that will
        manage the data parameter part
        '''
        container = {}
        container['mask'] = str([ key for key in self.env.mask.mask_dict.keys() ][self.process_box_masks.currentIndex()])

        #find strings
        self.env.scripts.synthesizePhaseScript(container)
        self._refresh()

    def _synthesizeReduction(self):
        '''
        prepare the python script part that will
        manage the data parameter part
        '''
        container = {}
        container['mask'] = str(self.process_box_mask_fit.currentText())

        #find strings
        self.env.scripts.synthesizeReductionScript(container)
        self._refresh()

    #######################################################################
    #######################################################################

    def _refresh(self):
        '''
        Refresh the text present in the code editors
        with the source present in the core env.process 
        class. 
        '''        
        self.text_widgets[0].setPlainText(self.env.scripts.editable_scripts[0])
        self.text_widgets[1].setPlainText(self.env.scripts.editable_scripts[1])
        self.text_widgets[2].setPlainText(self.env.scripts.editable_scripts[2])
        self.text_widgets[3].setPlainText(self.env.scripts.editable_scripts[3])
        self.text_widgets[4].setPlainText(self.env.scripts.editable_scripts[4])

    def _updateAllEditable(self):

        if not self.env == None:
            for i in range(5):
                try:
                    self.env.scripts.setEditable(i, self.text_widgets[i].toPlainText())
                except Exception as e:
                    dialog(
                        parent = self.local_widget,
                        icon = 'error', 
                        title= 'Could not update script',
                        message = 'The core encountered an error',
                        add_message = str(e),
                        det_message = traceback.format_exc())

    def _updateEditable(self, index):
        if not self.env == None:
            try:
                self.env.scripts.setEditable(index, self.text_widgets[index].toPlainText())
            except Exception as e:
                dialog(
                    parent = self.local_widget,
                    icon = 'error', 
                    title= 'Could not update script',
                    message = 'The core encountered an error',
                    add_message = str(e),
                    det_message = traceback.format_exc())

    def show(self, index):
        '''
        This is the run method that will determine the measure
        to undertake. 
        '''
        self.tabWidget.setCurrentIndex(2)
        self.script_tabs.setCurrentIndex(index)
        
    def run(self, index):
        '''
        This is the run method that will determine the measure
        to undertake. 
        '''
        if not self.env == None:
            mask_to_reset = self.env.mask.current_mask
            if index < 5:
                if index == 0:
                    self._runPythonCode(index)
                    self._runPythonCode(index+1)
                else:
                    self._runPythonCode(index+1)
            self.env.mask.setMask(mask_to_reset)
            # self.mask_interface.setModel()

    def runAll(self):
        '''
        Run all the scripts.
        '''
        for i in range(4):
            self.run(i)

    def _runPythonCode(self, index):
        '''
        Parse and run python code. 
        '''
        self._updateEditable(index)
        code_array, meta_array = self.env.scripts.preprocessScript(index)

        self.script_label_running.setText('Script running')
        self.scrip_label_action.setText('Command:')
        self.setActivity(0, len(meta_array))
        success = True

        for i in range(len(code_array)):
            self.setProgress(meta_array[i].strip('\n'), i)
            try:
                exec(code_array[i])
            except Exception as e:
                error = e
                dialog(
                    parent = self.local_widget,
                    icon = 'error', 
                    title= 'Script error',
                    message = 'Your script has encountered an error.',
                    add_message = str(e),
                    det_message = traceback.format_exc())
                success = False
                break
        if success:
            self.setProgress('Script ended with success', len(meta_array))
            self.fadeActivity()

        else:
            self.script_label_running.setText('Aborted')
            self.scrip_label_action.setText('Error: ')
            self.setProgress(str(error), i)

    def saveScripts(self):
        '''
        This method as the name indicates is in charge of
        prompting the user for a savefile name and location 
        through a QFileDialog and then saves the file as
        a script.
        '''
        filters = "mieze_script_save.py"

        # file_path = QtWidgets.QFileDialog.getSaveFileName(
        #         self.window, 
        #         'Select file',
        #         filters)[0]
        # self._updateAllEditable()
        # self.env.scripts.saveScripts(file_path)

    def loadScripts(self):
        '''
        This method will load the string from file through 
        a QFileDialog. Specify a file formated in the right
        way or saved through miezepy.
        '''
        filters = "*.py"

        # file_path = QtWidgets.QFileDialog.getOpenFileName(
        #         self.window, 
        #         'Select file',
        #         filters)[0]

        # self.env.scripts.loadScripts(file_path)
        # self.refresh()

    def setActivity(self, min_val, max_val):
        '''

        '''
        #make it visible in case it was hidden
        self.script_label_running.show()
        self.script_bar_running.show()
        self.scrip_label_action.show()
        self.script_label_action_2.show()

        #in case it was faded
        self._unfade(self.script_label_running)
        self._unfade(self.script_bar_running)
        self._unfade(self.scrip_label_action)
        self._unfade(self.script_label_action_2)

        self.script_bar_running.setMinimum(min_val)
        self.script_bar_running.setMaximum(max_val)

    def hideActivity(self):
        '''

        '''
        self.script_label_running.hide()
        self.script_bar_running.hide()
        self.scrip_label_action.hide()
        self.script_label_action_2.hide()

    def fadeActivity(self):
        '''

        '''
        self._fade(self.script_label_running)
        self._fade(self.script_bar_running)
        self._fade(self.scrip_label_action)
        self._fade(self.script_label_action_2)

    def _unfade(self, widget):
        '''


        '''
        effect = QtWidgets.QGraphicsOpacityEffect()
        effect.setOpacity(1)
        widget.setGraphicsEffect(effect)

    def _fade(self, widget):
        '''

        '''
        widget.effect = QtWidgets.QGraphicsOpacityEffect()
        widget.setGraphicsEffect(widget.effect)

        widget.animation = QtCore.QPropertyAnimation(widget.effect, b"opacity")
        widget.animation.setDuration(1000)
        widget.animation.setStartValue(1)
        widget.animation.setEndValue(0)
        widget.animation.start()

    def setProgress(self, label, val):
        '''

        '''
        self.script_bar_running.setValue(val)
        self.script_label_action_2.setText(label)
        self.parent.window_manager.app.processEvents()
