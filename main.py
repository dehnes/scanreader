import glob
import logging
import logging.config
import os
import shutil
from pathlib import Path

from PIL import Image

from config import CONFIG
from document import Document
from log_messaging import comp_compl, comp_start

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)


def read_files() -> list[Path]:
    input_path = CONFIG.paths.input_path
    logger.info(comp_start(f"Reading all Files in '{input_path}'"))
    files = glob.glob(f"{input_path}*")
    paths = [Path(f) for f in files if Path(f).is_file()]
    logger.info(comp_compl(f"Reading all Files in '{input_path}'"))
    return paths


def clear_folder(folder: str) -> None:
    logger.info(comp_start(f"Clearing folder '{folder}'"))
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logger.error((f"Failed to delete {file_path}. Reason: {e}"))
    logger.info(comp_compl(f"Clearing folder '{folder}'"))


def copy_and_save_file(source_file: Path, destination_file_name: str):
    pass  # TODO implement


def analyze_files(files):
    logger.info(comp_start("Analyzing all Files"))
    for file in files:
        clear_folder(CONFIG.paths.temp_path)
        d = Document(source_file=file)
        d.run_matching()
        logger.info(d.compose_file_name())
    logger.info(comp_compl("Analyzing all Files"))


def main():
    logger.info(comp_start("Initializing"))
    # Initialize PIllow
    Image.MAX_IMAGE_PIXELS = 1000000000
    logger.info(comp_compl("Initializing"))
    # Read all the files
    files = read_files()
    analyze_files(files)


if __name__ == "__main__":
    main()
