from astrokit.utils import get_image_data
from astrokit.image import Image

infile = get_image_data('imagingm31_1.fits')
im = Image(infile)
im.show()
