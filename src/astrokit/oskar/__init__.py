import zipfile

import wget
from astrokit.utils import get_pwd

from .Oskar import *

__all__ = ['Oskar', 'get_oskar_data']

def get_oskar_data(name: str):
    oskar_data = get_pwd(__file__) / 'data/oskar'
    zipdir = oskar_data / 'OSKAR-2.7-Example-Data'
    zipdata = oskar_data / 'OSKAR-2.7-Example-Data.zip'
    if not zipdata.exists():
        oskar_data.mkdir(parents=True, exist_ok=True)
        wget.download('https://github.com/OxfordSKA/OSKAR/files/1984210/OSKAR-2.7-Example-Data.zip', str(oskar_data))
    if zipdata.exists():
        with zipfile.ZipFile(zipdata, 'r') as zip_ref:
            zip_ref.extractall(oskar_data)
    file = oskar_data / zipdir / name
    if file.exists():
        return file
    raise FileNotFoundError(f'{file} not found!')
