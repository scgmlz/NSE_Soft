import unittest
from miezepy.core.module_environment import Environment

class Test_Environment(unittest.TestCase):

    def test_Environment_0(self):
        self.env = Environment(None, 'dummy')
        self.assertEqual(len(self.env.data), 1)

    # def test_Environment_addEnv_0(self):
    #     self.handler.reset()
    #     self.handler.addEnv('hey')
    #     self.assertEqual(len(self.handler.env_array), 1)

    # def test_Environment_addEnv_1(self):
    #     self.handler.reset()
    #     self.handler.addEnv('hey')
    #     self.handler.addEnv('hey')
    #     self.assertEqual(len(self.handler.env_array), 2)
    #     self.assertEqual(self.handler.env_array[1].name, 'hey_0')

    # def test_Environment_delEnv_0(self):
    #     self.handler.reset()
    #     self.handler.addEnv('hey')
    #     self.handler.addEnv('hey')
    #     self.handler.addEnv('hey')
    #     self.handler.addEnv('hey')
    #     self.handler.delEnv('hey_1')
    #     self.assertEqual(len(self.handler.env_array), 3)
    #     self.assertEqual(self.handler.current_env.name, 'hey_0')

    # def test_Environment_getEnv_0(self):
    #     self.handler.reset()
    #     self.handler.addEnv('hey')
    #     self.handler.addEnv('hey')
    #     self.assertEqual(self.handler.getEnv('hey_0').name, 'hey_0')

