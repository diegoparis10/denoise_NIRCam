#! /usr/bin/python3

# *****************************************************************************
#
# Filename    :    denoise_NIRCam.py
# Description :    Command line parsing and image processing
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
import sys
from astropy.io import fits
from datetime import datetime
from optparse import OptionParser
from _iofunc import *
from _procimage import *
from _softdef import *
from _writefits import *
from _writeinfo import *

def main():
    usage = "\n%s\n\n%s\n %s\n\n%s" % (SYNOPSIS,LICENSE,DESCRIPTION,VERSION_MESSAGE)
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--outsuffix", type="str", default=".dn.fits",
		      help="The suffix for output images [.dn.fits]")
    parser.add_option("-a", "--amp", action="store_true", dest="amp", default=False,
                      help="Correct background stripes for each amplifier? If False, the corrective medians of background stripes are computed along the entire horizontal axis {False}")
    parser.add_option("-d", "--dilation", type="int", default=5,
		      help="The dilation in pixels to flag sources [5]")
    parser.add_option("-f", "--fwhm", type="float", default=4,
		      help="The fwhm in pixels [4]")
    parser.add_option("-i", "--isoarea", type="int", default=4000,
		      help="The minimum area to mask extended objects [4000]")
    parser.add_option("-k", "--keepall", action="store_true", dest="keepall", default=False,
                      help="Keep all flags in DQ layer? If False, only pixels that are marked as 'DO NOT USE' are discarded {False}")
    parser.add_option("-m", "--mfactor", type="int", default=4,
		      help="The factor used to multiply the dilation of extended object mask [4]")
    parser.add_option("-p", "--purge", action="store_true", dest="purge", default=False,
                      help="Purge temporary intermediate files? {False}")
    parser.add_option("-s", "--detect_sigma", type="float", dest="detect_sigma", default=4,
                      help="The sigma used to detect sources [4]")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                      help="Verbose output [False]")
    parser.add_option("-V", "--version", 
                      action="store_true", dest="version", 
                      help="Print program version number, then"
                      " quit.")
    (options,args) = parser.parse_args()
    if options.version:
        print(VERSION_MESSAGE)
        sys.exit(0)
    if (len(args)<1):
        print(errstring("Error! No input image given."))
        print(parser.print_help())
        sys.exit(1)
    images=[]
    for arg in args:
        if (arg.startswith('@')):
            parseList(arg[1:],images)
        else:
            images.append(arg)
    if (len(images)<1):
        print(errstring("Error! No input image given."))
        sys.exit(1)
    start =  datetime.now()
    verb("--------------------------------------",options.verbose)
    verb("%s" % VERSION_MESSAGE,options.verbose)
    verb("--------------------------------------",options.verbose)
    verb("%s - START PROCESSING." % (start.strftime("%d-%m-%Y %H:%M:%S")),options.verbose)
    verb("PROCESSING INFO",options.verbose)
    verb("MODALITY: %s" % ("AMPLIFIER SUB-AXES" if options.amp else "WHOLE AXES"),options.verbose)
    verb("FWHM: %.1f pixels" % options.fwhm,options.verbose)
    verb("DETECTION SIGMA: %.1f " % options.detect_sigma,options.verbose)
    verb("MINIMUM ISOAREA TO DETECT EXTENDED SOURCES: %s pixels" % options.isoarea,options.verbose)
    verb("SOURCE DILATION: %d pixels" % options.dilation,options.verbose)
    verb("DILATION MAGNIFICATION FOR EXTENDED SOURCES: %d " % options.mfactor,options.verbose)
    verb("OUTPUT IMAGES SUFFIX: %s " % options.outsuffix,options.verbose)
    verb("--------------------------------------\n",options.verbose)
    for image in images:
        verb("Processing %s....\n" % image,options.verbose)
        verb("----------------------------------\n",options.verbose)
        sci=re.sub('.fits?$', '.sci.fits', image)
        dq=re.sub('.fits?$', '.sci.dq.fits', image)
        primary_header,sci_layer,err_layer,dq_layer,area_layer,var_poisson_layer,var_rnoise_layer,var_flat_layer,asdf_layer = extract_layers(image)
        scihdu = fits.PrimaryHDU(data=sci_layer.data,header=sci_layer.header)
        if os.path.isfile(sci):
            os.remove(sci)
        scihdu.writeto(sci)
        dqhdu = fits.PrimaryHDU(data=dq_layer.data,header=dq_layer.header)
        if os.path.isfile(dq):
            os.remove(dq)
        dqhdu.writeto(dq)
        bpm =  DQ2BPM(dq,options.keepall)
        n1f_layer = denoise_1of(sci,bpm,options.fwhm,options.detect_sigma,options.dilation,options.isoarea,options.mfactor,options.amp,options.outsuffix,options.purge,options.verbose)
        outimage=assemble_1f(sci,primary_header,n1f_layer,err_layer,dq_layer,area_layer,var_poisson_layer,var_rnoise_layer,var_flat_layer,asdf_layer,options.outsuffix,options.verbose)
        verb("----------------------------------\n",options.verbose)
    end = datetime.now()
    verb("%s - END PROCESSING." % (end.strftime("%d-%m-%Y %H:%M:%S")),options.verbose)
    verb("Total time elapsed: %s." % str(end-start),options.verbose)
    
if __name__ == "__main__":
    main()
