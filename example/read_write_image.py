from astrokit.image import Image
from astrokit.utils import get_astrokit_data, get_cwd

infile = get_astrokit_data('imagingm31_1.fits')
im = Image(infile)

# save image in different formats
save_path = get_cwd(__file__) / 'data/output'
save_path.mkdir(parents=True, exist_ok=True)
# fits image
fits_file = save_path / 'imagingm31_1.fits'
im.save(fits_file)
# tiff image
tiff_file = save_path / 'imagingm31_1.tiff'
im.save(tiff_file)
# png image
png_file = save_path / 'imagingm31_1.png'
im.save(png_file)
# jpg image
jpg_file = save_path / 'imagingm31_1.jpg'
im.save(jpg_file)
# npy image
npy_file = save_path / 'imagingm31_1.npy'
im.save(npy_file)

# read image in different formats
# fits image
Image(fits_file).show(title='FITS Image')
# tiff image
Image(tiff_file).show(title='TIFF Image')
# png image
Image(png_file).show(title='PNG Image')
# jpg image
Image(jpg_file).show(title='JPG Image')
# npy image
Image(npy_file).show(title='NPY Data File')
