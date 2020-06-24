from typing import List, Optional

from dataclasses import dataclass, field

from .base_codecs import Codec


@dataclass
class Identity(Codec):
    """A specific, recognizable object or person."""

    unique_name: str
    """The unique id of the identified detection.

    Not to be confused with the id of the object which is a field used by
    the database.
    """

    nickname: str
    """A display name for the identity which may not be unique, like a
    person's name.
    """

    metadata: dict = field(default_factory=dict)
    """Any additional user-defined information about the identity."""

    id: Optional[int] = None
    """A unique identifier."""

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        return Identity(
            id=d["id"],
            unique_name=d["unique_name"],
            nickname=d["nickname"],
            metadata=d["metadata"])


@dataclass
class Encoding(Codec):
    """An encoding attached to an identity."""

    identity_id: int
    """The ID of the identity this encoding is associated with."""

    class_name: str
    """The class of object this encoding is for."""

    from_image: Optional[int]
    """The storage ID of the image that this encoding was created from, or
    None if this encoding was not created from an image.
    """

    vector: List[int]
    """A low-dimensional representation of the object's appearance. This is
    what objects found in streams will be compared to in order to decide if
    the object is of the identity this encoding is associated with.
    """

    id: Optional[int] = None
    """The unique ID of the encoding."""

    def to_dict(self):
        d = dict(self.__dict__)
        return d

    @staticmethod
    def from_dict(d):
        return Encoding(id=d["id"],
                        identity_id=d["identity_id"],
                        class_name=d["class_name"],
                        from_image=d["from_image"],
                        vector=d["vector"])
