import unittest
import numpy as np

from miezepy.core.fit_modules.library_fit import *

from miezepy.core.module_result import ResultStructure
from miezepy.core.module_data import DataStructure, Metadata


class Test_fit_library(unittest.TestCase):
    results = ResultStructure()
    data    = DataStructure()
    meta    = Metadata(0)

    def test_sinus_fit_0(self):
        #generate the data
        x           = np.linspace(0, 2.*np.pi, 30)
        y           = 50.*np.cos(x+0.5*np.pi) + 100.

        #proceed
        passed = fitDataSinus(self.results, y, np.sqrt(y), time_chan=30)

        #test
        self.assertEqual(passed, True)
        self.assertGreaterEqual(
            self.results.getLastResult(name = 'Fit Data Sinus', key = 'amplitude'),49)
        self.assertLessEqual(
            self.results.getLastResult(name = 'Fit Data Sinus', key = 'amplitude'),51)
        self.assertGreaterEqual(
            self.results.getLastResult(name = 'Fit Data Sinus', key = 'mean'),99)
        self.assertLessEqual(
            self.results.getLastResult(name = 'Fit Data Sinus', key = 'mean'),101)
        self.assertGreaterEqual(
            self.results.getLastResult(name = 'Fit Data Sinus', key = 'phase'),1.65)
        self.assertLessEqual(
            self.results.getLastResult(name = 'Fit Data Sinus', key = 'phase'),1.67)

    def test_sinus_fit_1(self):
        #generate the data
        x           = np.linspace(0, 2.*np.pi, 30)
        y           = 0.*np.exp(x) + 10.

        #proceed
        passed = fitDataSinus(self.results, y, np.sqrt(y), time_chan=30)

        #test
        self.assertEqual(passed, False)

    def test_tau_calculation_0(self):
        self.assertAlmostEqual(miezeTauCalculation(6e-9, 3,6,1e10)[0], 0.0828,3)

    def test_tau_calculation_1(self):
        self.assertAlmostEqual(miezeTauCalculation(8e-9, 3,6,1e10)[0], 0.196,3)

    def test_tau_processing_0(self):
        self.meta.addMetadata('Wavelength', value = 6e-9)
        self.meta.addMetadata('Freq. first', value = 3)
        self.meta.addMetadata('Freq. second', value = 6)
        self.meta.addMetadata('lsd', value = 1e10)
        self.data.metadata_class.addMetadata('Wavelength error', value = 0)
        self.data.metadata_class.addMetadata('Distance error', value = 0)

        self.assertAlmostEqual(miezeTauProcessing(self.meta, self.data)[0], 0.0828,3)

    def test_tau_processing_1(self):
        self.meta.addMetadata('Wavelength', value = 8e-9)
        self.meta.addMetadata('Freq. first', value = 3)
        self.meta.addMetadata('Freq. second', value = 6)
        self.meta.addMetadata('lsd', value = 1e10)
        self.data.metadata_class.addMetadata('Wavelength error', value = 0)
        self.data.metadata_class.addMetadata('Distance error', value = 0)

        self.assertAlmostEqual(miezeTauProcessing(self.meta, self.data)[0], 0.196,3)

    def test_contrast_equation_0(self):
        target      = [0,0,0,0]
        BG_target   = [0,0,0,0]

        result = contrastEquation(target,BG_target)
        self.assertEqual(result,0)

    def test_contrast_equation_1(self):
        target      = [10,0,5,0]
        BG_target   = [1,0,1,0]

        result = contrastEquation(target,BG_target)
        self.assertEqual(result,2.25)

    def test_contrast_error_0(self):
        target      = [0,0,0,0]
        BG_target   = [0,0,0,0]

        result = contrastErrorEquation(target,BG_target)
        self.assertEqual(result,0)

    def test_contrast_error_1(self):        
        target      = [10,3,5,1]
        BG_target   = [1,2,1,0]

        result = contrastErrorEquation(target,BG_target)
        self.assertEqual(result,1.0625)