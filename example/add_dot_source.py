from src.astrokit.image import Image
from src.astrokit.utils import get_image_data

infile = get_image_data('imagingm31_1.fits')
im = Image(infile)
im.show(title='Original Image')
# add fixed dot source
im.add_dot_source(x=100, y=100, power=10)
im.show(title='Image with Fixed Dot Source')
# add random dot source
im.add_dot_source(num=100, power=10)
im.show(title='Image with Random Dot Source')