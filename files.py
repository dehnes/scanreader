import datetime
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum, auto
from pathlib import Path

from config import CONFIG


def is_supported_type(extension: str = "") -> bool:
    # Error conditions
    if extension == "":
        return False  # TODO implementnException
    # load from config and ensure lower case
    supp = CONFIG.supported_filetypes
    supp = list(map(str.lower, supp))
    # clean extension
    e = extension.replace(".", "")  # remove the dots
    e = e.lower()
    return True if e in supp else False


@dataclass
class File:
    path: Path

    _created_at: datetime.date = field(default_factory=datetime.now)
    _modified_at: datetime.date = field(default_factory=datetime.now)

    @property
    def extension(self) -> str:
        return self.path.suffix

    @property
    def filename(self) -> str:
        return self.path.stem

    @property
    def relative_path(self) -> str:
        return self.path.parent

    @property
    def abs_path(self) -> str:
        return self.path.resolve()

    @property
    def is_supported_type(self) -> bool:
        return is_supported_type(extension=self.extension)

    # def __repr__(self) -> str: TODO implement
    #    return self.full_path()

    # def __str__(self) -> str: TODO implement
    #    return self.full_path()


def compose_file_name_from_content_txt(txt: str):
    sep = "_"
    bind = "-"
    f = ""

    date_patterns = [
        r"\b(0[1-9]|1[0-2])[.-/](0[1-9]|[12]\d|3[01])[.-/](19\d\d|20\d\d)\b",  # MM/DD/YYYY oder MM-DD-YYYY
        r"\b(0[1-9]|[12]\d|3[01])[.-/](0[1-9]|1[0-2])[.-/](19\d\d|20\d\d)\b",  # DD/MM/YYYY oder DD-MM-YYYY
        r"\b(19\d\d|20\d\d)[.-/](0[1-9]|1[0-2])[.-/](0[1-9]|[12]\d|3[01])\b",  # YYYY/MM/DD oder YYYY-MM-DD
        r"\b(0[1-9]|1[0-2])[.-/](0[1-9]|[12]\d|3[01])[.-/](\d\d)\b",  # MM-DD-YY oder MM/DD/YY
        r"\b(19\d\d|20\d\d)-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b",  # YYYY-MM-DD (ISO 8601)
    ]
