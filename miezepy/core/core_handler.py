
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
import sys  
import numpy as np
import os
import logging
import glob

#############################
#import child components
from .io            import IO_Manager
from .environment   import Environment 

def setEnv(handler):
    return None


class Handler:

    def __init__(self, parent = None):
        self.parent = parent
        self.reset()
        self.info_string = ''
        self.info_val    = 0

    def reset(self):
        '''
        This will genrate the dictionary for the 
        loaded data and link the other core classes
        '''
        self.env_array  = []

    def new_environment(self, title = 'No_Name', select = 'MIEZE'):
        '''
        This function will automise the environment
        creation for the user.
        '''
        title_present = True
        names = [env.name for env in self.env_array]
        while title_present:
            if title in names:
                title = title + "_bis"
            else:
                title_present = False

        self.env_array.append(Environment(self, title = title, select = select))
        self.set_current_env(title)

        return self.env_array[-1]

    def set_current_env(self, key = None, idx = None):
        '''
        This function sets the current data
        with the right key
        '''
        if not idx == None:
            self.current_env        = self.env_array[idx]
            self.current_env_key    = self.current_env.name

        else:
            names = [env.name for env in self.env_array]

            if not key == None:
                if key in names:
                    self.current_env_key    = key
                    self.current_env        = self.env_array[names.index(key)]
                    return self.current_env

                else:
                    print("\nERROR: The key '"+str(key)+"' you have provided is not present as an environment...\n")

    def getEnv(self,key = None):
        names = [env.name for env in self.env_array]
        if not key == None:
            if key in names:
                return self.env_array[names.index(key)]
            else:
                print('This env does not exist')


    def saveSession(self, path, data_bool = True, mask_bool = False, script_bool = False):
        '''
        Save the session to be loaded again later on
        '''
        names = [env.name for env in self.env_array]
        for key in names:
            env_dir = os.path.join(path,self.env_array[names.index(key)].name)
            if not os.path.exists(env_dir):
                os.makedirs(env_dir)
            self.env_array[names.index(key)].saveToPy(os.path.join(env_dir,"env_def.py"))

            if data_bool:
                data_dir = os.path.join(env_dir,"data")
                if not os.path.exists(data_dir):
                    os.makedirs(data_dir)
                self.env_array[names.index(key)].io.saveToPython(
                    os.path.join(data_dir,key+"_data.py")
                )

            if mask_bool:
                mask_dir = os.path.join(env_dir,"mask")
                if not os.path.exists(mask_dir):
                    os.makedirs(mask_dir)
                self.env_array[names.index(key)].mask.saveAllMasks(
                    os.path.join(mask_dir,key+"_mask.txt")
                )

            if script_bool:
                data_dir = os.path.join(env_dir,"script")
                if not os.path.exists(data_dir):
                    os.makedirs(data_dir)
                self.env_array[names.index(key)].process.saveScripts(
                    os.path.join(data_dir,key+"_script.py"),
                    self.env_array[names.index(key)].process.editable_scripts
                )
    
    def prepSessionLoad(self, path, data_bool = True, mask_bool = True, script_bool = True, folder_list = []):
        '''
        Prepare the eventual load of a session.
        '''
        env_file_list = [
            element for element in glob.iglob(os.path.join(
                path,'**','*env_def.py'), recursive=True)]

        data_folder_list    = [None]*len(env_file_list)
        mask_folder_list    = [None]*len(env_file_list)
        script_folder_list  = [None]*len(env_file_list)

        for i,env_folder in enumerate([os.path.dirname(element) for element in env_file_list]):
            data_list = [
                element for element in glob.iglob(os.path.join(
                    env_folder,'**','*_data.py'), recursive=True)]
            mask_list = [
                element for element in glob.iglob(os.path.join(
                    env_folder,'**','*_mask.txt'), recursive=True)]
            script_list = [
                element for element in glob.iglob(os.path.join(
                    env_folder,'**','*_script.py'), recursive=True)]

            if len(data_list) > 0 and data_bool:
                data_folder_list[i]     = data_list[0]
            if len(mask_list) > 0 and mask_bool:
                mask_folder_list[i]     = mask_list[0]
            if len(script_list) > 0 and script_bool:
                script_folder_list[i]   = script_list[0]

        self.prep_load_list = [
            env_file_list,
            data_folder_list,
            mask_folder_list,
            script_folder_list,
            folder_list]

        return self.prep_load_list

    def sessionLoad(self, add_bool, main_window = None):
        '''
        Prepare the eventual load of a session.
        '''
        data_load_output    = []
        script_load_output  = []
        mask_load_output    = []

        if not add_bool:
            self.reset()

        for i, path in enumerate(self.prep_load_list[0]):
            if not main_window == None:
                main_window.setProgress('Setting env '+str(i),i)

            with open(path) as f:
                code = compile(f.read(), path, 'exec')
                exec(code,globals())

            env = setEnv(self)

            if not self.prep_load_list[1][i] == None:
                if not main_window == None:
                    main_window.setProgress(
                        'Loading data '+str(i),
                        i)
                data_load_output.append([
                    env.io.loadFromPython(
                        self.prep_load_list[1][i],
                        extra_folder = self.prep_load_list[4]),
                    self.prep_load_list[1][i]])
            
            if not self.prep_load_list[2][i] == None:
                if not main_window == None:
                    main_window.setProgress(
                        'Setting mask '+str(i),
                        i)
                env.mask.loadAllMasks(self.prep_load_list[2][i])

            if not self.prep_load_list[3][i] == None:
                if not main_window == None:
                    main_window.setProgress(
                        'Setting script '+str(i),
                        i)
                env.process.loadScripts(self.prep_load_list[3][i])

        return [data_load_output, mask_load_output, script_load_output]