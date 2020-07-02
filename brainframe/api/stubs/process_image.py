from typing import Dict, List

import numpy as np
import json

from brainframe.api.bf_codecs import Detection, image_utils
from .base_stub import BaseStub, DEFAULT_TIMEOUT


class ProcessImageStubMixIn(BaseStub):
    """Provides stubs to call APIs that run processing on a single frame."""

    def process_image(self, img_bgr: np.ndarray,
                      capsule_names: List[str],
                      option_vals: Dict[str, Dict[str, object]],
                      timeout=DEFAULT_TIMEOUT) \
            -> List[Detection]:
        """Process a single image using the given configuration.
        :param img_bgr: The image to process
        :param capsule_names: The capsule names to enable while processing the
            image
        :param option_vals: Capsule option values, where the key is a capsule
            name and the value is a dict with key-value pairs for each option
            and its corresponding value. Any specified options will override
            the global option values for that capsule
        :param timeout: The timeout to use for this request
        :return: All detections in the image
        """
        req = f"/api/process_image"

        metadata = {
            "plugins": capsule_names,
            "options": option_vals
        }
        metadata = json.dumps(metadata)

        # Encode the image
        img_bytes = image_utils.encode("jpeg", img_bgr)

        files = {
            "image": ("image.jpg",
                      img_bytes,
                      "image/jpeg"),
            "metadata": ("metadata.json",
                         metadata.encode("utf-8"),
                         "application/json")}

        resp = self._post_multipart(req, timeout, files)
        return [Detection.from_dict(d) for d in resp]
