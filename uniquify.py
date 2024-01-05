import os
from pathlib import Path


def uniquify(filename, target_path):
    p = Path(target_path + filename)
    if os.path.isfile(p):
        counter = 1

        while Path(f"{target_path}{p.stem}_{counter}{p.suffix}").is_file():
            counter += 1
        p = Path(f"{target_path}{p.stem}_{counter}{p.suffix}")
    return f"{p.stem}{p.suffix}"
