import unittest
from miezepy.core.library_logic import *

class Test_elementInList(unittest.TestCase):
    elements = ['hey_2', 'hey_3', 'hey_4','cool_thing_no']

    def test_elementInList_0(self):
        self.assertEqual(generateSingleName('hey', self.elements), 'hey')

    def test_elementInList_1(self):
        self.assertEqual(generateSingleName('hey_2', self.elements), 'hey_5')

    def test_elementInList_2(self):
        self.assertEqual(generateSingleName('cool_thing_no', self.elements), 'cool_thing_no_0')
       