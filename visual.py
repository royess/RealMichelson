from __future__ import unicode_literals
import sys, os
import random
import numpy as np
import matplotlib.pyplot as plt
from colour_system import cs_hdtv
from simulation import spec_wavelengths

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

cs = cs_hdtv

'''
    This function calculates RGB map from simulation pattern on varied wavelengths
    NOW ONLY WORKS FOR SPECTRUM THAT IS NOT TOO SPARSE!
    
    TODO: make this function compatible with more generlized spectrum! (Yuxuan)
'''
def RGBConverter(pattern):
    wavelength_arr = np.array([entry[1] for entry in pattern]).reshape(100,100,-1)[0,0,:]
    intensity_arr = np.array([entry[2] for entry in pattern]).reshape(100,100,-1)
    
    spec_map = np.ndarray((100,100,np.size(spec_wavelengths)))
    
    for i in range(np.size(wavelength_arr)):
        idx = int((wavelength_arr[i]-380)/5)
        if 0<=idx<np.size(spec_wavelengths):
            spec_map[:,:,idx] += intensity_arr[:,:,i]
        
    return np.apply_along_axis(cs.spec_to_rgb, axis=2, arr=spec_map)

def showPattern(ax, simulation, is_colored=False):
    if simulation.islocalInterference:
        pattern = simulation.localInterference()
    else:
        pattern = simulation.nonlocalInterference()
    
    if is_colored:
        ax.imshow(RGBConverter(pattern), interpolation='none')
    else:
        ax.imshow(np.array([entry[2] for entry in pattern]).reshape(100,100,-1).sum(axis=2))

