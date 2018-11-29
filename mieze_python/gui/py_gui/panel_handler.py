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

#new machinery
import numpy as np
from .qrangeslider import QRangeSlider
from simpleplot.multi_canvas import Multi_Canvas
from PyQt5 import QtWidgets, QtCore, QtGui
import sys



class PanelHandler:
    def __init__(self, env, main_widget, parameter_layout, mask_layout):
        self.launch_sp(env, main_widget, parameter_layout, mask_layout)

    def launch_sp(self, environment, main_widget, parameter_layout, mask_layout):
        '''
        ##############################################
        This will be the mieze panel able to manage 
        the visualisation of data. 
        ———————
        Input: 
        - environement class
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        ##############################################
        #set up parameters
        self.environment = environment
        self.threads = []
        self.setup_frame(main_widget, parameter_layout, mask_layout)

    def setup_frame(self, main_widget, parameter_layout, mask_layout):
        '''
        ##############################################
        populate the window layout. The grid is the main
        input of this method and all elements will be 
        placed accordingly.
        ———————
        Input: 
        - Qt layout grid
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.main_widget    = main_widget

        #the parameter layouts 
        self.para_group         = parameter_layout
        self.para_vbox          = QtWidgets.QVBoxLayout()
        self.para_grid          = QtWidgets.QGridLayout()

        self.mask_group         = mask_layout
        self.mask_vbox          = QtWidgets.QVBoxLayout()
        self.mask_grid          = QtWidgets.QGridLayout()
        
        self.vis_grid           = QtWidgets.QGridLayout()

        #populate 
        self.populate_para(self.para_grid)
        self.populate_mask(self.mask_grid)
        self.populate_vis(self.vis_grid)

        #set inner layouts
        self.para_vbox.addLayout(self.para_grid)
        self.para_vbox.addStretch(1)
        self.para_group.setLayout(self.para_vbox)

        self.mask_vbox.addLayout(self.mask_grid)
        self.mask_vbox.addStretch(1)
        self.mask_group.setLayout(self.mask_vbox)
        
        self.main_widget.setLayout(self.vis_grid)

    def populate_para(self, grid):
        '''
        ##############################################
        populate the window layout. The grid is the main
        input of this method and all elements will be 
        placed accordingly.
        ———————
        Input: 
        - Qt layout grid
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #initialise the tab
        self.widget_list    = []

        #----------
        self.widget_list.append([
            QtWidgets.QLabel('Parameter:', parent = self.para_group),
            0, 0, 1, 2, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter])

        self.widget_list.append([
            QtWidgets.QComboBox( parent = self.para_group),
            1, 0, 1, 2, None])

        self.para_drop = self.widget_list[-1][0]

        #----------
        self.widget_list.append([
            QtWidgets.QLabel('Measurement:', parent = self.para_group),
            2, 0, 1, 2, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter])

        self.widget_list.append([
            QtWidgets.QComboBox( parent = self.para_group),
            3, 0, 1, 2, None])

        self.meas_drop = self.widget_list[-1][0]

        #----------
        self.widget_list.append([
            QtWidgets.QLabel('Echo time:', parent = self.para_group),
            4, 0, 1, 2, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter])

        self.widget_list.append([
            QtWidgets.QComboBox( parent = self.para_group),
            5, 0, 1, 2, None])

        self.echo_drop = self.widget_list[-1][0]

        #----------
        self.widget_list.append([
            QtWidgets.QLabel('Foil:'),
            6, 0, 1, 2, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter])
        
        self.widget_list.append([
            QtWidgets.QComboBox( parent = self.para_group),
            7, 0, 1, 2, None])

        self.foil_drop = self.widget_list[-1][0]

        ##############################################
        #add the tabs
        for element in self.widget_list:

            grid.addWidget(element[0], element[1], element[2], element[3] , element[4])
            
            #manage alignement
            if not element[5] == None:
                element[0].setAlignment(element[5])

    def populate_mask(self, grid):
        '''
        ##############################################
        populate the window layout. The grid is the main
        input of this method and all elements will be 
        placed accordingly.
        ———————
        Input: 
        - Qt layout grid
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #initialise the tab
        self.widget_list    = []

        #----------
        self.widget_list.append([
            QtWidgets.QLabel('Position (x,y):', parent = self.mask_group),
            8, 0, 1, 2, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter])

        self.widget_list.append([
            QtWidgets.QLineEdit('0, 0',parent = self.mask_group),
            9, 0, 1, 2, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter])

        self.pos_in = self.widget_list[-1][0]
            
        #----------
        self.widget_list.append([
            QtWidgets.QLabel('Radius (inner, outer):', parent = self.mask_group),
            10, 0, 1, 2, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter])

        self.radi_in = QRangeSlider(parent = self.mask_group)
        self.radi_in.setFixedHeight(30)
        self.radi_in.setFixedWidth(160)

        self.widget_list.append([
            self.radi_in,
            11, 0, 1, 2, None])

        self.radi_in.setMin(0)
        self.radi_in.setMax(200)

        self.widget_list.append([
            QtWidgets.QSpinBox(parent = self.mask_group),
            12, 0, 1, 1, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter])

        self.radi_in_min = self.widget_list[-1][0]
        self.radi_in_min.setMaximum(128)

        self.widget_list.append([
            QtWidgets.QSpinBox(parent = self.mask_group),
            12, 1, 1, 1, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter])

        self.radi_in_max = self.widget_list[-1][0]
        self.radi_in_max.setMaximum(128)

        #----------
        self.widget_list.append([
            QtWidgets.QLabel('Angle (left, right):', parent = self.mask_group),
            13, 0, 1 , 2, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter])

        self.angle_in = QRangeSlider(parent = self.mask_group)
        self.angle_in.setFixedHeight(30)
        self.angle_in.setFixedWidth(160)

        self.widget_list.append([
            self.angle_in,
            14, 0, 1, 2, None])

        self.angle_in.setMin(0)
        self.angle_in.setMax(360)

        self.widget_list.append([
            QtWidgets.QSpinBox(parent = self.mask_group),
            15, 0, 1, 1, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter])

        self.angle_in_min = self.widget_list[-1][0]
        self.angle_in_min.setMaximum(360)

        self.widget_list.append([
            QtWidgets.QSpinBox(parent = self.mask_group),
            15, 1, 1, 1, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter])

        self.angle_in_max = self.widget_list[-1][0]
        self.angle_in_max.setMaximum(360)

        #----------
        self.widget_list.append([
            QtWidgets.QLabel('Default Mask:', parent = self.mask_group),
            16, 0, 1, 2, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter])

        self.widget_list.append([
            QtWidgets.QComboBox( parent = self.mask_group),
            17, 0, 1, 2, None])

        self.mask_drop = self.widget_list[-1][0]

        ##############################################
        #add the tabs
        for element in self.widget_list:

            grid.addWidget(element[0], element[1], element[2], element[3] , element[4])
            
            #manage alignement
            if not element[5] == None:
                element[0].setAlignment(element[5])

        ##############################################
        #connect elements
        self.radi_in.startValueChanged.connect(self.set_rad_text_start)
        self.radi_in.endValueChanged.connect(self.set_rad_text_end)
        self.radi_in_min.valueChanged.connect(self.set_rad_slider_start)
        self.radi_in_max.valueChanged.connect(self.set_rad_slider_end)

        self.angle_in.startValueChanged.connect(self.set_angle_text_start)
        self.angle_in.endValueChanged.connect(self.set_angle_text_end)
        self.angle_in_min.valueChanged.connect(self.set_angle_slider_start)
        self.angle_in_max.valueChanged.connect(self.set_angle_slider_end)

        self.mask_drop.currentIndexChanged.connect(self.set_mask)

    def populate_vis(self, grid):
        '''
        ##############################################
        populate the window layout. The grid is the main
        input of this method and all elements will be 
        placed accordingly.
        ———————
        Input: 
        - Qt layout grid
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        #initialise container widget
        widget      = QtWidgets.QWidget()
        self.data   = self.environment.current_data.return_as_np()

        self.mycanvas    = Multi_Canvas(
            widget,
            grid        = [[True,True],[True,True]],
            x_ratios    = [2,3],
            y_ratios    = [2,2],
            background  = "w",
            highlightthickness = 0)

        #set the subplots as local
        self.ax = self.mycanvas.get_subplot(0,0)
        self.bx = self.mycanvas.get_subplot(0,1)
        self.cx = self.mycanvas.get_subplot(1,0)
        self.dx = self.mycanvas.get_subplot(1,1)

        self.dx.zoomer.set_fixed(fixed = [False,True], fixed_range = [
            None,
            None,
            0,1
        ])

        self.ax.draw()
        self.bx.draw()
        self.cx.draw()
        self.dx.draw()

        self.ax.pointer['Sticky'] = 3
        self.bx.pointer['Sticky'] = 3

        #place the plot into the grid
        grid.addWidget(widget, 0,0)

    #-----------------------
    #the slots for the radius
    def set_rad_text_start(self, value):
        
        self.radi_in_min.setValue(int(value))

    def set_rad_text_end(self, value):
        
        self.radi_in_max.setValue(int(value))

    def set_rad_slider_start(self, value):
    
        self.radi_in.setStart(int(value))

    def set_rad_slider_end(self, value):
        
        self.radi_in.setEnd(int(value))

    #-----------------------
    #the slots for the angle
    def set_angle_text_start(self, value):
        
        self.angle_in_min.setValue(int(value))

    def set_angle_text_end(self, value):
        
        self.angle_in_max.setValue(int(value))

    def set_angle_slider_start(self, value):
    
        self.angle_in.setStart(int(value))

    def set_angle_slider_end(self, value):
        
        self.angle_in.setEnd(int(value))

    def set_mask(self):
        '''
        ##############################################
        the computation will be done in a thread and 
        if not finished interupted to allow the UI to
        run smoothly
        ———————
        Input: 
        - environement class
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        ##############################################
        #grab the parameters from the UI
        mask_str    = list(self.environment.mask.all_masks.keys())[self.mask_drop.currentIndex()]
        self.environment.mask.select_template(key = mask_str)

        # ##############################################
        # #grab the parameters from the mask class
        x0      = self.environment.mask.parameters[0][0]
        y0      = self.environment.mask.parameters[0][1]
        r_outer = self.environment.mask.parameters[1]
        r_inner = self.environment.mask.parameters[2]
        angle1  = self.environment.mask.parameters[3][0]
        angle2  = self.environment.mask.parameters[3][1]

        ##############################################
        #set the ranges
        self.pos_in.setText(str(x0)+', '+str(y0))
        self.set_rad_text_start(r_inner)
        self.set_rad_text_end(r_outer)
        self.set_rad_slider_start(r_inner)
        self.set_rad_slider_end(r_outer)

        self.set_angle_text_start(angle1)
        self.set_angle_text_end(angle2)
        self.set_angle_slider_start(angle1)
        self.set_angle_slider_end(angle2)

    def load_initial(self):
        '''
        ##############################################
        This method will set  p the widgets initial 
        values so that the user can select accordingly
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        
        ##############################################
        #grab them all
        para    = self.environment.current_data.get_axis(
            self.environment.current_data.axes.names[0])
        meas    = self.environment.current_data.get_axis(
            self.environment.current_data.axes.names[1])
        echo    = self.environment.current_data.get_axis(
            self.environment.current_data.axes.names[2])
        foil    = self.environment.current_data.get_axis(
            self.environment.current_data.axes.names[3])

        x0      = self.environment.mask.parameters[0][0]
        y0      = self.environment.mask.parameters[0][1]
        r_inner = self.environment.mask.parameters[1]
        r_outer = self.environment.mask.parameters[2]
        angle1  = self.environment.mask.parameters[3][0]
        angle2  = self.environment.mask.parameters[3][1]

        ##############################################
        #set the dropdown menues
        self.para_drop.clear()
        self.para_drop.addItems([str(e) for e in para])
        self.meas_drop.clear()
        self.meas_drop.addItems([str(e) for e in meas])
        self.foil_drop.clear()
        self.foil_drop.addItems([str(e) for e in foil])
        self.echo_drop.clear()
        self.echo_drop.addItems([str(e) for e in echo])
        self.mask_drop.clear()
        self.mask_drop.addItems(list(self.environment.mask.all_masks.keys()))
        self.mask_drop.setCurrentIndex(list(self.environment.mask.all_masks.keys()).index(self.environment.mask.selected))

        ##############################################
        #set the position
        self.pos_in.setText(str(x0)+', '+str(y0))

        ##############################################
        #set the ranges
        self.set_rad_text_start(r_inner)
        self.set_rad_text_end(r_outer)
        self.set_rad_slider_start(r_inner)
        self.set_rad_slider_end(r_outer)

        self.set_angle_text_start(angle1)
        self.set_angle_text_end(angle2)
        self.set_angle_slider_start(angle1)
        self.set_angle_slider_end(angle2)

        self.para_drop.currentIndexChanged.connect(self.build_thread)
        self.meas_drop.currentIndexChanged.connect(self.build_thread)
        self.echo_drop.currentIndexChanged.connect(self.build_thread)
        self.foil_drop.currentIndexChanged.connect(self.build_thread)

        self.pos_in.textChanged.connect(self.build_thread)
        self.angle_in_min.valueChanged.connect(self.build_thread)
        self.angle_in_max.valueChanged.connect(self.build_thread)
        self.radi_in_min.valueChanged.connect(self.build_thread)
        self.radi_in_max.valueChanged.connect(self.build_thread)

        ##############################################
        #run the plot
        #self.build_thread()

    def build_thread(self):
        '''
        ##############################################
        the computation will be done in a thread and 
        if not finished interupted to allow the UI to
        run smoothly
        ———————
        Input: 
        - environement class
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        #grab the parameters and get them ready to initialise worker
        parameters = self.prepare_thread()

        #initialize worker and thread
        self.worker = Worker(parameters)
        self.threads.append(QtCore.QThread())

        #send the worker to the thread
        self.worker.moveToThread(self.threads[-1])

        #connect the finished signals
        self.worker.finished.connect(self.update_visual)
        self.worker.finished.connect(self.threads[-1].quit)

        #connect the started and run
        self.threads[-1].started.connect(self.worker.run)
        self.threads[-1].start()


    def prepare_thread(self):
        '''
        ##############################################
        the computation will be done in a thread and 
        if not finished interupted to allow the UI to
        run smoothly
        ———————
        Input: 
        - environement class
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        ##############################################
        #grab the parameters from the UI
        para    = self.environment.current_data.get_axis(
            self.environment.current_data.axes.names[0])[
                self.para_drop.currentIndex()]
        meas    = self.environment.current_data.get_axis(
            self.environment.current_data.axes.names[1])[
                self.meas_drop.currentIndex()]
        echo    = self.environment.current_data.get_axis(
            self.environment.current_data.axes.names[2])[
                self.echo_drop.currentIndex()]
        foil    = self.environment.current_data.get_axis(
            self.environment.current_data.axes.names[3])[
                self.foil_drop.currentIndex()]

        x0      = float(str(self.pos_in.text()).split(",")[0])
        y0      = float(str(self.pos_in.text()).split(",")[1])
        r_inner = float(self.radi_in.start())
        r_outer = float(self.radi_in.end())
        angle1  = float(self.angle_in.start())
        angle2  = float(self.angle_in.end())

        ##############################################
        #process index
        para_idx = self.environment.current_data.get_axis_idx(
            self.environment.current_data.axes.names[0],
            para)
        meas_idx = self.environment.current_data.get_axis_idx(
            self.environment.current_data.axes.names[1],
            meas)
        echo_idx = self.environment.current_data.get_axis_idx(
            self.environment.current_data.axes.names[2],
            echo)
        foil_idx = self.environment.current_data.get_axis_idx(
            self.environment.current_data.axes.names[3], 
            foil)

        parameters = [
            [x0,y0],
            r_inner,
            r_outer,
            [angle1,angle2]]

        self.environment.mask.set_parameters(parameters)
        self.environment.mask.process_mask(self.environment.current_data)
        self.mask = self.environment.mask.mask

        return [
            self.data[para_idx,meas_idx,:,:,:],
            para,meas,
            echo,foil,
            para_idx, meas_idx,
            echo_idx, foil_idx,
            self.environment,
            self.mask]

    def update_visual(self):
        '''
        ##############################################
        Update the visual component from a thread
        ———————
        Input: 
        - environement class
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        ##############################################
        #fetch parameters from the worker
        para            = self.worker.parameters[1]
        self.reshaped   = self.worker.parameters[0]
        self.process    = self.worker.process
        self.counts     = self.worker.counts
        self.fit        = self.worker.fit

        ##############################################
        #try to clear the axes
        try:
            self.ax.clear()
            self.bx.clear()
            self.cx.clear()
            self.dx.clear()

        except:
            pass

        ##############################################
        #prepare rudimentary plto data
        x = np.arange(0,128,1)
        y = np.arange(0,128,1)
        x_1 = np.arange(0,15,0.01)

        #set the two bin
        self.ax.add_plot(
            'Bin', 
            x, 
            y, 
            np.log10(
                np.transpose(
                    np.sum(
                        self.reshaped[
                            self.echo_drop.currentIndex(),
                            self.foil_drop.currentIndex()], 
                        axis=(0)))+1), Name = 'bin' )

        self.bx.add_plot(
            'Bin', 
            x, 
            y,
            np.log10(np.transpose(
                self.mask * np.sum(
                    self.reshaped[
                        self.echo_drop.currentIndex(),
                        self.foil_drop.currentIndex()
                    ], 
                    axis=(0)))+1 ), Name = 'bin')

        #set the main scatter plot of the counts
        self.cx.add_plot(
            'Scatter', 
            range(16), 
            self.counts, 
            Style   = ['s','10'], 
            Log     = [False,False],
            Error   = {
                'bottom': np.sqrt(self.counts),
                'top': np.sqrt(self.counts)})

        if not self.fit == None:

            self.cx.add_plot(
                'Scatter', 
                x_1, 
                self.fit['ampl']*np.cos(x_1/16.*2*np.pi+self.fit['phase'])+self.fit['mean'], 
                Style   = ['-'], 
                Log     = [False,False])

        if not self.process == None:

            self.dx.add_plot(
                'Scatter', 
                self.process['Axis'][para], 
                self.process['Contrast'][para], 
                Style   = ['-','s','10'], 
                Log     = [True,False])

        ##############################################
        #draw the plots
        self.ax.redraw()
        self.bx.redraw()
        self.cx.redraw()
        self.dx.redraw()

class Worker(QtCore.QObject):

    #the pyslots
    finished = QtCore.pyqtSignal()
    intReady = QtCore.pyqtSignal(int)

    def __init__(self, parameters):
        '''
        ##############################################
        define the parameters
        ———————
        Input: 
        - 0 data as numpy array
        - 1 para
        - 2 meas
        - 3 echo
        - 4 foil
        - 5 para
        - 6 meas
        - 7 echo
        - 8 foil
        - 9 env
        - 10 mask
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        QtCore.QObject.__init__(self)
        self.parameters = parameters
        
    @QtCore.pyqtSlot()
    def run(self): # A slot takes no params

        '''
        ##############################################
        define the parameters
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        para    = self.parameters[1]
        foil    = self.parameters[4]

        ##############################################
        #process index
        echo_idx = self.parameters[7]
        foil_idx = self.parameters[8]

        self.reshaped       = self.parameters[0]
        self.mask           = self.parameters[10]
        self.environment    = self.parameters[9]

        ##############################################
        #set default
        self.fit            = None
        self.counts         = [
            np.sum(self.mask * self.reshaped[echo_idx,foil_idx,timechannel]) 
            for timechannel in range(16)]
        self.process        = None

        ##############################################
        #try to calculate
        try:
            self.environment.fit.fit_data_cov(
                self.environment.results, 
                self.counts, 
                np.sqrt(self.counts), 
                Qmin=0.)

            self.fit = self.environment.get_result('Fit data covariance')

        except:
            print('Fit failed')

        self.environment.fit.calcCtrstMain( 
            self.environment.current_data,
            self.environment.mask,
            self.environment.results,
            select = [para],
            foil = foil)

        self.process = self.environment.get_result('Contrast calculation')

        try:

            self.environment.fit.calcCtrstMain( 
                    self.environment.current_data,
                    self.environment.mask,
                    self.environment.results,
                    select = [para],
                    foil = foil)

            self.process = self.environment.get_result('Contrast calculation')

        except:
            print('Contrast')

        self.finished.emit()