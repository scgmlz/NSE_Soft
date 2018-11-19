import unittest

import mieze_python
from mieze_python.mieze import Mieze

class Test_launch(unittest.TestCase):
    def test_launch_version(self):
        self.assertEqual(mieze_python.__version__,'0.0.1')
        