import unittest
import miezepy
from miezepy.mieze import Mieze

class Test_launch(unittest.TestCase):

    def test_launch_version(self):
        self.assertEqual(miezepy.__version__,'0.0.1')
