import json
from typing import Dict, List, Optional

from brainframe.api.bf_codecs import Capsule
from .base_stub import BaseStub, DEFAULT_TIMEOUT


class CapsuleStubMixin(BaseStub):
    """Provides stubs to call APIs to inspect and configure capsules."""

    def get_capsule(self, name,
                    timeout=DEFAULT_TIMEOUT) -> Capsule:
        """
        :param name: The name of the capsule to get
        :param timeout: The timeout to use for this request
        :return: Capsule with the given name
        """
        req = f"/api/plugins/{name}"
        capsule, _ = self._get_json(req, timeout)
        return Capsule.from_dict(capsule)

    def get_capsules(self, timeout=DEFAULT_TIMEOUT) -> List[Capsule]:
        """
        :param timeout: The timeout to use for this request
        :return: All available capsules
        """
        req = "/api/plugins"
        capsules, _ = self._get_json(req, timeout)
        return [Capsule.from_dict(d) for d in capsules]

    def get_capsule_option_vals(self, capsule_name, stream_id=None,
                                timeout=DEFAULT_TIMEOUT) \
            -> Dict[str, object]:
        """Gets the current values for every capsule option. See the
        documentation for the CapsuleOption codec for more info about global
        and stream level options and how they interact.

        :param capsule_name: The capsule to find options for
        :param stream_id: The ID of the stream. If this value is None, then the
            global options are returned for that capsule
        :param timeout: The timeout to use for this request
        :return: A dict where the key is the option name and the value is the
            option's current value
        """
        if stream_id is None:
            req = f"/api/plugins/{capsule_name}/options"
        else:
            req = f"/api/streams/{stream_id}/plugins/{capsule_name}/options"
        capsule_option_vals, _ = self._get_json(req, timeout)

        return capsule_option_vals

    def set_capsule_option_vals(self, *, capsule_name, stream_id=None,
                                option_vals: Dict[str, object],
                                timeout=DEFAULT_TIMEOUT):
        """Sets option values for a capsule.

        :param capsule_name: The name of the capsule whose options to set
        :param stream_id: The ID of the stream, if these are stream-level
            options. If this value is None, then the global options are set
        :param option_vals: A dict where the key is the name of the option to
            set, and the value is the value to set that option to
        :param timeout: The timeout to use for this request
        """
        if stream_id is None:
            req = f"/api/plugins/{capsule_name}/options"
        else:
            req = f"/api/streams/{stream_id}/plugins/{capsule_name}/options"

        option_values_json = json.dumps(option_vals)
        self._put_json(req, timeout, option_values_json)

    def patch_capsule_option_vals(self, *, capsule_name, stream_id=None,
                                  option_vals: Dict[str, object],
                                  timeout=DEFAULT_TIMEOUT):
        """Patches option values for a capsule. Only the provided options are
        changed. To unset an option, provide that option with a value of None.

        :param capsule_name: The name of the capsule whose options to set
        :param stream_id: The ID of the stream, if these are stream-level
            options. If this value is None, then the global options are set
        :param option_vals: A dict where the key is the name of the option to
            set, and the value is the value to set that option to
        :param timeout: The timeout to use for this request
        """
        if stream_id is None:
            req = f"/api/plugins/{capsule_name}/options"
        else:
            req = f"/api/streams/{stream_id}/plugins/{capsule_name}/options"

        option_values_json = json.dumps(option_vals)
        self._patch_json(req, timeout, option_values_json)

    def is_capsule_active(self, capsule_name, stream_id=None,
                          timeout=DEFAULT_TIMEOUT) -> bool:
        """Returns True if the capsule is active. If a capsule is not marked as
        active, it will not run. Like capsule options, this can be configured
        globally and on a per-stream level.

        :param capsule_name: The name of the capsule to get activity for
        :param stream_id: The ID of the stream, if you want the per-stream
            active setting
        :param timeout: The timeout to use for this request
        :return: True if the capsule is active
        """
        if stream_id is None:
            req = f"/api/plugins/{capsule_name}/active"
        else:
            req = f"/api/streams/{stream_id}/plugins/{capsule_name}/active"
        capsules_active, _ = self._get_json(req, timeout)
        return capsules_active

    def set_capsule_active(self, *, capsule_name, stream_id=None,
                           active: Optional[bool],
                           timeout=DEFAULT_TIMEOUT):
        """Sets whether or not the capsule is active. If a capsule is active, it
        will be run on frames.

        :param capsule_name: The name of the capsule to set activity for
        :param stream_id: The ID of the stream, if you want to set the
            per-stream active setting
        :param active: True if the capsule should be set to active
        :param timeout: The timeout to use for this request
        """
        if stream_id is None:
            req = f"/api/plugins/{capsule_name}/active"
        else:
            req = f"/api/streams/{stream_id}/plugins/{capsule_name}/active"

        active_json = json.dumps(active)

        self._put_json(req, timeout, active_json)
