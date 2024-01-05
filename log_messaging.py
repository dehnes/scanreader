from config import CONFIG


def comp_start(msg: str = "") -> str:
    if msg == "":
        return ""
    else:
        return msg + CONFIG.log_str.started


def comp_compl(msg: str = "") -> str:
    if msg == "":
        return ""
    else:
        return msg + CONFIG.log_str.comp
