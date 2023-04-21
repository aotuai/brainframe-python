from typing import Optional
from enum import Enum

from dataclasses import dataclass, field

from .base_codecs import Codec


class AiIntervalType(Enum):
    TIME = "time"
    """time mode, Frames were analyzed according to time intervals
    """
    FRAME = "frame"
    """frame mode, Frames were taken for analysis according to the frame number interval 
    """
    @classmethod
    def values(cls):
        return [v.value for v in cls]


@dataclass
class Snip(Codec):
    """Describes a snip of a video that BrainFrame may process
    """

    class StorageType(Enum):
        SESSION_ID = "session_id"
        """a transaction number"""
        STORAGE_URI = "storage_uri"
        """a storage_uri, For example: OSS URL"""

        @classmethod
        def values(cls):
            return [v.value for v in cls]

    storage_type: StorageType
    """storage_type can be session_id or storage_uri. If session_id, then phase
    session_id is the appropriate storage; If storage_uri, storage is storage_uri
    For example: OSS URL.
    """
    storage: dict
    """The contents of this dict will depend on the storage_type.

    StorageType.SESSION_ID:
        ``session_id``: a transaction number.

    StorageType.STORAGE_URI :
        ``storage_uri``: a URL of the address from which the content was downloaded.
    """

    timestamp: float
    """a tstamp timestamp from the /api/streams/statuses interface. AI Server according to the time
    Interstamping locates the position of the picture in the offline video file and takes a screenshot.
    """

    def to_dict(self):
        d = dict(self.__dict__)
        d["storage_type"] = self.storage_type.value
        return d

    @staticmethod
    def from_dict(d):
        storage_t = Snip.StorageType(d["storage_type"])
        return Snip(storage_type=storage_t,
                    storage=d["storage"],
                    timestamp=d["timestamp"])


