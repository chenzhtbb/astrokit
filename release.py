import os
from pathlib import Path
import subprocess

if __name__ == '__main__':
    cwd = Path.cwd()
    subprocess.run(["twine", "check", "dist/*"], cwd=cwd, env=os.environ.copy())
    subprocess.run(["twine", "upload", "dist/*"], cwd=cwd, env=os.environ.copy())

