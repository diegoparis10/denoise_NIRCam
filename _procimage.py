#! /usr/bin/python3

# *****************************************************************************
#
# Filename    :    _procimage.py
# Description :    Functions to process and denoise image(s)
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
from _config import *
from _iofunc import *
from _setdetparams import *
from _writefits import *
from ctypes import *
import warnings
warnings.filterwarnings("ignore", message="All-NaN slice encountered")

so_file=os.path.dirname(os.path.realpath(__file__))+"/core.so"
functions=CDLL(so_file)

def mk_obm(sci,bpm,fwhm,det_sigma,dilation,factor,min_isoarea,v):
    SEX=loadSEX()
    sexconf,sexcatparam,sexnnw = loadSEXConf()
    conv = mk_kern()
    verbSEX="-VERBOSE_TYPE QUIET"
    if (v):
        verbSEX="-VERBOSE_TYPE NORMAL"
    msk = re.sub('.fits?$', '.msk.fits', sci)
    obm = re.sub('.fits?$', '.obm.fits', sci)
    wht = re.sub('.fits?$', '.wht.fits', sci)
    sgm = re.sub('.fits?$', '.sgm.fits', sci)
    flag= re.sub('.fits?$', '.flg.fits', sci)
    cat= re.sub('.fits?$', '.cat', sci)
    if os.path.isfile(msk):
        os.remove(msk)
    if os.path.isfile(obm):
        os.remove(obm)
    if os.path.isfile(wht):
        os.remove(wht)
    if os.path.isfile(flag):
        os.remove(flag)
    detectMinArea = getDetectMinArea(fwhm)
    detectThresh = getDetectThresh(det_sigma,detectMinArea)
    analysisThresh = detectThresh
    wht = getWht(bpm,wht)
    cmd = "%s %s -c %s -PARAMETERS_NAME %s -STARNNW_NAME %s -CATALOG_TYPE ASCII_HEAD -CATALOG_NAME %s -CHECKIMAGE_TYPE SEGMENTATION -CHECKIMAGE_NAME %s -DETECT_MINAREA %f -DETECT_THRESH %f  -ANALYSIS_THRESH %f  -FILTER_NAME %s -WEIGHT_TYPE MAP_WEIGHT -WEIGHT_IMAGE %s -MEMORY_OBJSTACK  40000 -MEMORY_PIXSTACK  4000000 -MEMORY_BUFSIZE 4096 -DEBLEND_MINCONT 1 %s" % (SEX,sci,sexconf,sexcatparam,sexnnw,cat,sgm,detectMinArea,detectThresh,analysisThresh,conv,wht,verbSEX)
    os.popen(cmd).read()
    flag = getFlag(sgm,flag)
    verb("Dilating sources mask... ",v)
    functions.dilate(flag.encode(),msk.encode(),dilation,factor,3,(1 if v else 0))
    verb("\nDone... ",v)
    verb("Checking for the presence of very extended objects (ISOAREA_IMAGE>%d) in image..." % min_isoarea,v)
    if (checkIsoarea(cat,min_isoarea)):
        verb("Yes... Re-detecting only extended objects... ",v)
        mskEO = re.sub('.fits?$', '.msk.EO.fits', sci)
        sgmEO = re.sub('.fits?$', '.sgm.EO.fits', sci)
        flagEO= re.sub('.fits?$', '.flg.EO.fits', sci)
        catEO= re.sub('.fits?$', '.EO.cat', sci)
        cmd = "%s %s -c %s -PARAMETERS_NAME %s -STARNNW_NAME %s -CATALOG_TYPE ASCII_HEAD -CATALOG_NAME %s -CHECKIMAGE_TYPE SEGMENTATION -CHECKIMAGE_NAME %s -DETECT_THRESH %f  -ANALYSIS_THRESH %f -DETECT_MINAREA %d -FILTER_NAME %s -WEIGHT_TYPE MAP_WEIGHT -WEIGHT_IMAGE %s -MEMORY_OBJSTACK  40000 -MEMORY_PIXSTACK  4000000 -MEMORY_BUFSIZE 4096 -DEBLEND_MINCONT 1 %s" % (SEX,sci,sexconf,sexcatparam,sexnnw,catEO,sgmEO,detectThresh,analysisThresh,min_isoarea,conv,wht,verbSEX)
        os.popen(cmd).read()
        flagEO = getFlag(sgmEO,flagEO)
        verb("Dilating extended sources mask. This may take some time... ",v)
        functions.dilate(flagEO.encode(),mskEO.encode(),dilation,factor,9,(1 if v else 0))
        verb("\nDone... ",v)
        msk = logical_OR(msk,mskEO)
    os.remove(sexconf)
    os.remove(sexcatparam)
    os.remove(sexnnw)
    os.remove(conv)
    return(getObm(msk,bpm,obm))

def denoise_1of(sci,bpm,fwhm,sigma,dilation,min_isoarea,factor,amp,outsuffix,c,v):
    obm=re.sub('.fits?$', '.obm.fits', sci)
    vstripe=re.sub('.fits?$', '.vstr.fits', sci)
    if not os.path.isfile(obm):
        obm = mk_obm(sci,bpm,fwhm,sigma,dilation,factor,min_isoarea,v)
    outimage=re.sub('.fits?$', outsuffix, sci)
    obmdata=fits.getdata(obm)
    scidata=fits.getdata(sci)
    sciheader=fits.getheader(sci)
    bkgdata=np.where(obmdata<0.5, scidata, np.NAN)
    bkgdata=np.transpose(bkgdata)
    outdata=scidata.copy()
    verb("Removing vertical stripes...",v)
    outdata = np.transpose(outdata)
    for k in range(len(outdata)):
        mean =  np.nanmedian(bkgdata[k])
        if not np.isnan(mean):
            outdata[k] -= mean
    outdata = np.transpose(outdata)
    verb("Done",v)
    hdu = fits.PrimaryHDU()
    hdu.header = sciheader
    hdu.data = np.float32(outdata)
    if os.path.isfile(vstripe):
        os.remove(vstripe)
    fits.writeto(vstripe,hdu.data,header=hdu.header)
    vstrdata=fits.getdata(vstripe)
    bkg1data=np.where(obmdata<0.5, vstrdata, np.NAN)
    outdata=vstrdata.copy()
    verb("Removing horizontal stripes...",v)
    if (amp):
        n=sciheader['NAXIS1']
        r7=n-1
        r6=int(n*3/4)
        r5=r6-1
        r4=int(n/2)
        r3=r4-1
        r2=int(n/4)
        r1=r2-1
        r0=0
    for k in range(len(outdata)):
        if not amp:
            mean =  np.nanmedian(bkg1data[k])
            if not np.isnan(mean):
                outdata[k] -= mean
        else:
            mean1=np.nanmedian(bkg1data[k][r0:r1])
            mean2=np.nanmedian(bkg1data[k][r2:r3])
            mean3=np.nanmedian(bkg1data[k][r4:r5])
            mean4=np.nanmedian(bkg1data[k][r6:r7])
            if not np.isnan(mean1):
                outdata[k][r0:r1] -= mean1
            if not np.isnan(mean2):
                outdata[k][r2:r3] -= mean2
            if not np.isnan(mean3):
                outdata[k][r4:r5] -= mean3
            if not np.isnan(mean4):
                outdata[k][r6:r7] -= mean4
    verb("Done",v)
    hdu1 = fits.PrimaryHDU()
    hdu1.header = sciheader
    hdu1.data = np.float32(outdata)
    fits.writeto(outimage,hdu1.data,header=hdu1.header)
    if (c):
        dq = re.sub('.fits?$', '.dq.fits', sci)
        msk = re.sub('.fits?$', '.msk.fits', sci)
        mskEO = re.sub('.fits?$', '.msk.EO.fits', sci)
        wht = re.sub('.fits?$', '.wht.fits', sci)
        sgm = re.sub('.fits?$', '.sgm.fits', sci)
        sgmEO = re.sub('.fits?$', '.sgm.EO.fits', sci)
        flg = re.sub('.fits?$', '.flg.fits', sci)
        flgEO= re.sub('.fits?$', '.flg.EO.fits', sci)
        cat = re.sub('.fits?$', '.cat', sci)
        catEO = re.sub('.fits?$', '.EO.cat', sci)
        sci1fc =  re.sub('.fits?$', outsuffix, sci)
        os.remove(sci)
        os.remove(bpm)
        os.remove(msk)
        os.remove(obm)
        os.remove(wht)
        os.remove(sgm)
        os.remove(flg)
        os.remove(cat)
        os.remove(dq)
        os.remove(vstripe)
        os.remove(sci1fc)
        if os.path.isfile(mskEO):
            os.remove(mskEO)
        if os.path.isfile(sgmEO):
            os.remove(sgmEO)
        if os.path.isfile(flgEO):
            os.remove(flgEO)
        if os.path.isfile(catEO):
            os.remove(catEO)
    return(hdu1)
