from astropy.io import fits
from astropy import wcs
from astropy.coordinates import SkyCoord
import pyds9
import sys
import astropy.units as u

p = pyds9.DS9('foo')
p.set('file coadd.fits')
p.set('scale zscale')

coadd = fits.open('coadd.fits')
cw = wcs.WCS(coadd[0].header)
for i in [2, 4, 5, 6, 7]:
    frame = fits.open('DAS{}_{}.new'.format(i, sys.argv[1]))
    w = wcs.WCS(frame[0].header)

    ra, dec = w.all_pix2world(1024, 1024, 0, ra_dec_order=True)
    x, y = cw.all_world2pix(ra, dec, 1)
    p.set('regions', 'circle({:.6f},{:.6f},1) # color=red text=D{}'.format(
                        x, y, i
    ))

    ra, dec = w.all_pix2world([0, 0, 2048, 2048], [0, 2048, 2048, 0], 0, ra_dec_order=True)
    x, y = cw.all_world2pix(ra, dec, 1)

    for j in [0, 1, 2, 3]:
        p.set('regions', 'line({:.6f},{:.6f},{:.6f},{:.6f}) # color=yellow'.format(
                            x[j], y[j], x[(j + 1) % 4], y[(j + 1) % 4]
        ))

    if i == 2:
        s = SkyCoord(frame[0].header['TEL-RA'], frame[0].header['TEL-DEC'], unit=(u.hourangle, u.deg))
        x, y = cw.all_world2pix(s.ra.to(u.deg).value, s.dec.to(u.deg).value, 1)
        p.set('regions', 'circle({:.6f},{:.6f},50) # color=green text=MNT'.format(
                            x, y
        ))
