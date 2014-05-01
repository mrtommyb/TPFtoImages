from __future__ import division, print_function

try:
    from astropy.io import fits as pyfits
except ImportError:
    try:
        import pyfits
    except ImportError:
        raise ImportError('You need astropy or pyfits modules')

import os
import numpy as np

def TPF2Im(filename,newdir=True):
    """
    Convert Kepler/K2 TPF to a bunch of images
    """
    with pyfits.open(filename) as f:
        objname = f[0].header['OBJECT']
        #replace spaces with underscore in objname
        objname = objname.replace (" ", "_")

        fluxarr = f[1].data['FLUX']
        cadnum = f[1].data['CADENCENO']
        time = f[1].data['TIME']
        quality = f[1].data['QUALITY']

        if newdir:
            outdir = objname
            try:
                os.stat(outdir)
            except:
                os.mkdir(outdir)
        else:
            outdir = '.'

        outname = np.array([],dtype=str)
        for num,image in enumerate(fluxarr):
            hdu = pyfits.PrimaryHDU(image)
            hdulist = pyfits.HDUList([hdu])

            hdulist.writeto('{0}/{1}-{2:05d}.fits'.format(outdir,objname,cadnum[num]))

            outname =  np.append(outname,'{0}-{1:05d}.fits'.format(objname,cadnum[num]))
        fmt = ['%s','%.9f','%i',]
        outarr = np.array([outname,time,quality]).T
        np.savetxt('{0}/{1}_filelist.txt'.format(outdir,objname), outarr,fmt='%s')


if __name__ == '__main__':
    ## test on my local machine if it works
    path = '../data'
    fn = path + '/kplr060017806-2014044044430_lpd-targ.fits'
    TPF2Im(fn)


