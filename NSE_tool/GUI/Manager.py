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
#   Alexander Schober <alexander.schober@mac.com>
#
# *****************************************************************************
import matplotlib as mpl
from ipywidgets import interact, interactive, fixed, interact_manual, widgets
from mpl_toolkits.axes_grid1 import make_axes_locatable
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cProfile
import timeit
import copy
# from SimplePlot import SimplePlot as sp
# import tkinter as tk

class Manager:

    def __init__(self):

        ##############################################
        #initiate the core manager  
        self.current_env = None

    def launch_panel(self, environement):
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

        #set the local environement for visualisaiton
        self.vis_env = environement

        #initialise parameters
        self.meas = None
        self.para = None
        

        def vis(
            para    = self.vis_env.current_data.get_axis('Temperature')[0], 
            meas    = self.vis_env.current_data.get_axis('Measurement')[0], 
            echo    = self.vis_env.current_data.get_axis('Echo')[0], 
            foil    = self.vis_env.current_data.get_axis('Foil')[0], 
            x0      = self.vis_env.mask.parameters[0][0], 
            y0      = self.vis_env.mask.parameters[0][1], 
            r_outer = self.vis_env.mask.parameters[1], 
            r_inner = self.vis_env.mask.parameters[2], 
            angle1  = self.vis_env.mask.parameters[3][0], 
            angle2  = self.vis_env.mask.parameters[3][1]):
            
            '''
            ##############################################
            The cisualisation function
            ———————
            Input: -
            ———————
            Output: -
            ———————
            status: active
            ##############################################
            '''

            para_idx = self.vis_env.current_data.get_axis_idx('Temperature', para)
            meas_idx = self.vis_env.current_data.get_axis_idx('Measurement', meas)
            echo_idx = self.vis_env.current_data.get_axis_idx('Echo', echo)
            foil_idx = self.vis_env.current_data.get_axis_idx('Foil', foil)

            if not para == self.para or not self.meas == meas:

                self.data = self.vis_env.current_data[para_idx,meas_idx,:,:,:]
                self.reshaped = self.data.return_as_np()

                self.meas = copy.deepcopy(meas)
                self.para = copy.deepcopy(para)


            fig = plt.figure(figsize=(15,10))

            ax = fig.add_subplot(2,2,1)

            #prepare the mask
            parameters = [
                [x0,y0],
                r_outer,
                r_inner,
                [angle1,angle2]]

            self.vis_env.mask.set_parameters(parameters)
            self.vis_env.mask.process_mask(self.vis_env.current_data)
            mask = self.vis_env.mask.mask
            ax.imshow(
                mask * np.sum(
                    self.reshaped, 
                    axis=(0,1,2)), 
                    norm=mpl.colors.LogNorm(), 
                    origin='lower', 
                    cmap='viridis')

            ax = fig.add_subplot(2,2,2)

            counts = [
                np.sum(mask*self.reshaped[echo_idx,foil_idx,timechannel]) 
                for timechannel in range(16)]

    
            self.vis_env.fit.fit_data_cov(
                self.vis_env.results, 
                counts, 
                np.sqrt(counts), 
                Qmin=0.)

            fit = self.vis_env.get_result('Fit data covariance')

            ax.errorbar(range(16), counts, np.sqrt(counts), fmt='o')
            x = np.arange(0,15,0.01)
            ax.errorbar(x, fit['ampl']*np.cos(x/16.*2*np.pi+fit['phase'])+fit['mean'])
            ax.set_ylim(0, np.max(counts)*1.2)
            ax.set_ylabel('counts')
            ax.set_xlabel('time channel')
            ax.text(0, np.max(counts)*1.15, r'contrast = %.2f $\pm$ %.2f' %(fit['pol'], fit['pol_error']['Cov']))

            ax = fig.add_subplot(2,2,3)
    
            self.vis_env.fit.calc_contrast_single_foil(
                foil, 
                [para], 
                self.vis_env.current_data,
                self.vis_env.mask,
                self.vis_env.results)

            process = self.vis_env.get_result('Contrast calculation single')

            ax.errorbar(
                process['Axis'][para], 
                process['Contrast'][para], 
                process['Contrast_error'][para], 
                fmt='o')

            ax.set_xscale('log')
            ax.set_ylim(0,1.)
            ax.set_xlabel('t(ns)')
            ax.set_ylabel('contrast')

            ax = fig.add_subplot(2,2,4)
            mean_value = [np.sum(np.sum(self.reshaped[echo,:,:,:,:], axis=(0,1))*mask) for echo in range(self.reshaped.shape[0])]
            ax.errorbar(process['Axis'][para], mean_value, np.sqrt(mean_value), fmt='o')
            ax.set_xscale('log')
            ax.set_ylim(0.,)
            ax.set_xlabel('t(ns)')
            ax.set_ylabel('mean value')

            plt.show()


        #set the function
        interact(
            vis,
            para    = self.vis_env.current_data.get_axis('Temperature'),
            meas    = self.vis_env.current_data.get_axis('Measurement'), 
            echo    = self.vis_env.current_data.get_axis('Echo'), 
            foil    = self.vis_env.current_data.get_axis('Foil'), 
            x0      = (0, 128, 1), 
            y0      = (0, 128, 1), 
            r_outer = (0, 128, 1), 
            r_inner = (0, 128, 1), 
            angle1  = (0,360,1), 
            angle2  = (0,360,1))


    # def launch_sp(self, environement):
    #     '''
    #     ##############################################
    #     This will be the mieze panel able to manage 
    #     the visualisation of data. 
    #     ———————
    #     Input: 
    #     - environement class
    #     ———————
    #     Output: -
    #     ———————
    #     status: active
    #     ##############################################
    #     '''
    #     self.vis_env = environement
    #     root        = tk.Tk()
    #     myframe     = tk.Frame(root,width=400, height=300)
    #     myframe.pack(fill=tk.BOTH, expand=tk.YES)
    #     mycanvas    = sp.MultiPlotCanvas(
    #         myframe,
    #         grid     = [[True,True],[True,True]],
    #          ratioX   = [1,1],
    #          ratioY   = [1,1],
    #          width    = 100,
    #          height   = 100,
    #          bg       = "white",
    #          highlightthickness = 0)
        
    #     ax = mycanvas.GetSubPlot(0,0)
    
    #     bx = mycanvas.GetSubPlot(1,0)
        
    #     cx = mycanvas.GetSubPlot(1,1)
    #     #cx.MakeGhost()
        
    #     dx = mycanvas.GetSubPlot(0,1)



    #     para    = self.vis_env.current_data.get_axis('Temperature')[0]
    #     meas    = self.vis_env.current_data.get_axis('Measurement')[0]
    #     echo    = self.vis_env.current_data.get_axis('Echo')[0]
    #     foil    = self.vis_env.current_data.get_axis('Foil')[0]
    #     x0      = self.vis_env.mask.parameters[0][0]
    #     y0      = self.vis_env.mask.parameters[0][1]
    #     r_outer = self.vis_env.mask.parameters[1]
    #     r_inner = self.vis_env.mask.parameters[2]
    #     angle1  = self.vis_env.mask.parameters[3][0]
    #     angle2  = self.vis_env.mask.parameters[3][1]

    #     para_idx = self.vis_env.current_data.get_axis_idx('Temperature', para)
    #     meas_idx = self.vis_env.current_data.get_axis_idx('Measurement', meas)
    #     echo_idx = self.vis_env.current_data.get_axis_idx('Echo', echo)
    #     foil_idx = self.vis_env.current_data.get_axis_idx('Foil', foil)

    #     self.data = self.vis_env.current_data[para_idx,meas_idx,:,:,:]
    #     self.reshaped = self.data.return_as_np()

    #     #prepare the mask
    #     parameters = [
    #         [x0,y0],
    #         r_outer,
    #         r_inner,
    #         [angle1,angle2]]

    #     self.vis_env.mask.set_parameters(parameters)
    #     self.vis_env.mask.process_mask(self.vis_env.current_data)
    #     mask = self.vis_env.mask.mask


    #     counts = [
    #         np.sum(mask*self.reshaped[echo_idx,foil_idx,timechannel]) 
    #         for timechannel in range(16)]

    #     self.vis_env.fit.fit_data_cov(
    #         self.vis_env.results, 
    #         counts, 
    #         np.sqrt(counts), 
    #         Qmin=0.)

    #     fit = self.vis_env.get_result('Fit data covariance')

    #     self.vis_env.fit.calc_contrast_single_foil(
    #             foil, 
    #             [para], 
    #             self.vis_env.current_data,
    #             self.vis_env.mask,
    #             self.vis_env.results)

    #     process = self.vis_env.get_result('Contrast calculation single')

    #     x = np.arange(0,128,1)
    #     y = np.arange(0,128,1)

    #     ax.AddBin(
    #         x,
    #         y,
    #         np.transpose(np.sum(self.reshaped, axis=(0,1,2))))

    #     dx.AddBin(
    #         x,
    #         y,
    #         np.transpose(mask * np.sum(self.reshaped, axis=(0,1,2))))

    #     x_1 = np.arange(0,15,0.01)

    #     bx.AddPlot(
    #         range(16), 
    #         counts, 
    #         color = 'blue',
    #         Thickness = 1,
    #         style = ['o-',4,4])

    #     bx.AddPlot(
    #         x_1, 
    #         fit['ampl']*np.cos(x_1/16.*2*np.pi+fit['phase'])+fit['mean'], 
    #         color = 'red',
    #         Thickness = 1)

    #     cx.AddPlot(
    #         process['Axis'][para], 
    #         process['Contrast'][para], 
    #         color = 'blue',
    #         Thickness = 0, 
    #         style = ['o-',4,4])

        
    #     dx.Live = 2
    #     ax.Live = 2
    #     bx.Live = 1

    #     root.mainloop()