import datetime as dt
import logging
import re

MONTHS_DICT = {
    "1": 1,
    "01": 1,
    "JAN": 1,
    "JANUAR": 1,
    "2": 2,
    "02": 2,
    "FEB": 2,
    "FEBRUAR": 2,
    "3": 3,
    "03": 3,
    "MRZ": 3,
    "MÄRZ": 3,
    "4": 4,
    "04": 4,
    "APR": 4,
    "APRIL": 4,
    "5": 5,
    "05": 5,
    "MAI": 5,
    "6": 6,
    "06": 6,
    "JUN": 6,
    "JUNI": 6,
    "7": 7,
    "07": 7,
    "JUL": 7,
    "JULI": 7,
    "8": 8,
    "08": 8,
    "AUG": 8,
    "AUGUST": 8,
    "9": 9,
    "09": 9,
    "SEP": 9,
    "SEPTEMBER": 9,
    "10": 10,
    "OKT": 10,
    "OKTOBER": 10,
    "11": 11,
    "NOV": 11,
    "NOVEMBER": 11,
    "12": 12,
    "DEZ": 12,
    "DEZEMBER": 12,
}


def get_month_by_str(month: str) -> int:
    m = month.upper()
    return MONTHS_DICT[m] if m in MONTHS_DICT else -1


def get_date_tuples_from_text(text: str = "", test_mode: bool = False):
    l = logging.getLogger(f"{__name__}.get_date_tuples_from_text")

    if test_mode:
        text = search_text
    results = []

    d = r"3[01]|[0-2][0-9]|[0-9]"
    m_short = r"[Jj]an|[Ff]eb|[Mm]rz|[Aa]pr|[Mm]ai|[Jj]un|[Jj]ul|[Aa]ug|[Ss]ep|[Oo]kt|[Nn]ov|[Dd]ez"
    m_long = r"[Jj]anuar|[Ff]ebruar|[Mm]ärz|[Mm]aerz|[Aa]pril|[Jj]uni|[Jj]uli|[Aa]ugust|[Ss]eptember|[Oo]ktober|[Nn]ovember|[Dd]ezember"
    m_digits = r"[0][0-9]|1[0-2]|[1-9]"
    y = r"[12][0-9][0-9][0-9]|[0-9][0-9]"

    patterns = [
        r"\b(\s)(" + m_digits + r")[/](" + y + r")",
        r"\b(" + d + r")[.](" + m_digits + r")[.](" + y + r")?",
        r"\b(" + d + r")[.]?\s?(" + m_long + r"|" + m_short + r")[.]?\s?(" + y + r")?",
    ]

    for p in patterns:
        results.extend(re.findall(p, text))

    if results:
        for r in results:
            l.debug(f"Found: {r}")
    else:
        l.debug("Nothing found")
    return results


def convert_to_archive_format(input) -> str:
    # create the Year
    y = f"{dt.date.today().year}" if input[2] == "" else input[2]
    y = int(y)
    if y >= 1000:
        y = f"{y}"
    elif 31 <= y <= 999:
        y = f"{1900+y}"
    elif 1 <= y <= 30:
        y = f"{2000+y}"

    # create the Month
    m = get_month_by_str(input[1])
    if m < 10:
        m = f"0{m}"
    elif m < 13:
        m = f"{m}"
    else:
        m = "01"  # TODO ggf 00 für undefined

    # create the Day
    d = input[0]
    if len(d) == 2:
        d = d
    elif d == " " or len(d) != 1:
        d = "01"  # TODO ggf 00 für undefined
    else:
        d = f"0{d}"
    return y + m + d


def get_archive_dates(context: str):
    tpls = get_date_tuples_from_text(context)
    ar_dates = [convert_to_archive_format(t) for t in tpls]
    # remove duplicates:
    results = []
    for d in ar_dates:
        if d not in results:
            results.append(d)

    return results


# Example text
search_text = """
Test String 11/2023
Test String 11/23
Test String 04.07.2018
Test String 14.02.2023
Test String 1.2.2023
Test String 1.02.2023
Test String 01.02.2023
Test String 01.02.23
Test String 1.02.
Test String 01.2.
Test String 1.2.
Test String 1.02.

Test String 02. Februar 2023
Test String 02. Februar 2023 
Test String 03. Feb 2023
Test String 04.Februar 2023
Test String 05.Feb 2023
Test String 06.februar2024
Test String 07.Feb2023
Test String 08. Feb. 2023
Test String 09.Feb. 2023
Test String 10.Feb.2023
Test String 11. Aug 2043
Test String 12. August 2019
"""


def test_regex():
    with open("test.txt") as f:
        lines = f.read()

        get_date_tuples_from_text(lines, test_mode=True)
