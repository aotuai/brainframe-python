from enum import Enum
from typing import Optional

from .base_codecs import Codec
from .detection_codecs import Attribute


condition_test_map = {'>': "Greater than",
                      '>=': "Greater than or equal to",
                      '<': "Less than",
                      '<=': "Less than or equal to",
                      "=": "Exactly",
                      "!=": "Not Equal To"}


class CountConditionTestType(Enum):
    """Defines the way a count condition compares the actual value to the
    alarm's test value.
    """

    GREATER_THAN = ">"
    LESS_THAN = "<"
    EQUAL_TO = "="
    NOT_EQUAL_TO = "!="

    @classmethod
    def values(cls):
        return [v.value for v in cls]


class IntersectionPointType(Enum):
    """The point on a detection that must be inside a zone for the detection to
    count as being inside the zone. The most commonly used intersection point
    is BOTTOM, which counts a detection as being inside a zone if the bottom
    center point of the detection in the zone.
    """

    BOTTOM = "bottom"
    TOP = "top"
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"

    @classmethod
    def values(cls):
        return [v.value for v in cls]


class ZoneAlarmCountCondition(Codec):
    """A condition that must be met for an alarm to go off. Compares the number
    of objects in a zone to some number.
    """

    def __init__(self, *,
                 test: CountConditionTestType,
                 check_value: int,
                 with_class_name: str,
                 with_attribute: Optional[Attribute],
                 window_duration: float,
                 window_threshold: float,
                 intersection_point: IntersectionPointType,
                 id_: int = None):
        self.test: CountConditionTestType = test
        """The way that the check value will be compared to the actual count
        """
        self.check_value: int = check_value
        """The value to test the actual count against"""
        self.with_class_name: str = with_class_name
        """The class name of the objects to count"""
        self.with_attribute: Optional[Attribute] = with_attribute
        """If provided, only objects that have this attribute value will be
        counted.
        """
        self.window_duration: float = window_duration
        """The sliding window duration for this condition"""
        self.window_threshold: float = window_threshold
        """The portion of time during the sliding window duration that this
        condition must be true in order for the associated alarm to trigger
        """
        self.intersection_point: IntersectionPointType = intersection_point
        """The point in each detection that must be within the zone in order
        for that detection to be counted as in that zone
        """
        self.id: int = id_
        """A unique identifier"""

    def __repr__(self):
        condition_str = condition_test_map[self.test.value]
        attr = self.with_attribute
        attr = attr.value + ' ' if attr else ''
        return f"{condition_str} {self.check_value} " \
               f"{attr}{self.with_class_name}(s) "

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        d["test"] = self.test.value
        d["intersection_point"] = self.intersection_point.value
        if self.with_attribute is not None:
            d["with_attribute"] = self.with_attribute.to_dict()

        return d

    @staticmethod
    def from_dict(d: dict):
        intersection_point = IntersectionPointType(
            d["intersection_point"])
        # with_attribute is an optional parameter
        with_attribute = None
        if d["with_attribute"] is not None:
            with_attribute = Attribute.from_dict(d["with_attribute"])
        test = ZoneAlarmCountCondition.TestType(d["test"])

        return ZoneAlarmCountCondition(
            test=test,
            check_value=d["check_value"],
            with_class_name=d["with_class_name"],
            with_attribute=with_attribute,
            window_duration=d["window_duration"],
            window_threshold=d["window_threshold"],
            intersection_point=intersection_point,
            id_=d["id"])


class RateConditionTestType(Enum):
    """Defines the way a rate condition compares the actual rate value to the
    alarm's test value.
    """

    GREATER_THAN_OR_EQUAL_TO = ">="
    LESS_THAN_OR_EQUAL_TO = "<="

    @classmethod
    def values(cls):
        return [v.value for v in cls]


class DirectionType(Enum):
    """Defines the direction of flow that a rate condition pertains to."""

    ENTERING = "entering"
    EXITING = "exiting"
    ENTERING_OR_EXITING = "entering_or_exiting"

    @classmethod
    def values(cls):
        return [v.value for v in cls]


class ZoneAlarmRateCondition(Codec):
    """A condition that must be met for an alarm to go off. Compares the rate
    of change in the count of some object against a test value.
    """

    direction_map = {DirectionType.ENTERING: "entered",
                     DirectionType.EXITING: "exited",
                     DirectionType.ENTERING_OR_EXITING: "entered or exited"}

    def __init__(self, *,
                 test: RateConditionTestType,
                 duration: float,
                 change: float,
                 direction: DirectionType,
                 with_class_name: str,
                 with_attribute: Optional[Attribute],
                 intersection_point: IntersectionPointType,
                 id_: int = None):
        self.test: RateConditionTestType = test
        """The way that the change value will be compared to the actual rate"""
        self.duration: float = duration
        """The time in seconds for this rate change to occur"""
        self.change: float = change
        """The rate change value to compare the actual rate value against"""
        self.direction: DirectionType = direction
        """The direction of flow this condition tests for"""
        self.with_class_name: str = with_class_name
        """The class name of the objects to measure rate of change for"""
        self.with_attribute: Optional[Attribute] = with_attribute
        """If provided, only objects that have this attribute will be counted
        in the rate calculation
        """
        self.intersection_point: IntersectionPointType = intersection_point
        """The point in each detection that must be within the zone in order
        for that detection to be counted as in that zone
        """
        self.id: int = id_
        """A unique identifier"""

    def __repr__(self):
        condition_str = condition_test_map[self.test.value]
        direction_str = self.direction_map[self.direction]
        return f"{condition_str} {self.change} {self.with_class_name}(s) " \
               f"{direction_str} within {self.duration} seconds"

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        d["intersection_point"] = self.intersection_point.value
        if self.with_attribute is not None:
            d["with_attribute"] = self.with_attribute.to_dict()

        d["direction"] = self.direction.value
        d["test"] = self.test.value

        return d

    @staticmethod
    def from_dict(d: dict):
        intersection_point = IntersectionPointType(
            d["intersection_point"])
        # with_attribute is an optional parameter
        with_attribute = None
        if d["with_attribute"] is not None:
            with_attribute = Attribute.from_dict(d["with_attribute"])
        test = ZoneAlarmRateCondition.TestType(d["test"])

        return ZoneAlarmRateCondition(
            test=test,
            duration=d["duration"],
            change=d["change"],
            direction=ZoneAlarmRateCondition.DirectionType(d["direction"]),
            with_class_name=d["with_class_name"],
            with_attribute=with_attribute,
            intersection_point=intersection_point,
            id_=d["id"])
