import logging
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

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)


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
        self.run_ocr()
        self.export_ocr_content()
        # Identify Date
        self._content_dates = get_archive_dates(self.ocr_content)
        logger.debug(f"Found dates: {self._content_dates}")
        self.business_partner = match_correspondent(self.ocr_content)
        self.doctype = match_doctype(self.ocr_content)
        self.member = match_member(self.ocr_content)

    def run_ocr(self) -> str:
        # https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/
        logger.info(comp_start(f"Running OCR in {self.source_file}"))
        img_files = []
        pdf_pages = convert_from_path(self.source_file, 500)
        for page_enumeration, page in enumerate(pdf_pages, start=1):
            filename = f"tmp/page_{page_enumeration:03}.jpg"
            page.save(filename, "JPEG")
            img_files.append(filename)
        text = ""
        for img in img_files:
            text = f"{text} {str(pytesseract.image_to_string(Image.open(img)))}"
        logger.info(comp_compl(f"Running OCR in {self.source_file}"))
        self.ocr_content = text

    def export_ocr_content(self) -> None:
        with open(CONFIG.paths.temp_path + CONFIG.content_file_name, "w") as f:
            # TODO improve Method to wirte to separate file name
            f.write(self.ocr_content)
            f.close()

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
