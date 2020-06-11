from typing import List, Optional, Tuple

import json

from brainframe.api.bf_codecs import Encoding, Identity, SortOptions
from .base_stub import BaseStub, DEFAULT_TIMEOUT


class IdentityStubMixin(BaseStub):
    """Provides stubs to call APIs that create and update identities, as well
    as add new examples of the identity in image or vector form.
    """

    def get_identity(self, identity_id: int,
                     timeout=DEFAULT_TIMEOUT) -> Identity:
        """Gets the identity with the given ID.

        :param identity_id: The ID of the identity to get
        :param timeout: The timeout to use for this request
        :return: Identity
        """
        req = f"/api/identities/{identity_id}"
        identity, _ = self._get_json(req, timeout)

        return Identity.from_dict(identity)

    def get_identities(self, unique_name: str = None,
                       encoded_for_class: str = None,
                       search: Optional[str] = None,
                       limit: int = None,
                       offset: int = None,
                       sort_by: SortOptions = None,
                       timeout=DEFAULT_TIMEOUT) \
            -> Tuple[List[Identity], int]:
        """Returns all identities from the server.

        :param unique_name: If provided, identities will be filtered by only
            those who have the given unique name
        :param encoded_for_class: If provided, identities will be filtered for
            only those that have been encoded at least once for the given class
        :param search: If provided, only identities that in some way contain
            the given search query are returned. This is intended for UI search
            features, and as such the specific semantics of how the search is
            performed are subject to change.
        :param limit: If provided, the number of returned identities is limited
            to this value.
        :param offset: The offset to start limiting results from. This is only
            useful when providing a limit.
        :param sort_by: If provided, the results will be sorted by the given
            configuration
        :param timeout: The timeout to use for this request
        :return: A list of identities, and the total number of identities that
            fit this criteria, ignoring pagination (the limit and offset)
        """
        req = f"/api/identities"

        params = {}
        if unique_name is not None:
            params["unique_name"] = unique_name
        if encoded_for_class is not None:
            params["encoded_for_class"] = encoded_for_class
        if search is not None:
            params["search"] = search
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if sort_by is not None:
            params["sort_by"] = sort_by.query_format()

        identities, headers = self._get_json(req, timeout, params=params)
        identities = [Identity.from_dict(d) for d in identities]

        total_count = int(headers["Total-Count"])

        return identities, total_count

    def set_identity(self, identity: Identity,
                     timeout=DEFAULT_TIMEOUT) -> Identity:
        """Updates or creates an identity. If the identity does not already
        exist, identity.id must be None. The returned identity will have an
        assigned ID.

        :param identity: The identity to save or create
        :param timeout: The timeout to use for this request
        :return: the saved identity
        """
        req = f"/api/identities"
        saved = self._post_codec(req, timeout, identity)
        return Identity.from_dict(saved)

    def delete_identity(self, identity_id: int,
                        timeout=DEFAULT_TIMEOUT):
        """Deletes the identity with the given ID.

        :param identity_id: The ID of the identity to delete
        :param timeout: The timeout to use for this request
        """
        req = f"/api/identities/{identity_id}"
        self._delete(req, timeout)

    def new_identity_image(self, identity_id: int, class_name: str,
                           storage_id: int,
                           timeout=DEFAULT_TIMEOUT):
        """Saves and encodes an image under the identity with the given ID.

        :param identity_id: Identity to associate the image with
        :param class_name: The type of object this image shows and should be
            encoded for
        :param storage_id: The ID of the image in storage to encode
        :param timeout: The timeout to use for this request
        """
        req = f"/api/identities/{identity_id}/images"
        req_obj = {
            "class_name": class_name,
            "storage_id": storage_id
        }
        encoding = self._post_json(req, timeout, json.dumps(req_obj))
        return Encoding.from_dict(encoding)

    def new_identity_vector(self, identity_id: int, class_name: str,
                            vector: List[float],
                            timeout=DEFAULT_TIMEOUT) -> int:
        """Saves the given vector under the identity with the given ID. In this
        case, a vector is simply a list of one or more numbers that describe
        some object in an image.

        :param identity_id: Identity to associate the vector with
        :param class_name: The type of object this vector describes
        :param vector: The vector to save
        :param timeout: The timeout to use for this request
        :return: The vector ID
        """
        req = f"/api/identities/{identity_id}/vectors"

        encoded_obj = {
            "class_name": class_name,
            "vector": vector
        }
        encoding = self._post_json(req, timeout, json.dumps(encoded_obj))
        return Encoding.from_dict(encoding)
