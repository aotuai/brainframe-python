from typing import Optional
from enum import Enum

from .base_codecs import Codec


class RoleType(Enum):
    """Controls the level of access a user has to API endpoints."""

    EDITOR = "editor"
    """A user that can access most endpoints but cannot do administrative tasks
    like adding users and managing the license.
    """
    ADMIN = "admin"
    """A user that can access all endpoints."""

    @classmethod
    def values(cls):
        return [v.value for v in cls]


class User(Codec):
    """Contains information on a user."""

    def __init__(self, *, username: str,
                 password: Optional[str],
                 role: RoleType,
                 id_=None):
        self.username = username
        """The username used for login"""
        self.password = password
        """This field will be None when retrieving users from the server. It
        should only be set by the client when creating a new user or updating a
        user's password.
        """
        self.role = role
        """The user's role"""
        self.id = id_
        """The user's unique ID"""

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        d["role"] = self.role.value
        return d

    @staticmethod
    def from_dict(d: dict):
        return User(
            username=d["username"],
            password=d["password"],
            role=User.RoleType(d["role"]),
            id_=d["id"],
        )
