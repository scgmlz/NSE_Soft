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


import sys
import io
import numpy as np
import time
from pprint import pprint
import os

class Import_SANS_PAD:

    def __init__(self,load_path, target):
        '''
        This class will simply initiate an run all
        the procedures on construct. 
        '''
        self.verbose    = True
        container       = self.process_input_pad(load_path,target)
        axes            = self.process_pad_axes(container)
        self.fetch_data_pad(container, axes)

    def process_input_pad(self,load_path, target):
        '''
        This function will go through the provided 
        text fill and try to parse the information
        in order to generate a dictionary that will
        be fed back to the data handler
        '''
        #open the file
        f               = open(load_path, "r")
        lines           = f.readlines()
        path            = ""
        dimensions_names= []
        units           = []
        para_array      = []
        ignore_array    = []
        meta_array      = []

        #first read of the lines to find path
        for line in lines:
            if len(line.split("Path : ")) > 1:
                path = line.strip("\n").split("Path : ")[1]

            elif len(line.split("Data : ")) > 1:
                templine = line.strip('\n')
                elements = templine.split(" : ")
                para_array.append([
                    eval(elements[1]),
                    elements[2],
                    elements[3],
                    elements[4]
                    ])

            #grab exclusion        
            elif len(line.split("Ignore : ")) > 1:
                templine = line.strip('\n')
                elements = templine.split(" : ")
                ignore_array.append([int(elements[1]),eval(elements[2]) ])

            #grab the metadata load instructions        
            elif len(line.split("Metadata : ")) > 1:
                templine = line.strip('\n')
                elements = templine.split(" : ")
                meta_array.append([element for element in elements])

            #grab the dimension names     
            elif len(line.split("Dim : ")) > 1:
                templine = line.strip('\n').strip("Dim : ")
                elements = templine.split(" : ")
                dimensions_names = elements

            #grab the units    
            elif len(line.split("Unit : ")) > 1:
                templine = line.strip('\n').strip("Unit : ")
                elements = templine.split(" : ")
                units = elements

        f.close()

        #Return the container
        container = [
            path,
            para_array,
            ignore_array,
            meta_array,
            dimensions_names,
            units, 
            target
            ]

        return container

    def process_pad_axes(self,container):
        '''
        Here the dataclass will be built up with its
        dimesions and corresponding data ...
        '''
        para_array          = container[1]

        #This will condense the parameter axis if 
        # it is multi dimensional
        temp_axis_definition = [
            [0 for i in range(len(para_array))] 
            for j in range(len(para_array[0][0]))]

        real_idx_definition = [
            [0 for i in range(len(para_array))] 
            for j in range(len(para_array[0][0]))]

        real_axis_definition = [
            [] for j in range(len(para_array[0][0]))]

        #loop over and make the temporary axes
        for i in range(len(para_array)):

            for j in range(len(para_array[0][0])):

                temp_axis_definition[j][i] = para_array[i][0][j]

        #run over and make unit axes
        for i in range(len(temp_axis_definition)):

            real_axis_definition[i] = list(set(temp_axis_definition[i]))

        #finally create the index
        for i in range(len(para_array)):

            for j in range(len(para_array[0][0])):

                real_idx_definition[j][i] = real_axis_definition[j].index(temp_axis_definition[j][i])

        #generate the non declared axes
        extra_dim = [
            int(para_array[0][-1].strip("(").strip(")").split("x")[i]) 
            for i in range(len(para_array[0][-1].split("x")))]

        return [temp_axis_definition, real_idx_definition, real_axis_definition, extra_dim]

    def fetch_data_pad(self,container, axes):

        '''
        Here the dataclass will be built up with its
        dimesions and corresponding data ...
        '''
        #unpack the containers
        path                = container[0]
        para_array          = container[1]
        ignore_array        = container[2]
        meta_array          = container[3]
        dimensions_names    = container[4]
        units               = container[5]
        target              = container[6]

        temp_axis_definition    = axes[0]
        real_idx_definition     = axes[1]
        real_axis_definition    = axes[2]    
        extra_dim               = axes[3]

        extra_idx = 0

        for idx_0, real_idx in enumerate(real_idx_definition[0]):
            source = para_array[idx_0]
            path_iter = [
                path
                + str(source[1]) 
                + str(path_string) 
                + ".pad" 
                for path_string in eval(source[2])]

            for idx_1,file_path in enumerate(path_iter):
                f = open(file_path,'rb')
                target.add_metadata_object(self.generate_pad_metadata(f, meta_array))
                dimensionality = [
                    int(source[-1].strip("(").strip(")").split("x")[i]) 
                    for i in range(len(source[-1].split("x")))]
                loadeddata = np.fromfile(f, dtype=np.int32)[:np.prod(dimensionality)]
                data = loadeddata.reshape(*dimensionality)
                f.close()
                target[real_idx,idx_1] = data
                extra_idx +=1

        target.sum_in_order(increment = 2)
        target.validate()

        #grab the axis names
        for idx, name in enumerate(dimensions_names):
            try:
                target.axes.set_name(idx,name)
                target.axes.set_unit(idx,units[idx])
                target.axes.set_axis(idx,[element for element in real_axis_definition[idx]])
            except:
                pass

        #fill the datastructure's own metadata
        target.metadata_class.add_metadata('Creation date', value = str(time.ctime()), logical_type = 'str')
        target.metadata_class.add_metadata('Source format', value = "PAD files", logical_type = 'str')
        target.metadata_class.add_metadata('Measurement type', value = "SANS", logical_type = 'float')

    def generate_pad_metadata(self,f,meta_array):
        '''
        Here is the routine managing the metadata 
        handling.
        '''
        metadata = {}
        Lines = f.readlines()
        for i, binaryLine in enumerate(Lines):
            try:
                line = binaryLine.decode('ascii').replace('\n','')
                for element in meta_array:
                    if len(line.split(element[1]+' :')) > 1:      
                        if not element[-2] == 1:
                            value = str(float(line.split(element[1]+' : ')[1].split(element[-1])[0])*float(element[-2]))
                        else:
                            value = line.split(element[1]+' : ')[1].split(element[-1])[0]
                        metadata[element[2]] = [
                            element[2],
                            element[3],
                            value,
                            element[4]
                            ]
            except:
                pass
        f.seek(0)
        return metadata