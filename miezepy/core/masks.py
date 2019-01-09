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
import json
import numpy as np

#############################
#import child components
from .mask_modules.generator     import MaskGenerator

class Masks:

    def __init__(self):
        '''
        This is the constructor of the mask class. 
        Feed the datastructure to it and it will 
        inspect if there is a usable data object
        within.
        '''
        self.initialize()

    def initialize(self):
        '''
        Set the mask environment and initialize
        the different components
        '''
        self.commands   = []
        self.mask_gen   = MaskGenerator()
        self.mask_dict  = self.generateDefaults()
        self.defaults   = [key for key in self.mask_dict.keys()]
        self.mask_types = [
            'square',
            'arc',
            'triangle',
            'linear composition',
            'radial composition']
        self.setMask(self.defaults[0])

    def setMask(self, name):
        '''
        Set the mask present in the dictionary
        '''
        if name in self.mask_dict.keys():
            self.current_mask = name
        
    def addMask(self, name):
        '''
        Add a mask to the dictionary
        '''
        self.mask_dict[name] = []
        self.setMask(name)

    def addElement(self, values, name = None):
        '''
        Add a mask element to the mask
        values should be a list of 
        properties like the defaults.
        '''
        if name == None:
            name = self.current_mask

        self.mask_dict[name].append(list(values))

    def removeElement(self, idx, name = None):
        '''
        Add a mask element to the mask
        values should be a list of 
        properties like the defaults.
        '''
        if name == None:
            name = self.current_mask

        del self.mask_dict[name][idx]

    def sendToGenerator(self, recreate = True):
        '''
        Send the currently defined class to 
        the generator which will create the
        adequate objects for the mask generation
        '''
        self.mask_gen.grabMask(self.mask_dict[self.current_mask], recreate = recreate)

    def generateMask(self, size_x, size_y):
        '''
        Generate the masks of the generator
        '''
        self.mask_gen.generateMask(size_x,size_y)

    def saveSingleMask(self, path):
        '''
        Writes a mask to json
        '''
        f = open(path, 'w')
        f.write(json.dumps(self.mask_dict[self.current_mask]))
        f.close()

    def saveAllMasks(self, path):
        '''
        Writes a mask to json
        '''
        f = open(path, 'w')
        f.write(json.dumps(self.mask_dict))
        f.close()

    def loadSingleMask(self, path):
        '''
        Writes a mask to json
        '''
        f = open(path, 'r')
        self.mask_dict[self.current_mask] = json.load(f)
        f.close()

    def loadAllMasks(self, path):
        '''
        Writes a mask to json
        '''
        f = open(path, 'r')
        self.mask_dict = json.load(f)
        f.close()

    def generateDefaults(self):
        '''
        Will load all the mask templates locally
        '''
        mask_dict = {
            'DB_5': [[
                'arc',
                (31,35),
                0,
                (0,5), 
                (0,360)]],
            '10x10_tile': [[
                'square',
                (100,100),
                0,
                10,10]],
            'SkX_peak': [[
                'arc',
                (31,35),
                0, 
                (55,100), 
                (8,46)]],
            'SkX_peak_circ': [[
                'arc',
                (100,70),
                0, 
                (0,20), 
                (0,360)]],
            'SkX_peak_small': [[
                'arc',
                (31,35),
                0, 
                (72,82), 
                (22,32)]],
            'SkX_between_peaks': [[
                'arc',
                (31,35),
                0, 
                (55,100), 
                (46,70)]],
            'noDB': [[
                'arc',
                (31,35),
                0, 
                (55,100), 
                (0,360)]],
            'DB_sixfold': [[
                'arc',
                (27,33),
                0, 
                (0,5), 
                (0,360)]],
            'SkX_peak_Sixfold': [[
                'arc',
                (27,33),
                0, 
                (47,90), 
                (15,52)]],
            'SkX_between_peaks_Sixfold': [[
                'arc',
                (27,33),
                0,
                (47,90), 
                (52,80)]],
            'noDB_Sixfold': [[
                'arc',
                (31,35),
                0, 
                (42,100), 
                (0,360)]],
            'SkX_peak_circ_Sixfold': [[
                'arc',
                (84,69),
                0, 
                (0,20), 
                (0,360)]],
            'SkX_peak_SkXCon': [[
                'arc',
                (28,34),
                0, 
                (65,85), 
                (82,100)]]
            }

        return mask_dict

        # self.all_pre_masks = {
        #     'Pre_SkX_peak': [
        #         (self.gen_pregroup_mask_circ),
        #         (31,31), 
        #         57, 
        #         102, 
        #         (11,50), 
        #         15, 
        #         13],

        #     'Pre_SkX_peak_Sixfold': [
        #         (self.gen_pregroup_mask_circ),
        #         (28,34), 
        #         45, 
        #         90, 
        #         (17,56), 
        #         15, 
        #         13],

        #     'Pre_SkX_peak_SkXCon': [
        #         (self.gen_pregroup_mask_circ),
        #         (28,34), 
        #         65,
        #         85, 
        #         (80,104), 
        #         10, 
        #         11],

        #     'Pre_tile': [
        #         (self.gen_pregroup_mask_square),
        #         (0,0), 
        #         0,
        #         0,
        #         128,
        #         128]
        #     }

    # def gen_pregroup_mask_circ(self, shape, parameters):

    #     ############################################
    #     #Unpack the parameters
    #     centre          = parameters[0]
    #     inner_radius    = parameters[1]
    #     outer_radius    = parameters[2]
    #     angle_range     = parameters[3] 
    #     r_width         = parameters[4]
    #     phi_width       = parameters[5]
        
    #     ############################################
    #     #Process
    #     mask = np.zeros(shape, dtype=np.int)

    #     index = 1

    #     for phi_step in range(int((angle_range[1]-angle_range[0]) / phi_width)):

    #         for r_step in range(int((outer_radius-inner_radius)/r_width)):

    #             #Pack the parameters
    #             parameters = [
    #                 centre,
    #                 inner_radius+r_step*r_width,
    #                 inner_radius+(r_step+1)*r_width,
    #                 (angle_range[0]+phi_step*phi_width,
    #                 angle_range[0]+(phi_step+1)*phi_width)
    #             ]

    #             #append the mask
    #             mask += self.sector_mask(shape,parameters)*index

    #             #move index forward
    #             index += 1

    #     return mask

    # def gen_pregroup_mask_square(self, shape, parameters):
    
    #     ############################################
    #     #Unpack the parameters
    #     centre          = parameters[0]
    #     x_dim           = parameters[1]
    #     y_dim           = parameters[2]
    #     n_x             = parameters[1]
    #     n_y             = parameters[2]
       
        
    #     ############################################
    #     #Process
    #     mask = np.zeros(shape, dtype=np.int)

    #     for x in range(mask.shape[0]/n_x):
    #         for y in range(mask.shape[1]/n_y):
    #             pass#mask[x*n:x*n+(n), y*n:y*n+(n)] = x*shape[0]/n + y + 1

    #     return mask

    # def sector_mask(self, shape, parameters):

    #     ############################################
    #     #Unpack the parameters
    #     centre          = parameters[0]
    #     inner_radius    = parameters[1]
    #     outer_radius    = parameters[2]
    #     angle_range     = parameters[3]

    #     ############################################
    #     #create the mask
    #     # -> Check whether sector is in image
    #     y, x = np.ogrid[:shape[1],:shape[0]]
    #     cx,cy = centre
    #     tmin,tmax = np.deg2rad(angle_range)
        
    #     #ensure stop angle > start angle
    #     if tmax<tmin:
    #         tmax += 2*np.pi

    #     #convert cartesian --> polar coordinates
    #     r2 = (x-cx)*(x-cx) + (y-cy)*(y-cy)
    #     theta = np.arctan2(y-cy,x-cx) - tmin

    #     #wrap angles between 0 and 2*pi
    #     theta %= (2*np.pi)

    #     #circular mask
    #     circmask    = r2 <  outer_radius*outer_radius
    #     circmask2   = r2 >= inner_radius*inner_radius

    #     # angular mask
    #     anglemask = theta <= (tmax-tmin)

    #     return circmask * circmask2 * anglemask

    # def rect_mask(self, shape, parameters):
        
    #     ############################################
    #     #Unpack the parameters
    #     centre  = parameters[0] 
    #     width   = parameters[1]
    #     height  = parameters[2]
        
    #     ############################################
    #     #create the mask
    #     mask = np.zeros((int(shape[0]),int(shape[1])), dtype=bool)
    
    #     cx, cy = centre
    #     mask[int(cy - height/2):int(cy + height/2),int(cx - width/2):int(cx + width/2)] = True
        
    #     return mask
    # def __str__(self):
    #     '''
    #     Generate a string output for the user to 
    #     see that the mask has initialised 
    #     properly.
    #     '''
    #     output =  "\n##########################################################\n"
    #     output +=  "################## MASK STRUCTURE ########################\n"
    #     output += "##########################################################\n"
    #     output += "The mask has been set as follows: \n"
    #     output += "- Selected mask template: "+str(self.selected)+"\n"
    #     output += "- Parameters:\n"

    #     for i in range(0,len(self.parameters)):

    #         output += "          "+str(self.parameters[i])+"\n"

    #     output += "----------------------------------------------------------\n"
        
    #     output += "##########################################################\n\n"

    #     return output

    def run_commands(self, mask):
        '''
        The user can here pass on commands and then 
        execute them after the mask has been set. 
        '''
        for command in self.commands:
            try:
                exec(command)
                self.log.add_log(
                    'info',
                    "Successfully applied '"
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
        The user can here pass on commands here
        that will be executed once the mask is
        finished. 

        the command has to be formated as a string
        '''
        self.commands.append(command_str)

        self.log.add_log(
            'info',
            "Added command '"
            +str(command_str)
            +"' to the mask process")

    def remove_command(self, command = '', index = None):
        '''
        Remove a command from the command list. Either
        pass the command in its full or its index
        '''
        if not index == None:
            del self.commands[index]

        elif command in self.commands:
            self.commands.remove(command)

    def purge_commands(self):
        '''
        Remove all commands from the command list. 
        '''
        self.commands = []

    def select_template(self, key = ''):
        '''
        Here we will allow to select the mask that 
        will be kept here until a change is 
        undertaken. 

        Note that this loads the parameters locally
        and that theses can be modified after
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

    # def set_parameters(self, parameters):
    #     '''
    #     Allows the user to inject the parameters of the
    #     mask that he wants to use. It basically sets
    #     self.parameters = parameters
    #     '''   
    #     self.parameters = list(parameters)

    # def process_mask(self, target):
    #     '''
    #     We will use the provided selection and 
    #     parameters to create a mask suited for the 
    #     provided data shape.
    #     '''
    #     ############################################
    #     #test the target
    #     assert len(target.data_objects) > 0,\
    #         "The datastructure is empty, cannot create mask ..."

    #     ############################################
    #     #This assumes that the mask has been set
    #     if  self.selected in self.all_masks.keys():

    #         mask_target = self.all_masks

    #     if  self.selected in self.all_pre_masks.keys():

    #         mask_target = self.all_pre_masks

    #     shape = target.data_objects[0].dim

    #     self.mask = mask_target[self.selected][0](shape,self.parameters)

    #     #run the post masks commands
    #     mask = self.mask
    #     mask = self.run_commands(mask)
    #     self.mask = mask


if __name__ == '__main__':
    masks = Masks()
    masks.addMask('circular at 50 50')
    masks.addElement([
        'arc',
        (31,35), 
        0,
        (0,5), 
        (0,360)])
    masks.addElement([
        'triangle',
        (65,65), 
        0,
        5,5])

    masks.removeElement(0)
    masks.sendToGenerator()
    masks.generateMask(128,128)

    import matplotlib.pyplot as plt
    plt.pcolormesh(masks.mask_gen.mask)
    plt.show()

