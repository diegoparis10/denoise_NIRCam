# denoise_NIRCam

Package to remove 1/f stripes from NIRCam calibrated images

Description: 

1/f noise introduces random vertical and horizontal stripes into the JWST NIRCam images. 

*denoise_NIRCam* has been developed to remove stripes from each row/column subtracting its median value, obtained
masking objects and DQ-flagged pixels as better as possible. The object masks are obtained 
by running SExtractor (Bertin & Arnouts 1996) and then dilating the resulting segmentation image, applying 
a careful procedure to dilate objects depending on their ISOAREA: the segmentation of objects having an ISOAREA 
lower than the desired threshold is dilated using a 3x3 convolution kernel and the desired dilation d in 
pixels, while for the segmentation of objects having an ISOAREA greater than the threshold a 9x9 convolution 
kernel and a dilation of (m x d) pixels is applied, being m a desired multiplicative factor to apply to the 
desired dilation d.

The procedure is executed over entire columns and can be executed separately for each amplificator row or over 
the entire rows. The entire rows modality is recommended in presence of denser areas containing extended objects 
(clusters and/or bright field stars).

Processing parameters are passed as command line options and the defaults are expressed inside brackets. 
Boolean options do not need arguments, calling or not calling a boolean option means 'True' or 'False' 
respectively. The defaults of boolean options are expressed in curly braces.

Here is the complete list:

# Usage: 

    denoise_NIRCam.py [ -h | --help ]

    denoise_NIRCam.py [ -V | --version ]

    denoise_NIRCam.py [-o OUTSUFFIX] [-a] [-d DILATION] [-f FWHM] [-i ISOAREA] [-k] [-m MFACTOR] [-p] [-s DETECT_SIGMA] [-v] image1 image2 ... imageN [@filelist]

# Options:


    -h, --help            show this help message and exit
    -o OUTSUFFIX, --outsuffix=OUTSUFFIX
                          The suffix for output images [.dn.fits]
    -a, --amp             Correct background stripes for each amplifier? If
                          False, the corrective medians of background stripes are 
                          computed along the entire horizontal axis {False}
    -d DILATION, --dilation=DILATION
                          The dilation in pixels to flag sources [5]
    -f FWHM, --fwhm=FWHM  The fwhm in pixels [4]
    -i ISOAREA, --isoarea=ISOAREA
                          The minimum area to mask extended objects [4000]
    -k, --keepall         Keep all flags in DQ layer? If False,
                          only pixels that are marked as 'DO NOT USE' are
                          discarded [False]
    -m MFACTOR, --mfactor=MFACTOR
                          The factor used to multiply the dilation of extended
                          object mask [4]
    -p, --purge           Purge temporary intermediate files? {False}
    -s DETECT_SIGMA, --detect_sigma=DETECT_SIGMA
                          The sigma used to detect sources [4]
    -v, --verbose         Verbose output [False]
    -V, --version         Print program version number, then quit.

# Tips:

The use of the '-k' option is highly recommended, in order to discard outliers in the median estimates as much as possible. 
The sigma for detection should not be chosen too low, to avoid spurious detections (e.g. parts of stripes or even entire stripes, which have 
to be removed and not masked) nor too high to miss many detections of real sources. 

# Run:

A typical Linux command line, using a dilation=5 pixels with mfactor=4x and a minimum isoarea=5000 pixels to mask extended objects, looks like:

    denoise_NIRCam.py -i 5000 -k -d 5 -m 4 -p -v jw_cal.fits 
    
# Result:

Here is a typical NIRCam image before (left) and after (right) the 1/f denoising:

<img src="https://user-images.githubusercontent.com/68115391/222123579-fe481925-48cf-4468-9fe5-c6e16672ccb4.jpeg" width="750" />



# Acknowledging denoise_NIRCam:

If you use the code for publishing purposes, please consider to add the following papers among citations:

- Paris, D., Merlin, M., Fontana A. & al. 2023: arXiv e-prints, arXiv:2301.02179. [https://arxiv.org/abs/2301.02179]

- Merlin, E., Bonchi, A., Paris, D., et al. 2022, A&A, 938,827 L14, doi: http://doi.org/10.3847/2041-8213/ac8f93

- Bertin, E., & Arnouts, S. 1996, A&AS, 117, 393 [https://ui.adsabs.harvard.edu/abs/1996A%26AS..117..393B/abstract]

