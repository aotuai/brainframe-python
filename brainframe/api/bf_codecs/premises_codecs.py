from typing import Optional

from dataclasses import dataclass

from .base_codecs import Codec


@dataclass
class Premises(Codec):
    """Information about a specific Premises"""

    name: str
    """The friendly name of the premises"""

    id: Optional[int] = None
    """The unique ID of the premises"""

    def to_dict(self):
        d = dict(self.__dict__)
        return d

    @staticmethod
    def from_dict(d):
        return Premises(name=d["name"], id=d["id"])
