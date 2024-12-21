from astrokit.utils import get_pwd

from astrokit.image import Image
run_path = get_pwd(__file__)
fitsfile = run_path / 'test/oskar/example_I.fits'
im = Image(fitsfile)
im.show()
im.add_dot_source(num=100, power=5)
im.show()