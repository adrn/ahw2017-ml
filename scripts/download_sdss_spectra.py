"""
- Read platelist from here:
https://data.sdss.org/sas/dr14/eboss/spectro/redux/platelist.txt
"""

# Standard library
import os
from os import path
from urllib.request import urlopen
from urllib.error import HTTPError

# Third-party
from astropy.io import ascii, fits
import numpy as np

# Project
from ahwpaths import (platelist_url, spPlate_base_fmt, spPlate_fmt,
                      photoPos_base_fmt, photoPos_fmt)

def download_file(url, local_path):
    try:
        with open(local_path, 'wb') as f:
            with urlopen(url) as resp:
                f.write(resp.read())

    except HTTPError as e:
        print("Error {0}: Failed to download {1}".format(e.code, url))
        os.unlink(local_path)

def main(download_path, overwrite):
    download_path = path.abspath(download_path)

    # Number of plates worth of data to download
    n_plates = 100

    # Random number seed used to pick which plates to download
    seed = 42
    np.random.seed(seed)

    # First, download the platelist file and read all Good plates
    platelist_file = path.join(download_path, 'platelist.txt')
    if not path.exists(platelist_file) or overwrite:
        with open(platelist_file, 'wb') as f:
            http_resp = urlopen(platelist_url)
            f.write(http_resp.read())

    tbl = ascii.read(platelist_file)

    # Get some random "good" plates with high S/N
    skip_plates = [] # determined to be bad
    tbl = tbl[(tbl['QUALITY'] == 'good') & (tbl['SN^2'] > 20) &
              np.logical_not(np.in1d(tbl['PLATE'], skip_plates))]

    # Unique on plate number
    _, idx = np.unique(tbl['PLATE'], return_index=True)
    tbl = tbl[idx]
    tbl = tbl[np.random.choice(len(tbl), size=n_plates, replace=False)]

    tot = 0
    for key in ['N_gal', 'N_QSO', 'N_star', 'N_unk', 'N_sky']:
        print(key, tbl[key].sum())
        tot += tbl[key].sum()
    print("total:", tot)

    # Construct URLs for the plate files to download
    for row in tbl:
        spPlate_url = spPlate_fmt.format(run2d=row['RUN2D'],
                                         plate=row['PLATE'],
                                         mjd=row['MJD'])
        photoPos_url = photoPos_fmt.format(run2d=row['RUN2D'],
                                           plate=row['PLATE'],
                                           mjd=row['MJD'])

        spPlate_local_path = path.join(
            download_path, spPlate_base_fmt.format(plate=row['PLATE'],
                                                   mjd=row['MJD']))
        photoPos_local_path = path.join(
            download_path, photoPos_base_fmt.format(plate=row['PLATE'],
                                                    mjd=row['MJD']))

        if path.exists(spPlate_local_path) and not overwrite:
            print("spPlate {0} already exists locally".format(row['PLATE']))

        else:
            print("Downloading spPlate {0}".format(row['PLATE']))
            try:
                download_file(spPlate_url, spPlate_local_path)
            except Exception as e:
                print("failed to download spPlate {0}: \n {1}"
                      .format(row['PLATE'], str(e)))
                continue

            hdulist = fits.open(spPlate_local_path)
            hdulist[0:2].writeto(spPlate_local_path, overwrite=True,
                                 output_verify='ignore')
            hdulist.close()

        # TODO: duplicate code
        if path.exists(photoPos_local_path) and not overwrite:
            print("photoPosPlate {0} already exists locally"
                  .format(row['PLATE']))

        else:
            print("Downloading photoPosPlate {0}".format(row['PLATE']))
            download_file(photoPos_url, photoPos_local_path)

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
