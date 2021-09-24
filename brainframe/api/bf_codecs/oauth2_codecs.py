from dataclasses import dataclass
from typing import List

from .base_codecs import Codec


@dataclass
class OAuth2Info(Codec):
    """Information necessary to start an OAuth2 flow on behalf of the BrainFrame server
    """
    domain: str
    """The domain of the OAuth2 server"""

    client_id: str
    """The OAuth2 client ID"""

    scopes: List[str]
    """The OAuth2 scopes that tokens must have access to"""

    def to_dict(self) -> dict:
        return dict(self.__dict__)

    @staticmethod
    def from_dict(d: dict) -> "OAuth2Info":
        return OAuth2Info(
            domain=d["domain"],
            client_id=d["client_id"],
            scopes=d["scopes"],
        )
