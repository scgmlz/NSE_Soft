import unittest
import miezepy
from miezepy.core.module_mask import MaskStructure

class Test_mask_system(unittest.TestCase):
    
    def test_init(self):
        masks = MaskStructure()
        keys = [key for key in masks.mask_dict.keys()]
        self.assertEqual(len(keys), 2)

    def test_add_mask(self):
        masks = MaskStructure()
        masks.addMask('circular at 50 50')
        self.assertIn('circular at 50 50', masks.mask_dict.keys())
        self.assertEqual(masks.current_mask, 'circular at 50 50')

        masks.addElement({
            'Name': 'Arc',
            'Position' : (35,80),
            'Angle':0, 
            'Radial range': (0,20), 
            'Angular range': (0,360)})
        self.assertEqual(len(masks.mask_dict[masks.current_mask]), 1)

        masks.addElement({
            'Name': 'Triangle',
            'Position' : (100,35),
            'Angle':0, 
            'Dimensions':[20,20]})
        self.assertEqual(len(masks.mask_dict[masks.current_mask]), 2)

        masks.sendToGenerator(True)
        self.assertEqual(len(masks.mask_gen.element_classes),2)

        masks.mask_gen.generateMask(128,128)
        self.assertEqual(masks.mask_gen.mask[0,0],0)
        self.assertEqual(masks.mask_gen.mask[35,80],1)
        self.assertEqual(masks.mask_gen.mask[34,104],2)
        self.assertEqual(masks.mask_gen.mask[33,97],3)

        masks.removeElement(0)
        masks.sendToGenerator(True)
        masks.mask_gen.generateMask(128,128)
        self.assertEqual(masks.mask_gen.mask[0,0],0)
        self.assertEqual(masks.mask_gen.mask[35,80],0)
        self.assertEqual(masks.mask_gen.mask[34,104],1)
        self.assertEqual(masks.mask_gen.mask[33,97],1)

        import matplotlib.pyplot as plt
        plt.pcolormesh(masks.mask_gen.mask)
        plt.show()
 
if __name__ == '__main__':
    print()
    mask = Test_mask_system()
    mask.test_add_mask()