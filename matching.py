from config import CORRESP, DOCTYPES, MEMBERS

"""
Catalogue Dict Structure:
{
 "Return-String": [
    [AND]OR[AND]
 ]
}


"""


class Catalogue:
    def __init__(self, catalogue) -> None:
        self.cat = catalogue

    def in_context(self, el, context: str = "") -> bool:
        el = el.lower()
        return el in context

    def match(self, context: str) -> str:
        context = context.lower()
        d = DOCTYPES.catalogue

        found = False
        for k in self.cat.keys():
            for l in self.cat[k]:  # OR Elements
                ands = all(self.in_context(i, context) for i in l)
                if ands:
                    return k


def match(context: str, catalogue_dict: dict) -> str:
    cat = Catalogue(catalogue=catalogue_dict)
    return cat.match(context)


def match_correspondent(context):
    return match(context=context, catalogue_dict=CORRESP.catalogue)


def match_doctype(context):
    return match(context=context, catalogue_dict=DOCTYPES.catalogue)


def match_member(context):
    return match(context=context, catalogue_dict=MEMBERS.catalogue)
