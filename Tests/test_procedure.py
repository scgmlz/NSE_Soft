import unittest
import numpy as np
import time

from miezepy.core.module_data import DataStructure
from miezepy.core.module_environment import Environment

def createDataset():
    data = DataStructure()

    loop = [ (i,j,k,l) 
        for i in range(0,10)
        for j in range(0,10)
        for k in range(0,6)
        for l in range(0,16)]

    loop_2 = [ (j,k,l) 
        for j in range(0,10)
        for k in range(0,6)
        for l in range(0,16)]

    meta_dict = {}
    meta_dict['Wavelength']     = ['Wavelength','float', 6e-9, ""]
    meta_dict['Freq. first']    = ['Freq. first','float', 3, ""]
    meta_dict['Freq. second']   = ['Freq. second','float', 6, ""]
    meta_dict['lsd']            = ['lsd','float', 1e10, ""]

    for i,j,k,l in loop:
        if k == 0 and l == 0:
            meta_dict['Freq. second']   = ['Freq. second','float', 6 + j/10*2 , ""]
            data.addMetadataObject(meta_dict)
        data[i,0,j,k,l] = generateMap([i,0,j,k,l])

    for j,k,l in loop_2:
        if k == 0 and l == 0:
            meta_dict['Freq. second']   = ['Freq. second','float', 6 + j/10*2 , ""]
            data.addMetadataObject(meta_dict)
        data[0,1,j,k,l] = generateMap([0,1,j,k,l])

    for j,k,l in loop_2:
        if k == 0 and l == 0:
            meta_dict['Freq. second']   = ['Freq. second','float', 6 + j/10*2 , ""]
            data.addMetadataObject(meta_dict)
        data[1,1,j,k,l] = generateMap([1,1,j,k,l])

    data.metadata_class.addMetadata(
        'Creation date', value = str(time.ctime()), logical_type = 'str')
    data.metadata_class.addMetadata(
        'Source format', value = "ToF files", logical_type = 'str')
    data.metadata_class.addMetadata(
        'Measurement type', value = "MIEZE", logical_type = 'float')
    data.metadata_class.addMetadata(
        'Wavelength error', value = 0.117 , logical_type = 'float')
    data.metadata_class.addMetadata(
        'Distance error', value = 0.0005 , logical_type = 'float')
    data.metadata_class.addMetadata(
        'R_1', value = 9. , logical_type = 'float', unit = 'm')
    data.metadata_class.addMetadata(
        'R_2', value = 5. , logical_type = 'float', unit = 'm')
    data.metadata_class.addMetadata(
        'L_1', value = 1200 , logical_type = 'float', unit = 'm')
    data.metadata_class.addMetadata(
        'L_2', value = 3500 , logical_type = 'float', unit = 'm')
    data.metadata_class.addMetadata(
        'Wavelength in', value = 6. , logical_type = 'float', unit = 'A')
    data.metadata_class.addMetadata(
        'Pixel size', value = 1.5625 , logical_type = 'float', unit = 'mum')
    data.metadata_class.addMetadata(
        'Qy', value = 0.035 , logical_type = 'float', unit = '-')

    return data

def generateMap(input):
    return np.fromfunction(
        lambda i,j: 100 + 50*np.sin((i-64)+(j-64)+input[-1]/16*2*np.pi),
        (128,128), 
        dtype=int)

class Test_data_module(unittest.TestCase):

    def test_data_init(self):
        self.data = DataStructure()
        self.assertEqual(self.data.generated, False)
        self.assertEqual(self.data.map, None)
        self.assertEqual(self.data.axes, None)
        self.assertEqual(self.data.id, 0)
        self.assertEqual(self.data.meta_id, 0)
        self.assertEqual(len(self.data.data_objects), 0)
        self.assertEqual(len(self.data.data_addresses), 0)
        self.assertEqual(len(self.data.metadata_objects), 0)
        self.assertEqual(len(self.data.metadata_addresses), 0)

    def test_data_creation(self):
        self.data = createDataset()
        self.assertEqual(self.data.generated, False)
        self.assertEqual(self.data.map, None)
        self.assertEqual(self.data.axes, None)
        self.assertEqual(self.data.id, 11520)
        self.assertEqual(self.data.meta_id, 120)
        self.assertEqual(len(self.data.data_objects), 11520)
        self.assertEqual(len(self.data.data_addresses), 11520)
        self.assertEqual(len(self.data.metadata_objects), 120)
        self.assertEqual(len(self.data.metadata_addresses), 120)

        self.data.validate()
        self.map = self.data.map
        self.assertEqual(self.map[0,0,0,0,0], 0)
        self.assertEqual(self.map[2,1,0,0,0], -1)
        self.assertEqual(self.map[1,1,9,5,15], 11519)

class Test_Phase_correction(unittest.TestCase):

    def test_phase_correction(self):
        self.env  = Environment(None, 'test_phase')
        self.env.data[0] = createDataset()
        self.env.data[0].validate()
        self.env.data[0].axes.set_name(0, 'Parameter')
        self.env.data[0].axes.set_name(1, 'Measurement')
        self.env.data[0].axes.set_name(2, 'Echo Time')
        self.env.data[0].axes.set_name(3, 'Foil')
        self.env.data[0].axes.set_name(4, 'Time Channel')
        self.env.setCurrentData()

        environnement = self.env
        foils_in_echo = []
        foils_in_echo.append([1, 1, 1, 1, 1, 1])
        foils_in_echo.append([1, 1, 1, 1, 1, 1])
        foils_in_echo.append([1, 1, 1, 1, 1, 1])
        foils_in_echo.append([1, 1, 1, 1, 1, 1])
        foils_in_echo.append([1, 1, 0, 1, 1, 1])
        foils_in_echo.append([1, 1, 0, 1, 1, 1])
        foils_in_echo.append([0, 0, 0, 0, 1, 0])
        foils_in_echo.append([0, 0, 0, 0, 1, 0])
        foils_in_echo.append([0, 0, 0, 0, 1, 0])
        foils_in_echo.append([0, 0, 0, 0, 1, 0])

        #set the values to be processed as data
        Selected = [0,1,2,3,4,5,6,7,8,9]

        #set the reference value
        Reference = [0,0]

        #set the background
        Background = 0

        environnement.fit.set_parameter( name = 'Select',        value = Selected     )
        environnement.fit.set_parameter( name = 'Reference',     value = Reference    )
        environnement.fit.set_parameter( name = 'Background',    value = Background   )
        environnement.fit.set_parameter( name = 'foils_in_echo', value = foils_in_echo)

        #override mask
        self.env.mask.mask = np.fromfunction(lambda i,j: (i+j*32),(32,32),dtype=int)
        self.env.mask.mask = np.kron(self.env.mask.mask, np.ones((4,4),dtype=int))

        #process the echos
        self.env.process.calculateEcho()
        self.assertEqual(self.env.current_data.metadata_objects[0]['tau'], 0.08281041638223735)

        #proceed with the buffering
        self.env.process.prepareBuffer()
        self.assertEqual(self.env.current_data.bufferedData.shape, (10,2,10,6,16, 128, 128))
        self.assertEqual(self.env.current_data.bufferedData.__getitem__((0,0)).shape,(10,6,16,128,128))

        #do the phase calculation
        self.env.fit.extractPhaseMask(
            self.env.current_data,
            self.env.mask,
            self.env.results)

        #check the result
        result = self.env.results.getLastResult('Phase calculation')['Phase']
        keys = [key for key in result.keys()]
        self.assertEqual(int(self.env.results.getLastResult('Phase calculation')['Phase'][keys[0]].sum()),204582)

        #correct the phase
        self.env.fit.correctPhase(
            self.env.current_data,
            self.env.mask,
            self.env.results)
        print(self.env.results.getLastResult('Corrected Phase'))


if __name__ == '__main__':
    ground_0 = Test_Phase_correction()
    ground_0.test_phase_correction()


