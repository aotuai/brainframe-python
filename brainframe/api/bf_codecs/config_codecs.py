from typing import Optional
from enum import Enum

from .base_codecs import Codec


class ConnType(Enum):
    IP_CAMERA = "ip_camera"
    """A network camera that uses RTSP or HTTP"""
    WEBCAM = "webcam"
    """A USB webcam"""
    FILE = "file"
    """An uploaded video file"""

    @classmethod
    def values(cls):
        return [v.value for v in cls]


# Stream Data structures
class StreamConfiguration(Codec):
    """Describes a video stream that BrainFrame may connect to and analyze.
    """

    def __init__(self, *, name: str,
                 connection_type: ConnType,
                 connection_options: dict,
                 runtime_options: dict,
                 premises_id: Optional[int],
                 metadata: dict = None,
                 id_=None):
        assert connection_type in ConnType, \
            "You must feed StreamConfiguration.ConnType into connection_type" \
            " You used a " + str(type(connection_type)) + " instead!"

        self.name = name
        """The human-readable name of the video stream"""
        self.premises_id = premises_id
        """The ID of the premises that this stream is a part of, or None if
        this stream is not part of a premises
        """
        self.id = id_
        """The unique ID of this stream"""
        self.connection_type = connection_type
        """The type of stream this configuration is describing"""
        self.connection_options = connection_options
        """Contains configuration describing how this stream can be connected
        to. The contents of this dict will depend on the connection type.
        
        ConnType.IP_CAMERA:
            ``url``: The URL of the IP camera to connect to
            
            ``pipeline`` (optional): A custom GStreamer pipeline to connect to
            the IP camera with
        
        ConnType.FILE:
            ``storage_id``: The storage ID of the video file to stream
            
            ``transcode`` (optional): If true, the video file will be
            transcoded before being streamed. By default, this value is true.
            
            ``pipeline`` (optional): A custom GStreamer pipeline to connect to
            the hosted stream of this video file with
                
        ConnType.WEBCAM:
            ``device_id``: The Video4Linux device ID of the webcam
        """
        self.runtime_options = runtime_options
        """"""
        self.metadata = metadata or {}

    def to_dict(self):
        d = dict(self.__dict__)
        d["connection_type"] = self.connection_type.value
        return d

    @staticmethod
    def from_dict(d):
        connection_t = ConnType(d["connection_type"])
        return StreamConfiguration(name=d["name"],
                                   id_=d["id"],
                                   connection_type=connection_t,
                                   connection_options=d["connection_options"],
                                   runtime_options=d["runtime_options"],
                                   metadata=d["metadata"],
                                   premises_id=d["premises_id"])
