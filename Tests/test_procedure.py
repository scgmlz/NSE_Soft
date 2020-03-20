import unittest
import numpy as np
import time
import os
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from miezepy.core.module_data import DataStructure
from miezepy.core.module_environment import Environment

def createFakeDataset():
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
    meta_dict['Wavelength']     = ['Wavelength','float', 6e-10, ""]
    meta_dict['Freq. first']    = ['Freq. first','float', 30, ""]
    meta_dict['Freq. second']   = ['Freq. second','float', 60, ""]
    meta_dict['lsd']            = ['lsd','float', 1200e9, ""]
    meta_dict['Monitor']        = ['Monitor','float', 100, ""]

    for i,j,k,l in loop:
        if k == 0 and l == 0:
            meta_dict['Freq. second']   = ['Freq. second','float', (60 + j) , ""]
            data.addMetadataObject(meta_dict)
        data[i,0,j,k,l] = generateMap([i,0,j,k,l])

    for j,k,l in loop_2:
        if k == 0 and l == 0:
            meta_dict['Freq. second']   = ['Freq. second','float', (60 + j) , ""]
            data.addMetadataObject(meta_dict)
        data[0,1,j,k,l] = generateMap([0,1,j,k,l])

    for j,k,l in loop_2:
        if k == 0 and l == 0:
            meta_dict['Freq. second']   = ['Freq. second','float', (60 + j), ""]
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

def createHTO(proc):
    
    env  = Environment(None, 'test_phase')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    env.io.load_MIEZE_TOF(os.path.join(dir_path, 'ressources','LoadTest.txt' ))
    env.data[0].axes.set_name(0, 'Parameter')
    env.data[0].axes.set_name(1, 'Measurement')
    env.data[0].axes.set_name(2, 'Echo Time')
    env.data[0].axes.set_name(3, 'Foil')
    env.data[0].axes.set_name(4, 'Time Channel')
    env.setCurrentData()

    #process the echos
    for meta_object in env.current_data.metadata_objects:
        meta_object.addMetadata('Wavelength', value = 8.e-10 , logical_type = 'float', unit = 'A')

    env.mask.mask_dict["HTO_1"]=[{"Visible": ["Visible", "bool", True], "Position": {"x": ["x", "float", 63.5], "y": ["y", "float", 63.5], "z": ["z", "float", 0.0]}, "Movable": ["Movable", "bool", False], "Angle": ["Angle", "float", 0.0], "Z": ["Z", "int", 0], "Dimensions": {"x": ["x", "float", 128.0], "y": ["y", "float", 128.0]}, "Subdivisions": {"x": ["x", "int", 16], "y": ["y", "int", 16]}, "Subdivision dimensions": {"Fill": ["Fill", "bool", True], "x": ["x", "float", 2.0], "y": ["y", "float", 2.0]}, "Fill": {"0": ["0", "bool", True], "1": ["1", "color", [0, 0, 255, 255]]}, "Line": {"Visible": ["Visible", "bool", True], "Thickness": ["Thickness", "float", 0.05], "Color": ["Color", "color", [0, 0, 0, 255]]}, "Draw faces": ["Draw faces", "bool", True], "Draw edges": ["Draw edges", "bool", False], "Draw smooth": ["Draw smooth", "bool", True], "OpenGl mode": ["OpenGl mode", "str", "opaque"], "Name": "Mask Element", "Type": "Rectangle"}]  

    env.mask.mask_dict["HTO_2"] = [{"Visible": ["Visible", "bool", True], "Position": {"x": ["x", "float", 63.5], "y": ["y", "float", 63.5], "z": ["z", "float", 0.0]}, "Movable": ["Movable", "bool", False], "Angle": ["Angle", "float", 0.0], "Z": ["Z", "int", 0], "Dimensions": {"x": ["x", "float", 128.0], "y": ["y", "float", 128.0]}, "Subdivisions": {"x": ["x", "int", 1], "y": ["y", "int", 1]}, "Subdivision dimensions": {"Fill": ["Fill", "bool", True], "x": ["x", "float", 2.0], "y": ["y", "float", 2.0]}, "Fill": {"0": ["0", "bool", True], "1": ["1", "color", [0, 0, 255, 255]]}, "Line": {"Visible": ["Visible", "bool", True], "Thickness": ["Thickness", "float", 0.05], "Color": ["Color", "color", [0, 0, 0, 255]]}, "Draw faces": ["Draw faces", "bool", True], "Draw edges": ["Draw edges", "bool", False], "Draw smooth": ["Draw smooth", "bool", True], "OpenGl mode": ["OpenGl mode", "str", "opaque"], "Name": "Mask Element", "Type": "Rectangle"}]

    foils_in_echo = []
    foils_in_echo.append([0, 0, 0, 0, 0, 0, 0, 1])
    foils_in_echo.append([0, 0, 0, 0, 0, 0, 0, 1])
    foils_in_echo.append([0, 0, 0, 0, 0, 0, 0, 1])

    #set the values to be processed as data
    Selected = ['reso', '5K', '50K']

    #set the reference value
    Reference = ['reso',0]

    #set the background
    Background = None

    dir_path = os.path.dirname(os.path.realpath(__file__))
    foil_0 = np.loadtxt(os.path.join(dir_path,'ressources', 'foilheight_final0.txt'))
    foil_1 = np.loadtxt(os.path.join(dir_path,'ressources', 'foilheight_final1.txt'))
    foil_2 = np.loadtxt(os.path.join(dir_path,'ressources', 'foilheight_final2.txt'))
    foil_5 = np.loadtxt(os.path.join(dir_path,'ressources', 'foilheight_final3.txt'))
    foil_6 = np.loadtxt(os.path.join(dir_path,'ressources', 'foilheight_final4.txt'))
    foil_7 = np.loadtxt(os.path.join(dir_path,'ressources', 'foilheight_final5.txt'))

    surface_profile = [
        foil_0,
        foil_1,
        foil_2,
        np.zeros(foil_0.shape),
        np.zeros(foil_0.shape),
        foil_5,
        foil_6,
        foil_7
    ]

    surface_profile = np.array(surface_profile)

    env.fit.set_parameter( name = 'Select',           value = Selected     )
    env.fit.set_parameter( name = 'Reference',        value = Reference    )
    env.fit.set_parameter( name = 'Background',       value = Background   )
    env.fit.set_parameter( name = 'foils_in_echo',    value = foils_in_echo)
    env.fit.set_parameter( name = 'surface_profile',  value = surface_profile )
    env.fit.set_parameter( name = 'processors',       value = proc )

    return env

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

    @unittest.skipIf(
        ("APPVEYOR" in os.environ and os.environ["APPVEYOR"] == "True") ,  "Skipping this test on Appveyor due to memory.")
    def test_data_creation(self):
        self.data = createFakeDataset()
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


    @unittest.skipIf(
        ("APPVEYOR" in os.environ and os.environ["APPVEYOR"] == "True")
        or ("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true") ,  "Skipping this test on CI.")
    def test_phase_correction_mask(self):
        self.env  = Environment(None, 'test_phase')
        self.env.data[0] = createFakeDataset()
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
        self.env.mask.mask = np.fromfunction(lambda i,j: (i+j*16),(16,16),dtype=int)
        self.env.mask.mask = np.kron(self.env.mask.mask, np.ones((8,8),dtype=int))

        #process the echos
        self.env.process.calculateEcho()
        self.assertEqual(self.env.current_data.metadata_objects[0]['tau'], 0.09937249956783661)

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
        self.assertEqual(int(result[keys[0]].sum()),305861)

        #correct the phase
        self.env.fit.correctPhase(
            self.env.current_data,
            self.env.mask,
            self.env.results)
        result = self.env.results.getLastResult('Corrected Phase')['Shift']
        keys = [key for key in result.keys()]
        self.assertEqual(int(result[0][0][self.env.current_data.get_axis('Echo Time')[0]].sum()),156672000)

    @unittest.skipIf(
        ("APPVEYOR" in os.environ and os.environ["APPVEYOR"] == "True")
        or ("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true") ,  "Skipping this test on CI.")
    def test_phase_correction_exposure(self):
        self.env  = Environment(None, 'test_phase')
        self.env.data[0] = createFakeDataset()
        self.env.data[0].validate()
        self.env.data[0].axes.set_name(0, 'Parameter')
        self.env.data[0].axes.set_name(1, 'Measurement')
        self.env.data[0].axes.set_name(2, 'Echo Time')
        self.env.data[0].axes.set_name(3, 'Foil')
        self.env.data[0].axes.set_name(4, 'Time Channel')
        self.env.setCurrentData()
        self.env.instrument.setDetector('Reseda', 14032019)

        environnement = self.env
        foils_in_echo = []
        foils_in_echo.append([1, 1, 1, 0, 0, 1, 1, 1])
        foils_in_echo.append([1, 1, 1, 0, 0, 1, 1, 1])
        foils_in_echo.append([1, 1, 1, 0, 0, 1, 1, 1])
        foils_in_echo.append([1, 1, 1, 0, 0, 1, 1, 1])
        foils_in_echo.append([1, 1, 0, 0, 0, 1, 1, 1])
        foils_in_echo.append([1, 1, 0, 0, 0, 1, 1, 1])
        foils_in_echo.append([0, 0, 0, 0, 0, 0, 1, 0])
        foils_in_echo.append([0, 0, 0, 0, 0, 0, 1, 0])
        foils_in_echo.append([0, 0, 0, 0, 0, 0, 1, 0])
        foils_in_echo.append([0, 0, 0, 0, 0, 0, 1, 0])

        #set the values to be processed as data
        Selected = [0,1,2,3,4,5,6,7,8,9]

        #set the reference value
        Reference = [0,0]

        #set the background
        Background = 0

        dir_path = os.path.dirname(os.path.realpath(__file__))
        foil_0 = np.loadtxt(os.path.join(dir_path,'ressources', 'foilheight_final0.txt'))
        foil_1 = np.loadtxt(os.path.join(dir_path,'ressources', 'foilheight_final1.txt'))
        foil_2 = np.loadtxt(os.path.join(dir_path,'ressources', 'foilheight_final2.txt'))
        foil_5 = np.loadtxt(os.path.join(dir_path,'ressources', 'foilheight_final3.txt'))
        foil_6 = np.loadtxt(os.path.join(dir_path,'ressources', 'foilheight_final4.txt'))
        foil_7 = np.loadtxt(os.path.join(dir_path,'ressources', 'foilheight_final5.txt'))
        surface_profile = [
            foil_0,
            foil_1,
            foil_2,
            np.zeros(foil_0.shape),
            np.zeros(foil_0.shape),
            foil_5,
            foil_6,
            foil_7
        ]
        surface_profile = np.array(surface_profile)

        environnement.fit.set_parameter( name = 'Select',           value = Selected     )
        environnement.fit.set_parameter( name = 'Reference',        value = Reference    )
        environnement.fit.set_parameter( name = 'Background',       value = Background   )
        environnement.fit.set_parameter( name = 'foils_in_echo',    value = foils_in_echo)
        environnement.fit.set_parameter( name = 'surface_profile',  value = surface_profile )

        #override mask
        self.env.mask.mask = np.fromfunction(lambda i,j: (i+j*16),(16,16),dtype=int)
        self.env.mask.mask = np.kron(self.env.mask.mask, np.ones((8,8),dtype=int))

        #process the echos
        self.env.process.calculateEcho()
        self.assertEqual(self.env.current_data.metadata_objects[0]['tau'], 0.09937249956783661)

        #proceed with the buffering
        self.env.process.prepareBuffer()
        self.assertEqual(self.env.current_data.bufferedData.shape, (10,2,10,6,16, 128, 128))
        self.assertEqual(self.env.current_data.bufferedData.__getitem__((0,0)).shape,(10,6,16,128,128))

        #do the phase calculation
        self.env.fit.correctPhaseExposure(
            self.env.current_data,
            self.env.mask,
            self.env.instrument,
            self.env.results)

        result = self.env.results.getLastResult('Corrected Phase')['Shift']
        keys = [key for key in result.keys()]
        self.assertEqual(int(result[0][0][self.env.current_data.get_axis('Echo Time')[0]].sum()),157286400)

        self.env.mask.mask = np.zeros((128,128))
        self.env.mask.mask[32:92, 32:92] = 1
        
        self.env.fit.calcContrastRef(
            self.env.current_data,
            self.env.mask,
            self.env.results)

        result = self.env.results.getLastResult('Reference contrast calculation')

        self.env.fit.calcContrastMain(
            self.env.current_data,
            self.env.mask,
            self.env.results,
            select = self.env.current_data.get_axis('Parameter'))

        self.env.fit.contrastFit(
            self.env.current_data,
            self.env.mask,
            self.env.results)

        self.result = self.env.results.getLastResult('Contrast fit')['Parameters']

    @unittest.skipIf(
        ("APPVEYOR" in os.environ and os.environ["APPVEYOR"] == "True")
        or ("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true") ,  "Skipping this test on CI.")
    def test_single_proc_mask_data(self):
        self.phase_correction_mask_data(1)
        
    @unittest.skipIf(
        ("APPVEYOR" in os.environ and os.environ["APPVEYOR"] == "True")
        or ("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true") ,  "Skipping this test on CI.")
    def test_multi_proc_mask_data(self):
        self.phase_correction_mask_data(12)

    @unittest.skipIf(
        ("APPVEYOR" in os.environ and os.environ["APPVEYOR"] == "True")
        or ("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true") ,  "Skipping this test on CI.")
    def test_single_proc_exposure_data(self):
        self.phase_correction_exposure_data(1)
        
    @unittest.skipIf(
        ("APPVEYOR" in os.environ and os.environ["APPVEYOR"] == "True")
        or ("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true") ,  "Skipping this test on CI.")
    def test_multi_proc_exposure_data(self):
        self.phase_correction_exposure_data(12)

    @unittest.skipIf(
        ("APPVEYOR" in os.environ and os.environ["APPVEYOR"] == "True")
        or ("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true") ,  "Skipping this test on CI.")
    def phase_correction_mask_data(self, proc):
        self.app = QtWidgets.QApplication(sys.argv)
        ######################################################
        #test the dataset
        self.env = createHTO(proc)
        data_sum = 0
        for data_object in self.env.current_data.data_objects:
            data_sum += data_object.data.sum()
        self.assertEqual(data_sum, 696802)

        ######################################################
        #Prepare the phase process
        self.env.mask.setMask("HTO_1")
        self.env.mask.generateMask(128,128)
        self.env.process.calculateEcho()
        self.env.process.prepareBuffer()

        self.assertEqual(
            self.env.current_data.bufferedData.shape, 
            (3,1,3,8,16, 128, 128))

        self.assertEqual(
            self.env.current_data.bufferedData.__getitem__((0,0)).shape,
            (3,8,16,128,128))

        #do the phase calculation
        self.env.fit.extractPhaseMask(
            self.env.current_data,
            self.env.mask,
            self.env.results)
        
        #correct the phase
        self.env.fit.correctPhase(
            self.env.current_data,
            self.env.mask,
            self.env.results)

        result = self.env.results.getLastResult('Corrected Phase')['Shift']
        self.assertEqual(int(result['50K'][0][self.env.current_data.get_axis('Echo Time')[0]].sum()),4539)

        ######################################################
        # do the contrast
        self.env.mask.setMask("HTO_2")
        self.env.mask.generateMask(128,128)
        
        self.env.fit.calcContrastRef(
            self.env.current_data,
            self.env.mask,
            self.env.results)

        self.env.fit.calcContrastMain(
            self.env.current_data,
            self.env.mask,
            self.env.results,
            select = self.env.current_data.get_axis('Parameter'))

        self.env.fit.contrastFit(
            self.env.current_data,
            self.env.mask,
            self.env.results)

        self.result = self.env.results.getLastResult('Contrast fit')['Parameters']
        
        self.assertEqual(self.result['reso']['y'].tolist(), [1,1,1])
        self.assertEqual(
            [round(e, 4) for e in self.result['5K']['y'].tolist()], 
            [round(e, 4) for e in [0.8326, 0.7797, 0.6768]])
        self.assertEqual(
            [round(e, 4) for e in self.result['50K']['y'].tolist()], 
            [round(e, 4) for e in [0.8443, 0.5087, 0.3239]])

    @unittest.skipIf(
        ("APPVEYOR" in os.environ and os.environ["APPVEYOR"] == "True")
        or ("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true") ,  "Skipping this test on CI.")
    def phase_correction_exposure_data(self, proc):
        self.app = QtWidgets.QApplication(sys.argv)

        ######################################################
        #test the dataset
        self.env = createHTO(proc)
        self.env.instrument.setDetector('Reseda', 14032019)
        data_sum = 0
        for data_object in self.env.current_data.data_objects:
            data_sum += data_object.data.sum()
        self.assertEqual(data_sum, 696802)

        ######################################################
        #Prepare the phase process
        self.env.process.calculateEcho()
        self.env.process.prepareBuffer()

        self.assertEqual(
            self.env.current_data.bufferedData.shape, 
            (3,1,3,8,16, 128, 128))

        self.assertEqual(
            self.env.current_data.bufferedData.__getitem__((0,0)).shape,
            (3,8,16,128,128))

        #do the phase calculation
        self.env.fit.correctPhaseExposure(
            self.env.current_data,
            self.env.mask,
            self.env.instrument,
            self.env.results)

        result = self.env.results.getLastResult('Corrected Phase')['Shift']
        self.assertEqual(int(result['50K'][0][self.env.current_data.get_axis('Echo Time')[0]].sum()),4539)

        self.env.mask.mask = np.zeros((128,128))
        self.env.mask.mask[32:92, 32:92] = 1
        
        self.env.fit.calcContrastRef(
            self.env.current_data,
            self.env.mask,
            self.env.results)

        result = self.env.results.getLastResult('Reference contrast calculation')

        self.env.fit.calcContrastMain(
            self.env.current_data,
            self.env.mask,
            self.env.results,
            select = self.env.current_data.get_axis('Parameter'))

        self.env.fit.contrastFit(
            self.env.current_data,
            self.env.mask,
            self.env.results)

        self.result = self.env.results.getLastResult('Contrast fit')['Parameters']
        self.assertEqual(self.result['reso']['y'].tolist(), [1,1,1])
        self.assertEqual(
            [round(e, 4) for e in self.result['5K']['y'].tolist()], 
            [round(e, 4) for e in [0.9202105470865976, 0.8952656900529399, 0.8204182337749286]])
        self.assertEqual(
            [round(e, 4) for e in self.result['50K']['y'].tolist()], 
            [round(e, 4) for e in [0.7607151726522323, 0.5407819350675142, 0.13512816355553667]])
