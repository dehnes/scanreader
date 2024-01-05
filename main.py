import glob
import logging
import logging.config
import os
import shutil
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

from config import CONFIG
from datematching import get_archive_dates, get_date_tuples_from_text
from log_messaging import comp_compl, comp_start
from matching import match_correspondent, match_doctype, match_member


def read_files():
    input_path = CONFIG.paths.input_path
    LOGGER.info(comp_start(f"Reading all Files in '{input_path}'"))
    files = glob.glob(f"{input_path}*")
    paths = []
    for f in files:
        p = Path(f)
        if p.is_file():
            paths.append(f)
    LOGGER.info(comp_compl(f"Reading all Files in '{input_path}'"))
    return paths


def ocr_file(p: Path):
    # https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/
    LOGGER.info(comp_start(f"Running OCR in {p}"))
    img_files = []
    pdf_pages = convert_from_path(p, 500)
    for page_enumeration, page in enumerate(pdf_pages, start=1):
        filename = f"tmp/page_{page_enumeration:03}.jpg"
        page.save(filename, "JPEG")
        img_files.append(filename)
    text = ""
    for img in img_files:
        text = f"{text} {str(pytesseract.image_to_string(Image.open(img)))}"
    LOGGER.info(comp_compl(f"Running OCR in {p}"))
    return text


def clear_folder(folder: str):
    LOGGER.info(comp_start(f"Clearing folder '{folder}'"))
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            LOGGER.error((f"Failed to delete {file_path}. Reason: {e}"))
    LOGGER.info(comp_compl(f"Clearing folder '{folder}'"))


def write_file_content(content: str):
    with open(CONFIG.paths.temp_path + CONFIG.content_file_name, "w") as file:
        file.write(content)
        file.close()


def compose_file_name(
    date_str: str = "00000000",  # TODO Maybe better to use current date in format yyyymmdd
    correspondent="CORR",
    doc_type: str = "DOCUMENT-TYPE",
    title: str = "",
    member: str = "",
    extension: str = "dat",
):
    ms = CONFIG.separators.main
    sp = CONFIG.separators.spacer

    if correspondent is None:
        correspondent = "CORRESPONDENT"
    correspondent = correspondent.replace(" ", sp)
    title = title.replace(" ", sp)
    doc_type = doc_type.replace(" ", sp)

    f = f"{date_str}{ms}{correspondent}{ms}{doc_type}"
    if title != "":
        f = f"{f}{ms}{title}"
    if member != "":
        f = f"{f}{ms}{member}"
    f = f"{f}.{extension}"
    return f


def analyze_file(file):
    clear_folder(CONFIG.paths.temp_path)

    content = ocr_file(file)
    write_file_content(content)

    # Identify Date
    dates = get_archive_dates(content)
    LOGGER.debug(f"Found dates: {dates}")
    if dates:
        d_date = dates[0]  # TODO add more intelligence
    corr = match_correspondent(content)
    dtype = match_doctype(content)
    title = ""  # TODO Add Document Title
    member = match_member(content)
    ext = "pdf"  # TODO Add Extension
    # Generate Filename
    file_name = compose_file_name(
        date_str=d_date,
        correspondent=corr,
        title=title,
        doc_type=dtype,
        member=member,
        extension=ext,
    )
    LOGGER.info(file_name)


def analyze_files(files):
    LOGGER.info(comp_start("Analyzing all Files"))
    for file in files:
        analyze_file(file)
    LOGGER.info(comp_compl("Analyzing all Files"))


def main():
    LOGGER.info(comp_start("Initializing"))
    # Initialize PIllow
    Image.MAX_IMAGE_PIXELS = 1000000000
    LOGGER.info(comp_compl("Initializing"))
    # Read all the files
    files = read_files()
    analyze_files(files)


def test_regex():
    with open("test.txt") as f:
        lines = f.read()

        get_date_tuples_from_text(lines, test_mode=True)


if __name__ == "__main__":
    logging.config.fileConfig("logging.conf")
    global LOGGER
    LOGGER = logging.getLogger(__name__)
    main()
    # test_regex()

    # print(CORRESP.test)

    # print(match_doctype(context="Ich schicke Dir das eis so  schnell wie möglich"))
