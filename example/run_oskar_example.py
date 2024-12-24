from astrokit.image import Image
from astrokit.oskar import Oskar
from astrokit.utils import get_cwd, get_astrokit_data
import shutil


def run():
    # create test directory
    oskar_path = get_cwd(__file__) / 'data/oskar'
    if not oskar_path.exists():
        oskar_path.mkdir(parents=True, exist_ok=True)

    # copy oskar running data to test directory
    interferometer = oskar_path / 'oskar_sim_interferometer.ini'
    shutil.copy(get_astrokit_data('oskar_sim_interferometer.ini'), interferometer)
    shutil.copy(get_astrokit_data('sky.osm'), oskar_path / 'sky.osm')
    shutil.copytree(get_astrokit_data('telescope.tm'), oskar_path / 'telescope.tm', dirs_exist_ok=True)
    imager = oskar_path / 'oskar_imager.ini'
    shutil.copy(get_astrokit_data('oskar_imager.ini'), imager)

    # init OSKAR
    # if you want to use singularity, set use_singularity=True
    oskar = Oskar(oskar_path, use_singularity=False)

    # oskar_sim_interferometer task
    # set oskar_sim_interferometer task
    oskar.use_task('oskar_sim_interferometer', interferometer, check=False)
    # update oskar_sim_interferometer settings
    oskar.set('sky/oskar_sky_model/file', 'sky.osm')
    oskar.set('telescope/input_directory', 'telescope.tm')
    oskar.set('interferometer/oskar_vis_filename', 'example.vis')
    # run oskar_sim_interferometer task
    oskar.run()

    # oskar_imager task
    # set oskar_imager task
    oskar.use_task('oskar_imager', imager, check=False)
    # update oskar_imager settings
    oskar.set('image/input_vis_data', 'example.vis')
    oskar.set('image/root_path', 'example')
    # run oskar_imager task
    oskar.run()

    # show fits image
    fits_files = oskar_path.glob('example*.fits')
    for fits_file in fits_files:
        Image(fits_file).show(title=fits_file.relative_to(oskar_path), save_name=[
            fits_file.with_suffix('.svg'),
        ])


if __name__ == '__main__':
    run()
