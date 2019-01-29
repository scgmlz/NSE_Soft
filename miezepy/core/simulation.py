import numpy as np
from numba import jit
from .fit_modules.fit_mieze_minuit import Fit_MIEZE_Minuit
from .result import Result_Handler

@jit(cache = True)
def phase(t_det_elastic, lambda_i, B_NSE, omega_A, omega_B):
    return 2*2*np.pi*(omega_B - omega_A)*t_det_elastic - 2*2*np.pi*(omega_B - omega_A)*(EchoTc.l_1 + EchoTc.l_2)*m_n/h_PlanckSI*lambda_i*1e-10 + 2*2*np.pi*omega_B*EchoTc.l_1*m_n/h_PlanckSI*lambda_i*1e-10 - 2*np.pi*gamma_n*B_NSE*EchoTc.l_nse/h_PlanckSI*m_n*lambda_i*1e-10
    
@jit(cache = True)
def detector_time(t_A0, lambda_i, lambda_f):
    return t_A0 + ((EchoTc.l_1+EchoTc.l_2-EchoTc.l_sd)/h_PlanckSI*m_n*lambda_i*1e-10) + (EchoTc.l_sd/h_PlanckSI*m_n*lambda_f*1e-10)

@jit(cache = True)
def lambda_final(lambda_i, omega):
    return np.sqrt(1/(1/(lambda_i*1e-10)**2 + 2*m_n*omega/1000./(h_PlanckSI*h_Planck)))*1e10

@jit(cache = True)
def scattering_vector(lambda_i, lambda_f, theta):
    return np.sqrt((2*np.pi/(lambda_i*1e-10))**2 + (2*np.pi/(lambda_f*1e-10))**2 - 2*2*np.pi/(lambda_i*1e-10)*2*np.pi/(lambda_f*1e-10)*np.cos(2.*theta))*1e-10

def minuit_fit_exp(contrast, SEtime, contrasterr):
    """Creates the minuit fit function and runs leastsquarefit."""
    def minuitfunction(Gamma):
        np.seterr(all='warn')
        with warnings.catch_warnings():
            try:
                return sum((((1.0*np.exp(-Gamma*1e-6*t*1e-9/(6.582*1e-16))+0.-c)**2)/e**2 for c,t,e in zip(contrast,SEtime,contrasterr)))
            except:
                return np.nan

    Gamma0 = 100.
    
    fit = iminuit.Minuit(minuitfunction,
                         Gamma = Gamma0,
                         pedantic=False,
                         print_level=0)
    fit.migrad()
    params = fit.values
    chi2 = fit.fval
    cov = fit.np_matrix()
    Cov = np.array(cov).reshape([1,1])
    Gamma = fit.values['Gamma']
    Gammaerr = np.sqrt(Cov[0][0])
    return {'Gamma': Gamma,
            'Gammaerr': Gammaerr
           }

class MIEZESimulation():
    """
    MIEZESimulation simulates the RESEDA instrument 
    taking into account the wavelength and different 
    scattering functions to reproduce
    experimental scattering data. 
    """
    def __init__(self):
        self.instrument = {}
        self.instrument['L1']   = 2.373
        self.instrument['L2']   = 4.78
        self.instrument['LNSE'] = 1.
        self.instrument['LSD']  = 3.5

    def defineWavelength(self, mean_value, FWHM, stepnumber):
        """
        defines the wavelength values, the width of 
        the triangular probability distribution and 
        the number of values
        """
        self.wavelength = {}
        self.wavelength['mean_value'] = mean_value
        self.wavelength['FWHM'] = FWHM
        self.wavelength['steps'] = stepnumber
        self.wavelength['values'] = np.linspace(self.wavelength['mean_value']*(1-self.wavelength['FWHM']),self.wavelength['mean_value']
                                            *(1+self.wavelength['FWHM']),self.wavelength['steps'])
        self.wavelength['probs'] = np.zeros(stepnumber)
        self.wavelength['probs'][:stepnumber/2] = np.linspace(0,2/self.wavelength['FWHM'],stepnumber/2)
        self.wavelength['probs'][stepnumber/2:] = np.linspace(2/self.wavelength['FWHM'],0,stepnumber/2)
        self.wavelength['probs'] /= np.sum(self.wavelength['probs'])
        
    def calc_initialTime(self, det_frequency, stepnumber):
        """
        calculates the time neutrons enter the first RF 
        flipper and the probability. The probability is 
        equal for all possible times.
        The initial time values are set to one detector 
        frequency period and need therefore be 
        calculated for every spin echo point
        otherwise there are problems for the large 
        discrepancy between 1Hz and up to some 100kHz 
        in time resolution of the detector
        """
        self.initial_time                = {}
        self.initial_time['frequency']   = det_frequency
        self.initial_time['steps']       = stepnumber
        self.initial_time['values']      = np.linspace(
            0, 
            1/float(self.initial_time['frequency']), 
            self.initial_time['steps'])
        self.initial_time['probs']       = np.ones(
            self.initial_time['steps'])/self.initial_time['steps']
        
        
    def calc_singleLorentzian(self, FWHM, stepnumber, width):
        """
        calculates the values and their probability for a 
        single Lorentzian centered around energytransfer = 0 as scattering function 
        """
        self.energytransfer             = {}
        self.energytransfer['FWHM']     = FWHM
        self.energytransfer['steps']    = stepnumber
        self.energytransfer['width']    = width
        self.energytransfer['values']   = np.linspace(
            -self.energytransfer['width'], 
            self.energytransfer['width'], 
            self.energytransfer['steps'])

        self.energytransfer['probs']    = self.calc_Cauchystri(
            self.energytransfer['values'], 
            self.energytransfer['FWHM'])

        self.energytransfer['probs']    /= np.sum(self.energytransfer['probs'])
    
    def def_tuning(self, freqs):
        """
        calculates the B_NSE values to receive a perfect 
        tuning for the direct beam
        Parameters
        """
        self.instrument['freqs'] = np.asarray(freqs)
        self.instrument['bnse'] = (2/co.physical_constants['neutron gyromag. ratio'][0]
                      *(-(self.instrument['L1'] + self.instrument['L2'])
                      *(self.instrument['freqs'][:,1]-self.instrument['freqs'][:,0])
                      +self.instrument['freqs'][:,1]*self.instrument['L1']) / self.instrument['LNSE'])
    
    def calc_Cauchystri(self, x, FWHM):
        return 1/np.pi*FWHM/(x**2 + FWHM**2)

    def calc_Cauchycumu(self, x, FWHM):
        return 1/np.pi*np.arctan(x/FWHM)+0.5

    def calc_wavelength_after_scattering(self, lambda_i, energytransfer):
        """
        calculates the wavelength lambda_f after an 
        scattering event with energy transfer energytransfer
        Parameters
        """        
        return 2*np.pi/(np.sqrt((2*np.pi/(lambda_i*1e-10))**2 - 2*co.m_n*energytransfer*1e-6*co.e/(co.hbar)**2))*1e10
    
    def calc_phase(self, echo, t_det_elastic, lambda_i):
        """
        calculates the neutron phase at the detector for a 
        neutron arriving at the detector at t_det_elastic 
        for the job number echo and wavelength lambda_i
        Parameters
        """
        return (
            4*np.pi*t_det_elastic*(
                self.instrument['freqs'][echo,1] 
                - self.instrument['freqs'][echo,0])
            -4*np.pi*(
                self.instrument['freqs'][echo,1] - self.instrument['freqs'][echo,0])
            *(
                self.instrument['L1']
                + self.instrument['L2'])*co.m_n/co.h*lambda_i*1e-10 
                + 4*np.pi*self.instrument['freqs'][echo,1]*self.instrument['L1']*co.m_n/co.h*lambda_i*1e-10
                - 2*np.pi*co.physical_constants['neutron gyromag. ratio'][0]*self.instrument['bnse'][echo]*self.instrument['LNSE']/co.h*co.m_n*lambda_i*1e-10)
    
    def calc_resolution(self):
        """
        calculates the resolution, i.e. the contrast for every 
        echo point if neutrons go through the instrument without 
        scattering
        Parameters
        """
        mieze_obj = mieze.mieze()
        contrast = []
        for freq in range(len(self.instrument['freqs'])):

            #process the echo parameters
            self.calc_initialTime(2*(self.instrument['freqs'][freq,1]-self.instrument['freqs'][freq,0]), 200)
            
            #parameters
            time, wavelength, energytransfer, probability = self.getParameterAxes()

            #elastic time
            time_el = self.detector_time_elastic(time, wavelength)

            #process
            time_el     = self.detector_time_elastic(time, wavelength)
            phase       = self.calc_phase(freq, time_el, wavelength)%(2*np.pi)
            t_channel   = time_el*(
                16*2*(self.instrument['freqs'][freq,1] - self.instrument['freqs'][freq,0]))
            t_channel   = t_channel%16
            counts      = np.histogram(t_channel, 16, range=(0,16), weights=(np.cos(phase)+1)*probability)
            fit         = mieze_obj.fit_data_cov(counts[0], np.ones(16)*0.001, 0)

            contrast.append(fit['pol'])
        return contrast
    
    def calc_intermed_scattering_fct(self):
        """
        calculates the signal measured at the detector for 
        several spin echo times if the neutrons are scattered by a
        scattering function S(omega) described by a Lorentzian
        Parameters
        ---------- 
        
        Returns
        -------
        list: contrast
        """
        # mieze_obj = mieze.mieze()
        
        contrast = []
        for freq in range(len(self.instrument['freqs'])):
            
            #process the echo parameters
            self.calc_initialTime(2*(self.instrument['freqs'][freq,1]-self.instrument['freqs'][freq,0]), 200)
            
            #parameters
            time, wavelength, energytransfer, probability = self.getParameterAxes()

            #inelastic time
            time_inel   = self.detector_time_inelastic(time, wavelength, energytransfer)

            #process
            time_el     = self.detector_time_elastic(time, wavelength)
            phase       = self.calc_phase(freq, time_el, wavelength)%(2*np.pi)
            t_channel   = time_inel*(
                16*2*(self.instrument['freqs'][freq,1] - self.instrument['freqs'][freq,0]))
            t_channel   = t_channel%16
            counts      = np.histogram(t_channel, 16, range=(0,16), weights=(np.cos(phase)+1)*probability)
            fit         = mieze_obj.fit_data_cov(counts[0], np.ones(16)*0.001, 0)

            contrast.append(fit['pol'])

        return contrast

    def detector_time_elastic(self, t_A0, lambda_i):
        """
        calculates the arrival time for a neutron with wavelength 
        lambda_i and initial start time into the instrument of t_A0
        """
        return t_A0 + ((self.instrument['L1']+self.instrument['L2'])/co.h*co.m_n*lambda_i*1e-10)
    
    def detector_time_inelastic(self, t_A0, lambda_i, energytransfer):
        """
        calculates the arrival time for a neutron with wavelength 
        lambda_i and initial start time into the instrument of t_A0
        """
        lambda_f = self.calc_wavelength_after_scattering(lambda_i, energytransfer)
        return (t_A0 + (self.instrument['L1']+self.instrument['L2']-self.instrument['LSD'])/co.h*co.m_n*lambda_i*1e-10 + self.instrument['LSD']/co.h*co.m_n*lambda_f*1e-10)

    def getParameterAxes(self):
    
        #set up time axis
        time = np.ones((
            self.wavelength['steps'], 
            self.energytransfer['steps'], 
            self.initial_time['steps']))*self.initial_time['values']

        #set up the wavelength axis
        wavelength = np.ones((
            self.wavelength['steps'], 
            self.energytransfer['steps'], 
            self.initial_time['steps']))
        wavelength = wavelength.swapaxes(0,2)*self.wavelength['values']
        wavelength = wavelength.swapaxes(0,2)

        #set up the energy transfer axis
        energytransfer = np.ones((
            self.wavelength['steps'], 
            self.energytransfer['steps'], 
            self.initial_time['steps']))
        energytransfer = energytransfer.swapaxes(1,2)*self.energytransfer['values']
        energytransfer = energytransfer.swapaxes(1,2)

        #set up the probability axis
        probability = np.ones((
            self.wavelength['steps'], 
            self.energytransfer['steps'], 
            self.initial_time['steps']))*self.initial_time['probs']
        probability = (probability.swapaxes(0,2)*self.wavelength['probs']).swapaxes(0,2)
        probability = (probability.swapaxes(1,2)*self.energytransfer['probs']).swapaxes(1,2)

        return time, wavelength, energytransfer, probability


if __name__ == '__main__':
    print('hey')