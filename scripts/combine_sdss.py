"""
Combine the photoPosPlate and spPlate files into HDF5 files.
"""

# Standard library
import glob
import os
from os import path
import re

# Third-party
import h5py
from astropy.table import Table
from astropy.io import ascii, fits
import numpy as np

# Project
from ahwpaths import (platelist_url, spPlate_base_fmt, spPlate_fmt,
                      photoPos_base_fmt, photoPos_fmt)

def get_wave_arr(header):
    npix = header['NAXIS1']
    c0 = header['COEFF0']
    c1 = header['COEFF1']
    return 10**(c0 + c1*np.arange(npix))

def main(download_path, overwrite):
    download_path = path.abspath(download_path)

    # Number of plates downloaded:
    spPlate_files = glob.glob(path.join(download_path, 'spPlate*.fit*'))
    n_plates = len(spPlate_files)
    print("{0} plates cached".format(n_plates))

    # Merged files to store all data:
    spPlate_merged_fn = path.join(download_path, 'spPlate-merged.hdf5')
    photoPos_merged_fn = path.join(download_path, 'photoPosPlate-merged.hdf5')

    if path.exists(spPlate_merged_fn) or path.exists(photoPos_merged_fn):
        print("Merged files already exist - deleting.")

        for fn in [spPlate_merged_fn, photoPos_merged_fn]:
            try:
                os.remove(fn)
            except OSError:
                pass

    # First, we go through all files and figure out the min/max wavelength
    # values to select to get all spectra on a common wavelength grid. This
    # slightly truncates some of the spectra, but we don't lose many pixels.
    wave_mins = []
    wave_maxs = []

    for fn in spPlate_files:
        hdr = fits.getheader(fn, 0)
        wave = get_wave_arr(hdr)
        wave_mins.append(wave.min())
        wave_maxs.append(wave.max())

    wave_min = max(wave_mins)
    wave_max = min(wave_maxs)

    i1, = np.where(np.isclose(wave, wave_min))[0]
    i2, = np.where(np.isclose(wave, wave_max))[0]
    n_wave = i2-i1

    # Create HDF5 file with resizable datasets to store the spPlate data
    with h5py.File(spPlate_merged_fn, 'a') as f:
        f.create_dataset('flux', (0, n_wave), maxshape=(None, n_wave))
        f.create_dataset('ivar', (0, n_wave), maxshape=(None, n_wave))
        f.create_dataset('wave', data=wave[i1:i2])

    # Create HDF5 file to store the photoPosPlate data
    photoPos_fn = glob.glob(path.join(download_path, 'photoPosPlate*.fits'))[0]

    # Now we load the data
    spPlate_pattr = re.compile("spPlate-([0-9]+)-([0-9]+).fits")
    all_photoPos_data = []
    for spPlate_fn in spPlate_files:
        res = spPlate_pattr.search(spPlate_fn)
        plate, mjd = map(int, res.groups())
        photoPos_fn = path.join(download_path,
                                photoPos_base_fmt.format(plate=plate, mjd=mjd))

        # Load data from this spPlate file
        flux_data = fits.getdata(spPlate_fn, 0)
        ivar_data = fits.getdata(spPlate_fn, 1)
        wave_data = get_wave_arr(fits.getheader(spPlate_fn, 0))

        i1, = np.where(np.isclose(wave_data, wave_min))[0]
        i2, = np.where(np.isclose(wave_data, wave_max))[0]

        with h5py.File(spPlate_merged_fn, 'a') as f:
            n_flux, n_pix = f['flux'].shape

            f['flux'].resize((n_flux + flux_data.shape[0], n_pix))
            f['ivar'].resize((n_flux + ivar_data.shape[0], n_pix))

            f['flux'][n_flux:, :] = flux_data[:, i1:i2]
            f['ivar'][n_flux:, :] = ivar_data[:, i1:i2]

        # Load data from this photoPosPlate file
        pPP_data = fits.getdata(photoPos_fn)
        all_photoPos_data.append(pPP_data)

    # TODO: might need to deal with unicode -> string bullshit
    photoPos = Table(np.lib.recfunctions.stack_arrays(all_photoPos_data,
                                                      autoconvert=True,
                                                      usemask=False))
    photoPos.write(photoPos_merged_fn)

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
