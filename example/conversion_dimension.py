from astrokit.image import Image
from astrokit.utils import get_astrokit_data
from copy import copy

# Read the original image
infile = get_astrokit_data('imagingm31_1.fits')
im = Image(infile)
print(f'Shape of the original image: {im.shape}')
# copy image
im2 = copy(im)
print(f'Shape of the copy image: {im2.shape}')
# Read image data
data1 = im2.get_data()
data2 = im2.data
print(f'Data shape obtained using .get_data(): {data1.shape}')
print(f'Data shape obtained using .data: {data2.shape}')
# Dimensioning the image, ascending from the higher dimensions
im2.set_data(data1[..., None])
print(f'Shape of the image after dimensional uplift: {im2.shape}')
# Dimensioning the image, ascending from the lower dimensions
im2.set_data(data1[None, ...])
print(f'Shape of the image after dimensional uplift: {im2.shape}')
