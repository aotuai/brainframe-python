from typing import Tuple

from brainframe.api.bf_codecs import CloudTokens, CloudUserInfo, LicenseInfo
from .base_stub import BaseStub, DEFAULT_TIMEOUT


class CloudTokensStubMixin(BaseStub):
    def set_cloud_tokens(self, cloud_tokens: CloudTokens,
                         timeout=DEFAULT_TIMEOUT) -> Tuple[CloudUserInfo, LicenseInfo]:
        """Authorizes the server against BrainFrame Cloud using the provided tokens.

        :param cloud_tokens: The tokens to use for authorization
        :param timeout: the timeout to use for this request
        :return: Info on the BrainFrame Cloud user that corresponds to these tokens
        """
        req = "/api/cloud_tokens"
        login_result = self._put_codec(req, timeout, cloud_tokens)

        cloud_user_info = CloudUserInfo.from_dict(login_result["cloud_user_info"])
        license_info = LicenseInfo.from_dict(login_result["license_info"])

        return cloud_user_info, license_info
