
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
import os
import glob

#############################
#import child components
from .module_environment    import Environment 
from .library_logic         import generateSingleName

def setEnv(handler):
    return None

class CoreHandler:
    '''
    In version 0.1.1 it became evident, that the core needs a
    major rework to allow a cleaner interfacing and functionality
    This will include more interfacing with Qt signaling as well
    ass clearer separation of both worker classes and the function
    libraries which are at the present point non existent.

    Furthermore a lot more testing coverage is required as well 
    as the possibility to manage environnement on different
    threads.
    '''

    def __init__(self):
        '''
        Initializing the core handler class without 
        any link to the the main objects. 
        '''
        self.reset()

    def reset(self):
        '''
        This will genrate the dictionary for the 
        loaded data and link the other core classes
        '''
        self.env_array  = []

    def addEnv(self, title = 'No_Name', select = 'MIEZE'):
        '''
        This function will automise the environment
        creation for the user.

        Parameters
        ----------
        title : str
            The string we are trying to set

        select: str
            The type of measurement the user whished to load

        Returns
        -------
        Environnement : python class
            Returns the environnement
        '''
        title_list  = [env.name for env in self.env_array]
        title       = generateSingleName(title, title_list)
        
        self.env_array.append(Environment(self, title, select = select))
        self.setCurrentEnv(title)

        return self.env_array[-1]

    def delEnv(self, key = None, idx = None):
        '''
        This function deletes the chosen environnement either
        through the key or through the idx (int)

        Parameters
        ----------
        key (optional) : str
            The string we are trying to set

        idx (optional): int
            Index of the environnement in the array
        '''
        if not idx == None:
            del self.env_array[idx]
            self.setCurrentEnv(idx = idx - 1)

        elif not key == None:
            names = [env.name for env in self.env_array]

            if key in names:
                idx = names.index(key)
                del self.env_array[idx]
                self.setCurrentEnv(idx = idx - 1)

            else:
                print("\nERROR: The key '"+str(key)+"' you have provided is not present as an environment...\n")
        
    def setCurrentEnv(self, key = None, idx = None):
        '''
        This function sets the current data
        with the right key

        Parameters
        ----------
        key (optional) : str
            The string we are trying to set

        idx (optional): int
            Index of the environnement in the array
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

    def getIdx(self, name):
        '''
        Return the current index of the environnement

        Parameters
        ----------
        name : str
            The string we are trying to set
        '''
        return [env.name for env in self.env_array].index(name)

    def getEnv(self,key):
        '''
        This function will allow the user to request
        an environnement specified by its key. Similar
        to the setCurrentEnv method and might be 
        refactored.

        Parameters
        ----------
        key : str
            The string we are trying to set

        Returns
        -------
        Environnement : python class
            Returns the environnement
        '''
        names = [env.name for env in self.env_array]
        if not key == None:
            if key in names:
                return self.env_array[names.index(key)]
            else:
                print('This env does not exist')

    def processOperation(self, from_env, perform, to_env):
        '''
        This method is here to allow transfer of items
        from one environnement to another

        Parameters
        ----------
        from_env : Environnement
            The source environnement
        to_env : Environnement
            The source environnement
        perform : str
            The identifier of the action to perform
        '''
        from_env    = self.getEnv(from_env)
        to_env      = self.getEnv(to_env)
        perform     = perform

        if perform == 'data':
            to_env.io.grabFromOther(from_env.io)
        elif perform == 'mask':
            to_env.mask.grabFromOther(from_env.mask)
        elif perform == 'scripts':
            to_env.scripts.grabFromOther(from_env.scripts)
        else:
            print('Not implemented')


    # TO-DO: test of save
    def saveSession(self, path, data_bool = True, mask_bool = False, script_bool = False):
        '''
        This is the general session saver that tells all
        savers to launch and perform their task.

        Parameters
        ----------
        path : str
            The path in which all will be saved

        data_bool (optional): bool
            Shall we save the data

        mask_bool (optional): bool
            Shall we save the masks

        script_bool (optional): bool
            Shall we save the scripts
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
                self.env_array[names.index(key)].scripts.saveScripts(
                    os.path.join(data_dir,key+"_script.py"))
    
    # TO-DO: test of load
    def prepSessionLoad(self, path, data_bool = True, mask_bool = True, script_bool = True, folder_list = []):
        '''
        In this routine we will prepare the load of a session. This is the
        work that has to be prepared before: sessionLoad

        Parameters
        ----------
        path : str
            The path in which all will be saved

        data_bool (optional): bool
            Shall we save the data

        mask_bool (optional): bool
            Shall we save the masks

        script_bool (optional): bool
            Shall we save the scripts

        folder_list : [str]
            List of strings that will contain additional folders
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

    # TO-DO: test of load
    def sessionLoad(self, add_bool, main_window = None):
        '''
        Proceed with the load after the parameters have been set
        in self.prep_load_list through the prepSessionLoad()
        method

        Parameters
        ----------
        add_bool : bool
            Shall we reset the env_array

        main_window (optional): QMainWindow
            The mainwindow for reporting

        Returns
        -------
        outputs : misc.
            ist of the load failures encountered
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
                temp = f.read()
                temp = temp.replace('.new_environment(', '.addEnv(')
                code = compile(temp, path, 'exec')
                exec(code,globals())

            #the setEnv method is overwritten in the load file
            env = setEnv(self)
            if not self.prep_load_list[1][i] == None:
                if not main_window == None:
                    main_window.setProgress('Loading data '+str(i),i)
                data_load_output.append([
                    env.io.loadFromPython(
                        self.prep_load_list[1][i],
                        extra_folder = self.prep_load_list[4]),
                    self.prep_load_list[1][i]])
            
            if not self.prep_load_list[2][i] == None:
                if not main_window == None:
                    main_window.setProgress('Setting mask '+str(i),i)
                env.mask.loadAllMasks(self.prep_load_list[2][i])

            if not self.prep_load_list[3][i] == None:
                if not main_window == None:
                    main_window.setProgress('Setting script '+str(i),i)
                env.scripts.loadScripts(self.prep_load_list[3][i])

        return [data_load_output, mask_load_output, script_load_output]
