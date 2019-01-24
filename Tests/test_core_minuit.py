import unittest
import numpy as np
from scipy import special as sp
from scipy import integrate as integrate
from scipy import special as sp
from scipy import constants as co
from scipy import optimize as op
from scipy import stats as st
from miezepy.core.fit_modules.fit_mieze_minuit import Fit_MIEZE_Minuit

class Test_minuit_system(unittest.TestCase):
    
    def test_minuit_sin_0(self):
        fit_mieze   = Fit_MIEZE_Minuit()
        x           = np.linspace(0, 2 * np.pi, 50)
        y           = np.cos(x) + 2
        time        = np.linspace(0, 50, 50)
        fit         = fit_mieze.minuit_fit_cosine(y,time ,2*np.pi/50, np.sqrt(y))

        self.assertAlmostEqual(np.abs(fit.values['ampl']), 1)
        self.assertAlmostEqual(fit.values['offset'], 2)

    def test_minuit_sin_1(self):
        fit_mieze = Fit_MIEZE_Minuit()

        for i in range(0, 50):
            x       = np.linspace(0, 2 * np.pi, 50)
            y       = np.cos(x+ i/50 * 2 * np.pi) + 2
            time    = np.linspace(0, 50, 50)
            fit = fit_mieze.minuit_fit_cosine(y, time  , 2*np.pi/50 , np.sqrt(y))

            self.assertAlmostEqual(np.abs(fit.values['ampl']), 1, 1)
            self.assertAlmostEqual(fit.values['offset'], 2, 1)

    def test_minuit_exp_0(self):
        fit_mieze   = Fit_MIEZE_Minuit()

        for i in range(0, 10):
            x           = np.linspace(0.05, 2., 5)
            y           = np.exp(-float(i)/10.*0.15*1e-6*co.e*x*1e-9/co.hbar)
            fit         = fit_mieze.minuit_fit_exp(y, x, np.sqrt(y))

            self.assertAlmostEqual(fit['Gamma'], float(i)/10.*0.15, 2)