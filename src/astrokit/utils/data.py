from pathlib import Path

import requests
import wget
import zipfile

from . import get_pwd, get_path_name


def get_astrokit_path():
    return get_pwd(__file__)

def get_astrokit_script(name: str):
    script = get_pwd(__file__) / 'scripts' / name
    if script.exists():
        return script
    raise FileNotFoundError(f'{script} not found!')

def get_astrokit_data(name: str):
    check_data()
    data = get_astrokit_path() / 'data' / name
    if data.exists():
        return data
    raise FileNotFoundError(f'{data} not found!')

def get_oskar_data(name: str):
    file = get_astrokit_data('oskar') / name
    if file.exists():
        return file
    raise FileNotFoundError(f'{file} not found!')

def get_image_data(name: str):
    file = get_astrokit_data('image') / name
    if file.exists():
        return file
    raise FileNotFoundError(f'{file} not found!')

def get_astrokit_example(download_path: str | Path, directory_name='example'):
    if not isinstance(download_path, Path):
        download_path = Path(download_path)
    download_path = download_path / directory_name
    download_path.mkdir(parents=True, exist_ok=True)

    url = r'https://api.github.com/repos/chenzhtbb/astrokit/contents/example'
    example_file_list = requests.get(url)
    if example_file_list.status_code == 200:
        example_file_list = example_file_list.json()
    else:
        raise Exception('Failed to get astrokit example file list from github.')

    for file in example_file_list:
        if file['type'] == 'file':
            file_name = file['name']
            file_url = file['download_url']
            file_content = requests.get(file_url)
            if file_content.status_code == 200:
                with open(download_path / file_name, 'wb') as f:
                    f.write(file_content.content)
            else:
                raise Exception(f'Failed to download {file_name} from github.')
    print(f'Download astrokit example files to {download_path} successfully.')

def check_data():
    data_path = get_astrokit_path() / 'data'
    if not data_path.exists():
        print('Data not found, start to download data...')
        update_data()

def update_data():
    files = []
    files += update_oskar_data()
    files += update_fits_data()
    for file in files:
        download_path = get_astrokit_path() / file['path']
        download_path.mkdir(parents=True, exist_ok=True)
        filepath = download_path / file['name']
        if not filepath.exists():
            download_file(file['url'], download_path)
        if file['type'] == 'zip':
            unzip_file(filepath, download_path)

def update_oskar_data():
    return [
        {'name': 'OSKAR-2.7-Example-Data.zip', 'path': 'data/oskar', 'url': 'https://github.com/OxfordSKA/OSKAR/files/1984210/OSKAR-2.7-Example-Data.zip', 'type': 'zip'},
    ]

def update_fits_data():
    return [
        {'name': 'imagingm31_1.fits', 'path': 'data/image', 'url': '', 'type': 'fits'},
    ]

def download_file(url: str, path: str | Path):
    if not isinstance(path, Path):
        path = Path(path)
    wget.download(url, get_path_name(path))

def unzip_file(zip_file: str | Path, extract_path: str | Path):
    if not isinstance(zip_file, Path):
        zip_file = Path(zip_file)
    if not isinstance(extract_path, Path):
        extract_path = Path(extract_path)
    if zip_file.exists():
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_path)