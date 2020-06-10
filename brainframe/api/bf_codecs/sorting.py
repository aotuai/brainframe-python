from enum import Enum


class Ordering(Enum):
    """Specifies in what order a field should be sorted by."""
    ASC = "asc"
    """The order of the field should be ascending (from low to high)"""
    DESC = "desc"
    """The order of the field should be descending (from high to low)"""


class SortOptions:
    """A sorting configuration. Used by some APIs that provide many of a
    certain object.
    """

    def __init__(self, field_name: str, ordering: Ordering):
        self.field_name: str = field_name
        """The name of the field to sort by"""
        self.ordering: Ordering = ordering
        """The order to sort the field by"""

    def query_format(self) -> str:
        return f"{self.field_name}:{self.ordering.value}"
