import re
from typing import Optional


kind_to_error_type = {}
"""Maps error kinds to their corresponding error type."""


def _register_error(kind: Optional[str] = None):
    """A class decorator. Registers the given class so that it will be used
    when an error with a kind equal to the class's name is provided as a
    response.

    :param kind: If provided, this class will be associated with this kind
        instead of using the class's name as the kind
    """
    def wrapper(cls):
        global kind_to_error_type
        nonlocal kind

        if kind is None:
            kind = cls.__name__
        kind_to_error_type[kind] = cls
        cls.kind = kind
        return cls

    return wrapper


class BaseAPIError(Exception):
    """All API errors subclass this error."""
    # This is set by the decorator
    kind = None

    def __init__(self, description):
        self.description = description
        super().__init__(f"{self.kind}: {description}")

    @property
    def pretty_name(self):
        name = self.__class__.__name__

        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1).capitalize()
        s3 = s2.rsplit(" error")[0]

        return s3


@_register_error()
class UnknownError(BaseAPIError):
    """Something unexpected happened. The server may be in an invalid state."""

    def __init__(self, description, status_code=None):
        super().__init__(description)
        self.status_code = status_code


@_register_error()
class StreamConfigNotFoundError(BaseAPIError):
    """A StreamConfiguration specified by the client could not be found."""


@_register_error()
class ZoneNotFoundError(BaseAPIError):
    """A Zone specified by the client could not be found."""


@_register_error()
class PremisesNotFoundError(BaseAPIError):
    """A Zone specified by the client could not be found."""


@_register_error()
class ZoneNotDeletableError(BaseAPIError):
    """A client tried to delete a default Zone"""


@_register_error()
class AlertNotFoundError(BaseAPIError):
    """An Alert specified by the client could not be found."""


@_register_error()
class InvalidSyntaxError(BaseAPIError):
    """The syntax of the request could not be parsed."""


@_register_error()
class InvalidFormatError(BaseAPIError):
    """The request was parsed, but some value within the request is invalid."""


@_register_error("NotImplementedError")
class NotImplementedInAPIError(BaseAPIError):
    """The client requested something that is not currently implemented."""


@_register_error()
class StreamNotOpenedError(BaseAPIError):
    """A stream failed to open when it was required to."""


@_register_error()
class DuplicateStreamSourceError(BaseAPIError):
    """There was an attempted to create a stream configuration with the same
    source as an existing one.
    """


@_register_error()
class DuplicateZoneNameError(BaseAPIError):
    """There was an attempt to make a zone with the same name as another zone
    within the same stream.
    """


@_register_error()
class DuplicateIdentityNameError(BaseAPIError):
    """There was an attempt to create a new identity with the same name as
    another identity.
    """


@_register_error()
class NoDetectorForClassError(BaseAPIError):
    """There was an attempt to use a class name that is not detectable."""


@_register_error()
class NoEncoderForClassError(BaseAPIError):
    """There was an attempt to create an identity for a class that is not
    encodable.
    """


@_register_error()
class IdentityNotFoundError(BaseAPIError):
    """An identity specified by the client could not be found."""


@_register_error()
class ImageNotFoundForIdentityError(BaseAPIError):
    """An image specified by the client could not be found for the specified
    identity.
    """


@_register_error()
class InvalidImageTypeError(BaseAPIError):
    """An image could not be decoded by OpenCV"""


@_register_error()
class AnalysisLimitExceededError(BaseAPIError):
    """There was an attempt to start analysis on a stream, but the maximum
    amount of streams that may have analysis run on them at once has already
    been reached.
    """


@_register_error()
class NoDetectionsInImageError(BaseAPIError):
    """There was an attempt to encode an image with no objects of the given
    class in the frame.
    """


@_register_error()
class TooManyDetectionsInImageError(BaseAPIError):
    """There was an attempt to encode an image with more than one object of the
    given class in the frame, causing ambiguity on which one to encode.
    """


@_register_error()
class ImageAlreadyEncodedError(BaseAPIError):
    """There was an attempt to encode an image that has already been encoded for
    a given identity and a given class.
    """


@_register_error()
class DuplicateVectorError(BaseAPIError):
    """There was an attempt to add a vector that already exists for the given
    identity and class.
    """


@_register_error()
class FrameNotFoundForAlertError(BaseAPIError):
    """There was an attempt to get a frame for an alert that has no frame."""


@_register_error()
class PluginNotFoundError(BaseAPIError):
    """There was an attempt to reference a plugin that does not exist."""


@_register_error()
class InvalidPluginOptionError(BaseAPIError):
    """The provided plugin options do not work for the given plugin. This could
    be because the option does not exist or the value for that option doesn't
    fit the constraints.
    """


@_register_error()
class StorageNotFoundError(BaseAPIError):
    """There was an attempt to access a storage object that does not exist."""


@_register_error()
class ZoneAlarmNotFoundError(BaseAPIError):
    """There was an attempt to access a zone alarm that does not exist."""


@_register_error()
class InvalidRuntimeOptionError(BaseAPIError):
    """There was an attempt to set a runtime option that is not supported or is
    of the wrong type.
    """


@_register_error()
class EncodingNotFoundError(BaseAPIError):
    """There was an attempt to access an encoding that does not exist."""


@_register_error()
class UnauthorizedError(BaseAPIError):
    """There was an attempt to access the API without proper authorization."""


@_register_error()
class InvalidSessionError(BaseAPIError):
    """There was an attempt to access the API with an invalid session ID,
    either because the session expired or no session with that ID has ever
    existed. The client should authenticate again to get a new session.
    """


@_register_error()
class VectorTooLongError(BaseAPIError):
    """The provided encoding vector is longer than the maximum allowed
    length.
    """


@_register_error()
class UserNotFoundError(BaseAPIError):
    """There was an attempt to access a user by ID that does not exist."""


@_register_error()
class InsufficientRoleError(BaseAPIError):
    """A user attempted an operation that they don't have permission to do."""


@_register_error()
class DuplicateUsernameError(BaseAPIError):
    """The requested username already exists."""


@_register_error()
class AdminMustExistError(BaseAPIError):
    """There was an attempt to delete the only remaining admin account."""


@_register_error()
class LicenseRequiredError(BaseAPIError):
    """There was an attempt to access a resource that requires an active
    license while no valid license is loaded.
    """


@_register_error()
class LicenseExpiredError(BaseAPIError):
    """There was an attempt to upload a license that is expired."""


@_register_error()
class LicenseInvalidError(BaseAPIError):
    """There was an attempt to upload a license that is in an invalid format.
    """
