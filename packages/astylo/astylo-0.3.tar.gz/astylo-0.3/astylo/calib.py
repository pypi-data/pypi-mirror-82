#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

SYNTHETIC PHOTOMETRY

"""
import os
import numpy as np
from astropy.io import ascii
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, NullFormatter
import subprocess as SP
import warnings
DEVNULL = open(os.devnull, 'w')

## astylo
from arrlib import allist
from iolib import (ascext,
                   read_fits, read_hdf5, write_hdf5#, read_ascii
)
from astrolib import fixwcs
from plotlib import plot2D_m, colib

aroot = os.path.dirname(os.path.abspath(__file__))

##-----------------------------------------------

##            "intercalib" based tools

##-----------------------------------------------

class intercalib:
    '''
    Intercalibration

    ------ INPUT ------
    filIN               target FITS file (Default: None)
    '''
    def __init__(self, filIN=None):
        
        ## INPUTS
        self.filIN = filIN

        if filIN is not None:
            self.hdr = fixwcs(filIN).header
            w = fixwcs(filIN).wcs
            ds = read_fits(filIN)
            self.im = ds.data
            self.wvl = ds.wave

    def synthetic_photometry(self, filt, w_spec=None, Fnu_spec=None, 
                             extrapoff=True, verbose=False):
        '''
        External Fortran library (SwING) needed

        ------ INPUT ------
        filt                photometry names (string, tuple or list)
        w_spec              wavelengths (Default: None - via filIN)
        Fnu_spec            spectra (Default: None - via filIN)
        extrapoff           set zeros for uncovered wave grid (Default: True)
        verbose             keep tmp files (Default: False)
        ------ OUTPUT ------
        ds                  output dataset
          wcen              center wavelength
          Fnu_filt          synthetic photometry
          smat              standard deviation matrices
        '''
        ds = type('', (), {})()

        ## Convert all format phot names to list
        filt = allist(filt)

        ## Input is a FITS file
        if self.filIN is not None:
            w_spec = self.wvl
            Fnu_spec = self.im

        w_spec = np.array(w_spec)
        Fnu_spec = np.array(Fnu_spec)
        if len(Fnu_spec.shape)==1:
            Ndim = 1
            Fnu_spec = Fnu_spec[:,np.newaxis,np.newaxis]
        else:
            Ndim = 3

        ## Do not extrapolate the wave grid that is not covered by input spectra
        ##-----------------------------------------------------------------------
        if extrapoff==True:
            for phot in filt:
                # w_grid = read_ascii(aroot+'/dat/filt_'+phot, dtype=float)[:,0]
                w_grid = ascii.read(aroot+'/dat/filt_'+phot+ascext,
                                    names=['Wave','Spectral Response'])['Wave']
                # print(w_spec[0], w_grid[0])
                # print(w_spec[-1], w_grid[-1])
                if w_spec[0]>w_grid[0] or w_spec[-1]<w_grid[-1]:
                    warnings.warn('Synthetic photometry of {} can be underestimated' \
                                  'due to uncovered wavelengths'.format(phot))
            ## Insert 2 wvl (0.01 um & w_spec[0]-0.01 um) with 0 value
            wave = np.insert(w_spec, 0, (.01, w_spec[0]-.01))
            flux = np.insert(Fnu_spec, 0, np.zeros(Fnu_spec.shape[-1]), axis=0)
        else:
            wave = w_spec
            flux = Fnu_spec

        ## Write input.h5
        ##----------------
        fortIN = os.getcwd()+'/synthetic_photometry_input'
        
        write_hdf5(fortIN, 'Filter label', filt)
        write_hdf5(fortIN, 'Wavelength (microns)', wave, append=True)
        write_hdf5(fortIN, 'Flux (x.Hz-1)', flux, append=True)
        write_hdf5(fortIN, '(docalib,dophot)', [1,1], append=True)

        ## Call the Fortran lib
        ##----------------------
        SP.call('synthetic_photometry', shell=True)

        ## Read output.h5
        ##----------------
        fortOUT = os.getcwd()+'/synthetic_photometry_output'

        ds.wcen = read_hdf5(fortOUT, 'Central wavelength (microns)')
        ds.Fnu_filt = read_hdf5(fortOUT, 'Flux (x.Hz-1)')
        ds.smat = read_hdf5(fortOUT, 'Standard deviation matrix')
        
        ## Convert zeros to NaNs
        ma_zero = np.ma.array(ds.Fnu_filt, mask=(ds.Fnu_filt==0)).mask
        ds.Fnu_filt[ma_zero] = np.nan

        ## Reform outputs
        if Ndim==1:
            ds.Fnu_filt = ds.Fnu_filt[:,0,0]
        if len(ds.wcen)==1:
            ds.wcen = ds.wcen[0]
            ds.Fnu_filt = ds.Fnu_filt[0]
            ds.smat = ds.smat[0][0]
        
        ## Clean temperary h5 files
        ##--------------------------
        if verbose==False:
            SP.call('rm -rf '+fortIN+'.h5', shell=True, cwd=os.getcwd())
            SP.call('rm -rf '+fortOUT+'.h5', shell=True, cwd=os.getcwd())

        return ds

    def specorrect(self, factor=1., offset=0., w_spec=None, Fnu_spec=None,
                   wlim=(None,None), filOUT=None):
        '''
        Calibrate spectra from different obs. in order to eliminate gaps
        
        
        ------ INPUT ------
        factor              scalar or ndarray (Default: 1.)
        offset              scalar or ndarray (Default: 0.)
        w_spec              wavelengths (Default: None - via filIN)
        Fnu_spec            spectra (Default: None - via filIN)
        wlim                wave limits (Default: (None,None))
        filOUT              overwrite fits file (Default: NO)
        ------ OUTPUT ------
        new_spec            new_spec = factor * Fnu_spec + offset
        '''
        ## Input is a FITS file
        if self.filIN is not None:
            w_spec = self.wvl
            Fnu_spec = self.im

        w_spec = np.array(w_spec)
        Fnu_spec = np.array(Fnu_spec)
        if len(Fnu_spec.shape)==1:
            Ndim = 1
            Fnu_spec = Fnu_spec[:,np.newaxis,np.newaxis]
        else:
            Ndim = 3

        ## Truncate wavelengths
        if wlim[0] is None:
            wmin = w_spec[0]
        else:
            wmin = wlim[0]
        if wlim[1] is None:
            wmax = w_spec[-1]
        else:
            wmax = wlim[1]

        ## Modify spectra
        new_spec = np.copy(Fnu_spec)
        for k, lam in enumerate(w_spec):
            if lam>=wmin and lam<=wmax:
                new_spec[k,:,:] = factor * Fnu_spec[k,:,:] + offset

        ## Reform outputs
        if Ndim==1:
            new_spec = new_spec[:,0,0]
                    
        if filOUT is not None:
            write_fits(filOUT, hdr, new_spec, wave=w_spec)
        
        return new_spec

"""
class spec2phot(intercalib):
    '''
    Intercalibration between spectrometry and photometry (REF)

    --- INPUT ---
    filIN       to convolve
    filREF      convolution ref
    phot        photometry name (once a phot)
    filKER      convolution kernel(s) (Default: None)
    --- OUTPUT ---
    '''
    def __init__(self, filIN, filREF, phot, filKER=None, saveKER=None, \
        uncIN=None, Nmc=0, filOUT=None):
        super().__init__(filIN)
        self.phot = phot

        if self.wave is not None: # filIN is spec
            ## Convolve filIN (spec)
            if filKER is not None:
                conv = iconvolve(filIN, filKER, saveKER, \
                    uncIN, filOUT=filPRO)
            else:
                filPRO = filIN # filPRO is spec
            
            ## Reprojection to spec (filIN)
            pro = imontage(filREF, filPRO)
            F_phot = pro.reproject(filOUT=filOUT)

        else: # filIN is phot
            ## Reset header (should be spec)
            self.hdr = read_fits(filREF).header
            self.im = read_fits(filREF).data
            self.wvl = read_fits(filREF).wave
            
            ## Convolve filIN (phot)
            if filKER is not None:
                conv = iconvolve(filIN, filKER, saveKER, \
                    uncIN, filOUT=filPRO)
            else:
                filPRO = filIN # filPRO is phot
            
            ## Reprojection to spec (filREF)
            pro = imontage(filPRO, filREF)
            F_phot = pro.reproject(filOUT=filOUT)

        ## Synthetic photometry
        wcen, Fsyn, Fsig = self.synthetic_photometry((phot))
        self.wcen = wcen[0]
        self.Fsyn = Fsyn[0]
        self.Fsig = Fsig[0][0]

        self.factor = F_phot / self.Fsyn

    def calib_factor(self):
        return self.factor

    def image(self):
        return self.Fsyn
    
    def write_image(self, filSYN):
        comment = "Synthetic photometry with " + self.phot
        write_fits(filSYN, self.hdr, self.Fsyn, self.wvl, COMMENT=comment)

class phot2phot:
    '''
    Intercalibration between two photometry
    '''
    def __init__(self, filIN, filREF, filKER=None, saveKER=None, \
        uncIN=None, Nmc=0, filOUT=None):

        ## Convolution (optional)
        if filKER is not None:
            conv = iconvolve(filIN, filKER, saveKER, \
                uncIN, filOUT=filPRO)
        else:
            filPRO = filIN

        ## Reprojection config
        pro = imontage(filPRO, filREF)
        self.im = pro.reproject(filOUT=filOUT)

    def image(self):
        return self.im
"""

def photometry_profile(datdir=None, *photometry):
    '''
    ------ INPUT ------
    datdir              profile data path (Default: ./dat/)
    photometry          photometry
    ------ OUTPUT ------
    '''
    ## Read data
    ##-----------
    lam = []
    val = []
    for phot in photometry:
        if datdir is None:
            datdir = aroot+'/dat/'
        # dat = read_ascii(datdir+'filt_'+phot, dtype=float)
        # lam.append(dat[:,0])
        # val.append(dat[:,1])
        dat = ascii.read(datdir+'filt_'+phot+ascext, names=['Wave','Spectral Response'])
        lam.append(dat['Wave'])
        val.append(dat['Spectral Response'])
    lam = np.array(lam)
    val = np.array(val)

    ## Plotting setting
    ##------------------
    p = plot2D_m(lam, val, xlim=(1.9, 40.), ylim=(-.01, 1.01), \
    xlog=1, ylog=1, cl=colib[2:], lw=1.8, \
    lablist=photometry, \
    xlab=r'$Wavelength,\,\,\lambda\,\,[\mu m]$', \
    ylab='Response', \
    # ylab='Spectral response\n(electrons / photon)', \
    legend='upper left', figsize=(12,3))

    p.set_border(left=.05, bottom=.2, right=.99, top=.99)

    # sizeXL = 50
    # p.set_font(xticksize=sizeXL, yticksize=sizeXL, \
    #     axesize=sizeXL, legendsize=sizeXL)

    ## vlines (e.g. band markers)
    ##----------------------------
    greylines = []
    pinklines = []
    greylines.extend([2.3567863, 5.1532226]) # AKARI/IRC
    greylines.extend([5.242817, 7.597705]) # Spitzer/IRS-SL2
    pinklines.extend([7.3675313, 8.66892]) # Spitzer/IRS-SL3
    greylines.extend([7.5337057, 14.736635]) # Spitzer/IRS-SL1
    greylines.extend([14.266611, 21.051888]) # Spitzer/IRS-LL2
    pinklines.extend([19.483675, 21.50092]) # Spitzer/IRS-LL3
    greylines.extend([20.555237, 38.41488]) # Spitzer/IRS-LL1
    p.ax.vlines(greylines, 0, 1.1, linestyles='dotted', colors='grey')
    p.ax.vlines(pinklines, 0, 1.1, linestyles='dotted', colors='pink')

    ## tick setting
    ##-------------------- x --------------------------
    xtic = [2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 30, 40]
    xtic_min = np.arange(2., 41., 1.)
    p.ax.set_xticks(xtic, minor=False) # major
    p.ax.set_xticks(xtic_min, minor=True) # minor
    # ScalarFormatter().set_scientific(False)
    p.ax.xaxis.set_major_formatter(ScalarFormatter()) # major
    p.ax.xaxis.set_minor_formatter(NullFormatter()) # minor
    # p.ax.minorticks_off()
    ##--------------------- y --------------------------
    ytic = np.arange(0, 1.01, .2)
    ytic_min = np.arange(0, 1., .1)
    p.ax.set_yticks(ytic, minor=False) # major
    p.ax.set_yticks(ytic_min, minor=True) # minor
    # ScalarFormatter().set_scientific(False)
    p.ax.yaxis.set_major_formatter(ScalarFormatter()) # major
    p.ax.yaxis.set_minor_formatter(NullFormatter()) # minor
    # p.ax.minorticks_off()
    ##-----------------------------------------------

    return p

"""
------------------------------ MAIN (test) ------------------------------
"""
if __name__ == "__main__":

    pass
