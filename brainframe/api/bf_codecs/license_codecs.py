from datetime import date, datetime
from typing import Optional
from enum import Enum

from dataclasses import dataclass

from .base_codecs import Codec


@dataclass
class LicenseTerms(Codec):
    """The terms of the currently active license."""

    online_checkin: bool
    """If True, the server will check in with a remote licensing server to
    verify license terms.
    """

    max_streams: int
    """The maximum number of streams that may have analysis enabled at any
    given time.
    """

    journal_max_allowed_age: float
    """The maximum amount of time in seconds that the server may hold data
    in the journal for.
    """

    expiration_date: Optional[date]
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


@dataclass
class LicenseInfo(Codec):
    """Information on the licensing status of the server"""

    class State(Enum):
        VALID = "valid"
        """A valid license is loaded, features should be enabled"""
        INVALID = "invalid"
        """A license was provided, but did not pass validation"""
        EXPIRED = "expired"
        """A license was provided, but it has expired"""
        MISSING = "missing"
        """No license was provided"""

    state: State
    """The licensing state of the server."""

    terms: Optional[LicenseTerms]
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
