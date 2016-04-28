# -*- coding: utf-8 -*-
import numpy as np
import astropy.units as u

class ZodiacalLight(object):
    """Zodiacal Light class template
    
    This class contains all variables and methods necessary to perform
    Zodiacal Light Module calculations in exoplanet mission simulation.
    
    Args:
        \*\*specs:
            user specified values
    
    Attributes:
        magZ (float):
            1 zodi brightness in mag per asec2
        magEZ (float):
            1 exozodi brightness in mag per asec2
        varEZ (float):
            exozodi variation (variance of log-normal distribution)
        nEZ (float):
            exozodi level in zodi
        
    """

    _modtype = 'ZodiacalLight'
    _outspec = {}

    def __init__(self, magZ=23, magEZ=22, varEZ=0., nEZ=1.5, **specs):
        
        self.magZ = float(magZ)         # 1 zodi brightness in mag per asec2
        self.magEZ = float(magEZ)       # 1 exozodi brightness in mag per asec2
        self.varEZ = float(varEZ)       # exozodi variation (variance of log-normal dist.)
        self.nEZ = float(nEZ)           # exozodi level in zodi
        
        # populate outspec
        for att in self.__dict__.keys():
            dat = self.__dict__[att]
            self._outspec[att] = dat.value if isinstance(dat,u.Quantity) else dat

    def __str__(self):
        """String representation of the Zodiacal Light object
        
        When the command 'print' is used on the Zodiacal Light object, this 
        method will return the values contained in the object"""
        
        for att in self.__dict__.keys():
            print '%s: %r' % (att, getattr(self, att))
        
        return 'Zodiacal Light class object attributes'

    def fZ(self, TL, sInds, lam):
        """Returns surface brightness of local zodiacal light
        
        Args:
            TL (TargetList):
                TargetList class object
            sInds (integer ndarray):
                Numpy ndarray containing integer indices of the stars of interest, 
                with the length of the number of planets of interest.
            lam:
                Central wavelength (default units of nm)
        
        Returns:
            fZ (ndarray):
                1D numpy ndarray of surface brightness of zodiacal light (per arcsec2)
        """
        
        sInds = np.array(sInds)
        if not sInds.shape:
            sInds = np.array([sInds])
        
        fZ = np.array([10**(-0.4*self.magZ)]*len(sInds))/u.arcsec**2
        
        return fZ

    def fEZ(self, TL, sInds, I):
        """Returns surface brightness of exo-zodiacal light
        
        Args:
            TL (TargetList):
                TargetList class object
            sInds (integer ndarray):
                Numpy ndarray containing integer indices of the stars of interest, 
                with the length of the number of planets of interest.
            I (ndarray):
                1D numpy ndarray or scalar value of inclination in degrees
        
        Returns:
            fEZ (ndarray):
                1D numpy ndarray of surface brightness of exo-zodiacal light (per arcsec2)
        
        """
        
        sInds = np.array(sInds)
        if not sInds.shape:
            sInds = np.array([sInds])
        
        # assume log-normal distribution of variance
        if self.varEZ != 0:
            mu = np.log(self.nEZ) - 0.5*np.log(1. + self.varEZ/self.nEZ**2)
            v = np.sqrt(np.log(self.varEZ/self.nEZ**2 + 1.))
            self.nEZ = np.random.lognormal(mean=mu, sigma=v, size=(len(sInds),))
            
        fEZ = np.array([10**(-0.4*self.magEZ)]*len(sInds))*self.nEZ/u.arcsec**2
        
        return fEZ