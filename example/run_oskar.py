import shutil

from astrokit.oskar import get_oskar_data, Oskar
from astrokit.utils import get_pwd, get_logger
from astrokit.image import Image


def init(task: str, logger):
    run_path = get_pwd(__file__)
    task_run = run_path / 'data' / task
    if not task_run.exists():
        task_run.mkdir(parents=True, exist_ok=True)
        shutil.copy(get_oskar_data('oskar_sim_interferometer.ini'), task_run)
        shutil.copy(get_oskar_data('oskar_imager.ini'), task_run)
        raise RuntimeError(f'A new settings file has been created, please configure.')
    result_path = task_run / 'result'
    vis_path = result_path / 'vis'
    image_path = result_path / 'image'
    ms_path = result_path / 'ms'
    vis_path.mkdir(parents=True, exist_ok=True)
    image_path.mkdir(parents=True, exist_ok=True)
    ms_path.mkdir(parents=True, exist_ok=True)
    logger.info(f'run_path: {run_path}')
    logger.info(f'task_run: {task_run.relative_to(run_path)}')
    logger.info(f'result_path: {result_path.relative_to(run_path)}')
    logger.info(f'vis_path: {vis_path.relative_to(run_path)}')
    logger.info(f'image_path: {image_path.relative_to(run_path)}')
    logger.info(f'ms_path: {ms_path.relative_to(run_path)}')
    return run_path, task_run, result_path, vis_path, image_path, ms_path


def get_settings(path, ini):
    return path / ini


def fits_show(image_name, run_path, **kwargs):
    fits_files = image_name.parent.glob(f'{image_name.name}_*.fits')
    for fits_file in fits_files:
        Image(fits_file).show(title=fits_file.relative_to(run_path), **kwargs)


def run():
    task = 'task1'
    logger = get_logger()
    run_path, task_run, result_path, vis_path, image_path, ms_path = init(task, logger)
    interferometer = get_settings(task_run, 'oskar_sim_interferometer.ini')
    imager = get_settings(task_run, 'oskar_imager.ini')
    logger.info(f'oskar_sim_interferometer.ini: {interferometer.relative_to(run_path)}')
    logger.info(f'oskar_imager.ini: {imager.relative_to(run_path)}')

    oskar = Oskar(run_path, use_singularity=False)

    # ==================== output file ==================================================
    num = len(list(vis_path.glob('*.vis')))
    output_file = f'%07d' % num

    # ==================== oskar_sim_interferometer =====================================
    oskar.use_task('oskar_sim_interferometer', interferometer)
    # your code
    vis_name = vis_path / (output_file + '.vis')
    oskar.set('interferometer/oskar_vis_filename', vis_name.relative_to(run_path))
    # run oskar_sim_interferometer task
    oskar.run(capture_output=True)

    # ==================== oskar_imager =================================================
    oskar.use_task('oskar_imager', imager)
    # your code
    image_name = image_path / output_file
    oskar.set('image/input_vis_data', vis_name.relative_to(run_path))
    oskar.set('image/root_path', image_name.relative_to(run_path))
    # run oskar_imager task
    oskar.run(capture_output=True)

    # show fits image
    fits_show(image_name, run_path)


if __name__ == '__main__':
    run()
