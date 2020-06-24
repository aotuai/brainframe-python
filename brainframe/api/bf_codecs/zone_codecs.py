from collections import Counter
from typing import List, Optional

from dataclasses import dataclass, field

from .base_codecs import Codec
from .alarm_codecs import Alert, ZoneAlarm
from .detection_codecs import Detection


@dataclass
class Zone(Codec):
    """The definition for a zone. It is a non-convex polygon or a line."""

    name: str
    """A friendly name for the zone"""

    stream_id: int
    """The ID of the stream this zone is in"""

    coords: List[List[int]]
    """Coordinates that define the region the zone occupies. It is a list
    of lists which are two elements in size. The coordinates are in pixels
    where the top left of the frame is [0, 0].
    
    Example: [[0, 0], [10, 10], [100, 500], [0, 500]]
    """

    alarms: List[ZoneAlarm] = field(default_factory=list)
    """All alarms that are attached to the zone"""

    id: Optional[int] = None
    """A unique identifier"""

    def get_alarm(self, alarm_id) -> Optional[ZoneAlarm]:
        """
        :param alarm_id: The ID of the alarm to search in the alarm list for
        :return: The alarm with the given ID, or None if no alarm with that ID
            exists in this zone
        """
        for alarm in self.alarms:
            if alarm.id == alarm_id:
                return alarm
        return None

    def to_dict(self):
        d = dict(self.__dict__)
        d["alarms"] = [alarm.to_dict() for alarm in self.alarms]
        return d

    @staticmethod
    def from_dict(d):
        alarms = [ZoneAlarm.from_dict(alarm_d) for alarm_d in d["alarms"]]
        return Zone(name=d["name"],
                    id=d["id"],
                    alarms=alarms,
                    stream_id=d["stream_id"],
                    coords=d["coords"])


@dataclass
class ZoneStatus(Codec):
    """The current status of everything going on inside a zone.
    """

    zone: Zone
    """The zone that this status pertains to"""

    tstamp: float
    """The time at which this ZoneStatus was created as a Unix timestamp in
    seconds
    """

    total_entered: dict
    """A dict of key-value pairs indicating how many objects have exited the
    zone. The key is the class name, and the value is the count.
    """

    total_exited: dict
    """A set of key-value pairs indicating how many objects have exited the
    zone. The key is the object type, and the value is the count.
    """

    within: List[Detection]
    """A list of all detections within the zone"""

    entering: List[Detection]
    """A list of all detections that entered the zone this frame"""

    exiting: List[Detection]
    """A list of all detections that have exited the zone this frame"""

    alerts: List[Alert]
    """A list of all active alerts for the zone at this frame"""

    @property
    def detection_within_counts(self) -> dict:
        """The current count of each class type detected in the video.

        :returns: A dict whose keys are class names and whose values are the
            count for that class name
        """
        counter = Counter([det.class_name for det in self.within])
        return counter

    def to_dict(self):
        d = dict(self.__dict__)
        d["zone"] = self.zone.to_dict()
        d["within"] = [det.to_dict() for det in self.within]
        d["entering"] = [det.to_dict() for det in self.entering]
        d["exiting"] = [det.to_dict() for det in self.exiting]
        d["alerts"] = [alert.to_dict() for alert in self.alerts]
        return d

    @staticmethod
    def from_dict(d):
        zone = Zone.from_dict(d["zone"])
        within = [Detection.from_dict(det) for det in d["within"]]
        entering = [Detection.from_dict(det) for det in d["entering"]]
        exiting = [Detection.from_dict(det) for det in d["exiting"]]
        alerts = [Alert.from_dict(alert) for alert in d["alerts"]]
        return ZoneStatus(zone=zone,
                          tstamp=d["tstamp"],
                          total_entered=d["total_entered"],
                          total_exited=d["total_exited"],
                          within=within,
                          entering=entering,
                          exiting=exiting,
                          alerts=alerts)
