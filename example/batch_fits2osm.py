import subprocess

from astrokit.utils import get_pwd, get_logger, get_file_list, get_path_name, get_astrokit_script

run_path = get_pwd(__file__) / 'test/oskar'
input_path = run_path.joinpath('fits')
output_path = run_path.joinpath('osm')
script = get_astrokit_script('fits2skymodel.py')

PARAMS = {
    # overwrite existing file
    # '--clobber': '',
    # [deg] R.A. of the image center (default: 0)
    # '--ra0': 0.0,
    # [deg] Dec. of the image center (default: -27)
    # '--dec0': -27.0,
    # image pixel size [arcsec]; (default: obtain from the FITS header 'PixSize')
    '--pixel-size': 20,
    # frequency [MHz] the image measured; (default: obtain from the FITS header 'FREQ')
    '--freq': 1450,
    # [K] minimum threshold to the output sky model (default: 1e-4, i.e., 0.1 mK)
    # '--min-value': 1e-4,
    # [K] maximum threshold to the output sky model (default: inf)
    # '--max-value': np.inf,
    # use a mask to determine the output sky model (NOTE: will override --min-value and --max-value)
    # '--mask': '',
    # save a FITS version of the converted sky model
    # '--osm-fits': '',
    # output directory for sky model files (default: current working directory)
    # '--outdir': '',
    # create a FITS mask for the output sky model
    # '--create-mask': '',
    # input FITS image
    # 'infile': '',
    # output OSKAR sky model (default: same basename as the input FITS image)
    # 'outfile': ''
}


def run():
    logger = get_logger()
    output_path.mkdir(parents=True, exist_ok=True)
    args = []
    for key, value in PARAMS.items():
        args.append(key)
        args.append(str(value))
    logger.info(f'Converting fits files from {input_path} to osm files in {output_path}')
    logger.info(f'Using script {script}')
    logger.info(f'Using params {args}')
    logger.info(f'==================================================')
    for _fits in get_file_list(input_path, '*.fits'):
        osm = output_path / _fits.name
        osm = osm.with_suffix('.osm')
        if osm.exists():
            logger.info(f'{osm.name} already exists. Skipping...')
            continue
        logger.info(f'Converting {_fits.name} to {osm.name}')
        subprocess.run(['python', get_path_name(script), get_path_name(_fits), get_path_name(osm)] + args)
    logger.info(f'==================================================')
    logger.info(f'All done!')


if __name__ == '__main__':
    run()
