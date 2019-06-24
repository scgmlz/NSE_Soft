import unittest
import numpy as np
import time
import os

from miezepy.core.module_instrument import InstrumentStructure


class Test_instrument_module(unittest.TestCase):

    def test_instrument_init(self):
        self.instrument = InstrumentStructure()
        self.assertEqual(self.instrument.success, True)

    def test_instrument_Reseda_0(self):
        self.instrument = InstrumentStructure()
        self.instrument.setDetector('Reseda')
        self.assertEqual(self.instrument.detector.foil_array.shape, (8,128,128))

    def test_instrument_Reseda_1(self):
        self.instrument = InstrumentStructure()
        self.instrument.setDetector('Reseda', 14032019)
        self.assertEqual(self.instrument.detector.foil_array.shape, (8,128,128))

if __name__ == '__main__':
    ground_0 = Test_instrument_module()
    ground_0.test_instrument_Reseda_0()