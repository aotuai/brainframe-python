from typing import Optional

from brainframe.api.bf_codecs import CloudUserInfo
from brainframe.api.bf_errors import CloudUserNotFoundError

from .base_stub import BaseStub, DEFAULT_TIMEOUT


class CloudUsersStubMixIn(BaseStub):
    def get_current_cloud_user(self, timeout=DEFAULT_TIMEOUT) \
            -> Optional[CloudUserInfo]:
        """Gets information on the cloud user that's currently logged in.

        :param timeout: The timeout to use for this request
        :return: Information on the cloud user, or None if no user is logged in
        """
        req = f"/api/cloud_user"
        try:
            data, _ = self._get_json(req, timeout=timeout)
        except CloudUserNotFoundError:
            return None
        else:
            return CloudUserInfo.from_dict(data)
