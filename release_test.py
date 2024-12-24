import os
import shutil
from pathlib import Path
import subprocess

if __name__ == '__main__':
    cwd = Path.cwd()
    dist = cwd / 'dist'
    if dist.exists():
        shutil.rmtree(dist)

    subprocess.run(["python", "-m", "build"], cwd=cwd, env=os.environ.copy())
    subprocess.run(["pip", "uninstall", "astronomy-kit"], cwd=cwd, env=os.environ.copy())
    whl = dist.glob('*.whl').__next__()
    subprocess.run(["pip", "install", whl], cwd=cwd, env=os.environ.copy())
    subprocess.run(["python", "tests/test.py"], cwd=cwd, env=os.environ.copy())
    shutil.rmtree(cwd.joinpath('example/data'))
