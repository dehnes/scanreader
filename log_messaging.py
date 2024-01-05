from config import CONFIG


def comp_start(msg: str = "") -> str:
    return msg + CONFIG.log_str.started if msg else ""


def comp_compl(msg: str = "") -> str:
    return msg + CONFIG.log_str.comp if msg else ""
