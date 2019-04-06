from astropy.io import fits
import sys

coadd = fits.open(sys.argv[1])
coadd[0].data = coadd[0].data[0:2048,0:2048]
coadd.writeto(sys.argv[1], overwrite=True)
