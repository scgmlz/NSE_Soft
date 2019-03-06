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
import numpy as np
import sys
import copy

#############################
#import child components
from .module_log import LogHandler

class DataStructure:
    '''
    This class we be the main building block of 
    the loaded data. It is written to survive any
    dimensionality ... 
    '''
    def __init__(self):
        '''
        This is the class constructor. Here we will 
        initialise the main datastructure elements. 

        set add_meta_auto to true to allow the data
        class to link automatically the data_object
        to the last created metadat instance. 
        '''
        #start local variables
        self.id                 = 0
        self.meta_id            = 0
        self.data_objects       = []
        self.data_addresses     = []
        self.metadata_objects   = []
        self.metadata_addresses = []
        self.map                = None
        self.slices             = {}
        self.generated          = False
        self.axes               = None

        #logical variables
        self.add_meta_auto = True

        #own metadata
        self.metadata_class = Metadata(0)
        self.metadata = self.metadata_class.metadata

        #set up the log
        self.log = LogHandler()

    def __str__(self):
        '''
        Generate a string output for the user to 
        see that the dataclass has initialized 
        properly.
        '''
        output ="\n##########################################################\n"
        output += "################## DATA STRUCTURE ########################\n"
        output += "##########################################################\n"
        output += "The datastructure currently consists of:\n"
        output += "- Number of elements: "+str(len(self.data_objects))+"\n"
        try:
            output += "- Number of dimensions: "+str(self.axes.dim)+"\n"
            output += "- The axes names are: "+str(self.axes.names)+"\n"
            output += "- The axes units are: "+str(self.axes.units)+"\n"
            output += "- The axes lengths are: "+str(self.axes.axes_len)+"\n"
            output += "- The base structure is: "+str(self.data_objects[0].type)+"\n"
            output += "- The base structure dim is: "+str(self.data_objects[0].dim)+"\n"
        except:
            output += "- No Axes defined\n"

        output += "- The metadata addition is set to: "+str(self.add_meta_auto)+"\n"
        output += "----------------------------------------------------------\n"
        if not len(self.metadata) == 0:            
            for key,row in self.metadata.items():
                output +=  row[0]+": "+row[2]+"\n"
        else:
            output += "- No Metadata defined\n"
        output += "##########################################################\n\n"

        #send it also out to the log
        self.log.add_log('info', output)

        return output

    def __setitem__(self, index, value):
        '''
        This is the classmethod __setitem__. It allows
        to set an element of the class through the 
        use of data_structure[index] = value.
        Input: 
        - index (int array) position if the element
        - value (data_object)
        '''
        self.addDataObject(value, index)

    def __getitem__(self, index):
        '''
        This is the classmethod __getitem__. It allows
        to retrieve an element of the data_structure
        at a position index. In the present case
        multiple options are available...

        - index = 'all' returns self as a copy
        - index = integer array returns data of data_object
        - index = integer array with slices inside 
                    returns a new datastructure with the
                    corresponding elements. 
        Input: 
        - index (int/slice array) position if the elements
        '''
        #process input
        if isinstance(index,int):
            id_array = self.axes.get_id_for_index([index])
        else:
            id_array = self.axes.get_id_for_index(index)
            
        if len(id_array) == 0:
            return False
        elif len(id_array) == 1: 
            return self.data_objects[self.get_pos_from_id(id_array[0])].data
        else:
            return self.process_reduction(index, id_array)

    def get_metadata(self, index):
        '''
        This function is to grab the exact element
        in the data objects. it is not error proof
        and assumes that the user knows what he is
        si doing...
        '''
        data_object = self.data_objects[
            self.data_addresses.index(
                self.map.__getitem__(tuple(index)))]
        metadata_array = [
            self.metadata_objects[self.metadata_addresses.index(data_object.meta_address[i])]
            for i in range(len(data_object.meta_address))
        ]

        return metadata_array

    def validate(self):
        '''
        If all data objects have been loaded the 
        structure can be validated to perform all the 
        side operations
        '''
        self.sanityCheck()
        self.delete_all_slices()
        self.generate_axes()
        self.createMap()
        self.generated = True

    def sanityCheck(self):
        '''
        While the suer can indeed incorporate any type
        of data with any type of dimensionally there
        still needs to be a coherence amongst them.

        In this function we will run through the 
        objects and check that they are all represented
        in the same dimensionality.
        '''
        dimensionality = len(self.data_objects[0].index)

        for element in self.data_objects:

            if not dimensionality == len(element.index):

                return False
        
        return True
    
    def addDataObject(self, data, index):
        '''
        here we instruct the Data_structure to add a
        data element. Note that this results in the
        creation of an element located at in the 
        data_objects array. 

        the data address allows to quickly access the 
        object through its id
        Input: 
        - data (data)
        - index (int array)
        '''
        self.data_objects.append(Data_Object(self.id, data, index))
        self.data_addresses.append(self.id)

        if self.add_meta_auto and not len(self.metadata_objects) < 1 :
            self.data_objects[-1].meta_address.append(self.metadata_objects[-1].meta_id)
            self.metadata_objects[-1].links.append(self.id)
        self.id += 1

    def addMetadataObject(self,dictionary):
        '''
        Here we have a routine which will add an
        element to the metadata and then process 
        indices
        Input: 
        - dictionary (dict)
        '''
        self.metadata_objects.append(Metadata(self.meta_id, dictionary))
        self.metadata_addresses.append(self.meta_id)
        self.meta_id += 1

    def inject_data_object(self, data_object):
        '''
        if the element is already formated as data_
        object we can immediately reference it
        Input: 
        - data_object (data_object)
        '''
        self.data_objects.append(copy.deepcopy(data_object))
        self.data_objects[-1].id = self.id 
        self.data_addresses.append(self.id)
        self.id += 1

    def inject_metadata_object(self, metadata_object):
        '''
        if the element is already formated as metadata_
        object we can immediately reference it
        Input: 
        - meatdata (Metadata)
        '''
        self.metadata_objects.append(copy.deepcopy(metadata_object))
        self.metadata_objects[-1].meta_id = self.meta_id
        self.metadata_addresses.append(self.meta_id)
        self.meta_id += 1

    def get_metadata_object(self, address):
        '''
        Returns the proper metadata object for a given
        address
        Input: 
        - address (int)
        Output: 
        - metadata object (Metadata)
        '''
        return self.metadata_objects[self.metadata_addresses.index(address)]

    def createMap(self):
        '''
        This will create an axes class that will
        generate the axes according to the loaded data.
        A pointer to the array listing the data is 
        given.
        '''
        self.map = np.zeros(self.axes.axes_len, dtype = 'int64') -1
        for data_object in self.data_objects:
            self.map.__setitem__(tuple(data_object.index),data_object.id)

    def returnAsNumpy(self):
        '''
        return numpy array of the entire data...
        note that this is done to allow performance
        improvements and does therefore not follow
        the practicality of the dataclass
        the ordering will follow the map scheme
        '''
        #evaluate total dimensionality
        dimensionality = self.axes.axes_len + list(self.data_objects[0].dim)

        #create the out matrix
        numpy_out = np.zeros(
            tuple(dimensionality), 
            dtype = str(np.asarray(self.data_objects[0].data.dtype)))
        extra_index = [slice(0,None,1) for i in list(self.data_objects[0].dim)]
        for data_object in self.data_objects:
            index = list(data_object.index) + extra_index
            numpy_out.__setitem__(
                tuple(index),
                data_object.data.__getitem__(tuple(extra_index)) )

        return numpy_out

    def bufferAsNumpy(self):
        '''
        return numpy array of the entire data...
        note that this is done to allow performance
        improvements and does therefore not follow
        the practicality of the dataclass
        the ordering will follow the map scheme
        '''
        self.bufferedData = self.returnAsNumpy()

    def generate_axes(self):
        '''
        This will create an axes class that will
        generate the axes according to the loaded data.
        A pointer to the array listing the data is 
        '''
        if self.sanityCheck():
            self.axes = Axes(self)
        else:
            print("Data sanity check failed")

    def get_pos_from_id(self,idx):
        '''
        In this method we will locate the position of
        the element through the Id array
        '''
        return self.data_addresses.index(idx)

    def get_pos_from_meta_id(self,id):
        '''
        In this method we will locate the position of
        the element through the Id array
        Input: 
        - id (int)
        Output: 
        - metadata (Metadata)
        '''
        return self.metadata_addresses.index(id)

    def add_slice(self,array, data_structure):
        '''
        This method will allow the user to generate 
        slices in advance to speed up the process. 
        This will allow that a repeated operation is
        not going to tax the ressources to much.
        Some major operation on the dataset will 
        obviously reset the slices. 
        ———————
        Input: 
        - 
        ———————
        Output: 
        - datastructure
        ———————
        status: active
        '''
        self.slices[repr(array)] = data_structure

    def delete_all_slices(self):
        '''
        This method will allow the user to generate 
        slices in advance to speed up the process. 
        This will allow that a repeated operation is
        not going to tax the ressources to much.
        Some major operation on the dataset will 
        obviously reset the slices. 
        Output: 
        - datastructure
        '''
        pointer = [key for key in self.slices.keys()]
        for key in pointer:
            del self.slices[key]

    def get_slice(self,array):
        '''
        Similar to __getitem__ but with actual values
        Input: 
        - *args are values determining an index position
          '-' will be replaced by a slice type 
          interpretation. so will missing elements
        Output: 
        - datastructure
        '''
        #first check if it is already in the slice dictionary
        if repr(array) in self.slices.keys():
            return self.slices[repr(array)]

        #or create it 
        index = []
        for i in range(self.axes.dim): 
            try:
                index.append(self.axes.get_position(array[i],i))
            except:
                index.append('-')
        id_array = self.axes.get_id_for_index(index)
        if len(id_array) == 0:
            return False
        else:
            self.add_slice(array, self.process_reduction(index, id_array))
            return self.slices[repr(array)]

    def process_reduction(self,index, id_array):
        '''
        We will initialise the structure and
        construct it with the right parameters
        ———————
        Input: 
        - array of integers pointing to locations
        ———————
        Output: 
        - datastructure with the reduced data
        '''

        #send it also out to the log
        self.log.add_log(
            'info', 
            'Trying to process a reduction of the datastructure')

        ##############################################
        #create the new structure
        new_data = Data_Structure()
        self.log.add_log(
            'info', 
            'Successfully created the new structure')
            
        for idx in id_array:
            new_data.inject_data_object(self.data_objects[self.get_pos_from_id(idx)])
        self.log.add_log(
            'info', 
            'Successfully injected the data_objects')

        #create the reduction boolean mask
        mask = [isinstance(element, int) for element in index]

        #apply the mask
        for data_object in new_data.data_objects:
            new_index = []
            for i in range(len(index)):
                if not mask[i]:
                    new_index.append(int(data_object.index[i]))
            data_object.index = list(new_index)
        self.log.add_log(
            'info', 
            'Successfully processed the necessary axis reductions')

        #validate the structure
        new_data.validate()

        ##############################################
        ##############################################
        #transfer the axis information
        new_idx = 0
        for i in range(len(index)):
            if not mask[i]:
                new_data.axes.names[new_idx] = copy.deepcopy(self.axes.names[i])
                new_data.axes.units[new_idx] = copy.deepcopy(self.axes.units[i])
                new_data.axes.axes[new_idx]  = copy.deepcopy(self.axes.axes[i])
                #perform minor surgery
                for i in range(len(new_data.axes.idx[new_idx]) , len(self.axes.idx[i])):
                    new_data.axes.idx[new_idx].append([])
                new_idx +=1
        self.log.add_log(
            'info', 
            'Successfully fixed axis informations')

        ##############################################
        ##############################################
        #transfer the metadata 
        metadata_idx = []
        for data_object in new_data.data_objects:
            for element in data_object.meta_address:
                metadata_idx.append(element)

        #copy the right elements
        metadata_idx_sorted = list(set(metadata_idx))
        for idx in metadata_idx_sorted:
            new_data.inject_metadata_object(
                self.metadata_objects[self.get_pos_from_meta_id(idx)])

        #rebuild the right id links in the data_objects
        for data_object in new_data.data_objects:
            for i in range(len(data_object.meta_address)):
                data_object.meta_address[i] = new_data.metadata_addresses[
                    metadata_idx_sorted.index(
                        data_object.meta_address[i])]

        #erase and rebuild links
        for metadata_object in new_data.metadata_objects:
            metadata_object.links = []
        for data_object in new_data.data_objects:
            for element in data_object.meta_address:
                new_data.metadata_objects[
                    new_data.get_pos_from_meta_id(element)].links.append(
                        int(data_object.id))
        
        #the local metadata
        new_data.metadata_class = copy.deepcopy(self.metadata_class)
        new_data.metadata = new_data.metadata_class.metadata
        #send it also out to the log
        self.log.add_log(
            'info', 
            'Successfully fixed metadata informations')

        ##############################################
        ##############################################
        #transfer the axis information
        new_data.clean()
        #send it also out to the log
        self.log.add_log(
            'info', 
            'returning new structure')
        return new_data

    def remove_from_axis(self, idx, array):
        '''
        This function will perform the deletion of 
        objects. more specifically an axis is given
        and then the axis points to delete are 
        marked in the array by 0
        Input:
        - idx is the axis idx (int)
        - array is the array of elements to delete
        '''
        new_data        = copy.deepcopy(self)
        remove_array    = new_data.axes.prepare_remove(idx, array)

        for element in remove_array:
            new_data.remove_data(element)
            new_data.unlink_metadata(element)
            new_data.axes.remove_from_axes(element)

        new_data.clean_metadata()
        equivalence = new_data.axes.clean_axes()
        new_data.clean_data(equivalence)

        new_data.create_map()
        self.log.add_log(
            'info', 
            'Successfully removed points from axis')
        self.log.add_log(
            'info', 
            'Returning result')
        return new_data
    
    def remove_data(self, idx):
        '''
        remove a single element from the data
        structure through the use of its unique ID
        Input:
        - data_object unique identifier (int)
        '''
        index = self.data_addresses.index(idx)

        del(self.data_objects[index])
        del(self.data_addresses[index])

    def unlink_metadata(self, idx):
        '''
        Remove the links in the metadata objects. 
        metadata objects which are orphaned will later
        be cleaned
        Input:
        - data_object unique identifier (int)
        '''
        for metadata_object in self.metadata_objects:
            if idx in metadata_object.links:
                index = metadata_object.links.index(idx)
                del(metadata_object.links[index])
        
    def clean_metadata(self):
        '''
        This function will go through the metadata and
        mark which ones to delete the 
        '''
        orphaned = []

        for metadata_object in self.metadata_objects:
            if len(metadata_object.links) == 0:
                orphaned.append(metadata_object.meta_id)

        for idx in orphaned:
            if idx in self.metadata_addresses:
                index = self.metadata_addresses.index(idx)
                del(self.metadata_objects[index])
                del(self.metadata_addresses[index])

    def clean_data(self, equivalence):
        '''
        This function will repair the indices in the 
        data_objects to match the restructured indices
        '''
        for data_object in self.data_objects:

            for i in range(len(data_object.index)):

                data_object.index[i] = equivalence[i].index(data_object.index[i])

    def sum_in_order(self, increment = 2, sum_metadata = True):
        '''
        This function will run through the data and 
        sum data objects with an increment. Note that
        the metadata can be summed by setting
        sum_metadata = True.

        Note that this logic assumes that the elements
        to be summed are folowing each other. This has
        to be done before the validation.
        '''
        #current length of the objects array
        current_data_length = len(self.data_objects)

        #create the new data_objects
        for idx_0 in range(0,current_data_length, increment):
            summed_object = self.data_objects[idx_0]
            for idx_1 in range(1, increment):
                summed_object += self.data_objects[idx_0 + idx_1]
            self.inject_data_object(summed_object)

        #send it also out to the log
        self.log.add_log(
            'info', 
            'Sucessfully summed the data with increment '
            +str(increment))

        #current length of the objects array
        if sum_metadata:
            for element in self.data_objects[current_data_length:]:
                new_meta = self.sum_metadata(element)
                new_meta.links = [element.id]
                self.inject_metadata_object(new_meta)
                element.meta_address = [self.metadata_objects[-1].meta_id]
                self.log.add_log(
                    'info', 
                    'Successfully summed the metadata with increment '
                    +str(increment))

        self.validate()

        #proceed to cleanup
        purge_list = [
            element.id 
            for element in self.data_objects[:current_data_length]]

        for element in purge_list:
            self.remove_data(element)
            self.unlink_metadata(element)
            self.axes.remove_from_axes(element)

        self.clean()

        self.log.add_log(
            'info', 
            'Successfully cleaned up after summation')

    def clean(self):
        '''
        Will process the cleaning mechanisms.
        '''
        self.clean_metadata()
        equivalence = self.axes.clean_axes()
        self.clean_data(equivalence)
        self.create_map()

    def sum_metadata(self,data_object):
        '''
        This function will sum the metadata over their
        keywords. It is assumed that all the keys are
        identical at this point. Further
        implementations could include a more selective
        approach only summing the keys present in both
        and combine the rest...
        '''
        links = data_object.meta_address
        summed_object = self.metadata_objects[
            self.metadata_addresses.index(links[0])]

        for idx_1 in range(1, len(links)):
            summed_object += self.metadata_objects[
            self.metadata_addresses.index(links[idx_1])]

        summed_object = summed_object / len(links)

        return summed_object

    def get_axis(self,axis_name):
        '''
        returns the axis len of an axis with the name
        being axis name. This avoids to hardcode the
        index of the axis and allows more flexibility
        '''
        if axis_name in self.axes.names:
            return self.axes.axes[self.axes.names.index(axis_name)]
        else:
            return None

    def get_axis_len(self,axis_name):
        '''
        returns the axis len of an axis with the name
        being axis name. This avoids to hardcode the
        index of the axis and allows more flexibility
        '''
        if axis_name in self.axes.names:
            return self.axes.axes_len[self.axes.names.index(axis_name)]
        else:
            return None

    def get_axis_unit(self,axis_name):
        '''
        returns the axis len of an axis with the name
        being axis name. This avoids to hardcode the
        index of the axis and allows more flexibility
        '''
        if axis_name in self.axes.names:
            return self.axes.units[self.axes.names.index(axis_name)]
        else:
            return None


    def get_axis_idx(self,axis_name, value):
        '''
        returns the axis len of an axis with the name
        being axis name. This avoids to hardcode the
        index of the axis and allows more flexibility
        '''
        if axis_name in self.axes.names:
            if value in self.axes.axes[self.axes.names.index(axis_name)]:
                return self.axes.axes[self.axes.names.index(axis_name)].index(value)
            else:
                return None
        else:
            return None

    def get_axis_val(self,axis_name, idx):
        '''
        returns the axis len of an axis with the name
        being axis name. This avoids to hardcode the
        index of the axis and allows more flexibility
        '''
        if axis_name in self.axes.names:
            if len(self.axes.axes[self.axes.names.index(axis_name)]) > idx:
                return self.axes.axes[self.axes.names.index(axis_name)][idx]
            else:
                return None
        else:
            return None

class Data_Object:
    '''
    The data_object class is to be used withe the
    data_structure class and is the lower block. 
    Each data_object will have a position given
    by the index. This position can then be
    evaluated on the axes object of the 
    datastructure. Furthermore the the meta_address
    array links to the metadata_objects that 
    describe this data_object. 

    The data stored in the object can be either a
    numpy array or list. 
    '''
    def __init__(self, id, data, index):

        '''
        Here we initiate the data object and can there-
        fore set thevariables as local.
        '''
        self.id             = int(id)
        self.data           = data
        self.index          = list(index)
        self.meta_address   = []
        self.is_backed_up   = False

        self.get_type()
        self.get_dim()

    def __str__(self):
        '''
        Generate a string output for the user to 
        see that the dataclass has initialised 
        properly.
        '''
        output =  "\n##########################################################\n"

        output += "The data object currently consists of:\n"
        output += "- The id: "+str(self.id)+"\n"
        output += "- The dimension: "+str(self.dim)+"\n"
        output += "- The type: "+str(self.type)+"\n"
        output += "- The index: "+str(self.index)+"\n"
        output += "- The meta addresses: "+str(self.meta_address)+"\n"

        output += "##########################################################\n\n"

        return output

    def __iadd__(self, data_object):
        '''
        This function is destined to return the sum 
        of self and object...
        '''
        self.data += data_object.data
        self.meta_address += data_object.meta_address
        return self

    def get_type(self):

        '''
        This will check the type of the loaded data
        structure and save easier as "np" or "py"

        This is important as the lists and numpy
        arrays are called with a different syntax.
        '''
        if isinstance(self.data,type(np.zeros(0))):
            self.type = "np"
            self.dim  = self.data.shape
        elif isinstance(self.data,type([0])):
            self.type = "py"
            self.dim = 0

    def get_dim(self):
        '''
        In this routine we want to evaluate the 
        dimension of the underlying object.
        '''
        #for numpy array
        if self.type == "np":
            self.dim  = self.data.shape

        #for python nested lists
        elif self.type == "py":
            self.dim = []
            end_not_reached = True
            current_object = self.data
            while end_not_reached:
                try:
                    self.dim.append(len(current_object))
                    self.current_object =  current_object[0]
                except:
                    end_not_reached = False
                    break

class Metadata:
    '''
    This class is the one that will store and 
    display metadat. It will be based on dictionary
    layout.

    The dictionaries will be set as strings that 
    can be reconverted to numerical or logical
    values

    self.parameter['name'] = [
        type str('bool', 'int', etc... ),
        value str(),
        unit str()
    ]
    '''

    def __init__(self, meta_id, dictionary = {}):

        self.metadata   = dict(dictionary)
        self.links      = []
        self.meta_id    = int(meta_id)


    def __str__(self):
        '''
        Generate a string output for the user to 
        see that the dataclass has initialised 
        properly.
        '''
        output =  "\n##########################################################\n"
        output += "The selected metadata has the current information: \n"
        for key,row in self.metadata.items():

            output +=  row[0]+": "+row[2]+" "+row[3]+" ("+row[1]+") "+"\n"
        
        output += "##########################################################\n\n"

        return output

    def __getitem__(self, key):
        '''
        This will return the value of the selected
        metadata key in the proper format
        Input: 
        - key of the metadata
        Output: 
        - the metadata information formated 
        '''
        if self.metadata[key][1] == 'float':
            return float(self.metadata[key][2])
        elif self.metadata[key][1] == 'bool':
            return bool(self.metadata[key][2])
        elif self.metadata[key][1] == 'int':
            return int(float(self.metadata[key][2]))
        elif self.metadata[key][1] == 'float_array':
            return [float(element) for element in self.metadata[key][2].split('[')[1].split(']')[0].split(',')]
        elif self.metadata[key][1] == 'int_array':
            return [int(element) for element in self.metadata[key][2].split('[')[1].split(']')[0].split(',')]
        else:
            return self.metadata[key][2]

    def __iadd__(self, metadata_object):
        '''
        This method will add all keys present in the 
        current metadata to the current. This method
        only runs over floats or integers.
        ''' 
        for key in self.metadata.keys():
            if self.metadata[key][1] == 'float' :
                self.metadata[key][2] = str(float(metadata_object.metadata[key][2]) + float(self.metadata[key][2]))
            elif self.metadata[key][1]  == 'int':
                self.metadata[key][2] = str(int(float(metadata_object.metadata[key][2])) + int(float(self.metadata[key][2])))

        return self


    def __truediv__(self, value):
        '''
        This method will divide by a value all keys that
        are either float or int. 
        ''' 
        for key in self.metadata.keys():
            if self.metadata[key][1] == 'float' :
                self.metadata[key][2] = str(float(self.metadata[key][2])/ value) 
            elif  self.metadata[key][1]  == 'int':
                self.metadata[key][2] = str(int(float(self.metadata[key][2])) / value) 
        return self
        
    def addMetadata(self, name, logical_type = 'float', value = '0', unit = '-'):
        '''
        add an element to the dictionary
        Input: 
        - name (str)
        - logycal_type (str)
        - value (str)
        - unit (str)
        '''
        name            = str(name)
        logical_type    = str(logical_type)
        value           = str(value)
        unit            = str(unit)

        self.metadata[name] = [name, logical_type, value, unit]

class Axes:
    '''
    This class will manage all the axes operations
    and is therefore called axes. The main vars of
    the class are the:
    - axis name
    - axis unit
    - axis values
    - and who populates the axis through ids
    '''
    def __init__(self, data_structure):

        #process dimensionality
        self.dim = len(data_structure.data_objects[0].index)

        #set the local variable
        self.names       = [None for i in range(self.dim)]
        self.units       = [None for i in range(self.dim)]
        self.types       = [None for i in range(self.dim)]
        self.axes        = [[] for i in range(self.dim)]
        self.idx         = [[] for i in range(self.dim)]

        #generate axes
        self.generate(data_structure)

    def __str__(self):

        '''
        Here we will mainly run through the objects 
        and try to first built the axes with the 
        appropriate length and then fill the ids
        '''
        return ""

    def generate(self,data_structure):
        '''
        Here we will mainly run through the objects 
        and try to first built the axes with the 
        appropriate length and then fill the ids
        '''
        #find out the length of the indexes
        max_idx = [0 for i in range(self.dim)]
        for i in range(self.dim):
            for element in data_structure.data_objects:
                if element.index[i] > max_idx[i]:
                    max_idx[i] = int(element.index[i])
        for i in range(len(max_idx)):
            max_idx[i] += 1
            
        #set the length of the indexes
        self.axes_values = [
            [None for j in range(max_idx[i])] 
            for i in range(self.dim)]
        self.idx    = [
            [[] for j in range(max_idx[i])] 
            for i in range(self.dim)]

        #fill idx with pointers
        for element in data_structure.data_objects:
            for i in range(self.dim):
                self.idx[i][element.index[i]].append(element.id)
        self.evaluate_length()

    def evaluate_length(self):
        '''
        This function will simply evaluate the length
        of the axes.
        '''
        self.axes_len    = [len(self.idx[i]) for i in range(self.dim)]
        for i in range(self.dim):
            if len(self.axes[i]) == 0:
                self.axes[i] = [j for j in range(len(self.idx[i]))]

    def set_name(self,idx, name = ""):
        '''
        set the name of an axis ...
        '''
        self.names[idx] = name

    def set_unit(self,idx, unit = ""):
        '''
        set the unit of an axis ...
        '''
        self.units[idx] = unit

    def set_axis(self,idx, axis = []):
        '''
        set the values of an axis ...
        '''
        self.axes[idx] = axis


    def get_position(self, val, idx):
        '''
        This function will try to convert the types of
        the values in the array. 
        Input: 
        - val the values
        - idx the axis index
        Output: 
        - position of the indices
        '''
        return self.axes[idx].index(val)

    def collapse_axis(self, idx, data_structure):
        '''
        In this method we will look at an axis and the
        associated values and reduce it. This can be 
        usefull if multiple indices exist with the
        same value...
        Input: 
        - idx index of the axis to evaluate
        '''
        #create and process new axis
        new_axis = list(sorted(set(self.axes[idx])))
        new_idx  = [[] for i in range(len(new_axis))]
        transfer = [
            new_axis.index(self.axes[idx][i]) 
            for i in range(len(self.axes[idx]))
            ]
            
        #fix the objects and their axes
        for i, data_object in enumerate(data_structure.data_objects):
            data_object.index[idx] = transfer[i]
            new_idx[data_object.index[idx]].append(data_object.id)

        #now inject the new axes into the current  definition
        self.axes[idx] = list(new_axis)
        self.idx[idx] = list(new_idx)   

        #reevaluate info
        self.evaluate_length()

    def grab_meta(self, idx, key, data_structure):
        '''
        In this function we would like to grab the 
        values of an axis defined in the metadata of
        the data_objects. Note that the routine will
        cycle through the metadata links and over-
        write itself if multiple definitions are present
        Input: 
        - key of the metadata
        - idx of the axis to be assigned
        '''
        values = []
        ids    = []
        for data_object in data_structure.data_objects:
            value = '-'
            for address in data_object.meta_address:
                try:
                    value = data_structure.get_metadata_object(address)[key]
                except:
                    pass
            values.append(value)
            ids.append(data_object.index[idx])
        self.axes[idx] = list(values)

    def get_id_for_index(self, index):
        '''
        This method will grab the ID of a single 
        element.
        it returns a list of the ids that represent
        the search result
        Input: 
        - index (int array)
        '''
        ids     = []
        purge   = []

        ##############################################
        #fill the arrays
        for idx, element in enumerate(index):
            if isinstance(element,type(slice(0))) or element == '-':
                idx_array = self.idx[idx][:]
                array = []
                
                for element_array in idx_array:
                    for pointer in element_array:
                        array.append(int(pointer))
                ids.append(array)
            else:
                ids.append(list(self.idx[idx][index[idx]]))

        ##############################################
        #go through the arrays and take shorterst
        lengths = [len(array) for array in ids]
        location = lengths.index(min(lengths))

        for element in ids[location]:
            for array in ids:
                if not element in array:
                    purge.append(element)
                    break
        
        for element in list(set(purge)):
            if element in ids[location]:
                ids[location].remove(element)

        return ids[location]

    def get_value(self, axis, idx):
        '''
        here we want to output the actual values 
        given from an index
        the argument '-' cab be given to skip a certain
        index
        '''
        return self.axes[axis][idx]
    
    def prepare_remove(self,idx, array):
        '''
        This prepares the removal of some elements 
        along an axis. it will return the ids of the 
        elements that are concerned
        Input:
        - idx is the axis idx (int)
        - array is the array of elements to delete
        '''
        remove_array = []
        for i in range(len(array)):
            if array[i] == 0:
                remove_array += self.idx[idx][i] 
        return remove_array

    def remove_from_axes(self,idx):
        '''
        This function aims at removing an ID from the 
        axes as it should not longer exist.
        Input:
        - idx is the axis idx (int)
        '''
        for axis in self.idx:
            for row in axis:
                if idx in row:
                    row.remove(idx)

    def clean_axes(self):
        '''
        This will effectively clean the axes and 
        return the equivalence for the indexes
        '''
        #perform a copy to allow building equivalence
        self.idx_copy    = [
            [j for j in range(len(self.idx[i]))] 
            for i in range(self.dim)]

        #grab the orphaned indices
        all_orphaned = []
        for i in range(self.dim):
            orphaned = []
            for j in range(len(self.idx[i])):
                if len(self.idx[i][j]) == 0:
                    orphaned.append(self.axes[i][j])
            all_orphaned.append(list(set(orphaned)))

        #now delete them
        for i in range(self.dim):
            for orphaned in all_orphaned[i]:
                index = self.axes[i].index(orphaned)
                del(self.axes[i][index])
                del(self.idx[i][index])
                del(self.idx_copy[i][index])

        #return equivalences
        self.evaluate_length()

        return self.idx_copy

