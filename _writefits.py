#! /usr/bin/python3

# *****************************************************************************
#
# Filename    :    _writefits.py
# Description :    Functions to handle fits images processing
# Version     :    1.0
# Authors     :    Diego Paris
# e-mail      :    diego.paris@inaf.it
# Last modify :    05/01/2023
# Copyright   :    (C) 2023 JWST GLASS-ERS Team
# License     :	   GNU General Public License
# 
#******************************************************************************
#
# This is a free software coming WITHOUT ANY WARRANTY and you can redistribute 
# it and/or modify it under the terms of the GNU General Public License as 
# published by the Free Software Foundation. You should have received a copy 
# of the GNU General Public License along with it. 
# If not, see <http://www.gnu.org/licenses/>.
#
# *****************************************************************************

import os
import re
import numpy as np
from astropy.io import fits
from _writeinfo import *

def DQ2BPM(dq,keepall):
    dqdata=fits.getdata(dq)
    if not keepall:
        odata=np.where(dqdata%2==1, 1, 0)
    else:
        odata=np.where(dqdata>0, 1, 0)
    odata=odata.astype(int)
    hdu = fits.PrimaryHDU()
    hdu.data = np.uint8(odata)
    bpm=re.sub('.dq.fits?$', '.bpm.fits', dq)
    if os.path.isfile(bpm):
        os.remove(bpm)
    fits.writeto(bpm,hdu.data)
    return(bpm)

def extract_layers(image):
    sci=re.sub('.fits?$', '.sci.fits', image)
    dq=re.sub('.fits?$', '.sci.dq.fits', image)
    hdul = fits.open(image)
    primary_header = hdul[0].header
    sci_layer=hdul[1]
    err_layer = hdul[2]
    dq_layer = hdul[3]
    area_layer = hdul[4]
    var_poisson_layer = hdul[5]
    var_rnoise_layer = hdul[6]
    var_flat_layer = hdul[7]
    asdf_layer = hdul[8]
    return(primary_header,sci_layer,err_layer,dq_layer,area_layer,var_poisson_layer,var_rnoise_layer,var_flat_layer,asdf_layer)

def assemble_1f(sci,primary_header,n1f_layer,err_layer,dq_layer,area_layer,var_poisson_layer,var_rnoise_layer,var_flat_layer,asdf_layer,outsuffix,v):
    outimage=re.sub('.sci.fits?$', outsuffix, sci)
    primary_hdu = fits.PrimaryHDU(header=primary_header)
    hdul = fits.HDUList()
    hdul.append(primary_hdu)
    hdul.append(n1f_layer)
    hdul.append(err_layer)
    hdul.append(dq_layer)
    hdul.append(area_layer)
    hdul.append(var_poisson_layer)
    hdul.append(var_rnoise_layer)
    hdul.append(var_flat_layer)
    hdul.append(asdf_layer)
    if os.path.isfile(outimage):
        os.remove(outimage)
    hdul.writeto(outimage)
    if (v):
        print("Writing relevant info in %s header" % outimage)
    write_fits_info(outimage)
    if (v):
        print("Done")
    return(outimage)

def getWht(bpm,wht):
    bpmdata=fits.getdata(bpm)
    whtdata=np.where(bpmdata>0.5, 0, 1)
    whtdata=whtdata.astype(int)
    hdu = fits.PrimaryHDU()
    hdu.data = np.uint8(whtdata)
    fits.writeto(wht,hdu.data)
    return(wht)

def getFlag(sgm,flag):
    sgmdata=fits.getdata(sgm)
    flgdata=np.where(sgmdata>0.5, 1, 0)
    flgdata=flgdata.astype(int)
    hdu = fits.PrimaryHDU()
    hdu.data = np.uint8(flgdata)
    fits.writeto(flag,hdu.data)
    return(flag)

def getObm(msk,bpm,obm):
    bpmdata=fits.getdata(bpm)
    mskdata=fits.getdata(msk)
    obmdata=np.logical_or(bpmdata, mskdata)
    hdu = fits.PrimaryHDU()
    hdu.data = np.uint8(obmdata)
    fits.writeto(obm,hdu.data)
    return(obm)

def logical_OR(msk,mskEO):
    mskdata=fits.getdata(msk)
    mskEOdata=fits.getdata(mskEO)
    data=np.logical_or(mskdata, mskEOdata)
    hdu = fits.PrimaryHDU()
    hdu.data = np.uint8(data)
    os.remove(msk)
    fits.writeto(msk,hdu.data)
    return(msk)
