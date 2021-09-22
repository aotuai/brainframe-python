from brainframe.api.bf_codecs import OAuth2Info
from .base_stub import BaseStub, DEFAULT_TIMEOUT


class OAuth2StubMixIn(BaseStub):
    """Provides stubs for calling APIs related to OAuth2"""

    def get_oauth2_info(self, timeout: float = DEFAULT_TIMEOUT) -> OAuth2Info:
        """Gets the necessary information to start an OAuth2 on behalf of the server.

        :param timeout: The timeout to use for this request
        :return: The OAuth2 info
        """
        req = "/api/oauth2_info"
        data, _ = self._get_json(req, timeout)
        return OAuth2Info.from_dict(data)
