import unittest
import numpy as np
from scipy import special as sp
from scipy import integrate as integrate
from scipy import special as sp
from scipy import constants as co
from scipy import optimize as op
from scipy import stats as st

from miezepy.core.fit_modules.library_iminuit import CosineMinuit
from miezepy.core.fit_modules.library_iminuit import ExpMinuit

class Test_minuit_system(unittest.TestCase):
    cosineStructure = CosineMinuit()
    expStructure    = ExpMinuit()
    
    def test_minuit_sin_0(self):
        x           = np.linspace(0, 2 * np.pi, 50)
        y           = np.cos(x) + 2
        time        = np.linspace(0, 50, 50)
        fit         = self.cosineStructure.fitCosine(y,time ,2*np.pi/50, np.sqrt(y))

        self.assertAlmostEqual(np.abs(fit.values['amplitude']), 1, 1)
        self.assertAlmostEqual(fit.values['offset'], 2, 1)

    def test_minuit_sin_1(self):

        for i in range(0, 50):
            x       = np.linspace(0, 2 * np.pi, 50)
            y       = np.cos(x+ i/50 * 2 * np.pi) + 2
            time    = np.linspace(0, 50, 50)
            fit     = self.cosineStructure.fitCosine(y, time  , 2*np.pi/50 , np.sqrt(y))

            self.assertAlmostEqual(np.abs(fit.values['amplitude']), 1, 1)
            self.assertAlmostEqual(fit.values['offset'], 2, 1)

    def test_minuit_exp_0(self):

        for i in range(0, 10):
            x           = np.linspace(0.05, 2., 5)
            y           = np.exp(-float(i)/10.*0.15*1e-6*co.e*x*1e-9/co.hbar)
            fit         = self.expStructure.fitExp(y, x, np.sqrt(y))

            self.assertAlmostEqual(fit['Gamma'], float(i)/10.*0.15, 2)