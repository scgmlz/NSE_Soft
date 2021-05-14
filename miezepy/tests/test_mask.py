import unittest
import miezepy
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from miezepy.core.module_mask import MaskStructure

class Test_mask_system(unittest.TestCase):
    
    def test_init(self):
        masks = MaskStructure()
        keys = [key for key in masks.mask_dict.keys()]
        self.assertEqual(len(keys), 0)

    def test_add_mask(self):
        self.app = QtWidgets.QApplication(sys.argv)
        masks = MaskStructure()
        masks.addMask('circular at 50 50')
        self.assertIn('circular at 50 50', masks.mask_dict.keys())
        self.assertEqual(masks.current_mask, 'circular at 50 50')

        masks.addElement(
            {"Visible": ["Visible", "bool", True], 
            "Position": {
                "x": ["x", "float", 64.0], 
                "y": ["y", "float", 64.0], 
                "z": ["z", "float", 0.0]}, 
            "Movable": ["Movable", "bool", False], 
            "Angle": ["Angle", "float", 0.0], 
            "Z": ["Z", "int", 0], 
            "Radial range": {
                "Inner": ["Inner", "float", 0.0], 
                "Outter": ["Outter", "float", 64.0]}, 
            "Angular range": {
                "Inner": ["Inner", "float", 0.0], 
                "Outter": ["Outter", "float", 360.0]}, 
            "Subdivisions": {
                "Radial": ["Radial", "int", 1], 
                "Angular": ["Angular", "int", 1]}, 
            "Subdivision dimensions": {
                "Fill": ["Fill", "bool", True], 
                "Radial": ["Radial", "float", 2.0], 
                "Angular": ["Angular", "float", 10.0]}, 
            "Name": "Mask Element", 
            "Type": "Pie"})
        self.assertEqual(len(masks.mask_dict[masks.current_mask]), 1)

        masks.addElement({
            "Visible": ["Visible", "bool", True], 
            "Position": {
                "x": ["x", "float", 64.0], 
                "y": ["y", "float", 64.0], 
                "z": ["z", "float", 0.0]}, 
            "Movable": ["Movable", "bool", False], 
            "Angle": ["Angle", "float", 0.0], 
            "Z": ["Z", "int", 0], 
            "Dimensions": {
                "Base": ["Base", "float", 64.0], 
                "Height": ["Height", "float", 64.0]}, 
            "Name": "Mask Element", 
            "Type": "Triangle"})
        self.assertEqual(len(masks.mask_dict[masks.current_mask]), 2)

        masks.sendToGenerator(True)
        self.assertEqual(len(masks.mask_gen.element_classes),2)

        masks.mask_gen.generateMask(128,128)
        self.assertEqual(masks.mask_gen.mask[0,0],1)
        self.assertEqual(masks.mask_gen.mask[64,64],3)
        self.assertEqual(masks.mask_gen.mask[127,127],1)
        self.assertEqual(masks.mask_gen.mask[84,84],2)
        self.assertEqual(masks.mask_gen.mask[84,30],2)

        masks.removeElement(0)
        masks.sendToGenerator(True)
        masks.mask_gen.generateMask(128,128)
        self.assertEqual(masks.mask_gen.mask[0,0],0)
        self.assertEqual(masks.mask_gen.mask[64,64],1)
        self.assertEqual(masks.mask_gen.mask[127,127],0)
        self.assertEqual(masks.mask_gen.mask[84,84],0)

if __name__ == '__main__':
    print()
    mask = Test_mask_system()
    mask.test_add_mask()