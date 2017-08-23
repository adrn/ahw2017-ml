"""
Combine the photoPosPlate and spPlate files into HDF5 files.
"""

# Standard library
import glob
import os
from os import path
import re

# Third-party
from astropy.table import Table
from astropy.io import ascii, fits
import numpy as np

# Project
from ahwpaths import (platelist_url, spPlate_base_fmt, spPlate_fmt,
                      specobj_base)

def main(download_path, overwrite):
    download_path = path.abspath(download_path)

    # Number of plates downloaded:
    spPlate_files = glob.glob(path.join(download_path, 'spPlate*.fit*'))
    n_plates = len(spPlate_files)
    print("{0} plates cached".format(n_plates))

    # Load a memmapped specObj file:
    specobj_hdul = fits.open(path.join(download_path, specobj_base),
                             memmap=True)

    # Get an array of all Plate, MJD
    spPlate_pattr = re.compile("spPlate-([0-9]+)-([0-9]+).fits")
    plates = []
    mjds = []
    for spPlate_fn in spPlate_files:
        res = spPlate_pattr.search(spPlate_fn)
        plate, mjd = map(int, res.groups())
        plates.append(plate)
        mjds.append(mjd)

    plates = np.array(plates)
    mjds = np.array(mjds)

    tmp_path = path.join(download_path, '_tmp_specObj.fits')
    if not path.exists(tmp_path):
        idx = np.in1d(specobj_hdul[1].data['PLATE'], plates)
        print(len(plates), idx.sum())

        tbl = specobj_hdul[1].data[idx]
        fits.writeto(tmp_path, tbl)

    tmp_tbl = fits.getdata(tmp_path)
    idx = np.zeros(len(tmp_tbl)).astype(bool)
    for p,m in zip(plates, mjds):
        idx |= (tmp_tbl['PLATE'] == p) & (tmp_tbl['MJD'] == m)

    tbl = Table(tmp_tbl[idx])

    for k in tbl.colnames:
        if tbl[k].dtype.type == np.str_:
            tbl[k] = tbl[k].astype('S')

    tbl.write(path.join(download_path, 'specObj-merged.hdf5'),
              path='/specObj', overwrite=True)

    os.remove(tmp_path)

if __name__ == "__main__":
    from argparse import ArgumentParser

    # Define parser object
    parser = ArgumentParser(description="")

    parser.add_argument('-p', '--path', dest='path', required=True,
                        type=str, help='Path to download and cache data to.')
    parser.add_argument('-o', '--overwrite', action='store_true',
                        dest='overwrite', default=False,
                        help='Destroy everything.')

    args = parser.parse_args()

    main(download_path=args.path, overwrite=args.overwrite)
