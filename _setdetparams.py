#! /usr/bin/python3

# *****************************************************************************
#
# Filename    :    _setdetparams.py
# Description :    Functions to get detection parameters
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

import math

def getDetectThresh(ds,dma):
    return(ds/math.sqrt(float(dma)))

def getDetectMinArea(fwhm):
    return(round(math.pi * (fwhm/2.0)**2))
