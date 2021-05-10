from dataclasses import dataclass

from .base_codecs import Codec


@dataclass
class CloudTokens(Codec):
    """OAuth2 tokens for a BrainFrame Cloud user"""

    access_token: str
    """Provides access to the API"""

    refresh_token: str
    """Used to refresh the access token when it expires"""

    def to_dict(self) -> dict:
        return dict(self.__dict__)

    @staticmethod
    def from_dict(d: dict) -> "CloudTokens":
        return CloudTokens(
            access_token=d["access_token"],
            refresh_token=d["refresh_token"],
        )


@dataclass
class CloudUserInfo(Codec):
    """Information on a BrainFrame Cloud user"""

    sub: str
    """A unique identifier for the user"""

    email: str
    """The user's email address"""

    def to_dict(self):
        return dict(self.__dict__)

    @staticmethod
    def from_dict(d: dict) -> "CloudUserInfo":
        return CloudUserInfo(
            sub=d["sub"],
            email=d["email"],
        )
