from datetime import date, datetime
from typing import Optional
from enum import Enum

from .base_codecs import Codec


class LicenseTerms(Codec):
    """The terms of the currently active license."""

    def __init__(self, *,
                 online_checkin: bool,
                 max_streams: int,
                 journal_max_allowed_age: float,
                 expiration_date: Optional[date]):
        self.online_checkin: bool = online_checkin
        """If True, the server will check in with a remote licensing server to
        verify license terms.
        """
        self.max_streams: int = max_streams
        """The maximum number of streams that may have analysis enabled at any
        given time.
        """
        self.journal_max_allowed_age: float = journal_max_allowed_age
        """The maximum amount of time in seconds that the server may hold data
        in the journal for.
        """
        self.expiration_date: Optional[date] = expiration_date
        """The date that this license expires, or None if the license is
        perpetual.
        """

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        if self.expiration_date is not None:
            d["expiration_date"] = self.expiration_date.isoformat()
        return d

    @staticmethod
    def from_dict(d: dict) -> "LicenseTerms":
        expiration_date = None
        if d["expiration_date"] is not None:
            # TODO: Switch to date.fromisoformat when we're on Python >= 3.7
            expiration_date = datetime.strptime(
                d["expiration_date"], DATE_FORMAT).date()

        terms = LicenseTerms(
            online_checkin=d["online_checkin"],
            max_streams=d["max_streams"],
            journal_max_allowed_age=d["journal_max_allowed_age"],
            expiration_date=expiration_date,
        )
        return terms


class LicenseState(Enum):
    VALID = "valid"
    """A valid license is loaded, features should be enabled"""
    INVALID = "invalid"
    """A license was provided, but did not pass validation"""
    EXPIRED = "expired"
    """A license was provided, but it has expired"""
    MISSING = "missing"
    """No license was provided"""


class LicenseInfo(Codec):
    """Information on the licensing status of the server"""

    def __init__(self, *, state: LicenseState, terms: Optional[LicenseTerms]):
        self.state: LicenseState = state
        """The licensing state of the server."""
        self.terms: Optional[LicenseTerms] = terms
        """The active license terms of the server, or None if no license is
        loaded.
        """

    def to_dict(self) -> dict:
        return {
            "state": self.state.value,
            "terms": self.terms.to_dict() if self.terms else None,
        }

    @staticmethod
    def from_dict(d: dict) -> "LicenseInfo":
        terms = None
        if d["terms"] is not None:
            terms = LicenseTerms.from_dict(d["terms"])

        return LicenseInfo(
            state=LicenseInfo.State(d["state"]),
            terms=terms,
        )


DATE_FORMAT = "%Y-%m-%d"
"""ISO 8601 date format used by the API"""
