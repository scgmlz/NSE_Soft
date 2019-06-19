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

class MaskStructure:

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
        # self.defaults   = [key for key in self.mask_dict.keys()]
        self.mask_types = [
            'Rectangle',
            'Arc',
            'Triangle',
            'Linear composition',
            'Radial composition']
        self.setMask('DB_5')

    def __str__(self):
        '''
        set out the dictionary of the current mask
        ''' 
        output = '############################\n'
        output += 'Mask name: '+self.current_mask+'\n'
        output +=  json.dumps(self.mask_dict[self.current_mask])+'\n'
        output += '############################\n'
        return output

    def grabFromOther(self, other):
        '''
        This method is to allow cross 
        environnement transfer of the 
        elements.

        Parameters
        ----------
        other : ScriptStructure
            The script structure to use
        '''
        self.mask_dict.update(other.mask_dict)
        for key in other.mask_dict.keys():
            if key not in self.mask_dict.keys():
                self.mask_dict[key] = list(other.mask_dict[key])

    def setMask(self, name):
        '''
        Set the mask present in the dictionary
        '''
        if name in self.mask_dict.keys():
            self.current_mask = name
            self.sendToGenerator()
        else:
            print('Mask does not exist')
        
    def addMask(self, name):
        '''
        Add a mask to the dictionary
        '''
        if name in self.mask_dict.keys():
            found_slot = False
            idx = 0
            while not found_slot:
                if not name +'_'+ str(idx) in self.mask_dict.keys():
                    found_slot = True
                    name = name +'_'+ str(idx)
                else:
                    idx += 1
        self.mask_dict[name] = []
        self.setMask(name)
        return name

    def addElement(self, values, name = None):
        '''
        Add a mask element to the mask
        values should be a list of 
        properties like the defaults.
        '''
        if name == None:
            name = self.current_mask

        self.mask_dict[name].append(dict(values))

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
        self.mask_gen.grabMask(
            self.mask_dict[self.current_mask], recreate = recreate)

    def generateMask(self, size_x, size_y):
        '''
        Generate the masks of the generator
        '''
        self.mask_gen.generateMask(size_x,size_y)
        self.mask = self.mask_gen.mask.astype(np.int16)

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
        self.checkMasks()
        
    def loadAllMasks(self, path):
        '''
        Writes a mask to json
        '''
        f = open(path, 'r')
        self.mask_dict = json.load(f)
        f.close()
        self.checkMasks()

    def checkMasks(self):
        '''
        The nomenclature has changed slightly and
        a small fix is implemented here
        '''
        pass
        # for key in self.mask_dict.keys():
        #     for element in self.mask_dict[key]:
        #         if element[0] == 'radial_comp' or element[0] == 'radial composition':
        #             element[0] = 'Radial composition'
        #             if element[7][0] == 'square':
        #                 element[7][0] = 'rectangle'    
        #         elif element[0] == 'linear_comp':
        #             element[0] = 'linear composition'
        #             if element[7][0] == 'square':
        #                 element[7][0] = 'rectangle'  
        #         elif element[0] == 'square':
        #             element[0] = 'rectangle'

    def generateDefaults(self):
        '''
        Will load all the mask templates locally
        '''
        mask_dict = {
            'DB_5': [{
                'Name':'Arc',
                'Position' :[31,35],
                'Angle':0,
                'Radial range': [0,5], 
                'Angular range': [0,360]}],
            'Tile': [{
                'Name':'Rectangle',
                'Position' :[31,35],
                'Angle':0,
                'Dimensions': [10,10]},
                {
                'Name':'Arc',
                'Position' :[31,35],
                'Angle':0,
                'Radial range': [0,5], 
                'Angular range': [0,360]}]}#,
            # '10x10_tile': [{
            #     'rectangle',
            #     (100,100),
            #     0,
            #     10,10]],
            # 'SkX_peak': [{
            #     'Name': 'Arc',
            #     (31,35),
            #     0, 
            #     (55,100), 
            #     (8,46)]],
            # 'SkX_peak_circ': [{
            #     'Name': 'Arc',
            #     (100,70),
            #     0, 
            #     (0,20), 
            #     (0,360)]],
            # 'SkX_peak_small': [{
            #     'Name': 'Arc',
            #     (31,35),
            #     0, 
            #     (72,82), 
            #     (22,32)]],
            # 'SkX_between_peaks': [{
            #     'Name': 'Arc',
            #     (31,35),
            #     0, 
            #     (55,100), 
            #     (46,70)]],
            # 'noDB': [[
            #     'Name': 'Arc',
            #     (31,35),
            #     0, 
            #     (55,100), 
            #     (0,360)]],
            # 'DB_sixfold': [{
            #     'Name': 'Arc',
            #     (27,33),
            #     0, 
            #     (0,5), 
            #     (0,360)]],
            # 'SkX_peak_Sixfold': [{
            #     'Name': 'Arc',
            #     (27,33),
            #     0, 
            #     (47,90), 
            #     (15,52)]],
            # 'SkX_between_peaks_Sixfold': [{
            #     'Name': 'Arc',
            #     (27,33),
            #     0,
            #     (47,90), 
            #     (52,80)]],
            # 'noDB_Sixfold': [{
            #     'Name': 'Arc',
            #     (31,35),
            #     0, 
            #     (42,100), 
            #     (0,360)]],
            # 'SkX_peak_circ_Sixfold': [[
            #     'Name': 'Arc',
            #     (84,69),
            #     0, 
            #     (0,20), 
            #     (0,360)]],
            # 'SkX_peak_SkXCon': [[
            #     'Name': 'Arc',
            #     (28,34),
            #     0, 
            #     (65,85), 
            #     (82,100)]],
            # 'Pre_SkX_peak': [[
            #     'radial composition',
            #     (31,31),
            #     0,
            #     15,13,
            #     [57, 102], 
            #     [11, 50], 
            #     [
            #         'Name': 'Arc', 
            #         [0,0],
            #         0,
            #         [0,10],
            #         [0,10], 
            #         [True, True, False]
            #     ]]],

            # 'Pre_SkX_peak_Sixfold': [[
            #     'radial composition',
            #     (43,40),
            #     -21,
            #     3,3,
            #     [45, 69], 
            #     [39, 58], 
            #     [
            #         'Name': 'Arc', 
            #         [0,0],
            #         0,
            #         [0,10],
            #         [0,10], 
            #         [True, True, False]
            #     ]]],

            # 'Pre_SkX_peak_SkXCon': [[
            #     'radial composition',
            #     (28,34),
            #     0,
            #     10,11,
            #     [65, 85], 
            #     [80, 104], 
            #     [
            #         'Name': 'Arc', 
            #         [0,0],
            #         0,
            #         [0,10],
            #         [0,10], 
            #         [True, True, False]
            #     ]]],

            # 'Pre_tile': [[
            #     'linear composition',
            #     (0,0),
            #     0, 
            #     5,5,
            #     128,128,
            #     [
            #         'rectangle', 
            #         [0,0],
            #         0,
            #         10,10,
            #         [True, True, False]
            #     ]]],
            # }

        return mask_dict

    def runCommands(self, mask):
        '''
        The user can here pass on commands and then 
        execute them after the mask has been set. 
        '''
        for command in self.commands:
            try:
                exec(command)

            except:
                pass

        return mask

    def addCommand(self, command_str = ''):
        '''
        The user can here pass on commands here
        that will be executed once the mask is
        finished. 

        the command has to be formated as a string
        '''
        self.commands.append(command_str)

    def removeCommand(self, command = '', index = None):
        '''
        Remove a command from the command list. Either
        pass the command in its full or its index
        '''
        if not index == None:
            del self.commands[index]

        elif command in self.commands:
            self.commands.remove(command)

    def purgeCommands(self):
        '''
        Remove all commands from the command list. 
        '''
        self.commands = []
