import unittest
import miezepy
from miezepy.core.masks import Masks

class Test_mask_system(unittest.TestCase):
    
    def test_init(self):
        masks = Masks()
        keys = [key for key in masks.mask_dict.keys()]
        self.assertEqual(len(keys), 13)

    def test_add_mask(self):
        masks = Masks()
        masks.addMask('circular at 50 50')
        self.assertIn('circular at 50 50', masks.mask_dict.keys())
        self.assertEqual(masks.current_mask, 'circular at 50 50')

        masks.addElement([
            'arc',
            (31,35),
            0, 
            (0,5), 
            (0,360)])
        self.assertEqual(len(masks.mask_dict[masks.current_mask]), 1)

        masks.addElement([
            'triangle',
            (65,65),
            0, 
            5,5])
        self.assertEqual(len(masks.mask_dict[masks.current_mask]), 2)

        masks.sendToGenerator()
        self.assertEqual(len(masks.mask_gen.element_classes),2)

        masks.mask_gen.generateMask(128,128)
        self.assertEqual(masks.mask_gen.mask[35,31],1)
        self.assertEqual(masks.mask_gen.mask[65,65],1)

        masks.removeElement(0)
        masks.sendToGenerator()
        masks.mask_gen.generateMask(128,128)
        self.assertEqual(masks.mask_gen.mask[35,31],0)
        self.assertEqual(masks.mask_gen.mask[65,65],1)