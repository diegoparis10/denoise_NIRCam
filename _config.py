#! /usr/bin/python3

# *****************************************************************************
#
# Filename    :    _config.py
# Description :    Functions to set up SExtractor configuration
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
import sys
from subprocess import *
from _iofunc import *

def loadSEX():
    SEX="sex"
    try:
        check_call(['sex'], stdout=DEVNULL, stderr=STDOUT)
    except:
        try:
            check_call(['source-extractor'], stdout=DEVNULL, stderr=STDOUT)
            SEX="source-extractor"
        except:
            print(errstring("Error! Can't find any Source Extractor executable. Exiting..."))
            sys.exit(2)
    return(SEX)

def mk_kern():
    SEX=loadSEX()
    conv="kern.conv"
    if os.path.isfile(conv):
        os.remove(conv)
    with open(conv,'w') as fw:
        fw.write("CONV NORM\n")
        fw.write("# 9x9 convolution mask of a gaussian PSF with FWHM = 5.0 pixels\n")
        fw.write("0.030531 0.065238 0.112208 0.155356 0.173152 0.155356 0.112208 0.065238 0.030531\n")
        fw.write("0.065238 0.139399 0.239763 0.331961 0.369987 0.331961 0.239763 0.139399 0.065238\n")
        fw.write("0.112208 0.239763 0.412386 0.570963 0.636368 0.570963 0.412386 0.239763 0.112208\n")
        fw.write("0.155356 0.331961 0.570963 0.790520 0.881075 0.790520 0.570963 0.331961 0.155356\n")
        fw.write("0.173152 0.369987 0.636368 0.881075 0.982004 0.881075 0.636368 0.369987 0.173152\n")
        fw.write("0.155356 0.331961 0.570963 0.790520 0.881075 0.790520 0.570963 0.331961 0.155356\n")
        fw.write("0.112208 0.239763 0.412386 0.570963 0.636368 0.570963 0.412386 0.239763 0.112208\n")
        fw.write("0.065238 0.139399 0.239763 0.331961 0.369987 0.331961 0.239763 0.139399 0.065238\n")
        fw.write("0.030531 0.065238 0.112208 0.155356 0.173152 0.155356 0.112208 0.065238 0.030531\n")        
    return(conv)

def setSexConf():
    SEX=loadSEX()
    sexconf = "sex.conf"
    if os.path.isfile(sexconf):
        os.remove(sexconf)
    cmd="%s -d > %s" % (SEX,sexconf)
    os.popen(cmd).read()
    return(sexconf)

def setSexNNW():
    sexnnw = "sexnnw.txt"
    if os.path.isfile(sexnnw):
        os.remove(sexnnw)
    with open(sexnnw, 'w') as fw:
        fw.write("NNW\n")
        fw.write("# Neural Network Weights for the SExtractor star/galaxy classifier (V1.3)\n")
        fw.write("# inputs:	9 for profile parameters + 1 for seeing.\n")
        fw.write("# outputs:	``Stellarity index'' (0.0 to 1.0)\n")
        fw.write("# Seeing FWHM range: from 0.025 to 5.5'' (images must have 1.5 < FWHM < 5 pixels)\n")
        fw.write("# Optimized for Moffat profiles with 2<= beta <= 4.\n")
        fw.write("\n")
        fw.write(" 3 10 10  1\n")
        fw.write("\n")
        fw.write("-1.56604e+00 -2.48265e+00 -1.44564e+00 -1.24675e+00 -9.44913e-01 -5.22453e-01  4.61342e-02  8.31957e-01  2.15505e+00  2.64769e-01\n")
        fw.write(" 3.03477e+00  2.69561e+00  3.16188e+00  3.34497e+00  3.51885e+00  3.65570e+00  3.74856e+00  3.84541e+00  4.22811e+00  3.27734e+00\n")
        fw.write("\n")
        fw.write("-3.22480e-01 -2.12804e+00  6.50750e-01 -1.11242e+00 -1.40683e+00 -1.55944e+00 -1.84558e+00 -1.18946e-01  5.52395e-01 -4.36564e-01 -5.30052e+00\n")
        fw.write(" 4.62594e-01 -3.29127e+00  1.10950e+00 -6.01857e-01  1.29492e-01  1.42290e+00  2.90741e+00  2.44058e+00 -9.19118e-01  8.42851e-01 -4.69824e+00\n")
        fw.write("-2.57424e+00  8.96469e-01  8.34775e-01  2.18845e+00  2.46526e+00  8.60878e-02 -6.88080e-01 -1.33623e-02  9.30403e-02  1.64942e+00 -1.01231e+00\n")
        fw.write(" 4.81041e+00  1.53747e+00 -1.12216e+00 -3.16008e+00 -1.67404e+00 -1.75767e+00 -1.29310e+00  5.59549e-01  8.08468e-01 -1.01592e-02 -7.54052e+00\n")
        fw.write(" 1.01933e+01 -2.09484e+01 -1.07426e+00  9.87912e-01  6.05210e-01 -6.04535e-02 -5.87826e-01 -7.94117e-01 -4.89190e-01 -8.12710e-02 -2.07067e+01\n")
        fw.write("-5.31793e+00  7.94240e+00 -4.64165e+00 -4.37436e+00 -1.55417e+00  7.54368e-01  1.09608e+00  1.45967e+00  1.62946e+00 -1.01301e+00  1.13514e-01\n")
        fw.write(" 2.20336e-01  1.70056e+00 -5.20105e-01 -4.28330e-01  1.57258e-03 -3.36502e-01 -8.18568e-02 -7.16163e+00  8.23195e+00 -1.71561e-02 -1.13749e+01\n")
        fw.write(" 3.75075e+00  7.25399e+00 -1.75325e+00 -2.68814e+00 -3.71128e+00 -4.62933e+00 -2.13747e+00 -1.89186e-01  1.29122e+00 -7.49380e-01  6.71712e-01\n")
        fw.write("-8.41923e-01  4.64997e+00  5.65808e-01 -3.08277e-01 -1.01687e+00  1.73127e-01 -8.92130e-01  1.89044e+00 -2.75543e-01 -7.72828e-01  5.36745e-01\n")
        fw.write("-3.65598e+00  7.56997e+00 -3.76373e+00 -1.74542e+00 -1.37540e-01 -5.55400e-01 -1.59195e-01  1.27910e-01  1.91906e+00  1.42119e+00 -4.35502e+00\n")
        fw.write("\n")
        fw.write("-1.70059e+00 -3.65695e+00  1.22367e+00 -5.74367e-01 -3.29571e+00  2.46316e+00  5.22353e+00  2.42038e+00  1.22919e+00 -9.22250e-01 -2.32028e+00\n")
        fw.write("\n")
        fw.write("\n")
        fw.write(" 0.00000e+00\n")
        fw.write(" 1.00000e+00\n")
    return(sexnnw)

def setSexCatParam():
    sexcatparam = "sexcatparam.txt"
    if os.path.isfile(sexcatparam):
        os.remove(sexcatparam)
    with open(sexcatparam, 'w') as fw:
        fw.write("NUMBER\n")
        fw.write("ALPHAWIN_J2000\n")
        fw.write("DELTAWIN_J2000\n")
        fw.write("XWIN_IMAGE\n")
        fw.write("YWIN_IMAGE\n")
        fw.write("A_IMAGE\n")
        fw.write("B_IMAGE\n")
        fw.write("THETA_IMAGE\n")
        fw.write("ELONGATION\n")
        fw.write("ELLIPTICITY\n")
        fw.write("FLUX_AUTO\n")
        fw.write("FLUXERR_AUTO\n")
        fw.write("MAG_AUTO\n")
        fw.write("MAGERR_AUTO\n")
        fw.write("ISOAREA_IMAGE\n")
        fw.write("KRON_RADIUS\n")
        fw.write("BACKGROUND\n")
        fw.write("FWHM_IMAGE\n")
        fw.write("CLASS_STAR\n")
        fw.write("FLAGS\n")
    return(sexcatparam)

def loadSEXConf():
    sexconf=setSexConf()
    sexcatparam=setSexCatParam()
    sexnnw=setSexNNW()
    return(sexconf,sexcatparam,sexnnw)
