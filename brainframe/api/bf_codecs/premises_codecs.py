from .base_codecs import Codec


class Premises(Codec):
    """Information about a specific Premises"""

    def __init__(self, *, name: str, id_: int = None):
        self.id: int = id_
        """The unique ID of the premises"""
        self.name: str = name
        """The friendly name of the premises"""

    def to_dict(self):
        d = dict(self.__dict__)
        return d

    @staticmethod
    def from_dict(d):
        return Premises(name=d["name"], id_=d["id"])
