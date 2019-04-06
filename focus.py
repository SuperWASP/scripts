from astropy.io import fits
from astropy import wcs
from astropy.coordinates import SkyCoord
import pyds9
import sep
import sys
import astropy.units as u
import numpy as np

p = pyds9.DS9('foo')
p.set('file ' + sys.argv[1])
p.set('scale zscale')

frame = fits.open(sys.argv[1])

image = frame[0].data.astype(float)
bkg = sep.Background(image)
subtracted = image - bkg

thresh = 5 * bkg.globalrms
raw_objects = sep.extract(subtracted, thresh)

objects = []
for star in raw_objects:
    # Discard spuriously small sources
    if star['npix'] < 9:
        continue

    x = star['x']
    y = star['y']
    a = star['a']
    b = star['b']

    try:
        theta = star['theta']
        kronrad, flag = sep.kron_radius(subtracted, x, y, a, b, theta, 6.0)
        if flag != 0:
            continue

        flux, _, flag = sep.sum_ellipse(subtracted, x, y, a, b, theta, 2.5 * kronrad,
                                        subpix=0)
        if flag != 0:
            continue

        r, flag = sep.flux_radius(subtracted, x, y, 6.0 * a, 0.5,
                                  normflux=flux, subpix=5)
        if flag != 0:
            continue

        objects.append((x, y, r))
    except Exception:
        # Ignore errors in individual objects
        pass

TILES = 8
STEP = 2048 // TILES

for j in range(TILES):
    for i in range(TILES):
        filt = []
        for o in objects:
            if STEP * i < o[0] < STEP * (i + 1) and STEP * j < o[1] < STEP * (j + 1):
                filt.append(o[2])

        p.set('regions', 'box({0:.6f},{1:.6f},{2},{2}) # color=yellow'.format(
              (i + 0.5) * STEP, (j + 0.5) * STEP, STEP))
        p.set('regions', 'text {0:.6f} {1:.6f} # color=red text="{2:.2f}"'.format(
              (i + 0.5) * STEP, (j + 0.5) * STEP, np.median(filt)))

