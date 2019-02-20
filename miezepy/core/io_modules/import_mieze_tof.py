import sys
import io
import numpy as np
import time

class Import_MIEZE_TOF:

    def __init__(self,load_path, target):
        '''
        This class will simply initiate an run all
        the procedures on construct. 
        '''
        self.verbose    = True
        container       = self.process_input_tof(load_path,target)
        axes            = self.process_tof_axes(container)
        self.fetch_data_tof(container, axes)

    def process_input_tof(self,load_path, target):

        '''
        This function will go through the provided 
        text fill and try to parse the information
        in order to generate a dictionary that will
        be fed back to the data handler
        '''
        f               = open(load_path, "r")
        lines           = f.readlines()
        path            = ""
        dimensions_names= []
        units           = []
        para_array      = []
        ignore_array    = []
        meta_array      = []

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

            ########################################
            #grab exclusions        
            elif len(line.split("Ignore : ")) > 1:
                templine = line.strip('\n')
                elements = templine.split(" : ")
                ignore_array.append([int(elements[1]),eval(elements[2]) ])

            ########################################
            #grab the metadata load instructions        
            elif len(line.split("Metadata : ")) > 1:             
                templine = line.strip('\n')
                elements = templine.split(" : ")
                meta_array.append([element for element in elements])

            ########################################
            #grab the dimension names     
            elif len(line.split("Dim : ")) > 1:
                templine = line.strip('\n').strip("Dim : ")
                elements = templine.split(" : ")
                dimensions_names = elements

            ########################################
            #grab the units    
            elif len(line.split("Unit : ")) > 1:
                templine = line.strip('\n').strip("Unit : ")
                elements = templine.split(" : ")

                units = elements
                
        f.close()
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

    def process_tof_axes(self,container):
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

    def fetch_data_tof(self,container, axes):
        '''
        Here the dataclass will be built up with its
        dimesions and corresponding data ...
        '''
        #unpack the container
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

        for idx_0, source in enumerate(para_array):

            #unfold generate the path array
            path_iter = [
                path
                + str(source[1]) 
                + str(path_string) 
                + ".tof" 
                for path_string in eval(source[2])]

            #Axis selection
            index = tuple([ element[idx_0] for element in real_idx_definition ])

            #loop over and process
            for idx_1,file_path in enumerate(path_iter):
                f = open(file_path,'rb')
                target.add_metadata_object(self.generate_tof_metadata(f, meta_array))
                dimensionality  = [
                    int(source[-1].strip("(").strip(")").split("x")[i]) 
                    for i in range(len(source[-1].split("x")))]
                loadeddata      = np.fromfile(f, dtype=np.int32)[:np.prod(dimensionality)]
                data            = loadeddata.reshape(*dimensionality)
                f.close()
                
                #fill the data into the target
                for idx_2 in range(extra_dim[0]):
                    for idx_3 in range(extra_dim[1]):
                        address = tuple(index) + (idx_1,idx_2,idx_3)
                        target[address] = data[idx_2,idx_3,:,:]

        #validate the loaded data
        target.validate()    
 
        for idx, name in enumerate(dimensions_names):
            try:
                target.axes.set_name(idx,name)
                target.axes.set_unit(idx,units[idx])
                try:
                    target.axes.set_axis(idx,[float(element) for element in real_axis_definition[idx]])
                except:
                    target.axes.set_axis(idx,[element for element in real_axis_definition[idx]])
            except:
                pass

        #set some metadata
        target.metadata_class.add_metadata('Creation date', value = str(time.ctime()), logical_type = 'str')
        target.metadata_class.add_metadata('Source format', value = "ToF files", logical_type = 'str')
        target.metadata_class.add_metadata('Measurement type', value = "MIEZE", logical_type = 'float')
        target.metadata_class.add_metadata('Wavelength error', value = 0.117 , logical_type = 'float')
        target.metadata_class.add_metadata('Distance error', value = 0.0005 , logical_type = 'float')

        target.metadata_class.add_metadata('R_1', value = 9. , logical_type = 'float', unit = 'm')
        target.metadata_class.add_metadata('R_2', value = 5. , logical_type = 'float', unit = 'm')
        target.metadata_class.add_metadata('L_1', value = 1200 , logical_type = 'float', unit = 'm')
        target.metadata_class.add_metadata('L_2', value = 3500 , logical_type = 'float', unit = 'm')
        target.metadata_class.add_metadata('Wavelength in', value = 6. , logical_type = 'float', unit = 'A')
        target.metadata_class.add_metadata('Pixel size', value = 1.5625 , logical_type = 'float', unit = 'mum')
        target.metadata_class.add_metadata('Qy', value = 0.035 , logical_type = 'float', unit = '-')
        target.metadata_class.add_metadata('Selected foils', value = '[1,1,1,0,0,1,1,1]' , logical_type = 'int_array', unit = '-')
        target.metadata_class.add_metadata('Resolution', value = '[28.6, 0]' , logical_type = 'float_array', unit = 'K')


    def generate_tof_metadata(self,f,meta_array):
        '''
        Here is the routine managing the metadata 
        handling.
        '''
        metadata = {}
        Lines = f.readlines()
        for i, binaryLine in enumerate(Lines):
            try:
                line = binaryLine.decode('ascii').replace('\n','')
            except:
                line = ''
            for element in meta_array:
                if len(line.split(element[1]+' :')) > 1:
                    try:
                        metadata[element[2]] = [
                            element[2],
                            element[3],
                            str(float(line.split(element[1]+' : ')[1].split(element[-1])[0])*float(element[4])),
                            element[4]
                            ]
                    except:
                        metadata[element[2]] = [
                            element[2],
                            element[3],
                            line.split(element[1]+' : ')[1].split(element[-1])[0],
                            element[4]
                            ]
        f.seek(0)
        return metadata
                

         