from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class DocType(Enum):
    NONE = "NN"
    RECHNUNG = "Rechnung"
    INFO = "Info"
    KUENDIGUNG = "Kündigung"
    ANGEBOT = "ANGEBOT"


@dataclass
class Document:
    title: str
    business_partner: str = ""
    doctype: DocType = DocType.NONE
    custom_doctype: str = ""
    filename: str = ""
    signed: bool = False
    issue_date: datetime.date = field(default_factory=datetime.now)
    _created_at: datetime.date = field(default_factory=datetime.now)
    _modified_at: datetime.date = field(default_factory=datetime.now)

    def get_cleaned_filename(self) -> str:
        return self.title
