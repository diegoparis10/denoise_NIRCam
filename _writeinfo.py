#! /usr/bin/python3

# *****************************************************************************
#
# Filename    :    _writeinfo.py
# Description :    Functions to write relevant header info
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

from astropy.io import fits
from datetime import datetime
from _softdef import *

def write_fits_info(image):
    hdu = fits.open(image, 'update')
    hdu[0].header['IMAGPROC'] = '1/f noise correction'
    hdu[0].header['IMAGNAME'] = (image, 'Image name')
    hdu[0].header['IMAGDATE'] = (datetime.now().strftime("%d-%m-%Y %H:%M:%S"), 'Date of creation of the image')
    hdu[0].header['PROGNAME'] = (PROGNAME, 'Program name')
    hdu[0].header['PROGVERS'] = (PROGVERS, 'Program version number')
    hdu[0].header['PROGAUTH'] = (PROGAUTH, 'Program author')
    hdu[0].header['PROGMAIL'] = (PROGMAIL, 'Program author email')
    hdu[0].header['PROGTEAM'] = (PROGTEAM, 'Program author team')
    hdu[0].header['PROGDATE'] = (PROGDATE, 'Program release date')
    hdu.flush()
    hdu.close()    
    
