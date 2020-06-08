from typing import List, Optional

from .base_codecs import Codec
from .condition_codecs import ZoneAlarmCountCondition, ZoneAlarmRateCondition


class ZoneAlarm(Codec):
    """This is the configuration for an alarm."""

    def __init__(self, *, name, count_conditions, rate_conditions,
                 use_active_time, active_start_time, active_end_time,
                 id_=None, zone_id=None, stream_id=None):
        self.name = name
        self.id = id_
        self.zone_id = zone_id
        self.stream_id = stream_id
        self.count_conditions: List[ZoneAlarmCountCondition] = count_conditions
        self.rate_conditions: List[ZoneAlarmRateCondition] = rate_conditions
        self.use_active_time = use_active_time
        self.active_start_time = active_start_time
        self.active_end_time = active_end_time

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

    def __init__(self, *, alarm_id, zone_id, stream_id, start_time, end_time,
                 verified_as, id_=None):
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

