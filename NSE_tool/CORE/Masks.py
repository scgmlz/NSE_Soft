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

#############################
#import general components
import matplotlib
import logging
import numpy as np

#############################
#import child components
from .Log import Log_Handler

class Masks:

    def __init__(self):
        '''
        ##############################################
        This is the constructor of the mask class. 
        Feed the datastructure to it and it will 
        inspect if there is a usable data object
        within.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        ############################################
        #run initialisation
        self.generate_default()

        ############################################
        #create the parameter and select instances
        self.selected   = None
        self.parameters = []
        self.commands   = []
        self.log        = Log_Handler()

    def __str__(self):
        '''
        ##############################################
        Generate a string output for the user to 
        see that the mask has initialised 
        properly.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        output =  "\n##########################################################\n"
        output +=  "################## MASK STRUCTURE ########################\n"
        output += "##########################################################\n"
        output += "The mask has been set as follows: \n"
        output += "- Selected mask template: "+str(self.selected)+"\n"
        output += "- Parameters:\n"

        for i in range(0,len(self.parameters)):

            output += "          "+str(self.parameters[i])+"\n"

        output += "----------------------------------------------------------\n"
        
        output += "##########################################################\n\n"

        return output

    def run_commands(self, mask):
        '''
        ##############################################
        The user can here pass on commands and then 
        execute them after the mask has been set. 

        ———————
        Input: 
        - numpy logical mask item
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        for command in self.commands:
            
            try:

                exec(command)
                self.log.add_log(
                    'info',
                    "Sucessfully applied '"
                    +str(command)
                    +"' on the mask")

            except:

                self.log.add_log(
                    'error',
                    "Failed to apply command '"
                    +str(command)
                    +"' on the mask")

        return mask

    def add_command(self, command_str = ''):
        '''
        ##############################################
        The user can here pass on commands here
        that will be executed once the mask is
        finished. 

        the command has to be formated as a string
        ———————
        Input: 
        - command string
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.commands.append(command_str)

        self.log.add_log(
            'info',
            "Added command '"
            +str(command_str)
            +"' to the mask process")

    def remove_command(self, command = '', index = None):
        '''
        ##############################################
        Remove a command from the command list. Either
        pass the command in its full or its index
        ———————
        Input: 
        - command string
        - index
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if not index == None:
            del self.commands[index]

        elif command in self.commands:
            self.commands.remove(command)

    def purge_commands(self):
        '''
        ##############################################
        Remove all commands from the command list. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.commands = []

    def select_template(self, key = ''):
        '''
        ##############################################
        Here we will allow to select the mask that 
        will be kept here until a change is 
        undertaken. 

        Note that this loads the parameters locally
        and that theses can be modified after

        ———————
        Input: 
        - key (str) that will be used to select
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if not key in self.all_masks.keys() and not key in self.all_pre_masks.keys():

            self.log.add_log(
                'error',
                "The mask template '"
                +str(key)
                +"' could not be found")

        else:

            self.selected = key

            if  key in self.all_masks.keys():

                self.parameters = self.all_masks[key][1:]

            if  key in self.all_pre_masks.keys():

                self.parameters = self.all_pre_masks[key][1:]

            self.log.add_log(
                'info',
                "Sucessfully selected the template '"
                +str(key)
                +"'")

    def set_parameters(self, parameters):
        '''
        ##############################################
        Allows the user to inject the parameters of the
        mask that he wants to use. It basically sets
        self.parameters = parameters

        ———————
        Input: 
        - data_structure
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''   
        self.parameters = list(parameters)

    def process_mask(self, target):
        '''
        ##############################################
        We will use the provided selection and 
        parameters to create a mask suited for the 
        provided data shape.

        ———————
        Input: 
        - data_structure
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        ############################################
        #test the target
        assert len(target.data_objects) > 0,\
            "The datastructure is empty, cannot create mask ..."

        ############################################
        #This assumes that the mask has been set
        if  self.selected in self.all_masks.keys():

            mask_target = self.all_masks

        if  self.selected in self.all_pre_masks.keys():

            mask_target = self.all_pre_masks

        shape = target.data_objects[0].dim

        self.mask = mask_target[self.selected][0][0](shape,self.parameters)

        #run the post masks commands
        mask = self.mask
        mask = self.run_commands(mask)
        self.mask = mask


    def generate_default(self):
        '''
        ##############################################
        Will load all the mask templates locally

        ———————
        Input: 
        - data_structure
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        ############################################
        #Run all defautl masks

        self.all_masks = {
            'DB_5': [
                (self.sector_mask, self.sector_mask_Vis),
                (31,35), 
                5, 
                0, 
                (0,360)],

            '10x10_tile': [
                (self.rect_mask, self.rect_mask_Vis),
                (100,100), 
                10,  
                10],

            'SkX_peak': [
                (self.sector_mask, self.sector_mask_Vis),
                (31,35), 
                100, 
                55, 
                (8,46)],

            'SkX_peak_circ': [
                (self.sector_mask, self.sector_mask_Vis),
                (100,70), 
                20, 
                0, 
                (0,360)],

            'SkX_peak_small': [
                (self.sector_mask, self.sector_mask_Vis),
                (31,35), 
                82, 
                72, 
                (22,32)],

            'SkX_between_peaks': [
                (self.sector_mask, self.sector_mask_Vis),
                (31,35), 
                100, 
                55, 
                (46,70)],

            'noDB': [
                (self.sector_mask, self.sector_mask_Vis),
                (31,35), 
                100, 
                55, 
                (0,360)],

            'DB_sixfold': [
                (self.sector_mask, self.sector_mask_Vis),
                (27,33), 
                5, 
                0, 
                (0,360)],

            'SkX_peak_Sixfold': [
                (self.sector_mask, self.sector_mask_Vis),
                (27,33), 
                90, 
                47, 
                (15,52)],

            'SkX_between_peaks_Sixfold': [
                (self.sector_mask, self.sector_mask_Vis),
                (27,33),
                90, 
                47, 
                (52,80)],

            'noDB_Sixfold': [
                (self.sector_mask, self.sector_mask_Vis),
                (31,35), 
                100, 
                42, 
                (0,360)],

            'SkX_peak_circ_Sixfold': [
                (self.sector_mask, self.sector_mask_Vis),
                (84,69), 
                20,
                0, 
                (0,360)],

            'SkX_peak_SkXCon': [
                (self.sector_mask, self.sector_mask_Vis),
                (28,34), 
                85, 
                65, 
                (82,100)]
            }

        self.all_pre_masks = {
            'Pre_SkX_peak': [
                (self.gen_pregroup_mask, self.gen_pregroup_mask_Vis),
                (31,31), 
                57, 
                102, 
                (11,50), 
                15, 
                13],

            'Pre_SkX_peak_Sixfold': [
                (self.gen_pregroup_mask, self.gen_pregroup_mask_Vis),
                (28,34), 
                45, 
                90, 
                (17,56), 
                15, 
                13],

            'Pre_SkX_peak_SkXCon': [
                (self.gen_pregroup_mask, self.gen_pregroup_mask_Vis),
                (28,34), 
                65,
                85, 
                (80,104), 
                10, 
                11]
            }

    def gen_pregroup_mask(self, shape, parameters):

        ############################################
        #Unpack the parameters
        centre          = parameters[0]
        inner_radius    = parameters[1]
        outer_radius    = parameters[2]
        angle_range     = parameters[3] 
        r_width         = parameters[4]
        phi_width       = parameters[5]
       
        
        ############################################
        #Process
        mask = np.zeros(shape, dtype=np.int)

        index = 1

        for phi_step in range(int((angle_range[1]-angle_range[0]) / phi_width)):

            for r_step in range(int((outer_radius-inner_radius)/r_width)):

                #Pack the parameters
                parameters = [
                    centre,
                    inner_radius+(r_step+1)*r_width,
                    inner_radius+r_step*r_width,
                    (angle_range[0]+phi_step*phi_width,
                    angle_range[0]+(phi_step+1)*phi_width)
                ]

                #append the mask
                mask += self.sector_mask(shape,parameters)*index

                #move index forward
                index += 1

        return mask

    def sector_mask(self, shape, parameters):

        ############################################
        #Unpack the parameters
        centre          = parameters[0]
        outer_radius    = parameters[1]
        inner_radius    = parameters[2]
        angle_range     = parameters[3]

        ############################################
        #create the mask
        # -> Check whether sector is in image
        y, x = np.ogrid[:shape[0],:shape[1]]
        cx,cy = centre
        tmin,tmax = np.deg2rad(angle_range)
        
        #ensure stop angle > start angle
        if tmax<tmin:
            tmax += 2*np.pi

        #convert cartesian --> polar coordinates
        r2 = (x-cx)*(x-cx) + (y-cy)*(y-cy)
        theta = np.arctan2(y-cy,x-cx) - tmin

        #wrap angles between 0 and 2*pi
        theta %= (2*np.pi)

        #circular mask
        circmask    = r2 <  outer_radius*outer_radius
        circmask2   = r2 >= inner_radius*inner_radius

        # angular mask
        anglemask = theta <= (tmax-tmin)

        return circmask * circmask2 * anglemask

    def rect_mask(self, shape, parameters):
        
        ############################################
        #Unpack the parameters
        centre  = parameters[0] 
        width   = parameters[1]
        height  = parameters[3]
        
        ############################################
        #create the mask
        mask = np.zeros((int(shape[0]),int(shape[1])), dtype=bool)
    
        cx, cy = centre
        mask[int(cy - height/2):int(cy + height/2),int(cx - width/2):int(cx + width/2)] = True
        
        self.mask = mask

    def gen_pregroup_mask_Vis(self,Target, parameters):

        ############################################
        #Unpack the parameters
        shape           = [int(parameters[0][0]),int(parameters[0][1])]
        center          = parameters[1]
        inner_radius    = parameters[2]
        outer_radius    = parameters[3]
        angle_range     = parameters[4] 
        r_width         = parameters[5]
        phi_width       = parameters[6]

        ############################################
        #send out the shapes
        index = 0

        phi_array = [phi_step for phi_step in range(int((angle_range[1]-angle_range[0]) / phi_width))]

        R_array = [r_step for r_step in range(int(((outer_radius-inner_radius)/r_width)))]

        colors = matplotlib.cm.rainbow(np.linspace(0, 1, len(phi_array)*len(R_array)))

        for phi_step in phi_array:

            
            for r_step in R_array:

                #Pack the parameters
                parameters = [
                    shape,
                    center,
                    inner_radius+(r_step+1)*r_width,
                    inner_radius+r_step*r_width,
                    (angle_range[0]+phi_step*phi_width,
                    angle_range[0]+(phi_step+1)*phi_width)
                ]

                #append the mask
                self.sector_mask_Vis(Target, parameters, color = matplotlib.colors.rgb2hex(colors[index][:3]))

                #move index forward
                index += 1

    def sector_mask_Vis(self, Target, parameters, color = "black"):

        ############################################
        #Unpack the parameters
        centre          = parameters[1]
        outer_radius    = parameters[2]
        inner_radius    = parameters[3]
        angle_range     = parameters[4]

        ############################################
        #send out the anular wedge
        tmin,tmax = np.deg2rad(angle_range)

        Target.annular_wedge(

            x = [centre[0]],
            y = [centre[1]],
            inner_radius = inner_radius,
            outer_radius = outer_radius,
            start_angle  = tmin,
            end_angle    = tmax,
            color   = color,
            alpha   = 0.5)

    def rect_mask_Vis(self, Target, parameters):

        ############################################
        #Unpack the parameters
        centre  = parameters[1] 
        width   = parameters[2]
        height  = parameters[3]
        print(parameters)

        ############################################
        #send out the rectangle
        Target.rect(
            x = [centre[0]],
            y = [centre[1]],
            width   = width,
            height  = height,
            color   = "black",
            alpha   = 0.5)

