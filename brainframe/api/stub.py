from typing import Tuple
from time import sleep, time

from requests.exceptions import ConnectionError, ReadTimeout

from .bf_errors import UnauthorizedError, UnknownError, ServerNotReadyError
from . import stubs
from .stubs.base_stub import DEFAULT_TIMEOUT


class BrainFrameAPI(stubs.AlertStubMixin,
                    stubs.AnalysisStubMixin,
                    stubs.IdentityStubMixin,
                    stubs.CapsuleStubMixin,
                    stubs.StreamStubMixin,
                    stubs.ZoneStatusStubMixin,
                    stubs.ZoneStubMixin,
                    stubs.StorageStubMixin,
                    stubs.ZoneAlarmStubMixin,
                    stubs.ProcessImageStubMixIn,
                    stubs.EncodingStubMixIn,
                    stubs.PremisesStubMixin,
                    stubs.UserStubMixin,
                    stubs.LicenseStubMixIn):
    """Provides access to BrainFrame API endpoints."""

    def __init__(self, server_url=None, credentials: Tuple[str, str] = None):
        """
        :param server_url: The URL of the BrainFrame instance to connect to. If
            None, it needs to be set later with set_url before use
        :param credentials: The username and password as a tuple. Used to
            authenticate with the server. If None, no authentication
            information will be provided.
        """
        super().__init__()
        self._server_url = server_url
        self._credentials = credentials

    def version(self, timeout=DEFAULT_TIMEOUT) -> str:
        """
        :return: The current BrainFrame version in the format X.Y.Z
        """
        req = f"/api/version"

        resp, _ = self._get_json(req, timeout)
        return resp

    def wait_for_server_initialization(self, timeout: float = None):
        """Waits for the server to be ready to handle requests.

        :param timeout: The maximum amount of time, in seconds, to wait for the
            server to start. If None, this method will wait indefinitely.
        """
        start_time = time()
        while True:
            if timeout is not None and time() - start_time > timeout:
                raise TimeoutError("The server did not start in time!")

            try:
                # Test connection to server
                self.version()
            except (ConnectionError, ConnectionRefusedError, ReadTimeout,
                    UnauthorizedError, ServerNotReadyError):
                # Server not started yet or there is a communication
                # error
                pass
            except UnknownError as exc:
                if exc.status_code not in [502]:
                    raise
            else:
                break

            # Prevent busy loop
            sleep(.1)

    def close(self):
        """Clean up the API. It may no longer be used after this call."""
        stubs.StreamStubMixin.close(self)
