from typing import List, Optional

from .base_codecs import Codec


class Identity(Codec):
    """A specific, recognizable object or person."""

    def __init__(self, *, unique_name, nickname, metadata=None, id_=None):
        self.unique_name = unique_name
        """The unique id of the identified detection.

        Not to be confused with the id of the object which is a field used by
        the database.
        """

        self.nickname = nickname
        """A display name for the identity which may not be unique, like a
        person's name.
        """

        self.metadata = {} if metadata is None else metadata
        """Any additional user-defined information about the identity."""

        self.id = id_
        """A unique identifier."""

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        return Identity(
            id_=d["id"],
            unique_name=d["unique_name"],
            nickname=d["nickname"],
            metadata=d["metadata"])


class Encoding(Codec):
    """An encoding attached to an identity."""

    def __init__(self, *, identity_id: int,
                 class_name: str,
                 from_image: Optional[int],
                 vector: List[int],
                 id_=None):
        self.identity_id = identity_id
        """The ID of the identity this encoding is associated with."""
        self.class_name = class_name
        """The class of object this encoding is for."""
        self.from_image = from_image
        """The storage ID of the image that this encoding was created from, or
        None if this encoding was not created from an image.
        """
        self.vector = vector
        """A low-dimensional representation of the object's appearance. This is
        what objects found in streams will be compared to in order to decide if
        the object is of the identity this encoding is associated with.
        """
        self.id = id_
        """The unique ID of the encoding."""

    def to_dict(self):
        d = dict(self.__dict__)
        return d

    @staticmethod
    def from_dict(d):
        return Encoding(id_=d["id"],
                        identity_id=d["identity_id"],
                        class_name=d["class_name"],
                        from_image=d["from_image"],
                        vector=d["vector"])
