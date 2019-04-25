import unittest
import numpy as np
from miezepy.core.mask_modules.rectangle    import Rectangle
from miezepy.core.mask_modules.triangle     import Triangle
from miezepy.core.mask_modules.circle_arc   import CircleArc
from miezepy.core.mask_modules.radial_comp  import RadialComposition
from miezepy.core.mask_modules.linear_comp  import LinearComposition

class Test_square(unittest.TestCase):

    def test_square_init(self):
        square  = Rectangle()
        para    = square.parameters

        self.assertEqual(para['Position'], [0,0])
        self.assertEqual(para['Angle'], 0)
        self.assertEqual(para['Dimensions'][0], 10)
        self.assertEqual(para['Dimensions'][1], 10)

    def test_square_move_absolute(self):
        square  = Rectangle()
        para    = square.parameters

        self.assertEqual(para['Position'], [0,0])
        square.move(absolute = (10,10))
        self.assertEqual(para['Position'], [10,10])
        
    def test_square_move_relative(self):
        square  = Rectangle()
        para    = square.parameters

        self.assertEqual(para['Position'], [0,0])
        square.move(relative = (20,20))
        self.assertEqual(para['Position'], [20,20])

    def test_square_rotate_absolute(self):
        square  = Rectangle()
        para    = square.parameters

        self.assertEqual(para['Angle'], 0)
        square.rotate(absolute = 45)
        self.assertEqual(para['Angle'], 45)

        square.generate(128,128)   
        self.assertEqual(square.mask[8,8],0)

    def test_square_rotate_relative(self):
        square  = Rectangle()
        para    = square.parameters

        self.assertEqual(para['Angle'], 0)
        square.rotate(relative = 45)
        self.assertEqual(para['Angle'], 45)

        square.generate(128,128)   
        self.assertEqual(square.mask[8,8],0)

    def test_square_generate(self):
        square  = Rectangle()
        square.generate(128,128)

        #test the mask value
        self.assertEqual(square.mask[0,0],1)
        self.assertEqual(square.mask[127,127],0)

        #test the move and mask values
        square.move(relative = (50,50))
        square.generate(128,128)   
        self.assertEqual(square.mask[49,49],1)
        self.assertEqual(square.mask[0,0],0)

        #test the sum
        self.assertEqual(square.mask.sum(),121)

class Test_triangle(unittest.TestCase):
    
    def test_triangle_init(self):
        triangle  = Triangle()
        para    = triangle.parameters

        self.assertEqual(para['Position'], [0,0])
        self.assertEqual(para['Angle'], 0)
        self.assertEqual(para['Dimensions'][0], 10)
        self.assertEqual(para['Dimensions'][1], 10)

    def test_triangle_move_absolute(self):
        triangle  = Triangle()
        para    = triangle.parameters

        self.assertEqual(para['Position'], [0,0])
        triangle.move(absolute = (10,10))
        self.assertEqual(para['Position'], [10,10])
        
    def test_triangle_move_relative(self):
        triangle  = Triangle()
        para    = triangle.parameters

        self.assertEqual(para['Position'], [0,0])
        triangle.move(relative = (20,20))
        self.assertEqual(para['Position'], [20,20])

    def test_triangle_rotate_absolute(self):
        triangle  = Triangle()
        para    = triangle.parameters

        self.assertEqual(para['Angle'], 0)
        triangle.rotate(absolute = 45)
        self.assertEqual(para['Angle'], 45)

        triangle.generate(128,128)   
        self.assertEqual(triangle.mask[8,8],0)

    def test_triangle_rotate_relative(self):
        triangle  = Triangle()
        para    = triangle.parameters

        self.assertEqual(para['Angle'], 0)
        triangle.rotate(relative = 45)
        self.assertEqual(para['Angle'], 45)

        triangle.generate(128,128)   
        self.assertEqual(triangle.mask[8,8],0)

    def test_triangle_generate(self):
        triangle  = Triangle()
        triangle.generate(128,128)

        #test the mask value
        self.assertEqual(triangle.mask[0,0],1)
        self.assertEqual(triangle.mask[127,127],0)

        #test the move and mask values
        triangle.move(relative = (50,50))
        triangle.generate(128,128)   
        self.assertEqual(triangle.mask[49,49],1)
        self.assertEqual(triangle.mask[0,0],0)
        self.assertEqual(triangle.mask[50,56],0)

class Test_arc(unittest.TestCase):
    
    def test_arc_init(self):
        arc  = CircleArc()
        para    = arc.parameters

        self.assertEqual(para['Position'], [0,0])
        self.assertEqual(para['Angle'], 0)
        self.assertEqual(para['Radial range'], (10,15))
        self.assertEqual(para['Angular range'], (0, 350))

    def test_arc_move_absolute(self):
        arc  = CircleArc()
        para    = arc.parameters

        self.assertEqual(para['Position'], [0,0])
        arc.move(absolute = (10,10))
        self.assertEqual(para['Position'], [10,10])
        
    def test_arc_move_relative(self):
        arc  = CircleArc()
        para    = arc.parameters

        self.assertEqual(para['Position'], [0,0])
        arc.move(relative = (20,20))
        self.assertEqual(para['Position'], [20,20])

    def test_arc_rotate_absolute(self):
        arc  = CircleArc()
        para    = arc.parameters

        self.assertEqual(para['Angle'], 0)
        arc.rotate(absolute = 45)
        self.assertEqual(para['Angle'], 45)

        arc.generate(128,128)   
        self.assertEqual(arc.mask[0,0],0)

    def test_arc_rotate_relative(self):
        arc  = CircleArc()
        para    = arc.parameters

        self.assertEqual(para['Angle'], 0)
        arc.rotate(relative = 45)
        self.assertEqual(para['Angle'], 45)

        arc.generate(128,128)   
        self.assertEqual(arc.mask[0,0],0)

    def test_arc_generate(self):
        arc  = CircleArc()
        arc.generate(128,128)

        #test the mask value
        self.assertEqual(arc.mask[0,0],0)
        self.assertEqual(arc.mask[0,12],1)
        self.assertEqual(arc.mask[12,0],1)
        self.assertEqual(arc.mask[127,127],0)

        #test the move and mask values
        arc.move(relative = (50,50))
        arc.generate(128,128)   
        self.assertEqual(arc.mask[50,37],1)
        self.assertEqual(arc.mask[0,0],0)
        self.assertEqual(arc.mask[37,50],1)

class Test_radial_composition(unittest.TestCase):

    def test_arc_square_triangle(self):

        comp = RadialComposition()
        comp.parameters['Multiplicity']  = [6,6]
        comp.parameters['Angle']   = 45
        comp.parameters['Increment'] = False
        comp.setChildType('Arc')
        comp.move(absolute = [100,100])
        comp.template.parameters['Angular range'] = (-90, 90)
        comp.template.parameters['Radial range'] = (10, 13)
        comp.generate(250,250)
        buff = np.array(comp.mask)
        comp.setChildType('Rectangle')
        comp.generate(250,250)
        buff_2 = np.array(comp.mask)
        comp.parameters['Angle']  = 0
        comp.setChildType('Triangle')
        comp.generate(250,250)

        mask = comp.mask + buff + buff_2

        self.assertGreaterEqual(mask[141,141],1)
        self.assertGreaterEqual(mask[85,127],1)
        self.assertGreaterEqual(mask[67,162],0)
        self.assertGreaterEqual(mask[78,38],0)
        self.assertGreaterEqual(mask[69,94],1)

class Test_linear_composition(unittest.TestCase):
    
    def test_arc_square_triangle(self):

        comp = LinearComposition()
        comp.parameters['Multiplicity']  = [6,6]
        comp.parameters['vertical']     = 6
        comp.parameters['Dimensions']   = [100,100]
        comp.parameters['height']       = 100
        comp.parameters['Angle']        = 30
        comp.parameters['Increment']    = False
        comp.setChildType('Arc')
        comp.template.parameters['Angular range'] = (0, 180)
        comp.template.parameters['Radial range'] = (3, 8)
        comp.move(absolute = [50,50])
        comp.generate(128,128)

        mask = comp.mask

        self.assertGreaterEqual(mask[28,100],1)
        self.assertGreaterEqual(mask[88,43],1)
        self.assertGreaterEqual(mask[64,7],1)