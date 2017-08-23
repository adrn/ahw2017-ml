from urllib.parse import urljoin

# To change the data release
DR = "dr14"

# URLs to get data
SAS_URL = "https://data.sdss.org/sas/"
DR_URL = urljoin(SAS_URL, DR) + "/"
platelist_url = urljoin(DR_URL, "eboss/spectro/redux/platelist.txt")

spPlate_base_fmt = "spPlate-{plate:04d}-{mjd:05d}.fits"
spPlate_fmt = urljoin(DR_URL, "eboss/spectro/redux/{run2d}/{plate:04d}/" +
                              spPlate_base_fmt)

photoPos_base_fmt = "photoPosPlate-{plate:04d}-{mjd:05d}.fits"
photoPos_fmt = urljoin(DR_URL, "eboss/spectro/redux/{run2d}/{plate:04d}/" +
                               photoPos_base_fmt)

specobj_base = "specObj-{0}.fits".format(DR)
