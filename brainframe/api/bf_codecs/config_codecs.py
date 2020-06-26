from typing import Optional
from enum import Enum

from dataclasses import dataclass, field

from .base_codecs import Codec


@dataclass
class StreamConfiguration(Codec):
    """Describes a video stream that BrainFrame may connect to and analyze.
    """

    class ConnType(Enum):
        IP_CAMERA = "ip_camera"
        """A network camera that uses RTSP or HTTP"""
        WEBCAM = "webcam"
        """A webcam (usually USB)"""
        FILE = "file"
        """An uploaded video file"""

        @classmethod
        def values(cls):
            return [v.value for v in cls]

    name: str
    """The human-readable name of the video stream"""

    premises_id: Optional[int]
    """The ID of the premises that this stream is a part of, or None if
    this stream is not part of a premises
    """

    connection_type: ConnType
    """The type of stream this configuration is describing"""

    connection_options: dict
    """Contains configuration describing how this stream can be connected
    to. The contents of this dict will depend on the connection type.

    ConnType.IP_CAMERA:
        ``url``: The URL of the IP camera to connect to

        ``pipeline`` (optional): A custom GStreamer pipeline to connect to
        the IP camera with

    ConnType.FILE:
        ``storage_id``: The storage ID of the video file to stream

        ``transcode`` (optional): If True, the video file will be
        transcoded before being streamed. By default, this value is True.

        ``pipeline`` (optional): A custom GStreamer pipeline to connect to
        the hosted stream of this video file with

    ConnType.WEBCAM:
        ``device_id``: The Video4Linux device ID of the webcam
    """

    runtime_options: dict
    """Key-value pairs of configuration information that changes the
    runtime behavior of the video stream from its defaults
    """

    metadata: dict = field(default_factory=dict)
    """Key-value pairs containing some custom user-defined set of data to
    further describe the stream
    """

    id: Optional[int] = None
    """The unique ID of this stream"""

    def to_dict(self):
        d = dict(self.__dict__)
        d["connection_type"] = self.connection_type.value
        return d

    @staticmethod
    def from_dict(d):
        connection_t = StreamConfiguration.ConnType(d["connection_type"])
        return StreamConfiguration(name=d["name"],
                                   id=d["id"],
                                   connection_type=connection_t,
                                   connection_options=d["connection_options"],
                                   runtime_options=d["runtime_options"],
                                   metadata=d["metadata"],
                                   premises_id=d["premises_id"])
