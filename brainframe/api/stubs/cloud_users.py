from typing import Optional

from brainframe.api.bf_codecs import CloudUserInfo
from brainframe.api.bf_errors import CloudUserNotFoundError

from .base_stub import BaseStub, DEFAULT_TIMEOUT


class CloudUsersStubMixIn(BaseStub):
    def get_cloud_user(self, timeout=DEFAULT_TIMEOUT) -> Optional[CloudUserInfo]:
        req = f"/api/cloud_user"
        try:
            data, _ = self._get_json(req, timeout=timeout)
            return CloudUserInfo.from_dict(data)
        except CloudUserNotFoundError:
            return None
