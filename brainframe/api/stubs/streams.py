from typing import Dict, List, Optional

import json

from brainframe.api.bf_codecs import StreamConfiguration
from .base_stub import BaseStub, DEFAULT_TIMEOUT


class StreamStubMixin(BaseStub):
    """Provides stubs for calling stream-related APIs and managing
    stream-related client objects.
    """

    def __init__(self):
        # These are evaluated lazily
        self._status_receiver = None

    def get_status_receiver(self) -> "StatusReceiver":
        """Returns a singleton StatusReceiver object"""
        from brainframe.api import StatusReceiver
        if self._status_receiver is None \
                or not self._status_receiver.is_running:
            self._status_receiver = StatusReceiver(self)
        return self._status_receiver

    def get_stream_configuration(self, stream_id, timeout=DEFAULT_TIMEOUT) \
            -> StreamConfiguration:
        """Gets the StreamConfiguration with the given ID.

        :param stream_id: The ID of the stream configuration to get
        :param timeout: The timeout to use for this request
        :return: The stream configuration
        """
        req = f"/api/streams/{stream_id}"
        data, _ = self._get_json(req, timeout)

        return StreamConfiguration.from_dict(data)

    def get_stream_configurations(self, premises_id=None,
                                  timeout=DEFAULT_TIMEOUT) \
            -> List[StreamConfiguration]:
        """Get all StreamConfigurations that currently exist.

        :return: [StreamConfiguration, StreamConfiguration, ...]
        """
        req = "/api/streams"
        params = {"premises_id": premises_id} if premises_id else None
        data, _ = self._get_json(req, timeout, params=params)

        configs = [StreamConfiguration.from_dict(d) for d in data]
        return configs

    def set_stream_configuration(self, stream_configuration,
                                 timeout=DEFAULT_TIMEOUT) \
            -> Optional[StreamConfiguration]:
        """Update an existing stream configuration or create a new one. If
        creating a new one, the stream_configuration.id will be None.

        :param stream_configuration: StreamConfiguration
        :param timeout: The timeout to use for this request
        :return: StreamConfiguration, initialized with an ID
        """
        req = "/api/streams"
        data = self._post_codec(req, timeout, stream_configuration)
        config = StreamConfiguration.from_dict(data)
        return config

    # TODO: Remove this long timeout when this endpoint is better optimized
    def delete_stream_configuration(self, stream_id,
                                    timeout=120):
        """Deletes a stream configuration with the given ID. Also stops
        analysis if analysis was running and closes the stream.

        :param stream_id: The ID of the stream to delete
        :param timeout: The timeout to use for this request
        """
        req = f"/api/streams/{stream_id}"
        self._delete(req, timeout)

    def get_stream_url(self, stream_id,
                       timeout=DEFAULT_TIMEOUT) -> str:
        """Gets the URL that the stream is available at.

        :param stream_id: The ID of the stream to get a URL for
        :param timeout: The timeout to use for this request
        :return: The URL
        """
        req = f"/api/streams/{stream_id}/url"
        url, _ = self._get_json(req, timeout)
        return url

    def get_runtime_options(self, stream_id: int,
                            timeout=DEFAULT_TIMEOUT) -> Dict[str, object]:
        """Returns the runtime options for the stream with the given ID. This
        can also be read from a StreamConfiguration object.

        :param stream_id: The ID of the stream to get runtime options from
        :param timeout: The timeout to use for this request
        :return: Runtime options
        """
        req = f"/api/streams/{stream_id}/runtime_options"
        runtime_options, _ = self._get_json(req, timeout)

        return runtime_options

    def set_runtime_option_vals(self, stream_id: int,
                                runtime_options: Dict[str, object],
                                timeout=DEFAULT_TIMEOUT):
        """Sets a stream's runtime options to the given values.

        :param stream_id: The ID of the stream to set runtime options for
        :param runtime_options: The runtime options
        :param timeout: The timeout to use for this requestz
        """
        req = f"/api/streams/{stream_id}/runtime_options"
        runtime_options_json = json.dumps(runtime_options)
        self._put_json(req, timeout, runtime_options_json)

    def close(self):
        if self._status_receiver is not None:
            self._status_receiver.close()
            self._status_receiver = None
