import json
from typing import Dict, Generator

import requests

from brainframe.api import bf_codecs, bf_errors
from .base_stub import BaseStub, DEFAULT_TIMEOUT

ZONE_STATUS_TYPE = Dict[int, Dict[str, bf_codecs.ZoneStatus]]
ZONE_STATUS_STREAM_TYPE = Generator[ZONE_STATUS_TYPE, None, None]


class ZoneStatusStubMixin(BaseStub):
    """Provides stubs for calling APIs to get zone statuses."""

    def get_latest_zone_statuses(self,
                                 timeout=DEFAULT_TIMEOUT) -> ZONE_STATUS_TYPE:
        """This method gets all of the latest processed zone statuses for every
        zone and for every stream.

        All active streams will have a key in the output dict.

        :param timeout: The timeout to use for this request
        :return: A dict whose keys are stream IDs and whose value is another
            dict. This nested dict's keys are zone names and their value is the
            ZoneStatus for that zone.
        """
        req = "/api/streams/status"
        data, _ = self._get_json(req, timeout)

        # Convert ZoneStatuses to Codecs
        out = {int(s_id): {key: bf_codecs.ZoneStatus.from_dict(val)
                           for key, val in statuses.items()}
               for s_id, statuses in data.items()}
        return out

    def get_zone_status_stream(self, timeout=None) -> ZONE_STATUS_STREAM_TYPE:
        """Streams ZoneStatus results from the server as they are produced.

        All active streams will have a key in the output dict.

        :param timeout: The timeout to use for this request
        :return: A generator that outputs dicts whose keys are stream IDs and
            whose value is another dict. This nested dict's keys are zone names
            and their value is the ZoneStatus for that zone.
        """
        req = "/api/streams/statuses"

        def zone_status_iterator():
            # Don't use a timeout for this request, since it's ongoing
            resp = self._get(req, timeout=timeout)

            packets = resp.iter_lines(delimiter=b"\r\n")
            while True:
                try:
                    packet = next(packets)
                except requests.exceptions.ChunkedEncodingError as exc:
                    message = "Incomplete packet while attempting to read " \
                              "from zone status iterator"
                    raise bf_errors.ServerNotReadyError(message) from exc
                except requests.exceptions.RequestException as exc:
                    message = "A network exception occurred while " \
                              "communicating with the BrainFrame server"
                    new_exc = bf_errors.ServerNotReadyError(message)
                    new_exc.__cause__ = exc
                    raise bf_errors.ServerNotReadyError(message)

                if packet == b'':
                    continue

                # Parse the line
                zone_statuses_dict = json.loads(packet)

                processed = {
                    int(s_id): {key: bf_codecs.ZoneStatus.from_dict(val)
                                for key, val in statuses.items()}
                    for s_id, statuses in zone_statuses_dict.items()}
                yield processed

        return zone_status_iterator()
