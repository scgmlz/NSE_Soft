import unittest
from miezepy.core.core_handler import CoreHandler

class Test_CoreHandler(unittest.TestCase):
    handler = CoreHandler()

    def test_CoreHandler_reset_0(self):
        self.handler.reset()
        self.handler.addEnv('hey')
        self.handler.addEnv('hey')
        self.assertEqual(len(self.handler.env_array), 2)
        self.handler.reset()
        self.assertEqual(len(self.handler.env_array), 0)

    def test_CoreHandler_0(self):
        self.handler.reset()
        self.assertEqual(len(self.handler.env_array), 0)

    def test_CoreHandler_addEnv_0(self):
        self.handler.reset()
        self.handler.addEnv('hey')
        self.assertEqual(len(self.handler.env_array), 1)

    def test_CoreHandler_addEnv_1(self):
        self.handler.reset()
        self.handler.addEnv('hey')
        self.handler.addEnv('hey')
        self.assertEqual(len(self.handler.env_array), 2)
        self.assertEqual(self.handler.env_array[1].name, 'hey_0')

    def test_CoreHandler_delEnv_0(self):
        self.handler.reset()
        self.handler.addEnv('hey')
        self.handler.addEnv('hey')
        self.handler.addEnv('hey')
        self.handler.addEnv('hey')
        self.handler.delEnv('hey_1')
        self.assertEqual(len(self.handler.env_array), 3)
        self.assertEqual(self.handler.current_env.name, 'hey_0')

    def test_CoreHandler_getEnv_0(self):
        self.handler.reset()
        self.handler.addEnv('hey')
        self.handler.addEnv('hey')
        self.assertEqual(self.handler.getEnv('hey_0').name, 'hey_0')

