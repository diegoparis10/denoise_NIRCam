#! /usr/bin/python3

# *****************************************************************************
#
# Filename    :    _iofunc.py
# Description :    I/O functions
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

from astropy.io import ascii

def warnstring(string):
    return("\033[33;47;5m%s  \033[m" % string)

def errstring(string):
    return("\033[31;47;5m%s  \033[m" % string)

def verb(string,v):
    if (v):
        print(string)
    else:
        print("",end='\r')

def parseList(inlist,images):
    with open(inlist,'r') as r:
        lines=r.readlines()
        for line in lines:
            f=line.rstrip('\n').strip()
            if (f!=""):
                images.append(f)

def checkIsoarea(cat,min_isoarea):
    data = ascii.read(cat)
    isoareas = data['ISOAREA_IMAGE']
    for isoarea in isoareas:
        if (isoarea>=min_isoarea):
            return True
    return False
