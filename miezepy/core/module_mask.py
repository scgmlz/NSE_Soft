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
        self.mask_types = [
            'Rectangle',
            'Pie',
            'Triangle',
            'Ellipse']
        self.current_mask = None

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

    def removeMask(self, name):
        '''
        Add a mask to the dictionary
        '''
        del self.mask_dict[name]

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
        mask_dict = {}
            # 'DB_5': [{
            #     'Name':'Pie',
            #     'Position' :[31,35],
            #     'Angle':0,
            #     'Radial range': [0,5], 
            #     'Angular range': [0,360]}],
            # 'Tile': [{
            #     'Name':'Rectangle',
            #     'Position' :[31,35],
            #     'Angle':0,
            #     'Dimensions': [10,10]},
            #     {
            #     'Name':'Arc',
            #     'Position' :[31,35],
            #     'Angle':0,
            #     'Radial range': [0,5], 
            #     'Angular range': [0,360]}]}

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
