#! /usr/bin/python3

# *****************************************************************************
#
# Filename    :    _softdef.py
# Description :    Global definitions
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

PROGRAM_NAME = 'denoise_NIRCam.py'
VERSION_NUMBER = "1.0"
OS = "Linux"
PROGNAME=PROGRAM_NAME
PROGVERS=VERSION_NUMBER
PROGAUTH='Diego Paris'
PROGMAIL='diego.paris@inaf.it'
PROGDATE='2023-05-01'
PROGTEAM='JWST GLASS-ERS Team'
VERSION_MESSAGE = "%s Ver %s, for %s. Copyright (C) <2023> %s <%s>" % (PROGRAM_NAME, VERSION_NUMBER, OS, PROGAUTH, PROGMAIL)
LICENSE = """This software comes with NO WARRANTY. This is free software, and you are welcome to modify and redistribute it under the GPL license"""
DESCRIPTION = """Package to remove 1/f stripes from NIRCam images. """
SYNOPSIS = """
    %s [ -h | --help ]

    %s [ -V | --version ]

    %s [-o OUTSUFFIX] [-a] [-d DILATION] [-f FWHM] [-i ISOAREA] [-k] [-m MFACTOR] [-p] [-s DETECT_SIGMA] [-v] image1 image2 ... imageN [@filelist]

""" % (PROGRAM_NAME, PROGRAM_NAME, PROGRAM_NAME)
