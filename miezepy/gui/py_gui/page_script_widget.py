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

#private dependencies
from ..qt_gui.main_script_ui        import Ui_script_widget
from ...gui.py_gui.python_syntax    import PythonHighlighter
from ...gui.py_gui.page_mask_widget import PageMaskWidget
from ...gui.py_gui.dialog           import dialog 

class PageScriptWidget(Ui_script_widget):
    
    def __init__(self, stack, parent):
        
        Ui_script_widget.__init__(self)
        self.parent         = parent
        self.stack          = stack
        self.local_widget   = QtWidgets.QWidget() 
        self.env            = None

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

        self.text_widgets = [
            self.script_text_import,
            self.script_text_phase,
            self.script_text_reduction,
            self.script_text_post]

        self.button_widgets = [
            self.script_button_import_run,
            self.script_button_phase_run,
            None,
            self.script_button_reduction_run,
            self.script_button_post_run,

            self.process_button_run_data,
            self.process_button_run_phase,
            self.process_button_run_fit,
            self.process_button_run_post,            
            
            self.process_button_script_data,
            self.process_button_script_phase,
            self.process_button_script_fit,
            self.process_button_script_post,
            
            self.script_button_import_gui,
            self.script_button_phase_gui,
            self.script_button_reduction_gui]

        self.syntaxHighliter_0 = PythonHighlighter(
            self.text_widgets[0].document())
        self.syntaxHighliter_1 = PythonHighlighter(
            self.text_widgets[1].document())
        self.syntaxHighliter_2 = PythonHighlighter(
            self.text_widgets[2].document())
        self.syntaxHighliter_3 = PythonHighlighter(
            self.text_widgets[3].document())

        self.tool = PageMaskWidget(self, self.parent)
        self.tool.local_widget.setStyleSheet(
            "#mask_editor{background:transparent;}")
        self.panel_layout.addWidget(self.tool.local_widget)

        #inject the parameter widget
        self.para_group = QtWidgets.QGroupBox(self.panel_tab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, 
            QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.para_group.setSizePolicy(sizePolicy)
        self.para_group.setMinimumSize(QtCore.QSize(425, 0))
        self.para_group.setMaximumSize(QtCore.QSize(425, 16777215))
        self.para_group.setBaseSize(QtCore.QSize(425, 200))
        self.para_group.setObjectName("para_group")
        self.tool.mask_layout_control.addWidget(self.para_group)

    def _connect(self):
        '''
        Connect all Qt slots to their respective methods.
        '''
        self.button_widgets[0].clicked.connect(partial(self.run,0))
        self.button_widgets[1].clicked.connect(partial(self.run,1))
        self.button_widgets[3].clicked.connect(partial(self.run,2))
        self.button_widgets[4].clicked.connect(partial(self.run,3))

        self.button_widgets[5].clicked.connect(partial(self.run,0))
        self.button_widgets[6].clicked.connect(partial(self.run,1))
        self.button_widgets[7].clicked.connect(partial(self.run,2))
        self.button_widgets[8].clicked.connect(partial(self.run,3))

        self.button_widgets[9].clicked.connect(partial(self.show,0))
        self.button_widgets[10].clicked.connect(partial(self.show,1))
        self.button_widgets[11].clicked.connect(partial(self.show,2))
        self.button_widgets[12].clicked.connect(partial(self.show,3))

        self.button_widgets[13].clicked.connect(partial(self.link, None))
        self.button_widgets[14].clicked.connect(partial(self.link, None))
        self.button_widgets[15].clicked.connect(partial(self.link, None))

        self.text_widgets[0].textChanged.connect(partial(self._updateEditable, 0))
        self.text_widgets[1].textChanged.connect(partial(self._updateEditable, 1))
        self.text_widgets[2].textChanged.connect(partial(self._updateEditable, 2))
        self.text_widgets[3].textChanged.connect(partial(self._updateEditable, 3))

    def link(self, env = None):
        '''
        Link the GUI to the environment that will be  read and
        taken care of.
        '''
        if not env == None:
            self.env = env

        self.tool.link(self.env.mask)
        self.populatePara()
        self._refresh()
        self._linkVisualComponents()

    def _linkVisualComponents(self):
        '''
        Once the link is done the system can inject the attributes
        into the selectors. This is manages through this dispatcher.
        '''
        self.synthesize_scripts     = False

        self._readFromScripts()
        self._linkVisualData()
        self._linkVisualPhase()
        self._linkVisualFit()

        self._setVisualData()
        self._updateFoilEnabled()
        self._setVisualFit()
        self._updateFoilTri()
        self._setVisualPhase()

        self.foil_header_active     = True
        self.foil_elements_active   = True
        self.synthesize_scripts     = True
        
        self._connectVisualData()
        self._connectVisualFit()
        self._connectVisualPhase()

        self._synthesize()

    def _readFromScripts(self):
        '''
        Read from the scripts to produce a dictionary
        with all the information that can be set if it
        is found.
        '''
        #----------------------------------------#
        text_array = self.env.process.editable_scripts[0].split("\n")

        #Foils to consider
        filtered_text_array = [
            element if "metadata_class.add_metadata('Selected foils'" in element 
            else '' 
            for element in text_array]
        foil_check = []
        for element in filtered_text_array:
            if not element == '':
                foil_check = eval('['+element.split('[')[1].split(']')[0]+']')

        #Foils to consider
        filtered_text_array = [
            element if "mask.setMask(" in element 
            else '' 
            for element in text_array]
        phase_mask = []
        for element in filtered_text_array:
            if not element == '':
                phase_mask = eval(element.split('(')[1].split(')')[0])

        #----------------------------------------#
        text_array = self.env.process.editable_scripts[1].split("\n")

        #Foils
        filtered_text_array = [
            element if 'foils_in_echo.append(' in element else '' 
            for element in text_array]
        foils_in_echo = []
        for element in filtered_text_array:
            if not element == '':
                exec(element.strip())
            
        #Selected
        filtered_text_array = [
            element if 'Selected = [' in element else '' 
            for element in text_array]
        Selected = []
        for element in filtered_text_array:
            if not element == '':
                Selected = eval(element.split('Selected =' )[1])

        #Reference
        filtered_text_array = [
            element if 'Reference = [' in element else '' 
            for element in text_array]
        Reference = None
        for element in filtered_text_array:
            if not element == '':
                Reference = eval(element.split('Reference = ' )[1])

        #Background
        filtered_text_array = [
            element if 'Background = ' in element else '' 
            for element in text_array]
        Background = None
        for element in filtered_text_array:
            if not element == '':
                Background = eval(element.split('Background = ' )[1])

        #----------------------------------------#
        text_array = self.env.process.editable_scripts[2].split("\n")

        #Foils to consider
        filtered_text_array = [
            element if "mask.setMask(" in element 
            else '' 
            for element in text_array]
        reduction_mask = []
        for element in filtered_text_array:
            if not element == '':
                reduction_mask = eval(element.split('(')[1].split(')')[0])

        self.container = {}
        self.container['foils_in_echo'] = foils_in_echo
        self.container['Selected']      = Selected
        self.container['Reference']     = Reference
        self.container['Background']    = Background
        self.container['foil_check']    = foil_check
        self.container['phase_mask']    = phase_mask
        self.container['reduction_mask']= reduction_mask

    #######################################################################
    #######################################################################
    def _linkVisualData(self):
        '''
        Create the widgets associated to the 
        present linked structure
        '''
        for i in reversed(range(self.process_layout_foil_check.count())): 
            self.process_layout_foil_check.itemAt(i).widget().deleteLater()

        self.foil_check = []
        for i in range(self.env.data[self.env.current_data_key.split('_reduced')[0]].get_axis_len('Foil')):
            self.foil_check.append(
                QtWidgets.QCheckBox(str(i),parent = self.local_widget))
            self.process_layout_foil_check.addWidget(self.foil_check[-1])

    def _setVisualData(self):
        '''
        Set the widget values depending on the input of the 
        environnement
        '''
        for i, checkbox in enumerate(self.foil_check):
            if self.container['foil_check'] == None:
                try:
                    checkbox.setChecked(bool(
                        self.env.data[self.env.current_data_key.split('_reduced')[0]].metadata_class['Selected foils'][i]))
                except:
                    pass
            else:
                try:
                    checkbox.setChecked(bool(self.container['foil_check'][i]))
                except:
                    pass   

    def _connectVisualData(self):
        '''
        Connect all the elements after the value has been
        set in the set routine.
        '''
        for i in range(self.env.data[self.env.current_data_key.split('_reduced')[0]].get_axis_len('Foil')):
            self.foil_check[i].stateChanged.connect(self._updateFoilEnabled)

    def _disconnectVisualData(self):
        '''
        Disconnect all the elements after the value has been
        set in the set routine.
        '''
        for i in range(self.env.data[self.env.current_data_key.split('_reduced')[0]].get_axis_len('Foil')):
            self.foil_check[i].stateChanged.disconnect(self._updateFoilEnabled)

    #######################################################################
    #######################################################################
    def _linkVisualPhase(self):
        '''
        Link the phase component
        '''
        self.process_box_masks.clear()
        self.process_box_masks.addItems(
            [ key for key in self.env.mask.mask_dict.keys() ])

        self.process_box_refs.clear()
        self.process_box_refs.addItems(
            [ str(val) for val in self.env.current_data.get_axis('Parameter') ])

    def _setVisualPhase(self):
        '''
        Set the widget values depending on the input of the 
        environnement
        '''
        if not self.container['phase_mask'] == None:
            try:
                self.process_box_masks.setCurrentIndex(
                    [ key for key in self.env.mask.mask_dict.keys() ].index(self.container['phase_mask']))
            except:
                pass

    def _connectVisualPhase(self):
        '''
        Connect all the elements after the value has been
        set in the set routine.
        '''
        self.process_box_masks.currentIndexChanged.connect(self._synthesizeData)

    def _disconnectVisualPhase(self):
        '''
        Disconnect all the elements after the value has been
        set in the set routine.
        '''
        self.process_box_masks.currentIndexChanged.disconnect(self._synthesizeData)

    #######################################################################
    #######################################################################

    def _linkVisualFit(self):
        '''
        Link the fit parameters component
        '''
        self._buildEchoFoils()
        self._buildSelectedItems()
        self._linkVisualMaskSelect()
        self._linkVisualBackground()
        self._linkVisualReference()
        self._updateFoilTri()

    def _linkVisualMaskSelect(self):
        '''
        Link the fit parameters component
        '''
        self.process_box_mask_fit.clear()
        self.process_box_mask_fit.addItems(
            [ key for key in self.env.mask.mask_dict.keys() ])

    def _linkVisualBackground(self):
        '''
        Link the fit parameters component
        '''
        array = [ str(val) for val in self.env.current_data.get_axis('Parameter') ]
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
        array = [ str(val) for val in self.env.current_data.get_axis('Parameter') ]
        if self.container['Background'] == None:
            try:
                self.process_box_back_fit.setCurrentIndex(
                    array.index(self.env.current_data.metadata_class['Background']))
            except:
                pass
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
        #Selected
        if not self.container['Selected'] == None:
            for i, item in enumerate(self.selected_items):
                checked = QtCore.Qt.Checked if str(item.text()) in [str(element) for element in self.container['Selected']] else QtCore.Qt.Unchecked
                item.setCheckState(checked)

    def _setVisualFitFoilsInEcho(self):   
        '''
        Set the widget values depending on the input of the 
        environnement
        '''
        #set the default values from script
        for idx, foil_select in enumerate(self.container['foils_in_echo']):
            l = 0
            for idx_2, element in enumerate(foil_select):
                if not self.grid_checkboxes[idx + 1][idx_2+ l].isEnabled():
                    found_enabled = False
                    while not found_enabled:
                        l += 1
                        if self.grid_checkboxes[idx + 1][idx_2+ l].isEnabled():
                            found_enabled = True
                try:
                    self.grid_checkboxes[idx + 1][idx_2 + l].setChecked(element == 1)
                except:
                    pass

    def _connectVisualFit(self):   
        '''
        Connect all the elements after the value has been
        set in the set routine.
        '''
        self.process_box_back_fit.currentIndexChanged.connect(self._synthesizeFit)
        self.process_box_refs_fit.currentIndexChanged.connect(self._synthesizeFit)
        self.process_box_mask_fit.currentIndexChanged.connect(self._synthesizeReduction)

        #link the boxes
        for check_row in self.grid_checkboxes:
            for checkbox in check_row:
                if not checkbox.isTristate():
                    checkbox.stateChanged.connect(self._updateFoilTri)

    def _disconnectVisualFit(self):   
        '''
        Disconnect all the elements after the value has been
        set in the set routine.
        '''
        self.process_box_back_fit.currentIndexChanged.disconnect(self._synthesizeFit)
        self.process_box_refs_fit.currentIndexChanged.disconnect(self._synthesizeFit)
        self.process_box_mask_fit.currentIndexChanged.disconnect(self._synthesizeReduction)
        
        #link the boxes
        for check_row in self.grid_checkboxes:
            for checkbox in check_row:
                if not checkbox.isTristate():
                    checkbox.stateChanged.disconnect(self._updateFoilTri)

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

    def _buildEchoFoils(self):
        '''
        Build the tiny widgets for the widget list containing
        all the foils that will or will not be active at
        different echo times.
        '''
        self.echo_foil_widgets = []
        self.grid_checkboxes   = []
        self.echo_widgets      = []
        self.process_list_echo_times.clear()

        #create the elements
        self._addEchoWidget('All times', tri = True)
        for element in self.grid_checkboxes[0]:
            element.stateChanged.connect(self._updateFoilCol)

        for i in range(self.env.data[self.env.current_data_key.split('_reduced')[0]].get_axis_len('Echo Time')):
            self._addEchoWidget(str(self.env.data[self.env.current_data_key.split('_reduced')[0]].get_axis('Echo Time')[i])[0:8])
        self._updateFoilEnabled(synthesize = False)
        
    def _addEchoWidget(self,name, tri = False):
        '''
        Add an echo type widget to the widget view
        '''
        self.echo_foil_widgets.append(
            QtWidgets.QWidget(parent = self.local_widget))
        layout      = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        label       = QtWidgets.QLabel(name,parent = self.echo_foil_widgets[-1])
        sizePolicy  = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, 
            QtWidgets.QSizePolicy.Expanding)
        label.setSizePolicy(sizePolicy)
        label.setMinimumSize(QtCore.QSize(50, 0))
        label.setMaximumSize(QtCore.QSize(100, 16777215))
        label.setBaseSize(QtCore.QSize(50, 0))
        label.setAlignment(
            QtCore.Qt.AlignLeading|
            QtCore.Qt.AlignHCenter|
            QtCore.Qt.AlignVCenter)
        layout.addWidget(label)

        checkboxes = []

        for i in range(self.env.data[self.env.current_data_key.split('_reduced')[0]].get_axis_len('Foil')):
            checkboxes.append(QtWidgets.QCheckBox(
                str(i),parent = self.local_widget))
            checkboxes[-1].setTristate(tri)
            layout.addWidget(checkboxes[-1])
        self.grid_checkboxes.append(checkboxes)
        self.echo_foil_widgets[-1].setLayout(layout)
        self.echo_widgets.append(
            QtWidgets.QListWidgetItem(self.process_list_echo_times))
        self.echo_widgets[-1].setSizeHint(self.echo_foil_widgets[-1].size())
        self.process_list_echo_times.addItem(self.echo_widgets[-1])
        self.process_list_echo_times.setItemWidget(
            self.echo_widgets[-1],
            self.echo_foil_widgets[-1])

    def _updateFoilEnabled(self, synthesize = True):
        '''
        Update the states of the list widgets depending on 
        the state of the data selected foils.
        '''
        self.synthesize_scripts = False
        for check_row in self.grid_checkboxes:
            for i, parent in enumerate(self.foil_check):
                check_row[i].setEnabled(parent.isChecked())
        self.synthesize_scripts = True

        if synthesize:
            self._synthesize()

    def _updateFoilTri(self):
        '''
        The first row in are tristate checkboxes who need to
        be set depending on the state of the column
        '''
        self.foil_header_active = False
        for i, parent in enumerate(self.grid_checkboxes[0]):
            active = []
            for row in self.grid_checkboxes[1:]:
                active.append(row[i].isChecked())
            if all(active):
                parent.setCheckState(2)            
            elif not any(active):
                parent.setCheckState(0)
            else:
                parent.setCheckState(1)
        self.foil_header_active = True

        self._synthesize()

    def _updateFoilCol(self):
        '''
        The first row in are tristate checkboxes who need to
        be set depending on the state of the column
        '''
        if self.foil_header_active:
            self.synthesize_scripts = False
            for i, element in enumerate(self.grid_checkboxes[0]):
                if element.checkState() == 1:
                    element.setCheckState(2)
                self.foil_elements_active = False
                self._setFoilCol(i, element.checkState())
                self.foil_elements_active = True
            self.synthesize_scripts = True
            self._synthesize()

    def _setFoilCol(self, col, state):
        '''
        set the state of the element in a column
        '''
        for check_row in self.grid_checkboxes[1:]:
            check_row[col].setChecked(state == 2)

    #######################################################################
    #######################################################################

    def _synthesize(self):
        '''
        run synthesis scripts
        '''
        self._synthesizeFit()
        self._synthesizeData()
        self._synthesizeReduction()

    def _synthesizeFit(self):
        '''
        prepare the python script part that will
        manage the fit parameter part
        '''
        if not self.synthesize_scripts:
            return None
            
        python_string_init = ""

        #set the foils
        python_string_init += "\n#Set the foils (edit in GUI)\n"
        python_string_init += "foils_in_echo = []\n"
        for i,row in enumerate(self.grid_checkboxes[1:]):
            items = []
            for j,element in enumerate(row): 
                if element.isEnabled():
                    if element.checkState():
                        items.append(1)
                    else:
                        items.append(0)
            python_string_init += "foils_in_echo.append("+str(items)+")\n"

        #set the selected
        python_string_init += "\n#Set the selected (edit in GUI)\n"
        python_string_init += "Selected = [ "
        string_array = []

        for i, item in enumerate(self.selected_items):
            if item.checkState() == QtCore.Qt.Checked:
                string_array.append(self.env.current_data.get_axis('Parameter')[i])

        string_array = sorted(string_array)
        for i, item in enumerate(string_array):
            python_string_init += str(item)+ ", "

        python_string_init = python_string_init[:-2]
        python_string_init += "]\n"

        #set the background
        python_string_init += "\n#Set the background (edit in GUI)\n"
        python_string_init += "Background = "+[ str(val) for val in self.env.current_data.get_axis('Parameter') ][self.process_box_back_fit.currentIndex()]+"\n"

        #set the background
        python_string_init += "\n#Set the reference (edit in GUI)\n"
        python_string_init += "Reference = ["+[ str(val) for val in self.env.current_data.get_axis('Parameter') ][self.process_box_refs_fit.currentIndex()]+",0]\n"

        #find area to edit
        text = self.env.process.editable_scripts[1]
        text_array = text.split("\n")

        edit_start = 0
        edit_end = len(text_array)

        for i,line in enumerate(text_array):
            if "self.env" in line:
                edit_start = i
            if ".fit.set_parameter( " in line:
                edit_end = i
                break

        self.env.process.editable_scripts[1] = self._concatenateText([
            text_array[0:edit_start+1],
            python_string_init.split("\n"),
            text_array[edit_end-1:]])

        self._refresh()

    def _synthesizeData(self):
        '''
        prepare the python script part that will
        manage the data parameter part
        '''
        if not self.synthesize_scripts:
            return None

        #find area to edit
        text = self.env.process.editable_scripts[0]
        text_array = text.split("\n")

        #Foils to consider
        checked = []
        for i, checkbox in enumerate(self.foil_check):
            checked.append(int(checkbox.isChecked()))
        for i,element in enumerate(text_array):
            if "metadata_class.add_metadata('Selected foils'" in element:
                text_array[i] = element.split(".current_data.metadata_class.add_metadata(")[0]+".current_data.metadata_class.add_metadata('Selected foils', value = '"+str(checked)+"' , logical_type = 'int_array', unit = '-')"
                break

        for i,element in enumerate(text_array):
            if "mask.setMask(" in element:
                text_array[i] = element.split(".mask.setMask(")[0]+".mask.setMask('"+str([ key for key in self.env.mask.mask_dict.keys() ][self.process_box_masks.currentIndex()])+"')"
                break

        #find strings
        self.env.process.editable_scripts[0] = self._concatenateText([text_array])
        self._refresh()

    def _synthesizeReduction(self):
        '''
        prepare the python script part that will
        manage the data parameter part
        '''
        if not self.synthesize_scripts:
            return None

        #find area to edit
        text = self.env.process.editable_scripts[2]
        text_array = text.split("\n")

        #the mask
        for i,element in enumerate(text_array):
            if "mask.setMask(" in element:
                text_array[i] = element.split(".mask.setMask(")[0]+".mask.setMask('"+str([ key for key in self.env.mask.mask_dict.keys() ][self.process_box_mask_fit.currentIndex()])+"')"
                break

        #find strings
        self.env.process.editable_scripts[2] = self._concatenateText([text_array])
        self._refresh()

    def _concatenateText(self, element_arrays):
        output = ''
        for element in element_arrays:
            for line in element:
                output += line + "\n"

        return output

    #######################################################################
    #######################################################################

    def _refresh(self):
        '''
        Refresh the text present in the code editors
        with the source present in the core env.process 
        class. 
        '''        
        self.text_widgets[0].setText(self.env.process.editable_scripts[0])
        self.text_widgets[1].setText(self.env.process.editable_scripts[1])
        self.text_widgets[2].setText(self.env.process.editable_scripts[2])
        self.text_widgets[3].setText(self.env.process.editable_scripts[3])

    def _updateEditable(self, index):
        if not self.env == None:
            try:
                self.env.process.editable_scripts[index] = self.text_widgets[index].toPlainText()
            except Exception as e:
                dialog(
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
            if index < 5:
                self._runPythonCode(self.text_widgets[index].toPlainText())
            elif index == 5:
                self._runPanel() 

    def runAll(self):
        '''
        Run all the scripts.
        '''
        for i in range(5):
            self.run(i)

    def _runPythonCode(self, code):
        '''
        Parse and run python code. 
        '''
        code_array = self._parseCode(code)
        meta_array = self._parseMeta(code_array)
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

    def _parseCode(self, code):
        '''
        This function will break down the code into smaller 
        parts to allow interpretation of the failed sequence
        as well as a meaningfull understanding of the progress.
        '''

        temp_code_array = []
        indentation     = False
        comment_bool    = False
        code_lines      = code.split('\n') 

        for line in code_lines:
            if line == '' or line[0] == '#':
                pass
            elif line[0] == "'" or line[0] == '"':
                comment_bool = not comment_bool

            elif line[0].isspace() and not line == '' and not comment_bool:
                if not indentation:
                    indentation = not indentation
                    temp = temp_code_array[-1]
                    temp.append(line)
                else:
                    temp.append(line)
            elif not comment_bool:
                if indentation:
                    indentation = not indentation
                temp_code_array.append([line])

        code_array = []
        for element in temp_code_array:
            if len(element) > 1:
                code_string = ''
                for sub_element in element:
                    code_string += sub_element + '\n'
                code_array.append(code_string)
            else:
                code_array.append(element[0])

        return code_array

    def _parseMeta(self, code_array):
        '''
        This function will try to identify the individual 
        function parts to provide nice insight on what is 
        being processed at the moment.
        '''
        meta_array = []
        for element in code_array:
            if len(element.split('for ')) > 1:
                meta_array.append(
                    "'for' loop over "+str(element.split(' in ')[1].split(':')[0]))
            elif '(' in element and ')' in element:
                meta_array.append(
                    "'function' "+element.split('(')[0]+' with the parameters ('+''.join(element.split('(')[1].split(')')[0])[0:30]+')')
            else:
                 meta_array.append(element[0:40])

        return meta_array

    def _runPanel(self):
        '''
        This function will initiate the panel from the current 
        phase processed data.
        '''
        # self.tool.load_initial(self.env)

    def saveScripts(self):
        '''
        This method as the name indicates is in charge of
        prompting the user for a savefile name and location 
        through a QFileDialog and then saves the file as
        a script.
        '''
        filters = "mieze_script_save.py"

        file_path = QtWidgets.QFileDialog.getSaveFileName(
                self.window, 
                'Select file',
                filters)[0]

        self.env.process.saveScripts(
            file_path,
            [
                self.script_text_import.toPlainText(),
                self.script_text_phase.toPlainText(),
                self.script_text_reduction.toPlainText(),
                self.script_text_post.toPlainText()
            ])

    def loadScripts(self):
        '''
        This method will load the string from file through 
        a QFileDialog. Specify a file formated in the right
        way or saved through miezepy.
        '''
        filters = "*.py"

        file_path = QtWidgets.QFileDialog.getOpenFileName(
                self.window, 
                'Select file',
                filters)[0]

        self.env.process.loadScripts(
            file_path)
        self.refresh()

    def populatePara(self):
        '''
        populate the window layout. The grid is the main
        input of this method and all elements will be 
        placed accordingly.
        '''
        self.para_vbox  = QtWidgets.QVBoxLayout()
        self.para_grid  = QtWidgets.QGridLayout()
        self.para_vbox.addLayout(self.para_grid)
        self.para_vbox.addStretch(1)
        self.para_group.setLayout(self.para_vbox)

        #initialise the tab
        self.widget_list    = []

        self.widget_list.append([
            QtWidgets.QLabel('Parameter:', parent = self.para_group),
            0, 0, 1, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter])
        self.widget_list.append([
            QtWidgets.QComboBox( parent = self.para_group),
            0, 1, 1, 1, None])
        self.para_drop = self.widget_list[-1][0]

        self.widget_list.append([
            QtWidgets.QLabel('Measurement:', parent = self.para_group),
            0, 2, 1, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter])
        self.widget_list.append([
            QtWidgets.QComboBox( parent = self.para_group),
            0, 3, 1, 1, None])
        self.meas_drop = self.widget_list[-1][0]

        self.widget_list.append([
            QtWidgets.QLabel('Echo time:', parent = self.para_group),
            1, 0, 1, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter])
        self.widget_list.append([
            QtWidgets.QComboBox( parent = self.para_group),
            1, 1, 1, 1, None])
        self.echo_drop = self.widget_list[-1][0]

        self.widget_list.append([
            QtWidgets.QLabel('Foil:'),
            1, 2, 1, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter])
        self.widget_list.append([
            QtWidgets.QComboBox( parent = self.para_group),
            1, 3, 1, 1, None])
        self.foil_drop = self.widget_list[-1][0]

        ##############################################
        #add the tabs
        for element in self.widget_list:
            self.para_grid.addWidget(
                element[0], 
                element[1], 
                element[2], 
                element[3], 
                element[4])

            if not element[5] == None:
                element[0].setAlignment(element[5])

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