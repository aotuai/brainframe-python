import json
import logging
import typing
from typing import Any, BinaryIO, Optional, Tuple, Union
from urllib.parse import urlparse

import requests
from requests import Response

from brainframe.api import bf_codecs, bf_errors

DEFAULT_TIMEOUT = 30
"""The default timeout for most requests."""


class BaseStub:
    """A base class for API stubs: Classes that provide methods which call the
    API to provide some functionality. Included are methods to make
    communicating with the API easier.
    """

    _server_url = None
    _credentials = None
    _session_id = None

    def set_url(self, url):
        scheme = urlparse(url).scheme
        if scheme not in ["http", "https"]:
            raise ValueError(f"Invalid URL schema ({scheme}://). Must be "
                             f"either http:// or https://")

        self._server_url = url

    def set_credentials(self, credentials: Optional[Tuple[str, str]]):
        """Start authorizing requests with the given credentials for all future
        requests.

        :param credentials: The username and password in a tuple, or None to
            not use authorization on requests
        """
        self._credentials = credentials

        # Stop using the old session with outdated credentials
        self._session_id = None

    def _get_json(self, api_url, timeout, params=None) -> Tuple[Any, dict]:
        """Send a GET request to the given URL and parse the result as JSON.

        :param api_url: The /api/blah/blah to append to the base_url
        :param timeout: The timeout to use for this request
        :param params: The "query_string" to add to the url. In the format
            of a dict, {"key": "value", ...} key and val must be a string
        :return: The response, parsed with JSON
        """
        resp = self._get(api_url, timeout, params=params)

        if resp.content:
            return json.loads(resp.content), resp.headers
        return None, resp.headers

    def _put_json(self, api_url, timeout, json_data):
        """Send a PUT request to the given URL.

        :param api_url: The /api/blah/blah to append to the base_url
        :param timeout: The timeout to use for this request
        :param json_data: Pre-formatted JSON to send
        :return: The JSON response as a dict, or None if none was sent
        """
        resp = self._put(api_url,
                         timeout,
                         data=json_data,
                         content_type="application/json")

        if resp.content:
            return json.loads(resp.content)
        return None

    def _post_codec(self, api_url, timeout, codec: bf_codecs.Codec):
        """Send a POST request to the given URL.

        :param api_url: The /api/blah/blah to append to the base_url
        :param timeout: The timeout to use for this request
        :param codec: A codec to convert to JSON and send
        :return: The JSON response as a dict, or None if none was sent
        """
        codec_data = codec.to_json()
        resp = self._post(api_url,
                          timeout,
                          data=codec_data.encode("utf-8"),
                          content_type="application/json")

        if resp.content:
            return json.loads(resp.content)
        return None

    def _post_json(self, api_url, timeout, json_data):
        """Send a POST request to the given URL.
        :param api_url: The /api/blah/blah to append to the base_url
        :param timeout: The timeout to use for this request
        :param json_data: Pre-formatted JSON to send
        :return: The JSON response as a dict, or None if none was sent
        """
        resp = self._post(api_url,
                          timeout,
                          data=json_data,
                          content_type="application/json")

        if resp.content:
            return json.loads(resp.content)
        return None

    def _post_multipart(self, api_url, timeout, files):
        """Send a POST request to the given URL.
        :param api_url: The /api/blah/blah to append to the base_url
        :param timeout: The timeout to use for this request
        :param files: A tuple in Requests format for a multipart body
        :return: The JSON response as a dict, or None if none was sent
        """
        resp = self._post(api_url, timeout, files=files)

        if resp.content:
            return json.loads(resp.content)
        return None

    def _patch_json(self, api_url, timeout, json_data):
        """Sends a PATCH request to the given URL.

        :param api_url: The /api/blah/blah to append to the base_url
        :param timeout: The timeout to use for this request
        :param json_data: Pre-formatted JSON to send
        :return: The JSON response as a dict, or None if none was sent
        """
        resp = self._patch(api_url,
                           timeout,
                           data=json_data,
                           content_type="application/json")

        if resp.content:
            return json.loads(resp.content)
        return None

    def _get(self, api_url, timeout, params=None) -> Response:
        """Send a GET request to the given URL, managing authentication and
        error handling, if necessary.

        :param api_url: The /api/blah/blah to append to the base_url
        :param timeout: The timeout to use for this request
        :param params: The "query_string" to add to the url. In the format
            of a dict, {"key": "value", ...} key and val must be a string
        :return: The response object
        """
        request = requests.Request(
            method="GET",
            url=self._full_url(api_url),
            params=params)

        return self._send_authorized(request, timeout)

    def _put(self, api_url,
             timeout,
             data: Union[bytes, str],
             content_type: str) \
            -> Response:
        """Send a PUT request to the given URL, managing authentication and
        error handling, if necessary.

        :param api_url: The /api/blah/blah to append to the base_url
        :param timeout: The timeout to use for this request
        :param data: The data to send
        :param content_type: The content type of the data
        :return: The response object
        """
        headers = None
        if content_type is not None:
            headers = {"content-type": content_type}

        request = requests.Request(
            method="PUT",
            url=self._full_url(api_url),
            data=data,
            headers=headers)

        return self._send_authorized(request, timeout)

    def _post(self, api_url,
              timeout,
              data: Union[bytes, str, BinaryIO] = None,
              content_type: str = None,
              files=None) \
            -> Response:
        """Send a POST request to the given URL, managing authentication and
        error handling, if necessary.

        :param api_url: The /api/blah/blah to append to the base_url
        :param timeout: The timeout to use for this request
        :param data: The data to send
        :param content_type: The content type of the data
        :param files: If provided, the POST request will be a multipart request
        :return: The response object
        """
        headers = None
        if content_type is not None:
            headers = {"content-type": content_type}

        request = requests.Request(
            method="POST",
            url=self._full_url(api_url),
            data=data,
            files=files,
            headers=headers)

        return self._send_authorized(request, timeout)

    def _delete(self, api_url, timeout, params=None) -> Response:
        """Sends a DELETE request to the given URL, managing authentication and
        handling errors, as necessary.

        :param api_url: The /api/blah/blah to append to the base_url
        :param timeout: The timeout to use for this request
        :param params: The "query_string" to add to the URL. Must be a
          str-to-str dict
        :return: The response object
        """
        request = requests.Request(
            method="DELETE",
            url=self._full_url(api_url),
            params=params)

        return self._send_authorized(request, timeout)

    def _patch(self, api_url,
               timeout,
               data: Union[bytes, str] = None,
               content_type: str = None) -> Response:
        """Sends a PATCH request to the given URL, managing authentication and
        handling errors. as necessary.

        :param api_url: The /api/blah/blah to append to the base_url
        :param timeout: The timeout to use for this request
        :param data: The data to send
        :param content_type: The content type of the data
        :return: The response object
        """
        headers = None
        if content_type is not None:
            headers = {"content-type": content_type}

        request = requests.Request(
            method="PATCH",
            url=self._full_url(api_url),
            data=data,
            headers=headers)

        return self._send_authorized(request, timeout)

    def _full_url(self, api_url):
        """Converts an API URL path to a fully qualified URL.

        :param api_url: A URL path in the format /api/blah/blah
        :return: Full URL
        """
        url = "{base_url}{api_url}".format(
            base_url=self._server_url,
            api_url=api_url)
        return url

    def _send_authorized(self, request: requests.Request, timeout) \
            -> Response:
        """Sends the given request, using whatever authorization path that is
        necessary and raising any errors.
        """
        if self._credentials is None:
            # No credentials provided, send the request without any auth
            send_func = self._send_no_auth
        elif self._session_id is None:
            # Authenticate with username and password to get a new session ID
            send_func = self._send_with_credentials
        else:
            # Authenticate with the session ID
            send_func = self._send_with_session_id

        resp = send_func(request, timeout)
        return resp

    def _send_no_auth(self, request: requests.Request, timeout) \
            -> requests.Response:
        """Sends the given request with no authorization."""
        resp = self._perform_request(request, timeout)
        return resp

    def _send_with_credentials(self, request: requests.Request, timeout) \
            -> requests.Response:
        """Sends the given request with HTTP Basic Authorization."""

        request.auth = self._credentials
        resp = self._perform_request(request, timeout)

        if "session_id" in resp.cookies:
            # Update the session ID if we don't already have one
            self._session_id = resp.cookies["session_id"]

        return resp

    def _send_with_session_id(self, request: requests.Request, timeout) \
            -> requests.Response:
        """Sends the given request with the session ID."""
        request.cookies = {"session_id": self._session_id}
        try:
            resp = self._perform_request(request, timeout)
        except bf_errors.InvalidSessionError:
            # The session likely expired. Try again with the username and
            # password to fetch a new session
            request.cookies = None
            return self._send_with_credentials(request, timeout)

        return resp

    def _perform_request(self, *args, **kwargs):
        """Sends a request and handles any errors in the result

        All arguments are passed to BaseStub._send_request
        """
        try:
            resp = self._send_request(*args, **kwargs)
        except requests.exceptions.RequestException as exc:
            raise _make_api_error(exception=exc)

        if not resp.ok:
            raise _make_api_error(resp=resp)

        return resp

    @staticmethod
    def _send_request(request: requests.Request, timeout: int) \
            -> requests.Response:
        """Sends a request to the server. This method is mocked out in unit
        tests.

        :param request: The request to send
        :return: The response data
        """
        prepared = request.prepare()
        return requests.Session().send(prepared, stream=True, timeout=timeout)


@typing.overload
def _make_api_error(exception: Exception) -> bf_errors.BaseAPIError:
    ...


@typing.overload
def _make_api_error(resp: requests.Response) -> bf_errors.BaseAPIError:
    ...


def _make_api_error(resp: requests.Response = None,
                    exception: BaseException = None) \
        -> bf_errors.BaseAPIError:
    """Makes the corresponding error for this response.

    Pass either a requests.Response with a status code, or an exception

    :param resp: The HTTP response to inspect for info
    :param exception: An exception during the request
    :return: An error that can be thrown describing this failure
    """

    server_not_ready_msg = "A network exception occurred while communicating " \
                           "with the BrainFrame server"

    if resp is not None:
        if len(resp.content) == 0:
            description = ("A failure happened but the server did not respond "
                           "with a proper error")
            return bf_errors.UnknownError(description)
        else:
            resp_content = resp.content.decode("utf-8")

            # This is here to catch the nginx error that can occur as the server
            # starts up
            if resp.status_code == 502:
                description = f"{server_not_ready_msg}: {resp_content}"
                return bf_errors.ServerNotReadyError(description)

            try:
                resp_content = json.loads(resp.content)
                kind = resp_content["title"]
                description = resp_content["description"]
            except ValueError:
                # The content of the error was not in the proper format. This
                # might happen if some part of our request handling pipeline
                # failed that doesn't know about our error handling format. Not
                # ideal.
                exc_type = bf_errors.UnknownError
                description = (
                    f"A failure happened, and the response was not in "
                    f"the proper error format: {resp_content}"
                )
            else:
                try:
                    exc_type = bf_errors.kind_to_error_type[kind]
                except KeyError:
                    description = f"Unknown error kind {kind}: {description}"
                    logging.error(description)
                    exc_type = bf_errors.UnknownError

            if exc_type is bf_errors.UnknownError:
                return exc_type(description, resp.status_code)
            else:
                return exc_type(description)

    elif exception is not None:
        if isinstance(exception, requests.exceptions.RequestException):
            exc_type = bf_errors.ServerNotReadyError
            description = server_not_ready_msg
        else:
            exc_type = bf_errors.UnknownError
            description = "An unknown network exception occurred while " \
                          "attempting to communicate with the BrainFrame server"

        new_exc = exc_type(description)
        # This is identical to `raise x from y`, but does not immediately raise
        new_exc.__cause__ = exception
        return new_exc

    else:
        description = f"{_make_api_error.__name__} called without arguments"
        new_exc = ValueError(description)
        if exception is not None:
            new_exc.__cause__ = exception
        raise new_exc
