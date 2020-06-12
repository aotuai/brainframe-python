from typing import List, Optional

from .base_codecs import Codec
from .condition_codecs import ZoneAlarmCountCondition, ZoneAlarmRateCondition


class ZoneAlarm(Codec):
    """This is the configuration for an alarm."""

    def __init__(self, *,
                 name: str,
                 count_conditions: List[ZoneAlarmCountCondition],
                 rate_conditions: List[ZoneAlarmRateCondition],
                 use_active_time: bool,
                 active_start_time: str,
                 active_end_time: str,
                 id_: int = None,
                 zone_id: int = None,
                 stream_id: int = None):
        self.name: str = name
        """A friendly name for the zone alarm"""
        self.id: int = id_
        """A unique identifier"""
        self.zone_id: int = zone_id
        """The ID of the zone this alarm is associated with"""
        self.stream_id: int = stream_id
        """The ID of the stream the associated zone is in"""
        self.count_conditions: List[ZoneAlarmCountCondition] = count_conditions
        """All count conditions for this alarm"""
        self.rate_conditions: List[ZoneAlarmRateCondition] = rate_conditions
        """All rate conditions for this alarm"""
        self.use_active_time: bool = use_active_time
        """If True, the alarm will only be triggered when the current time is
        between the active_start_time and active_end_time.
        """
        self.active_start_time: str = active_start_time
        """The time of day where this alarm starts being active, in the format
        "hh:mm:ss"
        """
        self.active_end_time: str = active_end_time
        """The time of day where this alarm starts being active, in the format
        "hh:mm:ss"
        """

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
                         id_=d["id"],
                         count_conditions=count_conditions,
                         rate_conditions=rate_conditions,
                         use_active_time=d["use_active_time"],
                         active_start_time=d["active_start_time"],
                         active_end_time=d["active_end_time"],
                         zone_id=d["zone_id"],
                         stream_id=d["stream_id"])


class Alert(Codec):
    """This is sent when an Alarm has been triggered."""

    def __init__(self, *,
                 alarm_id: int,
                 zone_id: int,
                 stream_id: int,
                 start_time: float,
                 end_time: float,
                 verified_as: Optional[bool],
                 id_: int = None):
        self.id: int = id_
        """A unique identifier"""
        self.alarm_id: int = alarm_id
        """The ID of the alarm that this alert came from"""
        self.zone_id: int = zone_id
        """The ID of the zone this alert pertains to"""
        self.stream_id: int = stream_id
        """The ID of the stream this alert pertains to"""
        self.start_time: float = start_time
        """When the event started happening, in Unix Time (seconds)"""
        self.end_time: Optional[float] = end_time
        """When the event stopped happening, in Unix Time (seconds), or None
        if the alert is ongoing.
        """
        self.verified_as: Optional[bool] = verified_as
        """
        - If True, then this alert was labeled by a person as legitimate
        - If False, then this alert was labeled by a person as a false alarm
        - If None, then this alert has not been reviewed by a person
        """

    def to_dict(self):
        d = dict(self.__dict__)
        return d

    @staticmethod
    def from_dict(d):
        return Alert(id_=d["id"],
                     alarm_id=d["alarm_id"],
                     zone_id=d["zone_id"],
                     stream_id=d["stream_id"],
                     start_time=d["start_time"],
                     end_time=d["end_time"],
                     verified_as=d["verified_as"])
