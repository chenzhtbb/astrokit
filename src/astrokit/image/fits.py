import pathlib
import matplotlib.pyplot as plt
import numpy as np
from .noise import add_dot_source
from astropy.io import fits
from astropy.wcs import WCS
from tifffile import tifffile
from PIL import Image as PILImage

from astrokit.utils import normalize


class Image(object):
    file = None
    hdu = None
    data = None
    header = {}
    shape = None
    image_type = None

    def __init__(self, file=None, data=None, header=None, **kwargs):
        if kwargs.get('dtype', np.float32) is not None:
            self.dtype = kwargs.get('dtype')
        if file is not None:
            if type(file) is str:
                file = pathlib.Path(file)
            self.image_type = file.suffix
            self.file = pathlib.Path(file)
            if self.image_type == '.fits':
                self.load_image_from_fits()
            elif self.image_type in ['.tiff', '.tif']:
                self.load_image_from_tiff(header)
            elif self.image_type == '.npy':
                self.load_image_from_npy(header)
            else:
                self.load_image(header)
        elif data is not None:
            self.data = data
            self.init_fits_image(data, header)
        else:
            raise ValueError('file or data must be provided')

    def load_image_from_fits(self):
        self.hdu = fits.open(self.file)
        self.data = np.array(self.hdu[0].data, dtype=self.dtype)
        self.header = self.hdu[0].header
        self.shape = self.data.shape
        self.hdu.close()

    def load_image_from_tiff(self, header):
        self.data = tifffile.imread(self.file)
        self.init_fits_image(self.data, header)

    def load_image_from_npy(self, header):
        self.data = np.load(self.file)
        self.init_fits_image(self.data, header)

    def load_image(self, header):
        with PILImage.open(self.file) as data:
            self.data = np.array(data)
        self.init_fits_image(self.data, header)

    def init_fits_image(self, data, header=None):
        self.data = np.array(np.flipud(data), dtype=self.dtype)
        self.shape = data.shape
        if header is None:
            header = {}
        header['WCSAXES'] = len(self.shape)
        header['CTYPE1'] = 'RA---SIN'
        header['CTYPE2'] = 'DEC--SIN'
        header['CRPIX1'] = np.floor(self.shape[0] / 2 + 1)
        header['CRPIX2'] = np.floor(self.shape[0] / 2 + 1)
        header['CRVAL1'] = 15.0
        header['CRVAL2'] = -45.0
        header['CDELT1'] = -0.054539420584031
        header['CDELT2'] = 0.054539420584031
        header['CUNIT1'] = 'deg'
        header['CUNIT2'] = 'deg'

        self.header = fits.Header(header)

    def show(self, **kwargs):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection=kwargs.get('wcs', None))
        im = ax.imshow(np.squeeze(self.data),
                       cmap=kwargs.get('cmap', 'viridis'),
                       origin='lower',
                       )
        ax.set_title(kwargs.get('title', str(self.file)))
        if kwargs.get('color_bar', True):
            fig.colorbar(im)
        if kwargs.get('show', True):
            fig.show()
        if kwargs.get('save_name', None) is not None:
            save_list = kwargs.get('save_name')
            if type(save_list) is not list:
                save_list = [save_list]
            for save_name in save_list:
                fig.savefig(save_name, dpi=kwargs.get('dpi', 100))

    def show_fits(self, **kwargs):
        self.show(wcs = WCS(self.header).sub(2),**kwargs)

    def get_data(self):
        return np.flipud(np.squeeze(self.data))

    def save(self, filename):
        suffix = filename.suffix
        data = self.get_data()
        if suffix == '.fits':
            hdu = fits.PrimaryHDU(self.data, header=self.header)
            hdu.writeto(filename, overwrite=True)
        elif suffix in ['.tiff', '.tif']:
            tifffile.imwrite(filename, data, shape=data.shape)
        elif suffix == '.npy':
            np.save(filename, data)
        else:
            img = normalize(data) * 255
            img = PILImage.fromarray(img.astype(np.uint8), mode='L')
            img.save(filename)

    def add_noise(self, noise_type='dot-source', **kwargs):
        if noise_type == 'dot-source':
            self.add_dot_source(**kwargs)

    def add_dot_source(self, **kwargs):
        data = add_dot_source(self.get_data(), **kwargs)
        data = np.flipud(data)
        for _ in range(len(self.shape) - len(data.shape)):
            data  = data[np.newaxis, ...]
        self.data = data

