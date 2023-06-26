from typing import Dict, List, Optional


from brainframe.api.bf_codecs import Snip
from .base_stub import BaseStub, DEFAULT_TIMEOUT


class ImagesStubMixIn(BaseStub):
    """Provides stubs to call APIs for images 
    """

    def get_snip_image(self, snip: Snip, 
        timeout=DEFAULT_TIMEOUT) -> Optional[dict]:
        """get a snip image from the server.
        :param snip:  Snip 
        :param timeout: The timeout to use for this request
        :return: a dict or None
        """
        req = "/api/images/snip"

        data = self._post_codec(req, 
                    timeout, 
                    snip)
        return data


