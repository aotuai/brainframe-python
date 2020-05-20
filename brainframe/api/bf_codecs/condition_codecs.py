from enum import Enum

from .base_codecs import Codec
from .detection_codecs import Attribute


condition_test_map = {'>': "Greater than",
                      '>=': "Greater than or equal to",
                      '<': "Less than",
                      '<=': "Less than or equal to",
                      "=": "Exactly",
                      "!=": "Not Equal To"}


class CountConditionTestType(Enum):
    GREATER_THAN = ">"
    LESS_THAN = "<"
    EQUAL_TO = "="
    NOT_EQUAL_TO = "!="

    @classmethod
    def values(cls):
        return [v.value for v in cls]


class IntersectionPointType(Enum):
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

    TestType = CountConditionTestType
    IntersectionPointType = IntersectionPointType

    def __init__(self, *, test, check_value, with_class_name, with_attribute,
                 window_duration, window_threshold, intersection_point,
                 id_=None):
        self.test = test
        self.check_value = check_value
        self.with_class_name = with_class_name
        self.with_attribute = with_attribute
        self.window_duration = window_duration
        self.window_threshold = window_threshold
        self.intersection_point = intersection_point
        self.id = id_

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
    GREATER_THAN_OR_EQUAL_TO = ">="
    LESS_THAN_OR_EQUAL_TO = "<="

    @classmethod
    def values(cls):
        return [v.value for v in cls]


class DirectionType(Enum):
    ENTERING = "entering"
    EXITING = "exiting"
    ENTERING_OR_EXITING = "entering_or_exiting"

    @classmethod
    def values(cls):
        return [v.value for v in cls]


class ZoneAlarmRateCondition(Codec):
    """A condition that must be met for an alarm to go off. Compares the rate of
    change in the count of some object against a test value.
    """

    TestType = RateConditionTestType
    DirectionType = DirectionType

    direction_map = {DirectionType.ENTERING: "entered",
                     DirectionType.EXITING: "exited",
                     DirectionType.ENTERING_OR_EXITING: "entered or exited"}

    def __init__(self, *, test, duration, change, direction, with_class_name,
                 with_attribute, intersection_point, id_=None):
        self.test = test
        self.duration = duration
        self.change = change
        self.direction = direction
        self.with_class_name = with_class_name
        self.with_attribute = with_attribute
        self.intersection_point = intersection_point
        self.id = id_

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
