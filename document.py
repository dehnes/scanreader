import logging
import os

from uniquify import uniquify

logger = logging.getLogger(__name__)

import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

from config import CONFIG
from datematching import get_archive_dates
from log_messaging import comp_compl, comp_start
from matching import match_correspondent, match_doctype, match_member


@dataclass
class Document:
    source_file: Path
    title: str = "untitled"
    business_partner: str = "partner"
    doctype: str = "document-type"
    member: str = ""
    ocr_content: str = ""
    signed: bool = False
    issue_date: datetime.date = field(default_factory=datetime.now)
    _content_dates: List = field(default_factory=lambda: [])
    _created_at: datetime.date = field(default_factory=datetime.now)
    _modified_at: datetime.date = field(default_factory=datetime.now)

    def run_matching(self):
        logger.info(comp_start(f"Running Matching in {self.source_file}"))
        self.run_ocr()
        # Identify Date
        self._content_dates = get_archive_dates(self.ocr_content)
        logger.debug(f"Found dates: {self._content_dates}")
        self.business_partner = match_correspondent(self.ocr_content)
        self.doctype = match_doctype(self.ocr_content)
        self.member = match_member(self.ocr_content)
        logger.info(comp_compl(f"Running Matching in {self.source_file}"))

    def run_ocr(self) -> str:
        # https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/
        logger.info(comp_start(f"Running OCR in {self.source_file}"))
        img_files = []
        pdf_pages = convert_from_path(self.source_file, 500)
        logger.debug(comp_start("  Converting pages to image files"))
        for page_enumeration, page in enumerate(pdf_pages, start=1):
            filename = f"tmp/page_{page_enumeration:03}.jpg"
            page.save(filename, "JPEG")
            img_files.append(filename)
        logger.debug(comp_compl("  Converting pages to image files"))
        logger.debug(comp_start("  Grabbing text from image files"))
        text = ""
        for img in img_files:
            text = f"{text} {str(pytesseract.image_to_string(Image.open(img)))}"
        logger.debug(comp_compl("  Grabbing text from image files"))
        logger.info(comp_compl(f"Running OCR in {self.source_file}"))
        self.ocr_content = text

    def compose_file_name(self) -> str:
        ms = CONFIG.separators.main
        sp = CONFIG.separators.spacer

        date_str = self._content_dates[0] if self._content_dates else "00000000"
        partner = self.business_partner.replace(" ", sp)
        title = self.title.replace(" ", sp)
        dtype = self.doctype.replace(" ", sp)

        f = f"{date_str}{ms}{partner}{ms}{dtype}{ms}{title}"

        if self.member != "":
            f = f"{f}{ms}{self.member}"
        f = f"{f}{self.source_file.suffix}"
        logger.info(f"Composed: {f}")
        return f

    def export(
        self,
        folder: str = CONFIG.paths.output_path,
        ocr_folder: str = CONFIG.paths.output_ocr_path,
    ):
        self.export_file(folder)
        self.export_ocr(ocr_folder)

    def export_file(self, folder: str = CONFIG.paths.output_path) -> None:
        # sourcery skip: class-extract-method
        initial_name = self.compose_file_name()
        logger.debug(f"Initial filename: {initial_name}")
        unique_name = uniquify(initial_name, folder)
        logger.debug(f"Unique filename: {unique_name}")
        shutil.copy(self.source_file, folder + unique_name)
        # TODO add try Except

    def export_ocr(self, ocr_folder=CONFIG.paths.output_ocr_path) -> None:
        initial_name = (
            f"{os.path.splitext(os.path.basename(self.compose_file_name()))[0]}.txt"
        )
        logger.debug(f"Initial filename: {initial_name}")
        unique_name = uniquify(initial_name, ocr_folder)
        logger.debug(f"Unique filename: {unique_name}")

        with open(ocr_folder + unique_name, "w") as f:
            f.write(self.ocr_content)
            f.close()
        # TODO add try except
