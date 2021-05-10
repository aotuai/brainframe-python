from brainframe.api.bf_codecs import CloudTokens, CloudUserInfo
from .base_stub import BaseStub, DEFAULT_TIMEOUT


class CloudTokensStubMixin(BaseStub):
    def set_cloud_tokens(self, cloud_tokens: CloudTokens,
                         timeout=DEFAULT_TIMEOUT) -> CloudUserInfo:
        """Authorizes the server against BrainFrame Cloud using the provided tokens.

        :param cloud_tokens: The tokens to use for authorization
        :param timeout: the timeout to use for this request
        :return: Info on the BrainFrame Cloud user that corresponds to these tokens
        """
        req = "/api/cloud_tokens"
        user_info_dict = self._put_codec(req, timeout, cloud_tokens)

        return CloudUserInfo.from_dict(user_info_dict)
