from typing import List, Optional

from dataclasses import dataclass

from .base_codecs import Codec
from .condition_codecs import ZoneAlarmCountCondition, ZoneAlarmRateCondition


@dataclass
class ZoneAlarm(Codec):
    """This is the configuration for an alarm."""

    name: str
    """A friendly name for the zone alarm"""

    count_conditions: List[ZoneAlarmCountCondition]
    """All count conditions for this alarm"""

    rate_conditions: List[ZoneAlarmRateCondition]
    """All rate conditions for this alarm"""

    use_active_time: bool
    """If True, the alarm will only be triggered when the current time is
    between the active_start_time and active_end_time.
    """

    active_start_time: str
    """The time of day where this alarm starts being active, in the format
    "hh:mm:ss"
    """

    active_end_time: str
    """The time of day where this alarm starts being active, in the format
    "hh:mm:ss"
    """

    id: Optional[int] = None
    """A unique identifier"""

    zone_id: Optional[int] = None
    """The ID of the zone this alarm is associated with"""

    stream_id: Optional[int] = None
    """The ID of the stream the associated zone is in"""

    def to_dict(self):
        d = dict(self.__dict__)
        d["count_conditions"] = [ZoneAlarmCountCondition.to_dict(cond)
                                 for cond in self.count_conditions]
        d["rate_conditions"] = [ZoneAlarmRateCondition.to_dict(cond)
                                for cond in self.rate_conditions]

        return d

    @staticmethod
    def from_dict(d):
        count_conditions = [ZoneAlarmCountCondition.from_dict(cond)
                            for cond in d["count_conditions"]]
        rate_conditions = [ZoneAlarmRateCondition.from_dict(cond)
                           for cond in d["rate_conditions"]]

        return ZoneAlarm(name=d["name"],
                         id=d["id"],
                         count_conditions=count_conditions,
                         rate_conditions=rate_conditions,
                         use_active_time=d["use_active_time"],
                         active_start_time=d["active_start_time"],
                         active_end_time=d["active_end_time"],
                         zone_id=d["zone_id"],
                         stream_id=d["stream_id"])


@dataclass
class Alert(Codec):
    """This is sent when an Alarm has been triggered."""

    alarm_id: int
    """The ID of the alarm that this alert came from"""

    zone_id: int
    """The ID of the zone this alert pertains to"""

    stream_id: int
    """The ID of the stream this alert pertains to"""

    start_time: float
    """When the event started happening, in Unix Time (seconds)"""

    end_time: Optional[float]
    """When the event stopped happening, in Unix Time (seconds), or None
    if the alert is ongoing.
    """

    verified_as: Optional[bool]
    """
    - If True, then this alert was labeled by a person as legitimate
    - If False, then this alert was labeled by a person as a false alarm
    - If None, then this alert has not been reviewed by a person
    """

    id: Optional[int] = None
    """A unique identifier"""

    def to_dict(self):
        d = dict(self.__dict__)
        return d

    @staticmethod
    def from_dict(d):
        return Alert(id=d["id"],
                     alarm_id=d["alarm_id"],
                     zone_id=d["zone_id"],
                     stream_id=d["stream_id"],
                     start_time=d["start_time"],
                     end_time=d["end_time"],
                     verified_as=d["verified_as"])
