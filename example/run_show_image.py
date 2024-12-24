from astrokit.utils import get_astrokit_data
from astrokit.image import Image

infile = get_astrokit_data('imagingm31_1.fits')
im = Image(infile)
im.show(title='M31', cmap='jet')
