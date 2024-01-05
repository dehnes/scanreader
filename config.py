import json

CONFIG_FILE = "config.json"
TYPE_MATCHES_FILE = "match_doctypes.json"
CORR_MATCHES_FILE = "match_correspond.json"
MEMBER_MATCHES_FILE = "match_member.json"


class Dict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Loader(object):
    @staticmethod
    def __load__(data):
        if type(data) is dict:
            return Loader.load_dict(data)
        elif type(data) is list:
            return Loader.load_list(data)
        else:
            return data

    @staticmethod
    def load_dict(data: dict):
        result = Dict()
        for key, value in data.items():
            result[key] = Loader.__load__(value)
        return result

    @staticmethod
    def load_list(data: list):
        return [Loader.__load__(item) for item in data]

    @staticmethod
    def load_json(path: str):
        with open(path, "r") as f:
            result = Loader.__load__(json.loads(f.read()))
        return result


CONFIG = Loader.load_json(CONFIG_FILE)
DOCTYPES = Loader.load_json(TYPE_MATCHES_FILE)
CORRESP = Loader.load_json(CORR_MATCHES_FILE)
MEMBERS = Loader.load_json(MEMBER_MATCHES_FILE)
